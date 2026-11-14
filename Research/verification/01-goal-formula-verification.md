# Verification: Daily Drink-Goal Formula (checks `01-daily-water-requirements.md`)

*Verification pass, 2026-11-13. The equation was checked against the authors' accepted manuscript of Yamada et al., Science 2022 [1][2]. The examples were re-run with a Python script, and the conversion chain was compared with measured and surveyed intakes.*

---

## TL;DR verdict: **VERIFIED, with five small corrections**

1. **The equation is correct.** The original note reconstructed Yamada eq. 1, and all 12 coefficients, the sex/athlete/HDI coding and the intercept match the accepted manuscript exactly [2]. The paper's four worked examples reproduce to the millilitre (3,184 / 2,666 / 7,338 / 6,820 mL/d).
2. **The conversion chain is sound.** The ×0.85 turnover→intake factor matches a first-principles estimate of about 0.83–0.86. The ×0.80 drinks share sits within the measured US range of 0.76–0.83 [3].
3. **The 70 kg, 30-year-old active man stays at 2,300 mL.** The chain does not undercount. The gap to NASEM's ~3.0 L comes from three things: NASEM's figure is a self-reported median for heavier US men, self-report overstates intake compared with isotope measurement, and NASEM does not scale for body size (§3).
4. **Corrections:**
   - (a) Replace the hard BMI-30 weight cap with a soft cap. Weight above BMI 30 counts at 65%.
   - (b) If steps come from the iPhone only, an "inactive" result is raised to "low active".
   - (c) With no HealthKit data, the default tier is **low active (PAL 1.60)**.
   - (d) The temperature input must be the **24-hour mean** air temperature, not the daily maximum.
   - (e) Fix an arithmetic typo in the note's Example 3. The final number was already right.

Everything else stays as written: floors, ceiling, age-35 freeze, workout, heat, altitude, pregnancy and lactation add-ons, and the step bands.

---

## 1. The Yamada equation, verified

### 1.1 Source

- **Where it was found:** the PMC HTML [1] omits the typeset equation. The authors' accepted manuscript on UCL Discovery [2] prints it in full as "eq. 1", with the variable coding directly below it, and also prints a fat-free-mass version as "eq. 2".
- **Errata:** none found.

**Eq. 1 (body-weight version), water turnover in mL/day [2]:**

```
WT = 1076·PAL + 14.34·BW + 374.9·Sex + 5.823·RH + 1070·Athlete + 104.6·HDI
     + 0.4726·Alt − 0.3529·Age² + 24.78·Age + 1.865·T² − 19.66·T − 713.1
```

| Variable | Unit / coding [2] |
|---|---|
| PAL | TEE ÷ BEE. In the paper, BEE was *predicted* with Mifflin–St Jeor for ages ≥18 and Schofield for younger people, because only about 30% of participants had measured BEE [2]. This is the same TEE/BEE definition NASEM uses, so NASEM PAL values can be used directly [7] |
| BW | Body weight, kg. The authors used weight plus sex as a stand-in for fat-free mass [2] |
| Sex | 0 = female, 1 = male. Reference: female |
| RH | Relative humidity, % (mean during the measurement period, from weather-station data) |
| Athlete | 0 = non-athlete, 1 = athlete. Reference: non-athlete |
| HDI | 0 = high, 1 = middle, 2 = low HDI country. Reference: high |
| Alt | Altitude, metres |
| Age | Years. The age curve peaks at 24.78 / (2·0.3529) = **35.1 years** |
| T | Mean air temperature, °C. The curve is U-shaped with its lowest point at 19.66 / (2·1.865) = **5.3 °C** |

- **Fit:** eq. 1 explains 47.1% of the variance [2].
- **Dataset:** 5,604 people aged 8 days to 96 years in 26 countries [1].

**Eq. 2 (fat-free-mass version, no sex term), for reference only [2]:**

`WT = 861.9·PAL + 37.34·FFM + 4.288·RH + 699.7·Athlete + 105.0·HDI + 0.5140·Alt − 0.3625·Age² + 29.42·Age + 1.937·T² − 23.15·T − 984.8`

The app cannot measure FFM reliably, so eq. 1 stays the core. Eq. 2 is used only to justify the soft weight cap (§4.3).

### 1.2 How water turnover was measured

- **Formula:** turnover was computed as rH₂O = k_D × N_D, the deuterium elimination rate times the deuterium dilution space [2].
- **Possible overstatement:** N_D is a few percent larger than true total body water, and evaporative isotope fractionation was not corrected [2][13]. Absolute WT may therefore be slightly overstated, on the order of a few percent.
- **Effect on the app:** this is small, under about 100 mL of drinks, and it partly cancels with the conservative 0.80 drinks share. No adjustment.

### 1.3 Coefficient comparison with the original note

| Term | Original note | Verified [2] | Match |
|---|---|---|---|
| PAL | 1076 | 1076 | ✔ |
| Body weight | 14.34 | 14.34 | ✔ |
| Sex (male = 1) | 374.9 | 374.9 | ✔ |
| RH (%) | 5.823 | 5.823 | ✔ |
| Athlete | 1070 | 1070 | ✔ |
| HDI (0 high / 1 mid / 2 low) | 104.6 | 104.6 | ✔ (coding also matches) |
| Altitude (m) | 0.4726 | 0.4726 | ✔ |
| Age² | −0.3529 | −0.3529 | ✔ |
| Age | 24.78 | 24.78 | ✔ |
| T² | 1.865 | 1.865 | ✔ |
| T | −19.66 | −19.66 | ✔ |
| Intercept | −713.1 | −713.1 | ✔ |
| Reference constant (15 °C, 50% RH, 0 m, non-athlete, high HDI) | −297.2 | −297.22 | ✔ |

---

## 2. Re-running the note's examples

The examples were re-run with a throwaway Python script (not kept in the repo); the table below records its output.

| Note example | Note value | Re-computed | Status |
|---|---|---|---|
| Paper: man, 20 y, 70 kg, PAL 1.75, 10 °C, 50% RH | 3,184 → "3.2 L" | 3,184 | ✔ |
| Paper: woman, 60 kg, same setting | 2,666 → "2.7 L" | 2,666 | ✔ |
| Paper: athletic man, PAL 2.5, 2,000 m, 30 °C, 90% RH | 7,338 → "7.3 L" | 7,338 | ✔ |
| Paper: athletic woman, 60 kg, same setting | 6,820 → "6.8 L" | 6,820 | ✔ |
| Ex 1: man, 30, 70 kg, active | WT 3,390 → 2,300 | 3,390 → 2,305 → **2,300** | ✔ |
| Ex 2: woman, 65, 58 kg, inactive | 2,476 → 1,700 | 2,476 → 1,684 → **1,700** | ✔ |
| Ex 3: pregnant, 31, 64 kg, low active | 2,771 → 2,200 | 2,771 → 2,184 → **2,200** | ✔ |
| Ex 3 at 22 °C, 60% RH | +343 → 2,550 | +343 → **2,550** | ✔ result, but the intermediate is wrong: the note writes the 22 °C temperature term as 352.7; it is **470.1** (0.85 × (470.1 − 124.7 + 58.2) = 343) |
| Ex 3 lactating | 2,600 | **2,600** | ✔ |
| Ex 4: boy, 16, 65 kg, very active, rest / practice day | 2,400 / 4,218 → 4,000 | 2,395 → **2,400** / 4,218 → **4,000** | ✔ |
| Ex 5: Ex 1 man at 30 °C, 60% RH, 1 h moderate | 3,774 → 3,750 | 3,774 → **3,750** | ✔ |
| §2 table: 120 kg man, BMI 39, hard cap | 2,250 | 2,250 hard cap / 2,450 with the soft cap in §4.3 (inactive, age ≥35) | changed by correction (a) |

---

## 3. Conversion chain: turnover → intake → drinks

### 3.1 Is ×0.85 justified?

**Yamada's own figure [2]:** metabolic water is about 10% of WT, and respiratory plus skin vapour uptake are 2–3% each. So intake from food and drink is about 85% of WT. The paper cites the doubly-labelled-water study by Raman et al. for this [6].

**First-principles check for the 70 kg, 30-year-old active man (WT = 3,390 mL):**

1. **Energy expenditure.** BEE (Mifflin, 178 cm) = 1,668 kcal. TEE = 1.75 × 1,668 = 2,918 kcal.
2. **Metabolic water.** Oxidising food yields about 0.6 g water per g carbohydrate, about 1.07 g per g fat and about 0.41 g per g protein. On a 50/35/15% energy diet that is about 0.13 mL per kcal. 0.13 × 2,918 ≈ **385 mL** (11.4% of WT). This agrees with NASEM's description of metabolic water as a few hundred mL/day, rising with activity [4].
3. **Vapour uptake.** Lungs plus skin at 2–3% each [2] gives about **135–205 mL** (4–6%).
4. **Intake share.** (3,390 − 385 − 135…205) / 3,390 = **0.83–0.86**.

**Verdict:** keep **0.85**. The plausible range moves the drink goal by only about ±40 mL.

**Cross-check against measured intake.** Raman et al. measured preformed water intake (drinks plus food water, from isotope turnover minus metabolic and vapour water) in 458 US adults aged 40–79 [6]:
- Men averaged about 3.0 L/d and women about 2.5 L/d.
- Eq. 1 × 0.85, for a typical OPEN-study man (about 55 y, 88 kg, PAL 1.7, temperate), gives about 2.94 L.
- For a woman (about 72 kg, PAL 1.6), it gives about 2.34 L.
- So the chain matches isotope-measured intake to within about 2–6%, with no systematic undercount.

### 3.2 Is ×0.80 (drinks share of intake) justified?

| Source | Food share of total water | Drinks share |
|---|---|---|
| NASEM / NHANES III [4] | ≈19–22% | ≈0.78–0.81 |
| NHANES 2005–10, ages 20–50 [3] | 590 of 3,560 mL = 16.6% | 0.83 |
| NHANES 2005–10, ages 51–70 [3] | 18.5% | 0.82 |
| NHANES 2005–10, ages ≥71 [3] | 24.3% | 0.76 |
| EFSA (Europe) [5] | ≈20–30% | ≈0.70–0.80 |
| Yamada: surveys likely *under*-count food water [2] | — | true share probably ≤ survey values |

**Verdict:** keep **0.80**. US self-report puts it at 0.76–0.83, and Yamada's point about survey bias pushes the true value lower, not higher.

### 3.3 Is 2,300 mL right for the 70 kg, 30-year-old active man?

| Benchmark | Drinks, mL/d | What it really is |
|---|---|---|
| **This algorithm** | **2,300** | Isotope-based prediction for *this* person (70 kg, temperate) |
| Raman isotope-derived intake, US men 40–79 [6] | ≈2,400 (3.0 L × 0.80) | Measured. Heavier, older men |
| EFSA AI men [5] | 2,000 (2.5 L × 0.80) | Based on intake surveys plus a desirable urine-concentration target |
| Liq.In7, 7-day fluid diaries, 13 countries [8] | median 1,780 for men (1,390 Japan to 2,430 Germany) | Measured drinks, diary method |
| NHANES 2005–10, 24-h recall [3] | ≈2,940 drinks (ages 20–50, both sexes); men's total 3,779 | Self-report, US |
| NASEM AI men [4] | ≈3,000 | Median of NHANES III self-reports; not scaled to body size |

**Why NASEM is higher:**
1. **Body size.** The average US man weighs about 90 kg. The same algorithm for a 90 kg, 35-year-old, low-active man gives 2,400 mL. At PAL 1.75 it gives 2,500 mL.
2. **Self-report bias.** NHANES men report 3.78 L total. Isotope-derived intake in a comparable US sample is about 3.0 L [3][6], so self-report runs about 20–25% higher.
3. **Median by design.** The NASEM AI is the median observed intake, not a requirement [4].

**Decision:** 2,300 mL stands. It sits above EFSA's osmolality-informed figure, above what most Europeans actually drink, and in line with isotope-measured US intake once body size is accounted for. **No correction factor is applied.**

---

## 4. Floors, ceiling and add-ons

### 4.1 Floors: women 1,600 / men 2,000 / unspecified 1,800 / pregnant 1,840 / lactating 2,160 mL. **Keep.**
- 0.8 × EFSA total-water AI [5] equals ESPEN's minimum drink offer for older adults (≥1.6 L women, ≥2.0 L men) [9].
- EFSA treats ages 14 and over as adults, so the floors apply from 14.
- The floor binds for small, inactive women: a 50 kg inactive woman gets about 1,606 mL. That is the intended behaviour.

### 4.2 Ceiling: 4,500 mL (adults), 4,000 mL (14–17). **Keep.**
- This is a product safety cap, not a physiological maximum.
- It sits above EFSA's 95th-percentile male *total* intake of 4.0 L [5] and below the US 95th percentile of about 6.4 L [4].
- It keeps the app from pushing large volumes. Overdrinking relative to losses is the main cause of exercise-associated hyponatremia [12].

### 4.3 Weight term: hard BMI-30 cap → **soft cap (CORRECTED)**
- **Problem with the hard cap:** it ignores all weight above BMI 30. Eq. 1 was fitted on a sample that included people with obesity, and their absolute turnover does keep rising with weight. Excess weight is not pure fat.
- **Soft cap:**
  - Weight above the BMI-30 weight is counted at **0.65**.
  - Basis: excess weight in adults with obesity is roughly one-quarter fat-free mass [14], and eq. 2 gives 37.34 mL WT per kg of FFM [2]. So 0.25 × 37.34 ≈ 9.3 mL per excess kg, which is 0.65 of eq. 1's 14.34 mL/kg.
- **Effect:** an inactive 120 kg, 175 cm man (age ≥35) gets 2,450 mL instead of 2,250 (2,550 with no cap at all). The overall clamp of 35–150 kg still applies after the soft cap.
- **Without height:** no cap.

### 4.4 Age-35 freeze. **Keep.**
- The eq. 1 age curve peaks at 35.1 y [2], so freezing at 35 holds the goal at its maximum.
- The equation's fall after 35 (about −700 mL WT by age 80 [2]) describes what older people *do*, not what they need. Thirst blunting is the reason NASEM and ESPEN did not lower older adults' values [4][9].
- Lower bound 14: below that, use the note's child table mode.

### 4.5 Workout add-on: 400 mL/h moderate, 600 mL/h vigorous, +200 mL/h if mean T ≥ 25 °C, workouts ≥ 20 min, cap +1,500. **Keep.**
- Hot vigorous sessions reach 800 mL/h, which keeps every rate inside the ACSM 0.4–0.8 L/h starting range [10].
- The overlap with the PAL tier is intended. Eq. 1's PAL slope works out to only about 0.6 mL per kcal of activity, far below acute sweat losses. Athletes show about 1 L/d of extra turnover beyond what PAL explains [2].
- Coaching copy: "drink to thirst, don't gain weight during exercise" [12].

### 4.6 Heat add-on: `0.85 × [ (1.865T² − 19.66T) − 124.7 + (T ≥ 20 ? 5.823·max(0, RH − 50) : 0) ]`, for T > 15 °C, cap +1,000. **Keep, with a clarification.**
- **T is the 24-hour mean outdoor temperature** (e.g. (Tmax + Tmin)/2 from a weather API), because the paper used mean air temperature [2]. A 30 °C *mean* day is roughly a 35–37 °C *maximum* day.
- Manual toggles: "Hot day" = 25 °C mean (+~470 mL), "Very hot day" = 30 °C mean (+~820 mL, or +869 at 60% RH).
- Yamada found that temperature effects were smaller in high-HDI countries, probably because of indoor climate control [2]. The pooled coefficient may therefore overstate the effect for people in air-conditioning. The +1,000 cap bounds this. No further change.
- Cold-weather increases stay ignored in v1.

### 4.7 Altitude add-on: `min(500, 0.85 × 0.4726 × max(0, alt − 1500))`. **Keep, low confidence.**
- The coefficient is verified [2].
- The 1,500 m threshold and the 500 mL cap are product choices.

### 4.8 Pregnancy +300 / lactation +700 mL of drinks. **Keep.**
- These are EFSA's total-water increments [5], applied fully to drinks.
- That is generous compared with NASEM's beverage increments (+100 pregnancy, +900 lactation) [4], and sits near Yamada's measured +670 mL WT in the third trimester and +260 mL in lactation [2].
- Use **pre-pregnancy weight** so gestational weight gain isn't counted twice.

---

## 5. Step count → PAL

- **NASEM 2023 categories:** the four PAL categories are approximate **quartiles** of the doubly-labelled-water PAL distribution [7]:
  - inactive 1.00–<1.53
  - low active 1.53–<1.68
  - active 1.68–<1.85
  - very active 1.85–<2.50
- **NASEM example values:** 1.40, 1.60, 1.75 and 2.05 [7]. NASEM itself warns that no valid tool assigns an individual to a category [7], so any step mapping is approximate.
- **Evidence for the bands:**
  - Free-living Japanese adults measured with doubly-labelled water averaged PAL 1.73 at about 10,000 steps/day, but steps and PAL were not significantly correlated. Non-walking activity drives much of PAL [15].
  - Tudor-Locke et al. translate meeting the activity guideline into about 7,100–11,000 steps/day [16].
  - Both fit "active ≈ 7,500–12,499 steps → PAL 1.75".
- **iPhone-only data:** smartphone step data run low because people don't carry the phone all day. In 717,000 phone users, the mean was about 4,960 steps/day [17]. Phone-only users would otherwise fall into "inactive" far too often.

**Final mapping (14-day mean of daily steps; recompute weekly, with hysteresis as in the note):**

| Tier | Steps/day [11][16] | PAL used [7] |
|---|---|---|
| Inactive | < 5,000 | **1.40** |
| Low active | 5,000–7,499 | **1.60** |
| Active | 7,500–12,499 | **1.75** |
| Very active | ≥ 12,500 | **2.05** |

**Additional rules:**
- **iPhone-only steps:** if no Apple Watch contributed steps in the window, raise "inactive" to "low active". This is a judgment call, based on [17].
- **Fallbacks:** keep the note's order. Weekly exercise minutes come next (<60 / 60–149 / 150–299 / ≥300 → the four tiers), then self-report.
- **Combining sources:** if both steps and exercise minutes exist, use the **higher** of the two tiers.

## 6. Users with no HealthKit data

- **Onboarding question:** ask one self-report question with four plain-language choices, mapped to the four tiers.
- **If skipped, default to low active (PAL 1.60).** Reasons:
  - Because NASEM's categories are quartiles, the population median PAL sits at about 1.68, the low-active/active boundary [7]. 1.60 is the nearest example value without assuming above-median activity.
  - It matches EFSA's moderate-activity assumption of PAL about 1.6 [5].
  - The floors protect anyone who is actually less active.
- **Effect:** a 62 kg, 30-year-old woman with no data gets 1,850 mL; a 30-year-old 75 kg man gets 2,250 mL.

---

## 7. FINAL ALGORITHM (implementation-ready)

```
CONSTANTS
  // Yamada 2022 eq.1 [2] — mL/day
  C_PAL = 1076.0;  C_BW = 14.34;  C_SEX = 374.9;  C_RH = 5.823
  C_ALT = 0.4726;  C_AGE2 = -0.3529;  C_AGE = 24.78
  C_T2 = 1.865;    C_T = -19.66
  REF_CONST = -297.22        // = 5.823*50 + (1.865*15² − 19.66*15) − 713.1
                             //   (15 °C, 50 % RH, 0 m, non-athlete, high HDI)
  TEMP_REF_TERM = 124.65     // 1.865*15² − 19.66*15
  INTAKE_SHARE = 0.85        // food+drink share of turnover [2], verified §3.1
  DRINK_SHARE  = 0.80        // drinks share of intake [3][4], verified §3.2
  PAL = { inactive: 1.40, lowActive: 1.60, active: 1.75, veryActive: 2.05 }   // [7]
  DEFAULT_TIER = lowActive                                                    // §6
  SEX_CODE = { male: 1.0, female: 0.0, unspecified: 0.5 }
  BMI_SOFT_CAP = 30.0;  EXCESS_WEIGHT_FACTOR = 0.65                           // §4.3
  WEIGHT_MIN_KG = 35;  WEIGHT_MAX_KG = 150
  AGE_MIN = 14;  AGE_MAX_EFF = 35                                             // §4.4
  PREG_ADD = 300;  LACT_ADD = 700                                             // [5]
  ALT_THRESHOLD_M = 1500;  ALT_CAP = 500
  CLIMATE_CAP = 1000;  CLIMATE_T_MIN = 15.0;  HUMIDITY_T_MIN = 20.0
  WORKOUT_MIN_MIN = 20; RATE_MOD = 400; RATE_VIG = 600; RATE_HEAT_BONUS = 200 // mL/h [10]
  HEAT_WORKOUT_T = 25.0;  WORKOUT_CAP = 1500
  FLOOR = { male: 2000, female: 1600, unspecified: 1800, pregnant: 1840, lactating: 2160 }
  CEILING_ADULT = 4500 (age ≥ 18);  CEILING_TEEN = 4000 (14–17)
  ROUND_METRIC = 50 mL;  ROUND_US = 4 fl oz (118.294 mL)

INPUTS
  ageYears (Double), sex, weightKg (7-day median; PRE-pregnancy weight if pregnant),
  heightCm (optional), tier (from §5/§6), repro ∈ {none, pregnant, lactating},
  elevationM (default 0), fluidRestricted (Bool),
  day: meanTempC? (24-h MEAN outdoor), meanRH? (%), workouts[(minutes, moderate|vigorous)]

if ageYears < 4  → unsupported
if ageYears < 14 → child table mode (unchanged from original note §6.3)

// ---- base goal (profile only) ----
sexC   = SEX_CODE[sex]
ageEff = clamp(ageYears, AGE_MIN, AGE_MAX_EFF)
w      = weightKg
if heightCm != nil:
    wCap = BMI_SOFT_CAP * (heightCm/100)²
    if w > wCap: w = wCap + EXCESS_WEIGHT_FACTOR * (w − wCap)
w      = clamp(w, WEIGHT_MIN_KG, WEIGHT_MAX_KG)

WT     = C_PAL*PAL[tier] + C_BW*w + C_SEX*sexC + C_AGE2*ageEff² + C_AGE*ageEff + REF_CONST
base   = INTAKE_SHARE * DRINK_SHARE * WT                     // = 0.68 * WT
base  += (repro == pregnant ? PREG_ADD : repro == lactating ? LACT_ADD : 0)
base  += min(ALT_CAP, INTAKE_SHARE * C_ALT * max(0, elevationM − ALT_THRESHOLD_M))

// ---- today's add-ons (skipped entirely if fluidRestricted) ----
climate = 0
if meanTempC != nil and meanTempC > CLIMATE_T_MIN:
    T  = meanTempC
    dW = (C_T2*T² + C_T*T) − TEMP_REF_TERM
    if T ≥ HUMIDITY_T_MIN and meanRH != nil: dW += C_RH * max(0, meanRH − 50)
    climate = min(CLIMATE_CAP, INTAKE_SHARE * max(0, dW))
workout = 0
for (m, intensity) in workouts where m ≥ WORKOUT_MIN_MIN:
    rate = (intensity == vigorous ? RATE_VIG : RATE_MOD)
    if meanTempC != nil and meanTempC ≥ HEAT_WORKOUT_T: rate += RATE_HEAT_BONUS
    workout += m/60 * rate
workout = min(WORKOUT_CAP, workout)

// ---- clamp and round once ----
floor   = FLOOR[pregnant|lactating if applicable, else sex]
ceiling = ageYears ≥ 18 ? CEILING_ADULT : CEILING_TEEN
goal    = clamp(base + climate + workout, floor, ceiling)
goal    = round-half-up(goal / 50) * 50          // metric; US: round(goalML/118.294 / 4)*4 fl oz
```

Notes for the Swift developer:
- Keep everything in `Double` until the final rounding.
- The "base goal" shown on the long-term chart is `clamp(base, floor, ceiling)` rounded the same way.
- Store a `goalAlgorithmVersion` with each snapshot, as in the original note.
- Recognised manual heat toggles: Hot = 25 °C mean, Very hot = 30 °C mean. In that case RH is unknown and gets no humidity term.

### 7.1 Worked examples (sea level; "temperate" = no weather input)

| # | Person | Inputs | WT (mL) | Base drinks | Add-ons | **Goal** |
|---|---|---|---|---|---|---|
| 1 | Man, 30, 70 kg, 178 cm | Active (PAL 1.75) | 3,390 | 2,305 | — | **2,300** |
| 2 | Woman, 75, 58 kg, 160 cm | Inactive (1.40); age frozen at 35 | 2,476 | 1,684 | — | **1,700** |
| 3 | Boy, 16, 65 kg, 178 cm | Very active (2.05); rest day | 3,522 | 2,395 | — | **2,400** |
| 3b | Same boy | 90 min vigorous, 27 °C mean, 55% RH | 3,522 | 2,395 | climate +623, workout +1,200 = 4,218 | **4,000** (teen ceiling) |
| 4 | Girl, 16, 50 kg, 165 cm | Low active (1.60) | 2,448 | 1,664 | — | **1,650** |
| 5 | Pregnant woman, 30, 64 kg pre-pregnancy, 168 cm | Low active (1.60) | 2,768 | 1,882 + 300 = 2,182 | — | **2,200** (lactating: 2,582 → **2,600**) |
| 6 | Man, 50, 110 kg, 180 cm (BMI 34) | Inactive (1.40); soft cap → w_eff 105.5 kg | 3,532 | 2,402 | — | **2,400** (old hard cap: 2,300) |
| 7 | Woman, 50, 80 kg, 165 cm (BMI 29.4) | Very active (2.05) | 3,491 | 2,374 | — | **2,350** |
| 8 | Man #1 on a hot workout day | 30 °C mean, 60% RH, 60 min moderate | 3,390 | 2,305 | climate +869, workout +600 = 3,774 | **3,750** |
| (9) | Woman, 30, 62 kg, no HealthKit data | Default low active (1.60), no height | 2,739 | 1,863 | — | **1,850** |

---

## 8. Discrepancy table

| Item | Original note | Verified value | Source | Action |
|---|---|---|---|---|
| Eq. 1 coefficients | Reconstructed: 1076 / 14.34 / 374.9 / 5.823 / 1070 / 104.6 / 0.4726 / −0.3529 / 24.78 / 1.865 / −19.66 / −713.1 | Identical (eq. 1 printed in full) | [2] | None. Change the note's status from "reconstructed" to "verified" and cite [2] |
| Coding of sex, athlete, HDI | Male 1; athlete 1; HDI 0 high / 1 mid / 2 low | Identical | [2] | None |
| Predictor: body weight or FFM | §1.4 says "fat-free mass/weight" | Eq. 1 uses body weight plus sex as an FFM proxy. Eq. 2 uses FFM (861.9 PAL, 37.34 FFM, no sex term, −984.8 intercept) | [2] | Clarify. Keep eq. 1 |
| PAL definition | Not stated | TEE ÷ Mifflin- (adults) or Schofield- (<18) predicted BEE | [2] | None. NASEM PAL values are compatible |
| Temperature input | "mean daily air temperature" | Mean air temperature over the measurement period | [2] | Specify the **24-h mean**, not the maximum, in code and UI |
| Ex 3 heat arithmetic | 22 °C term written as 352.7 | 470.1 (result +343 unchanged) | script | Fix the typo |
| Turnover → intake factor | 0.85 | 0.85 (first principles 0.83–0.86; consistent with measured intake) | [2][4][6] | Keep |
| Drinks share | 0.80 | 0.80 (NHANES 0.76–0.83; surveys likely overstate drinks) | [2][3][4] | Keep |
| 70 kg active man, 30 | 2,300 mL | 2,300 mL. No undercount: NASEM's 3.0 L reflects self-reported medians of heavier men | [3][4][6][8] | Keep |
| Age freeze | 35 | Age-curve vertex at 35.1 y | [2][4][9] | Keep |
| BMI-30 cap | Hard cap at BMI-30 weight | Soft cap: excess counted × 0.65 | [2][14] | **Correct** |
| Floors | 1,600 F / 2,000 M / 1,800 U / 1,840 preg / 2,160 lact | Same (0.8 × EFSA = ESPEN) | [5][9] | Keep |
| Ceiling | 4,500 adult / 4,000 teen | Same (product safety choice) | [4][5][12] | Keep |
| Workout add-on | 400 / 600 mL/h, +200 hot, cap 1,500 | Within the ACSM 0.4–0.8 L/h starting range | [10][12] | Keep |
| Heat add-on | 0.85 × Yamada T and RH terms above 15 °C, cap 1,000 | Coefficients verified. Effect may be overstated indoors in high-HDI countries | [2] | Keep. Clarify mean temperature |
| Altitude | 0.85 × 0.4726 per m above 1,500 m, cap 500 | Coefficient verified. Threshold and cap are judgment | [2] | Keep (low confidence) |
| Pregnancy / lactation | +300 / +700 | EFSA values verified as cited; Yamada +670 / +260 WT | [2][5] | Keep. Use pre-pregnancy weight |
| PAL categories | 1.53 / 1.68 / 1.85 cut-points; 1.40 / 1.60 / 1.75 / 2.05 values | Same; categories are DLW quartiles | [7] | Keep |
| Step bands → tier | <5k / 5–7.5k / 7.5–12.5k / ≥12.5k | Supported loosely (PAL 1.73 at ~10k steps; guideline ≈ 7.1–11k) | [11][15][16] | Keep. Add the iPhone-only rule and use the higher of the step and exercise-minute tiers |
| No-data default | Not specified (self-report as last resort) | Low active, PAL 1.60 | [5][7] | **Add** |
| Turnover measurement | Not discussed | rH₂O = k_D·N_D; dilution space and fractionation not corrected (a few % high) | [2][13] | Note only, no change |

---

## 9. Confidence

| Component | Confidence |
|---|---|
| Equation coefficients | High: verified from the primary source and every paper example reproduced |
| Turnover → intake (0.85) | Medium–high |
| Drinks share (0.80) | Medium: depends on diet; Yamada flags food water as unresolved [2] |
| Step → PAL mapping | Low–medium: steps explain PAL weakly [15] |
| BMI soft cap, iPhone-only rule, altitude threshold | Judgment calls, bounded by floors and ceiling |

---

## References

1. Yamada Y, Zhang X, Henderson MET, et al. Variation in human water turnover associated with environmental and lifestyle factors. *Science* 2022;378(6622):909–915. doi:10.1126/science.abm8668. https://www.science.org/doi/10.1126/science.abm8668 ; PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC9764345/
2. Same paper, authors' accepted manuscript (eq. 1, eq. 2, variable coding, worked examples, methods: rH₂O = k_D·N_D, PAL = TEE/predicted BEE, the 85% intake statement). UCL Discovery. https://discovery.ucl.ac.uk/id/eprint/10158948/1/Science_accepted.pdf
3. Drewnowski A, Rehm CD, Constant F. Water and beverage consumption among adults in the United States: cross-sectional study using data from NHANES 2005–2010. *BMC Public Health* 2013;13:1068. doi:10.1186/1471-2458-13-1068. https://pmc.ncbi.nlm.nih.gov/articles/PMC3840570/
4. Institute of Medicine. *Dietary Reference Intakes for Water, Potassium, Sodium, Chloride, and Sulfate.* National Academies Press; 2005. doi:10.17226/10925. https://nap.nationalacademies.org/catalog/10925
5. EFSA NDA Panel. Scientific Opinion on Dietary Reference Values for water. *EFSA Journal* 2010;8(3):1459. doi:10.2903/j.efsa.2010.1459. https://www.efsa.europa.eu/en/efsajournal/pub/1459
6. Raman A, Schoeller DA, Subar AF, et al. Water turnover in 458 American adults 40–79 yr of age. *Am J Physiol Renal Physiol* 2004;286(2):F394–F401. doi:10.1152/ajprenal.00295.2003. Summary of results: https://www.eurekalert.org/news-releases/483939
7. National Academies of Sciences, Engineering, and Medicine. *Dietary Reference Intakes for Energy.* National Academies Press; 2023. doi:10.17226/26818. PAL chapter: https://www.nationalacademies.org/read/26818/chapter/9 ; adult PAL cut-points also tabulated by Health Canada: https://www.canada.ca/en/health-canada/services/food-nutrition/healthy-eating/dietary-reference-intakes/tables/equations-estimate-energy-requirement.html
8. Ferreira-Pêgo C, Guelinckx I, Moreno LA, et al. Total fluid intake and its determinants: cross-sectional surveys among adults in 13 countries worldwide. *Eur J Nutr* 2015;54(Suppl 2):35–43. doi:10.1007/s00394-015-0943-9. https://pmc.ncbi.nlm.nih.gov/articles/PMC4472938/
9. Volkert D, Beck AM, Cederholm T, et al. ESPEN guideline on clinical nutrition and hydration in geriatrics. *Clin Nutr* 2019;38(1):10–47. doi:10.1016/j.clnu.2018.05.024. https://pubmed.ncbi.nlm.nih.gov/30005900/
10. American College of Sports Medicine; Sawka MN, et al. Exercise and fluid replacement (position stand). *Med Sci Sports Exerc* 2007;39(2):377–390. doi:10.1249/mss.0b013e31802ca597. https://pubmed.ncbi.nlm.nih.gov/17277604/
11. Tudor-Locke C, Bassett DR Jr. How many steps/day are enough? Preliminary pedometer indices for public health. *Sports Med* 2004;34(1):1–8. doi:10.2165/00007256-200434010-00001. https://pubmed.ncbi.nlm.nih.gov/14715035/
12. Hew-Butler T, Rosner MH, Fowkes-Godek S, et al. Statement of the Third International Exercise-Associated Hyponatremia Consensus Development Conference, Carlsbad, 2015. *Clin J Sport Med* 2015;25(4):303–320. https://pubmed.ncbi.nlm.nih.gov/26102445/
13. Speakman JR, Yamada Y, Sagayama H, et al. A standard calculation methodology for human doubly labeled water studies. *Cell Rep Med* 2021;2(2):100203. doi:10.1016/j.xcrm.2021.100203. https://research.tue.nl/en/publications/a-standard-calculation-methodology-for-human-doubly-labeled-water/
14. Heymsfield SB, Gonzalez MC, Shen W, Redman L, Thomas D. Weight loss composition is one-fourth fat-free mass: a critical review and critique of this widely cited rule. *Obes Rev* 2014;15(4):310–321. doi:10.1111/obr.12143. https://pubmed.ncbi.nlm.nih.gov/24447775/
15. Ohkawara K, Ishikawa-Takata K, Park JH, Tabata I, Tanaka S. How much locomotive activity is needed for an active physical activity level: analysis of total step counts. *BMC Res Notes* 2011;4:512. doi:10.1186/1756-0500-4-512. https://pmc.ncbi.nlm.nih.gov/articles/PMC3245484/
16. Tudor-Locke C, Craig CL, Brown WJ, et al. How many steps/day are enough? For adults. *Int J Behav Nutr Phys Act* 2011;8:79. doi:10.1186/1479-5868-8-79. https://ijbnpa.biomedcentral.com/articles/10.1186/1479-5868-8-79
17. Althoff T, Sosič R, Hicks JL, King AC, Delp SL, Leskovec J. Large-scale physical activity data reveal worldwide activity inequality. *Nature* 2017;547:336–339. doi:10.1038/nature23018. https://www.nature.com/articles/nature23018
