# Containers, Fountains and Equivalencies: Logging Presets and the Lifetime-Intake Card

*Research note 04 for Hydrate. Compiled 2026-11-13. Labels used below: **[measured]** means a published measurement, **[spec]** means a manufacturer or regulatory specification, **[secondary]** means a third-party or retailer source with no primary source found, **[derived]** means our own arithmetic or estimate from cited inputs, and **[background]** means general knowledge we could not confirm with a source during this research.*

---

## TL;DR

- **Presets:** Ship six quick-add buttons: **Sip 20 mL, Glass 250 mL, Mug 350 mL, Bottle 500 mL, Large bottle 750 mL, My bottle (custom)**. Add a "pick your bottle" catalog. Brand bottles are sold in nominal fluid ounces, so the app should store the exact mL conversion (1 US fl oz = 29.5735 mL [26]). Examples: Stanley 30/40 oz = 887/1,183 mL, Hydro Flask 21/32/40 oz = 621/946/1,183 mL, Nalgene 32 oz = 946 mL (not 1 L), Owala 24/32/40 oz = 710/946/1,183 mL.
- **Sip size:** Habitual cup sips average about **20 mL for women and 25 mL for men** [1][3]. When people drink naturally rather than under instruction, sips are smaller: about **16 to 17 mL** [2][4]. Sips get smaller as a drinking bout goes on and are smaller through a straw [1]. A single default of **20 mL** is defensible.
- **Fountain intake rate:** We found **no empirical study of how much water people take in per second at a bubbler.** We derived a default of **8 mL/s (plausible range 4 to 12 mL/s)**. It is capped above by maximum-effort cup drinking, about 10 to 14 mL/s in healthy adults [5][6], and by bubbler output of about 20 to 47 mL/s, only part of which reaches the mouth [11][12][13]. Our recommendation: a **"seconds drinking" picker × 8 mL/s**, with **gulp count × 15 mL** as an alternative and an optional one-time calibration.
- **Bottle fillers** deliver **1.1 GPM, about 69 mL/s, on refrigerated units and 1.5 GPM, about 95 mL/s, on non-refrigerated units** (Elkay EZH2O, Oasis VersaFiller) [14][15]. Log these by bottle and fill level, not by time.
- **Equivalency card:** Below is a ladder of 46 comparisons, from a sip (0.02 L) to Lake Bellagio (83 million L). Flow-rate items (Niagara at 2,832 L per millisecond, the Mississippi, the Amazon) scale to any total, so they work as a fallback for every user.
- **Selection logic:** Score each item by how readable its ratio is. Multiples score best between **1.5× and 50×**, with a peak around 3 to 10×. Progress framings score best when the user is 10 to 95% of the way to an item. Choose one practical item, one fun item and one next-milestone item. Rotate daily with a date-seeded random choice, and celebrate when the user passes an item for the first time.
- **Realistic range:** A user drinking 2.6 L/day logs about **950 L a year** [derived from 31]. The ladder is therefore densest between 0.02 L and 10,000 L. Items above that mostly appear as "% of the way" or as durations.

---

## Part 1: Logging presets and the fountain estimate

### 1.1 Standard container sizes

#### Unit basics
- 1 US fluid ounce = 29.5735 mL exactly, and 1 US gallon = 231 in³ = 3.785411784 L exactly [26].
- The **US customary cup** is 8 fl oz, or **236.6 mL** [26] [derived]. **US nutrition labels use 240 mL for a cup** (21 CFR 101.9) [25]. The app should store 237 mL and display "1 cup".
- Imperial (UK) fluid ounces and pints differ from US ones [background]. If the UK is supported, label presets in mL rather than oz.

#### Everyday vessels (no single standard exists)
| Vessel | Typical size | mL | Basis |
|---|---|---|---|
| US cup (measure) | 8 fl oz | 237 | [26] |
| Coffee mug | 8 to 12 oz is commonly called standard; 10 to 12 oz is the most common answer. Mugs sold as 12 oz usually hold 9 to 10 oz in practice | 240 to 355 (default **350**) | [27] [secondary] |
| Restaurant water glass | 12 oz is the most common answer; water glasses range from 5.5 to 13.5 oz | 355 | [28] [secondary] |
| Pint glass | 16 oz (US) | 473 | [28] |
| Metric drinking glass | 250 mL is the conventional European glass | 250 | [background] (we used it as the round metric preset) |

#### Single-use bottles and cans (label volumes)
| Container | Market | mL |
|---|---|---|
| Can, 12 fl oz | US | 355 |
| Can, 330 mL | EU/UK | 330 |
| Water bottle, 16.9 fl oz | US/global | 500 |
| Soda/water bottle, 20 fl oz | US | 591 |
| Wine/"sport cap" bottle, 750 mL | global; 750 mL is a TTB-authorized standard of fill for wine [30] | 750 |
| 1 L, 1.5 L, 2 L bottles | global | 1,000 / 1,500 / 2,000 |

The volumes are printed on the labels. The mL equivalents of US ounce sizes are [derived] from [26].

#### Popular reusable bottles (nominal capacity)
| Bottle | Nominal | mL | Source note |
|---|---|---|---|
| Stanley Quencher H2.0 | 14 / 20 / **30** / **40** / 64 oz | 414 / 591 / **887** / **1,183** / 1,893 | Stanley's size guide [17]. Retailers list the 30 oz as 887 mL [18]. Some round the 40 oz to "1.20 L" [18]; the exact conversion is 1,183 mL [derived] |
| Hydro Flask Standard Mouth | **21** oz | **621** | retailer [20] |
| Hydro Flask Wide Mouth | **32** / **40** oz | **946** / **1,182** | Hydro Flask's listing (32 oz = 946 mL) [20]; third-party chart (40 oz = 1,182 mL) [21] |
| Nalgene Wide Mouth | **32** oz | **946** | Retailers advertise it as "1 L", but 32 oz is 946 mL [22] [derived] |
| Owala FreeSip | **24** / **32** / **40** oz | **710** / **946** / **1,183** | Owala's own size guide [19]; mL [derived] |

*Caveat:* "Nominal" usually means filled to the brim. With the lid on, with ice, or with a straw lid, the usable volume is lower. The app should let users edit the mL value of any saved bottle.

#### Fast-food and coffee-shop cups
| Chain / size | oz | mL | Notes |
|---|---|---|---|
| Starbucks Short / Tall / Grande | 8 / 12 / 16 | 237 / 355 / 473 | [23] [secondary]. Starbucks publishes no official spec page that we could find |
| Starbucks Venti **hot** | 20 | 591 | [23] |
| Starbucks Venti **iced** | 24 | 710 | The extra 4 oz allows for ice [23] |
| Starbucks Trenta (iced only) | about 30 to 31 | about 887 to 917 | Sources disagree [23] |
| McDonald's Small / Medium / Large (US) | 16 / 21 / 30 (some sources say 32) | 473 / 621 / 887 (946) | [24] [secondary]. Sizes vary by country |

Cold cups contain ice, so liquid volume is less than cup volume. We found no reliable figure for how much ice displaces (see Open questions). For iced drinks, the app could log about 70% of cup size, but that factor is our own assumption and is unverified.

#### Recommended default preset list
**Quick-add row (6 buttons, locale-aware labels):**
1. **Sip, 20 mL.** This is the mid-point of habitual sip data (§1.2).
2. **Glass, 250 mL** (metric locales) or **Cup, 8 oz / 237 mL** (US).
3. **Mug, 350 mL / 12 oz.**
4. **Bottle, 500 mL / 16.9 oz.**
5. **Large bottle, 750 mL** (EU) or **20 oz / 591 mL** (US).
6. **My bottle**, set during onboarding from a catalog of Stanley 30/40, Hydro Flask 21/32/40, Nalgene 32, Owala 24/32/40 and Custom.

**Secondary sheet:** can 330/355, 1 L, 1.5 L, the Starbucks sizes, fountain, and bottle filler. Partial fills (¼, ½, ¾ of any container) cover most edge cases without adding more presets.

---

### 1.2 Sip and gulp volumes: what the literature says

| Study | Population / method | Result |
|---|---|---|
| **Lawless et al. 2003**, *Dysphagia* [1] | Adults and elderly drinking from cups and straws; vessel size and sequential sips varied | Recommended guideline for cup sips: **about 25 mL for males and 20 mL for females**. Going from a 150 mL to a 600 mL vessel made sips **about 15% larger**. Cup sips were larger than straw sips in adults (not in the elderly group). Sip volume **fell across sips 1 to 5**. Height predicted individual differences, and the sex gap mostly disappeared when taller women were compared with shorter men. |
| **Adnerhill, Ekberg & Groher 1989**, *Dysphagia* 4:1–3 (as summarized in [2]) | Healthy adults; water, cola, barium | Thin-liquid sips averaged **25 mL in men and 20 mL in women**. Barium sips were smaller. |
| **Halpern** (as summarized in [2]) | Healthy adults | Men about **21.3 mL**, women about **13.6 mL**. The sex difference was not tested statistically. |
| **Bennett et al. 2009**, *Dysphagia* [2] | Natural (unobserved) vs. instructed drinking | Natural drinking averaged about **16 mL** per sip. Instructed tasks averaged about **6.6 to 6.8 mL**. The natural-vs-instructed gap was much larger than any sex or age effect. |
| **Self-selected volume study, n = 95**, *Dysphagia* 2022;37(5):1172–82 [4] | Healthy adults, thin liquid, "comfortable" volume | **16.66 ± 7.70 mL**. Larger volumes were associated with older age, male sex and a larger pharyngeal hold area. |
| **Timed water swallow test (TWST)**, Hughes & Wiles 1996 and later work [5][6][7] | Drink 100 to 150 mL from a cup as fast as is comfortable | A 2024 study measured healthy swallowing capacity at about **13.7 mL/s** [6]. Below **10 mL/s** is a commonly used threshold for dysfunction [6]. In one bedside version, finishing 100 mL in fewer than 5 swallows (**more than 20 mL per swallow**) counts as normal [7]. Capacity is lower in women and declines with age [5]. |
| **Cup vs. straw, older adults** [8] | Sequential drinking of 100 mL | The cup gave higher intake in less time, with more spillage, than the straw. |

**Takeaways for Hydrate**
- A **"gulp" in the 20 to 30 mL range** is a maximum-effort or "comfortable large swallow" figure. Everyday habitual sips are **about 15 to 25 mL**.
- **Default sip/gulp: 20 mL** for cups and bottles. Optionally use 25 mL for users who choose a larger body size or male sex in a profile; we do not recommend asking for sex just for this purpose.
- For **straw cups** such as Stanley straw lids or Owala FreeSip, sips are smaller than from a cup [1]. We found no clean mL figure for straws, so keep 20 mL and let calibration adjust it.

---

### 1.3 Drinking fountains: flows, standards, and actual intake

#### Standards
- **2010 ADA Standards §602.6:** the spout must produce a water stream at least **4 in (100 mm) high**, with the outlet no more than 5 in from the front of the unit [9][10]. The 4 in requirement exists so that a cup can be held under the stream [9]. §602 also sets spout heights: no more than 36 in for wheelchair-accessible units, and 38 to 43 in for standing units [9][10]. **The ADA sets no flow rate.**
- **ASME / CSA:** The bubbler listings we found say they are certified to **ASME A112.18.1/CSA B125.1** (plumbing supply fittings) [11][12]. We could not access the standard's text to confirm whether it sets a bubbler flow requirement. The brief mentioned **ASME A112.19.1**; that standard covers enameled cast-iron and steel fixtures, not bubbler flow [background].
- **ASHRAE 18** rates how much water a refrigerated cooler can chill, in gallons per hour (for example, 8 to 10 gph of 50 °F water). That is a chilling capacity, not a dispense rate [16].

#### Manufacturer flow rates
| Device | Rated flow | mL/s [derived, 1 GPM = 63.09 mL/s] |
|---|---|---|
| Elkay deck-mount classroom bubbler | 0.5 GPM [11] | 31.5 |
| Chicago Faucets 748-series bubbler | 0.74 GPM (with a flow control) [12] | 46.7 |
| T&S B-2360 bubbler | 0.32 GPM at a 4 in stream, 0.43 GPM at 8 in, at 60 psi [13] | 20.2 / 27.1 |
| Elkay EZS8WSSK fountain head (listing value; unclear) | 0.13 GPM [14] | 8.2 |
| **Elkay EZH2O bottle filler, refrigerated** | **1.1 GPM** (one model lists 1.0) [14] | **69.4** |
| **Elkay EZH2O bottle filler, non-refrigerated** | **1.5 GPM** [14] | **94.6** |
| **Oasis VersaFiller** | **1.1 GPM** advertised; one manual gives a 1.2 GPM factory default and a 20 s maximum dispense time [15] | 69.4 (75.7) |

#### How much does a person actually drink per second at a bubbler?
**We found no empirical measurement** in the swallowing literature, the plumbing literature, or a targeted extended search. The estimate below is **[derived]**:

1. **Ceiling set by swallowing.** Healthy adults drinking from a cup *as fast as is comfortable* reach about 10 to 14 mL/s [5][6]. Fountain drinking is less efficient than cup drinking: the mouth has to collect water from an arc, and people breathe between swallows. Fountain intake should therefore fall **below** this ceiling.
2. **Ceiling set by supply.** Bubblers put out about 20 to 47 mL/s [11][12][13]. Much of the arc misses the mouth and drains away, so supply is not the limiting factor.
3. **Bottom-up estimate.** Assume a self-selected bolus of about 10 to 20 mL. This is slightly below the cup values of 16 to 17 mL [2][4], since collecting from an arc is harder. Assume one swallow every 1.5 to 2.5 s, including the time to refill the mouth (an assumption). That gives **4 to 13 mL/s, with a central value of about 8 mL/s.**

**Default: 8 mL/s. Uncertainty: about ±50% (4 to 12 mL/s).** This is the least certain constant in this note, which is why calibration matters.

---

### 1.4 Recommendation: fountain and bottle-filler logging

#### Fountain (bubbler): primary method is seconds × rate
- **UI:** Three chips plus a fine-tune picker:
  - "Quick sip, about 3 s" → **24 mL**
  - "Good drink, about 6 s" → **48 mL**
  - "Long drink, about 10 s" → **80 mL**
  - The picker covers 1 to 30 s.
- **Formula:** `volume_mL = seconds × rate_mLps`, with `rate_mLps` = 8 by default, or the user's calibrated value.
- **Alternative method (toggle): gulps × gulp volume.** Default **15 mL per fountain gulp** (range 10 to 20) [derived from 2, 4]. Some people count gulps more reliably than seconds. Offer both and remember which one the user prefers.
- **Rounding:** Round fountain logs to the nearest 5 mL so the number does not look more precise than it is.

#### Optional one-time calibration ("Find your gulp", about 30 seconds)
1. "Pour **250 mL** (1 cup) into a glass. Drink it the way you normally would, without rushing."
2. The app shows a **stopwatch** (tap to start and stop) and a **gulp counter**. The user taps once per gulp, or enters the count afterward.
3. Compute `personal_gulp = 250 / gulps` and `personal_rate = 250 / seconds`.
4. **Fountain values:** `fountain_gulp = 0.75 × personal_gulp` and `fountain_rate = 0.75 × personal_rate`. The 0.75 factor is an **[assumption]** that fountain drinking is about 25% less efficient than cup drinking; no data supports or refutes it.
5. Clamp results to sensible bounds: gulp 8 to 40 mL, rate 3 to 15 mL/s. Store the values and let the user redo calibration at any time.
- *Advanced alternative:* Users with a measuring cup can drink from a fountain for 5 timed seconds after weighing a glass of water before and after. This is too fiddly for most users; offer it as an option only.

#### UX copy (one sentence)
> **"We estimate about 8 mL for every second you drink, roughly one swallow every two seconds. Calibrate once with a 250 mL glass for a number that fits you."**

#### Bottle-filler station
- The fill volume is easy to know, so **log it by container, not by time:** "Filled: [My bottle 946 mL ▾] × [Full / ¾ / ½ / ¼]".
- The app should log the water **when the user drinks it**, not when they fill the bottle. Otherwise a refill counts as intake. Two options: (a) refilling resets a "bottle level" that the user drains, or (b) log the fill and accept the overcount. (a) is better if bottle tracking exists; (b) is the simple MVP.
- **Timer fallback** for unknown bottles: `volume = seconds × 69 mL/s` (1.1 GPM refrigerated) [14][15], or 95 mL/s if the user picks "non-refrigerated / fast" [14]. Uncertainty is about ±15%, because flow regulators hold output roughly constant from 20 to 105 psi on Elkay units [14 family spec sheets]. Many units display a "bottles saved" counter, which suggests the user's bottle size is the more natural input.
- **UX copy:** **"Choose the bottle you filled. We'll log it as you drink it, not when you fill it."**

---

## Part 2: The "Equivalency" retention card

### 2.1 Design principles
- **Readable ratios.** People grasp "3 bathtubs" or "half a hot tub" easily. "0.0004 Olympic pools" or "2,317 shot glasses" are much harder to take in.
- **Truthful framings.** Every number comes from a cited value or a labeled derivation. For a range such as bathtubs, use a representative value and keep the range in metadata.
- **Three framing types:**
  - **Multiple:** "You've drunk **3.2 bathtubs**."
  - **Progress:** "You're **64% of the way** to filling a hot tub."
  - **Duration:** "That's **4 milliseconds of Niagara Falls**." (Used for flow-rate items; works at any scale.)
  - (Also **Days:** "Enough to keep an elephant going for **2 days**.")

### 2.2 The ladder (46 items, smallest to largest)

SF Symbol names are suggestions. Check each one in the SF Symbols app, because availability depends on the OS version; for example, `waterbottle` requires iOS 17. Where no matching glyph exists (camel, cement mixer), we suggest a generic one.

| # | Item | Liters | Source / derivation | One-line framing | SF Symbol idea |
|---|---|---|---|---|---|
| 1 | A habitual sip | 0.02 | 20 to 25 mL cup sips [1][3] | "That's about {n} sips, one at a time." | `drop` |
| 2 | A shot glass (1.5 fl oz) | 0.044 | NIAAA standard spirits pour, 1.5 fl oz [29] → 44 mL [derived] | "{n} shot glasses, all of them water." | `wineglass` |
| 3 | A US cup (8 fl oz) | 0.237 | 8 fl oz [26] | "{n} cups. Your grandma's '8 glasses' rule, met many times over." | `cup.and.saucer.fill` |
| 4 | A 330 mL can | 0.33 | EU can label size | "{n} cans' worth, with zero sugar." | `takeoutbag.and.cup.and.straw.fill` |
| 5 | A 12 oz soda can | 0.355 | 12 fl oz [26] | "{n} soda cans, minus the fizz." | `takeoutbag.and.cup.and.straw.fill` |
| 6 | A Starbucks Grande | 0.473 | 16 oz [23] | "{n} Grandes, and no line." | `cup.and.saucer` |
| 7 | A standard water bottle | 0.5 | 16.9 fl oz / 500 mL label | "{n} plastic bottles you didn't have to buy." | `waterbottle` |
| 8 | A Starbucks Venti Iced | 0.71 | 24 oz [23] | "{n} Venti Iced cups, minus the ice." | `cup.and.saucer.fill` |
| 9 | A wine bottle | 0.75 | TTB standard of fill, 750 mL [30] | "{n} wine bottles of the good stuff: H₂O." | `wineglass.fill` |
| 10 | A 32 oz Nalgene | 0.946 | 32 oz [22] | "{n} Nalgenes, the trail classic." | `waterbottle.fill` |
| 11 | A Stanley 40 oz Quencher | 1.183 | 40 oz [17] → 1,183 mL [derived] | "{n} Stanley cups. Viral and hydrated." | `cup.and.heat.waves` (or `waterbottle`) |
| 12 | A 2-liter bottle | 2.0 | label | "{n} party-size bottles." | `waterbottle` |
| 13 | A day's adequate intake (women) | 2.7 | NASEM total water AI, women 19 to 30 [31] | "{n} days of a woman's total recommended water." | `calendar` |
| 14 | A day's adequate intake (men) | 3.7 | NASEM total water AI, men 19 to 30 [31] | "{n} days of a man's total recommended water." | `calendar` |
| 15 | A gallon jug | 3.785 | 231 in³ [26] | "{n} gallon jugs. Gym-bro approved." | `drop.fill` |
| 16 | All the blood in your body | 5.0 | Average adult about 5 L [33] | "{n}× the blood in your body. (Don't worry, it went elsewhere.)" | `heart.fill` |
| 17 | A toilet flush (federal max) | 6.06 | 1.6 gal/flush, Energy Policy Act 1992 [34] → [derived] | "{n} flushes' worth, but you drank yours." | `toilet.fill` |
| 18 | An elephant's trunkful | 7.6 | A large elephant's trunk holds about 2 gal [37] → [derived] | "{n} elephant trunkfuls." | `pawprint.fill` |
| 19 | The water in your body | 42 | Up to 60% of an adult is water [32] × 70 kg reference adult [derived] | "You've drunk your own body's water content {n} times over." | `figure.stand` |
| 20 | A half-barrel beer keg | 58.7 | 15.5 gal [39] | "{n} kegs. Party of one, very hydrated." | `cylinder.fill` |
| 21 | A 10-minute WaterSense shower | 75.7 | 2.0 gpm WaterSense maximum [35] × 10 min [derived] | "{n} ten-minute showers, poured down your throat instead." | `shower.fill` |
| 22 | An oil barrel | 159 | 42 US gal [41] | "{n} oil barrels, much cleaner." | `cylinder.split.1x2.fill` |
| 23 | An elephant's daily drink | 175 | Savanna elephant needs 150 to 200 L/day [36] (mid-point) | "Enough to keep an elephant going for {n} days." | `pawprint.fill` |
| 24 | A 50-gallon water heater tank | 189 | Common family size [42] → [derived]. DOE sizes heaters by first-hour rating, not by tank [42] | "{n} water heater tanks, served cold." | `heater.vertical.fill` |
| 25 | A full bathtub | 200 | Typical capacity 40 to 80 gal, or 150 to 300 L [43]. A 2026 USGS finding that one Old Faithful eruption fills about 140 tubs implies about 200 L per tub [48] [derived] | "{n} bathtubs. Rubber duck not included." | `bathtub.fill` |
| 26 | A thirsty camel's chug | 200 | A camel can drink about 200 L in roughly 3 minutes [38] | "{n} camel-sized chugs. Took you a bit longer than 3 minutes." | `sun.max.fill` |
| 27 | A 55-gallon drum / rain barrel | 208 | 55 gal [40] → [derived] | "{n} rain barrels." | `cloud.rain.fill` |
| 28 | A year of drinking | 950 | NASEM survey beverage intake 2.2 to 3.0 L/day [31] → 2.6 × 365 [derived] | "{n} years of an average adult's drinking." | `calendar.circle` |
| 29 | A hot tub | 1,325 | Average 300 to 400 gal [44]; 350 gal [derived] | "{n} hot tubs. Bubbles optional." | `water.waves` |
| 30 | A fire engine's tank | 2,839 | NFPA 1901 minimum is 300 gal [45]; 500 to 750 gal is typical [45]; 750 gal [derived] | "{n} fire engine tanks, used for good." | `flame.fill` |
| 31 | A cement truck drum | 7,646 | Rated load 8 to 10 yd³ [46]; 10 yd³ [derived] | "{n} cement-mixer loads, but liquid." | `box.truck.fill` |
| 32 | An Old Faithful eruption | 27,900 | Average 27.9 m³ over 45 measured eruptions (range 12.2 to 44.3 m³), USGS 2026 [48] | "{n} Old Faithful eruptions, one sip at a time." | `humidity.fill` |
| 33 | A gasoline tanker truck | 32,176 | Typical load 8,000 to 8,500 gal [47]; 8,500 gal [derived] | "{n} tanker trucks of the only fuel you need." | `fuelpump.fill` |
| 34 | A backyard in-ground pool | 72,700 | 16 × 32 ft at 5 ft average depth ≈ 19,150 gal [49] [derived] | "{n} backyard pools. Cannonball!" | `figure.pool.swim` |
| 35 | A lifetime of drinking | 75,900 | 2.6 L/day × 365 × 80 yr [derived from 31] | "{n} of an entire human lifetime of drinking." | `hourglass` |
| 36 | A blue whale's single gulp | 80,000 | About 80 m³ per lunge [50] | "{n}% of one blue-whale gulp." | `fish.fill` |
| 37 | A small municipal water tower | 189,300 | 50,000 gal, the low end of a 50,000 to 1,000,000 gal range for elevated steel tanks [51] | "{n}% of a small-town water tower." | `building.2.fill` |
| 38 | A large water tower | 1,893,000 | 500,000 gal, common in manufacturer configurations [51] | "{n}% of a big-city water tower." | `building.2.fill` |
| 39 | An Olympic swimming pool | 2,500,000 | 50 m × 25 m × 2 m minimum depth under FINA/World Aquatics facilities rules [52] [derived] | "{n}% of an Olympic pool." | `figure.pool.swim` |
| 40 | Niagara Falls, 1 second | 2,832,000 | 100,000 cfs = 2,832 m³/s (tourist-season daytime flow) [53]. Flow is at least 50,000 cfs at other times; the long-run average is about 2,400 m³/s [53] | "Niagara Falls would pour that in {t} milliseconds." | `water.waves.and.arrow.down` |
| 41 | Mississippi at New Orleans, 1 second | 16,990,000 | Average 600,000 cfs [54] → [derived] | "The Mississippi moves that past New Orleans in {t}." | `water.waves` |
| 42 | Lake Bellagio (the fountain lake) | 83,280,000 | 22 million gal [55] → [derived] | "{n}% of the Bellagio fountain lake." | `sparkles` |
| 43 | Amazon River, 1 second | 209,000,000 | 209,000 m³/s [54] | "The Amazon empties that into the sea in {t}." | `water.waves` |
| 44 | Elephant water *loss*, hot day | 427 | Average daily loss on hot days (2020 study) [56] | "What an elephant sweats and breathes out on {n} hot days." | `thermometer.sun.fill` |
| 45 | A UK typical bath fill | 80 | Average UK bath uses about 80 L [43] | "{n} ordinary (not brim-full) baths." | `bathtub` |
| 46 | A pint glass | 0.473 | 16 oz [28] | "{n} pints. Bartender's pour, zero ABV." | `mug.fill` |

*Rows 44 to 46 are out of size order. They are alternates for variety and should be inserted in liter order in code.*

**Duration framing for flow items.** For any total `T` liters, compute `t = T / flow_L_per_s` and display it in the best unit:

| Total logged | Niagara (2,832,000 L/s) | Mississippi (16,990,000 L/s) | Amazon (209,000,000 L/s) |
|---|---|---|---|
| 2 L | 0.7 µs | 0.12 µs | 0.01 µs |
| 100 L | 35 µs | 5.9 µs | 0.48 µs |
| 1,000 L | 0.35 ms | 59 µs | 4.8 µs |
| 20,000 L | 7.1 ms | 1.2 ms | 96 µs |

[derived] Durations shorter than about 1 ms are hard to picture. Gate the duration framing to values of 1 ms or more, unless the app phrases it as "a blink-and-you-miss-it {t} µs".

### 2.3 Selection logic

**Goals:** pick 1 to 3 comparisons that are (a) readable, (b) varied from day to day, and (c) a mix of practical (household objects) and fun (animals, landmarks, nature), plus (d) one forward-looking milestone.

**Scoring rules**
- **Multiple** (`r = T / V`): valid when 1.5 ≤ r ≤ 50. Score peaks near r ≈ 4: a log-normal bump centered at log₁₀ 4 with σ ≈ 0.45. Whole numbers between 2 and 10 read best.
- **Progress** (`f = T / V`): valid when 0.10 ≤ f ≤ 0.95. Score rises toward f ≈ 0.6 to 0.9, the "almost there" range. People tend to work harder as a goal gets close (the goal-gradient effect [background]).
- **Duration:** valid when 1 ms ≤ t ≤ 60 s.
- **Days:** valid when 1.5 ≤ days ≤ 60.
- **Novelty:** −∞ if the item was shown in the last 3 days, −0.3 if shown in the last 7 days.
- **Celebration override:** If `T` crossed an item's volume since the card was last shown (r went from below 1 to 1 or more), show that item first with a celebratory framing.
- **Daily rotation:** add a small deterministic jitter, seeded by `hash(userID, yyyy-MM-dd)`. The card is then stable all day but changes tomorrow.

```swift
enum Framing { case multiple, progress, duration, days }
enum Category { case practical, fun }

struct Equivalent {
    let id: String
    let liters: Double          // V, or flow L/s for .duration, or L/day for .days
    let framings: Set<Framing>  // which framings make sense for this item
    let category: Category
    let symbol: String
    let template: [Framing: String]
}

func pickEquivalents(totalLiters T: Double,
                     ladder: [Equivalent],
                     history: ShownHistory,
                     userID: String, today: Date,
                     maxCount: Int = 3) -> [(Equivalent, Framing, Double)] {

    var rng = SeededRNG(seed: hash(userID, today.yyyyMMdd))
    var candidates: [(item: Equivalent, framing: Framing, value: Double, score: Double)] = []

    // 0. Tiny totals: just count sips.
    if T < 0.05 { return [(ladder["sip"], .multiple, T / 0.02)] }

    for item in ladder {
        for framing in item.framings {
            let value: Double
            var score: Double
            switch framing {
            case .multiple:
                value = T / item.liters
                guard (1.5...50).contains(value) else { continue }
                score = gaussian(log10(value), mean: log10(4), sd: 0.45)        // 0…1
                if abs(value - value.rounded()) < 0.1 && value <= 10 { score += 0.1 }
            case .progress:
                value = T / item.liters
                guard (0.10...0.95).contains(value) else { continue }
                score = 0.4 + 0.6 * value                                       // favors "almost there"
            case .duration:
                value = T / item.liters                                         // seconds
                guard value >= 0.001 && value <= 60 else { continue }
                score = 0.7
            case .days:
                value = T / item.liters
                guard (1.5...60).contains(value) else { continue }
                score = 0.75
            }
            // novelty
            if history.shownWithin(days: 3, id: item.id) { continue }
            if history.shownWithin(days: 7, id: item.id) { score -= 0.3 }
            // daily jitter for rotation
            score += Double.random(in: 0...0.25, using: &rng)
            candidates.append((item, framing, value, score))
        }
    }

    var result: [(Equivalent, Framing, Double)] = []

    // 1. Celebration: the largest item crossed since last view
    if let crossed = ladder.filter({ history.lastSeenTotal < $0.liters && T >= $0.liters
                                     && $0.framings.contains(.multiple) })
                           .max(by: { $0.liters < $1.liters }) {
        result.append((crossed, .multiple, T / crossed.liters))
    }

    // 2. Best practical multiple, 3. best fun item (any framing), 4. best progress milestone
    func best(_ pred: ((item: Equivalent, framing: Framing, value: Double, score: Double)) -> Bool) {
        if let c = candidates.filter({ pred($0) && !result.contains(where: { $0.0.id == c.item.id }) })
                             .max(by: { $0.score < $1.score }) {
            result.append((c.item, c.framing, c.value))
        }
    }
    best { $0.item.category == .practical && $0.framing == .multiple }
    best { $0.item.category == .fun }
    best { $0.framing == .progress }

    return Array(result.prefix(maxCount))
}
```

**Display rules**
- Round multiples to 2 significant figures ("3.4 bathtubs", "18 kegs"). Use whole numbers when r ≥ 10.
- Never show "1.0×". Below 1.5×, use the progress framing or the celebration.
- Progress values display as integer percent. Durations use µs, ms or s, rounded to 2 significant figures.
- Pluralize properly ("1 hot tub", "2 hot tubs"). Use "about" for any item marked as a range in metadata (bathtub, hot tub, fire engine, water tower).
- **Compact widget:** 1 item (the celebration if there is one, otherwise the top-scoring item). **Expanded card:** up to 3 items.
- **Tap for source:** each item shows its derivation ("Bathtub ≈ 200 L; typical tubs hold 150 to 300 L"). This builds trust and matches the app's accuracy-first approach.

**Worked examples** [derived]
- **T = 2 L** (day 1): "8.4 cups" or "2.7 wine bottles" (practical multiples near the sweet spot); "45 shot glasses" is valid but scores low. Progress: "53% of a gallon jug" or "74% of a day's adequate intake for women".
- **T = 300 L** (about 4 months): "1.5 bathtubs", "1.7 elephant-days", "23% of a hot tub". Celebration if the first bathtub was just passed.
- **T = 5,000 L** (about 5 years): "1.8 fire engine tanks", "65% of a cement truck drum", "Niagara would pour it in 1.8 ms".
- **T = 20,000 L** (a heavy multi-year user): "15 hot tubs", "72% of an Old Faithful eruption", "7 ms of Niagara".

---

## Key values

### Logging constants
| Constant | Default | Range / uncertainty | Basis |
|---|---|---|---|
| Sip / gulp (cup or bottle) | **20 mL** | 14 to 25 mL; habitual vs. natural drinking differ | [1][2][3][4] |
| Fountain gulp | **15 mL** | 10 to 20 mL | [derived from 2, 4] |
| Fountain intake rate | **8 mL/s** | 4 to 12 mL/s (±50%) | [derived; ceilings from 5, 6, 11–13] |
| Calibration: fountain/cup efficiency factor | 0.75 | unknown | [assumption] |
| Bottle filler, refrigerated | 69 mL/s (1.1 GPM) | 63 to 76 mL/s (1.0 to 1.2 GPM) | [14][15] |
| Bottle filler, non-refrigerated | 95 mL/s (1.5 GPM) | — | [14] |
| Bubbler output (not intake) | 20 to 47 mL/s | 0.32 to 0.74 GPM | [11][12][13] |
| ADA stream height | ≥ 4 in (100 mm) | — | [9] |

### Container presets (mL)
| Preset | mL |
|---|---|
| Sip | 20 |
| US cup | 237 |
| Metric glass | 250 |
| Mug | 350 |
| Can (EU / US) | 330 / 355 |
| Bottle | 500 |
| 20 oz bottle | 591 |
| 750 bottle | 750 |
| Stanley 30 / 40 oz | 887 / 1,183 |
| Hydro Flask 21 / 32 / 40 oz | 621 / 946 / 1,182 |
| Nalgene 32 oz | 946 |
| Owala 24 / 32 / 40 oz | 710 / 946 / 1,183 |
| Starbucks Tall / Grande / Venti hot / Venti iced / Trenta | 355 / 473 / 591 / 710 / about 917 |

### Equivalency anchors with the strongest sources
| Item | Liters | Source quality |
|---|---|---|
| Oil barrel | 159 | Strong (EIA) [41] |
| Olympic pool | 2,500,000 | Strong (World Aquatics minimums) [52] |
| Niagara, per second | 2,832,000 | Strong (treaty flow, Niagara Parks) [53] |
| Old Faithful eruption | 27,900 | Strong (USGS 2026 measurement) [48] |
| Blue whale gulp | 80,000 | Peer-reviewed estimate [50] |
| Bathtub | about 200 (150 to 300) | Weak (retailer ranges) [43] |
| Hot tub | about 1,325 (1,135 to 1,515) | Weak (Angi) [44] |
| Fire engine | about 2,839 (minimum 1,136) | Moderate (NFPA minimum, trade press typical) [45] |

---

## Open questions

1. **Fountain intake rate has no empirical basis.** A small in-house test would give Hydrate a real number: 10 to 20 people drinking from a bubbler for a timed 5 s, with water mass measured before and after using a cup held under the arc, or bottle weigh-ins. Until then, 8 mL/s is a derived estimate.
2. **Straw-lid sip volume.** Lawless et al. found straw sips smaller than cup sips in adults [1], but we could not get the full-text numbers. A large share of users drink from Stanley or Owala straw lids, so this matters.
3. **Ice displacement in iced drinks.** We found no reliable source for how much of an iced cup's volume is liquid. A 70% factor would be our own guess. Consider asking "with ice?" and verifying the factor before using it.
4. **ASME A112.18.1 bubbler flow requirements** and **AHRI 1010** were not accessible. We have manufacturer ratings only.
5. **Current Starbucks and McDonald's sizes** come from secondary sources and vary by country. The McDonald's US Large is reported as either 30 or 32 oz.
6. **Hydro Flask 40 oz and Owala capacities in mL** are converted from nominal oz. We found no official metric spec sheet that states fill-line volume.
7. **Showerhead federal maximum (2.5 gpm)** is [background] only. We used the verified WaterSense figure of 2.0 gpm [35].
8. **Bathtub and hot tub "averages"** rest on retailer content. Show them with "about" and their ranges.
9. **Should sex or height personalize sip size?** The data support it [1][4], but asking adds onboarding friction and is sensitive. Calibration achieves the same result without asking.
10. **Hughes & Wiles 1996 age and sex norms** for swallowing capacity are behind a paywall. They would let us tailor the swallowing ceiling by age.

---

## References

1. Lawless HT, Bender S, Oman C, Pelletier C. Gender, age, vessel size, cup vs. straw sipping, and sequence effects on sip volume. *Dysphagia*. 2003;18(3). doi:10.1007/s00455-002-0105-0. https://www.springermedizin.de/gender-age-vessel-size-cup-vs-straw-sipping-and-sequence-effects/8524174
2. Bennett JW, et al. Sip-sizing behaviors in natural drinking conditions compared to instructed experimental conditions. *Dysphagia*. 2009. doi:10.1007/s00455-008-9183-y. https://doi.org/10.1007/s00455-008-9183-y
3. Adnerhill I, Ekberg O, Groher ME. Determining normal bolus size for thin liquids. *Dysphagia*. 1989;4:1–3 (summarized in [2]). https://springerlink.bibliotecabuap.elogim.com/content/pdf/10.1007/s00455-008-9183-y.pdf
4. Factors influencing self-selected swallow volume, 95 healthy adults. *Dysphagia*. 2022;37(5):1172–1182. doi:10.1007/s00455-021-10373-6. https://doi.org/10.1007/s00455-021-10373-6
5. Hughes TA, Wiles CM. Clinical measurement of swallowing in health and in neurogenic dysphagia. *QJM*. 1996;89(2):109. https://academic.oup.com/qjmed/article/89/2/109/1556307
6. Timed water swallow test in stroke survivors vs. healthy participants (healthy mean 13.73 mL/s). *Eur Arch Otorhinolaryngol*. 2024. doi:10.1007/s00405-024-08884-7. https://link.springer.com/article/10.1007/s00405-024-08884-7
7. Physiopedia. Assessment of Dysphagia (100 mL water swallow test criteria). https://www.physio-pedia.com/Assessment_of_Dysphagia
8. Sequential swallowing of liquid in elderly adults: cup or straw? https://www.springermedicine.com/sequential-swallowing-of-liquid-in-elderly-adults-cup-or-straw/21129040
9. U.S. Access Board. 2010 ADA Standards, Chapter 6 (§602 Drinking Fountains). https://www.access-board.gov/ada/chapter/ch06/
10. U.S. Access Board. Guide to the ADA Standards, Chapter 6: Drinking Fountains. https://www.access-board.gov/ada/guides/chapter-6-drinking-fountains/
11. Elkay deck-mount push-button classroom bubbler (0.5 GPM; ASME A112.18.1). Ferguson listing. https://m.ferguson.com/product/elkay-deck-mount-single-hole-push-button-metal-classroom-bubbler-in-stainless-steel-elkssvr1141a/_/R-3156439
12. Chicago Faucets 748-244ABCP 0.74 GPM bubbler (ASME A112.18.1/CSA B125.1). https://www.ferguson.com/product/chicago-faucet-0-74-gpm-bubbler-or-drinking-fountain-in-polished-chrome-c748244abcp/_/R-4534667 ; https://www.webstaurantstore.com/chicago-faucets-748-244abcp-0-74-gpm-drinking-fountain-bubbler-with-2-3-8-lever-handle/857748244ABCP.html
13. T&S Brass B-2360 bubbler spec sheet (0.32 GPM at 4 in, 0.43 GPM at 8 in, 60 psi). https://cdn.restaurantsupply.com/pdf/B/2/3/B-2360-03.pdf
14. Elkay EZH2O bottle filling stations: 1.1 GPM refrigerated / 1.5 GPM non-refrigerated. https://chicagofaucetshoppe.com/Elkay-LZSTL8WSLK-EZH2O-Bi-Level-Bottle-p/elk-lzstl8wslk.htm ; EZS8WSSK listing: https://www.fergusonhome.com/elkay-ezs8wssk/s502393 ; EZS8WSLK spec: https://www.drinkingfountaindoctor.com/pdf/elkay/fountains/spec/EZS8WSLK-spec.pdf
15. Oasis VersaFiller 1.1 GPM listings and PWSMEBF manual (1.2 GPM default, 20 s maximum dispense). https://www.webstaurantstore.com/oasis-507012-pwsbf-versafiller-1-1-gpm-stainless-steel-retrofit-bottle-filling-station-kit-115v/81A507012.html ; https://www.thewaterguy.ca/library/pwsmebf_manual.pdf
16. Oasis PFCP10EBF spec sheet (ASHRAE 18 cooling capacity in gph). https://cdn.shopify.com/s/files/1/2680/3638/files/Oasis_48842_PFCP10EBF_Spec_Sheet.pdf
17. Stanley 1913. What Size Stanley Should You Get? https://www.stanley1913.com/blogs/my-stanley/stanley-cup-sizes-explained
18. Ace Hardware. Stanley Quencher H2.0 30 oz / 40 oz listings. https://www.acehardware.com/p/8100304 ; https://www.acehardware.com/p/8128688
19. Owala. Which water bottle size is best for me? https://owalalife.com/blogs/water-cooler/this-or-that-which-water-bottle-size-is-best-for-me
20. Hydro Flask Flex Cap bottles (32 oz = 946 mL). https://www.hydroflask.com/gb/shop/bottles-drinkware/bottles/flex-cap-bottles ; 21 oz Standard Mouth (621 mL): https://campmor.com/products/hydro-flask-21-oz-standard-mouth-bottle
21. Hunting Waterfalls. Hydro Flask Sizes Chart. https://huntingwaterfalls.com/hydro-flask-sizes-chart/
22. REI. Nalgene Wide-Mouth Water Bottle, 32 fl oz. https://rei.com/product/141628/nalgene-wide-mouth-water-bottle-32-fl-oz
23. Chowhound. Your Complete Guide to Starbucks' Coffee Sizes. https://www.chowhound.com/1829061/what-are-starbucks-coffee-sizes
24. The Daily Meal. The Ultimate Guide to McDonald's Soft Drinks. https://www.thedailymeal.com/1134964/the-ultimate-guide-to-mcdonalds-soft-drinks
25. FDA. Guidelines for Determining Metric Equivalents of Household Measures (1 cup = 240 mL). https://www.fda.gov/food/guidance-documents-regulatory-information-topic/guidance-industry-guidelines-determining-metric-equivalents-household-measures
26. Wikipedia. Gallon (US liquid gallon = 231 in³ = 3.785411784 L); Fluid ounce (29.5735295625 mL). https://www.wikipedia.com/wiki/US_gal ; https://EN.wikipedia.com/wiki/Fl_oz
27. Wayfair. Standard Mug Sizes. https://www.wayfair.com/sca/ideas-and-advice/guides/standard-mug-sizes-T24194
28. WebstaurantStore. Types of Beverageware; Libbey 16 oz pint glass. https://www.webstaurantstore.com/guide/1227/types-of-beverageware.html ; https://www.webstaurantstore.com/libbey-15385-restaurant-basics-16-oz-tall-mixing-glass-case/55115385.html
29. NIAAA. Rethinking Drinking: What is a standard drink? (archived). https://webarchive.library.unt.edu/web/20201218103258/http://rethinkingdrinking.niaaa.nih.gov/
30. TTB. Wine Labeling: Net Contents (authorized standards of fill). https://www.ttb.gov/regulated-commodities/beverage-alcohol/wine/labeling-wine/wine-labeling-net-contents
31. National Academies. Report Sets Dietary Intake Levels for Water, Salt, and Potassium (2004). https://www.nationalacademies.org/news/report-sets-dietary-intake-levels-for-water-salt-and-potassium-to-maintain-health-and-reduce-chronic-disease-risk
32. USGS Water Science School. The Water in You: Water and the Human Body. https://www.usgs.gov/water-science-school/science/water-you-water-and-human-body
33. StatPearls. Physiology, Blood Volume. https://www.ncbi.nlm.nih.gov/books/NBK526077
34. EPA WaterSense. Flushometer-valve toilets support statement (federal 1.6 gpf; WaterSense 1.28 gpf). https://www.epa.gov/sites/production/files/2017-01/documents/ws-products-support-statement-fv-toilets.pdf
35. EPA WaterSense. Specification for Showerheads v1.1 (2.0 gpm maximum). https://www.epa.gov/sites/production/files/2018-07/documents/ws-products-specification-showerheads-v1-1.pdf
36. San Diego Zoo Wildlife Alliance Library. African elephant fact sheet: Diet (150 to 200 L/day). https://ielc.libguides.com/sdzg/factsheets/african_elephant/diet
37. San Diego Zoo Wildlife Alliance Library. Asian elephant fact sheet: Diet (trunk about 2 gal; up to 225 L/day). https://ielc.libguides.com/sdzg/factsheets/asianelephant/diet
38. Baird CS. How much water can a camel store in its hump? West Texas A&M University, 2013. https://www.wtamu.edu/~cbaird/sq/2013/09/18/how-much-water-can-a-camel-store-in-its-hump/
39. KegWorks. Guide to Beer Keg Sizes (half barrel 15.5 gal). https://www.kegworks.com/blog/guide-to-beer-keg-sizes
40. Repackify. 55 Gallon Drum Dimensions. https://www.repackify.com/blog/55-gallon-drum-dimensions
41. U.S. EIA. International Energy Statistics: Units (1 barrel = 42 US gal = 159 L) (archived). https://webarchive.library.unt.edu/web/20120916015359/http://www.eia.gov/cfapps/ipdbproject/docs/unitswithpetro.cfm
42. U.S. DOE Energy Saver. Sizing a New Water Heater. https://www.energy.gov/energysaver/sizing-new-water-heater ; Direct Energy. What size water heater do I need? https://apps.directenergy.com/learning-center/what-size-water-heater-home
43. Hunker. Capacity of the Average Bathtub. https://www.hunker.com/13400924/capacity-of-the-average-bathtub ; Royal Bathrooms. How much water does a bathtub hold? https://royalbathrooms.co.uk/blog/how-much-water-does-a-bathtub-hold
44. Angi. How Much Water Does a Hot Tub Hold? https://angi.com/articles/how-much-water-does-a-hot-tub-hold.htm
45. NFPA 1901 pumper requirements summary (300 gal minimum). https://gfdtraining2011.blogspot.com/2011/01/pumper-fire-apparatus-requirements-nfpa.html ; Fire Apparatus Magazine. Departments Are Specifying Larger Pumps and Water Tanks on Engines. https://fireapparatusmagazine.com/?p=127215 ; Fire Engineering. Initial Supply. https://www.fireengineering.com/firefighting/initial-supply/
46. EngineerFix. How Many Cubic Feet in a Concrete Truck? https://engineerfix.com/how-many-cubic-feet-in-a-concrete-truck/ ; Chaney Enterprises. Evolution of concrete mixer trucks. https://www.chaneyenterprises.com/the-evolution-of-concrete-mixer-trucks-from-2-yards-to-10
47. Fire Engineering. Gasoline Tanker Emergencies, Part 1. https://www.fireengineering.com/industrial-firefighting/gasoline-tanker-emergencies-part-1/
48. USGS Yellowstone Volcano Observatory. How much water erupts from Old Faithful Geyser? (2026). https://www.usgs.gov/observatories/yvo/news/how-much-water-erupts-old-faithful-geyser ; USGS publication 70275178: Water volumes, heat flow, and solute discharge from Old Faithful Geyser eruptions. https://pubs.usgs.gov/publication/70275178 ; Buckrail. One Old Faithful eruption could fill 140 household bathtubs. https://buckrail.com/study-shows-one-old-faithful-eruption-could-fill-140-household-bathtubs/
49. HomeGuide. Swimming Pool Size Chart. https://homeguide.com/articles/swimming-pool-size-chart
50. Goldbogen JA, et al. Mechanics, hydrodynamics and energetics of blue whale lunge feeding. *J Exp Biol*. 2011;214:131. https://cob.silverchair.com/jeb/article-pdf/214/1/131/1435232/131.pdf ; UC Berkeley News (2007). https://newsarchive.berkeley.edu/news/media/releases/2007/11/27_lungewhale.shtml
51. Unified Facilities Guide Specification 33 16 15 (elevated welded steel tanks, 50,000 to 1,000,000 gal). https://legacy.wbdg.org/FFC/DOD/UFGS/UFGS%2033%2016%2015.pdf ; CST Aquastore composite elevated tanks brochure. https://www.cstindustries.com/wp-content/uploads/2021/01/Aquastore-Composite-Elevated-Tanks-Brochure-2021_web.pdf
52. Wikipedia. Olympic-size swimming pool (citing FINA Facilities Rules 2021–2025). https://en.wikipedia.org/wiki/Olympic-size_swimming_pool ; Fluidra. Olympic swimming pool size. https://www.fluidra.com/projects/olympic-swimming-pool-size/
53. Niagara Parks. Niagara Falls Geology Facts & Figures (100,000 cfs = 2,832 m³/s). https://www.niagaraparks.com/visit-niagara-parks/plan-your-visit/niagara-falls-geology-facts-figures/ ; Wikipedia. Niagara Falls. https://en.wikipedia.org/wiki/Niagara_Falls
54. National Park Service. Mississippi River Facts (Mississippi 600,000 cfs at New Orleans; Amazon 209,000 m³/s). https://nps.gov/miss/riverfacts.htm
55. Las Vegas Sun. Bellagio fountains (22 million gallons). https://m.lasvegassun.com/news/2012/apr/30/bellagio-fountains-help-whet-appetite-learning-dur/ ; Wikipedia. Fountains of Bellagio. https://www.wikipedia.org/wiki/Bellagio_Fountains
56. Phys.org. Elephants have the highest volume of daily water loss (2020). https://phys.org/news/2020-12-elephants-highest-volume-daily-loss.html
