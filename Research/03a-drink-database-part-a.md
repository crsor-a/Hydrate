# 03a — Drink Database, Part A

**Scope:** sodas and soft drinks, fruit juices and nectars (plus lemonade and punch), dairy milks and cultured dairy drinks, plain water variants (including coconut water), and generic smoothies and protein shakes.
**Not in scope (Part B):** coffee, tea, energy and sports drinks, alcohol, plant milks, and other drinks.
**Machine-readable companion:** `03a-drinks-part-a.json`: 81 entries, validated with `python3 -m json.tool`.
**Compiled:** 13 Nov 2026. All nutrient values are **per 100 mL**. `hydrationFactor` is left `null` on purpose: another research track sets it from the Beverage Hydration Index work.

---

## 1. Summary

| | |
|---|---|
| Entries | **81** (water 8, soda 31, juice 22, dairy 12, smoothies and shakes 8) |
| Diet / zero-sugar / caffeine-free / light / low-sodium variants | 18 |
| Brand entries from manufacturer labels | 13 (Coca-Cola, Diet Coke, Coke Zero Sugar, Pepsi, Diet Pepsi, Pepsi Zero Sugar, Mountain Dew, Dr Pepper, Sprite, Sprite Zero Sugar, Fanta Orange US, Fanta Zero Sugar Orange US, Fanta Orange UK) |
| Primary source | USDA FoodData Central: SR Legacy (45 entries), FNDDS 2021–2023 (23 entries); Foundation Foods used as a cross-check |
| Cross-checks | Canadian Nutrient File (Health Canada API) for about 20 items; USDA Foundation Foods for the milks and buttermilk; UK figures from coca-cola.com/gb and The Grocer |
| Confidence | high 48 · medium 32 · low 1 |

---

## 2. Method

### 2.1 Source priority
1. **USDA FoodData Central (FDC)**. Every non-brand entry cites one FDC record and its ID:
   - **SR Legacy (April 2018)** is the default for generic beverages. It is mostly analytical: for example, the regular cola water value comes from 12 analysed samples. It is stable and also underlies the Canadian Nutrient File.
   - **FNDDS 2021–2023 (published 31 Oct 2024)** is used where it is the better match for what people actually drink: NHANES-style averages such as "Fruit smoothie, NFS", recipe-based smoothies, RTD protein shakes, diet versions of root beer, ginger ale and orange soda that SR does not split out, drinkable yogurt, nectars, and the milks. For milks, FNDDS reproduces the newer **Foundation Foods** analytical values (2018 sampling) and supplies a portion weight; Foundation records carry an odd 249 g/cup.
   - **Foundation Foods** is used to cross-check the milks (FDC 746772/746776/746778/746782) and buttermilk (FDC 2259792).
2. **National databases (cross-check).** The **Canadian Nutrient File (CNF)** was queried through Health Canada's public API, and its food codes are given in `source.crossCheck`. Where CNF is derived from USDA SR the numbers match; where it is independent (kefir, buttermilk sodium), the differences are noted. **UK CoFID / McCance & Widdowson** and **AUSNUT** were not queried, because CoFID ships as a spreadsheet download and AUSNUT has no open API. UK formula differences were checked against the manufacturer's GB site instead (see §5).
3. **Manufacturer nutrition facts** for brand sodas: coca-cola.com/us product pages and FAQ, a PepsiCo Beverage Facts nutrition sheet (PepsiCo-issued PDF), pepsicoproductfacts.com, and coca-cola.com/gb. Where the manufacturer page could not be read (PepsiCo's site is bot-protected; Keurig Dr Pepper's product facts site is script-rendered), I used label values as shown by US grocery retailers, marked `medium` confidence and said so in the notes. The CSPI caffeine chart could not be used: its data sits in an embedded third-party widget that cannot be machine-read.

### 2.2 How the data was pulled
- FDC search (API with the DEMO_KEY, which is rate-limited) found candidate records. Full records, including portion weights, came from the public FDC portal endpoint that backs fdc.nal.usda.gov. Nutrient IDs used: water 1051, energy 1008 (Foundation falls back to Atwater 2047), sugars 2000/1063, carbohydrate 1005, protein 1003, fat 1004, sodium 1093, potassium 1092, caffeine 1057.
- Values were copied from the records as-is, then converted. No values were typed in by hand from memory.

### 2.3 Converting per 100 g to per 100 mL
FDC reports per 100 g, so `per100mL = per100g × density`. The density for each entry is stored in `densityGPerML`.
- **Density source.** It is the median of the record's own volume-based portion weights (1 fl oz, 12 fl oz can, 1 cup, etc.; 1 fl oz = 29.5735 mL, 1 cup = 236.588 mL). Portions "with ice", fountain cups, and portions that are clearly label servings rather than weights were excluded.
- **Fallbacks** when a record has no usable portion: the closest equivalent USDA record's portion (for example, mango nectar uses FNDDS mango nectar at 31 g/fl oz, and kefir uses FNDDS kefir at 244 g/cup). Each fallback is spelled out in that entry's `notes`.
- **Water, diet sodas and seltzers** are set to 1.000 g/mL. This is backed by USDA SR can weights (12 fl oz club soda or diet cola = 355 g). FNDDS rounds every water-like drink to 30 g/fl oz (1.014), which is a convention, not a measurement.
- **Typical densities used:** sugared sodas 1.031–1.048; juices 1.03–1.07 (grape and cranberry 1.069); milks 1.031; chocolate milk 1.055; blended smoothies **0.913** (FNDDS: 216 g/cup, because they are aerated); milkshake 0.947.
- **Rounding.** Grams and milligrams are rounded to 0.1 and kcal to a whole number, after conversion.

### 2.4 Brand entries (label-based)
- Label values per serving were scaled to 100 mL using the **actual** volume: 12 fl oz = 354.9 mL and 20 fl oz = 591.5 mL. Some labels say "12 fl oz (360 mL)" under FDA rounding rules.
- Labels do not state water, so `waterG` comes from the closest USDA generic record (water % × density). That record is cited in `source.waterFrom`.
- If a label does not declare potassium, `potassiumMg` is `null`. A missing value on a US label means "not significant", not a measured zero.

### 2.5 Field conventions (beyond the requested schema)
| Field | Meaning |
|---|---|
| `densityGPerML` | Density used for the conversion (`null` only for the UK Fanta label entry, which is already per 100 mL) |
| `source.description` | FDC food description, verbatim |
| `source.crossCheck` | Secondary database comparison (CNF code, FNDDS/SR sibling, Foundation record) |
| `source.waterFrom` | Brand entries only: the USDA record that supplied the water value |
| `quickPick` / `quickPickRank` | Suggested quick-pick default and its slot in an app-wide list of 12 (see §8) |
| `region` | `"US"` or `"UK"` on brand entries, where formulas differ by market |
| **`null` in `per100mL`** | **Unknown, not zero.** The app must not treat a null caffeine value as caffeine-free (relevant for `pepsi_zero_sugar`, `orange_soda`, `grape_soda`). |

---

## 3. Entries at a glance (per 100 mL)

#### Water

| id | Name | Water g | kcal | Sugar g | Na mg | K mg | Caffeine mg | Density | Source | Conf. |
|---|---|---|---|---|---|---|---|---|---|---|
| `water_tap` | Tap water | 99.9 | 0 | 0 | 4 | 0 | 0 | 1 | FDC 173647 | high |
| `water_bottled_still` | Bottled water (still) | 100 | 0 | 0 | 2 | 0 | 0 | 1 | FDC 174158 | high |
| `water_sparkling_plain` | Sparkling water / seltzer (unflavored) | 99.9 | 0 | 0 | 21 | 2 | 0 | 1 | FDC 2710539 | medium |
| `water_sparkling_flavored` | Flavored sparkling water (unsweetened) | 99.8 | 0 | 0 | 6 | 2 | 0 | 1 | FDC 2710540 | medium |
| `water_mineral_sparkling` | Sparkling mineral water | 99.9 | 0 | – | 1 | 0 | – | 1 | FDC 173233 | high |
| `water_mineral_high` | Mineral water (high mineral) | 100 | 0 | 0 | 13 | 2 | 0 | 1 | FDC 174827 | high |
| `coconut_water` | Coconut water (unsweetened) | 96.3 | 18 | 4 | 26.4 | 167.3 | 0 | 1.014 | FDC 174831 | high |
| `coconut_water_sweetened` | Coconut water (sweetened) | 91.5 | 38 | 8.9 | 25.4 | 159.2 | 0 | 1.014 | FDC 2707573 | medium |

#### Soda & soft drinks

| id | Name | Water g | kcal | Sugar g | Na mg | K mg | Caffeine mg | Density | Source | Conf. |
|---|---|---|---|---|---|---|---|---|---|---|
| `cola_regular` | Cola | 93 | 44 | 10.3 | 3.1 | 5.2 | 9.4 | 1.04 | FDC 174852 | high |
| `cola_diet` | Diet cola | 99.5 | 2 | 0 | 8 | 8 | 12 | 1 | FDC 175099 | high |
| `cola_caffeine_free` | Cola, caffeine-free | 93 | 43 | 11 | 4.2 | 3.1 | 0 | 1.038 | FDC 174851 | high |
| `cola_diet_caffeine_free` | Diet cola, caffeine-free | 99.7 | 1 | 0 | 4 | 7 | 0 | 1 | FDC 174850 | high |
| `lemon_lime_soda` | Lemon-lime soda | 92.9 | 43 | 10.8 | 10.4 | 1 | 0 | 1.038 | FDC 173205 | high |
| `lemon_lime_soda_diet` | Lemon-lime soda, diet / zero | 99.8 | 0 | 0 | 6 | 2 | 0 | 1 | FDC 173204 | high |
| `root_beer` | Root beer | 93.1 | 43 | 11 | 13.5 | 1 | 0 | 1.042 | FDC 171871 | high |
| `root_beer_diet` | Root beer, diet / zero | 99.8 | 0 | 0 | 6 | 2 | 0 | 1 | FDC 2710558 | medium |
| `ginger_ale` | Ginger ale | 94 | 35 | 9.2 | 7.2 | 1 | 0 | 1.031 | FDC 174846 | high |
| `ginger_ale_diet` | Ginger ale, diet / zero | 99.8 | 0 | 0 | 6 | 2 | 0 | 1 | FDC 2710556 | medium |
| `orange_soda` | Orange soda | 91.8 | 50 | – | 12.6 | 2.1 | – | 1.048 | FDC 174854 | medium |
| `orange_soda_diet` | Orange soda, diet / zero | 99.8 | 0 | 0 | 6 | 2 | 0 | 1 | FDC 2710552 | medium |
| `pepper_soda` | Pepper-style soda | 92.8 | 43 | – | 10.4 | 1 | 10.4 | 1.038 | FDC 173209 | medium |
| `pepper_soda_diet` | Pepper-style soda, diet / zero | 99.5 | 2 | 0 | 8 | 8 | 12 | 1 | FDC 2710546 | medium |
| `cream_soda` | Cream soda | 90.6 | 53 | 13.9 | 12.5 | 1 | 0 | 1.045 | FDC 173199 | high |
| `grape_soda` | Grape soda | 93.1 | 45 | – | 15.7 | 1 | – | 1.048 | FDC 173203 | medium |
| `tonic_water` | Tonic water | 93.9 | 35 | 9.1 | 12.4 | 0 | 0 | 1.031 | FDC 171869 | high |
| `club_soda` | Club soda | 99.9 | 0 | 0 | 21 | 2 | 0 | 1 | FDC 174842 | high |
| `coca_cola_original` | Coca-Cola Original | 93 | 41 | 11 | 12.7 | – | 9.6 | 1.04 | The Coca-Cola Company | high |
| `diet_coke` | Diet Coke | 99.5 | 0 | 0 | 11.3 | – | 13 | 1 | The Coca-Cola Company | high |
| `coke_zero_sugar` | Coca-Cola Zero Sugar | 99.5 | 0 | 0 | 11.3 | 16.9 | 9.6 | 1 | The Coca-Cola Company | high |
| `pepsi` | Pepsi | 93 | 42 | 11.6 | 8.5 | – | 10.7 | 1.04 | PepsiCo Beverage Facts nutrition sheet / pepsicoproductfacts.com | high |
| `diet_pepsi` | Diet Pepsi | 99.5 | 0 | 0 | 9.9 | – | 9.9 | 1 | PepsiCo product facts | medium |
| `pepsi_zero_sugar` | Pepsi Zero Sugar | 99.5 | 0 | 0 | – | – | – | 1 | PepsiCo product facts | low |
| `mountain_dew` | Mountain Dew | 91.8 | 48 | 13 | 16.9 | – | 15.2 | 1.048 | PepsiCo label values | medium |
| `dr_pepper` | Dr Pepper | 92.8 | 42 | 11 | 15.5 | – | 11.6 | 1.038 | Keurig Dr Pepper label | medium |
| `sprite` | Sprite | 93.1 | 39 | 10.7 | 18.3 | – | 0 | 1.04 | The Coca-Cola Company | high |
| `sprite_zero` | Sprite Zero Sugar | 99.8 | 0 | 0 | 9.9 | 31 | 0 | 1 | The Coca-Cola Company | high |
| `fanta_orange_us` | Fanta Orange (US) | 91.8 | 46 | 12.3 | 13.5 | – | 0 | 1.048 | The Coca-Cola Company | high |
| `fanta_orange_zero_us` | Fanta Zero Sugar Orange (US) | 99.8 | 0 | 0 | 10.1 | 20.3 | 0 | 1 | The Coca-Cola Company | high |
| `fanta_orange_uk` | Fanta Orange (UK) | – | 19 | 4.5 | – | – | 0 | – | The Coca-Cola Company | high |

#### Juices, nectars, lemonade & punch

| id | Name | Water g | kcal | Sugar g | Na mg | K mg | Caffeine mg | Density | Source | Conf. |
|---|---|---|---|---|---|---|---|---|---|---|
| `orange_juice` | Orange juice | 91.7 | 52 | 8.7 | 2.1 | 187.3 | 0 | 1.052 | FDC 169100 | high |
| `orange_juice_fresh` | Orange juice, freshly squeezed | 92.5 | 47 | 8.8 | 1 | 209.6 | 0 | 1.048 | FDC 169098 | high |
| `apple_juice` | Apple juice | 92.4 | 48 | 10.1 | 4.2 | 105.8 | 0 | 1.048 | FDC 173933 | high |
| `grape_juice` | Grape juice | 90.3 | 64 | 15.2 | 5.3 | 111.2 | 0 | 1.069 | FDC 173042 | high |
| `cranberry_juice_cocktail` | Cranberry juice cocktail | 92.1 | 58 | 12.7 | 2.1 | 15 | 0 | 1.069 | FDC 171903 | high |
| `cranberry_juice_cocktail_light` | Cranberry juice cocktail, light | 95.3 | 19 | 4.6 | 3 | 25 | 0 | 1.001 | FDC 171904 | medium |
| `cranberry_juice_100` | Cranberry juice, 100% unsweetened | 93.1 | 49 | 12.9 | 2.1 | 82.3 | 0 | 1.069 | FDC 168117 | medium |
| `pineapple_juice` | Pineapple juice | 91.4 | 56 | 10.6 | 2.1 | 137.5 | 0 | 1.058 | FDC 169947 | high |
| `grapefruit_juice` | Grapefruit juice | 94.6 | 38 | 8 | 2.1 | 146.6 | 0 | 1.04 | FDC 174678 | high |
| `tomato_juice` | Tomato juice | 96.8 | 17 | 2.7 | 260.1 | 223.1 | 0 | 1.028 | FDC 170458 | high |
| `tomato_juice_low_sodium` | Tomato juice, low sodium | 96.7 | 17 | 2.6 | 10.3 | 222.9 | 0 | 1.027 | FDC 170545 | high |
| `vegetable_juice` | Vegetable juice cocktail | 96.7 | 23 | 2.9 | 173.7 | 190.2 | 0 | 1.028 | FDC 170063 | high |
| `juice_blend` | Mixed fruit juice (100%) | 91.2 | 52 | 11.4 | 7.3 | 100.6 | 0 | 1.048 | FDC 2709316 | medium |
| `lemonade` | Lemonade | 93.3 | 42 | 10.4 | 4.2 | 15.7 | 0 | 1.044 | FDC 173217 | high |
| `lemonade_bottled` | Lemonade, bottled (Minute Maid) | 91.9 | 48 | 12.2 | 6.3 | 10.4 | 0 | 1.045 | FDC 171884 | medium |
| `lemonade_light` | Lemonade, light / powdered drink mix | 97.7 | 26 | 6.8 | 12.6 | 3.1 | 0 | 1.048 | FDC 2710571 | medium |
| `fruit_punch` | Fruit punch | 92.4 | 50 | 11.9 | 10.5 | 26.2 | 0 | 1.05 | FDC 171914 | high |
| `fruit_drink` | Fruit-flavored drink (<3% juice) | 84.4 | 64 | 15.9 | 36.2 | 31.2 | 0 | 1.006 | FDC 174179 | medium |
| `mango_nectar` | Mango nectar | 90.8 | 53 | 13 | 5.2 | 25.2 | 0 | 1.048 | FDC 167785 | high |
| `peach_nectar` | Peach nectar | 91.5 | 52 | 11.7 | 8.4 | 52.4 | – | 1.048 | FDC 168185 | high |
| `pear_nectar` | Pear nectar | 88.6 | 63 | 16 | 4.2 | 13.7 | – | 1.055 | FDC 168186 | high |
| `apricot_nectar` | Apricot nectar | 88 | 58 | 13.2 | 8.2 | 68.9 | 0 | 1.028 | FDC 171704 | high |

#### Dairy milks & cultured drinks

| id | Name | Water g | kcal | Sugar g | Na mg | K mg | Caffeine mg | Density | Source | Conf. |
|---|---|---|---|---|---|---|---|---|---|---|
| `milk_whole` | Whole milk (3.25%) | 90.8 | 63 | 5 | 39.2 | 154.6 | 0 | 1.031 | FDC 2705385 | high |
| `milk_2pct` | Reduced-fat milk (2%) | 91.9 | 52 | 5 | 40.2 | 163.9 | 0 | 1.031 | FDC 2705386 | high |
| `milk_1pct` | Low-fat milk (1%) | 92.5 | 44 | 5.1 | 40.2 | 163.9 | 0 | 1.031 | FDC 2705387 | high |
| `milk_skim` | Skim milk (fat-free) | 93.6 | 35 | 5.2 | 42.3 | 172.2 | 0 | 1.031 | FDC 2705388 | high |
| `chocolate_milk` | Chocolate milk (reduced fat) | 86.7 | 80 | 10.1 | 69.6 | 178.3 | 1.1 | 1.055 | FDC 170880 | high |
| `chocolate_milk_whole` | Chocolate milk (whole) | 86.8 | 88 | 10.1 | 63.3 | 176.2 | 1.1 | 1.055 | FDC 170879 | high |
| `chocolate_milk_lowfat` | Chocolate milk (low fat 1%) | 89.1 | 68 | 10.5 | 68.6 | 181.5 | 1.1 | 1.055 | FDC 170881 | high |
| `strawberry_milk` | Strawberry milk | 89.5 | 68 | 8.9 | 40.9 | 157.2 | 0 | 1.048 | FDC 2705495 | medium |
| `buttermilk` | Buttermilk (low fat, cultured) | 93.3 | 41 | 5.5 | 153.2 | 156.3 | 0 | 1.035 | FDC 170874 | medium |
| `kefir_plain` | Kefir (plain, low fat) | 92.5 | 44 | 4.8 | 41.2 | 169.1 | 0 | 1.031 | FDC 170904 | medium |
| `kefir_flavored` | Kefir (fruit-flavored, low fat) | 87.4 | 64 | 9.5 | 38.1 | 158.8 | 0 | 1.031 | FDC 171301 | medium |
| `drinkable_yogurt` | Drinkable yogurt | 84.9 | 77 | 10.6 | 54.9 | 176.1 | 0 | 1.036 | FDC 2705442 | medium |

#### Smoothies & shakes

| id | Name | Water g | kcal | Sugar g | Na mg | K mg | Caffeine mg | Density | Source | Conf. |
|---|---|---|---|---|---|---|---|---|---|---|
| `smoothie_fruit_dairy` | Fruit smoothie (with yogurt/milk) | 76.7 | 60 | 8.1 | 25.6 | 158.9 | 0 | 0.913 | FDC 2705514 | medium |
| `smoothie_fruit_nondairy` | Fruit smoothie (no dairy) | 78.5 | 49 | 8 | 1.8 | 156.1 | 0 | 0.913 | FDC 2709334 | medium |
| `smoothie_bottled` | Fruit smoothie (bottled) | 91.5 | 52 | 10.5 | 2.1 | 210.6 | 0 | 1.048 | FDC 2709339 | medium |
| `smoothie_green` | Green / fruit-and-vegetable smoothie | 76.8 | 58 | 9 | 17.3 | 273.9 | 0 | 0.913 | FDC 2710151 | medium |
| `smoothie_protein` | Protein smoothie (fruit + dairy + protein) | 73.1 | 72 | 6.7 | 36.5 | 157.9 | 0 | 0.913 | FDC 2705515 | medium |
| `protein_shake_rtd` | Protein shake (ready-to-drink) | 92.8 | 64 | 0.6 | 75.5 | 187.6 | 0 | 1.048 | FDC 2710726 | medium |
| `meal_replacement_shake` | Nutrition / meal-replacement shake | 79.9 | 110 | 10.2 | 88 | 163.5 | 0 | 1.048 | FDC 2710725 | medium |
| `milkshake` | Milkshake (vanilla/strawberry) | 66 | 140 | 12.9 | 76.7 | 157.2 | 0 | 0.947 | FDC 2705509 | medium |

---

## 4. Notes per category

### 4.1 Water
- Tap and bottled water both come out at 0 kcal, with 2–4 mg Na per 100 mL. Local tap sodium varies, and USDA gives municipal at 3 mg and well water at 5 mg.
- **Seltzer and club soda.** FNDDS combines unflavored seltzer with club soda and gives both the club-soda sodium figure (21 mg/100 mL). Real seltzer is usually close to 0 mg. I kept the FNDDS number, rated it `medium`, and explained this in the entry. If the app ever shows sodium, the seltzer entry could use bottled-water sodium instead, but that would be a judgment call rather than a sourced value.
- **Flavored sparkling water** (LaCroix, Bubly) is mapped by FNDDS to the zero-calorie non-cola profile.
- **Mineral water.** The low-mineral example is Perrier and the high-mineral example is Gerolsteiner (13 mg Na/100 mL, which matches CNF code 2918). Calcium and magnesium are not part of the schema.
- **Coconut water** is the potassium outlier in this category (about 167 mg/100 mL) and also has meaningful sodium (26 mg). Its value for electrolyte and hydration tracking belongs to the hydration-factor track.

### 4.2 Sodas
- **Generic records versus brands.** USDA generic cola (9 mg caffeine/100 g, so about 33 mg per can) agrees with the brands: Coca-Cola 34 mg and Pepsi 38 mg per 12 fl oz. The generic diet cola (12 mg/100 g, about 43 mg per can) falls between Coke Zero Sugar (34 mg) and Diet Coke (46 mg), so brand entries exist for anyone who wants exact caffeine.
- **Brand caffeine per 12 fl oz (355 mL), as used:** Coca-Cola 34 · Diet Coke 46 · Coke Zero Sugar 34 · Pepsi 38 · Diet Pepsi 35 (the fountain sheet says 34) · Mountain Dew 54 · Dr Pepper 41 · Sprite / Fanta 0 · Pepsi Zero Sugar **unknown**. Sources disagree there: 69 mg on older labels, 38 mg on newer PepsiCo listings, and the formula changed around 2022–2023.
- **Sugar in sodas.** Two USDA SR records (orange soda, pepper-type) and the grape soda record report carbohydrate but not total sugars. Carbohydrate in a soda is essentially all sugar, but the instructions say not to fill gaps, so `sugarG` is `null` and `carbsG` is present. The app can fall back to `carbsG` for sugar when `sugarG` is null **in the soda category only**. The brand entries (Fanta, Dr Pepper) give label sugar.
- **Caffeinated surprises** are mentioned in notes: regular Barq's root beer and some Sunkist formulas contain caffeine, while the generic root beer and orange soda records do not.
- **Tonic water** has about 9 g sugar/100 mL, close to ginger ale, so it is not the zero-calorie mixer many people assume. **Club soda** is unsweetened.

### 4.3 Juices, nectars, lemonade, punch
- **100% juice** runs from 38 kcal (grapefruit) to 64 kcal (grape) per 100 mL. Orange juice uses the chilled-carton SR record (169100). Fresh-squeezed is listed separately. The values match CNF and FNDDS within about 1 g of sugar.
- **Cranberry.** "Juice cocktail" (about 27% juice, sweetened) is the default. Light cocktail and 100% unsweetened are separate entries. The SR 100% unsweetened record lists 12.1 g sugar/100 g, but FNDDS lists 3.4 g for "Cranberry juice, 100%, not a blend". Pure cranberry juice is very tart, so the SR figure is suspect, and I flagged that entry `medium`.
- **Tomato and vegetable juice** are the sodium outliers (174–260 mg/100 mL). Low-sodium versions are included.
- **Lemonade.** The classic entry is about 42 kcal and 10.4 g sugar. The bottled Minute Maid entry is 48 kcal and 12.2 g. The light / powdered-mix entry is 26 kcal. Zero-sugar mixes such as Crystal Light are not included (FNDDS 2710599, about 2 kcal; a possible addition).
- **Fruit punch** and **fruit-flavored drinks (<3% juice)** are juice-drink products, not juice. The "<3% juice" record is the highest-sugar entry in Part A (15.9 g/100 mL).
- **Nectars** (mango, peach, pear, apricot) are 52–63 kcal/100 mL, mostly added sugar.

### 4.4 Dairy
- **Milks.** Values are FNDDS 2021–2023, which equal USDA Foundation Foods analytical data (2018 sampling); the older SR Legacy records serve as the cross-check. The differences are small (whole milk: Foundation K 150 vs SR 132 mg/100 g; Na 38 vs 43). Lactose-free milk has the same values as regular milk (FNDDS 2705392), so it is listed as a variant rather than a separate entry.
- **UK semi-skimmed** (1.5–1.8% fat) sits between the 1% and 2% entries, which is mentioned in the 2% notes.
- **Buttermilk sodium** varies a lot between sources: USDA SR 148, USDA Foundation 2022 92.5, and CNF 190 mg/100 g. The SR value is used and the entry is marked `medium`.
- **Kefir.** The plain entry uses the USDA branded Lifeway plain low-fat analysis (44 kcal, 4.8 g sugar/100 mL). The FNDDS generic kefir is sweeter (6.9 g/100 g) because it mixes in flavored products. CNF plain low-fat kefir is 37 kcal and 3.0 g sugar.
- **Drinkable yogurt** uses FNDDS "Yogurt, liquid" (sweetened). Salted ayran and plain lassi are different products and are not covered.

### 4.5 Smoothies and shakes
- These are recipe-based FNDDS averages, so they get `medium` confidence by design. Shop smoothies vary by a factor of more than two.
- **Density matters here.** FNDDS weighs blended smoothies at 216 g per cup (0.913 g/mL) because they contain air. A 16 fl oz cup therefore holds about 432 g of smoothie. Water per 100 mL comes out at about 77 g, against about 84 g per 100 g.
- **RTD protein shake:** the FNDDS high-protein NFS record has 6.9 g protein and 0.6 g sugar per 100 mL. Its own portion weights imply 1.082 g/mL, which looks inflated, so I used the identical-profile Slim Fast high-protein record's can weight (1.048).
- **Meal-replacement shake** follows the Ensure profile (110 kcal/100 mL). The "Plus" versions are about 140 kcal and are named in the notes.
- **Milkshake** is included because people log it, but it is low in water (66 g/100 mL).

---

## 5. US versus UK/EU formula differences
| Drink | US | UK / EU | Source |
|---|---|---|---|
| **Fanta Orange** | 46 kcal, **12.3 g sugar**/100 mL; HFCS; no juice; caffeine-free | 19 kcal, **4.5 g sugar**/100 mL; sugar plus sweeteners; 3.7% orange juice | coca-cola.com/us (20 fl oz label: 270 kcal, 73 g sugar); coca-cola.com/gb per-100 mL panel. Reformulated in March 2017 to 4.6 g/100 mL to stay under the UK Soft Drinks Industry Levy threshold of 5 g/100 mL (The Grocer) |
| **Coca-Cola** | 11.0 g sugar/100 mL (HFCS); 34 mg caffeine per 355 mL | Classic sugar per 100 mL was not retrieved for this pass; caffeine 32–33 mg per 330–355 mL per Coca-Cola IE/PH FAQ pages | coca-cola.com/us, coca-cola.com FAQs |
| **Diet Coke / Coca-Cola Light** | 46 mg caffeine per 355 mL | about 42 mg per 355 mL (Coca-Cola PH) | coca-cola.com FAQs |
| **Sprite** | 10.7 g sugar/100 mL | The UK Sprite was also reformulated under the levy (sugar plus sweeteners), but its per-100 mL value was not retrieved | — |

**Recommendation:** add a `region` key to the app (the JSON already includes it on brand entries) and show the regional Fanta and Sprite variants based on the device locale. The generic USDA entries reflect US formulations.

---

## 6. Judgment calls
1. **The generic entry is the primary pick, and brands are optional detail.** USDA generic records are analytical and stable. Brand labels change often (Pepsi Zero Sugar caffeine, Diet Pepsi sweeteners) and are rounded. Brand entries exist mainly for exact **caffeine** and **sugar**.
2. **Unknown means `null`, never a guess.** This applies to missing SR sugars (orange, pepper and grape soda), Pepsi Zero Sugar caffeine and sodium, undeclared label potassium, and UK Fanta water and sodium.
3. **Density comes from USDA portion weights, not textbook values.** Where a record's portion was clearly a label serving or produced an impossible value (such as more than 100 g of water per 100 mL), I swapped in the closest USDA record with a sane portion and recorded the swap. This applies to lemonade-light, the RTD protein shake, bottled lemonade, grapefruit juice and vegetable juice.
4. **Milk values use FNDDS = Foundation**, not SR Legacy, because the Foundation data is the newer analytical sampling. Density is 1.031 g/mL (FNDDS 244 g/cup), not Foundation's 249 g/cup.
5. **Seltzer sodium:** I kept the FNDDS value (21 mg), even though it is club-soda sodium. It is the only USDA record for seltzer, and the caveat is documented.
6. **Diet root beer, ginger ale and orange soda** come from FNDDS, which maps them to one generic low-calorie non-cola profile. That is correct for these fields (0 kcal, trace sodium) but not specific to each product.
7. **Smoothies use an aerated density of 0.913.** This follows USDA's own weights. If the app logs a smoothie by cup volume, this gives a more accurate water mass than assuming 1.0.
8. **Retailer-shown labels** were accepted for Dr Pepper and Mountain Dew sodium and sugar only when several retailers agreed and the manufacturer site could not be read. These are marked `medium`.

---

## 7. Data gaps and suggested follow-ups
- **Pepsi Zero Sugar** caffeine and sodium are unresolved. The next step is reading a current US can label or pepsicoproductfacts.com in a browser.
- **Diet Mountain Dew, Diet Dr Pepper / Dr Pepper Zero, 7UP, A&W, Canada Dry** brand entries were not created, because no primary source could be read for their sodium and sugar. Their generic equivalents exist.
- **UK CoFID and AUSNUT cross-checks** were not done; only CNF was used. Worth adding CoFID values for cola, orange juice and semi-skimmed milk if a UK launch is planned.
- **Unsweetened drinking yogurt / ayran, sugar-free lemonade mixes, diet tonic, Spindrift-style juice seltzers and fairlife-style ultra-filtered milk** are not included.
- The **sugar in 100% unsweetened cranberry juice** is disputed (SR 12.1 g vs FNDDS 3.4 g per 100 g).
- **Mineral composition** (Ca, Mg, bicarbonate) is not in the schema. If hydration scoring ever uses electrolytes beyond Na and K, mineral waters will need their own data.

---

## 8. Proposed drink-picker taxonomy (Part A portion)

```
Water
  ├─ Still ............ tap · bottled
  ├─ Sparkling ........ plain seltzer · flavored (unsweetened)
  ├─ Mineral .......... low-mineral (Perrier-type) · high-mineral (Gerolsteiner-type)
  └─ Coconut water .... unsweetened · sweetened
Soda & Soft Drinks
  ├─ Cola ............. regular · diet · zero sugar · caffeine-free · diet caffeine-free · [brands: Coca-Cola, Diet Coke, Coke Zero Sugar, Pepsi, Diet Pepsi, Pepsi Zero Sugar]
  ├─ Lemon-lime ....... regular · diet/zero · [Sprite, Sprite Zero Sugar]
  ├─ Citrus (Dew) ..... [Mountain Dew]
  ├─ Pepper-style ..... regular · diet/zero · [Dr Pepper]
  ├─ Root beer ........ regular · diet/zero
  ├─ Ginger ale ....... regular · diet/zero
  ├─ Orange & fruit ... orange · orange diet · grape · [Fanta Orange US / UK, Fanta Zero Sugar]
  ├─ Cream soda ....... regular
  └─ Mixers ........... tonic water · club soda
Juice
  ├─ Citrus ........... orange (carton) · orange (fresh) · grapefruit
  ├─ Apple & grape .... apple · grape
  ├─ Cranberry ........ cocktail · light cocktail · 100% unsweetened
  ├─ Tropical ......... pineapple
  ├─ Vegetable ........ tomato · tomato low-sodium · vegetable cocktail
  ├─ Blends ........... 100% mixed fruit
  ├─ Nectars .......... mango · peach · pear · apricot
  ├─ Lemonade & punch . lemonade · bottled lemonade · light/mix · fruit punch
  └─ Juice drinks ..... fruit-flavored drink (<3% juice)
Dairy
  ├─ Milk ............. whole · 2% · 1% · skim  (lactose-free = same values)
  ├─ Flavored milk .... chocolate (2%, whole, 1%) · strawberry
  └─ Cultured ......... buttermilk · kefir plain · kefir flavored · drinkable yogurt
Smoothies & Shakes
  ├─ Fruit smoothie ... with dairy · no dairy · bottled
  ├─ Green smoothie ... fruit + vegetable
  ├─ Protein .......... protein smoothie · RTD protein shake
  ├─ Meal replacement . Ensure/Boost type
  └─ Milkshake ........ fast-food milkshake
(Part B adds: Coffee, Tea, Energy & Sports, Alcohol, Plant milks, Other)
```

UI guidance:
- **Top level:** about 10 categories with icons, combining Part A and Part B.
- **Second level:** subcategories.
- **Variant chips:** regular / diet / zero sugar / caffeine-free / light / low-sodium. Variant chips should change the selected entry ID rather than be a separate screen.
- **Brands:** show them as a searchable "brand" list inside a subcategory, not as top-level items.

## 9. Suggested quick-pick defaults (app-wide 12)
These are the drinks people log most often, mixing everyday water with the most common caloric and caffeinated drinks. Part A provides 8 slots, flagged `quickPick: true` with `quickPickRank` in the JSON. Part B fills the other 4.

| Rank | Drink | Entry |
|---|---|---|
| 1 | Water | `water_tap` (tap and bottled water have the same nutrition) |
| 2 | Sparkling water | `water_sparkling_plain` |
| 3 | Coffee (brewed) | *Part B* |
| 4 | Tea | *Part B* |
| 5 | Milk (2%) | `milk_2pct` |
| 6 | Orange juice | `orange_juice` |
| 7 | Cola | `cola_regular` |
| 8 | Diet / zero cola | `cola_diet` |
| 9 | Sports drink | *Part B* |
| 10 | Energy drink, or another Part B pick such as iced tea or oat milk | *Part B* |
| 11 | Smoothie | `smoothie_fruit_dairy` |
| 12 | Protein shake | `protein_shake_rtd` |

Part A alternates if a slot is freed: apple juice, lemonade, coconut water, whole milk, lemon-lime soda. After a week of use, the app should replace these defaults with the user's own most-logged drinks.

---

## 10. Source list
- USDA FoodData Central. SR Legacy (April 2018), FNDDS 2021–2023 (published Oct 2024), and Foundation Foods. Record pages follow `https://fdc.nal.usda.gov/food-details/<fdcId>/nutrients`; every FDC ID is in the JSON.
- Health Canada, Canadian Nutrient File (2015), via the public API at `food-nutrition.canada.ca/api/canadian-nutrient-file/`.
- The Coca-Cola Company (US): Coca-Cola Original product page (caffeine 34 mg / sugar 39 g per 12 fl oz); Coke Zero Sugar, Diet Coke, Sprite and Fanta product pages; "What is caffeine?" FAQ (Diet Coke 46 mg). All on coca-cola.com/us/en/…
- The Coca-Cola Company (GB): Fanta nutritional information (per 100 mL), coca-cola.com/gb/en/brands/fanta.
- PepsiCo: Beverage Facts nutrition sheets for Pepsi and Diet Pepsi (fountain, last updated 28 Jul 2022, downloaded via a foodservice distributor); pepsicoproductfacts.com product pages for Pepsi 16.9 fl oz (53 mg), Diet Pepsi 12 fl oz (35 mg), Diet Pepsi Caffeine Free, and Pepsi Zero Sugar Wild Cherry & Cream (38 mg).
- Keurig Dr Pepper / Dr Pepper and PepsiCo Mountain Dew: 12 fl oz label values as shown by US grocery retailers (Giant, Food Lion, Lowe's Foods, HEB). KDP's own product-facts site is script-rendered.
- The Grocer (UK), "Reformulated: the soft drinks that have slashed sugar", for the March 2017 Fanta Orange reformulation to 4.6 g/100 mL.
