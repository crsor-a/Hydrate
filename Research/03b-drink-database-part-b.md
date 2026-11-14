# Hydrate drink database, Part B: coffee, tea, energy, sports, plant milks, alcohol, other

Companion data file: `03b-drinks-part-b.json` (92 entries, valid JSON checked with `python3 -m json.tool`).
Part A (sodas, juices, dairy milk, water variants, smoothies) is a separate file. A few Part B entries touch Part A's scope; they are flagged in Section 7 so they can be de-duplicated when the two files are merged.

| Category | Entries | High | Medium | Low |
|---|---|---|---|---|
| coffee | 20 | 13 | 7 | 0 |
| tea | 16 | 7 | 7 | 2 |
| energy | 11 | 3 | 8 | 0 |
| sports | 10 | 5 | 5 | 0 |
| plant milk | 10 | 8 | 2 | 0 |
| alcohol | 19 | 7 | 12 | 0 |
| other | 6 | 3 | 2 | 1 |
| **Total** | **92** | **46** | **43** | **3** |

---

## 1. Method

### 1.1 Order of sources (best first)
1. **USDA FoodData Central (FDC)**, in this order:
   - **Foundation Foods**: lab-analysed values (used for soy milk and oat milk).
   - **SR Legacy**: the classic National Nutrient Database. Used for brewed coffee, espresso, teas, the Red Bull, Monster and Rockstar records, wines, beers and spirits.
   - **FNDDS 2021-2023 (Survey)**: recipe-based records for prepared drinks such as latte, cappuccino, mocha, iced coffee, bubble tea, kombucha, margarita, sparkling wine and hard seltzer.
   - Every USDA entry records its `fdcId` and a link to `fdc.nal.usda.gov/food-details/<id>/nutrients`.
2. **Manufacturer label data** for branded energy and sports drinks. Sources were Abbott's Pedialyte page, Oatly's US page, Sierra Nevada's brew page, Campbell's V8 page, Red Bull's site and a PepsiCo Gatorade nutrition sheet. Where the manufacturer page could not be read, the current label was taken as shown on US grocery-retailer listings (H-E-B, Lowes Foods, Stop & Shop and others). Each entry's note says which.
3. **Peer-reviewed caffeine studies** for ranges:
   - McCusker et al. 2003 (*J Anal Toxicol* 27:520), specialty coffee
   - McCusker et al. 2006 (*J Anal Toxicol* 30:611), decaf
   - Chin et al. 2008 (*J Anal Toxicol* 32:702), brewed teas
   - Fuller & Rao 2017 (*Sci Rep* 7:17979), cold brew vs hot brew
   - Min, Green & Kim 2017 (*Food Sci Nutr*), boba milk tea
4. **Standards bodies**:
   - NIAAA US standard drink: 14 g ethanol.
   - NHS UK unit: 10 mL or 8 g ethanol.
   - WHO/UNICEF reduced-osmolarity ORS composition.
   - FDA guidance of 400 mg caffeine/day for most adults (as quoted on CSPI's caffeine page).
5. **Other national databases for cross-checks**:
   - UK CoFID, via reproductions of its coffee and tea infusion values.
   - Norway's Matvaretabellen (whole-milk caffè latte, also used as the flat-white base).
   - Japan's Standard Tables of Food Composition (matcha, sencha and gyokuro caffeine, via secondary summaries).
6. **Coffee-shop disclosures** (Starbucks) for caffeine in coffee-shop drinks. Secondary listings were used because the Starbucks site needs JavaScript. The CSPI caffeine chart page also loads its table with JavaScript, so its numbers could not be read directly; Starbucks, Bang and Ghost values cited elsewhere match the CSPI-sourced figures.

### 1.2 How values were obtained
- **USDA FDC API.** SR Legacy beverages (all 371 records) and FNDDS coffee records were pulled from the API with the public `DEMO_KEY`. That key's daily quota (about 10 calls per hour, shared per IP) ran out partway through.
- **Third-party mirror.** The remaining FNDDS and Foundation records were read from getfoodfacts.com, which republishes FDC data with FDC IDs. Its cappuccino record (2710472) matched the API exactly, so it was trusted for: latte 2710386, bubble tea 2710508, kombucha 2710509, sweet iced tea 2710515, hard seltzer 2710622, margarita 2710638, sparkling wine 2710687, soy milk 1999630, oat milk 2257046 and chicken broth 174536. **The mirror does not display caffeine**, so caffeine for those records is either taken from a sister record, estimated, or left null; each note says which.
- **Before shipping**, re-pull those 10 IDs with a free api.data.gov key (see Section 8).

### 1.3 Unit conversion (per 100 g to per 100 mL)
The schema is per 100 mL, but USDA reports per 100 g. Each value was multiplied by a density (g/mL), and the density used is stated in each entry's `notes`:

| Drink type | Density used | Basis |
|---|---|---|
| Brewed coffee, tea, espresso, broth, zero-sugar drinks | 1.00 | under 2% dissolved solids |
| Plant milks | 1.01 (almond, coconut) to 1.03 (soy, oat, rice) | milk-like emulsions |
| Lattes and cappuccinos | 1.02-1.03 | milk-based (cappuccino foam lowers it) |
| Sports drinks, sweet tea | 1.03 | about 6-8% sugar solution |
| Energy drinks, mocha, frappé, hot chocolate | 1.04-1.05 | about 10-13% sugar |
| Beer, cider | 1.005-1.01 | |
| Wine | 0.993-0.995 | about 12-13% ethanol |
| 40% spirits | 0.948 | ethanol-water density table |

The density adds at most about 5% error, which is smaller than real brand-to-brand variation. For label-based entries the per-serving label values were divided by the labelled volume, so no density was needed.

### 1.4 Alcohol
- `alcoholG` is grams of ethanol per 100 mL.
- `abvPercent` = `alcoholG / 0.789` (ethanol density 0.789 g/mL).
- The app can compute grams per serving as `alcoholG x mL / 100`, then:
  - **US standard drinks** = grams / 14 (NIAAA)
  - **UK units** = grams / 8 (NHS: one unit = 10 mL = 8 g pure alcohol)
  - Other definitions to offer in a locale setting: 10 g (Australia, NZ) and 20 g (Austria).
- Checks against NIAAA examples:
  - USDA regular beer comes out at 3.94 g/100 mL = 5.0% ABV, so a 355 mL can is 14.0 g, exactly one US standard drink.
  - USDA 80-proof spirits come out at 31.7 g/100 mL = 40% ABV, so a 44 mL shot is 13.9 g.

### 1.5 Caffeine ranges
`caffeineRangePer100mL` is the plausible real-world spread for the same named drink. It is set where caffeine varies a lot (by brew method, shop or shot count) and null where the label fixes caffeine or it is zero. Narrow ranges such as `[56, 57]` on brand cans just bracket the label value. Suggested UI: show "approx. X mg (typically Y-Z)" and offer a "stronger/weaker" slider or a custom value.

### 1.6 Nulls
**58 nutrient fields are null.** A value was left null whenever it could not be verified from a source; nothing was guessed. Typical cases:
- **Matcha:** energy, protein and minerals of the powder.
- **5-hour Energy:** everything except caffeine.
- **Celsius:** carbs and potassium.
- **Starbucks chai:** sodium and potassium.
- **IPA:** sugar, sodium and potassium (Sierra Nevada does not publish them).
- **Pea milk, Oatly, V8:** potassium.
- **Bubble tea and kombucha:** caffeine.

The app should treat null as "unknown", not zero, in summaries.

---

## 2. Coffee (20 entries)

**Core records.** USDA SR brewed coffee (FDC 171890: 40 mg caffeine/100 mL, about 95 mg per 8 oz) and espresso (171891: 212 mg/100 g, about 64 mg per 30 mL shot) anchor the category. FNDDS supplies the milk drinks:
- latte 2710386
- nonfat latte 2710387
- plant-milk latte 2710388
- cappuccino 2710472
- mocha 2710410
- macchiato 2710382
- iced coffee 2710428
- frozen blended 2710398
- bottled coffee 2710478
- Cuban coffee 2710381

**Caffeine varies by brew method and by shop:**
- **McCusker et al. 2003.** Brewed specialty coffee ranged 58-259 mg per 16 oz (about 12-55 mg/100 mL). The same Starbucks Breakfast Blend ranged 259-564 mg/16 oz across six days. Espresso was steadier, at about 75 mg per shot.
- **Starbucks publishes:**
  - grande Pike Place: 310-315 mg (about 66 mg/100 mL)
  - grande Americano: 225 mg
  - grande latte or cappuccino: 150 mg
  - grande flat white: 195 mg
  - grande cold brew: 205 mg (Nitro 280 mg)
- **Cold brew.** Fuller & Rao 2017 brewed at 1:10 and found 990-1230 mg/L for cold brew vs 840-1060 mg/L for hot brew. Cold brew is not inherently stronger; its caffeine depends on the grind-to-water ratio and dilution. The database default is the Starbucks per-mL figure, with a range up to 125 mg/100 mL for undiluted concentrate.
- **Decaf is not caffeine-free.** McCusker 2006 found 0-13.9 mg per 16 oz brewed decaf and **3-15.8 mg per decaf espresso shot**. USDA lists only 1 mg/100 g for decaf espresso, so its range goes to 53.

**Judgment calls:**
- **Americano** has no USDA record. It is derived from USDA espresso (3 shots in 473 mL), with caffeine from Starbucks.
- **Cold brew** uses USDA brewed-coffee nutrients as a proxy, with Starbucks caffeine.
- **Flat white** has no USDA record. Its macros use Norway's whole-milk latte record and its caffeine is Starbucks'. Classic 160-180 mL Australian/UK flat whites are about twice as concentrated, hence the range of 35-85.
- **Latte caffeine (36 mg/100 g)** comes from the sister FNDDS records, all of which list 36.
- **Single and double espresso** share per-100 mL data; only the default serving differs. The picker can also simply offer a "shots" stepper.
- **Cross-checks.** UK CoFID "coffee, infusion, average" is about 2 kcal/100 g, consistent with USDA's 1. Norway's whole-milk latte (59 kcal/100 g) is richer than FNDDS's latte (43 kcal/100 g), because FNDDS uses reduced-fat milk.

## 3. Tea (16 entries)

**Core records.** USDA SR brewed black tea (20 mg/100 mL), green (12), oolong (16), decaf black (1), herbal, chamomile and hibiscus (0).

**Caffeine range.** Chin et al. 2008 tested 20 commercial teas and found 14-61 mg per 6- or 8-oz serving (about 6-36 mg/100 mL), with **no consistent difference between white, green and black**; steep time mattered more. All brewed teas therefore share a range of `[6, 36]`. Decaf teas were under 12 mg per serving, and herbal teas had no detectable caffeine.

**Entries built from proxies or derivations:**
- **White tea** uses the green tea record as a proxy (low confidence). The popular claim that white tea has the least caffeine is not supported by Chin et al.
- **Rooibos** uses USDA's herbal tea record (it is naturally caffeine-free).
- **Matcha:** 32 mg/g from the Japanese Standard Tables (via secondary summaries). 2 g in 240 mL gives 26.7 mg/100 mL. Other published figures run 19-44 mg/g, and traditional usucha (2 g in about 70 mL) is about 90 mg/100 mL. Low confidence; macros are null.

**Iced and bottled tea:**
- **Sweet iced tea:** FNDDS 2710515 gives 32 kcal and 7.7 g sugar per 100 g. Its caffeine (18 mg/100 mL) is estimated from brewed black tea and marked as an estimate.
- **Unsweetened iced tea:** USDA's Wendy's restaurant brewed iced tea (8 mg/100 mL).
- **Bottled black and green teas:** USDA SR.

**Milk teas:**
- **Chai latte:** Starbucks grande with 2% milk (240 kcal, 42 g sugar, 95 mg caffeine).
- **Bubble tea:** FNDDS 2710508 gives 55 kcal and 3.5 g sugar per 100 g. Shop drinks are often sweeter: Min et al. and shop menus show about 260-300 kcal and about 38 g sugar per 16 oz. The pearls are eaten rather than drunk, which the hydration-factor agent may want to account for.

## 4. Energy drinks (11 entries)

Values are from labels, cross-checked with USDA SR where it has a record.

| Drink | Size | Caffeine | mg/100 mL | Cross-check |
|---|---|---|---|---|
| Red Bull | 250 mL | 80 mg | 32 | USDA SR 173210 consistent |
| Red Bull Sugarfree | 250 mL | 80 mg | 32 | USDA SR 171870 |
| Monster original | 473 mL | 160 mg | 33.8 | USDA SR 171935 consistent |
| Monster Lo-Carb | 473 mL | about 140 mg | 30 | USDA SR 173162 |
| Celsius | 355 mL | 200 mg | 56 | label (retailer) |
| Bang | 473 mL | 300 mg | 63 | label (retailer) |
| Ghost | 473 mL | 200 mg | 42 | label (retailer) |
| 5-hour Energy | 57 mL | 200 mg (Extra Strength 230 mg) | 351-404 | Consumer Reports 2012 measured 215 / 242 mg |
| Rockstar | 473 mL | about 160 mg | 34.5 | USDA SR 171937 |
| Generic sugared / sugar-free | n/a | n/a | n/a | USDA SR 174821 / 174822 |

- **Monster sugar label:** 230 kcal, 54 g sugar, 370 mg sodium per can (older labels say 210 kcal).
- **Bang:** one can comes close to the FDA's 400 mg/day guidance for adults.
- **Celsius:** the label says not to exceed 2 cans a day.
- **Alcohol:** 0 for all.
- **Caffeine in the UI:** caffeine per can matters more than per mL, so the picker should show "mg per can" prominently for this category.

## 5. Sports and electrolyte drinks (10 entries)

| Drink (per labelled serving) | kcal | Sugar | Sodium | Potassium | Source |
|---|---|---|---|---|---|
| Gatorade Thirst Quencher, 591 mL | 140 | 34 g | 270 mg | 80 mg | PepsiCo sheet |
| Gatorade G2 | lower | about 1/4 of regular | same as regular | same as regular | USDA SR 174178 |
| Powerade, 591 mL (current label) | 130 | 34 g | **400 mg** | 130 mg | label |
| Powerade Zero | 0 | 0 | | | USDA SR 171923 |
| BODYARMOR, 473 mL | 110 | 29 g | 30 mg | **680 mg** | label |
| Pedialyte Classic, per L | 70 | 13 g | 1080 mg (about 47 mEq) | 780 mg (20 mEq) | Abbott |
| WHO ORS, per L | 54 | 13.5 g glucose | 1725 mg (75 mmol) | 782 mg (20 mmol) | WHO/UNICEF, 245 mOsm/L |
| Liquid I.V., per stick in 16 oz | 45 | 11 g | 500 mg | about 370 mg | label |
| Prime Hydration, 500 mL | 20-25 | | 10 mg | 700 mg | label |
| Propel Zero | | | | | USDA SR 175109 |

- **Powerade sodium:** the old USDA record says 42 mg/100 g; the current label is higher. Use the label.
- **WHO ORS energy:** computed at 4 kcal per gram of glucose.

**Point for the electrolyte UI.** BODYARMOR and Prime are potassium-heavy and very low in sodium (6 and 2 mg/100 mL). Gatorade is about 46, Powerade about 68, Pedialyte 108 and WHO ORS 172 mg/100 mL. If Hydrate shows electrolytes, show sodium separately; marketing does not reflect it.

## 6. Plant milks (10 entries)

| Milk | kcal/100 mL | Protein/100 mL | Source |
|---|---|---|---|
| Soy, unsweetened | about 40 | 3.7 g | USDA Foundation 1999630 |
| Oat, unsweetened | about 50 | 0.8 g | USDA Foundation 2257046 |
| Almond, unsweetened | 15 | 0.4 g | USDA SR 174832 |
| Almond, sweetened vanilla | | | USDA SR 168751 |
| Almond, chocolate | | | USDA SR 174820 |
| Rice | | | USDA SR 171942 |
| Coconut beverage, sweetened | | | USDA SR 174116 |
| Coconut beverage, unsweetened | | | So Delicious label |
| Oatly Original | | | Oatly US page |
| Pea (Ripple Original) | about 42 | 3.3 g | Ripple page |

- **Hidden sugars.** "Unsweetened" oat and rice milks still contain sugars formed when the grain's starch is broken down. Total sugars were not declared in the Foundation records, so the measured sugars were summed: oat = glucose 0.77 + maltose 1.55 g/100 g.
- **Protein.** Soy and pea are the only plant milks close to cow's milk.
- **Coconut beverage** in a carton is not canned coconut milk (about 170-200 kcal/100 mL) or coconut water.

## 7. Alcohol (19 entries)

**Beer:**
- **Regular** (USDA, 5.0%) and **light** (USDA, about 3.9%; the Bud Light record is 4.2%).
- **Craft IPA** uses Sierra Nevada Hazy Little Thing: 6.7% ABV, 214 kcal, 20.6 g carbs per 12 oz, which is 1.3 US standard drinks. IPAs usually run 5.5-7.5%.
- **Strong / double IPA:** USDA "beer, higher alcohol" at 9.9% ABV. Its kcal and carbs look low for the style and are flagged.
- **Non-alcoholic beer:** USDA malt beverage (about 0.4%).

**Wine and other fermented drinks:**
- **Hard seltzer:** White Claw label (5%, 100 kcal per 12 oz, exactly 1 standard drink), cross-checked with FNDDS (which implies about 4%).
- **Cider:** USDA (about 5.1%).
- **Wines:**
  - red: 13.3% (5 oz = 1.1 standard drinks)
  - white: about 13.0%
  - rosé: 12.1%
  - sparkling (FNDDS): 12.0%
- **Non-alcoholic wine** is also included.

**Spirits:** USDA 80-proof, 40.1% ABV. A 44 mL US shot is one standard drink; a 25 mL UK single is one UK unit.

**Cocktails:**
- **Margarita** (FNDDS, about 10.7% ABV, 1 drink = 225 g = 1.3 standard drinks; high sodium from the salted rim).
- **Piña colada** and **whiskey sour** (USDA SR recipe records).
- **Gin & tonic** and **rum & cola** are composites built from USDA components: 1.5 oz 40% spirit + 4 oz tonic or cola, so about 14 g ethanol and about 11% ABV in the glass. Real bar pours and canned versions vary, so the picker should let the user change the pour (see Section 9).
- **Hard lemonade / flavored malt beverage:** USDA, about 5.2%.

**Serving conventions:**

| Drink | United States | UK | Other |
|---|---|---|---|
| Beer | 355 mL can, 473 mL "pint" | 568 mL imperial pint | EU 330 / 500 mL |
| Wine | 5 oz / 148 mL | 125 / 175 / 250 mL | |
| Spirits | 1.5 oz / 44 mL | 25 or 35 mL | EU often 20 / 40 mL |

Standard-drink definitions differ: 14 g (US), 8 g (UK unit), 10 g (Australia).

**Possible overlap with Part A:** Propel (water variant), vegetable juice (juice), non-alcoholic beer and wine. Part A covers soda, so tonic and cola appear here only as cocktail components.

## 8. Other (6 entries)
- **Kombucha** (FNDDS): 16 kcal and 4 g sugar per 100 g; GT's labels cross-check at about 2.5-3.4 g sugar/100 mL. Caffeine is unknown (null). US "non-alcoholic" kombucha must be under 0.5% ABV; hard kombucha should be logged as alcohol.
- **Chicken broth** (USDA SR 174536): 371 mg sodium/100 g, about 890 mg per cup.
- **Hot chocolate made with milk** (USDA SR homemade) and **cocoa mix made with water** (USDA SR).
- **Vegetable juice:** V8 Original label, 640 mg sodium per 8 oz.
- **Apple cider vinegar drink:** Bragg Refreshers label (low confidence; no national-database record exists).

---

## 9. Recommendations for the drink picker

### 9.1 Custom drinks
A **"Custom drink" form** should store the same schema as the database, so custom drinks flow through the same maths.
- **Required:** name, volume, category.
- **Optional:** caffeine (mg per serving), sugar (g), kcal, ABV (%), sodium (mg).
- **Convert on save:** turn per-serving inputs into per-100 mL.
  - For alcohol, ask for **ABV and volume** rather than grams. Compute `alcoholG = ABV x 0.789` per 100 mL and show "= X US standard drinks / Y UK units" live.
- **Start from an existing drink.** Offer "Start from…" (for example, start from "Energy drink (generic sugar-free)" and edit caffeine to 300 mg). Custom entries then inherit sensible macros and the category's hydration factor.
- **Leave blanks blank.** Fields left empty are stored as null (unknown), not 0, unless the user taps "none".
- **Caffeine guardrails:**
  - Warn when one entry exceeds 200 mg; EFSA considers single doses up to 200 mg safe for healthy adults.
  - Warn when the daily total passes 400 mg (FDA, EFSA).
  - Offer a pregnancy setting at 200 mg/day (EFSA, ACOG).
- **Barcode or label-photo entry** would be nice later. Even then, keep the built-in database offline.

### 9.2 Size modifiers
- Store per 100 mL and let the user pick from `commonServingsML` with localized labels, for example:
  - US: Tall / Grande / Venti; 12 oz can; 16 oz pint
  - UK: 568 mL pint; 175 mL glass
  - Metric: 330 / 500 mL
- Fall back to a free mL/oz entry (1 US fl oz = 29.57 mL; 1 UK fl oz = 28.41 mL).
- For espresso drinks, a **"shots" stepper** is better than size alone, because caffeine follows shots, not cup size. Default shots by size: Starbucks short/tall = 1-2, grande = 2-3, venti = 3-4 (the counts differ between drink types).
- For iced drinks, assume ice takes about 25-40% of cup volume if the user logs the cup size. Better: ask "with ice?" and scale the liquid.

### 9.3 Flavor and add-in modifiers (added to the base drink)

| Modifier | Per unit | Notes |
|---|---|---|
| Extra espresso shot | +64 mg caffeine (USDA, 30 mL); Starbucks about 75 mg | +30 mL volume |
| White sugar, 1 tsp | 4.2 g sugar, 16 kcal | USDA granulated sugar (387 kcal/100 g; 1 tsp = 4.2 g) |
| Sugar packet | about 2.8-4 g sugar, 11-16 kcal | US packets are often 2.8 g; UK sachets about 3-4 g |
| Honey, 1 tsp (about 7 g) | about 5.7 g sugar, 21 kcal | USDA honey 304 kcal/100 g, 82 g sugars/100 g |
| Flavored syrup, 1 pump | about 5 g sugar, 20 kcal | Coffee-shop syrup pump (approximate) |
| Splash of milk (30 mL) | about 15 kcal / 1.5 g sugar (2%); about 18 kcal (whole) | Use Part A's dairy-milk per-100 mL values × 0.3 for exact numbers |
| Plant-milk splash (30 mL) | entry × 0.3 | Use the Part B plant-milk entries |
| Half-and-half, 1 tbsp (15 mL) | about 20 kcal, 1.7 g fat | USDA half-and-half about 131 kcal/100 g |
| Liquid creamer, flavored, 1 tbsp | about 35 kcal, 5 g sugar | Varies by brand; offer custom |
| Whipped cream (drink topping) | about 70-100 kcal | Coffee-shop topping (approximate) |
| Lemon slice / mint | negligible | |
| Sugar-free sweetener | 0 kcal, 0 sugar | |

Modifier values marked "about" are approximate. Verify them against USDA (granulated sugar SR 169655, honey SR 169640) and Part A's milk entries before shipping. Modifiers should add **volume** too (a 30 mL milk splash is 30 mL of fluid) so hydration totals stay right.

---

## 10. Data gaps and follow-ups
1. **Re-check the 10 FDC records read from the mirror** (IDs in 1.2) with a free api.data.gov key. Also pull their **caffeine** values from FDC: plain latte, sweet iced tea, bubble tea and kombucha currently use a sister record, an estimate or null.
2. **Brand labels change**, notably Powerade sodium, Monster kcal and Pedialyte flavors. Recheck yearly; most came from retailer copies of the label.
3. **Fields not verified:** matcha macros; 5-hour Energy nutrients; Celsius carbs and potassium; Prime sugars; Powerade total carbs; chai sodium and potassium; potassium for pea milk, Oatly and V8; IPA sugar, sodium and potassium.
4. **Records that could be improved:**
   - USDA "beer, higher alcohol" macros look implausibly low.
   - FNDDS bubble tea sugar is far below shop drinks.
   - The white tea entry is a proxy.
5. **Not covered (candidates for v2):**
   - yerba mate (caffeinated; must NOT use the herbal tea entry), Thai iced tea, horchata (USDA SR 171941 exists)
   - sake (the USDA record implies about 20% ABV, which looks off)
   - liqueurs, mojito, Long Island iced tea, espresso martini
   - Prime Energy, Gatorade Zero, Monster Zero Ultra
   - coconut water (left to Part A)
6. **CSPI chart** could not be read directly (its table loads with JavaScript). Values that cite CSPI are corroborated by Starbucks and manufacturer figures.

## 11. Main sources
- USDA FoodData Central (SR Legacy, Foundation, FNDDS 2021-2023): https://fdc.nal.usda.gov (per-entry IDs in the JSON).
- McCusker RR, Goldberger BA, Cone EJ. Caffeine content of specialty coffees. *J Anal Toxicol* 2003;27:520-522.
- McCusker RR, Fuehrlein B, Goldberger BA, Gold MS, Cone EJ. Caffeine content of decaffeinated coffee. *J Anal Toxicol* 2006;30:611-613.
- Chin JM, Merves ML, Goldberger BA, Sampson-Cone A, Cone EJ. Caffeine content of brewed teas. *J Anal Toxicol* 2008;32:702-704.
- Fuller M, Rao NZ. The effect of time, roasting temperature, and grind size on caffeine and chlorogenic acid concentrations in cold brew coffee. *Sci Rep* 2017;7:17979 (PMC5740146).
- Min JE, Green DB, Kim L. Calories and sugars in boba milk tea. *Food Sci Nutr* 2017 (doi:10.1002/fsn3.362).
- NIAAA, "What is a standard drink?": https://www.niaaa.nih.gov/alcohols-effects-health/what-standard-drink
- NHS, "Calculating alcohol units": https://www.nhs.uk/live-well/alcohol-advice/calculating-alcohol-units/
- WHO/UNICEF reduced-osmolarity ORS (WHO Drug Information 16(2), 2002): https://www.rehydrate.org/ors/newformula-studies.html
- CSPI caffeine chart: https://www.cspi.org/caffeine-chart (FDA 400 mg/day statement)
- Matvaretabellen (Norway): https://www.matvaretabellen.no/en/caffe-latte-single-with-whole-milk/
- Manufacturer and label pages: Abbott Pedialyte, Oatly US, Sierra Nevada, Campbell's V8, Red Bull, PepsiCo Gatorade sheet; retailer label copies for Monster, Celsius, Bang, Ghost, Powerade, BODYARMOR, Prime, Liquid I.V., White Claw, So Delicious, Bragg. URLs are in each JSON entry.
