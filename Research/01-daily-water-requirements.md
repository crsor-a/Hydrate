# Daily Water Requirements: a Personalized Drink Goal for Hydrate

*Research brief, compiled 2026-11-13. It covers reference intakes (NASEM/IOM 2004, EFSA 2010, WHO and newer work up to 2026), weight-based formulas, adjustments, the inputs the app can realistically get, safety bounds, and one recommended algorithm with worked examples. Drinks are covered in depth in `02-beverage-hydration-model.md` and platform limits in `05-platform-capabilities.md`.*

---

## TL;DR

**Use the 2022 doubly-labelled-water equation from Yamada et al. [4] as the personalized core. Adapt it in two ways, keep its add-ons for activity, heat and altitude, add pregnancy/lactation increments, convert to a drinks-only number, and clamp it with EFSA/ESPEN floors and a hard ceiling.**

Why this approach:
- It is the only large, objectively measured dataset of human water turnover: 5,604 people aged 8 days to 96 years in 26 countries, measured with isotope tracking.
- It uses exactly the inputs the app has: age, sex, weight, activity level, temperature, humidity and altitude.
- It sits between the two main authorities. NASEM [1] is higher because it is based on median US intake surveys. EFSA [3] is lower.

```
// All values in mL/day. Adults and teens aged 14 and over (see §6 for ages 4–13).
ageEff  = clamp(age, 14, 35)                 // Freeze at 35. Don't lower the goal for older adults (blunted thirst) [1][7]
wEff    = clamp(weightKg, 35, 150), and if BMI > 30 use the weight at BMI 30
sexC    = 1 male, 0 female, 0.5 unspecified
PAL     = 1.40 inactive | 1.60 low active | 1.75 active | 2.05 very active   // from steps or exercise minutes, §4

WT_base = 1076·PAL + 14.34·wEff + 374.9·sexC − 0.3529·ageEff² + 24.78·ageEff − 297.2
          // Yamada equation at reference conditions: 15 °C, 50 % RH, sea level, non-athlete, high-HDI country
drinks  = 0.68 · WT_base                     // 0.85 (intake share of turnover [4]) × 0.80 (drinks share; food ≈ 20 % [1])
        + climateAdd                         // 0.85 × Yamada temperature/humidity terms above 15 °C, cap +1000
        + altitudeAdd                        // 0.40 mL per metre above 1500 m, cap +500 (low confidence)
        + 300 if pregnant | 700 if lactating // EFSA increments [3]
        + workoutAdd                         // 400 mL/h moderate, 600 mL/h vigorous, +200 mL/h if ≥ 25 °C; cap +1500 [9][11]
goal    = clamp(drinks, floor, 4500)         // floor = 0.8 × EFSA AI: men 2000, women 1600, pregnant 1840, lactating 2160
goal    = round to nearest 50 mL (or 4 fl oz in US units), rounding only the final number
```

Worked results (§6):

| Person | Daily drink goal |
|---|---|
| 70 kg man, 30, active | **2,300 mL** |
| 58 kg woman, 65, sedentary | **1,700 mL** |
| 64 kg pregnant woman, 31 | **2,200 mL** (2,600 mL when breastfeeding) |
| 65 kg boy, 16, athlete | **2,400 mL** on a rest day, **4,000 mL** on a 90-min practice at 27 °C (hits the ceiling) |
| The 70 kg man on a 30 °C day with a 1 h workout | **3,750 mL** |

For comparison, the NASEM beverage reference is 3,000 mL for men and 2,200 mL for women. The EFSA-derived drink figure is about 2,000 mL for men and 1,600 mL for women.

Other recommendations:
- **Show a "talk to your doctor" gate** for heart failure, CKD stage 4–5/dialysis, cirrhosis, SIADH or prior hyponatremia, any prescribed fluid restriction, and kidney stones (stone formers usually need *more*).
- **Never prompt more than about 1 L in an hour.** The kidneys can clear only about 0.7–1.0 L/h [1].

---

## 1. Authoritative reference values

### 1.1 US: NASEM (formerly IOM), 2004 Adequate Intakes [1][2]

- **Type of value:** Adequate Intakes (AIs), not requirements. The panel could not set an Estimated Average Requirement, so it set each AI at the **median total water intake** in NHANES III [1].
- **Definition:** total water = drinking water + other beverages + water in food [1].
- **Upper limit:** none set [1].
- **Assumed conditions:** the AIs are meant for generally healthy people in temperate climates. People who are very active or in hot weather may need more [2].
- **Not revisited since:** the 2019 NASEM update covered only sodium and potassium [39].

**Table 1. NASEM AIs (L/day)** [1]

| Life stage | Total water AI | From beverages incl. drinking water | Implied from food |
|---|---|---|---|
| Infants 0–6 mo | 0.7 (assumed from human milk) | — | — |
| Infants 7–12 mo | 0.8 | ≈0.6 (milk/formula, juice, water) | ≈0.2 |
| Children 1–3 y | 1.3 | ≈0.9 | ≈0.4 |
| Children 4–8 y | 1.7 | ≈1.2 | ≈0.5 |
| Boys 9–13 y | 2.4 | ≈1.8 | ≈0.6 |
| Girls 9–13 y | 2.1 | ≈1.6 | ≈0.5 |
| Boys 14–18 y | 3.3 | ≈2.6 | ≈0.7 |
| Girls 14–18 y | 2.3 | ≈1.8 | ≈0.5 |
| Men 19 y and over (incl. 51–70 and >70) | 3.7 | ≈3.0 | ≈0.7 |
| Women 19 y and over (incl. 51–70 and >70) | 2.7 | ≈2.2 | ≈0.5 |
| Pregnancy 14–50 y | 3.0 | ≈2.3 | ≈0.7 |
| Lactation 14–50 y | 3.8 | ≈3.1 | ≈0.7 |

- **Food share:** about 19–20% of total water in the US survey data. It was about 22% in pregnancy and 19% in lactation [1].
- **Older adults:** the report deliberately set the AI for people over 50 equal to the young-adult value rather than the lower intakes actually seen in older people. Thirst is blunted with age, so observed intake was judged an unreliable guide [1].

### 1.2 Europe: EFSA, 2010 Dietary Reference Values for water [3]

- **Method:** AIs derived from observed intakes, a desirable urine osmolality, and desirable water volumes per energy unit consumed.
- **Assumptions:** moderate environmental temperature and moderate physical activity (PAL about 1.6).
- **Values:**
  - Ages 1–2: 1.1–1.2 L/day (interpolated)
  - Ages 2–3: 1.3 L
  - Ages 4–8: 1.6 L
  - Ages 9–13: boys 2.1 L, girls 1.9 L
  - **Ages 14 and over: treated as adults**
- **Adults, including the elderly:** women **2.0 L/day**, men **2.5 L/day** total water. The 95th-percentile intakes were 3.1 L and 4.0 L.
- **Pregnancy:** the non-pregnant AI plus **300 mL/day**, in proportion to the higher energy intake.
- **Lactation:** about **700 mL/day** above the non-lactating AI.
- **Food share:** these are total water values. With roughly 20% from food, the drink equivalents are about 1.6 L (women) and 2.0 L (men). That matches ESPEN's geriatric drink recommendation exactly [7][37].

### 1.3 WHO

- **No nutrient-style recommendation:** WHO has never published a water DRI or AI.
- **Drinking-water quality guidelines:** for deriving chemical guideline values, WHO assumes a **60 kg adult drinking 2 L/day** [33]. This is an exposure-modelling convention, not an intake recommendation.
- **Domestic water quantity report:** the 2003 edition (2nd edition 2020) proposed about **7.5 L per person per day** for drinking plus food preparation. This was based on lactating women doing moderate activity in above-average temperatures [34]. It is a water-supply planning figure, not a personal drinking goal.

### 1.4 Newer guidance and evidence (2015–2026)

- **Yamada et al., *Science* 2022 [4]:** water turnover (WT) measured by deuterium elimination in 5,604 people.
  - **Predictors:** age, fat-free mass/weight, sex, PAL, athletic status, pregnancy, country HDI, temperature, humidity, altitude and latitude.
  - **Equation:** published, and explains 47% of the variance.
  - **Effect sizes** (all else equal):
    - PAL +1.0 → about +1,000 mL WT
    - +50 kg body weight → about +700 mL
    - +50% relative humidity → about +300 mL
    - +1,000 m altitude → about +500 mL
    - Men → about +400 mL vs women
    - Athletes → about +1,000 mL
    - Low-HDI countries → about +200 mL
  - **Temperature:** U-shaped. Turnover is about 1,000 mL higher at a mean air temperature of 30 °C than at the 0–10 °C low point.
  - **Age:** turnover peaks between the 20s and 40s. It is about 700 mL lower at age 80 than at 30.
  - **Pregnancy and lactation:** in 63 women measured repeatedly, WT rose about **670 mL/day in the third trimester** and about **260 mL/day during lactation**, compared with before pregnancy.
  - **Worked example from the paper:** a 20-year-old non-athletic man, 70 kg, PAL 1.75, temperate (10 °C, 50% RH), sea level → **3.2 L/day**. A 60 kg woman in the same setting → **2.7 L/day**.
  - **Turnover is not intake:** metabolic water is about 10% of WT, and respiratory plus skin uptake about 2–3% each. Water intake from food and drink is therefore **about 85% of WT**.
  - **Food share in this paper:** self-reported estimates of the food share range from 20% to 50%. The authors call these questionable.
  - **On "8 glasses":** the authors state it has no objective evidence behind it.
- **Armstrong & Johnson, *Nutrients* 2018 [5]:**
  - **AVP marker:** plasma arginine vasopressin (AVP, the antidiuretic hormone) is proposed as an individual marker of whether someone is drinking enough. A mild hormonal water-conserving response starts when total water intake falls **below about 1.8 L/day**.
  - **Prevalence:** 19–71% of adults in various countries drink less than this.
  - **Implication:** this supports a floor of roughly 1.5 L of drinks (1.8 L total) for adults.
- **ESPEN geriatrics guideline 2019 (practical version 2022) [7][8]:** offer older women **at least 1.6 L** and older men **at least 2.0 L of drinks** per day, unless a clinical condition requires otherwise. The recommendation is grade B. Sources disagree on whether these figures include water from food. A PMC review notes they equal EFSA's values minus about 20% for food [37].
- **Other countries:**
  - **Germany (DGE):** about 35 mL/kg total water for adults up to about 50 and 30 mL/kg for older adults, with about 1.5 L/day from drinks [22]. Confidence is medium because this was verified only through secondary sources.
  - **Australia/New Zealand (NHMRC 2006) and China (2023 DRIs):** both publish water AIs. I could not read the primary tables, so their numbers are not used here.

**Bottom line:** the authorities differ by about 1 L for men.
- NASEM total 3.7 L = about 3.0 L drinks.
- EFSA total 2.5 L = about 2.0 L drinks.
- Yamada-based estimate for a 70 kg active 30-year-old = about 2.3 L drinks.

All of these are **population descriptors of adequate intake**, not proven requirements [5]. That is why the app should present its goal as a guide, not a prescription.

---

## 2. Weight-based formulas

| Formula | Origin | What it was built for | Evidence quality |
|---|---|---|---|
| **Holliday–Segar** (100 mL/kg for the first 10 kg + 50 mL/kg for the next 10 kg + 20 mL/kg beyond; hourly "4-2-1") | Holliday & Segar, *Pediatrics* 1957 [18] | **IV maintenance in hospitalized children.** Based on estimated energy expenditure of about 100 mL per 100 kcal [18][40] | Physiological estimate, not validated as an oral drinking target. Hypotonic IV fluids given this way have been linked to hospital-acquired hyponatremia. The AAP 2018 guideline now recommends isotonic maintenance fluids [19] |
| **30–35 mL/kg/day** | Clinical nutrition convention. DGE uses 35 mL/kg (adults under about 51) and 30 mL/kg (older) as **total** water [22] | Quick bedside or dietetic estimate | Low. The origin is convention, not trials. Applied to institutionalized elderly, 30 mL/kg gave unrealistically low targets for underweight residents [21] |
| **NICE CG174:** 25–30 mL/kg/day; 20–25 mL/kg for older/frail people or those with renal/cardiac disease | NICE 2013 (updated 2017) [20] | **IV maintenance in hospitalized adults** | Guideline consensus. NICE notes that giving more than 2.5 L/day IV raises hyponatremia risk [20] |
| **1 mL/kcal** (1.0–1.5 mL/kcal) | US RDA 1989, as summarized in [12] | Links water to energy turnover | Moderate as a physiological link. Yamada found WT averages about 1.4 mL/kcal of total energy expenditure [4] |
| **Yamada WT equation** | 2022, 5,604 doubly-labelled-water measurements [4] | Free-living total water turnover | Best available objective data. Explains 47% of variance, describes turnover rather than "need", and is cross-sectional |

**Limits at extremes.** Compare a linear mL/kg rule with the Yamada weight slope of 14.34 mL WT per kg (about 10 mL of drinks per kg):

| Weight | 30 mL/kg | 35 mL/kg | Holliday–Segar extended to adults | Yamada-based goal (adult, low active, temperate) |
|---|---|---|---|---|
| 45 kg (woman, 155 cm) | 1,350 | 1,575 | 2,000 | 1,700 |
| 58 kg | 1,740 | 2,030 | 2,260 | ≈1,800–1,850 (woman) |
| 70 kg | 2,100 | 2,450 | 2,500 | ≈2,200–2,300 (man) |
| 120 kg (man, 175 cm, BMI 39) | 3,600 | 4,200 | 3,500 | 2,250 with the BMI-30 cap; 2,550 without |

- **Light people:** linear rules under-prescribe [21].
- **Heavy people:** linear rules over-prescribe. Adipose tissue holds little water, and fat-free mass, not total weight, drives turnover. When fat-free mass is in Yamada's model, sex drops out as a predictor [4].
- **Recommendation:** don't use a pure mL/kg rule. Use the gentle Yamada slope, and cap the weight term at BMI 30 when height is known. The BMI-30 cap is a judgment call (§9).

---

## 3. Adjustments

### 3.1 Activity and exercise

- **Sweat rates:**
  - Athletes typically lose about **0.5–2.0 L/h** of sweat, occasionally more than 3 L/h [10].
  - Distance runners in temperate conditions average about 0.7 L/h (women) and 1.0 L/h (men). Competitive men in heat lose 1.0 to more than 2.0 L/h [1].
  - Occupational work in hot climates: 0.3–1.2 L/h. Light work in protective clothing in heat: 1–2 L/h [1].
- **ACSM 2007 position stand [9]:**
  - Drink during exercise to prevent losses **greater than 2% of body weight** and large electrolyte shifts.
  - Customize intake, because sweat rates vary widely. Estimate sweat rate from body weight before and after exercise.
  - Prehydrate about **5–7 mL/kg** at least 4 h before exercise (via secondary sources [11]).
  - After exercise, replace the deficit, about **150%** of the fluid lost if recovery must be fast.
  - Both the stand and the International Marathon Medical Directors Association are reported to suggest **0.4–0.8 L/h** as a typical starting range during endurance exercise [11]. The full text was paywalled, so this figure comes via Armstrong 2021. Confidence: medium.
- **Practical examples:** a 1 h workout ≈ 1 L sweat; an acclimated triathlete ≈ 1.5 L/h [12].
- **Daily totals:** active adults often need more than 3–4 L/day, sometimes more than 10 L [12]. NASEM cites modelled daily needs of about 2–4 L in cool climates and up to about 15 L in very hot climates, depending on activity [1].
- **Habitual activity in the DLW data:** PAL +1.0 adds only about 1 L/day of turnover, and athletes add another 1 L [4]. Averaged over weeks, habitual activity raises water turnover less than per-hour sweat figures suggest.
- **App consequences:**
  - Use a modest daily tier term (Yamada PAL coefficient) for habitual activity.
  - Add a same-day workout bonus at the low-to-middle end of the ACSM range (400–600 mL/h, +200 mL/h when hot).
  - Never aim to replace 100% of sweat. Overdrinking during exercise is the main cause of exercise-associated hyponatremia [13].

### 3.2 Hot or humid climates, cold, and altitude

- **Heat:**
  - Requirements can double or triple in very hot weather (about 40 °C). Active people in continuous heat may need 6–8 L/day or more [1].
  - NIOSH advises **1 cup (about 240 mL) every 15–20 minutes** during moderate work in heat, which is 0.7–0.95 L/h. It sets a ceiling of **48 oz (about 1.4 L) per hour** [15].
  - US Army guidance (TB MED 507 materials) limits intake to about **1–1.5 qt/h (0.95–1.4 L/h)** and **12 qt/day (about 11.4 L)** [17].
- **Yamada temperature term [4]:** WT += 1.865·T² − 19.66·T, where T is the mean daily air temperature in °C. Relative to 15 °C this adds:

  | Mean temperature | Extra WT (mL/day) |
  |---|---|
  | 20 °C | +227 |
  | 25 °C | +550 |
  | 30 °C | +964 |

  Cold also raises WT (about +400 mL at −10 °C vs the low point), through respiratory loss and cold-induced diuresis.
- **Humidity [4]:** WT += 5.823 mL per % RH (about +300 mL per +50% RH).
- **Altitude:**
  - Respiratory water loss rises and early acclimatization brings a diuresis. Altitude estimates of insensible loss are extrapolated from sea-level data [36].
  - Yamada: about +500 mL WT per 1,000 m [4]. This comes from mostly long-term residents and may partly reflect lifestyle.
  - Wilderness Medical Society guidance: forced overhydration does not prevent acute mountain sickness [38].
  - Consumer figures of "+1–1.5 L/day above 2,500 m" trace to apps, not guidelines.
  - **Confidence: Low.**
- **Platform note:** WeatherKit is **not available on a free Personal Team** (`05-platform-capabilities.md`). Weather therefore has to come from one of these:
  - a manual "Hot day" / "Very hot day" toggle, mapped to mean 25 °C / 30 °C
  - a user-chosen home-climate setting
  - a free keyless web API (e.g. Open-Meteo). This needs no entitlement but sends approximate location to a third party, so it must be opt-in.

### 3.3 Age

- **Older adults:** the thirst threshold is much higher. Many healthy elderly people didn't feel thirsty even with plasma osmolality above 300 mOsm/kg. Kidney concentrating ability also declines. Stroke, dementia and systemic illness lower thirst further [1].
  - NASEM therefore set the over-50 AI at young-adult intake [1].
  - ESPEN says every older person should be considered at risk of low-intake dehydration and offered at least 1.6 L (women) / 2.0 L (men) of drinks [7][8].
  - Yamada shows turnover *falls* with age (about −700 mL at 80 vs 30) [4]. That is what older people *do*, not necessarily what they *need*.
  - **Recommendation:** freeze the age term at its peak, which the equation reaches at about 35 years.
- **Children:**
  - Children sweat less than adults in similar conditions, and the difference appears around mid-puberty [1].
  - NASEM gives beverage AIs for ages 1–13 (Table 1).
  - For junior sport, one review suggests about **13 mL/kg per hour** during exercise as a conservative intake [41].

### 3.4 Pregnancy and lactation

| Source | Pregnancy | Lactation |
|---|---|---|
| NASEM [1] | Total +0.3 L (2.7 → 3.0); beverages +0.1 L (2.2 → 2.3) | Total +1.1 L (→ 3.8); beverages +0.9 L (→ 3.1) |
| EFSA [3] | +300 mL total | +700 mL total |
| Yamada [4] (measured WT) | +670 mL in the third trimester | +260 mL |

- **Pregnancy physiology:** total body water rises by about 6–9 L. Plasma osmolality falls by 8–10 mOsm/kg because the thresholds for thirst and vasopressin reset. NASEM does not interpret this as dehydration [1].
- **Recommendation:** add **+300 mL** (pregnant) and **+700 mL** (lactating) to drinks, following EFSA. These sit mid-range of the three sources.
- **HealthKit flags:** cycle-tracking factors can flag pregnancy or lactation, but the user should confirm.

### 3.5 Illness (keep general)

- **Fever, vomiting and diarrhea** all increase water and electrolyte losses.
- **Fever rule of thumb:** clinical teaching material adds about **10% per °C above 38 °C** to replacement of losses through the skin; some sources say 10–15% per °C above 37 °C [35]. These are pediatric and inpatient rules of thumb. **Confidence: Low.**
- **Recommendation:** don't auto-adjust the goal for illness. Offer a "Feeling unwell" card that suggests:
  - small, frequent drinks
  - oral rehydration solution for vomiting or diarrhea
  - red flags that need care: no urine for 8+ hours, confusion, inability to keep fluids down, bloody diarrhea, infants or frail elderly people
- **When to hide the card:** suppress it when the user has a fluid-restriction condition (§5.4).

### 3.6 Caffeine and alcohol (pointer only)

- **Caffeine:**
  - NASEM concluded that caffeinated drinks contribute to daily water like other drinks. Any diuretic effect is transient [2].
  - In habitual coffee drinkers, 4 × 200 mL coffee (4 mg/kg caffeine) hydrated as well as water over 3 days [28].
- **Alcohol and the Beverage Hydration Index:** alcohol is diuretic, especially stronger drinks. The Beverage Hydration Index ranks drinks by short-term fluid retention [29].
- **App handling:** none of this changes the *goal*. It changes how much each logged drink is *credited* (see `02-beverage-hydration-model.md`).

---

## 4. Inputs the app can realistically get

| Input | Source | Notes |
|---|---|---|
| Age (date of birth) | HealthKit characteristic or manual entry | Recompute on birthday |
| Sex | HealthKit biological sex or manual entry | Offer "prefer not to say" → coefficient 0.5 (judgment) |
| Weight | HealthKit `bodyMass` (latest), or manual | Use a 7-day median to smooth scale noise |
| Height | HealthKit `height`, or manual | Optional. Enables the BMI-30 weight cap |
| Activity tier | HealthKit `stepCount`, `appleExerciseTime`, `activeEnergyBurned` | See below |
| Today's workouts | HealthKit workouts (duration, activity type) | Moderate vs vigorous: 3.0–5.9 METs vs ≥6 METs [25] |
| Pregnancy / lactation | Manual toggle; HealthKit cycle-tracking factors if present | Ask for confirmation |
| Weather | Manual toggle / home climate / opt-in web API | WeatherKit unavailable on a free team |
| Elevation | CoreLocation altitude, or manual | Only matters above 1,500 m |
| Medical flags | Onboarding question | Drives the "talk to your doctor" gate (§5.4) |

### Activity tier thresholds

**Primary input: steps, as a 14-day rolling mean of daily totals.** Use the Tudor-Locke & Bassett indices for healthy adults [23], mapped onto the four NASEM 2023 PAL categories [24]:

| Tier | Steps/day [23] | NASEM 2023 PAL range [24] | PAL value used (NASEM illustrative) [24] |
|---|---|---|---|
| Inactive | < 5,000 (sedentary lifestyle index) | 1.0 ≤ PAL < 1.53 | 1.40 |
| Low active | 5,000–7,499 (typical daily life without exercise) | 1.53–1.68 | 1.60 |
| Active | 7,500–12,499 (somewhat active plus active) | 1.68–1.85 | 1.75 |
| Very active | ≥ 12,500 (highly active) | 1.85–2.50 | 2.05 |

- **Status of the mapping:** the step-to-PAL link is a **judgment that connects two literatures**. It is not a validated conversion. NASEM itself says its PAL categories do not correspond to the physical activity guidelines [24].
- **Fallback 1: weekly exercise minutes** (`appleExerciseTime`, last 7 days), using WHO 2020 activity bands [25]:

  | Minutes per week | Tier |
  |---|---|
  | < 60 | inactive |
  | 60–149 | low active |
  | 150–299 | active (meets guidelines) |
  | ≥ 300 | very active |

  Count vigorous minutes double if the app can classify them.
- **Fallback 2: active energy.**
  - Formula: PAL ≈ (1 + AEE/BMR) / 0.9, with BMR from Mifflin–St Jeor [27] and thermic effect of food about 10% of total energy.
  - **Not recommended as primary.** Wrist devices showed no energy-expenditure error below 20% [26]. In practice, Apple "active energy" values are much lower than doubly-labelled-water activity energy, so most users would be classed as inactive.
- **Last resort:** self-report.
- **Stability:** recompute the tier at most once a week (e.g. Monday morning, from the previous 14 days) and require a full threshold crossing. Otherwise the chart line flickers.
- **Wheelchair users:** steps are not meaningful. Use exercise minutes ("push" workouts) or self-report.

---

## 5. Safety bounds

### 5.1 Upper intakes

- **No UL:** neither NASEM nor EFSA set a Tolerable Upper Intake Level for water. Healthy kidneys excrete excess water [1][3].
- **Observed high intakes:** the 99th percentile of US intake was 8.1 L/day in men aged 31–50, and 5% of men exceeded 6.4 L/day. No chronic harm was reported in healthy people when intake roughly matched losses [1].
- **Acute limits:** the kidneys' maximal excretion rate is about **0.7–1.0 L/h**. Acute water toxicity has been reported when rapid intake greatly exceeded this [1]. Gastric emptying limits useful replacement to about 1.0–1.5 L/h [1].
- **Occupational ceilings:** **≤ 1.4–1.5 L/h** (NIOSH/OSHA) [15][16]. US Army materials suggest 12 qt (about 11.4 L) per day as an absolute ceiling under heavy heat stress [17].

### 5.2 Hyponatremia from overdrinking

- **Definition and symptoms:** serum sodium below 135 mmol/L. Symptoms usually appear only below about 130 mmol/L. Severe cases cause cerebral edema, with headache, vomiting, confusion, seizures and death [1][13].
- **Who is at risk:**
  - very rare in healthy people eating a normal diet [1]
  - endurance events
  - people following "drink ahead of thirst" or "drink until urine is clear" advice
  - psychiatric polydipsia
  - water-drinking contests
  - infants given plain water [1][2][13]
- **Boston Marathon 2002 [14]:** 13% of finishers had sodium ≤135 mmol/L and 0.6% had ≤120 mmol/L.
  - **Independent predictors:** weight gain during the race (odds ratio 4.2), finishing time over 4 h, and BMI extremes.
  - **Univariate only:** drinking more than 3 L during the race and drinking at every mile were associated, but did not survive adjustment.
  - **Mechanism:** sustained drinking faster than sweat loss.
- **2015 consensus [13]:**
  - Drink palatable fluids **when thirsty** before, during and after exercise.
  - Don't follow fixed schedules or "drink as much as possible" advice.
  - Overdrinking relative to sweat loss, plus non-osmotic vasopressin keeping the body from excreting it, is the main cause.
- **App rules:**
  1. Never schedule or suggest more than **1.0 L in any 60-minute window**. Spread reminders across waking hours.
  2. Never send a "catch up" nudge late in the day that asks for more than about 750 mL at once.
  3. Show a gentle warning if logged intake exceeds about 1.5 L in 1 h or 6 L in a day. Also warn if the user is far above goal and sweat losses are low (no workout, not hot).
  4. Workout guidance should say "drink to thirst; don't gain weight during exercise", not "replace every drop".

### 5.3 Recommended clamp for the computed goal

| Group | Floor (mL drinks) | Ceiling (mL drinks) | Rationale |
|---|---|---|---|
| Women 14 y and over | 1,600 | 4,500 | Floor = 0.8 × EFSA 2.0 L = ESPEN geriatric minimum [3][7]. It is above the AVP-defense threshold (about 1.8 L total ≈ 1.45 L drinks) [5] |
| Men 14 y and over | 2,000 | 4,500 | 0.8 × EFSA 2.5 L = ESPEN [3][7] |
| Sex unspecified | 1,800 | 4,500 | Midpoint (judgment) |
| Pregnant | 1,840 | 4,500 | 0.8 × (2.0 + 0.3) L [3] |
| Lactating | 2,160 | 4,500 | 0.8 × (2.0 + 0.7) L [3] |
| Teens 14–17 | as above | 4,000 | Smaller bodies; judgment |
| Children 9–13 | NASEM beverage AI (girls 1,600 / boys 1,800) | 3,000 | [1]; ceiling is judgment |
| Children 4–8 | 1,200 | 2,500 | [1]; ceiling is judgment |
| Under 4 | **not supported** | — | Milk/formula-based. Pediatric guidance only |

- **Why 4,500 mL:** the 4.5 L ceiling is a **product safety choice**, not a physiological maximum.
  - It is below the 95th-percentile *total* intake of US men (6.4 L) [1].
  - It is a little above EFSA's 95th percentile for men (4.0 L total) [3].
  - Days needing more (long work in heat, ultra-endurance) should rely on thirst plus explicit coaching rather than a bigger number.
- **Manual override:** allow 1,000–6,000 mL, and show a confirmation note above 4,500 mL.

### 5.4 "Talk to your doctor" conditions

At onboarding, ask: *"Has a clinician told you to limit fluids, or do you have any of these?"* If yes, show the computed goal as **"suggested, check with your clinician"**. Let the user set their own target, and switch off auto add-ons (heat, workouts, illness card).

| Condition | Why it matters |
|---|---|
| **Heart failure** | The ESC now considers fluid restriction of **1.5–2 L/day only in selected patients**, e.g. with hyponatremia or congestion that is hard to control. It also recommends salt ≤5 g/day [30] |
| **Chronic kidney disease (stage 4–5) / dialysis** | Fluid limits are usually set individually. In stage 3 CKD, coaching people to drink about 0.6 L/day more did **not** slow eGFR decline over 1 year [31]. "More is better" is not established |
| **Cirrhosis with ascites; SIADH; prior hyponatremia** | Water excretion is impaired, so the goal may need to be much lower (general clinical knowledge; no specific source read for this note) |
| **Any prescribed fluid restriction**, e.g. after surgery | Clinician target overrides |
| **Kidney stones** | Opposite direction: the AUA recommends fluid enough for **≥ 2.5 L of urine/day**, which usually means about 3 L+ of intake [32]. Offer a "stone prevention" mode |
| **Medicines affecting water balance**, e.g. diuretics, lithium, SGLT2 inhibitors, desmopressin | Ask a clinician or pharmacist. General caution, no source read |
| **Pregnancy with hyperemesis; eating disorders; psychiatric polydipsia** | Specialist guidance |

---

## 6. Recommended algorithm

### 6.1 Design choices (and why)

1. **Core = Yamada 2022 water-turnover equation [4].** It is measured rather than surveyed, and it is personalized by exactly the app's inputs.
   - The equation (mL/day) is:

     `WT = 1076·PAL + 14.34·BM + 374.9·sex + 5.823·RH + 1070·athlete + 104.6·HDI + 0.4726·altitude − 0.3529·age² + 24.78·age + 1.865·T² − 19.66·T − 713.1`

     - BM = body mass (kg)
     - sex: 1 = male, 0 = female
     - RH = relative humidity (%)
     - athlete: 0 or 1
     - HDI: 0 high, 1 middle, 2 low
     - altitude in metres
     - T = mean air temperature (°C)
   - **How the coefficients were verified:** the PMC text I read omitted the typeset equation. I checked the coefficients above by reproducing all of the paper's worked examples exactly: 3,184 → "3.2 L", 2,666 → "2.7 L", 7,338 → "7.3 L" and 6,820 → "6.8 L/d".
   - **Fixed reference values in the app:** athlete = 0 (use the workout bonus instead) and HDI = 0.
2. **Turnover → total intake (×0.85) → drinks (×0.80).** The 85% comes from Yamada's own breakdown [4], and 80% from NASEM's survey food share [1]. Food share is the most uncertain constant (20–50% in some diets) [4].
3. **Freeze age at 35.** That is the peak of the equation's age curve. Older adults keep the young-adult value, as in the NASEM and ESPEN reasoning [1][7].
4. **Weight term with a BMI-30 cap.** This keeps obese users from getting inflated goals, because water turnover tracks fat-free mass [4].
5. **Add-ons follow Yamada's coefficients** for climate and altitude, EFSA for pregnancy/lactation, and the ACSM range for workouts.
6. **Clamp:** floors at 0.8 × EFSA (= ESPEN), ceiling 4.5 L. Round once, at the end.
7. **Two numbers:**
   - **Base goal:** profile only. This is what the long-term chart shows.
   - **Today's goal:** base + weather + workouts. This drives the progress ring.

### 6.2 Pseudocode (Swift-flavoured)

```swift
enum ActivityTier: Double { case inactive = 1.40, lowActive = 1.60, active = 1.75, veryActive = 2.05 }
enum Repro { case none, pregnant, lactating }
enum Intensity { case moderate, vigorous }            // vigorous ≈ ≥ 6 METs

struct Profile {
    var ageYears: Double
    var sex: Sex                                      // .male, .female, .unspecified
    var weightKg: Double                              // 7-day median
    var heightCm: Double?
    var tier: ActivityTier                            // weekly, from 14-day step mean (§4)
    var repro: Repro
    var elevationM: Double = 0
    var fluidRestricted: Bool                         // §5.4 gate
}
struct DayContext { var meanTempC: Double?; var meanRH: Double?; var workouts: [(minutes: Double, intensity: Intensity)] }

func yamadaTemp(_ t: Double) -> Double { 1.865*t*t - 19.66*t }   // [4]

func baseGoal(_ p: Profile) -> Double {               // unrounded mL; profile only
    if p.ageYears < 4 { return .nan }                 // unsupported
    if p.ageYears < 14 { return childBase(p) }        // §6.3
    let sexC = p.sex == .male ? 1.0 : (p.sex == .female ? 0.0 : 0.5)
    let ageEff = min(max(p.ageYears, 14), 35)
    var w = p.weightKg
    if let h = p.heightCm { let cap = 30 * pow(h/100, 2); if w > cap { w = cap } }
    w = min(max(w, 35), 150)
    // Yamada at reference conditions (15 °C, 50 % RH, 0 m, non-athlete, high HDI):
    // 5.823*50 + yamadaTemp(15) − 713.1 = −297.2
    let wt = 1076*p.tier.rawValue + 14.34*w + 374.9*sexC - 0.3529*ageEff*ageEff + 24.78*ageEff - 297.2
    var drinks = 0.85 * 0.80 * wt
    switch p.repro { case .pregnant: drinks += 300; case .lactating: drinks += 700; case .none: break }   // [3]
    drinks += min(500, 0.85 * 0.4726 * max(0, p.elevationM - 1500))                                     // [4], low confidence
    return drinks
}

func todayGoal(_ p: Profile, _ d: DayContext) -> Int {
    var g = baseGoal(p)
    if !p.fluidRestricted {
        if let t = d.meanTempC {                                         // climate, [4]
            var dWT = max(0, yamadaTemp(t) - yamadaTemp(15))
            if t >= 20, let rh = d.meanRH { dWT += 5.823 * max(0, rh - 50) }
            g += min(1000, 0.85 * dWT)                                   // extra intake all comes from drinks
        }
        var wk = 0.0                                                     // workouts, [9][11]
        for w in d.workouts where w.minutes >= 20 {
            var rate = (w.intensity == .vigorous) ? 600.0 : 400.0        // mL per hour
            if let t = d.meanTempC, t >= 25 { rate += 200 }
            wk += w.minutes / 60 * rate
        }
        g += min(1500, wk)
    }
    let floor: Double = {
        switch p.repro { case .pregnant: return 1840; case .lactating: return 2160; case .none: break }
        return p.sex == .male ? 2000 : (p.sex == .female ? 1600 : 1800)
    }()
    let ceiling: Double = p.ageYears >= 18 ? 4500 : 4000
    g = min(max(g, floor), ceiling)
    return Int((g / 50).rounded()) * 50                                  // round once, at the end
}
```

### 6.3 Children 4–13 (simpler "table mode")

- **Base:** NASEM beverage AI [1]:
  - ages 4–8: 1,200 mL
  - girls 9–13: 1,600 mL
  - boys 9–13: 1,800 mL
- **Adjustments:**
  - No PAL or weight term.
  - Workout add-on of 13 mL/kg/h [41].
  - Climate add-on scaled by weight/70 (judgment).
- **Ceilings:** 2,500 mL (ages 4–8) and 3,000 mL (ages 9–13).
- **Parental confirmation:** require it.

### 6.4 Rounding and units

- **Calculation:** compute in floating-point mL throughout.
- **Rounding:** round **only the final goal**, half-up:
  - to the nearest **50 mL** in metric
  - to the nearest **4 fl oz** (half a cup) in US units, converted from the unrounded mL
- **Display:** never compound rounding by summing rounded parts. Show the breakdown (base + heat + workout) with each part rounded to 50 mL for display only.

### 6.5 Worked examples (temperate means no weather input or mean temperature ≤ 15 °C; sea level)

**Example 1: man, 30, 70 kg, 178 cm, active (about 10,000 steps/day)**
- WT = 1076·1.75 + 14.34·70 + 374.9 − 0.3529·900 + 24.78·30 − 297.2
- = 1,883.0 + 1,003.8 + 374.9 − 317.6 + 743.4 − 297.2 = **3,390 mL**
- Drinks = 0.68 × 3,390 = 2,305 mL. That is above the 2,000 floor.
- **Goal 2,300 mL.** For comparison: NASEM beverages 3,000 and EFSA-derived 2,000.

**Example 2: woman, 65, 58 kg, 160 cm, sedentary (< 5,000 steps)**
- ageEff = 35.
- WT = 1076·1.40 + 14.34·58 + 0 − 0.3529·1225 + 24.78·35 − 297.2
- = 1,506.4 + 831.7 − 432.3 + 867.3 − 297.2 = **2,476 mL**
- Drinks = 0.68 × 2,476 = 1,684 mL. That is above the 1,600 ESPEN floor.
- **Goal 1,700 mL.**
- Without the age freeze, the raw equation would give about 1,470 mL, below ESPEN. That is why the freeze exists.

**Example 3: pregnant woman, 31, 64 kg pre-pregnancy, 168 cm, low active**
- WT = 1076·1.60 + 14.34·64 − 0.3529·961 + 24.78·31 − 297.2
- = 1,721.6 + 917.8 − 339.1 + 768.2 − 297.2 = **2,771 mL**
- Drinks = 1,884 + 300 (pregnancy) = 2,184 mL.
- **Goal 2,200 mL** (NASEM pregnancy beverages: 2,300).
- On a 22 °C, 60% RH day, add 0.85 × (352.7 − 124.7 + 58.2) = +343 → **2,550 mL**.
- Breastfeeding instead: 1,884 + 700 = 2,584 → **2,600 mL** (NASEM: 3,100).

**Example 4: boy, 16, 65 kg, 178 cm, athlete, very active (≥ 12,500 steps)**
- WT = 1076·2.05 + 14.34·65 + 374.9 − 0.3529·256 + 24.78·16 − 297.2
- = 2,205.8 + 932.1 + 374.9 − 90.3 + 396.5 − 297.2 = **3,522 mL**
- Drinks = 2,395 mL → **rest-day goal 2,400 mL** (NASEM boys 14–18 beverages: 2,600).
- Practice day: 90 min vigorous at a 27 °C mean, 55% RH.
  - Climate: 0.85 × (1,359.4 − 530.8 − 124.7 + 29.1) = +623 mL
  - Workout: 1.5 h × (600 + 200) = +1,200 mL
  - Raw total = 4,218 mL → clamped to the teen ceiling, **4,000 mL**
- Show a note: "Drink to thirst during practice; weigh before and after to learn your sweat rate."

**Example 5: Example 1's man on a hot day (mean 30 °C, 60% RH) with a 60-minute moderate workout**
- Climate: 0.85 × (1,088.7 − 124.7 + 58.2) = +869 mL
- Workout: 1 h × (400 + 200) = +600 mL
- Total: 2,305 + 869 + 600 = 3,774 mL → **3,750 mL**

**Sensitivity of the base goal** (age 40, low active, temperate):
- Weight: each +10 kg adds about **+100 mL**.
  - Men: 50 kg → 2,000; 70 kg → 2,200; 100 kg → 2,500.
  - Women: 60 kg → 1,850; 80 kg → 2,050.
- Activity tier, man 75 kg: inactive 2,100 → very active 2,600. Woman 62 kg: 1,700 → 2,200.
- Mean temperature, man 75 kg, 50% RH: 15 °C → 2,250; 20 °C → 2,450; 25 °C → 2,700; 30 °C → 3,050; capped at +1,000 mL from about 32 °C.

---

## 7. How the goal changes over time (for the chart)

- **Age:**
  - From 14 to 35 the age term rises slowly: about +100 mL of turnover from 18 to 35, which is +50 to +70 mL of drinks. The goal goes from 2,200 → 2,250 (man, 75 kg) and 1,800 → 1,850 (woman, 60 kg).
  - **After 35 the goal does not fall with age**, by design (§3.3).
  - The raw Yamada curve would drop about 700 mL of turnover by age 80 [4]. Show this in an info sheet, not in the goal.
- **Weight:** about **+9.75 mL of drinks per kg** (0.68 × 14.34), roughly +100 mL per 10 kg. Above BMI 30 (when height is known) the goal stops rising with weight.
  - Recompute when the 7-day median weight moves by ≥ 1 kg, to avoid daily jitter.
- **Activity tier:** a tier change moves the base goal by about 100–330 mL per step (Yamada's PAL coefficient × 0.68). Recompute weekly with hysteresis.
- **Pregnancy/lactation:** step changes of +300 / +700 mL for the duration. Mark them as shaded periods on the chart.
- **Season and climate:** these affect *today's* goal, not the base goal. On the chart, show the base line plus a lighter band or markers for heat and workout add-ons.
- **Store snapshots:** keep a dated snapshot of the profile inputs and formula version whenever the base goal changes. History should never be recomputed retroactively when the user edits their profile or the algorithm is updated. Include `goalAlgorithmVersion` in each snapshot.

---

## 8. Key values

| Value | Unit | Population | Source | Confidence |
|---|---|---|---|---|
| 3.7 total / ≈3.0 beverages | L/day | Men 19 y and over (NASEM AI) | [1] | High |
| 2.7 total / ≈2.2 beverages | L/day | Women 19 y and over (NASEM AI) | [1] | High |
| 3.0 / ≈2.3 | L/day | Pregnancy (NASEM) | [1] | High |
| 3.8 / ≈3.1 | L/day | Lactation (NASEM) | [1] | High |
| 1.3/0.9; 1.7/1.2; 2.4/1.8 (boys), 2.1/1.6 (girls); 3.3/2.6 (boys), 2.3/1.8 (girls) | L/day total/beverages | Ages 1–3; 4–8; 9–13; 14–18 (NASEM) | [1] | High |
| ≈19–22 | % of total water | Share from food (US) | [1][6] | Med |
| 2.5 (men) / 2.0 (women) | L/day total | Adults incl. elderly, from age 14 (EFSA) | [3] | High |
| +300 / +700 | mL/day | Pregnancy / lactation increment (EFSA) | [3] | High |
| 1.1–1.2; 1.3; 1.6; 2.1 (boys) / 1.9 (girls) | L/day total | Ages 1–2; 2–3; 4–8; 9–13 (EFSA) | [3] | High |
| ≥1.6 (women) / ≥2.0 (men) | L/day drinks | Older adults (ESPEN) | [7][8] | High |
| ≈1.8 | L/day total | Intake below which AVP rises (water conservation starts) | [5] | Med |
| ≈85 | % of water turnover | Share of turnover supplied by food + drink | [4] | Med |
| +1,000 per PAL unit; +700 per 50 kg; +400 male; +300 per 50% RH; +500 per 1,000 m; +1,000 athlete | mL/day WT | Adults, free-living (DLW) | [4] | Med–High |
| +670 / +260 | mL/day WT | 3rd trimester / lactation vs pre-pregnancy | [4] | Med |
| 3.2 (man 70 kg) / 2.7 (woman 60 kg) | L/day WT | Age 20, PAL 1.75, 10 °C, sea level | [4] | High |
| 0.5–2.0 (occasionally > 3) | L/h | Athlete sweat rate | [10] | High |
| 0.4–0.8 | L/h | Typical starting drink rate in endurance exercise (ACSM/IMMDA) | [9][11] | Med |
| > 2 | % body mass | Dehydration level to avoid during exercise | [9] | High |
| 5–7 | mL/kg | Pre-exercise drink, ≥ 4 h before | [9][11] | Med |
| 0.7–1.0 | L/h | Maximal renal water excretion | [1] | High |
| ≤ 1.4–1.5 (48 oz) | L/h | Upper hourly intake during heat work | [15][16] | High |
| 0.24 every 15–20 min | L | Heat work, moderate intensity (NIOSH) | [15] | High |
| ≈11.4 (12 qt) | L/day | Military daily ceiling under heat stress | [17] | Med |
| < 135 / symptomatic usually < 130 | mmol/L | Hyponatremia definition / symptom threshold | [1][13] | High |
| 13 / 0.6 | % of finishers | Hyponatremia / critical hyponatremia, Boston 2002 | [14] | High |
| 100 / 50 / 20 | mL/kg/day | Holliday–Segar tiers (IV maintenance, children) | [18] | High (as a definition) |
| 25–30 (20–25 for older/frail) | mL/kg/day | IV maintenance, adults (NICE) | [20] | High (as a definition) |
| 35 (< 51 y) / 30 (older) | mL/kg/day total | DGE weight-based guide | [22] | Med |
| < 5,000 / 5,000–7,499 / 7,500–9,999 / ≥ 10,000 / > 12,500 | steps/day | Sedentary / low / somewhat / active / highly active | [23] | Med (preliminary indices) |
| < 1.53 / 1.53–1.68 / 1.68–1.85 / 1.85–2.50 | PAL | Inactive / low / active / very active (NASEM 2023) | [24] | Med |
| 150–300 min moderate (or 75–150 vigorous) | min/week | Adult activity guideline | [25] | High |
| > 20 | % error | Wrist-device energy expenditure (best device) | [26] | High |
| ≈10 per °C above 38 °C | % increase in skin-loss replacement | Fever (clinical rule of thumb) | [35] | Low |
| 1.5–2 | L/day | Fluid restriction in *selected* heart-failure patients | [30] | High |
| ≥ 2.5 | L/day urine | Kidney stone prevention target | [32] | High |
| 1,600 / 2,000 / 4,500 | mL/day drinks | App floor (women) / floor (men) / ceiling | This note (derived from [3][7]) | Judgment |

---

## 9. Open questions / judgment calls

1. **Base authority.** The Yamada-based core lands between EFSA and NASEM. If the product wants to match US norms, it could offer a "Reference: US (NASEM)" setting that adds about 600–700 mL for men and about 500 mL for women. I recommend against making that the default: it is based on median self-reported intakes, and Yamada's measured data sit lower.
2. **Food share (0.80).** This is the least certain constant. Diets heavy in fruit, vegetables and soup can get 30–50% of water from food [4][6]. A "my diet is fruit- or veg-heavy" option could use 0.70.
3. **Age freeze at 35.** This is a policy choice backed by NASEM's and ESPEN's reasoning, not by data showing that older people need young-adult turnover. Revisit if better evidence appears.
4. **BMI-30 weight cap and the sex 0.5 coefficient** are both judgment calls.
5. **Step-to-PAL mapping** is not validated. Tudor-Locke's bands describe ambulatory activity, while PAL comes from doubly-labelled water. Consider letting users nudge their tier.
6. **Workout rates (400/600, +200 mL/h when hot).** These sit at the low-to-middle end of the ACSM range on purpose, for hyponatremia safety. Heavy sweaters will need more. A "sweat test" feature (weigh before and after a workout) could personalize this later [9][10].
7. **Double counting.** A daily runner gets both a higher tier and a workout bonus. This is acceptable because Yamada shows athletes have about 1 L extra turnover beyond PAL [4], and the ceiling bounds it. An alternative is computing the tier only from non-workout steps.
8. **Climate input without WeatherKit.** The options are manual toggles or a third-party API. Both have trade-offs (accuracy vs privacy). Indoor air-conditioned days could halve the climate add-on (judgment). Cold-weather increases are ignored in v1.
9. **Altitude add-on** has low confidence. It could be dropped from v1 entirely.
10. **Illness.** I chose not to auto-adjust the goal and to give guidance instead. A "sick day +500 mL" toggle is possible but not well evidenced.
11. **Not verified and therefore not used:** NHMRC (Australia/NZ) and Chinese 2023 DRI water values; the ACOG pregnancy figure ("8–12 cups", seen only on secondary sites); the full text of the ACSM 2007 stand (paywalled; its 0.4–0.8 L/h figure was taken from a secondary review); and the exact KDIGO 2024 wording on water intake.
12. **Regulatory framing.** Present the goal as general wellness guidance, never as medical advice. Keep the §5.4 gate.

---

## References

1. Institute of Medicine (now NASEM), Panel on Dietary Reference Intakes for Electrolytes and Water. *Dietary Reference Intakes for Water, Potassium, Sodium, Chloride, and Sulfate.* Washington, DC: National Academies Press; 2005 (report released Feb 2004). Chapter 4, "Water". doi:10.17226/10925. https://nap.nationalacademies.org/catalog/10925 (chapter read at https://www.nationalacademies.org/read/10925/chapter/6)
2. National Academies. "Report sets dietary intake levels for water, salt, and potassium to maintain health and reduce chronic disease risk." News release, 11 Feb 2004. https://www.nationalacademies.org/news/report-sets-dietary-intake-levels-for-water-salt-and-potassium-to-maintain-health-and-reduce-chronic-disease-risk
3. EFSA Panel on Dietetic Products, Nutrition, and Allergies (NDA). Scientific Opinion on Dietary Reference Values for water. *EFSA Journal* 2010;8(3):1459. doi:10.2903/j.efsa.2010.1459. https://www.efsa.europa.eu/en/efsajournal/pub/1459
4. Yamada Y, Zhang X, Henderson MET, et al. Variation in human water turnover associated with environmental and lifestyle factors. *Science* 2022;378(6622):909–915. doi:10.1126/science.abm8668. PMID 36423296; PMCID PMC9764345. https://pmc.ncbi.nlm.nih.gov/articles/PMC9764345/
5. Armstrong LE, Johnson EC. Water intake, water balance, and the elusive daily water requirement. *Nutrients* 2018;10(12):1928. doi:10.3390/nu10121928. PMCID PMC6315424. https://pmc.ncbi.nlm.nih.gov/articles/PMC6315424/
6. Popkin BM, D'Anci KE, Rosenberg IH. Water, hydration, and health. *Nutrition Reviews* 2010;68(8):439–458. doi:10.1111/j.1753-4887.2010.00304.x. PMCID PMC2908954. https://pmc.ncbi.nlm.nih.gov/articles/PMC2908954/
7. Volkert D, Beck AM, Cederholm T, et al. ESPEN guideline on clinical nutrition and hydration in geriatrics. *Clinical Nutrition* 2019;38(1):10–47. doi:10.1016/j.clnu.2018.05.024. PMID 30005900. https://pubmed.ncbi.nlm.nih.gov/30005900/
8. Volkert D, Beck AM, Cederholm T, et al. ESPEN practical guideline: clinical nutrition and hydration in geriatrics. *Clinical Nutrition* 2022;41(4):958–989. doi:10.1016/j.clnu.2022.01.024. PMID 35306388. https://pubmed.ncbi.nlm.nih.gov/35306388/
9. American College of Sports Medicine; Sawka MN, Burke LM, Eichner ER, Maughan RJ, Montain SJ, Stachenfeld NS. American College of Sports Medicine position stand. Exercise and fluid replacement. *Medicine & Science in Sports & Exercise* 2007;39(2):377–390. doi:10.1249/mss.0b013e31802ca597. PMID 17277604. https://pubmed.ncbi.nlm.nih.gov/17277604/
10. Baker LB. Sweating rate and sweat sodium concentration in athletes: a review of methodology and intra/interindividual variability. *Sports Medicine* 2017;47(Suppl 1):111–128. doi:10.1007/s40279-017-0691-5. PMCID PMC5371639. https://pmc.ncbi.nlm.nih.gov/articles/PMC5371639/
11. Armstrong LE. Rehydration during endurance exercise: challenges, research, options, methods. *Nutrients* 2021;13(3):887. doi:10.3390/nu13030887. PMCID PMC8001428. https://pmc.ncbi.nlm.nih.gov/articles/PMC8001428/
12. Kenney WL. Dietary water and sodium requirements for active adults. *Sports Science Exchange* 92, 2004;17(1). Gatorade Sports Science Institute. https://www.gssiweb.org/en/sports-science-exchange/article/sse-92-dietary-water-and-sodium-requirements-for-active-adults
13. Hew-Butler T, Rosner MH, Fowkes-Godek S, et al. Statement of the Third International Exercise-Associated Hyponatremia Consensus Development Conference, Carlsbad, California, 2015. *Clinical Journal of Sport Medicine* 2015;25(4):303–320. doi:10.1097/JSM.0000000000000221. PMID 26102445. https://pubmed.ncbi.nlm.nih.gov/26102445/
14. Almond CS, Shin AY, Fortescue EB, et al. Hyponatremia among runners in the Boston Marathon. *New England Journal of Medicine* 2005;352(15):1550–1556. doi:10.1056/NEJMoa043901. PMID 15829535. https://pubmed.ncbi.nlm.nih.gov/15829535/
15. National Institute for Occupational Safety and Health (NIOSH). *Heat Stress: Hydration.* CDC/NIOSH fact sheet, 2017. https://stacks.cdc.gov/view/cdc/45851
16. Orysiak J, Młynarczyk M, Bugajska J, Łastowiecka-Moras E. Hydration of workers in thermal environments: practical recommendation. *Nutrients* 2025;18(1):64. doi:10.3390/nu18010064. PMCID PMC12787638. https://pmc.ncbi.nlm.nih.gov/articles/PMC12787638/
17. US Army. *TB MED 507: Heat Stress Control and Heat Casualty Management* (12 Apr 2022), with Army Public Health Center fluid-replacement materials. https://ph.health.mil/PHC%20Resource%20Library/cphe-heat-fluid-replacement-poster.pdf (hourly/daily limits taken from Army public-health handouts; primary TB MED 507 table not read)
18. Holliday MA, Segar WE. The maintenance need for water in parenteral fluid therapy. *Pediatrics* 1957;19(5):823–832. doi:10.1542/peds.19.5.823. https://pubmed.ncbi.nlm.nih.gov/13431307/
19. Feld LG, Neuspiel DR, Foster BA, et al. Clinical practice guideline: maintenance intravenous fluids in children. *Pediatrics* 2018;142(6):e20183083. doi:10.1542/peds.2018-3083. PMID 30478247. https://pubmed.ncbi.nlm.nih.gov/30478247/
20. National Institute for Health and Care Excellence. *Intravenous fluid therapy in adults in hospital* (CG174). 2013, updated 2017. https://www.nice.org.uk/guidance/cg174/chapter/recommendations
21. Chidester JC, Spangler AA. Fluid intake in the institutionalized elderly. *Journal of the American Dietetic Association* 1997;97(1):23–28. doi:10.1016/S0002-8223(97)00011-4. PMID 8990413. https://pubmed.ncbi.nlm.nih.gov/8990413/
22. Deutsche Gesellschaft für Ernährung (DGE). Referenzwerte für die Nährstoffzufuhr: Wasser (reference values for water). https://www.dge.de/wissenschaft/referenzwerte/wasser/ (values confirmed via secondary summaries only)
23. Tudor-Locke C, Bassett DR Jr. How many steps/day are enough? Preliminary pedometer indices for public health. *Sports Medicine* 2004;34(1):1–8. doi:10.2165/00007256-200434010-00001. PMID 14715035. https://pubmed.ncbi.nlm.nih.gov/14715035/
24. National Academies of Sciences, Engineering, and Medicine. *Dietary Reference Intakes for Energy.* Washington, DC: National Academies Press; 2023. doi:10.17226/26818. https://nap.nationalacademies.org/catalog/26818
25. Bull FC, Al-Ansari SS, Biddle S, et al. World Health Organization 2020 guidelines on physical activity and sedentary behaviour. *British Journal of Sports Medicine* 2020;54(24):1451–1462. doi:10.1136/bjsports-2020-102955. https://bjsm.bmj.com/content/54/24/1451
26. Shcherbina A, Mattsson CM, Waggott D, et al. Accuracy in wrist-worn, sensor-based measurements of heart rate and energy expenditure in a diverse cohort. *Journal of Personalized Medicine* 2017;7(2):3. doi:10.3390/jpm7020003. PMCID PMC5491979. https://pmc.ncbi.nlm.nih.gov/articles/PMC5491979/
27. Mifflin MD, St Jeor ST, Hill LA, et al. A new predictive equation for resting energy expenditure in healthy individuals. *American Journal of Clinical Nutrition* 1990;51(2):241–247. doi:10.1093/ajcn/51.2.241. PMID 2305711. https://pubmed.ncbi.nlm.nih.gov/2305711/
28. Killer SC, Blannin AK, Jeukendrup AE. No evidence of dehydration with moderate daily coffee intake: a counterbalanced cross-over study in a free-living population. *PLoS One* 2014;9(1):e84154. doi:10.1371/journal.pone.0084154. PMCID PMC3886980. https://pmc.ncbi.nlm.nih.gov/articles/PMC3886980/
29. Maughan RJ, Watson P, Cordery PA, et al. A randomized trial to assess the potential of different beverages to affect hydration status: development of a beverage hydration index. *American Journal of Clinical Nutrition* 2016;103(3):717–723. doi:10.3945/ajcn.115.114769. PMID 26702122. https://pubmed.ncbi.nlm.nih.gov/26702122/
30. Mullens W, Damman K, Dhont S, et al. Dietary sodium and fluid intake in heart failure. A clinical consensus statement of the Heart Failure Association of the ESC. *European Journal of Heart Failure* 2024;26(4):730–741. doi:10.1002/ejhf.3244. PMID 38606657. https://pubmed.ncbi.nlm.nih.gov/38606657/
31. Clark WF, Sontrop JM, Huang SH, et al. Effect of coaching to increase water intake on kidney function decline in adults with chronic kidney disease: the CKD WIT randomized clinical trial. *JAMA* 2018;319(18):1870–1879. doi:10.1001/jama.2018.4930. PMCID PMC6583759. https://pmc.ncbi.nlm.nih.gov/articles/PMC6583759/
32. American Urological Association. *Medical Management of Kidney Stones* guideline (2014, amended 2019; updated 2026). https://www.auanet.org/guidelines/guidelines/kidney-stones-medical-mangement-guideline
33. World Health Organization. *Guidelines for drinking-water quality: fourth edition incorporating the first and second addenda.* Geneva: WHO; 2022. https://www.who.int/publications/i/item/9789240045064
34. Howard G, Bartram J. *Domestic water quantity, service level and health.* Geneva: WHO; 2003. 2nd edition: Howard G, Bartram J, Williams A, et al. WHO; 2020. https://www.who.int/publications/i/item/9789240015241
35. University of Texas Medical Branch, Pediatric Education. Maintenance fluid requirements in disease. https://www.utmb.edu/Pedi_Ed/CoreV2/Fluids/Fluids7.html (teaching material; low-grade evidence)
36. Institute of Medicine, Committee on Military Nutrition Research. *Nutritional Needs in Cold and in High-Altitude Environments.* Washington, DC: National Academies Press; 1996. https://www.nationalacademies.org/read/5197/chapter/23
37. Masot O, Miranda J, Santamaría AL, Paraiso Pueyo E, Pascual A, Botigué T. Fluid intake recommendation considering the physiological adaptations of adults over 65 years: a critical review. *Nutrients* 2020;12(11):3383. doi:10.3390/nu12113383. PMCID PMC7694182. https://pmc.ncbi.nlm.nih.gov/articles/PMC7694182/
38. Luks AM, McIntosh SE, Grissom CK, et al. Wilderness Medical Society practice guidelines for the prevention and treatment of acute altitude illness: 2014 update. *Wilderness & Environmental Medicine* 2014;25(4 Suppl):S4–S14. doi:10.1016/j.wem.2014.06.017. https://pubmed.ncbi.nlm.nih.gov/25498261/ (cited via secondary summary; primary text not read)
39. National Academies of Sciences, Engineering, and Medicine. *Dietary Reference Intakes for Sodium and Potassium.* Washington, DC: National Academies Press; 2019. doi:10.17226/25353. https://nap.nationalacademies.org/catalog/25353
40. University of Texas Medical Branch, Pediatric Education. Normal maintenance requirements (Holliday–Segar derivation). https://www.utmb.edu/Pedi_Ed/CoreV2/Fluids/Fluids4.html
41. Rowland T. Fluid replacement requirements for child athletes. *Sports Medicine* 2011;41(4):279–288. doi:10.2165/11584320-000000000-00000. https://pubmed.ncbi.nlm.nih.gov/21425887/ (figure taken from an abstract-level summary)
