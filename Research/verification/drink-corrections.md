# Drink database verification: corrections log

Verification pass over `03a-drinks-part-a.json` (81 entries) and `03b-drinks-part-b.json` (92 entries). Compiled 14 Nov 2026. The source files were not edited; every change is a patch in `drink-corrections.json` for the lead to apply.

## 1. Summary

| | |
|---|---|
| Patch objects | **30** (0 removals) |
| Field-level changes | **101** (62 nutrient values, the rest notes/source/confidence/range/density/name) |
| Null `per100mL` fields before | **81** (Part A 23, Part B 58) |
| Nulls filled | **30** |
| Nulls remaining | **51** (19 water, 16 potassium, 7 carbs, 4 sugar, 3 sodium, 2 protein; see Section 5) |
| USDA re-pull (task 1) | 10 records re-read from USDA; 8 entries patched, 2 confirmed unchanged (`other_broth_chicken`, `alc_hard_seltzer`) |
| Spot-check (task 4) | 25 high-confidence entries; **2 errors** (1 dead source URL, 1 field not matching its cited label); no wrong values in the 21 USDA-sourced entries |
| A/B overlaps (task 5) | 1 real duplicate (vegetable juice / V8); Propel, non-alcoholic beer and wine have no Part A counterpart |

Validation: `python3 -m json.tool` passes; every patch id exists in one of the two files; every non-removal patch has `source` and `reason`; every dot path resolves to an existing field except `orange_soda.caffeineRangePer100mL`, which is new to that Part A entry (Part A entries do not carry the key yet; the lead asked for this path to be allowed).

### Notable corrections
- **Pepsi Zero Sugar**: caffeine 38 mg and sodium 40 mg per 12 fl oz on the current US label (10.7 and 11.3 mg/100 mL); the 69 mg figure predates the January 2023 reformulation. Confidence low -> medium.
- **100% cranberry juice**: the SR Legacy record (12.1 g sugar/100 g) was wrong for pure juice. The Ocean Spray unsweetened pure cranberry label (9 g sugar, 18 g carbs, 60 kcal per 8 fl oz) agrees with FNDDS, so the entry is re-based: sugar 12.9 -> 3.8, kcal 49 -> 25, carbs 13.0 -> 7.6 per 100 mL.
- **Seltzer sodium** 21 -> 0 mg/100 mL (Polar Seltzer label; FNDDS used club-soda sodium).
- **Strong beer**: USDA "beer, higher alcohol" (0.27 g carbs) replaced with brewery data for a 9% double IPA: 71.6 kcal, 4.2 g carbs/100 mL, ABV 9.9 -> 9.0. UK CoFID could not settle this because it counts only sugars as beer carbohydrate.
- **Bubble tea**: sugar 3.6 -> 6.5 g/100 mL (representative of three lab analyses of shop drinks, range about 1.7-8). Caffeine null -> 32 mg/100 mL (range 8-49): USDA's recipe value is 8, but measured Taiwanese-style milk tea in Hong Kong averaged 32.
- **Kombucha** caffeine null -> 2.9 mg/100 mL (median of nine commercial products, HPLC). USDA FNDDS lists 11 mg/100 g, which is a recipe estimate.
- **White tea** caffeine 12 -> 20 mg/100 mL (low confidence). This is derived from the white/green leaf-caffeine ratio of about 1.7 in Hilal & Engelhardt 2007; the entry previously copied green tea.
- **Rooibos**: sodium 1 -> 3.8 mg/100 mL from the SA Rooibos Council's lab values; it previously used the generic herbal-tea record.
- **Matcha**: 7 nulls filled from the official Japanese food table, scaled to the entry's 2 g / 240 mL recipe.
- **Sweet iced tea** caffeine is now taken from the USDA record (18.5 mg/100 mL) instead of being estimated. **Latte** caffeine is confirmed directly from its own record.

## 2. Task 1: re-pull of the 10 mirror records

All 10 were read from `https://fdc.nal.usda.gov/portal-data/external/<fdcId>`, the public endpoint behind fdc.nal.usda.gov. One DEMO_KEY API call returned HTTP 429, so the portal endpoint was used throughout. Values are per 100 g, as published; the entry's own density is applied for per-100 mL.

| FDC | Record | Result |
|---|---|---|
| 2710386 | Coffee, Latte | Matches, including caffeine 36 mg/100 g (now confirmed from the record itself, not a sister record). Water 93.32 -> 93.29. |
| 2710508 | Tea, bubble | Water and carbs differ slightly (89.65 -> 89.69, 10.71 -> 10.76). **Caffeine reported: 8 mg/100 g.** Sugar 3.5 g/100 g confirmed (then replaced by the shop value under task 3). |
| 2710509 | Tea, kombucha | Macros match. **Caffeine reported: 11 mg/100 g** (recipe-based; see task 2). |
| 2710515 | Tea, iced, brewed, black, pre-sweetened | **Caffeine reported: 18 mg/100 g** -> 18.5 mg/100 mL (was estimated 18). Water 94.76 -> 94.79. |
| 2710622 | Hard seltzer | Confirms the cross-check note exactly (24 kcal, 0.55 g carbs, 0 sugars, 17 mg Na, 6 mg K, 3.2 g alcohol, caffeine 0). The entry is label-based (White Claw), so no change. |
| 2710638 | Margarita | Sugar/carbs 16.58 -> 16.54, water 77.35 -> 77.33; everything else matches. |
| 2710687 | Wine, sparkling | Water 87.46 -> 87.49; everything else matches. |
| 1999630 | Soy milk, unsweetened (Foundation) | Energy 38 kcal/100 g (Atwater), so 39.7 -> 39.1; fat 2.19 -> 2.18; Na 35.3 -> 35.0. The mirror's energy seems to be computed from macros. |
| 2257046 | Oat milk, unsweetened (Foundation) | Energy 48 kcal/100 g -> 49.4 (was 49.7). The record now declares total sugars as 2.32 g, which equals the summed sugars used before. |
| 174536 | Soup, chicken broth, ready-to-serve | Identical; no change. |

Most mirror differences are rounding-level (under 1%). None changed a value by more than 1.5% except the caffeine fields, which the mirror never showed.

## 3. Table of every change

| id | field | old | new | source |
|---|---|---|---|---|
| `coffee_latte` | per100mL.waterG | 93.32 | 93.29 | [1] |
| `coffee_latte` | notes | (text) | rewritten | [1] |
| `tea_bubble_milk` | per100mL.waterG | 89.65 | 89.69 | [1], [2], [3], [4], [5] |
| `tea_bubble_milk` | per100mL.carbsG | 10.71 | 10.76 | [1], [2], [3], [4], [5] |
| `tea_bubble_milk` | per100mL.sugarG | 3.64 | 6.5 | [1], [2], [3], [4], [5] |
| `tea_bubble_milk` | per100mL.caffeineMg | null | 32 | [1], [2], [3], [4], [5] |
| `tea_bubble_milk` | caffeineRangePer100mL | null | [8, 49] | [1], [2], [3], [4], [5] |
| `tea_bubble_milk` | source | (object) | replaced | [1], [2], [3], [4], [5] |
| `tea_bubble_milk` | notes | (text) | rewritten | [1], [2], [3], [4], [5] |
| `tea_bubble_milk` | confidence | medium | medium | [1], [2], [3], [4], [5] |
| `other_kombucha` | per100mL.caffeineMg | null | 2.9 | [6], [1] |
| `other_kombucha` | caffeineRangePer100mL | null | [1.5, 11.3] | [6], [1] |
| `other_kombucha` | notes | (text) | rewritten | [6], [1] |
| `tea_iced_sweet` | per100mL.waterG | 94.76 | 94.79 | [1] |
| `tea_iced_sweet` | per100mL.caffeineMg | 18 | 18.5 | [1] |
| `tea_iced_sweet` | notes | (text) | rewritten | [1] |
| `alc_margarita` | per100mL.waterG | 77.35 | 77.33 | [1] |
| `alc_margarita` | per100mL.sugarG | 16.58 | 16.54 | [1] |
| `alc_margarita` | per100mL.carbsG | 16.58 | 16.54 | [1] |
| `alc_wine_sparkling` | per100mL.waterG | 87.46 | 87.49 | [1] |
| `plant_soy_unsweetened` | per100mL.energyKcal | 39.7 | 39.1 | [1] |
| `plant_soy_unsweetened` | per100mL.fatG | 2.19 | 2.18 | [1] |
| `plant_soy_unsweetened` | per100mL.sodiumMg | 35.3 | 35.0 | [1] |
| `plant_oat_unsweetened` | per100mL.energyKcal | 49.7 | 49.4 | [1] |
| `plant_oat_unsweetened` | notes | (text) | rewritten | [1] |
| `water_mineral_sparkling` | per100mL.sugarG | null | 0.0 | [9], [1] |
| `water_mineral_sparkling` | per100mL.caffeineMg | null | 0.0 | [9], [1] |
| `orange_soda` | per100mL.caffeineMg | null | 0.0 | [10], [11], [1] |
| `orange_soda` | caffeineRangePer100mL | null | [0, 5.4] | [10], [11], [1] |
| `orange_soda` | notes | (text) | rewritten | [10], [11], [1] |
| `grape_soda` | per100mL.sugarG | null | 11.7 | [10], [1] |
| `grape_soda` | per100mL.caffeineMg | null | 0.0 | [10], [1] |
| `grape_soda` | notes | (text) | rewritten | [10], [1] |
| `pepsi_zero_sugar` | per100mL.caffeineMg | null | 10.7 | [7], [8], [32] |
| `pepsi_zero_sugar` | per100mL.sodiumMg | null | 11.3 | [7], [8], [32] |
| `pepsi_zero_sugar` | confidence | low | medium | [7], [8], [32] |
| `pepsi_zero_sugar` | source | (object) | replaced | [7], [8], [32] |
| `pepsi_zero_sugar` | notes | (text) | rewritten | [7], [8], [32] |
| `peach_nectar` | per100mL.caffeineMg | null | 0.0 | [12], [1] |
| `pear_nectar` | per100mL.caffeineMg | null | 0.0 | [1] |
| `tea_matcha` | per100mL.waterG | null | 99.2 | [13] |
| `tea_matcha` | per100mL.energyKcal | null | 2.0 | [13] |
| `tea_matcha` | per100mL.carbsG | null | 0.33 | [13] |
| `tea_matcha` | per100mL.proteinG | null | 0.24 | [13] |
| `tea_matcha` | per100mL.fatG | null | 0.04 | [13] |
| `tea_matcha` | per100mL.sodiumMg | null | 0.05 | [13] |
| `tea_matcha` | per100mL.potassiumMg | null | 22.3 | [13] |
| `tea_matcha` | source | (object) | replaced | [13] |
| `tea_matcha` | notes | (text) | rewritten | [13] |
| `tea_chai_latte` | per100mL.alcoholG | null | 0 | n/a (consistency) |
| `energy_celsius` | per100mL.carbsG | null | 0.0 | [14] |
| `energy_5hour` | per100mL.energyKcal | null | 7.0 | [15] |
| `energy_5hour` | per100mL.sodiumMg | null | 26.3 | [15] |
| `energy_5hour` | per100mL.potassiumMg | null | 22.8 | [15] |
| `energy_5hour` | notes | (text) | rewritten | [15] |
| `plant_oat_original` | per100mL.proteinG | null | 1.25 | [16] |
| `plant_oat_original` | per100mL.potassiumMg | null | 162.5 | [16] |
| `plant_pea` | per100mL.sugarG | null | 2.5 | [17] |
| `plant_pea` | per100mL.carbsG | null | 2.5 | [17] |
| `plant_pea` | per100mL.potassiumMg | null | 156.3 | [17] |
| `other_vegetable_juice` | per100mL.proteinG | null | 0.83 | [18] |
| `other_vegetable_juice` | per100mL.potassiumMg | null | 195.8 | [18] |
| `other_vegetable_juice` | name | Vegetable Juice (tomato-based, V8-type) | V8 Original 100% Vegetable Juice | [18] |
| `other_vegetable_juice` | brandExamples | ["V8", "Campbell's Tomato Juice"] | ["V8 Original"] | [18] |
| `other_vegetable_juice` | notes | (text) | rewritten | [18] |
| `water_sparkling_plain` | per100mL.sodiumMg | 21.0 | 0.0 | [19], [1] |
| `water_sparkling_plain` | notes | (text) | rewritten | [19], [1] |
| `water_sparkling_plain` | source | (object) | replaced | [19], [1] |
| `alc_beer_strong` | per100mL.energyKcal | 58.6 | 71.6 | [20], [21], [1] |
| `alc_beer_strong` | per100mL.carbsG | 0.27 | 4.23 | [20], [21], [1] |
| `alc_beer_strong` | per100mL.proteinG | 0.91 | 0.85 | [20], [21], [1] |
| `alc_beer_strong` | per100mL.alcoholG | 7.78 | 7.1 | [20], [21], [1] |
| `alc_beer_strong` | abvPercent | 9.9 | 9.0 | [20], [21], [1] |
| `alc_beer_strong` | source | (object) | replaced | [20], [21], [1] |
| `alc_beer_strong` | notes | (text) | rewritten | [20], [21], [1] |
| `cranberry_juice_100` | per100mL.waterG | 93.1 | 96.7 | [22], [1] |
| `cranberry_juice_100` | per100mL.energyKcal | 49 | 25 | [22], [1] |
| `cranberry_juice_100` | per100mL.sugarG | 12.9 | 3.8 | [22], [1] |
| `cranberry_juice_100` | per100mL.carbsG | 13.0 | 7.6 | [22], [1] |
| `cranberry_juice_100` | per100mL.proteinG | 0.4 | 0.0 | [22], [1] |
| `cranberry_juice_100` | per100mL.fatG | 0.1 | 0.0 | [22], [1] |
| `cranberry_juice_100` | per100mL.sodiumMg | 2.1 | 6.3 | [22], [1] |
| `cranberry_juice_100` | per100mL.potassiumMg | 82.3 | 76.1 | [22], [1] |
| `cranberry_juice_100` | densityGPerML | 1.069 | 1.048 | [22], [1] |
| `cranberry_juice_100` | confidence | medium | medium | [22], [1] |
| `cranberry_juice_100` | source | (object) | replaced | [22], [1] |
| `cranberry_juice_100` | notes | (text) | rewritten | [22], [1] |
| `buttermilk` | notes | (text) | rewritten | [23], [1] |
| `tea_white` | per100mL.caffeineMg | 12 | 20 | [24], [25], [1] |
| `tea_white` | source | (object) | replaced | [24], [25], [1] |
| `tea_white` | notes | (text) | rewritten | [24], [25], [1] |
| `tea_rooibos` | per100mL.energyKcal | 1 | 0 | [26], [27], [1] |
| `tea_rooibos` | per100mL.carbsG | 0.2 | 0.0 | [26], [27], [1] |
| `tea_rooibos` | per100mL.sodiumMg | 1 | 3.8 | [26], [27], [1] |
| `tea_rooibos` | source | (object) | replaced | [26], [27], [1] |
| `tea_rooibos` | notes | (text) | rewritten | [26], [27], [1] |
| `coffee_flat_white` | source | (object) | replaced | [28] |
| `coffee_flat_white` | notes | (text) | rewritten | [28] |
| `sports_ors_who` | source | (object) | replaced | [29] |
| `sports_gatorade` | per100mL.carbsG | 6.62 | 6.09 | [30] |
| `sports_gatorade` | notes | (text) | rewritten | [30] |

## 4. Task 4: spot-check of 25 random high-confidence entries

Sampling: entries with `confidence: "high"`, excluding the 10 mirror records already re-pulled (89 eligible), random sample with a fixed seed. USDA-sourced entries were checked automatically: each FDC record was fetched and every per-100 mL value was compared with USDA per-100 g × the entry's stated density. Label-sourced entries were checked by opening the cited URL.

| # | id | Cited source | Result |
|---|---|---|---|
| 1 | `fanta_orange_us` | coca-cola.com/us | OK (270 kcal, 80 mg Na, 74 g carbs, 73 g sugar / 20 fl oz) |
| 2 | `water_mineral_sparkling` | FDC 173233 | OK (sugar/caffeine nulls filled separately) |
| 3 | `coca_cola_original` | coca-cola.com/us | OK (240 kcal, 75 mg Na, 65 g sugar / 20 fl oz; 34 mg caffeine / 12 fl oz) |
| 4 | `chocolate_milk_whole` | FDC 170879 | OK |
| 5 | `alc_beer_regular` | FDC 168746 | OK |
| 6 | `water_bottled_still` | FDC 174158 | OK |
| 7 | `coffee_instant_decaf` | FDC 171894 | OK |
| 8 | `cola_diet_caffeine_free` | FDC 174850 | OK (0.1 vs 0.12 g is rounding) |
| 9 | `tea_chamomile` | FDC 174156 | OK |
| 10 | `alc_spirits_40` | FDC 174815 | OK (density 0.948 applied consistently) |
| 11 | `ginger_ale` | FDC 174846 | OK |
| 12 | `cola_diet` | FDC 175099 | OK |
| 13 | `coffee_espresso_single` | FDC 171891 | OK |
| 14 | `plant_almond_chocolate` | FDC 174820 | OK |
| 15 | `sports_gatorade` | PepsiCo sheet + FDC 173660 | **Error (minor):** carbsG 6.62 came from the old USDA record, but the cited label says 36 g / 591 mL = 6.09. Patched. |
| 16 | `tonic_water` | FDC 171869 | OK |
| 17 | `pear_nectar` | FDC 168186 | OK |
| 18 | `water_mineral_high` | FDC 174827 | OK |
| 19 | `peach_nectar` | FDC 168185 | OK |
| 20 | `tea_oolong` | FDC 174120 | OK |
| 21 | `alc_wine_red` | FDC 173190 | OK |
| 22 | `sports_ors_who` | rehydrate.org | **Error:** the cited URL now redirects to a parked domain. Values are correct (75 mmol Na, 20 mmol K, 13.5 g glucose per L). Source replaced with WHO/FCH/CAH/06.1. |
| 23 | `tea_herbal` | FDC 173232 | OK |
| 24 | `coffee_mocha` | FDC 2710410 | OK |
| 25 | `tomato_juice_low_sodium` | FDC 170545 | OK (energy 17 vs 17.5 is rounding) |

**Result: 2 errors in 25 (8%); no USDA transcription or conversion errors found.**

Other observations, not patched: five Part A entries carry sugar slightly above carbohydrate (`ginger_ale` 9.2/9.0, `grapefruit_juice` 8.0/7.8, `milk_whole` 5.0/4.8, `milk_skim` 5.2/5.1, `buttermilk` 5.5/5.0). These are faithful copies of quirks in the USDA records (sugars and carbohydrate-by-difference are measured separately), not transcription errors. The app should not assert sugar ≤ carbs.

## 5. Nulls still remaining (51) and why

| Field(s) | Entries | Why it is still null |
|---|---|---|
| sugarG | `orange_soda` | USDA gives carbohydrate only. US orange sodas list modified food starch (Fanta: 74 g carbs vs 73 g sugar), so the sugar = carbs rule does not apply. Use the `fanta_orange_us` brand entry for label sugar. |
| sugarG | `pepper_soda` | USDA gives carbohydrate only. The reference product's ingredients include caramel color, and the analytical USDA cola record shows sugar about 5% below carbs (10.3 vs 10.8), so sugar = carbs would overstate. FNDDS "Soft drink, pepper type" (2710545) maps to the cola record, so it adds nothing independent. |
| potassiumMg | 9 US soda brand entries (`coca_cola_original`, `diet_coke`, `pepsi`, `diet_pepsi`, `pepsi_zero_sugar`, `mountain_dew`, `dr_pepper`, `sprite`, `fanta_orange_us`) | Labels do not list potassium. Under 21 CFR 101.9(c), potassium is mandatory unless the panel carries a "not a significant source" statement, which is allowed only when the amount rounds to 0 (under 5 mg per serving). The lead could set these to 0 after confirming that statement on each current label; this pass did not set them. |
| waterG, sodiumMg, potassiumMg | `fanta_orange_uk` | The GB label gives salt as 0 g (EU rounding allows this below 0.0125 g/100 mL, i.e. under about 5 mg Na). No USDA analog for a 4.5%-sugar soda supplies water. |
| waterG, carbsG, sodiumMg, potassiumMg | `tea_chai_latte` | Starbucks' US site renders with scripts and could not be read. Aggregators give 115 mg Na and 45 g carbs per grande (2% milk) but disagree with each other (one lists 190 kcal / 32 g carbs), so nothing was filled. Verify in the Starbucks app: 115 mg -> 24.3 mg/100 mL, 45 g -> 9.5 g/100 mL. |
| potassiumMg, waterG | `energy_celsius` | Potassium is not on the panel (see the 21 CFR note above). Water is not declared. |
| carbsG, proteinG, potassiumMg | `energy_ghost` | Not prioritized; no primary label read this pass. |
| carbsG, proteinG | `energy_5hour` | The Supplement Facts panel declares neither (a supplement panel lists only nutrients present in significant amounts). |
| carbsG / sugarG | `sports_powerade`, `sports_liquid_iv`, `sports_prime_hydration` | Not in this pass's priority list; labels not re-read. |
| potassiumMg | `plant_coconut_unsweetened` | Not in the priority list; the So Delicious label was not re-read. |
| sugarG, sodiumMg, potassiumMg | `alc_beer_ipa` | Sierra Nevada publishes only ABV, kcal, carbs and protein. A generic USDA beer value would describe a different product. |
| carbsG, potassiumMg | `other_drinking_vinegar` | Bragg's label was not re-read (low-confidence entry). |
| waterG | 18 label-based Part B entries (plus `fanta_orange_uk`, above) | Labels never state water. Part A filled water for brand entries from the closest USDA generic record (water% × density); Part B did not. The lead can apply the same convention, for example `sports_powerade` from FDC 175108 and `other_vegetable_juice` from FDC 170063. It was not done here because it is a modelling convention, not a sourced value. |

## 6. Task 5: overlaps between Part A and Part B

| Part B id | Part A counterpart | Finding | Recommendation |
|---|---|---|---|
| `other_vegetable_juice` (V8 label) | `vegetable_juice` (USDA SR 170063) | **True duplicate concept.** But the current V8 label has 267 mg Na/100 mL vs about 174 in the USDA record, so the two are not interchangeable. | Keep **`vegetable_juice`** as the generic id. Keep `other_vegetable_juice` only as a brand entry: the patch renames it "V8 Original 100% Vegetable Juice" and fills its protein and potassium. If the lead prefers no brand entry, replace that patch with `{"id":"other_vegetable_juice","remove":true,"reason":"duplicate of vegetable_juice"}`. |
| `sports_propel` | none | Part A has no Propel or fitness-water entry (`water_sparkling_flavored` is an unsweetened seltzer). | Keep `sports_propel`. |
| `alc_beer_na`, `alc_wine_nonalcoholic` | none | Part A has no alcohol-free beer or wine entries. | Keep both. |
| `alc_rum_cola`, `alc_gin_tonic` | `cola_regular`, `tonic_water` | Composites built from the Part A records (same FDC IDs); not duplicates. | Keep. Recompute them if the lead ever changes `cola_regular` or `tonic_water`. |
| `plant_coconut_*` | `coconut_water*` | Different products (coconut milk beverage vs coconut water). | Keep all. |
| `other_hot_chocolate_milk` | `chocolate_milk*` | Different products (hot cocoa vs cold chocolate milk). | Keep all. |

No id appears in both files.

## 7. Method notes and judgment calls
- **Rounding.** Part A rounds to 0.1 g/mg and whole kcal; Part B uses up to 2 decimals. Patches follow each file's convention.
- **Measured over recipe.** Where USDA FNDDS (recipe-calculated) and peer-reviewed or government lab measurements of the actual product disagree (bubble tea caffeine and sugar, kombucha caffeine), the measured value is the default and the FNDDS value is kept inside the range and named in the notes.
- **Retailer label copies.** These were used where manufacturer sites blocked automated reads (Pepsi Zero Sugar, Celsius, 5-hour Energy, Ocean Spray, Polar). Each is noted in the source object. Where several retailers were consistent, confidence is medium.
- **Derived values.** These are the matcha macros (MEXT powder × 2/242) and white tea caffeine (USDA green × leaf ratio from Hilal & Engelhardt). Both state their method in `notes` and stay low confidence.
- **Not done.** No new drinks were added. `hydrationFactor` was not touched.

## 8. References
1. USDA FoodData Central portal records (read directly, Nov 2026): 2710386, 2710508, 2710509, 2710515, 2710622, 2710638, 2710687, 1999630, 2257046, 174536, plus 174854, 173203, 173209, 173233, 168185, 168186, 168117, 2709324, 170874, 2259792, 171906, 174842, 2710539, 173232, 171917, 2710545, 2710551, 2710553. https://fdc.nal.usda.gov/portal-data/external/<fdcId>
2. Min JE, Green DB, Kim L. Calories and sugars in boba milk tea: implications for obesity risk in Asian Pacific Islanders. Food Sci Nutr 2017;5(1):38-45. PMC5217910. https://pmc.ncbi.nlm.nih.gov/articles/PMC5217910/
3. CHOICE (Australia). Bubble tea test, 21 drinks. https://www.choice.com.au/food-and-drink/drinks/tea-and-coffee/articles/bubble-tea
4. Centre for Food Safety, Hong Kong. Sugar and energy in tea based beverages (Feb 2019; samples May-Jul 2018). https://www.cfs.gov.hk/english/programme/programme_rafs/files/Sugar_and_energy_in_tea_based_beverages.pdf
5. Centre for Food Safety / Consumer Council, Hong Kong. Caffeine in hot drinks (Oct 2013). https://www.cfs.gov.hk/english/programme/programme_rafs/programme_rafs_fci_01_04.html
6. Yang J, Lagishetty V, et al. Microbial and Chemical Profiles of Commercial Kombucha Products. Nutrients 2022;14(3):670. PMC8838605. https://pmc.ncbi.nlm.nih.gov/articles/PMC8838605/
7. Food Lion listing, Pepsi Zero Sugar 12 fl oz can (Nutrition Facts, caffeine, ingredients). https://foodlion.com/groceries/product/pepsi-zero-sugar-cola-soda-12-pk-12-oz-cans/147262
8. PepsiCo Product Facts, Pepsi Zero Sugar Wild Cherry & Cream 12 fl oz (38 mg caffeine). https://www.pepsicoproductfacts.com/Home/Product?gtin=00012000240577
9. Perrier Canada, nutrition information. https://www.perrier.com/ca/en-ca/node/1051
10. The Coca-Cola Company US, Fanta products (Orange and Grape nutrition and ingredients). https://www.coca-cola.com/us/en/brands/fanta/products
11. Caffeine Informer, Sunkist Orange Soda (19 mg / 12 fl oz; retailer labels agree). https://www.caffeineinformer.com/caffeine-content/sunkist-orange-soda
12. Hy-Vee listing, Jumex Peach Nectar ingredients. https://hy-vee.com/aisles-online/p/27563/Jumex-Peach-Nectar-from-Concentrate
13. MEXT Standard Tables of Food Composition in Japan 2020 (8th ed., 2023 suppl.), food 16035 matcha. https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=16_16035_7
14. Food Lion listing, Celsius Sparkling Orange 12 fl oz (Nutrition Facts, ingredients). https://foodlion.com/groceries/beverages/energy-drinks/celsius-live-fit-sparkling-orange-energy-drink-12-oz-can.html
15. Brookshire's listing, 5-hour Energy Regular Strength Berry (Supplement Facts). https://www.brookshires.com/product/5hour-energy-energy-shot-regular-strength-berry-id-00719410500016
16. Oatly US, Oatmilk Original 32 oz. https://www.oatly.com/en-us/products/oatmilk/oatmilk-32-oz
17. Ripple Foods, Ripple Original 8 fl oz. https://dev.ripplefoods.com/on-the-go/original/
18. Campbell's, V8 Original 100% Vegetable Juice. https://www.campbells.com/v8/vegetable-juice/v8-original
19. HEB listing, Polar Seltzer Original (0 mg sodium; ingredient: carbonated water). https://www.heb.com/product-detail/polar-seltzer-water-original/2801533
20. Sierra Nevada, Big Little Thing product stats (9.0% ABV, 254 kcal, 15 g carbs, 3 g protein per 12 oz; read via search snippet, page blocks automated fetch). https://dev.sierranevada.com/beer/big-little-thing
21. Public Health England / FSA. McCance and Widdowson's Composition of Foods Integrated Dataset (CoFID) 2021. https://www.gov.uk/government/publications/composition-of-foods-integrated-dataset-cofid
22. Hannaford listing, Ocean Spray Unsweetened Pure Cranberry Juice 32 oz (Nutrition Facts, ingredients). https://hannaford.com/groceries/product/ocean-spray-unsweetened-pure-cranberry-juice-32-oz-btl/288550
23. Darigold 1% Low Fat Buttermilk (260 mg Na/cup); Kemps Cultured 1% Lowfat (380 mg); also Lucerne, Meadow Gold, TG Lee, Cass-Clay labels via brand/retailer pages. https://www.darigold.com/?p=1105
24. Hilal Y, Engelhardt U. Characterisation of white tea - comparison to green and black tea. J Verbr Lebensm 2007;2:414-421. https://link.springer.com/doi/10.1007/s00003-007-0250-3
25. Chin JM, et al. Caffeine content of brewed teas. J Anal Toxicol 2008;32:702-704 (PMID 19007524). https://pubmed.ncbi.nlm.nih.gov/19007524/
26. South African Rooibos Council, FAQ nutrition table (per 100 mL infusion). https://sarooibos.co.za/frequently-asked-questions/
27. Olivier J, et al. Comparison of the mineral composition of leaves and infusions of traditional and herbal teas. S Afr J Sci 2012. https://sajs.co.za/article/view/9939
28. Matvaretabellen (Norway), food 13.040 Caffe latte, single, with whole milk. https://www.matvaretabellen.no/en/caffe-latte-single-with-whole-milk/
29. WHO. Oral rehydration salts: production of the new ORS. WHO/FCH/CAH/06.1 (2006). https://www.who.int/publications/i/item/WHO-FCH-CAH-06.1
30. PepsiCo Gatorade Lemon-Lime 20 fl oz product-facts sheet (updated 30 Jun 2023). https://argo.webstaurantstore.com/documents/nutrition/gatorade_thirst_quencher_lemon_lime_sports_drink_nutrition.pdf
31. The Coca-Cola Company US, Coca-Cola Original Taste product page. https://www.coca-cola.com/us/en/brands/coca-cola/products/original/original-taste
32. Wikipedia, Pepsi Zero Sugar (reformulation history; 69 mg pre-2023). https://en.wikipedia.org/wiki/Pepsi_Zero
