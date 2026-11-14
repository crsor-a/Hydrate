# Verification of Note 04: Containers, Fountains and Equivalencies

*Verification pass on `Research/04-containers-fountains-equivalencies.md`, done 2026-11-14. The original note was not edited. Machine-readable output is in `verification/equivalencies.json` (ladder, bottles, chain cups, constants, references). Tags: **verified** means the value matches its source; **corrected** means a value, framing, symbol or source was changed; **new** means an item added to fill a gap.*

---

## TL;DR

- **20 corrections**: 5 numeric values, 3 logging constants, 7 framing lines or claims, 3 SF Symbol names, and 2 sources. Most of the 46 ladder figures check out against their sources. The real errors are the backyard pool arithmetic (72,700 → **72,491 L**), the hot-tub value (1,325 → **1,264 L**, DOE's 334-gallon representative spa), the Starbucks Trenta (about 917 → **887 mL**; starbucks.com lists it as 30 fl oz) and the McDonald's US Large (**887 mL**; McDonald's own US page names it "Large 30 oz").
- **Bathtub stays at 200 L, but now rests on government sources.** The USGS authors of the 2026 Old Faithful study equate 27.9 m³ to about 140 standard household tubs, which implies about 200 L per tub. Keep the range **136 to 265 L**: the USGS Water Science School uses 36 gal for a full tub and EPA uses up to 70 gal [9][10][11].
- **Fountain: one default, one calibration.** Default **8 mL/s** (plausible 6 to 12, clamp 4 to 15). This is no longer just a guess. Measured school fountains run at about **25.7 mL/s** (9 fl oz in 10.3 s) [3], and the public-health literature assumes a person drinking straight from the stream takes in **32 to 35%** of it, citing an ergonomics study of fountain efficiency [2][4][5]. 0.33 × 25.7 ≈ 8.5 mL/s. **Drop the 0.75 cup factor**: it has no source, and cup drinking measures swallowing, not the fountain stream. The replacement is a **stream-capture calibration**: hold a bottle under the stream for 5 s, enter the mL collected, and set rate = 0.33 × mL/s.
- **Ice:** there is no study, but chain guidance exists. Coca-Cola's foodservice crew poster says to fill the cup with **1/3 ice** [17], a restaurant cost model assumes 30% ice [18], and a 2016 lawsuit alleged that a 24 oz Starbucks Venti held about 14 oz of liquid (58%) [19]. Default **liquid fraction 0.75**, with light ice 0.85, extra ice 0.6, and 1.0 if the user also drinks the meltwater. Confidence: low.
- **SF Symbols: every suggested name exists.** I checked them against Apple's own `name_availability.plist` on this Mac (SF Symbols 2026.2) [1]. Two names are **deprecated renames**: `box.truck.fill` → `truck.box.fill` (iOS 17) and `water.waves.and.arrow.down` → `water.waves.and.arrow.trianglehead.down` (iOS 18). One is a poor fit: `cup.and.heat.waves` means a hot drink, and it needs iOS 18, for a cold Stanley tumbler. No glyph exists for a can, whale, camel, geyser or keg.
- **Ladder gaps:** two gaps were more than 3× below 10,000 L: shot glass → cup (5.4×) and elephant trunk → body water (5.5×). **Seven sourced items** close them: espresso, a 3 oz bathroom cup, a standard wine pour, an ENERGY STAR dishwasher load, a water-cooler jug, a 5-minute shower, and a day of US at-home water use. The largest gap left below 10,000 L is 2.7× (fire engine → cement truck). The ladder now has **53 items**.

---

## 1. Corrections table

| # | Item | Old | New | Source |
|---|---|---|---|---|
| 1 | Backyard pool (16 × 32 × 5 ft) | 72,700 L | **72,491 L** | Arithmetic: 2,560 ft³ × 28.3168 L/ft³. 19,150 gal × 3.7854 also gives 72,491; the old figure was a slip [56] |
| 2 | Hot tub | 1,325 L (350 gal, Angi) | **1,264 L** (334 gal); range 640 to 1,990 L | DOE's 2022 spa standards proposal uses a 334-gal unit as its representative hard-sided spa [13]. Manufacturer specs: Jacuzzi J-LX 440 gal full (330 average fill), Hot Spring Limelight Prism 525 gal, Hydropool 3-seat 204 gal [14] |
| 3 | Starbucks Trenta | "about 887 to 917 mL", key values about 917 | **887 mL (30 fl oz)** | starbucks.com Cold Brew page: Tall 12, Grande 16, Venti 24, Trenta 30 fl oz [15]. Coverage of the 2011 launch said 31 oz; the current site says 30 |
| 4 | McDonald's US Large | 887 (946) mL | **887 mL (30 oz)** | McDonald's US product page is titled "Coke (Large 30 oz Paper)" [16]. The 32 oz figure is an outlier from a third-party site |
| 5 | Hydro Flask 40 oz | 1,182 mL | **1,183 mL** | 40 × 29.5735 = 1,182.9 [43] |
| 6 | Fountain rate range | 4 to 12 mL/s | **6 to 12 mL/s** (clamp 4 to 15); default 8 unchanged | Stream × capture fraction, see §4 [2][3][4] |
| 7 | Fountain calibration factor | 0.75 × cup-drinking rate | **Removed.** Use stream capture: 0.33 × measured stream | §4 |
| 8 | Ice liquid fraction | 0.70 (unsourced guess) | **0.75** default; 0.85 / 0.6 / 1.0 options | §5 [17][18][19] |
| 9 | Elephant water loss framing | "What an elephant **sweats** and breathes out" | "What a zoo elephant loses (breath, skin, urine and all)" | The 427 L figure is *total* water turnover measured with a deuterium tracer, and it includes urine and faeces. Elephants have sweat glands only in their feet [33] |
| 10 | US cup framing | "Your grandma's '8 glasses' rule, met many times over" | "{n} measuring cups of water" | The line is wrong when n < 8, and it endorses the 8×8 rule, which the cited intake source (NASEM) does not use [48] |
| 11 | Year of drinking framing | "years of an average adult's drinking" | "years of the US recommended intake from drinks" | 2.2 and 3.0 L/day are the drink portions of the NASEM Adequate Intakes, not a measured average [48] |
| 12 | Body water framing | "Up to 60%" stated as a fixed 42 L | "about {n} times"; range 35 to 45 L | USGS says *up to* 60%; women and older adults are lower [47] |
| 13 | 500 mL bottle framing | "plastic bottles you didn't have to buy" | "standard 500 mL bottles" | The user may have logged bottled water, so the line could be false |
| 14 | Adequate Intake items (2.7 / 3.7 L) | "a woman's total recommended water" | Add "(food and drinks combined)" | About 20% of the AI comes from food; comparing drinks alone to the AI understates progress [48] |
| 15 | TL;DR claim on flow items | "Flow-rate items … work as a fallback for every user" | Only true once the total passes 2,832 L (Niagara at 1 ms, about 3 years at 2.6 L/day). Mississippi needs 17,000 L and the Amazon 209,000 L | The note's own 1 ms gate |
| 16 | SF Symbol, cement truck | `box.truck.fill` | **`truck.box.fill`** (iOS 17); the old name is a deprecated alias (iOS 16) | `name_aliases.strings` [1] |
| 17 | SF Symbol, Niagara | `water.waves.and.arrow.down` | **`water.waves.and.arrow.trianglehead.down`** (iOS 18); keep the legacy name if targeting iOS 16 or 17 | [1] |
| 18 | SF Symbol, Stanley 40 oz | `cup.and.heat.waves` (iOS 18, hot drink) | **`takeoutbag.and.cup.and.straw.fill`** (iOS 15) | [1] |
| 19 | Bathtub source | Retailer pages (Hunker, Royal Bathrooms) | **USGS 2026 + USGS Water Science School + EPA**; 200 L kept | [9][10][11] |
| 20 | Blue whale source | Goldbogen 2011 + UC Berkeley 2007 release | **Goldbogen 2011 corrected figure (80 m³ per lunge)** only | The Berkeley release gives 60 to 82 m³ for **fin** whales, not blue whales [36] |

**Values I checked that need no change:** sip 20 mL [65], shot 44 mL [40], wine bottle 750 mL [62], NASEM AIs 2.7 / 3.7 L [48], blood 5 L [46], toilet 6.06 L [45], trunk 7.57 L (about 2 gal) [35], keg 58.7 L [49], showers at 2.0 gpm [44], oil barrel 159 L [50], elephant 150 to 200 L/day [61], 50-gal heater 189 L [51], camel 200 L in 3 min [32], 55-gal drum 208 L [52], fire engine 2,839 L (NFPA 1901 minimum 300 gal) [53], cement truck 7,646 L [54], Old Faithful 27.9 m³ (± 9.4, n = 45, range 12.2 to 44.3) [9], tanker 32,176 L [55], lifetime 75,920 L, water towers [57], Olympic pool 2.5 ML (a minimum) [58], Niagara 100,000 cfs [59], Mississippi 600,000 cfs and Amazon 209,000 m³/s (NPS) [34], Bellagio 22 million gal [60]. I also rechecked every duration in the Niagara / Mississippi / Amazon table and every worked example (8.4 cups, 53% of a gallon, 1.5 bathtubs, 65% of a cement truck, 7 ms of Niagara): all are arithmetically correct.

**Aside (code, not data):** in the Swift `best(_:)` helper, the filter closure refers to `c.item.id` inside the expression that defines `c`, so it will not compile. Filter with `!result.contains { $0.0.id == candidate.item.id }` on the closure's own parameter.

---

## 2. Final verified ladder (53 items)

`liters` is in L, L/day (for "days of" framings) or L/s (flow items, used for "{t}" durations). Minimum iOS for each symbol comes from Apple's plist [1]. Insert in liter order in code. Kinds: **practical** = household or everyday, **fun** = animals, landmarks, body, **flow** = rivers and falls.

| # | Item | Liters | Unit | Kind | Framing | SF Symbol (min iOS) | Source # | Confidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | A habitual sip | 0.02 | L | practical | That's about {n} sips, one at a time. | `drop` (14.0) | [65] | medium | verified |
| 2 | A single espresso | 0.025 | L | practical | {n} espresso shots of water. No jitters. | `cup.and.saucer.fill` (15.0) | [39] | high | new |
| 3 | A shot glass (1.5 fl oz) | 0.0444 | L | practical | {n} shot glasses, all of them water. | `wineglass` (16.0) | [40], [43] | high | verified |
| 4 | A 3 oz bathroom cup | 0.0887 | L | practical | {n} little bathroom cups. | `sink.fill` (16.0) | [41], [43] | medium | new |
| 5 | A standard glass of wine (5 fl oz) | 0.148 | L | practical | {n} glasses of wine, zero hangover. | `wineglass.fill` (16.0) | [40], [43] | high | new |
| 6 | A US cup (8 fl oz) | 0.2366 | L | practical | {n} measuring cups of water. | `mug.fill` (16.1) | [43] | high | framing-corrected |
| 7 | A 330 mL can | 0.33 | L | practical | {n} cans' worth, with zero sugar. | `takeoutbag.and.cup.and.straw.fill` (15.0) | label | high | verified |
| 8 | A 12 oz soda can | 0.355 | L | practical | {n} soda cans, minus the fizz. | `takeoutbag.and.cup.and.straw.fill` (15.0) | [43] | high | verified |
| 9 | A Starbucks Grande | 0.473 | L | practical | {n} Grandes, and no line. | `cup.and.saucer` (15.0) | [15], [64] | high | verified |
| 10 | A US pint glass | 0.473 | L | practical | {n} pints. Bartender's pour, zero ABV. | `mug.fill` (16.1) | [43] | high | verified |
| 11 | A standard 500 mL bottle | 0.5 | L | practical | {n} standard 500 mL bottles. | `waterbottle` (17.0) | label | high | framing-corrected |
| 12 | A Starbucks Venti iced cup | 0.71 | L | practical | {n} Venti iced cups (24 oz), filled with just water. | `takeoutbag.and.cup.and.straw.fill` (15.0) | [15] | high | verified |
| 13 | A wine bottle | 0.75 | L | practical | {n} wine bottles of the good stuff: H2O. | `wineglass` (16.0) | [62] | high | verified |
| 14 | A 32 oz Nalgene | 0.946 | L | practical | {n} Nalgenes, the trail classic. | `waterbottle.fill` (17.0) | [22], [43] | high | verified |
| 15 | A 40 oz Stanley Quencher | 1.183 | L | practical | {n} Stanley cups. Viral and hydrated. | `takeoutbag.and.cup.and.straw.fill` (15.0) | [20], [43] | high | symbol-corrected |
| 16 | A 2-liter bottle | 2 | L | practical | {n} party-size bottles. | `waterbottle` (17.0) | label | high | verified |
| 17 | A day of a woman's total water intake target | 2.7 | L/day | practical | {n} days of a woman's total daily water target (food and drinks combined). | `calendar` (13.0) | [48] | high | framing-corrected |
| 18 | A day of a man's total water intake target | 3.7 | L/day | practical | {n} days of a man's total daily water target (food and drinks combined). | `calendar` (13.0) | [48] | high | framing-corrected |
| 19 | A gallon jug | 3.785 | L | practical | {n} gallon jugs. Gym-bro approved. | `drop.fill` (14.0) | [43] | high | verified |
| 20 | All the blood in your body | 5 | L | fun | {n} times the blood in your body. | `heart.fill` (13.0) | [46] | medium | verified |
| 21 | A toilet flush (US federal max) | 6.06 | L | practical | {n} toilet flushes' worth, but you drank yours. | `toilet.fill` (16.0) | [45] | high | verified |
| 22 | An elephant's trunkful | 7.57 | L | fun | {n} elephant trunkfuls. | `pawprint.fill` (15.0) | [35] | medium | verified |
| 23 | An efficient dishwasher load | 12.1 | L | practical | {n} loads in an ENERGY STAR dishwasher. | `dishwasher.fill` (16.0) | [37] | high | new |
| 24 | An office water-cooler jug | 18.9 | L | practical | {n} office water-cooler jugs. | `waterbottle.fill` (17.0) | [42], [43] | high | new |
| 25 | A 5-minute shower | 37.9 | L | practical | {n} five-minute showers, poured down your throat instead. | `shower.fill` (16.0) | [44] | high | new |
| 26 | The water in your body | 42 | L | fun | You've drunk your own body's water about {n} times over. | `figure.stand` (14.0) | [47] | medium | framing-corrected |
| 27 | A half-barrel beer keg | 58.7 | L | practical | {n} kegs. Party of one, very hydrated. | `cylinder.fill` (14.0) | [49] | high | verified |
| 28 | A 10-minute shower | 75.7 | L | practical | {n} ten-minute showers. | `shower.handheld.fill` (16.0) | [44] | high | verified |
| 29 | A typical UK bath | 80 | L | practical | {n} ordinary (not brim-full) baths. | `bathtub` (16.0) | [12] | medium | verified |
| 30 | An oil barrel | 159 | L | practical | {n} oil barrels, much cleaner. | `cylinder.split.1x2.fill` (14.0) | [50] | high | verified |
| 31 | An elephant's daily drink | 175 | L/day | fun | Enough to keep an elephant going for {n} days. | `pawprint.fill` (15.0) | [61] | medium | verified |
| 32 | A 50-gallon water heater tank | 189 | L | practical | {n} water heater tanks, served cold. | `heater.vertical.fill` (16.0) | [51] | medium | verified |
| 33 | A full bathtub | 200 | L | practical | About {n} bathtubs. Rubber duck not included. | `bathtub.fill` (16.0) | [9], [10], [11] | medium | source-corrected |
| 34 | A thirsty camel's chug | 200 | L | fun | {n} camel-sized chugs. Took you longer than 3 minutes. | `sun.max.fill` (13.0) | [32] | medium | verified |
| 35 | A 55-gallon drum | 208 | L | practical | {n} rain barrels. | `cloud.rain.fill` (13.0) | [52] | high | verified |
| 36 | A day of an American's at-home water use | 310 | L/day | practical | {n} days of an average American's water use at home. | `house.fill` (13.0) | [38] | high | new |
| 37 | An elephant's water loss on a hot day | 427 | L/day | fun | What a zoo elephant loses (breath, skin, urine and all) on {n} hot days. | `thermometer.sun.fill` (14.0) | [33] | medium | framing-corrected |
| 38 | A year of recommended drinking | 949 | L | practical | {n} years of the US recommended intake from drinks. | `calendar.circle` (13.0) | [48] | medium | framing-corrected |
| 39 | A hot tub | 1,264 | L | practical | About {n} hot tubs. Bubbles optional. | `water.waves` (16.0) | [13], [14] | medium | value-corrected |
| 40 | A fire engine's water tank | 2,839 | L | practical | About {n} fire engine tanks, used for good. | `flame.fill` (13.0) | [53] | medium | verified |
| 41 | A cement-mixer load | 7,646 | L | practical | {n} cement-mixer loads, but liquid. | `truck.box.fill` (17.0); legacy `box.truck.fill` (16.0) | [54] | medium | symbol-corrected |
| 42 | An Old Faithful eruption | 27,900 | L | fun | {n} Old Faithful eruptions, one sip at a time. | `humidity.fill` (15.0) | [9] | high | verified |
| 43 | A gasoline tanker truck | 32,176 | L | practical | {n} tanker trucks of the only fuel you need. | `fuelpump.fill` (15.0) | [55] | medium | verified |
| 44 | A backyard in-ground pool | 72,491 | L | practical | {n} backyard pools. Cannonball! | `figure.pool.swim` (16.0) | [56] | medium | value-corrected |
| 45 | A lifetime of drinking | 75,920 | L | fun | {n}% of a whole lifetime of drinking. | `hourglass` (13.0) | [48] | medium | verified |
| 46 | A blue whale's single gulp | 80,000 | L | fun | {n}% of one blue-whale gulp. | `fish.fill` (16.0) | [36] | medium | source-corrected |
| 47 | A small-town water tower | 189,271 | L | practical | {n}% of a small-town water tower. | `building.2.fill` (14.0) | [57] | medium | verified |
| 48 | A big-city water tower | 1,892,706 | L | practical | {n}% of a big-city water tower. | `building.2.fill` (14.0) | [57] | medium | verified |
| 49 | An Olympic swimming pool | 2,500,000 | L | fun | {n}% of an Olympic pool. | `figure.pool.swim` (16.0) | [58] | high | verified |
| 50 | Niagara Falls, per second | 2,831,685 | L/s | flow | Niagara Falls would pour that in {t}. | `water.waves.and.arrow.trianglehead.down` (18.0); legacy `water.waves.and.arrow.down` (16.0) | [59] | high | symbol-corrected |
| 51 | The Mississippi at New Orleans, per second | 16,990,108 | L/s | flow | The Mississippi moves that past New Orleans in {t}. | `water.waves` (16.0) | [34] | high | verified |
| 52 | Lake Bellagio (the fountain lake) | 83,279,000 | L | fun | {n}% of the Bellagio fountain lake. | `sparkles` (13.0) | [60] | medium | verified |
| 53 | The Amazon, per second | 209,000,000 | L/s | flow | The Amazon empties that into the sea in {t}. | `water.waves` (16.0) | [34] | high | verified |

### Framing and selection notes
- **Use "about"** for items with a `rangeLiters` field: bathtub, hot tub, fire engine, cement truck, body water, blood, elephant/day, Old Faithful, sip.
- **Localize the pint.** A UK pint is 568 mL. For UK users, show the pint item at 0.568 L or hide it.
- **No glyph exists** for a can, whale, camel, geyser, keg or bubbler. I searched all 9,649 names in the plist. The stand-ins (`takeoutbag.and.cup.and.straw.fill`, `fish.fill`, `sun.max.fill`, `humidity.fill`, `cylinder.fill`) are approximations. A blue whale is a mammal, so `fish.fill` is only a placeholder; consider a custom SF Symbol for the whale and the can.
- **Gap check after additions:** no two adjacent items below 10,000 L are more than 2.7× apart.
- **Flow items:** with the 1 ms gate, Niagara first appears at 2,832 L (about 3 years at 2.6 L/day). If you want flow items earlier, allow "{t} µs" phrasing, or add a smaller flow item. (I did not source one, so none is included.)

### Extra items added (gap fillers)
| Item | Liters | Fills gap | Source |
|---|---|---|---|
| Single espresso | 0.025 | sip → shot | Italian Espresso National Institute certified espresso: 25 mL ± 2.5 in the cup [39] |
| 3 oz bathroom cup | 0.0887 | shot → cup (5.4×) | Dixie 3 oz bath cups (retail listing) [41] |
| Standard glass of wine | 0.148 | shot → cup | NIAAA standard drink: 5 fl oz wine [40] |
| ENERGY STAR dishwasher load | 12.1 | trunk → body water (5.5×) | ENERGY STAR v7: at most 3.2 gal per cycle (federal limit 5.0) [37] |
| Water-cooler jug | 18.9 | trunk → body water | 5 US gal (18.9 L) cooler bottle [42] |
| 5-minute shower | 37.9 | trunk → body water | WaterSense 2.0 gpm × 5 min [44] |
| A day of US at-home use | 310 (L/day) | drum → elephant loss | EPA WaterSense: 82 gal per person per day at home (citing USGS 2015) [38] |

---

## 3. SF Symbols check

**Method.** Instead of third-party mirrors, I read Apple's own symbol database on this Mac: `/System/Library/CoreServices/CoreGlyphs.bundle/Contents/Resources/name_availability.plist`, which maps every symbol to its release year and minimum OS (9,649 symbols, newest release 2026.2 = iOS 27.2), along with `name_aliases.strings`, which lists deprecated names (1,130 aliases) [1]. The build script asserted that every final symbol exists and is not deprecated.

| Original suggestion | Exists? | Added (iOS) | Verdict |
|---|---|---|---|
| `drop`, `drop.fill` | yes | 14.0 | ok |
| `wineglass`, `wineglass.fill` | yes | 16.0 | ok |
| `cup.and.saucer`, `cup.and.saucer.fill` | yes | 15.0 | ok |
| `takeoutbag.and.cup.and.straw.fill` | yes | 15.0 | ok (no can glyph exists) |
| `waterbottle`, `waterbottle.fill` | yes | 17.0 | ok (the original note was right that it needs iOS 17) |
| `cup.and.heat.waves` | yes | 18.0 | **replace**: means a hot drink, and gated to iOS 18 |
| `calendar`, `calendar.circle` | yes | 13.0 | ok |
| `heart.fill` | yes | 13.0 | ok |
| `toilet.fill` | yes | 16.0 | ok |
| `pawprint.fill` | yes | 15.0 | ok |
| `figure.stand` | yes | 14.0 | ok |
| `cylinder.fill`, `cylinder.split.1x2.fill` | yes | 14.0 | ok |
| `shower.fill` | yes | 16.0 | ok |
| `heater.vertical.fill` | yes | 16.0 | ok |
| `bathtub`, `bathtub.fill` | yes | 16.0 | ok |
| `sun.max.fill`, `cloud.rain.fill`, `flame.fill`, `hourglass`, `sparkles` | yes | 13.0 | ok |
| `water.waves` | yes | 16.0 | ok |
| `box.truck.fill` | yes, **deprecated** | 16.0 | use `truck.box.fill` (17.0) |
| `humidity.fill`, `fuelpump.fill` | yes | 15.0 | ok |
| `figure.pool.swim`, `fish.fill` | yes | 16.0 | ok (`fish.fill` for a whale is a stretch) |
| `building.2.fill` | yes | 14.0 | ok |
| `water.waves.and.arrow.down` | yes, **deprecated** | 16.0 | use `water.waves.and.arrow.trianglehead.down` (18.0), or keep the legacy name below iOS 18 |
| `thermometer.sun.fill` | yes | 14.0 | ok |
| `mug.fill` | yes | **16.1** | ok; note the point release |

**New symbols used:** `sink.fill` (16.0), `dishwasher.fill` (16.0), `shower.handheld.fill` (16.0), `house.fill` (13.0), `truck.box.fill` (17.0), `water.waves.and.arrow.trianglehead.down` (18.0). **Invalid (nonexistent) names found: 0. Deprecated: 2. Poor fit: 1.** If the app's minimum target is iOS 17, everything in the final ladder works, except that Niagara must use its legacy name (the JSON carries `sfSymbolLegacy` for this).

---

## 4. Fountain constants (final)

### Evidence found
1. **Measured fountain streams.** In 2016, Kenney et al. timed how long school drinking sources took to fill a 9 fl oz cup. Fountains averaged **10.34 s**, which is **25.7 mL/s** [3]. That sits inside the 20 to 47 mL/s manufacturer range from the original note [7].
2. **How much of the stream people take in.** Two school water-intake studies estimate fountain intake as *time at the fountain × flow × capture fraction*. They use **32%** (Kenney 2015, AJPH) and **35%** (IJERPH 2020) for students drinking straight from the stream. Both cite **Coetzee & Bennett 1978, "The efficiency of a drinking fountain," *Applied Ergonomics* 9:97–100**, which measured what share of the stream users actually drank across eight flow rates. That study found fountains highly inefficient and least efficient at extreme flow rates [2][4][5]. The paper itself is paywalled, so I have its findings only through these citing papers.
3. **Observed totals.** With this method, students drinking directly from fountains averaged about **2.0 to 2.4 fl oz per lunch period**, compared with **5.2 oz with a cup** [2][4]. This shows that capture, not swallowing, is the bottleneck.
4. **Swallowing ceiling** (unchanged): healthy cup drinking as fast as is comfortable is about 13.7 mL/s [6].
5. **Not found:** no dysphagia or swallow-flow paper measures intake at a bubbler. One search summary attributed "1.8 oz per 3–6 s use" to the 1978 study, but I could not find that figure in any retrievable source, so I do not use it.

### Final constants
| Constant | Value | Justification |
|---|---|---|
| **Default fountain intake rate** | **8 mL/s** | 0.33 × 25.7 mL/s = 8.5, rounded down to stay conservative. Independent cross-check: the original bottom-up swallow estimate (4 to 13, centre 8) |
| Plausible range | 6 to 12 mL/s | 0.33 × the 20 to 35 mL/s typical bubbler range [7][3]; the top end is capped below the 13.7 mL/s swallowing ceiling [6] |
| Clamp for calibrated values | 4 to 15 mL/s | Allows weak and strong outliers |
| Stream capture fraction | **0.33** | Mid-point of the 0.32 and 0.35 used in the literature [2][4], based on [5] |
| Gulp alternative | 15 mL/gulp | Unchanged from the original note (derived, low confidence) |
| Rounding | nearest 5 mL | Unchanged |

### Calibration method (replaces the 0.75 cup factor)
**"Measure your fountain" (about 15 s, done at the fountain):**
1. The app runs a **5-second countdown**. The user holds their bottle or a cup under the stream. The ADA requires the stream to be at least 4 in high so that a cup or glass can be held under it [8].
2. The user enters what they collected: bottle graduations, "about ¼ of my 500 mL bottle", or a picker in 10 mL steps. Alternative: time how long the stream takes to fill to a known mark.
3. `fountain_rate = clamp(0.33 × collected_mL / seconds, 4, 15)`. Save it per fountain (for example, "work", "gym") or as a global value.
4. **No-measure fallback:** a stream-strength picker. Weak = 6, normal = 8, strong = 11 mL/s (0.33 × roughly 19 / 25.7 / 34 mL/s) [derived].

*Why not cup drinking?* Drinking 250 mL from a glass measures how fast a person swallows. The literature shows that fountain intake is limited by how much of the arc reaches the mouth, which depends on the fountain. The 0.75 factor had no source.

UX copy: **"We count about 8 mL for each second at a fountain, roughly a third of what the spout puts out. Measure your fountain once for a closer number."**

---

## 5. Ice in iced drinks (final)

| Evidence | What it says | Strength |
|---|---|---|
| Coca-Cola foodservice "Valves of Gold" crew poster (©2015) | "Fill the cup with 1/3 ice" for best quality [17] | Chain/bottler standard |
| McDonald's US nutrition note | Fountain-drink calories are based on "standard fill levels plus ice" [63] | Shows nominal cup sizes include ice |
| Restaurant cost calculator | Assumes a 30% ice fill (16 oz cup → 11.2 oz liquid) [18] | Industry model, no data |
| 2016 Pincus v. Starbucks complaint | Alleged a 24 oz Venti iced held about 14 oz of liquid (58%) [19] | Allegation, not a finding |
| Peer-reviewed studies | None found | — |

**Recommendation.** Ask "With ice?" only for cups flagged as iced (chain cold cups, tumblers). Use **liquid fraction = 0.75** by default (between Coca-Cola's 1/3-ice standard and the 58% end alleged for Starbucks), **0.85 for light ice, 0.6 for extra ice**, and **1.0** if the user says they drank the melted ice too. Melted ice is plain water and counts toward intake. Confidence is low, so show "about" and let the user edit. The Starbucks Venti iced (24 oz) at 0.75 logs 532 mL.

---

## 6. Final bottle catalog

Store **exact mL from nominal US fl oz** (1 fl oz = 29.5735 mL [43]). Exception: brands that specify bottles in metric (LARQ, S'well, CamelBak's international labels) state their own mL, which can differ from the oz conversion; the notes column shows these cases. Capacities are nominal (brim-full); lids, straws, filters and ice reduce what the bottle holds in use.

| Brand | Model | Nominal oz | mL to store | Source # | Confidence | Note |
|---|---|---|---|---|---|---|
| Stanley | Quencher H2.0 14 oz | 14 | 414 | [20] | high |  |
| Stanley | Quencher H2.0 20 oz | 20 | 591 | [20] | high |  |
| Stanley | Quencher H2.0 30 oz | 30 | 887 | [20] | high |  |
| Stanley | Quencher H2.0 40 oz | 40 | 1,183 | [20] | high |  |
| Stanley | Quencher H2.0 64 oz | 64 | 1,893 | [20] | high |  |
| Hydro Flask | Standard Mouth 21 oz | 21 | 621 | [21] | high |  |
| Hydro Flask | Standard Mouth 24 oz | 24 | 710 | [21] | high |  |
| Hydro Flask | Wide Mouth 20 oz | 20 | 591 | [21] | high |  |
| Hydro Flask | Wide Mouth 32 oz | 32 | 946 | [21] | high |  |
| Hydro Flask | Wide Mouth 40 oz | 40 | 1,183 | [21] | high |  |
| Hydro Flask | Wide Mouth 64 oz | 64 | 1,893 | [21] | high |  |
| Nalgene | Wide Mouth 32 oz | 32 | 946 | [22] | high | Often marketed as 1 L; nominal 32 oz = 946 mL. |
| Nalgene | Wide Mouth 16 oz | 16 | 473 | [22] | high |  |
| Owala | FreeSip 24 oz | 24 | 710 | [23] | high |  |
| Owala | FreeSip 32 oz | 32 | 946 | [23] | high |  |
| Owala | FreeSip 40 oz | 40 | 1,183 | [23] | high |  |
| YETI | Rambler bottle 18 oz | 18 | 532 | [24] | high |  |
| YETI | Rambler bottle 26 oz | 26 | 769 | [24] | high |  |
| YETI | Rambler bottle 36 oz | 36 | 1,065 | [24] | high |  |
| YETI | Rambler bottle 46 oz | 46 | 1,360 | [24] | high |  |
| YETI | Rambler bottle 64 oz | 64 | 1,893 | [24] | high |  |
| YETI | Rambler tumbler 20 oz | 20 | 591 | [24] | high |  |
| YETI | Rambler tumbler 30 oz | 30 | 887 | [24] | high |  |
| CamelBak | Chute Mag 20 oz | 20 | 591 | [25] | high | CamelBak's metric label: 0.6 L. |
| CamelBak | Eddy+ 20 oz | 20 | 591 | [25] | medium | Sizes from CamelBak and retailer listings; metric label 0.6 L. |
| CamelBak | Chute Mag 25 oz | 25 | 739 | [25] | high | CamelBak's metric label: 0.75 L. |
| CamelBak | Eddy+ 25 oz | 25 | 739 | [25] | medium | Sizes from CamelBak and retailer listings; metric label 0.75 L. |
| CamelBak | Chute Mag 32 oz | 32 | 946 | [25] | high | CamelBak's metric label: 1 L. |
| CamelBak | Eddy+ 32 oz | 32 | 946 | [25] | medium | Sizes from CamelBak and retailer listings; metric label 1 L. |
| Contigo | West Loop 2.0 travel mug 16 oz | 16 | 473 | [26] | high |  |
| Contigo | Jackson Chill 2.0 20 oz | 20 | 591 | [26] | high |  |
| Contigo | Ashland 2.0 24 oz | 24 | 710 | [26] | high |  |
| Contigo | Cortland 2.0 24 oz | 24 | 710 | [26] | high |  |
| Contigo | Cortland Chill 2.0 32 oz | 32 | 946 | [26] | high |  |
| S'well | Original 9 oz | 9 | 260 | [27] | medium | Retailers label it 260 mL; exact 9 oz = 266 mL. |
| S'well | Original 17 oz | 17 | 500 | [27] | medium | Labelled 500 mL. |
| S'well | Original 25 oz | 25 | 750 | [27] | medium | Labelled 750 mL. |
| LARQ | Bottle PureVis 17 oz | 17 | 500 | [28] | high | LARQ spec: 500 mL. Filtered version holds 430 mL. |
| LARQ | Bottle PureVis 25 oz | 25 | 740 | [28] | high | LARQ spec: 740 mL. Filtered version holds 670 mL. |
| Simple Modern | Summit 22 oz | 22 | 651 | [29] | medium | Size from simplemodern.com product listings; line changes often. |
| Simple Modern | Summit 32 oz | 32 | 946 | [29] | medium | Size from simplemodern.com product listings; line changes often. |
| Simple Modern | Summit 40 oz | 40 | 1,183 | [29] | medium | Size from simplemodern.com product listings; line changes often. |
| Simple Modern | Summit 64 oz | 64 | 1,893 | [29] | medium | Size from simplemodern.com product listings; line changes often. |
| Simple Modern | Summit 2 30 oz | 30 | 887 | [29] | high |  |
| Simple Modern | Summit Kids 14 oz | 14 | 414 | [29] | high |  |
| Simple Modern | Summit Kids 18 oz | 18 | 532 | [29] | high |  |
| Ello | Cooper 22 oz | 22 | 651 | [30] | medium | Retailer listings; no manufacturer page reachable. |
| Ello | Cooper 32 oz | 32 | 946 | [30] | medium | Retailer listings; no manufacturer page reachable. |
| Brita | Filtering bottle 20 oz (stainless) | 20 | 591 | [31] | medium | Retailer listings; filter reduces usable volume. |
| Brita | Filtering bottle 26 oz (plastic) | 26 | 769 | [31] | medium | Retailer listings; filter reduces usable volume. |
| Brita | Filtering bottle 36 oz (plastic) | 36 | 1,065 | [31] | medium | Retailer listings; filter reduces usable volume. |

**Notes.** Stanley's Quencher sizes (14/20/30/40/64 oz) are confirmed on stanley1913.com's Quencher collection and size guide; the US site lists oz only [20]. YETI's bottle line is 18/26/36/46/64 oz [24]. Owala FreeSip comes in 24/32/40 oz [23]. Contigo's current US lineup is on gocontigo.com (contigo.com is an unrelated company) [26]. Ello and Brita pages were not reachable, so their sizes come from retailer listings (medium confidence) [30][31].

### Chain cups (verified)
| Chain / size | fl oz | mL | Source |
|---|---|---|---|
| Starbucks Short (hot) | 8 | 237 | starbucks.com Pike Place page [64] |
| Starbucks Tall | 12 | 355 | [15][64] |
| Starbucks Grande | 16 | 473 | [15][64] |
| Starbucks Venti (hot) | 20 | 591 | [64] |
| Starbucks Venti (iced) | 24 | 710 | [15] |
| Starbucks Trenta (iced) | **30** | **887** | [15] |
| McDonald's US Large | **30** | **887** | McDonald's US page "Coke (Large 30 oz Paper)" [16] |
| McDonald's US Medium / Small | 21 / 16 | 621 / 473 | secondary (The Daily Meal); McDonald's pages did not show oz |

---

## 7. References

1. Apple. SF Symbols system database on macOS 27.2 (SF Symbols 2026.2): `name_availability.plist` and `name_aliases.strings` in `/System/Library/CoreServices/CoreGlyphs.bundle/Contents/Resources/`. Overview: https://developer.apple.com/sf-symbols/
2. Kenney EL, Gortmaker SL, Carter JE, Howe MCW, Reiner JF, Cradock AL. Grab a Cup, Fill It Up! *Am J Public Health*. 2015;105:1777–1783 (32% capture assumption; 2.4 vs 5.2 oz). https://pmc.ncbi.nlm.nih.gov/articles/PMC4539814
3. Kenney EL, Gortmaker SL, Cohen JFW, Rimm EB, Cradock AL. Limited school drinking water access for youth. *J Adolesc Health*. 2016;59(1):24–29 (fountain fill time for 9 oz: 10.34 s). https://pmc.ncbi.nlm.nih.gov/articles/PMC4920716/
4. Providing Students with Adequate School Drinking Water Access in an Era of Aging Infrastructure: A Mixed Methods Investigation. *Int J Environ Res Public Health*. 2020;17(1):62 (35% capture assumption; 2.0 oz at lunch). https://pmc.ncbi.nlm.nih.gov/articles/PMC6981468/
5. Coetzee K, Bennett C. The efficiency of a drinking fountain. *Applied Ergonomics*. 1978;9(2):97–100. doi:10.1016/0003-6870(78)90155-2. https://www.sciencedirect.com/science/article/abs/pii/0003687078901552 (abstract paywalled; findings via [2][4])
6. Timed water swallow test, healthy mean 13.73 mL/s. *Eur Arch Otorhinolaryngol*. 2024. https://link.springer.com/article/10.1007/s00405-024-08884-7
7. Bubbler flow specs (from the original note): T&S B-2360 https://cdn.restaurantsupply.com/pdf/B/2/3/B-2360-03.pdf ; Elkay 0.5 GPM https://m.ferguson.com/product/elkay-deck-mount-single-hole-push-button-metal-classroom-bubbler-in-stainless-steel-elkssvr1141a/_/R-3156439 ; Chicago Faucets 0.74 GPM https://www.ferguson.com/product/chicago-faucet-0-74-gpm-bubbler-or-drinking-fountain-in-polished-chrome-c748244abcp/_/R-4534667
8. U.S. Access Board. 2010 ADA Standards §602.6 (stream at least 4 in high, to allow a cup or glass). https://www.access-board.gov/ada/chapter/ch06/
9. USGS Yellowstone Volcano Observatory. How much water erupts from Old Faithful Geyser? (2026; 27.9 ± 9.4 m³, 45 eruptions; "about 140 standard household bathtubs"). https://www.usgs.gov/observatories/yvo/news/how-much-water-erupts-old-faithful-geyser ; paper record: https://www.usgs.gov/publications/water-volumes-heat-flow-and-solute-discharge-old-faithful-geyser-eruptions-yellowstone
10. USGS Water Science School. How much water do you use at home? (full tub about 36 gal). https://water.usgs.gov/edu/activity-percapita.html
11. EPA (archived 2008). Simple water-saving steps ("a full bath tub requires about 70 gallons"). https://webarchive.library.unt.edu/eot2008/20080916161824/http:/www.epa.gov/watersense/water/simple.htm ; WaterSense Current, Summer 2017: https://19january2021snapshot.epa.gov/watersense/watersense-current-summer-2017_.html
12. Saga Magazine. Bath vs shower (about 80 L per bath, attributed to Waterwise). https://www.saga.co.uk/magazine/homes/bath-vs-shower-which-is-better-for-you-and-your-wallet
13. U.S. DOE. Energy Conservation Standards for Portable Electric Spas, NOPR, 87 FR 69082 (Nov 17, 2022) (representative 334-gal hard-sided unit; 200-gal inflatable). https://www.govinfo.gov/content/pkg/FR-2022-11-17/html/2022-24290.htm
14. Manufacturer spa specs: Jacuzzi J-LX (440 gal full, 330 average fill) https://galaxyhomerecreation.com/wp-content/uploads/2023/08/J-LX.pdf ; Hot Spring Limelight Prism (525 gal) https://www.hotspring.com/wp-content/uploads/2018/09/2019-hot-spring-limelight-prism-spec-sheet-rev-d.pdf ; Hydropool Signature technical specifications (379: 204 gal) https://www.hydropoolhottubs.com/-/media/Project/Sites/Hydropool/Documents---Brochures-Buyers-Guides-Owner-Manuals/Technical-Specifications-and-Drawings/Hot-Tubs/Signature-Collection-Technical-Specifications-and-Drawings.pdf
15. Starbucks. Cold Brew product page (Tall 12, Grande 16, Venti 24, Trenta 30 fl oz), accessed 2026-11-13. https://www.starbucks.com/menu/product/2121255/iced
16. McDonald's US. "Coke (Large 30 oz Paper)" product page. https://www.mcdonalds.com/us/es-us/product/coca-cola-large-no-ice.html
17. The Coca-Cola Company. Valves of Gold foodservice crew poster ("Fill the cup with 1/3 ice"). https://www.cokesolutions.com/content/dam/cokesolutions/us/documents/foodservice-quality/foodservice-quality-ValvesfGoldCrewPosterFSR.pdf
18. RestaurantCalcs. Fountain drink cost calculator (30% ice assumption). https://restaurantcalcs.com/calculators/fountain-cost/
19. ABA Journal (2016). Suit says Starbucks puts too much ice in cups (24 oz vs about 14 oz liquid alleged). https://www.abajournal.com/news/article/customer_lawsuit_says_her_starbucks_cup_runneth_over_with_ice_cubes ; Quartz: https://qz.com/674232/clearly-meant-to-mislead-the-complaint-filed-against-starbucks-for-putting-too-much-ice-in-iced-drinks
20. Stanley 1913. Cup sizes explained; Quencher collection (14/20/30/40/64 oz). https://www.stanley1913.com/blogs/my-stanley/stanley-cup-sizes-explained ; https://www.stanley1913.com/collections/adventure-quencher-travel-tumblers
21. Hydro Flask. Bottles collection. https://www.hydroflask.com/shop/bottles-drinkware/bottles
22. Nalgene. 32oz Wide Mouth Bottle (Bottle Volume: 32oz). https://nalgene.com/product/32oz-wide-mouth-bottle/
23. Owala. FreeSip (24/32/40 oz). https://owalalife.com/products/freesip
24. YETI. Bottles (Rambler 18/26/36/46/64 oz; tumblers 20/30 oz). https://www.yeti.com/drinkware/bottles
25. CamelBak. Chute Mag 20/25/32 oz pages: https://www.camelbak.com/product/chute-mag-25oz-bottle-with-tritan%E2%84%A2-renew/CB-2470.html ; 32 oz (1L): https://international.camelbak.com/en/bottles/R02028--Chute_Mag_Vacuum_32oz ; Eddy+ 20 oz: https://www.camelbak.com/recreation/bottles/stainless-steel/CB-1649.html
26. Contigo. Water bottles. https://www.gocontigo.com/water-bottles-2/
27. S'well. Original Bottle (9/17/25 oz). https://www.swell.com/products/moonstone-bottle ; 260 mL retail label: https://www.altitude-sports.com/p/swell-bottle-9oz-swl-sw09bt
28. LARQ Support. Specifications (PureVis 17 oz / 500 mL; 25 oz / 740 mL). https://support.livelarq.com/hc/en-us/articles/36962689064219-Specifications ; filtered capacities: https://www.livelarq.com/support/larq-bottle-filtered
29. Simple Modern. Summit collection and product pages. https://www.simplemodern.com/collections/summit ; https://simplemodern.com/products/summit-water-bottle-with-straw-lid-chug-lid-and-handle-lid-64oz-8
30. Ello Cooper 22/32 oz (Walmart listings). https://www.walmart.com/ip/Ello-Cooper-32oz-Stainless-Steel-Water-Bottle/3689898080 ; https://www.walmart.com/ip/seort/252523104
31. Brita filtering bottles (retailers). 36 oz: https://www.staples.com/brita-plastic-filtered-water-bottle-36-oz-night-sky-36465/product_24640935 ; 20 oz: https://www.kohls.com/product/prd-5993245/brita-20-oz-stainless-steel-water-bottle-with-filter.jsp ; 26 oz: https://www.walmart.com/ip/Brita-Premium-Leak-Proof-Filtered-Water-Bottle-Blush-Pink-26-oz/621399176
32. Baird CS. How much water can a camel store in its hump? WTAMU, 2013 (200 L in three minutes). https://www.wtamu.edu/~cbaird/sq/2013/09/18/how-much-water-can-a-camel-store-in-its-hump/
33. Phys.org (2020), on Pontzer H et al., *R Soc Open Sci* 2020, doi:10.1098/rsos.201155 (427 L hot / 325 L cool; total turnover). https://phys.org/news/2020-12-elephants-highest-volume-daily-loss.html
34. National Park Service. Mississippi River Facts (600,000 cfs at New Orleans; Amazon 209,000 m³/s). https://nps.gov/miss/riverfacts.htm
35. San Diego Zoo Wildlife Alliance Library. Asian elephant diet (trunk about 2 gal). https://ielc.libguides.com/sdzg/factsheets/asianelephant/diet
36. Goldbogen JA et al. Mechanics, hydrodynamics and energetics of blue whale lunge feeding. *J Exp Biol* 2011;214:131, correction 214:698 (80 m³ per lunge). https://cob.silverchair.com/jeb/article-pdf/214/1/131/1435232/131.pdf ; https://cob.silverchair.com/jeb/article-pdf/214/4/698/1440891/698.pdf
37. Appliance Standards Awareness Project. Dishwashers (ENERGY STAR v7: 3.2 gal/cycle; federal 5.0). https://appliance-standards.org/product/dishwashers ; ENERGY STAR Most Efficient 2025 criteria: https://www.energystar.gov/sites/default/files/2024-09/Dishwasher%20ENERGY%20STAR%20Most%20Efficient%202025%20Criteria.pdf
38. EPA WaterSense. Statistics and Facts (82 gal per person per day at home). https://www.epa.gov/watersense/statistics-and-facts
39. Istituto Nazionale Espresso Italiano. Certified Italian Espresso (25 mL ± 2.5). https://www.nespressoguide.com/files/File/istituzionale_inei_hq_en.pdf
40. NIAAA. Rethinking Drinking: What is a standard drink? (archived; 5 oz wine, 1.5 oz spirits). https://webarchive.library.unt.edu/web/20201218103258/http://rethinkingdrinking.niaaa.nih.gov/
41. Dixie 43900 bath cups, 3 oz (retail listing). https://www.toolboxsupply.com/products/dixie-43900-everyday-disposable-bath-cup-3-oz-assorted-design-200-pack
42. Home Hardware. Water bottle, 5 gal / 18.9 L. https://www.homehardware.ca/en/pet-polyethylene-terephthalate-water-bottle-5-gal-189-l/p/3160091
43. NIST Office of Weights and Measures. Unit conversion (US fl oz, gallon, ft³). https://www.nist.gov/pml/owm/metric-si/unit-conversion
44. EPA WaterSense. Specification for Showerheads v1.1 (2.0 gpm). https://www.epa.gov/sites/production/files/2018-07/documents/ws-products-specification-showerheads-v1-1.pdf
45. EPA WaterSense. Flushometer-valve toilets support statement (federal 1.6 gpf). https://www.epa.gov/sites/production/files/2017-01/documents/ws-products-support-statement-fv-toilets.pdf
46. StatPearls. Physiology, Blood Volume. https://www.ncbi.nlm.nih.gov/books/NBK526077
47. USGS Water Science School. The Water in You. https://www.usgs.gov/water-science-school/science/water-you-water-and-human-body
48. National Academies (2004). Dietary Reference Intakes for Water (AI 2.7 / 3.7 L total water). https://www.nationalacademies.org/news/report-sets-dietary-intake-levels-for-water-salt-and-potassium-to-maintain-health-and-reduce-chronic-disease-risk
49. KegWorks. Guide to Beer Keg Sizes (15.5 gal). https://www.kegworks.com/blog/guide-to-beer-keg-sizes
50. U.S. EIA (archived). Units: 1 barrel = 42 US gal. https://webarchive.library.unt.edu/web/20120916015359/http://www.eia.gov/cfapps/ipdbproject/docs/unitswithpetro.cfm
51. U.S. DOE Energy Saver. Sizing a New Water Heater. https://www.energy.gov/energysaver/sizing-new-water-heater
52. Repackify. 55 Gallon Drum Dimensions. https://www.repackify.com/blog/55-gallon-drum-dimensions
53. Fire Apparatus Magazine. Larger pumps and water tanks on engines; NFPA 1901 300-gal minimum (original note's ref 45). https://fireapparatusmagazine.com/?p=127215
54. Chaney Enterprises. Evolution of concrete mixer trucks (up to 10 yd³). https://www.chaneyenterprises.com/the-evolution-of-concrete-mixer-trucks-from-2-yards-to-10
55. Fire Engineering. Gasoline Tanker Emergencies, Part 1. https://www.fireengineering.com/industrial-firefighting/gasoline-tanker-emergencies-part-1/
56. HomeGuide. Swimming Pool Size Chart. https://homeguide.com/articles/swimming-pool-size-chart
57. UFGS 33 16 15, Elevated welded steel water tanks (50,000 to 1,000,000 gal). https://legacy.wbdg.org/FFC/DOD/UFGS/UFGS%2033%2016%2015.pdf
58. Wikipedia. Olympic-size swimming pool (World Aquatics facilities rules). https://en.wikipedia.org/wiki/Olympic-size_swimming_pool
59. Niagara Parks. Niagara Falls Geology Facts & Figures. https://www.niagaraparks.com/visit-niagara-parks/plan-your-visit/niagara-falls-geology-facts-figures/
60. Las Vegas Sun (2012). Bellagio fountains (22 million gal). https://m.lasvegassun.com/news/2012/apr/30/bellagio-fountains-help-whet-appetite-learning-dur/
61. San Diego Zoo Wildlife Alliance Library. African elephant diet (150 to 200 L/day). https://ielc.libguides.com/sdzg/factsheets/african_elephant/diet
62. TTB. Wine labeling: net contents (750 mL standard of fill). https://www.ttb.gov/regulated-commodities/beverage-alcohol/wine/labeling-wine/wine-labeling-net-contents
63. McDonald's US. Coca-Cola (Large) page, nutrition note ("standard fill levels plus ice"). https://www.mcdonalds.com/us/en-us/product/coca-cola-large.html
64. Starbucks. Pike Place Roast page (Short 8, Tall 12, Grande 16, Venti 20 fl oz), accessed 2026-11-13. https://www.starbucks.com/menu/product/480/hot
65. Lawless HT et al. Gender, age, vessel size, cup vs. straw sipping, and sequence effects on sip volume. *Dysphagia*. 2003;18(3). https://www.springermedizin.de/gender-age-vessel-size-cup-vs-straw-sipping-and-sequence-effects/8524174
