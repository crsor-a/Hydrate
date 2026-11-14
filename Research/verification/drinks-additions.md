# Drink database additions (verification pass)

**Companion data:** `drinks-additions.json`, a JSON array of **56 new entries** (validated with `python3 -m json.tool`). No id or name collides with the 173 entries in `03a-drinks-part-a.json` / `03b-drinks-part-b.json`, and every entry uses an existing category string.
**Compiled:** 14 Nov 2026. All nutrient values are per 100 mL. `hydrationFactor` is `null` throughout, as in Parts A and B.
**Scope:** additions only. Existing entries were not edited; where a new entry overlaps an existing generic (for example 7UP vs `lemon_lime_soda`), the note says how the two relate.

| Category | New | High | Medium | Low |
|---|---|---|---|---|
| alcohol | 16 | 1 | 12 | 3 |
| soda | 10 | 6 | 4 | 0 |
| sports | 7 | 5 | 2 | 0 |
| energy | 4 | 0 | 3 | 1 |
| tea | 4 | 1 | 2 | 1 |
| dairy | 4 | 1 | 1 | 2 |
| juice | 4 | 2 | 2 | 0 |
| coffee | 3 | 2 | 1 | 0 |
| water | 2 | 1 | 1 | 0 |
| plant milk | 1 | 1 | 0 | 0 |
| other | 1 | 0 | 1 | 0 |
| **Total** | **56** | **20** | **29** | **7** |

---

## 1. Method

### 1.1 Sources, in order of preference
1. **USDA FoodData Central (FDC)**
   - **SR Legacy and FNDDS 2021-2023** for generic drinks and cocktails (horchata, aloe drink, tamarind agua fresca, iced latte, sangria, mojito, mimosa, Moscow mule, Bloody Mary, mulled wine, Long Island iced tea, liqueurs, port). FNDDS records also carry their **recipe inputs**, and each cocktail note restates that recipe.
   - **FDC Branded Foods** (label data supplied by manufacturers through GS1/Label Insight) for 30 brand entries. These records already express label values per 100 mL. Each entry cites one record, normally the most recent one with complete data, and names sibling records in `source.crossCheck`.
   - Records were read from the public portal endpoints behind fdc.nal.usda.gov (`/portal-data/external/search` and `/portal-data/external/{fdcId}`). The API `DEMO_KEY` was already rate-limited (HTTP 429) at the start, so it was not used.
2. **Japan Standard Tables of Food Composition (MEXT, 8th revision, 2023 supplement)** for barley tea and sake.
3. **Manufacturer pages** for Nuun Sport (nutrition panel), LMNT (per-stick electrolytes), Yerba Madre/Guayakí (can panel) and JuneShine (can panel).
4. **Peer-reviewed analysis:** Bastos et al. 2005 (HPLC caffeine in chimarrão, tereré and mate tea).
5. **Secondary caffeine sources.** Caffeine Informer was used where it cites the manufacturer's facts site (KDP or PepsiCo): Sunkist, Diet Dr Pepper, Diet Mountain Dew, Starbucks bottled drinks, A&W and Mug. US grocery-retailer copies of labels were used where nothing better could be read (Monster Zero Ultra, Alani Nu, Reign, Prime Energy, Guayakí caffeine). Each of these is marked medium or low.

### 1.2 Conversions and conventions
- **Density.** Per-100 g data were converted with `per100mL = per100g x density`, and the density is stored in `densityGPerML`. It comes from the record's own USDA portion weight where possible: horchata and tamarind 1.048, aloe 1.014, port 0.9975, cream liqueur 1.052, coffee liqueur 1.177, sake 0.984 (USDA sake record), iced latte 1.014. FNDDS mixed drinks without a usable volume portion use an assumed 1.00 (1.02 for Bloody Mary), and the note says so.
- **Brand entries.** FDC Branded per-100 mL values are used as published. For sodas, `waterG` is copied from the analog generic used in Part A, and the analog is recorded in `source.waterFrom` (Part A's convention). For energy, sports and other label-only drinks, `waterG` is `null` (Part B's convention), because labels do not state water.
- **Alcohol.** `alcoholG` is grams of ethanol per 100 mL and `abvPercent = alcoholG / 0.789`. Cocktail composites state the recipe in mL, convert each component with its USDA density, ignore ice melt (as Part B did) and sum the components.
- **Nulls.** `null` means not verified, never zero. Zero caffeine is given only where the ingredient list or the source shows the drink is caffeine-free.

---

## 2. Notes by category

### Soda (10)
- **Brand entries** (7UP, A&W, Mug, Canada Dry, Sunkist, Diet Dr Pepper, Diet Mountain Dew) fill the gap Part A §7 listed: "no primary source could be read". FDC Branded supplies the manufacturer labels.
- **Caffeine surprises:**
  - **Sunkist** contains caffeine: 19 mg per 12 oz, with caffeine on the ingredient list. Part A's `orange_soda` has caffeine `null`.
  - **Diet Mountain Dew** has 54 mg per 12 oz. Three sources agree: FDC Branded (15 mg/100 mL), Caffeine Informer citing PepsiCo, and FNDDS 2710554.
  - **Diet Dr Pepper** has 41 mg per 12 oz.
- **Diet tonic** uses the Canada Dry label. No Schweppes diet tonic record was found.
- **Olipop and Poppi** are prebiotic sodas whose carbohydrate is mostly fiber, so `carbsG` is much greater than `sugarG`. No water analog fits them, so `waterG` is `null`.
- **Not added:** LaCroix and Bubly are already covered by `water_sparkling_flavored`. Liquid Death has no FDC record and no manufacturer panel could be read; still and sparkling Liquid Death map to the existing bottled and sparkling water entries.

### Water (2)
- **Topo Chico** has 4 mg Na/100 mL. The generic seltzer entry carries club-soda sodium (21 mg/100 mL).
- **Lemon water** is a composite: 240 mL tap water plus 15 mL lemon juice. It is about 1 kcal/100 mL, so for hydration purposes it is essentially water.

### Energy (4)
- Monster Zero Ultra, Alani Nu, Reign and Prime Energy were added.
- Nutrients come from FDC Branded. Caffeine comes from retailer label copies, because the manufacturer sites block automated access.
- **C4 Energy was not added.** At 200 mg per 16 oz it has the same caffeine concentration as Part B's `energy_ghost`, which already lists C4 as a brand example.
- Red Bull editions use the same base formula as `energy_red_bull`, so they were not added either.

### Sports (7)
- **Added:** Gatorade Zero, Gatorlyte, BODYARMOR LYTE, Electrolit, Nuun Sport, LMNT and protein water.
- **Sodium per 100 mL, for comparison:**

  | Drink | Na mg/100 mL |
  |---|---|
  | BODYARMOR LYTE | 8 |
  | Gatorade Zero | 45 |
  | Nuun (16 oz) | 63 |
  | Electrolit | 69 |
  | Gatorlyte | 83 |
  | Pedialyte (Part B) | 108 |
  | LMNT (16 oz) | 211 |

- **Tablets and sticks** (Nuun, LMNT) assume a 16 oz dilution, so per-tablet or per-stick logging is recommended.
- **Nuun reformulation.** The current manufacturer panel (300 mg Na, 150 mg K) differs from the 2021 FDC record (about 360 mg Na, 100 mg K). The current panel is used.
- **Protein water.** Several Protein2o flavors list caffeine as an ingredient without stating an amount, so `caffeineMg` is `null`.

### Coffee (3)
- **Starbucks bottled Frappuccino.** Caffeine is uncertain: the cited source gives 110 mg in one place and 130 mg in another. 110 mg is used, with a range of 11-32 mg/100 mL to cover the different flavors.
- **Starbucks Doubleshot Espresso & Cream** has 120 mg per 6.5 oz can.
- **Iced latte** comes from FNDDS. Its recipe already includes ice melt.
- **Not added:** Starbucks iced matcha latte and cold-foam cold brew. Starbucks' nutrition pages need JavaScript, and third-party figures disagreed.

### Tea (4)
- **Yerba mate (brewed)** combines FNDDS herbal-tea macros (that record explicitly includes mate tea) with Bastos et al. caffeine:
  - chimarrão: 27 mg/100 mL
  - tereré: 17 mg/100 mL
  - mate cocido: 7 mg/100 mL
- **Canned Guayakí** has about 150 mg caffeine and 28 g sugar per 15.5 oz can.
- **Barley tea** values come from MEXT, and the drink is caffeine-free.
- **Thai iced tea** is a bottled product, with caffeine `null`.
- **Not added:** jasmine and Earl Grey. They are scented green and black teas covered by `tea_green` and `tea_black`, and no separate caffeine analysis was found. Turmeric latte was also not added, because no database record was found.

### Dairy (4)
- **Yakult** uses the 2024 FDC Branded record. It has 12.5 g sugar/100 mL.
- **Mango lassi and sweet lassi** come from a single brand each. No USDA or CoFID generic was found.
- **Ayran** is salty: about 312 mg Na/100 mL.
- **Salted lassi (chaas)** was not added for lack of a source. Ayran is the closest entry.

### Juice and other (5)
- **Martinelli's sparkling cider** is 100% apple juice.
- **Clamato** has 333 mg Na/100 mL.
- **Aloe vera drink** uses the USDA SR record, which is the light end of the category.
- **Agua de tamarindo** uses the FNDDS recipe, which is very sweet.
- **Horchata** uses the USDA SR restaurant record, which is analytical. Part B §10 listed it as a gap.
- **Sikhye** was not added, because no FDC, MEXT or other open record was found.

### Plant milk (1)
- **Oatly Barista** has more fat than Oatly Original. That extra fat is what makes it foam.

### Alcohol (16)
- **FNDDS cocktails.** Sangria, mojito, mimosa, Moscow mule, Bloody Mary, mulled wine ("Glug") and Long Island iced tea. Each note gives the FNDDS recipe and any stand-in ingredient. For example, FNDDS uses cilantro in place of mint in the mojito, ginger ale plus sugar in place of ginger beer, and white table wine in place of champagne in the mimosa.
- **Composites:**
  - Cosmopolitan, IBA-style: 40/15/15/30 mL.
  - Aperol Spritz, 3-2-1. It uses the Aperol EU label: 159 kcal, 26.1 g sugar per 100 mL, 11% vol.
- **Sake** uses MEXT rather than USDA. USDA SR 167723 implies about 20% ABV, which Part B already flagged. MEXT with the USDA density gives 15.3% ABV.
- **Coffee liqueur.** The USDA SR record's alcohol (21.7 g/100 g) contradicts its own "53 proof" label once converted to volume. `alcoholG` therefore follows the stated proof, and energy was recomputed. Low confidence.
- **Cream liqueur** uses USDA SR "coffee with cream, 34 proof". Its computed 18.4% ABV is slightly above Baileys' 17%.
- **Port** is USDA SR sweet dessert wine, 19.3% ABV.
- **Hard kombucha** uses the JuneShine panel, 6% ABV.
- **Guinness-type stout** uses secondary sources only: 125 kcal and 4.2% per 12 oz.
- **Soju** has a sourced ABV (16%), but its energy and sugar are `null`.

---

## 3. Additions table

| id | Name | Category | Key source | Confidence |
|---|---|---|---|---|
| `seven_up` | 7UP | soda | FDC Branded 2109524 | high |
| `aw_root_beer` | A&W Root Beer | soda | FDC Branded 2571090 | high |
| `mug_root_beer` | Mug Root Beer | soda | FDC Branded 2494406 | high |
| `canada_dry_ginger_ale` | Canada Dry Ginger Ale | soda | FDC Branded 2571107 | high |
| `sunkist_orange` | Sunkist Orange Soda | soda | FDC Branded 2442918 + Caffeine Informer (KDP) | medium |
| `diet_dr_pepper` | Diet Dr Pepper | soda | FDC Branded 2110838 + Caffeine Informer (KDP) | high |
| `diet_mountain_dew` | Diet Mountain Dew | soda | FDC Branded 1457612 / 1457183 | high |
| `tonic_water_diet` | Tonic water, diet / zero | soda | FDC Branded 2111431 (Canada Dry) | medium |
| `olipop` | Olipop (prebiotic soda) | soda | FDC Branded 2584830 | medium |
| `poppi` | Poppi (prebiotic soda) | soda | FDC Branded 2551032 | medium |
| `topo_chico` | Topo Chico Mineral Water | water | FDC Branded 2561564 | high |
| `water_lemon` | Lemon water | water | USDA SR 173647 + 167747 (composite) | medium |
| `energy_monster_zero_ultra` | Monster Energy Zero Ultra | energy | FDC Branded 2597762 + retailer caffeine | medium |
| `energy_alani_nu` | Alani Nu Energy | energy | FDC Branded 2554138 + retailer caffeine | medium |
| `energy_reign` | Reign Total Body Fuel | energy | FDC Branded 2604284 + retailer caffeine | medium |
| `energy_prime` | Prime Energy | energy | Retailer label copies (HEB, Kroger, Safeway) | low |
| `sports_gatorade_zero` | Gatorade Zero Sugar | sports | FDC Branded 2597050 | high |
| `sports_gatorlyte` | Gatorlyte | sports | FDC Branded 2502060 | high |
| `sports_bodyarmor_lyte` | BODYARMOR LYTE | sports | FDC Branded 2670350 | high |
| `sports_electrolit` | Electrolit | sports | FDC Branded 2652442 | high |
| `sports_nuun_sport` | Nuun Sport (tablet in 16 oz) | sports | nuunlife.com panel | high |
| `sports_lmnt` | LMNT (stick in 16 oz) | sports | drinklmnt.com | medium |
| `sports_protein_water` | Protein water | sports | FDC Branded 2670366 (Protein2o) | medium |
| `coffee_starbucks_frappuccino_bottled` | Starbucks Frappuccino (bottled) | coffee | FDC Branded 540579 + Caffeine Informer (PepsiCo) | medium |
| `coffee_starbucks_espresso_cream` | Starbucks Doubleshot Espresso & Cream | coffee | FDC Branded 2560212 + Caffeine Informer (PepsiCo) | high |
| `coffee_iced_latte` | Iced Latte | coffee | FNDDS 2710431 | high |
| `tea_yerba_mate` | Yerba mate (brewed / gourd) | tea | Bastos et al. 2005 + FNDDS 2710502 | medium |
| `tea_yerba_mate_canned` | Yerba mate, canned (Guayakí) | tea | FDC Branded 2585798 + Yerba Madre panel | medium |
| `tea_barley_mugicha` | Barley tea (mugicha) | tea | MEXT 16055 | high |
| `tea_thai_iced` | Thai iced tea (bottled) | tea | FDC Branded 1957353 (FOCO) | low |
| `yakult` | Yakult | dairy | FDC Branded 2719414 | high |
| `lassi_mango` | Mango lassi | dairy | FDC Branded 2490375 (Deep) | medium |
| `lassi_sweet` | Sweet lassi | dairy | FDC Branded 1892140 (Deep) | low |
| `ayran` | Ayran / doogh | dairy | FDC Branded 2066050 (Byblos) | low |
| `sparkling_cider_na` | Sparkling cider (non-alcoholic) | juice | FDC Branded 2596277 (Martinelli's) | high |
| `clamato` | Clamato | juice | FDC Branded 2560714 | high |
| `aloe_vera_drink` | Aloe vera drink | juice | USDA SR 174131 | medium |
| `agua_fresca_tamarindo` | Agua fresca, tamarind | juice | FNDDS 2710568 | medium |
| `horchata` | Horchata | other | USDA SR 171941 | medium |
| `plant_oat_barista` | Oat milk, barista edition | plant milk | FDC Branded 2462067 (Oatly) | high |
| `alc_sake` | Sake | alcohol | MEXT 16001 | medium |
| `alc_soju` | Soju | alcohol | LCBO label ABV | low |
| `alc_sangria` | Sangria (red) | alcohol | FNDDS 2710695 | medium |
| `alc_mojito` | Mojito | alcohol | FNDDS 2710644 | medium |
| `alc_cosmopolitan` | Cosmopolitan | alcohol | USDA composite (SR 174818, FNDDS 2710623, SR 168156, SR 171903) | medium |
| `alc_mimosa` | Mimosa | alcohol | FNDDS 2710642 | medium |
| `alc_aperol_spritz` | Aperol Spritz | alcohol | FNDDS 2710687 + Aperol EU label + SR 174842 | medium |
| `alc_moscow_mule` | Moscow Mule | alcohol | FNDDS 2710645 | medium |
| `alc_bloody_mary` | Bloody Mary | alcohol | FNDDS 2710628 | medium |
| `alc_mulled_wine` | Mulled wine | alcohol | FNDDS 2710698 | medium |
| `alc_long_island_iced_tea` | Long Island Iced Tea | alcohol | FNDDS 2710679 | medium |
| `alc_coffee_liqueur` | Coffee liqueur | alcohol | USDA SR 175097 (alcohol from stated proof) | low |
| `alc_cream_liqueur` | Cream liqueur | alcohol | USDA SR 175098 | medium |
| `alc_port` | Port / sweet fortified wine | alcohol | USDA SR 173176 | high |
| `alc_hard_kombucha` | Hard kombucha | alcohol | juneshine.com panel | medium |
| `alc_beer_stout` | Stout (Guinness-type) | alcohol | Healthline / Food Republic | low |

---

## 4. Gaps and caveats
1. **Not added for lack of a usable source:**
   - Liquid Death (still and sparkling). It is plain water, so the existing water entries cover it.
   - Starbucks iced matcha latte and cold-foam cold brew. The Starbucks site needs JavaScript.
   - Turmeric latte, sikhye, salted lassi, and a Schweppes-specific diet tonic.
2. **Covered by existing entries, so skipped:**
   - LaCroix and Bubly (`water_sparkling_flavored`).
   - C4 Energy (`energy_ghost`, same 200 mg/16 oz).
   - Red Bull editions (`energy_red_bull`).
   - Earl Grey and jasmine (`tea_black`, `tea_green`).
3. **Caffeine taken from retailer label copies** (medium/low): Monster Zero Ultra (140 mg; some listings say 150), Alani Nu, Reign, Prime Energy, Guayakí canned. If possible, recheck these against a physical can or the manufacturer site in a browser.
4. **Caffeine unknown (`null`):** Thai iced tea, protein water (some flavors caffeinated, amount undeclared), hard kombucha.
5. **Internal inconsistencies in sources:**
   - USDA SR coffee liqueur: alcohol vs proof.
   - Caffeine Informer's bottled Frappuccino: 110 vs 130 mg.
   - The SR horchata portion weight (likely includes ice).
6. **Water `null`** for label-only energy and sports drinks, Olipop, Poppi, soju, Aperol Spritz, hard kombucha and stout. The hydration-factor track may want analog water values. For zero-sugar drinks, ~99.5 g is a reasonable analog, but it was not entered because it is not sourced.
7. **Formulas change:** Nuun was reformulated, and Monster, Reign and Prime vary by flavor. FDC Branded records are dated 2021-2024. Recheck yearly, as Part B recommends.
8. **Densities assumed at 1.00** for most FNDDS cocktails, which gives roughly ±2% on per-mL values.

---

## 5. References
1. USDA FoodData Central (SR Legacy, FNDDS 2021-2023, Branded Foods). Record pages: `https://fdc.nal.usda.gov/food-details/<fdcId>/nutrients` (each ID in the JSON). Portal search used: https://fdc.nal.usda.gov
2. Japan MEXT, Standard Tables of Food Composition in Japan (8th rev., 2023 suppl.): barley tea infusion https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=16_16055_7 ; sake, regular https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=16_16001_7
3. Bastos DHM, Fornari AC, Queiroz YS, Soares RAM, Torres EAFS. The chlorogenic acid and caffeine content of yerba maté (Ilex paraguariensis) beverages. *Acta Farm. Bonaerense* 2005;24(1):91-95. https://www.e-lactancia.org/media/papers/MateCafeina-ActFarmBona2005.pdf
4. Nuun Sport product page (nutrition panel and directions). https://nuunlife.com/products/nuun-sport
5. LMNT formulation page. https://drinklmnt.com/pages/ingredients
6. Yerba Madre (Guayakí) Revel Berry nutrition panel. https://yerbamadre.com/products/revel-berry
7. JuneShine Ocean Squeeze nutrition panel. https://juneshine.com/products/ocean-squeeze-1
8. Caffeine Informer, Sunkist Orange Soda (cites sunkistsoda.com, kdpproductfacts.com). https://www.caffeineinformer.com/caffeine-content/sunkist-orange-soda
9. Caffeine Informer, Diet Dr Pepper (cites drpepper.com, kdpproductfacts.com). https://www.caffeineinformer.com/caffeine-content/diet-dr-pepper
10. Caffeine Informer, Diet Mountain Dew (cites PepsiCo Beverage Facts). https://www.caffeineinformer.com/caffeine-content/diet-mountain-dew
11. Caffeine Informer, Starbucks Espresso and Cream (cites pepsicoproductfacts.com). https://www.caffeineinformer.com/caffeine-content/starbucks-espresso-and-cream
12. Caffeine Informer, Starbucks bottled Frappuccino (cites pepsicobeveragefacts.com). https://www.caffeineinformer.com/caffeine-content/starbucks-bottled-frappucino
13. Caffeine Informer, A&W Root Beer. https://www.caffeineinformer.com/caffeine-content/aw-root-beer ; Mug Root Beer. https://www.caffeineinformer.com/caffeine-content/mug-root-beer
14. Monster Zero Ultra label copy (Harris Teeter). https://www.harristeeter.com/p/monster-zero-ultra-energy-drink/0007084701712
15. Alani Nu label copy (Safeway). https://www.safeway.com/shop/product-details.970307026.html
16. Reign Total Body Fuel label copy (HEB). https://www.heb.com/product-detail/reign-total-body-fuel-energy-drink-orange-dreamsicle/3335244
17. Prime Energy label copy (HEB). https://www.heb.com/product-detail/prime-energy-drink-blue-raspberry/9045077
18. Guayakí Revel Berry retailer listing (caffeine). https://hannaford.com/groceries/beverages/tea/yerba-mate/guayaki-organic-revel-berry-yerba-mate-herbal-tea-155-oz-can.html
19. Aperol 11% per-100 mL label (Delicando). https://www.delicando.com/en/products/10813-aperol-aperitivo-11-vol-07l ; cross-check (Frankfurt Airport shop). https://shop.frankfurt-airport.com/en-US/product/aperol-likoer-11-1l_4cd7b26a1bf2358c
20. LCBO, Jinro Chamisul Fresh (16% ABV). https://www.lcbo.com/en/jinro-chamisul-fresh-13612
21. Healthline, Guinness ABV and nutrition. https://www.healthline.com/nutrition/guinness-abv ; Food Republic, Guinness calories. https://www.foodrepublic.com/1292700/does-guinness-really-have-as-many-calories-as-bud-light
22. NIAAA standard drink (14 g ethanol), as used in Part B. https://www.niaaa.nih.gov/alcohols-effects-health/what-standard-drink
