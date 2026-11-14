#!/usr/bin/env python3
"""
Build Hydrate's unified, app-ready drink database.

Inputs (all in Research/):
  03a-drinks-part-a.json                 Part A research (sodas, juices, dairy, water, smoothies)
  03b-drinks-part-b.json                 Part B research (coffee, tea, energy, sports, plant milk, alcohol, other)
  verification/drink-corrections.json    optional patch list from the verification pass
  verification/drinks-additions.json     optional new entries from the verification pass

Outputs:
  hydrate-drinks.json                    unified database (schema version below)
  hydrate-drinks-report.md               generated build report (stats, warnings, worked credits)

Usage:
  python3 -I Research/tools/build_drink_db.py

The hydration model implemented here mirrors Research/00-decisions.md section 3. The Swift app
must implement the same maths; the `examples` block in the report doubles as a test fixture.
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # Research/
SCHEMA_VERSION = 1

# --------------------------------------------------------------------------------------------
# Hydration model constants (see 00-decisions.md §3; derived from 02-beverage-hydration-model.md)
# --------------------------------------------------------------------------------------------
CAFFEINE_THRESHOLD_MG = 250.0   # per rolling 2-hour window
CAFFEINE_ML_PER_MG = 0.5
CAFFEINE_CAP_ML = 150.0         # per window
ALCOHOL_ML_PER_G = 5.0
ETHANOL_DENSITY = 0.789         # g/mL
LACTOSE_G_PER_100ML = 4.8       # intrinsic milk sugar, not "free sugar" (WHO)
BADGE_SODIUM_MG_PER_100ML = 103.5  # 45 mmol/L Na (BHI evidence threshold) = 45 * 22.99 mg / 10

# Picker taxonomy: research category string -> (pickerCategory id, display name, order)
CATEGORY_MAP = {
    "water":      ("water",      "Water",                 1),
    "coffee":     ("coffee",     "Coffee",                2),
    "tea":        ("tea",        "Tea",                   3),
    "soda":       ("soda",       "Soda & Soft Drinks",    4),
    "juice":      ("juice",      "Juice",                 5),
    "dairy":      ("dairy",      "Milk & Dairy",          6),
    "plant milk": ("plantMilk",  "Plant Milk",            7),
    "sports":     ("sports",     "Sports & Electrolytes", 8),
    "energy":     ("energy",     "Energy Drinks",         9),
    "smoothie":   ("smoothie",   "Smoothies & Shakes",   10),
    "alcohol":    ("alcohol",    "Alcohol",              11),
    "other":      ("other",      "Other",                12),
}

# Plain dairy whose sugar is all lactose (WHO: not a free sugar)
PLAIN_DAIRY_IDS = {"milk_whole", "milk_2pct", "milk_1pct", "milk_skim", "buttermilk", "kefir_plain"}
# Long-lasting badge (high Beverage Hydration Index): plain + flavoured dairy milk, soy drink,
# and electrolyte drinks >= 45 mmol/L sodium. Orange juice is deliberately excluded: its BHI
# advantage was not significant after correcting for water content and was gone by 4 h.
BADGE_SUBCATEGORIES = {("dairy", "milk"), ("dairy", "flavored milk")}
BADGE_IDS = {"plant_soy_unsweetened"}

# Quick picks for the slots Part A left open (ranks 3, 4, 9, 10)
PART_B_QUICK_PICKS = {"coffee_brewed": 3, "tea_black": 4, "sports_gatorade": 9, "energy_red_bull": 10}

NUTRIENTS = ["waterG", "energyKcal", "sugarG", "carbsG", "proteinG", "fatG",
             "sodiumMg", "potassiumMg", "caffeineMg", "alcoholG"]

warnings: list[str] = []


def load(name: str, required: bool = True):
    path = ROOT / name
    if not path.exists():
        if required:
            sys.exit(f"missing input: {path}")
        return None
    with path.open() as f:
        return json.load(f)


def set_path(entry: dict, dotted: str, value):
    parts = dotted.split(".")
    node = entry
    for p in parts[:-1]:
        node = node.setdefault(p, {})
    node[parts[-1]] = value


def get_path(entry: dict, dotted: str):
    node = entry
    for p in dotted.split("."):
        if not isinstance(node, dict) or p not in node:
            return None
        node = node[p]
    return node


def apply_corrections(entries: dict[str, dict], patches: list[dict]) -> list[dict]:
    log = []
    for patch in patches:
        pid = patch.get("id")
        if pid not in entries:
            warnings.append(f"correction targets unknown id '{pid}' (skipped)")
            continue
        if patch.get("remove"):
            del entries[pid]
            log.append({"id": pid, "action": "removed", "reason": patch.get("reason", "")})
            continue
        for path, value in (patch.get("set") or {}).items():
            old = get_path(entries[pid], path)
            set_path(entries[pid], path, value)
            log.append({"id": pid, "action": "set", "field": path, "old": old, "new": value,
                        "reason": patch.get("reason", "")})
        if patch.get("source") and "source" not in (patch.get("set") or {}):
            entries[pid].setdefault("corrections", []).append(
                {"source": patch["source"], "reason": patch.get("reason", "")})
    return log


def num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def estimate_water(entry: dict, peers: dict) -> tuple[float | None, str]:
    """Water (mL per 100 mL) when the source gives none. Returns (value, method)."""
    p = entry["per100mL"]
    carbs = num(p.get("carbsG"))
    if carbs is None:
        carbs = num(p.get("sugarG"))
    if carbs is None and num(p.get("energyKcal")) is not None:
        prot = num(p.get("proteinG")) or 0
        fat = num(p.get("fatG")) or 0
        carbs = max(0.0, (p["energyKcal"] - 4 * prot - 9 * fat - 7 * (num(p.get("alcoholG")) or 0)) / 4)
    if carbs is None and (num(p.get("alcoholG")) or 0) > 0:
        carbs = 0.0  # spirit-like label with only ABV known (e.g. soju): treat solids as negligible
    if carbs is not None:
        solids = carbs + (num(p.get("proteinG")) or 0) + (num(p.get("fatG")) or 0)
        minerals = ((num(p.get("sodiumMg")) or 0) * 2.54 + (num(p.get("potassiumMg")) or 0) * 1.9) / 1000
        solids += minerals
        alcohol_g = num(p.get("alcoholG")) or 0
        # density of a dilute aqueous solution: ~ +0.0038 g/mL per g solids/100 mL; ethanol lowers it
        density = 1.0 + 0.0038 * solids - 0.0013 * alcohol_g
        water = 100 * density - solids - alcohol_g
        return round(min(water, 99.9), 1), "estimated from label solids"
    key = (entry["category"], entry["subcategory"])
    pool = peers.get(key) or peers.get((entry["category"], None)) or []
    if pool:
        return round(statistics.median(pool), 1), f"proxy: median of {key[0]}/{key[1]} peers"
    return None, "unknown"


def credit(volume_ml: float, d: dict, prior_caffeine_mg: float = 0.0, prior_penalty_ml: float = 0.0) -> dict:
    """Python mirror of the app's hydration-credit function (00-decisions.md §3.2)."""
    h = d["hydration"]
    water = volume_ml * h["waterMLPer100mL"] / 100 * h["hydrationFactor"]
    this_mg = volume_ml * (d["per100mL"].get("caffeineMg") or 0) / 100
    over_before = max(0.0, prior_caffeine_mg - CAFFEINE_THRESHOLD_MG)
    over_after = max(0.0, prior_caffeine_mg + this_mg - CAFFEINE_THRESHOLD_MG)
    caf_pen = min((over_after - over_before) * CAFFEINE_ML_PER_MG, max(0.0, CAFFEINE_CAP_ML - prior_penalty_ml))
    ethanol_g = volume_ml * (d["per100mL"].get("alcoholG") or 0) / 100
    alc_pen = ethanol_g * ALCOHOL_ML_PER_G
    raw = max(0.0, water - caf_pen - alc_pen)
    # Store the exact credit (sums stay exact); round only for display, never above the water content.
    display = round(raw / 5) * 5
    if display > water:
        display = int(water // 5) * 5
    return {"volumeML": volume_ml, "waterML": round(water, 1), "caffeineMg": round(this_mg, 1),
            "caffeinePenaltyML": round(caf_pen, 1), "ethanolG": round(ethanol_g, 1),
            "alcoholPenaltyML": round(alc_pen, 1), "creditML": round(raw, 1), "displayCreditML": display}


def main():
    part_a = load("03a-drinks-part-a.json")
    part_b = load("03b-drinks-part-b.json")
    additions = load("verification/drinks-additions.json", required=False) or []
    corrections = load("verification/drink-corrections.json", required=False) or []

    entries: dict[str, dict] = {}
    for origin, items in (("part-a", part_a), ("part-b", part_b), ("verification-additions", additions)):
        for e in items:
            if e["id"] in entries:
                warnings.append(f"duplicate id '{e['id']}' in {origin} (kept first)")
                continue
            e = json.loads(json.dumps(e))  # deep copy
            e["origin"] = origin
            entries[e["id"]] = e

    correction_log = apply_corrections(entries, corrections)

    # Normalise nutrient blocks
    for e in entries.values():
        p = e.setdefault("per100mL", {})
        for k in NUTRIENTS:
            p.setdefault(k, None)
        if e["category"] != "alcohol" and p["alcoholG"] is None and e["id"] != "other_kombucha":
            p["alcoholG"] = 0.0
        if p["alcoholG"] is not None and e.get("abvPercent") is None and p["alcoholG"] > 0:
            e["abvPercent"] = round(p["alcoholG"] / ETHANOL_DENSITY, 1)
        e.setdefault("abvPercent", None)
        e.setdefault("caffeineRangePer100mL", None)
        e.setdefault("region", None)
        e.setdefault("brandExamples", [])
        e.setdefault("variants", [])
        servings = sorted(set((e.get("commonServingsML") or []) + [e["defaultServingML"]]))
        e["commonServingsML"] = servings
        if e["category"] not in CATEGORY_MAP:
            warnings.append(f"{e['id']}: unknown category '{e['category']}' mapped to Other")
            e["category"] = "other"

    # Peer water values for proxies
    peers: dict = defaultdict(list)
    for e in entries.values():
        w = num(e["per100mL"]["waterG"])
        if w is not None:
            peers[(e["category"], e["subcategory"])].append(w)
            peers[(e["category"], None)].append(w)

    # Derived hydration block
    for e in entries.values():
        p = e["per100mL"]
        water = num(p["waterG"])
        method = "source"
        if water is None:
            water, method = estimate_water(e, peers)
            if water is None:
                warnings.append(f"{e['id']}: no water value and no way to estimate it")
                water = 0.0
        if water > 100.5:
            warnings.append(f"{e['id']}: water {water} mL/100 mL is impossible")
        sugar = num(p["sugarG"])
        if sugar is None and e["category"] == "soda" and num(p["carbsG"]) is not None:
            sugar = p["carbsG"]  # soda carbohydrate is effectively all sugar
        if e["id"] in PLAIN_DAIRY_IDS:
            free_sugar = 0.0
        elif e["category"] == "dairy" and sugar is not None:
            free_sugar = round(max(0.0, sugar - LACTOSE_G_PER_100ML), 1)
        else:
            free_sugar = sugar
        sodium = num(p["sodiumMg"])
        badge = ((e["category"], e["subcategory"]) in BADGE_SUBCATEGORIES or e["id"] in BADGE_IDS
                 or (e["category"] == "sports" and sodium is not None and sodium >= BADGE_SODIUM_MG_PER_100ML))
        e["hydration"] = {
            "waterMLPer100mL": water,
            "waterSource": method,
            "hydrationFactor": 1.0,
            "longLastingBadge": bool(badge),
            "freeSugarGPer100mL": free_sugar,
            "caffeineKnown": p["caffeineMg"] is not None,
        }
        e.pop("hydrationFactor", None)
        e["defaultServing"] = credit(e["defaultServingML"], e)
        cat_id, cat_name, cat_order = CATEGORY_MAP[e["category"]]
        e["pickerCategory"] = cat_id

    # Search terms: name words, brands, variants, subcategory, plus hand-kept aliases
    alias_path = ROOT / "tools" / "drink-aliases.json"
    aliases = json.loads(alias_path.read_text()) if alias_path.exists() else {}
    known_ids = set(entries)
    for key in aliases:
        if key.startswith("id:") and key[3:] not in known_ids:
            warnings.append(f"alias key '{key}' matches no drink")
    for e in entries.values():
        terms: list[str] = []

        def add(t):
            t = str(t).strip().lower()
            if t and t not in terms:
                terms.append(t)

        add(e["name"])
        for b in e.get("brandExamples") or []:
            add(b)
        for v in e.get("variants") or []:
            add(v)
        add(e["subcategory"])
        add(CATEGORY_MAP[e["category"]][1])
        for k in (f"category:{e['category']}", f"subcategory:{e['category']}/{e['subcategory']}", f"id:{e['id']}"):
            for t in aliases.get(k, []):
                add(t)
        e["searchTerms"] = terms

    # Quick picks
    for pid, rank in PART_B_QUICK_PICKS.items():
        if pid in entries:
            entries[pid]["quickPick"] = True
            entries[pid]["quickPickRank"] = rank
        else:
            warnings.append(f"quick pick '{pid}' not found")
    for e in entries.values():
        e.setdefault("quickPick", False)
        e.setdefault("quickPickRank", None)
    ranks = Counter(e["quickPickRank"] for e in entries.values() if e["quickPick"])
    for r, n in ranks.items():
        if n > 1:
            warnings.append(f"quick-pick rank {r} used {n} times")

    # Validation
    for e in entries.values():
        if not e.get("defaultServingML") or e["defaultServingML"] <= 0:
            warnings.append(f"{e['id']}: bad defaultServingML")
        for k, v in e["per100mL"].items():
            if v is not None and (not isinstance(v, (int, float)) or v < 0):
                warnings.append(f"{e['id']}: bad {k}={v!r}")
        if not (e.get("source") or {}).get("name"):
            warnings.append(f"{e['id']}: missing source name")

    order = {k: v[2] for k, v in CATEGORY_MAP.items()}
    ordered = sorted(entries.values(), key=lambda e: (order[e["category"]], e["subcategory"], e["name"]))
    key_order = ["id", "name", "category", "pickerCategory", "subcategory", "variants", "region",
                 "defaultServingML", "commonServingsML", "per100mL", "caffeineRangePer100mL", "abvPercent",
                 "hydration", "defaultServing", "densityGPerML", "quickPick", "quickPickRank", "searchTerms",
                 "brandExamples",
                 "confidence", "source", "corrections", "notes", "origin"]
    drinks = [{k: e[k] for k in key_order if k in e} | {k: v for k, v in e.items() if k not in key_order}
              for e in ordered]

    out = {
        "format": "hydrate-drink-database",
        "schemaVersion": SCHEMA_VERSION,
        "builtOn": date.today().isoformat(),
        "units": {"per100mL": "nutrients per 100 mL of drink", "waterMLPer100mL": "mL of water per 100 mL"},
        "model": {
            "caffeineThresholdMg": CAFFEINE_THRESHOLD_MG, "caffeineWindowHours": 2,
            "caffeineMLPerMg": CAFFEINE_ML_PER_MG, "caffeineCapML": CAFFEINE_CAP_ML,
            "alcoholMLPerGram": ALCOHOL_ML_PER_G, "ethanolDensity": ETHANOL_DENSITY,
            "creditRoundingML": 5,
        },
        "categories": [{"id": v[0], "name": v[1], "order": v[2]} for v in sorted(CATEGORY_MAP.values(), key=lambda x: x[2])],
        "drinks": drinks,
    }
    (ROOT / "hydrate-drinks.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    write_report(drinks, correction_log, additions)
    print(f"built {len(drinks)} drinks, {len(correction_log)} corrections applied, {len(warnings)} warnings")
    for w in warnings:
        print("  WARN", w)


def write_report(drinks, correction_log, additions):
    by_cat = Counter(d["pickerCategory"] for d in drinks)
    conf = Counter(d.get("confidence") for d in drinks)
    nulls = Counter(k for d in drinks for k, v in d["per100mL"].items() if v is None)
    est = [d for d in drinks if d["hydration"]["waterSource"] != "source"]
    unknown_caf = [d["id"] for d in drinks if d["per100mL"]["caffeineMg"] is None]
    lines = [
        "# Hydrate drink database: build report",
        "",
        f"Generated by `tools/build_drink_db.py` on {date.today().isoformat()}. Do not edit by hand; rerun the script.",
        "",
        f"- **Drinks:** {len(drinks)} ({len(additions)} from the verification additions)",
        f"- **Corrections applied:** {len(correction_log)}",
        f"- **Confidence:** " + ", ".join(f"{k} {v}" for k, v in conf.most_common()),
        f"- **Long-lasting badge:** {sum(d['hydration']['longLastingBadge'] for d in drinks)} drinks",
        f"- **Warnings:** {len(warnings)}",
        "",
        "## Drinks per picker category",
        "",
        "| Category | Drinks |",
        "|---|---|",
    ]
    lines += [f"| {c} | {n} |" for c, n in sorted(by_cat.items(), key=lambda x: -x[1])]
    lines += ["", "## Unknown (null) nutrient fields", "", "| Field | Count |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in nulls.most_common()]
    lines += ["", f"Drinks with unknown caffeine ({len(unknown_caf)}): " + (", ".join(f"`{i}`" for i in unknown_caf) or "none"),
              "", "## Water values estimated rather than sourced", "",
              "| id | mL water / 100 mL | method |", "|---|---|---|"]
    lines += [f"| `{d['id']}` | {d['hydration']['waterMLPer100mL']} | {d['hydration']['waterSource']} |" for d in est]
    lines += ["", "## Credit at default serving (test fixture for the Swift implementation)", "",
              "| id | serving mL | water mL | caffeine mg | penalties mL | credit mL | % |", "|---|---|---|---|---|---|---|"]
    for d in drinks:
        s = d["defaultServing"]
        pct = round(100 * s["creditML"] / s["volumeML"]) if s["volumeML"] else 0
        lines.append(f"| `{d['id']}` | {s['volumeML']:g} | {s['waterML']:g} | {s['caffeineMg']:g} | "
                     f"{s['caffeinePenaltyML'] + s['alcoholPenaltyML']:g} | {s['creditML']:g} (shows {s['displayCreditML']}) | {pct} |")
    if correction_log:
        lines += ["", "## Corrections applied", "", "| id | action | field | old | new |", "|---|---|---|---|---|"]
        for c in correction_log:
            lines.append(f"| `{c['id']}` | {c['action']} | {c.get('field', '')} | {json.dumps(c.get('old'))[:40]} | "
                         f"{json.dumps(c.get('new'))[:40]} |")
    lines += ["", "## Warnings", ""] + ([f"- {w}" for w in warnings] or ["- none"])
    (ROOT / "hydrate-drinks-report.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
