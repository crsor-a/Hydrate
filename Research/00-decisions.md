# Hydrate: Decisions

*The one answer for every question the research raised. This is the reference the app is built from. Research notes (01–05) and the verification pass (`verification/`) hold the evidence; this file holds the verdicts, with section links back to the evidence. Where I overruled a research note, §15 says so and why.*

*Last updated: 2026-11-14 · Status: **FINAL for v1** (all sections verified; see `verification/`)*

---

## 1. Product rules (settled with the owner)

| Topic | Decision |
|---|---|
| Audience | Personal app, shared with friends, later open source. Not for the App Store. Built on a **free Apple ID Personal Team**. No paid-account features. |
| Streak day | A day counts only when **credit ≥ 100% of that day's goal**. No streak freezes. |
| Backfilled days | Logging a past day (from Calendar) completes the record but **never** counts toward or repairs a streak. Each log stores `loggedAt` (real time) as well as `timestamp` (when it was drunk); a log counts toward a streak only if `loggedAt` falls on the same calendar day as `timestamp`, or within a 2-hour grace window after midnight for late-night entries. |
| Goal change mid-streak | The new goal applies from the moment it changes. Past days keep the goal they had (stored per day). |
| Day boundary | Local midnight, using the calendar day at the time the drink was drunk (`dayKey = yyyymmdd`). Time-zone travel never moves past drinks to another day. |
| Units | Metric or US customary, defaulting to the device locale. All storage is in mL. |
| Notifications | Local only (no push server). |
| Live Activities | None. |
| Widgets, Control Center, Siri/Shortcuts | Yes. A first-class part of v1. |
| Disclaimer | "About & Sources" section in Settings next to Changelog, with every citation, plus one line of fine print on the onboarding goal screen. |

---

## 2. Daily goal

*Verified against the authors' accepted manuscript of Yamada et al., Science 2022 (eq. 1 printed in full). Every coefficient matches; the paper's four worked examples reproduce exactly. Evidence: note 01 §6 and `verification/01-goal-formula-verification.md` (§7 has the implementation-ready pseudocode; implement that verbatim, minus altitude and child mode).*

```
WT        = 1076·PAL + 14.34·w + 374.9·sexC − 0.3529·ageEff² + 24.78·ageEff − 297.22
            // Yamada eq. 1 at 15 °C, 50 % RH, sea level, non-athlete, high-HDI country
base      = 0.68 · WT  (+300 pregnant | +700 breastfeeding)      // 0.85 turnover→intake × 0.80 drinks share
today     = base + heat + workouts                               // add-ons skipped if the medical gate is on
goal      = round50( clamp(today, floor, ceiling) )               // or nearest 4 fl oz in US units
```

| Input | Rule |
|---|---|
| `sexC` | male 1, female 0, unspecified 0.5 |
| `ageEff` | age clamped to 14–35 (the equation peaks at 35.1; older adults keep the peak value, because thirst blunts with age) |
| `w` | 7-day median weight (pre-pregnancy weight if pregnant). If height is known, weight above the BMI-30 weight counts at **0.65** (soft cap). Then clamped to 35–150 kg |
| `PAL` | From the 14-day mean of daily steps: < 5,000 → 1.40 · 5,000–7,499 → 1.60 · 7,500–12,499 → 1.75 · ≥ 12,500 → 2.05. iPhone-only steps (no Watch) never classify below 1.60. If weekly exercise minutes also exist (< 60 / 60–149 / 150–299 / ≥ 300), use the **higher** tier. No Health data → one onboarding question; skipped → 1.60. Recomputed weekly with hysteresis |
| Heat | Manual toggle: "Hot day" = 25 °C mean (+≈470 mL), "Very hot day" = 30 °C mean (+≈820 mL). Formula: 0.85 × ((1.865T² − 19.66T) − 124.65), cap +1,000. T is the **24-hour mean**, never the daily high |
| Workouts | From HealthKit, ≥ 20 min each: 400 mL/h moderate, 600 mL/h vigorous, +200 mL/h on hot days, cap +1,500 |
| Floor | women 1,600 · men 2,000 · unspecified 1,800 · pregnant 1,840 · breastfeeding 2,160 |
| Ceiling | 4,500 (18+) · 4,000 (14–17) |

**Worked results:** man, 30, 70 kg, active → **2,300 mL** (3,750 on a 30 °C day with a 1-hour workout) · woman, 75, 58 kg, inactive → **1,700** · man, 50, 110 kg, 180 cm, inactive → **2,400** · woman, 30, 62 kg, no Health data → **1,850** · pregnant woman, 30, 64 kg → **2,200** (2,600 breastfeeding).

**Why 2,300 and not the US 3.0 L guideline:** the US figure is the median *self-reported* intake of US men (who average about 90 kg), and self-report runs 20–25% above isotope-measured intake. The formula matches isotope-measured US intake to within 2–6% once body size is accounted for.

- **No altitude, no weather API:** see §14.
- **Two numbers:** *base goal* (profile only; the long-term chart) and *today's goal* (base + heat + workouts; the ring).
- **History:** every base-goal change writes a dated `GoalSnapshot` with the inputs and `goalAlgorithmVersion`. History is never recomputed.
- **Manual override:** 1,000–6,000 mL, with a confirmation note above 4,500 mL.
- **Medical gate:** onboarding asks about fluid restriction, heart failure, advanced kidney disease/dialysis, cirrhosis, prior low blood sodium. If yes, the goal shows "check with your clinician", the user sets their own target, and automatic add-ons switch off. Kidney stones flip the other way (a "stone prevention" target of ≥3 L).
- **Altitude:** dropped from v1 (low confidence, and few users need it).
- **Children:** ages under 14 are not supported in v1. (Hydrate is a personal app; the research's child table mode stays in note 01 §6.3 if ever needed.)

---

## 3. Hydration credit (how much each drink counts)

### 3.1 The rule

**A drink counts for the water it contains, minus two evidence-based diuretic effects, never below zero.** Evidence: note 02 §1–§8.

```
waterML        = volumeML × waterMLPer100mL / 100 × hydrationFactor     // factor = 1.0 for all drinks in v1
caffeinePenalty = 0.5 mL per mg of caffeine above 250 mg in the rolling 2 h window, capped at 150 mL per window
alcoholPenalty  = 5 mL per gram of ethanol                              // grams = volumeML × ABV × 0.789
creditML        = max(0, waterML − caffeinePenalty − alcoholPenalty)       // stored exactly
displayCredit   = round5(creditML), or floor5(waterML) if that would exceed the water content
```

- **Store exact, display rounded.** Each log stores the exact credit, so a day's total never accumulates rounding error; the UI shows the nearest 5 mL. (The audit caught a 473 mL energy drink whose rounded credit would have exceeded its water content.)

- **Water is measured by volume, not weight.** The database stores mL of water per 100 mL of drink (computed from USDA grams per 100 g × density). This removes the up-to-4% undercount for sugary drinks that note 02 §6 flagged. Example: 355 mL cola = 330 mL water, not 315.
- **Unknown caffeine** (a null in the database) adds no penalty, but the drink sheet says "caffeine unknown". Never "caffeine-free".
- **The goal ring, reminders and streaks use credit.** Every log row shows both numbers: "355 mL · counts as 330 mL".
- **Setting:** "Count drinks by: Hydration value (default) / Full volume".
- **Spirits floor at 0.** A neat shot adds nothing and never subtracts from other drinks.

### 3.2 The long-lasting badge

Drinks with a proven Beverage Hydration Index advantage get a small badge and the line "May help you stay hydrated longer". They do **not** get extra credit.

- **Badge:** plain and flavored dairy milk, unsweetened soy drink, and electrolyte drinks with ≥ 45 mmol/L sodium (≥ 103.5 mg/100 mL: Pedialyte, WHO ORS, LMNT).
- **No badge:** orange juice (its advantage disappeared after correcting for water content and by 4 hours), regular sports drinks (inconsistent results).

### 3.3 Health facts on each drink

Shown on the drink sheet, separate from hydration, with neutral wording:

- **Free sugar** against the WHO references (25 g and 50 g/day). Lactose in plain milk doesn't count; flavored milk counts only the added sugar.
- **Caffeine** against 400 mg/day and 200 mg per serving for adults. 200 mg/day and 3 mg/kg/day references appear only if the profile says pregnant or under 18.
- **Alcohol** in grams and standard drinks (US 14 g by default; UK 8 g units by locale).
- **Sodium** for electrolyte drinks.

### 3.4 Worked results (generated by the build script; full table in `hydrate-drinks-report.md`)

| Drink | Logged | Counts as |
|---|---|---|
| Cola | 355 mL | 330 mL |
| Whole milk | 237 mL | 215 mL + badge |
| Cold brew (≈205 mg) | 473 mL | 470 mL |
| Bang (300 mg) | 473 mL | 445 mL |
| Gatorade | 591 mL | 565 mL |
| Red Bull | 250 mL | 230 mL |
| Bubble tea (≈150 mg) | 473 mL | 420 mL |
| Beer, 5% | 355 mL | 260 mL |
| Red wine | 148 mL | 50 mL |
| Spirits, 40% | 44 mL | 0 mL |

---

## 4. Drink database

- **File:** `Research/hydrate-drinks.json`, built by `Research/tools/build_drink_db.py` from the research files plus the verification patches (101 field corrections, 56 additions) and the alias list `tools/drink-aliases.json`. The app bundles it read-only. Rebuild with `python3 -I Research/tools/build_drink_db.py`; the build report (`hydrate-drinks-report.md`) lists every estimate, null and correction.
- **Contents (v1):** 229 drinks: soda 41, alcohol 35, juice 26, coffee 23, tea 20, sports & electrolytes 17, milk & dairy 16, energy 15, plant milk 11, water 10, smoothies & shakes 8, other 7. Confidence: 114 high, 105 medium, 10 low. Only 3 drinks have unknown caffeine (bottled Thai iced tea, protein water, hard kombucha).
- **Water for label-only drinks** (energy, sports, brand RTDs; 47 drinks) is estimated from label solids, and each is marked `waterSource: "estimated from label solids"`. For these near-water drinks, the estimate's error (≈1%) is far smaller than brand-to-brand variation.
- **Null means unknown, never zero.** The UI must show "unknown" rather than 0.
- **Region:** brand entries carry `region` (US/UK). The picker shows the device-locale version first.
- **Taxonomy:** 12 picker categories (Water, Coffee, Tea, Soda & Soft Drinks, Juice, Milk & Dairy, Plant Milk, Sports & Electrolytes, Energy Drinks, Smoothies & Shakes, Alcohol, Other) → subcategories → variant chips (regular / diet / zero sugar / caffeine-free / decaf …). Brands live inside subcategories, not at the top level.
- **Search in the log sheet:** a search field at the top of the log sheet (`.searchable` inside the sheet's `NavigationStack`). When empty, the sheet shows quick picks, then recents, then categories. Search matches name, brand, subcategory, variant and **aliases** (e.g. "coke" → Coca-Cola, "pop"/"fizzy drink" → soda, "boba" → bubble tea, "OJ" → orange juice). Results rank exact and prefix matches first, then the user's own history, then everything else. No results → "Add custom drink '…'". The build script will generate a `searchTerms` array per drink from these fields plus a hand-kept alias list.
- **Quick picks:** 12 defaults (water, sparkling water, brewed coffee, black tea, 2% milk, orange juice, cola, diet cola, Gatorade, Red Bull, fruit smoothie, protein shake). After a week, the app replaces them with the user's own most-logged drinks.
- **Custom drinks:** same schema as the database. Ask for volume, category, and optionally caffeine per serving, sugar, kcal, ABV, sodium. "Start from…" an existing drink. Blank = unknown.
- **Add-ins:** extra espresso shot (+64 mg caffeine, +30 mL), sugar (4.2 g/tsp), honey (5.7 g sugar/tsp), syrup pump (≈5 g sugar), milk splash (30 mL of the chosen milk entry). Add-ins add volume too.
- **Espresso drinks** get a "shots" stepper; caffeine follows shots, not cup size.
- **Iced drinks:** see §5.
- **Tablets and sticks** (Nuun, LMNT, Liquid I.V.) log per tablet or stick, dissolved in a chosen water volume.
- **Formulas change.** Brand entries (Monster, Prime, Nuun, Powerade) get a yearly recheck; the changelog notes database updates. Logged history keeps its frozen values.

---

## 5. Logging presets and estimates

*Evidence: note 04 and `verification/04-equivalencies-verification.md`. Machine-readable bottle catalog, chain cups and constants: `verification/equivalencies.json`.*

- **Quick-add presets:** Sip 20 mL · Glass 250 mL (Cup 237 mL in US units) · Mug 350 mL · Bottle 500 mL · Large bottle 750 mL (591 mL in US units) · **My bottle**.
- **My bottle:** picked from a 51-bottle catalog (Stanley, Hydro Flask, Nalgene, Owala, YETI, CamelBak, Contigo, S'well, LARQ, Simple Modern, Ello, Brita), stored as exact mL from nominal fl oz (metric brands keep their labelled mL), or entered by hand. A "how full?" slider (¼ steps) for partial bottles.
- **Chain cups:** Starbucks Short 237 / Tall 355 / Grande 473 / Venti hot 591 / Venti iced 710 / Trenta 887 mL; McDonald's US Small 473 / Medium 621 / Large 887 mL.
- **Fountain:** "seconds drinking" picker (3 s, 5 s, 10 s, custom) × **8 mL/s**. That's about a third of a typical 25.7 mL/s stream, the share studies find people actually catch. Copy: *"We count about 8 mL for each second at a fountain, roughly a third of what the spout puts out. Measure your fountain once for a closer number."*
  - **Measure your fountain (optional):** hold a bottle under the stream for a 5-second countdown, enter what you collected; rate = clamp(0.33 × mL ÷ 5, 4, 15) mL/s. Saved per named fountain (e.g. "Work", "Gym").
  - **No measurement:** stream-strength picker: weak 6 · normal 8 · strong 11 mL/s.
- **Bottle-filler station:** log by bottle and how full it got (filling is fast and visible; no timing needed).
- **Iced drinks:** "With ice?" appears only for cold cups. Liquid fraction **0.75** by default (Coca-Cola's foodservice standard is ⅓ ice); light ice 0.85, extra ice 0.6, "I drank the melted ice too" 1.0. Shown as "about".
- **Reorderable presets** (iOS 27 `.reorderable()`).

---

## 6. Equivalency card

*Data: `verification/equivalencies.json` (53 items, every volume sourced, every SF Symbol name checked against Apple's own symbol database on macOS 27.2).*

- **Ladder:** 53 comparisons from a sip (0.02 L) to the Amazon's flow per second. Kinds: practical (cans, bathtubs, hot tubs, cement trucks), fun (elephants, blue-whale gulps, Old Faithful), flow ("Niagara would pour that in 7 ms"). No two neighbors below 10,000 L are more than 2.7× apart, so every user, from day one to year ten, has a comparison close to their total.
- **Selection:** each day the card shows one practical comparison, one fun one and the next milestone. Items score best when the ratio reads naturally (multiples from 1.5× to 50×, peaking near 4×; or "X% of the way" from 10% to 95%). A "you just passed a bathtub" celebration goes first when a milestone was crossed since the last visit. Rotates daily (seeded by date), never repeats an item within 3 days. Flow items appear once the total passes 2,832 L (1 ms of Niagara).
- **Honesty:** items with a range (bathtub 136–265 L, hot tub 640–1,990 L, blood, body water, Old Faithful) say "about". Pints localize (US 473 / UK 568 mL).
- **Icons:** stand-ins where no SF Symbol exists (can, whale, camel, geyser, keg). A custom whale symbol is a nice-to-have.
- **Lifetime total uses credit**, the same number as the rings.

---

## 7. Apple Health

- **Source of truth:** Hydrate's own store. HealthKit gets a **one-way push**; there is no two-way sync.
- **What gets written per drink:** `dietaryWater` = the drink's **water content** (not the credit; Health records what you consumed, and the credit is Hydrate's interpretation), plus `dietaryCaffeine` and `dietarySugar` when known and > 0. Metadata: `HKMetadataKeySyncIdentifier` = `<log UUID>.<water|caffeine|sugar>`, `HKMetadataKeySyncVersion`, `HKMetadataKeyFoodType` = drink name, and custom keys for drink id and logged volume. No food correlations.
- **Edits** bump `syncVersion` and re-save (HealthKit replaces the lower version). **Deletes** remove our own samples by sync identifier. If an edit drops caffeine to 0, the caffeine sample is deleted, not set to 0.
- **Outbox:** each log has `healthState` (pending / synced / pendingDelete / failed). Widgets and intents write to the store only; the app drains the outbox on foreground, after each in-app log, and in background refresh.
- **Reads:** body mass (7-day median), height, date of birth, biological sex, daily steps (14-day mean), exercise minutes, workouts (today's add-on).
- **Other apps' water:** opt-in, read-only mirror (Apple Watch, other trackers), excluding Hydrate's own source. Shown as "From Health" and counted in the day total. Per-source exclusion to avoid double counting.
- **Permissions:** requested in onboarding, in context. Read denial is invisible, so copy says "No weight found in Health", never "Permission denied".
- **Sync history:** Hydrate's own log of pushes and failures, plus the anchored-query history for imports.
- **Background delivery:** not relied on (free-team entitlement unknown). Foreground refresh is the baseline.

---

## 8. Platform, data and backup

- **Signing for open source:** `Config/Local.xcconfig` (git-ignored, copied from a checked-in template) holds `DEVELOPMENT_TEAM`, the bundle-ID prefix and the App Group ID. The group ID reaches code through an Info.plist key.
- **Store:** SwiftData in the App Group container, `cloudKitDatabase: .none`, `VersionedSchema` + `SchemaMigrationPlan` from day one, defaults on every property.
- **Models (v1):** `DrinkLog` (id, timestamp, loggedAt, dayKey, drinkId, drinkName, volumeML, waterML, creditML, caffeineMg?, sugarG?, ethanolG?, source, syncVersion, healthState, deletedAt?), `GoalSnapshot`, `DailyGoal` (one per dayKey, frozen), `Profile`, `DrinkPreset`, `CustomDrink`, `ExternalWaterSample`, `StreakGoal`, `HealthSyncEvent`. Daily totals are computed, never stored.
- **Log values are frozen at log time.** A later database update never rewrites history.
- **Backup:** versioned JSON export/import (`{"format":"hydrate-backup","version":1,…}`), idempotent by log id, plus CSV export. Uses the `Transferable` `fileExporter(item:)` API (the `FileDocument` overload is deprecated in the 27.3 SDK). The file picker can save to iCloud Drive with no entitlement. Optional weekly "back up now" reminder.
- **No iCloud sync.** If the owner ever joins the paid program, the models already follow CloudKit's rules, except `#Unique`, which would need removing.
- **7-day profile expiry:** Settings shows "Installed … · re-run from Xcode by …".
- **Reset:** "Delete all data" asks for confirmation, offers an export first, and also deletes Hydrate's own Health samples if the user ticks that.

---

## 9. Navigation and Liquid Glass

- **Tab bar:** one glass pill with Home, Calendar, Streak, plus a set-apart **"+" tab using `Tab(role: .prominent)`** (iOS 27). Its selection is intercepted to present the log sheet instead of switching tabs. This bends the HIG's "tabs are for navigation" rule on purpose; the owner chose it, and it's the pattern Apple itself demoed for a cart tab.
- **Log sheet:** system glass sheet with detents, zooming out of the "+" button (`matchedTransitionSource` + `.navigationTransition(.zoom)`).
- **Settings:** a top-right toolbar button on Home that opens a sheet.
- **Glass only on the control layer.** Content (the hero, cards, charts) uses standard materials and fills, per the HIG.
- **`tabBarMinimizeBehavior(.onScrollDown)`** on long scrolling pages.

---

## 10. Notifications

- **Smart reminders:** recomputed on every log and on foreground. Skipped when the user is ahead of their pro-rated pace; only inside the wake window (default 8:00–21:00); never more than one per 60 minutes.
- **"Streak at risk"** at a user-chosen time (default 20:00) if credit < goal. Cancelled as soon as the goal is met.
- **"Update your weight"** every 4 weeks, only when Health isn't providing weight.
- **Weekly backup reminder** (optional).
- **Notification actions:** "+250 mL" (or the user's default preset) and "Snooze 1 h". Logging from the notification doesn't open the app.
- Scheduled 1–2 days ahead and topped up on app open and in background refresh, staying under the 64-pending limit.

---

## 11. Widgets, Control Center and Siri

- **One `LogDrinkIntent`** (drink + serving as `AppEnum`s, optional mL) powers widget buttons, the Control Center control, App Shortcuts phrases, notification actions and, later, a Siri AI tool (`@AppIntent(.tool)`, iOS 27.3).
- **Widgets:** Small (ring + "+"), Medium (ring + 3 preset buttons), Large (ring + week dots + streak), Lock Screen circular / rectangular / inline, StandBy. All support tinted and clear Home Screen modes (`widgetAccentable`, `widgetRenderingMode`).
- **Control:** "Log Water" Control Center button (default preset), with a configurable variant.
- **App Shortcuts phrases:** "Log a glass of water in Hydrate", "Log [serving] of [drink] in Hydrate", "How much have I drunk in Hydrate".
- **Intent process:** writes to the store first, then pushes to Health if write access is authorized, else leaves it in the outbox.

---

## 12. Safety

- Never prompt more than about **1 L in any 60-minute window**. No late-day catch-up nudge above 750 mL.
- Gentle warning if logged intake passes **1.5 L in an hour** or **6 L in a day**.
- Workout copy: "Drink to thirst. You don't need to replace every drop."
- The medical gate in §2.
- A "Feeling unwell" card (small frequent drinks, ORS for vomiting or diarrhea, red flags that need care) instead of automatic illness add-ons. Hidden when the medical gate is on.

---

## 13. Tests to run before building on assumptions

1. **App Group smoke test:** app + widget on the owner's free team; write in the app, read in the widget.
2. **Siri voice phrase** for an App Shortcut without the Siri capability.
3. **HealthKit background delivery** entitlement on a free team (nice to have).
4. **`Tab(role: .prominent)` selection interception:** the tab must not visibly switch.

---

## 14. Not in v1

Weather API, altitude add-on, children's mode, iCloud sync, Live Activities, food logging, barcode scanning, Apple Watch app.

---

## 15. Where I overruled the research notes

| Topic | Research note said | Decision | Why |
|---|---|---|---|
| Water fraction basis | g water per g drink (note 02 §6) | mL water per 100 mL | The database already has per-100 mL values; this removes a known ≤4% undercount for free. |
| Orange juice badge | Badge (note 02 §8.1) | No badge | Its BHI advantage wasn't significant after correcting for water content and was gone by 4 hours. A badge should mean something. |
| Health "water" value | Effective water (note 05 §2.1) | Water content, not credit | Same thing in practice: Health's Water is what you consumed. The credit's diuretic penalties are Hydrate's model and stay in Hydrate. |
| Altitude add-on | Included, low confidence (note 01 §6) | Dropped from v1 | Low confidence, and it's an extra input for almost nobody. |
| Children 4–13 | Table mode (note 01 §6.3) | Not supported in v1 | Personal app; adds a parental-consent flow for no current user. |
| Credit rounding | Round each drink to 5 mL (note 02 §8) | Store exact, display rounded, capped at the water content | Avoids rounding drift in daily totals and a rounded credit above the water a drink contains. |
| Weight cap | Hard cap at the BMI-30 weight (note 01) | Soft cap: excess counts at 0.65 | Verification: excess weight in obesity is about ¼ fat-free mass, and turnover follows fat-free mass. |
| Fountain calibration | 0.75 × cup-drinking rate (note 04) | 0.33 × measured stream | The 0.75 factor had no source; capture, not swallowing, limits fountain intake. |

## 16. Data provenance (where every number comes from)

| Area | Primary sources | Verification |
|---|---|---|
| Daily goal | Yamada 2022 (*Science*), NASEM 2004/2023, EFSA 2010, ESPEN 2019 | `verification/01-goal-formula-verification.md` |
| Hydration credit | Maughan 2016/2019, Killer 2014, Polhuis 2017, Hobson & Maughan 2010, UKHSA 2025 | note 02 (37 references) |
| Drink nutrition | USDA FoodData Central (SR Legacy, FNDDS, Foundation, Branded), manufacturer labels, MEXT (Japan), Canadian Nutrient File, peer-reviewed caffeine analyses | `verification/drink-corrections.md`, `verification/drinks-additions.md`, `hydrate-drinks-report.md` |
| Presets, fountain, ice, equivalencies | Manufacturer specs, Starbucks/McDonald's, Kenney 2015/2016, Coetzee & Bennett 1978, USGS, EPA, DOE | `verification/04-equivalencies-verification.md` |
| Platform | Apple developer documentation, WWDC25/26, Apple DTS forum replies | note 05 (79 references) |
