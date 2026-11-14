# Beverage Hydration Model for Hydrate

*Research brief, compiled 2026-11-13. Covers the Beverage Hydration Index (BHI) literature from 2016 to 2026, the evidence on caffeine and alcohol diuresis, beverage composition, and a recommended crediting model for the app.*

---

## TL;DR

**Recommended model (v1): count the water a drink actually contains, then subtract two well-evidenced diuretic effects. Never count a drink as more than its water content, and never count it below zero.**

```
water_mL        = volume_mL × waterFraction × hydrationFactor   (hydrationFactor = 1.0 for every category in v1)
caffeinePenalty = 0.5 mL × (caffeine_mg in the 2-h window above 250 mg), capped at 150 mL
alcoholPenalty  = 5 mL × grams of ethanol            (grams = volume_mL × ABV × 0.789)
credit_mL       = max(0, water_mL − caffeinePenalty − alcoholPenalty)
```

- **Show both numbers.** For example, "355 mL logged, counts as 315 mL". The daily goal ring fills with the **credit** (effective hydration). Raw volume stays visible in the log and in history.
- **Coffee and tea count fully.** Normal servings (under about 250 mg caffeine at a time) do not measurably increase urine output, and regular drinkers become tolerant [1][3][14][15][18][19]. Only very strong single servings get a small deduction.
- **Alcohol counts partially.** At typical strengths, beer counts for about 70% of its volume, wine for about 30%, and neat spirits for 0%. Modern controlled studies show roughly 3–5 mL of extra urine per gram of ethanol over the first few hours. The classic figure of about 10 mL/g came from a single subject [23][24][26][27].
- **Milk, oral rehydration solution (ORS) and orange juice score above water on the BHI** (milk about 1.5, ORS about 1.5, orange juice about 1.4) [1]. **They are not credited above their water content.** The app shows a "long-lasting" badge instead. The BHI measures how long fluid is retained over 2–4 hours, not extra water. Over 24 hours, studies find drinks converge [21][22], and individual BHI results are noisy [8].
- **Sugar does not reduce hydration credit.** It actually slows water delivery and slightly raises the BHI [3]. Sugar is shown as health information against the WHO free-sugar guidance [32], not as a hydration penalty.
- Worked results: 355 mL cola → **315 mL**; 250 mL whole milk → **220 mL**; 473 mL cold brew → **470 mL**; 355 mL 5% beer → **255 mL**; 150 mL red wine → **50 mL**; 500 mL sports drink → **475 mL**; 250 mL orange juice → **220 mL**; 250 mL energy drink → **225 mL** (rounded to 5 mL; full arithmetic in §8).

---

## 1. The Beverage Hydration Index (BHI)

### 1.1 Method

Maughan et al. (2016) built the BHI by analogy with the glycemic index [1]:

- **Participants:** 72 healthy, recreationally active men aged 18–35, studied at three UK labs. Each drank still water plus 3 of 12 other drinks in random order, giving n ≈ 15–17 observations per drink and n = 72 for water.
- **Protocol:** After an overnight fast and a 500 mL water pre-load, participants drank **1 L of the test drink over 30 minutes** (4 equal portions). Urine was collected hourly for 4 hours.
- **Index:** BHI = cumulative urine after water ÷ cumulative urine after the test drink, computed per person at **2 hours** after drinking. A BHI above 1 means less urine than with water, so more of the drink is still in the body.
- **Why 2 hours:** differences between drinks first appeared at about 2 hours; roughly 82% of the 4-hour urine had already been passed by then; most people drink again within 2 hours; and the 2-hour and 4-hour BHI gave similar rankings.
- **Repeatability:** coefficient of variation of about 18% (about 180 mL), measured in a separate group of 12 people who did the same drink twice.
- **Water-content correction:** the drinks ranged from 88% to 100% water, so the authors reported BHI both uncorrected (per litre of drink) and corrected (per litre of water ingested).
- **Funding:** European Hydration Institute. The lead author chaired its scientific advisory board.

### 1.2 Drinks tested and their measured composition (Maughan 2016, Table 2) [1]

| Drink | Water % | kcal/L | CHO g/100 mL | Fat g/100 mL | Protein g/100 mL | Osmolality mOsm/kg | Na mmol/L | K mmol/L | Caffeine mg/L |
|---|---|---|---|---|---|---|---|---|---|
| Still water | 100 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| Sparkling water | 100 | 0 | 0 | 0 | 0 | 7 | 1 | 0 | 0 |
| Cola | 89 | 420 | 10.6 | 0 | 0 | 432 | 2 | 0 | 96 |
| Diet cola | 100 | 4 | 0 | 0 | 0 | 23 | 2 | 0 | 127 |
| Sports drink | 96 | 160 | 3.9 | 0 | 0 | 297 | 21 | 4 | 0 |
| ORS | 97 | 80 | 1.8 | 0.1 | 0 | 229 | 55 | 20 | 0 |
| Orange juice | 89 | 470 | 10.5 | 0.1 | 0.5 | 570 | 1 | 33 | 0 |
| Lager | 94 | 330 | 2.2 | 0 | 0.4 | 774 | 1 | 6 | 0 |
| Coffee (black) | 99 | 4 | 0.1 | 0 | 0 | 34 | 1 | 7 | 212 |
| Hot tea (black) | 100 | 0 | 0 | 0 | 0 | 16 | 1 | 4 | 179 |
| Cold tea (black) | 100 | 0 | 0 | 0 | 0 | 18 | 1 | 5 | 179 |
| Whole milk (3.6% fat) | 88 | 640 | 4.7 | 3.6 | 3.2 | 286 | 18 | 41 | 0 |
| Skimmed milk (0.1% fat) | 91 | 350 | 5.0 | 0.1 | 3.4 | 282 | 19 | 40 | 0 |

The lager's ABV is not listed in Table 2. The test drink contained 96–212 mg caffeine per litre.

### 1.3 BHI results (2-hour values)

**Significantly above water** [1]:

| Drink | BHI, mean (SD) | Mean difference vs water (95% CI) | Corrected for water content: difference (95% CI) |
|---|---|---|---|
| Skimmed milk | 1.58 (0.60) | +0.58 (0.28 to 0.89) | +0.44 (0.16 to 0.72) |
| ORS | 1.54 (0.74) | +0.54 (0.16 to 0.93) | +0.50 (0.13 to 0.87) |
| Whole milk | 1.50 (0.58) | +0.50 (0.20 to 0.80) | +0.32 (0.06 to 0.58) |
| Orange juice | ≈1.39 | +0.39 (0.05 to 0.73) | +0.24 (−0.06 to 0.54), **not significant** |

- At 4 hours, cumulative urine was lower than with water by 294 g (154 to 434) for whole milk, 339 g (190 to 489) for skimmed milk and 362 g (222 to 505) for ORS. Orange juice was no longer significant at 4 hours (p = 0.06).
- **Not different from water:** sparkling water, cola, diet cola, sports drink, lager, coffee, hot tea and cold tea. The paper gives exact BHI means for these only in a figure, so this brief does not report numeric values for them. With a CV of about 18%, the study could not detect differences much smaller than about ±0.2.

### 1.4 Follow-up BHI studies (2018–2026)

| Study | Population | Key BHI results (mean ± SD unless stated) |
|---|---|---|
| Sollanek 2018 [4] | 40 adults (17 M, 23 F) | Sports drink 1.09 ± 0.26 (not different from water); glucose-ORS 1.21 ± 0.28*; amino-acid ORS 1.15 ± 0.28*. Neither body mass nor sex affected the BHI. |
| Maughan 2019 [3] | 3 × 12 men; graded single ingredients | **Sucrose:** 10% and 20% gave higher BHI than 0% and 5%. **Sodium:** 27 and 52 mmol/L higher than 7 and 15 mmol/L. **Caffeine 0–400 mg/L: no effect** on urine or fluid balance (p = 0.83). No difference in vasopressin or aldosterone. |
| Clarke 2019 [5] | 12 young vs 12 older adults | In young adults the BHI rose with drink sodium; AA-60 (60 mmol/L Na) 1.24 ± 0.10*. In older adults the best was AA-30, 1.20 ± 0.13*. A 4-h BHI may suit older adults better because they excrete urine more slowly. |
| Berry 2020 [6] | 12 young adults | Milk-permeate drink (electrolyte-rich) above water at every time point; a standard carbohydrate-electrolyte drink was not different from water. |
| Millard-Stafford 2021 [2] | 19 adults (15 M, 4 F) | Electrolytes only (21 mmol/L Na): 1.12 ± 0.24 to 1.15 ± 0.25, **not significant**. Sports drink (5.8% CHO + electrolytes): 1.15 ± 0.17*. Alanyl-glutamine + electrolytes: 1.14–1.15* (at 240 min only). Authors conclude electrolytes contribute most, and the minimum effective sodium is likely above 21 mmol/L. Funded by Coca-Cola. |
| Peden 2024 [10] | 10 men | Skimmed milk vs sweetened soya drink (1 L of water from each): total urine 986 vs 950 g, not different. Soya is a viable non-dairy option. |
| Millard-Stafford 2025 [7] | 28 adults (14 M, 14 F) | Protocol used 500 mL test drink + 500 mL water. Energy drink with 280 mg caffeine: **0.86 ± 0.16*** at 4 h. 280 mg + electrolytes: **0.91 ± 0.16***. 106 mg caffeine + carbohydrate + 45 mmol Na: **1.01 ± 0.12** (same as water). Habitual vs caffeine-naive users did not differ; women retained more fluid than men. |
| Bassett 2026 [8] | 24 adults | Sugar-free caffeinated electrolyte drink (210 mg caffeine/L, about 44 mmol Na): 0.90–0.97 at 2 h and 0.99–1.01 at 4 h (not different from water). Only the 1-h value was below water (0.75–0.83). **Repeated water trials had poor within-person reliability (ICC 0.11 at 2 h, 0.31 at 4 h).** |
| Yamaguchi 2026 [9] | Methods paper | "Augmented BHI": adds plasma-volume change, free-water clearance, and osmolar and sodium clearance, plus a 4-h protocol for older adults. |

\* = significantly different from water.

### 1.5 Limits of the BHI, and why the app should not use it as a multiplier

1. **Narrow setting.** Results come from a single 1 L bolus drunk quickly by a fasted, euhydrated person at rest, mostly young men [1][2]. Real drinking happens in smaller amounts, with food, spread over the day.
2. **It measures timing, not total water.** A high BHI can come from **slower delivery** of water to the blood (energy-dense drinks) rather than true extra retention. The method cannot separate the two [2][3].
3. **24-hour convergence.** In free-living 24-hour studies, mixed beverages (colas, coffee, juice) hydrated the same as water when total volume was matched [21][22]. Maughan 2016 also cites this as support.
4. **Noise.** The CV is about 18% [1]. Within-person reproducibility of water diuresis is poor [8]. Some drinks, notably sports drinks, are significant in some studies and not in others [1][2][4][6].
5. **Funding.** Industry and industry-linked funders back many BHI studies (European Hydration Institute [1], Coca-Cola [2]). This does not invalidate the data, but it argues for conservative use.
6. **Older adults** keep excreting urine longer, so a 2-hour index may misrank drinks for them [5].

---

## 2. Mechanisms: what makes a drink hydrate more or less than water

- **Kidney set-point.** In a hydrated person, a water bolus dilutes plasma, vasopressin (AVP) falls, and the kidneys excrete most of the load within 2–3 hours. Anything that slows water entry or holds water in the extracellular space reduces that urine spike [1][12].
- **Sodium** is the main ion holding water in the extracellular fluid. BHI rises in steps with drink sodium: 27–52 mmol/L beat 7–15 mmol/L [3]; 45–60 mmol/L drinks beat water [4][5]. The WHO ORS formula uses 75 mmol/L [2]. Sports drinks (about 20 mmol/L) are borderline [1][2][4]. Typical sodas, juices, coffee and tea contain almost no sodium (1–2 mmol/L) [1].
- **Potassium** matters in milk (about 40 mmol/L) and orange juice (about 33 mmol/L). These drinks produced positive potassium balance and high BHI [1]. Potassium's separate contribution is uncertain because it is handled through aldosterone and uptake into cells [2].
- **Carbohydrate and energy density.** More energy per mL means slower stomach emptying and slower water delivery [1][12]. Sucrose at 10–20% clearly raised BHI, while 5% did not [3]. Hypertonic glucose (10%, about 565 mOsm/kg) **briefly reduced plasma volume** in the first hour, because water moved into the gut before being absorbed [13]. This is a short-term effect and does not cost net water over 2–4 hours.
- **Protein and fat (why milk scores high).** Milk combines about 18 mmol/L Na, about 40 mmol/L K, protein, lactose and (in whole milk) fat. The result is slow stomach emptying plus electrolyte retention [1][11]. After exercise, milk drinkers stayed in positive fluid balance for 5 hours, while water and sports-drink drinkers did not [11]. Skimmed milk scored at least as high as whole milk [1], so fat is not essential. Soya drink performed like skimmed milk [10].
- **Osmolality.** Isotonic drinks (about 280–300 mOsm/kg: milk, sports drinks) empty and absorb efficiently. Strongly hypertonic drinks (orange juice 570, cola 432 mOsm/kg [1]) slow emptying and pull water into the gut briefly [12][13]. Lager's high osmolality (774 [1]) is mostly ethanol. Ethanol crosses cell membranes freely, so it does not hold water the way sodium does.
- **Diuretic substances.** Caffeine (adenosine antagonism; natriuresis) and alcohol (suppression of AVP release) increase urine output in a dose-dependent way [1][14][23]. Details are in §3 and §4.

---

## 3. Caffeine

### 3.1 Dose–response evidence

| Study | Dose and context | Result |
|---|---|---|
| Maughan & Griffin 2003 review [14] | Literature 1966–2002 | Acute doses of **at least 250–300 mg** briefly raise urine output, mainly in people deprived of caffeine for days or weeks. Regular users develop **profound tolerance**. Doses in normal servings of tea, coffee or soda show no diuretic action. |
| Maughan 2016 [1] | 96–212 mg/L in 1 L of coffee, tea or cola | No effect on fluid balance. |
| Maughan 2019 [3] | 0–400 mg in 1 L | No effect (p = 0.83). |
| Seal 2017 [17] | Habitual drinkers, coffee at 3 vs 6 mg/kg | 269 mg (3 mg/kg): no effect. **537 mg (6 mg/kg): 613 mL urine over 3 h vs 356 mL for water**, about +260 mL. |
| Riesenhuber 2006 [20] | 750 mL energy drink, 240 mg caffeine, after 12 h without fluid | +243 mL urine over 6 h, attributable to caffeine. Taurine had no effect. |
| Millard-Stafford 2025 [7] | 280 mg energy drinks | BHI 0.86–0.91 (about 9–14% lower than water); 106 mg drink not different. No difference by habitual intake. |
| Bassett 2026 [8] | 210 mg/L with electrolytes | Lower than water only at 1 h; same as water at 2–4 h. |
| Zhang 2015 meta-analysis [16] | 16 studies, 28 effect sizes, median dose 300 mg | Urine +109 ± 195 mL (+16%). Effect size 0.29 (95% CI 0.11–0.48). At rest the effect size was 0.54; **during exercise it disappeared** (0.10, CI −0.07 to 0.27). Women were more affected than men in the meta-analysis. |
| Killer 2014 [15] | 50 habitual male coffee drinkers, 4 × 200 mL coffee/day (4 mg/kg/day) for 3 days | No difference vs water in total body water (deuterium), 24-h urine (2409 vs 2428 mL) or any blood or urine marker. |
| Armstrong 2005 [18] | 0, 3 or 6 mg/kg/day for 11 days | No difference in 24-h urine volume or any hydration marker. |
| Ruxton & Hart 2011 [19] | 4–6 mugs of black tea (168–252 mg) | Same as water on all blood and urine measures. |
| Grandjean 2000 [21] | Caffeinated colas and coffee as part of daily fluid | No difference in hydration markers. |

### 3.2 Interpretation

- **Threshold.** Acute diuresis shows up reliably only above about **250–300 mg in one sitting** [14][17]. Results around 240–280 mg are mixed: positive in [7][20], null in [3][8].
- **Tolerance.** Daily use blunts the effect [14]. However, the 2025 trial found no difference between habitual and naive users at 280 mg [7], so tolerance is real but not complete.
- **Daily scale.** Several days of 3–6 mg/kg/day (about 200–450 mg/day for a 75 kg adult) do not change 24-hour urine or body water [15][18].

### 3.3 Verdict for the app

**Coffee, tea, and caffeinated soft drinks count toward intake at their full water content.** A small, capped deduction applies only to the part of caffeine above 250 mg within a 2-hour window. That covers very strong cold brews, large energy drinks, multiple espresso shots, and pre-workout drinks. This keeps the "myth-busting" message accurate while respecting the high-dose evidence. Calibration of the deduction is in §8.

---

## 4. Alcohol

### 4.1 Evidence on extra urine per gram of ethanol

| Source | Conditions | Extra urine | Approx. mL per g |
|---|---|---|---|
| Eggleton 1942 [27] (as summarized in [24]) | Classic estimate | About 100 mL per 10 g | **≈10 mL/g**. Based on one subject; drink strength not reported [24]. |
| Hobson & Maughan 2010 [23] | 12 men, 1 L of beer with 4% vs 0% alcohol (≈31.6 g ethanol, computed from 40 mL × 0.789 g/mL) | **Euhydrated:** 1279 ± 256 vs 1121 ± 148 mL over 4 h (+158 mL). **Hypohydrated:** 261 vs 174 mL, not significant (p = 0.057). | **≈5 mL/g** when hydrated; blunted when dehydrated |
| Polhuis 2017 [24] | 20 older men (≈69 y), 30 g alcohol as 5% beer (≈750 mL), 13.5% wine (≈280 mL) or 35% spirits (≈108 mL), each vs a non-alcoholic counterpart, with lunch | **Wine** +88 ± 158 mL at 2 h; **spirits** +74 to +81 mL at 1–2 h; **beer** +73 at 1 h, falling to −45 at 4 h (not significant). **No difference at 24 h for any drink.** The net effect did not grow with strength. | ≈2.5–3 mL/g at the peak; ≈0 over 24 h |
| Wijnen 2016 [26] | 11 men after exercise (1% body mass loss), drank 100% of sweat loss | Fluid retained: **5% beer 21%**, 2% beer 36%, alcohol-free beer 36%, water 34%, sports drink 42%. Net fluid balance not different by 5 h. | ≈3 mL/g (derived: ~13 percentage points of ~750 mL for ~30 g) |
| Shirreffs & Maughan 1997 [25] | Rehydration after exercise with 0, 1, 2 and 4% alcohol drinks | Up to 2% made no difference. 4% tended to delay recovery of blood and plasma volume. Total urine not significantly different. | Small |
| Maughan 2016 BHI [1] | 1 L lager | Not different from water. The authors suggest alcohol cancelled the retention benefit lager's energy content would otherwise give. | — |
| UKHSA rapid evidence summary, 2025 (search to July 2023) [28] | 14 studies | Evidence on increased urine is inconsistent. **No study tested a dose–response.** Most studies were small, mostly male, and low quality. | — |

### 4.2 How strength (ABV) matters

- Ethanol grams scale directly with ABV × volume. A glass of wine or a shot of spirits delivers about the same ethanol as a can of beer in far less water.
- **Net effect** = water supplied − extra urine. For beer, the drink's own water (about 92%) outweighs the diuresis. For wine, the balance is slightly positive. For spirits, it is negative in the first hours.
- In Polhuis, the extra urine **per gram** did not rise with concentration [24]. Strength matters because of how little water comes with each gram, not because stronger alcohol is "more diuretic" per gram.
- Diuresis is larger when hydrated and blunted when dehydrated [23]. The available data show no clear dose–response [28].

### 4.3 Recommendation

- Treat beer, wine and spirits as **partial** credit using `alcoholPenalty = 5 mL × g ethanol`. This sits at the upper end of modern controlled data (≈3–5 mL/g) and well below the single-subject 10 mL/g classic.
- **Floor each drink at 0.** Do not subtract from other drinks. Reasons: 24-hour data show no lasting net loss at moderate intake [24], and a negative number feels punitive and invites "compensating" behaviour.
- Results: beer about 70% of volume, wine about 30%, neat spirits 0, mixed drinks according to the mixer.

**Suggested copy (neutral, not preachy):**
- Beer: *"Counts as about 70% of its volume. Alcohol prompts your kidneys to release a little extra water for a few hours."*
- Spirits: *"Adds 0 mL to your total. The alcohol roughly offsets the small amount of water in a shot."*
- Do not use "should", "avoid" or moral framing. Optionally show "≈1 standard drink (14 g alcohol)" as plain information [37].

---

## 5. Sugar, hypertonic juices and energy drinks

- **High sugar does not reduce hydration** over 2–4 hours. 10–20% sucrose actually raised the BHI by slowing water delivery [3]. Orange juice (10.5% sugar, 570 mOsm/kg) scored about 1.39 uncorrected [1].
- **The one short-term catch:** very hypertonic drinks briefly pull water into the gut and reduce plasma volume during the first hour [13]. This matters for rapid rehydration during sport, not for daily totals.
- **No sugar penalty in the hydration model.** Sugar is a **health** dimension and is shown separately (§9).
- **Energy drinks:** hydration is driven by caffeine dose and electrolytes. At 280 mg the BHI is about 0.86–0.91; at about 106 mg with electrolytes it equals water [7]. A sugar-free drink with 210 mg/L caffeine plus about 44 mmol/L sodium matched water at 2–4 h [8]. Taurine has no diuretic effect [20]. The caffeine modifier handles energy drinks automatically. A standard 250 mL can (about 80 mg) gets no deduction.

---

## 6. Water content vs. hydration effect

There are two ways an app can count a non-water drink:

| Approach | What it counts | 250 mL whole milk | 355 mL 5% beer | Problem |
|---|---|---|---|---|
| **Raw volume** | Every mL as water | 250 mL | 355 mL | Ignores solids and alcohol. Overcounts beer and spirits. |
| **Water content** | Water actually in the drink (≈88% for milk [1][36]) | 220 mL | ≈327 mL | Ignores diuresis from alcohol and high-dose caffeine. |
| **BHI-adjusted** | Water retained at 2 h relative to plain water | ≈375 mL (×1.50) | ≈355 mL (BHI ≈1, n.s.) | Counts more water than was drunk. Short time window, noisy, and converges at 24 h (§1.5). |
| **Recommended** | Water content minus evidence-based diuresis | **220 mL** | **≈255 mL** | Conservative and explainable. Misses short-term "staying power", which a badge covers. |

**Water fractions used** (by weight; USDA SR Legacy via nutritionvalue.org mirror [36], cross-checked with Maughan Table 2 [1]):

| Drink | Water fraction |
|---|---|
| Still or sparkling water | 1.00 |
| Diet soda | ≈1.00 |
| Black coffee, tea | ≈0.99–1.00 |
| ORS | 0.97 |
| Sports drink | 0.94–0.96 |
| Beer (≈5%) | 0.92 |
| Skimmed milk | 0.91 |
| Regular cola | 0.89 (USDA 89.4) |
| Sugared energy drink | 0.89 |
| Whole milk | 0.88 (USDA 88.1) |
| Orange juice | 0.88 (USDA 88.3) |
| Red wine | 0.865 |
| 40% spirits | ≈0.67 (*calculated* from ABV and density, not measured) |

**Weight vs. volume nuance.** These fractions are g water per g of drink. Sugary drinks are denser than water (about 1.04 g/mL), so a 355 mL cola actually holds about 330 mL of water, not 316. Using the weight fraction directly on mL **underestimates by up to about 4%**. That is acceptable for v1 (conservative, simple). A v2 can store "mL water per 100 mL" per product.

---

## 7. Food moisture (why the goal is drinks-only)

- Food supplies about **20%** of total water intake in the US: 20.7% in the main US analysis and about 22% in a review estimate [35]. The share is higher in diets rich in fruit and vegetables; some European countries and South Korea are cited as higher [35]. Metabolic water from oxidizing food adds a little more and is roughly offset by water lost in breathing [35].
- Official adequate intakes cover **total** water from drinks plus food: EFSA 2.0 L/day for women and 2.5 L/day for men [33]; IOM 2.7 L and 3.7 L [34]. About 80% of total intake comes from beverages [34].
- **App implication:** a drinks-only goal should target about **80% of a total-water reference**, so food moisture is implicitly assumed rather than logged. This avoids food logging, which is burdensome and inaccurate.
- **Suggested explainer copy:** *"Food usually provides about a fifth of your water. Your goal covers drinks only and assumes typical meals."*
- Soups, broths and smoothies can be offered as optional drink categories with their own water fractions. This is a judgment call (§11).

---

## 8. Recommended model

### 8.1 Design decisions

1. **Credit = water content × hydrationFactor − diuretic penalties, floored at 0.**
2. **hydrationFactor = 1.0 for all categories in v1.** The slot stays in the data model so evidence-based factors can be added later without a migration. BHI values above 1 are **not** used to inflate credit (reasons in §1.5). High-BHI drinks get a "long-lasting" badge instead: milk (dairy and soya), ORS and electrolyte drinks with at least 45 mmol/L Na, and orange juice.
3. **Caffeine:** deduction of 0.5 mL per mg of caffeine above **250 mg in a rolling 2-hour window**, capped at 150 mL per window.
   - Calibration: 300 mg gives 25 mL; 400 mg gives 75 mL; 537 mg gives 144 mL.
   - This is deliberately conservative. It sits below the +260 mL observed at 537 mg [17] and below the 280 mg energy-drink result [7], and above the null findings at up to 400 mg/L [3] and 210 mg [8], reflecting 24-hour neutrality [15][18].
4. **Alcohol:** 5 mL per gram of ethanol (grams = mL × ABV × 0.789).
5. **Display both values.** The log row shows "Logged 355 mL · Counts 315 mL". The goal ring and streaks use **credit**. An info sheet explains the breakdown. Values are rounded to the nearest 5 mL to avoid false precision.
6. **Setting:** "Count drinks by: *Hydration value* (default) / *Full volume*", for users who prefer simplicity.
7. **Scope note in the app:** the model targets healthy adults and is not medical advice. People on fluid restriction or diuretics should follow their clinician.

### 8.2 Pseudocode

```swift
struct DrinkProfile {
    let id: String
    let category: Category            // water, coffee, tea, soda, dietSoda, milk, plantMilk, juice,
                                      // sportsDrink, ors, energyDrink, beer, wine, spirits, smoothie, broth
    let waterFraction: Double         // g water / g drink (USDA or label)
    let hydrationFactor: Double = 1.0 // reserved; 1.0 for all v1 categories
    let caffeineMgPer100mL: Double
    let abvPercent: Double            // % v/v
    let sugarGPer100mL: Double
    let sugarIsFree: Bool             // WHO: added sugar + juice sugar = free; milk lactose = not free
    let sodiumMgPer100mL: Double
    let longLastingBadge: Bool        // high-BHI: milk, soya, ORS (≥45 mmol/L Na), orange juice
}

enum Model {
    static let caffeineThresholdMg = 250.0  // per rolling 2-h window
    static let caffeineMLPerMg     = 0.5
    static let caffeineCapML       = 150.0  // per window
    static let alcoholMLPerGram    = 5.0
    static let ethanolDensity      = 0.789  // g/mL
}

struct Credit { let loggedML, waterML, caffeinePenaltyML, alcoholPenaltyML, creditML: Double }

func credit(volumeML v: Double, profile p: DrinkProfile,
            caffeineInPrior2hMg prior: Double,          // caffeine from drinks logged in the previous 2 h
            caffeinePenaltyInPrior2hML priorPen: Double) -> Credit {

    let water = v * p.waterFraction * p.hydrationFactor

    // Caffeine: penalize only the increment above the threshold within the window
    let thisMg     = v * p.caffeineMgPer100mL / 100
    let overBefore = max(0, prior - Model.caffeineThresholdMg)
    let overAfter  = max(0, prior + thisMg - Model.caffeineThresholdMg)
    var cafPen     = (overAfter - overBefore) * Model.caffeineMLPerMg
    cafPen         = min(cafPen, max(0, Model.caffeineCapML - priorPen))

    // Alcohol
    let ethanolG = v * (p.abvPercent / 100) * Model.ethanolDensity
    let alcPen   = ethanolG * Model.alcoholMLPerGram

    let raw = max(0, water - cafPen - alcPen)
    return Credit(loggedML: v, waterML: water, caffeinePenaltyML: cafPen,
                  alcoholPenaltyML: alcPen, creditML: (raw / 5).rounded() * 5)
}

// Daily goal progress
dailyCredit = sum(credit.creditML for drinks today)        // drives ring, reminders, streaks
dailyVolume = sum(volumeML for drinks today)               // shown as secondary stat
```

**Mixed drinks** (latte, rum and cola, shandy): compute each component with its own profile and sum, or store a composite profile.

### 8.3 Worked examples

Assumptions: water fractions from §6; caffeine and alcohol defaults stated per row; no other caffeine in the previous 2 hours. Final credit is rounded to the nearest 5 mL.

| # | Drink | Water | Caffeine / alcohol | Penalty | **Credit** | % of volume |
|---|---|---|---|---|---|---|
| 1 | **355 mL cola** | 355 × 0.89 = 316 | Caffeine 96 mg/L [1] → 34 mg | 0 | **315 mL** | 89% |
| 2 | **250 mL whole milk** | 250 × 0.88 = 220 | — | 0 | **220 mL** + long-lasting badge | 88% |
| 3 | **473 mL cold brew** | 473 × 0.99 = 468 | Caffeine default 240 mg* | 0 (below 250) | **470 mL** | 99% |
| 3b | Strong cold brew, 330 mg | 468 | 80 mg over threshold × 0.5 | 40 | **430 mL** | 91% |
| 4 | **355 mL beer, 5%** | 355 × 0.92 = 327 | Ethanol 355 × 0.05 × 0.789 = 14.0 g | 70 | **255 mL** | 72% |
| 5 | **150 mL red wine, 13.5%** | 150 × 0.865 = 130 | Ethanol 150 × 0.135 × 0.789 = 16.0 g | 80 | **50 mL** | 33% |
| 5b | 44 mL spirits, 40% | 44 × 0.67 = 29 | Ethanol 13.9 g | 69 | **0 mL** (floored from −40) | 0% |
| 6 | **500 mL sports drink** | 500 × 0.95 = 475 | Na ≈20 mmol/L → ≈10 mmol (≈230 mg) | 0 | **475 mL** | 95% |
| 7 | **250 mL orange juice** | 250 × 0.88 = 220 | — | 0 | **220 mL** + long-lasting badge | 88% |
| 8 | **250 mL energy drink** | 250 × 0.89 = 223 | Caffeine ≈80 mg (typical can; USDA lists 75 mg [36]) | 0 | **225 mL** | 89% |
| 8b | 473 mL energy drink, 300 mg | 473 × 0.89 = 421 | 50 mg over threshold × 0.5 | 25 | **395 mL** | 84% |

\* Cold brew caffeine varies widely. Scaling FDA's brewed-coffee range of 113–247 mg per 12 fl oz [29] to 16 fl oz gives about 150–330 mg; 240 mg is the midpoint. The app should let users pick "regular / strong" or enter a brand value.

---

## 9. Health information per drink (neutral wording)

Show these as plain facts on the drink detail sheet. Keep them separate from hydration credit.

**Sugar.** WHO strongly recommends free sugars below 10% of energy, and conditionally recommends below 5%, about 25 g/day [32]. Ten percent of a 2,000 kcal diet is about 50 g (calculation). Fruit-juice sugars **count as free sugars**; milk lactose does not [32].
- Example copy: *"Cola 355 mL: ≈37 g free sugar, about 1.5× WHO's 25 g reference / about 75% of 50 g."*
- Per serving: orange juice 250 mL ≈ 22 g [36]; energy drink 250 mL ≈ 26–27 g [36]; sports drink 500 mL ≈ 20–30 g (3.9–6% carbohydrate) [1][2].

**Caffeine** (show mg and the share of each reference):
- Healthy adults: up to **400 mg/day** is not generally linked to negative effects [29][30]. EFSA finds single doses up to **200 mg** raise no safety concerns, and notes about 100 mg near bedtime can affect sleep in some people [30].
- **Pregnancy / breastfeeding:** EFSA, up to 200 mg/day from all sources [30]. ACOG found moderate intake below 200 mg/day does not appear to be a major factor in miscarriage or preterm birth [31]. FDA advises discussing caffeine with a provider [29].
- **Children and adolescents:** EFSA proposes 3 mg/kg body weight per day [30]. AAP advises against energy drinks for children and teens (as cited by FDA [29]).
- Example copy: *"Cold brew 473 mL: ≈240 mg caffeine, 60% of the 400 mg daily reference for adults."* Pregnancy and teen references appear only if the user opts in in their profile.

**Alcohol.** Show grams of ethanol and US standard drinks (14 g) [37]. No judgmental language.

**Sodium.** Optionally show mg per serving. It is relevant for electrolyte drinks and ORS.

---

## 10. Key values

| Drink / factor | Value | CI / range | Source | Confidence |
|---|---|---|---|---|
| BHI, skimmed milk (2 h) | 1.58 (SD 0.60) | Δ vs water +0.58 (0.28–0.89) | [1] | Moderate–high |
| BHI, whole milk (2 h) | 1.50 (SD 0.58) | +0.50 (0.20–0.80); corrected +0.32 (0.06–0.58) | [1] | Moderate–high |
| BHI, ORS (2 h) | 1.54 (SD 0.74) | +0.54 (0.16–0.93) | [1] | Moderate–high |
| BHI, orange juice (2 h) | ≈1.39 | +0.39 (0.05–0.73); corrected n.s. | [1] | Moderate |
| BHI, cola, diet cola, coffee, tea, lager, sparkling water | Not different from 1.0 | Detection limit about ±0.2 (CV 18%) | [1] | Moderate |
| BHI, sports drink | 1.09–1.15 | Significant in [2], not in [1][4][6] | [1][2][4][6] | Low–moderate |
| BHI, 45–60 mmol/L Na drinks | 1.20–1.24 | SD 0.10–0.28 | [4][5] | Moderate |
| BHI, 280 mg caffeine energy drink | 0.86–0.91 (4 h) | Δ −9% to −14% (CIs exclude 0) | [7] | Moderate (single study) |
| BHI, 210 mg/L caffeine + electrolytes | 0.90–1.01 (2–4 h) | n.s. vs water | [8] | Moderate |
| Caffeine with no measurable acute diuresis | Up to ≈250 mg acute | Null up to 400 mg/L in [3]; positive at 240–280 mg in [7][20] | [3][14][17] | Moderate |
| Caffeine meta-analytic effect | +109 mL (+16%) | ES 0.29 (0.11–0.48); null during exercise | [16] | Moderate |
| Caffeine, daily scale | No 24-h effect at 3–6 mg/kg/day | — | [15][18] | High |
| Alcohol diuresis, classic | ≈10 mL/g | Single subject | [27] via [24] | Low |
| Alcohol diuresis, modern | ≈3–5 mL/g (first 2–4 h) | ≈0 at 24 h (one study) | [23][24][26] | Moderate |
| Alcohol diuresis when dehydrated | Blunted | p = 0.057 | [23] | Low–moderate |
| App caffeine penalty (design) | 0.5 mL/mg above 250 mg per 2 h, cap 150 mL | Judgment, calibrated to above | §8 | Design choice |
| App alcohol penalty (design) | 5 mL/g ethanol | Plausible 3–10 | §8 | Design choice |
| Water fraction: whole milk / OJ / cola / beer / red wine | 0.88 / 0.88 / 0.89 / 0.92 / 0.865 | ±0.01–0.02 by product | [1][36] | High |
| Water from food | ≈20% of total intake (US) | 20.7–22%; higher in fruit- and vegetable-rich diets | [34][35] | Moderate |
| WHO free sugars | <10% energy (strong); <5% ≈ 25 g (conditional) | — | [32] | High (guideline) |
| Caffeine, adults | ≤400 mg/day; single dose ≤200 mg no concern | — | [29][30] | High (guideline) |
| Caffeine, pregnancy | ≤200 mg/day | — | [30][31] | High (guideline) |
| Caffeine, children/teens | 3 mg/kg/day (EFSA) | — | [30] | High (guideline) |

---

## 11. Open questions / judgment calls

1. **Credit above water content for milk, ORS and juice?** This brief recommends **no**, using a badge instead. A "BHI mode" that multiplies by about 1.3–1.5 is defensible for short windows (heat, long meetings, travel) but would let a glass of milk out-score its own water. Revisit if 24-hour data emerge.
2. **Floor at 0 vs allowing negatives for spirits.** Recommended floor at 0 (24-hour neutrality [24]; avoids punitive feel). A purist model would show about −40 mL for a neat shot.
3. **Alcohol coefficient:** 5 mL/g chosen. 3 mL/g fits the older-adult and post-exercise data [24][26]; 10 mL/g is the classic but weak [27]. The UKHSA review found no dose–response data [28].
4. **Caffeine threshold, tolerance and sex.** Should a "rarely drink caffeine" profile lower the threshold, for example to 200 mg? The meta-analysis found women more affected [16], but the 2025 trial found women retained more [7]. Evidence conflicts, so v1 stays sex-neutral.
5. **Rolling 2-hour caffeine window** vs per-drink calculation. The window is more physiological but harder to explain. Per-drink is simpler but misses three espressos drunk back-to-back.
6. **Sports drinks and electrolyte mixes.** Badge only at 45 mmol/L Na or more (strong evidence [3][4][5]). Sports drinks at about 20 mmol/L stay at factor 1.0 because results are inconsistent [1][2][4].
7. **Weight vs volume water fraction** (up to about 4% conservative bias for sugary drinks). Fix in v2 with per-100 mL data.
8. **Older adults:** retention lasts longer and a 4-hour BHI is more relevant [5]. This does not change the v1 credit.
9. **Composite and homemade drinks** (lattes, smoothies, protein shakes, broths): need composite profiles. Smoothie and shake water fractions vary widely; use product data.
10. **Funding and reliability caveats** for the BHI literature [1][2][8]. Keep claims modest in UI copy, for example "may help you stay hydrated longer", not "hydrates 50% better".
11. **Decaf, herbal tea, kombucha, and low-alcohol or alcohol-free beer** reduce to existing rules (water fraction, caffeine, ABV). Alcohol-free beer retained like water after exercise [26].

---

## References

1. Maughan RJ, Watson P, Cordery PAA, et al. A randomized trial to assess the potential of different beverages to affect hydration status: development of a beverage hydration index. *Am J Clin Nutr*. 2016;103(3):717–723. https://doi.org/10.3945/ajcn.115.114769 (accepted manuscript: https://researchonline.ljmu.ac.uk/id/eprint/12468/)
2. Millard-Stafford M, Snow TK, Jones ML, Suh H. The Beverage Hydration Index: influence of electrolytes, carbohydrate and protein. *Nutrients*. 2021;13(9):2933. https://pmc.ncbi.nlm.nih.gov/articles/PMC8465972/
3. Maughan RJ, Watson P, Cordery PAA, et al. Sucrose and sodium but not caffeine content influence the retention of beverages in humans under euhydrated conditions. *Int J Sport Nutr Exerc Metab*. 2019;29(1):51–60. https://pubmed.ncbi.nlm.nih.gov/29893590/
4. Sollanek KJ, Tsurumoto M, Vidyasagar S, Kenefick RW, Cheuvront SN. Neither body mass nor sex influences beverage hydration index outcomes during randomized trial when comparing 3 commercial beverages. *Am J Clin Nutr*. 2018;107(4):544–549. https://pubmed.ncbi.nlm.nih.gov/29635499/
5. Clarke MM, Stanhewicz AE, Wolf ST, Cheuvront SN, Kenefick RW, Kenney WL. A randomized trial to assess beverage hydration index in healthy older adults. *Am J Clin Nutr*. 2019;109(6):1640–1647. https://pmc.ncbi.nlm.nih.gov/articles/PMC6537935/
6. Berry CW, Wolf ST, Murray B, Kenney WL. Hydration efficacy of a milk permeate-based oral hydration solution. *Nutrients*. 2020;12(5):1502. https://pmc.ncbi.nlm.nih.gov/articles/PMC7284605/
7. Millard-Stafford M, Hack B, Harp A, Smith E. Caffeinated energy drink formulations differentially impact hydration versus water: does habitual caffeine intake or biological sex matter? *Nutrients*. 2025;17(18):2913. https://pmc.ncbi.nlm.nih.gov/articles/PMC12472760/
8. Bassett SD, Hack B, Harp A, Millard-Stafford M. Reproducibility of water diuresis: implications for establishing the beverage hydration index of a sugar-free caffeinated electrolyte beverage. *Nutrients*. 2026;18(19):3279. https://doi.org/10.3390/nu18193279 (PubMed 42884730)
9. Yamaguchi A, Martin IA, Fisher K, Kenney WL. Augmented Beverage Hydration Index methodology for comparing beverage efficacy. *J Appl Physiol*. 2026. https://doi.org/10.1152/japplphysiol.90175.2026
10. Peden DL, Derbyshire S, Funnell MP, et al. Fluid and electrolyte balance following consumption of skimmed milk and a plant-based soya beverage at rest in euhydrated males. *Eur J Appl Physiol*. 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC11467101/
11. Shirreffs SM, Watson P, Maughan RJ. Milk as an effective post-exercise rehydration drink. *Br J Nutr*. 2007;98(1):173–180. https://pubmed.ncbi.nlm.nih.gov/17459189/
12. Leiper JB. Fate of ingested fluids: factors affecting gastric emptying and intestinal absorption of beverages in humans. *Nutr Rev*. 2015;73(Suppl 2):57–72. https://pubmed.ncbi.nlm.nih.gov/26290292/
13. Evans GH, Shirreffs SM, Maughan RJ. Acute effects of ingesting glucose solutions on blood and plasma volume. *Br J Nutr*. 2009;101(10):1503–1508. https://pubmed.ncbi.nlm.nih.gov/18840313/
14. Maughan RJ, Griffin J. Caffeine ingestion and fluid balance: a review. *J Hum Nutr Diet*. 2003;16(6):411–420. https://pubmed.ncbi.nlm.nih.gov/19774754/
15. Killer SC, Blannin AK, Jeukendrup AE. No evidence of dehydration with moderate daily coffee intake: a counterbalanced cross-over study in a free-living population. *PLoS One*. 2014;9(1):e84154. https://pmc.ncbi.nlm.nih.gov/articles/PMC3886980/
16. Zhang Y, Coca A, Casa DJ, Antonio J, Green JM, Bishop PA. Caffeine and diuresis during rest and exercise: a meta-analysis. *J Sci Med Sport*. 2015;18(5):569–574. https://pmc.ncbi.nlm.nih.gov/articles/PMC4725310/
17. Seal AD, Bardis CN, Gavrieli A, et al. Coffee with high but not low caffeine content augments fluid and electrolyte excretion at rest. *Front Nutr*. 2017;4:40. https://pmc.ncbi.nlm.nih.gov/articles/PMC5563313/
18. Armstrong LE, Pumerantz AC, Roti MW, et al. Fluid, electrolyte, and renal indices of hydration during 11 days of controlled caffeine consumption. *Int J Sport Nutr Exerc Metab*. 2005;15(3):252–265. https://pubmed.ncbi.nlm.nih.gov/16131696/
19. Ruxton CH, Hart VA. Black tea is not significantly different from water in the maintenance of normal hydration in human subjects: results from a randomised controlled trial. *Br J Nutr*. 2011;106(4):588–595. https://pubmed.ncbi.nlm.nih.gov/21450118/
20. Riesenhuber A, Boehm M, Posch M, Aufricht C. Diuretic potential of energy drinks. *Amino Acids*. 2006;31(1):81–83. https://pubmed.ncbi.nlm.nih.gov/16847703/
21. Grandjean AC, Reimers KJ, Bannick KE, Haven MC. The effect of caffeinated, non-caffeinated, caloric and non-caloric beverages on hydration. *J Am Coll Nutr*. 2000;19(5):591–600. https://pubmed.ncbi.nlm.nih.gov/11022872/
22. Tucker MA, Ganio MS, Adams JD, et al. Hydration status over 24-h is not affected by ingested beverage composition. *J Am Coll Nutr*. 2015;34(4):318–327. https://pubmed.ncbi.nlm.nih.gov/25789444/
23. Hobson RM, Maughan RJ. Hydration status and the diuretic action of a small dose of alcohol. *Alcohol Alcohol*. 2010;45(4):366–373. https://pubmed.ncbi.nlm.nih.gov/20497950/
24. Polhuis KCMM, Wijnen AHC, Sierksma A, Calame W, Tieland M. The diuretic action of weak and strong alcoholic beverages in elderly men: a randomized diet-controlled crossover trial. *Nutrients*. 2017;9(7):660. https://pmc.ncbi.nlm.nih.gov/articles/PMC5537780/
25. Shirreffs SM, Maughan RJ. Restoration of fluid balance after exercise-induced dehydration: effects of alcohol consumption. *J Appl Physiol*. 1997;83(4):1152–1158. https://pubmed.ncbi.nlm.nih.gov/9338423/
26. Wijnen AH, Steennis J, Catoire M, Wardenaar FC, Mensink M. Post-exercise rehydration: effect of consumption of beer with varying alcohol content on fluid balance after mild dehydration. *Front Nutr*. 2016;3:45. https://pmc.ncbi.nlm.nih.gov/articles/PMC5066341/
27. Eggleton MG. The diuretic action of alcohol in man. *J Physiol*. 1942;101(2):172–191. https://doi.org/10.1113/jphysiol.1942.sp003973
28. Brini S, Carter N, Hill J, Kumah E, Qureshi M, Carville S. Minimum amount of alcohol to cause dehydration: a rapid evidence summary. UK Health Security Agency; published December 2025. https://assets.publishing.service.gov.uk/media/6932d5954bedc0e76230414a/Minimum-amount-of-alcohol-to-cause-dehydration-rapid-evidence-summary.pdf
29. US Food and Drug Administration. Spilling the beans: how much caffeine is too much? https://www.fda.gov/consumers/consumer-updates/spilling-beans-how-much-caffeine-too-much
30. European Food Safety Authority. Caffeine (topic page) and Scientific Opinion on the safety of caffeine. *EFSA J*. 2015;13(5):4102. https://www.efsa.europa.eu/en/topics/topic/caffeine ; https://doi.org/10.2903/j.efsa.2015.4102
31. American College of Obstetricians and Gynecologists. Committee Opinion No. 462: Moderate caffeine consumption during pregnancy. *Obstet Gynecol*. 2010;116(2 Pt 1):467–468. https://pubmed.ncbi.nlm.nih.gov/20664420/
32. World Health Organization. Guideline: sugars intake for adults and children (2015); and WHO news release, 4 March 2015. https://www.who.int/publications/i/item/9789241549028 ; https://www.who.int/news/item/04-03-2015-who-calls-on-countries-to-reduce-sugars-intake-among-adults-and-children
33. EFSA Panel on Dietetic Products, Nutrition and Allergies. Scientific Opinion on Dietary Reference Values for water. *EFSA J*. 2010;8(3):1459. https://doi.org/10.2903/j.efsa.2010.1459
34. National Academies (Institute of Medicine). Report sets dietary intake levels for water, salt, and potassium (news release for *Dietary Reference Intakes for Water, Potassium, Sodium, Chloride, and Sulfate*, 2004/2005). https://www.nationalacademies.org/news/report-sets-dietary-intake-levels-for-water-salt-and-potassium-to-maintain-health-and-reduce-chronic-disease-risk
35. Popkin BM, D'Anci KE, Rosenberg IH. Water, hydration, and health. *Nutr Rev*. 2010;68(8):439–458. https://pmc.ncbi.nlm.nih.gov/articles/PMC2908954/
36. USDA FoodData Central, SR Legacy entries (whole milk 3.25%, regular cola, orange juice raw, regular beer, red table wine, Red Bull energy drink), accessed via the nutritionvalue.org mirror. https://fdc.nal.usda.gov/
37. National Institute on Alcohol Abuse and Alcoholism. What is a standard drink? https://www.niaaa.nih.gov/alcohols-effects-health/what-standard-drink
