# Moneyball Football Scouting - Quick Reference

## The Four Prospect Quadrants

### 🟢 ELITE (Top Right)
**Profile:** High xG/90 + Positive Finishing Efficiency  
**What it means:** Excellent positioning AND clinical finishing  
**Examples:** Mbappé, Haaland, Kane (before 2024)  
**Scouting Action:** Already expensive; skip unless market anomaly  
**Probability of success:** Very High  

---

### 🟡 OUTPERFORMERS (Top Left)
**Profile:** Low xG/90 + Positive Finishing Efficiency  
**What it means:** Few chances, but scores anyway  
**Red flag:** Likely unsustainable; finishing regression coming  
**Examples:** Players in lucky purple patch  
**Scouting Action:** CAUTION — verify sustainability  
**Probability of success:** Medium (finishing regression risk)  

---

### 🟣 HIDDEN GEMS (Bottom Right) ⭐⭐⭐
**Profile:** High xG/90 + Negative Finishing Efficiency  
**What it means:** Gets into ELITE positions, underperforms goals  
**Why it matters:** Positioning repeats; finishing is cyclical  
**Examples:** Vinicius Jr (early 2023), Rodrygo (certain periods)  
**Scouting Action:** PRIMARY BUY TARGET  
**Probability of success:** Very High  
**Key insight:** When xG/90 is elite (>0.5) and finishing is negative,  
this is one of the highest-conviction value plays in football analytics.

---

### 🔴 STRUGGLES (Bottom Left)
**Profile:** Low xG/90 + Negative Finishing Efficiency  
**What it means:** Few chances AND poor conversion  
**Examples:** Young/struggling forwards  
**Scouting Action:** Skip (both metrics weak)  
**Probability of success:** Low  

---

## Metric Definitions & Thresholds

| Metric | Calculation | Low | Medium | High | Usage |
|--------|-------------|-----|--------|------|-------|
| **Goals/90** | Total Goals ÷ Matches | <0.3 | 0.3–0.6 | >0.6 | Raw output |
| **xG/90** | Exp. Goals ÷ Matches | <0.3 | 0.3–0.5 | >0.5 | Positioning skill |
| **npxG/90** | Non-Pen xG ÷ Matches | <0.25 | 0.25–0.45 | >0.45 | Elite positioning |
| **Shot_Accuracy** | SoT ÷ Total Shots | <0.35 | 0.35–0.45 | >0.45 | Shot quality |
| **Shots_per_90** | Total Shots ÷ Matches | <2.5 | 2.5–3.5 | >3.5 | Volume/activity |
| **Fin. Efficiency** | (Gls - npxG) | <-0.5 | -0.5 to +0.5 | >+0.5 | Over/underperformance |

**Thresholds for Under-25 Prospects:**
- **Elite Chance Creator:** npxG/90 > 0.5
- **High-Volume Shooter:** Shots/90 > 3.5
- **Accurate Finisher:** Shot_Accuracy > 45%
- **Underperforming:** Finishing_Efficiency < -0.3
- **Outperforming:** Finishing_Efficiency > +0.3

---

## The Hidden Gem Decision Tree

```
START: Looking at prospect data
│
├─ Is Age <= 25? 
│  ├─ NO → STOP (not target age)
│  └─ YES → Continue
│
├─ Is Playing Time >= 10 matches (90s)?
│  ├─ NO → STOP (insufficient data)
│  └─ YES → Continue
│
├─ Is npxG/90 > 0.5? (Top 25% chance creation)
│  ├─ NO → Likely STRUGGLES or OUTPERFORMERS
│  └─ YES → Continue (strong positioning)
│
├─ Is Finishing_Efficiency < 0? (Underperforming)
│  ├─ NO → Not a hidden gem
│  └─ YES → ✅ HIDDEN GEM IDENTIFIED
│
└─ FINAL CHECK: Is margin < -0.5?
   └─ The larger the negative margin, the stronger the buy signal
      because regression to mean is more pronounced
```

---

## Scouting Signal Strength (Ranked)

### 🔴 Very Strong Buy Signal
- **Criteria:** npxG/90 > 0.55 + Finishing_Efficiency < -0.4
- **Conviction:** 95%+
- **Action:** High priority monitoring
- **Timeline:** 6–12 months (finishing regression)

### 🟠 Strong Buy Signal
- **Criteria:** npxG/90 > 0.45 + Finishing_Efficiency < -0.2
- **Conviction:** 85%+
- **Action:** Add to shortlist
- **Timeline:** Next 6 months

### 🟡 Moderate Buy Signal
- **Criteria:** npxG/90 > 0.4 + Finishing_Efficiency < 0
- **Conviction:** 70%+
- **Action:** Monitor for 2–3 matches
- **Timeline:** Verify consistency

### 🟢 Weak Signal
- **Criteria:** npxG/90 > 0.3 + Finishing_Efficiency near 0
- **Conviction:** 50–60%
- **Action:** Lower priority
- **Timeline:** Requires multi-season analysis

---

## Common Prospect Types & Handling

### Type 1: The Emerging Talent
**Profile:** Age 19–21, high xG/90, inconsistent finishing  
**What to do:** Track over 2–3 seasons; potential elite finisher  
**Red flag:** If xG/90 drops, positioning skill may decline  

---

### Type 2: The Established Hidden Gem
**Profile:** Age 22–24, consistent high xG/90, recent negative efficiency  
**What to do:** PRIMARY BUY — high conviction; short regression timeline  
**Confidence:** Very High (positioning repeatable, finishing will improve)  

---

### Type 3: The Aging Outlier
**Profile:** Age 25–26, high metrics, but aging curve approaching  
**What to do:** Buy if margin is large; shorter window than younger players  
**Caution:** Regression may be age-related, not just finishing luck  

---

### Type 4: The League Anomaly
**Profile:** Dominant in lower league, struggling in top league  
**What to do:** Likely adaptation phase; give 2–3 seasons  
**Caution:** May not adapt; high variance outcome  

---

## Quick Prospect Evaluation Checklist

When you identify a prospect, use this checklist:

- [ ] **Age:** 20–24? (Sweet spot for value)
- [ ] **Playing Time:** >12 matches? (Sufficient sample)
- [ ] **xG/90:** >0.4? (Positioning skill present)
- [ ] **Finishing Gap:** < -0.3? (Margin for regression)
- [ ] **Shot Accuracy:** Reasonable (>35%)? (Technical competence)
- [ ] **Team Context:** Mid-table or better? (Not inflated stats)
- [ ] **Injury History:** Clean? (Availability risk)
- [ ] **Consistency:** Improving or stable? (Not declining)

**Scoring:**
- 8/8 checks: Elite buy signal
- 7/8 checks: Strong buy signal
- 6/8 checks: Consider, but monitor
- <6/8: Skip or revisit later

---

## Real-World Examples

### Example 1: The Hidden Gem in Action
**Player:** Young RW, Age 23  
**Stats:**
- Goals/90: 0.38
- xG/90: 0.52 (Top 10%)
- Finishing_Efficiency: -0.14 (underperforming)
- Shots_per_90: 3.2
- Shot_Accuracy: 41%

**Analysis:**
✓ Consistently gets into elite positions (0.52 xG/90)  
✓ Moderate underperformance (-0.14) suggests temporary slump  
✓ Shot accuracy (41%) is reasonable; technical skill present  
✓ No obvious red flags  

**Scouting Verdict:** STRONG BUY  
**Reasoning:** Positioning repeats; finishing reverts. Likely to add 3–5 goals next season.

---

### Example 2: The Outperformer (Caution)
**Player:** Forward, Age 22  
**Stats:**
- Goals/90: 0.71 (Elite)
- xG/90: 0.28 (Below average)
- Finishing_Efficiency: +0.43 (ELITE overperformance)
- Shots_per_90: 2.1
- Shot_Accuracy: 48%

**Analysis:**
⚠️ Massive overperformance (+0.43)  
⚠️ Low xG/90 means few chances  
⚠️ If overperformance regresses, goals drop significantly  

**Scouting Verdict:** CAUTION / MONITOR  
**Reasoning:** Likely lucky streak. Regression risk high. Verify over next 5–10 matches.

---

### Example 3: The Elite (Already Expensive)
**Player:** Striker, Age 23  
**Stats:**
- Goals/90: 0.68
- xG/90: 0.61 (Top 5%)
- Finishing_Efficiency: +0.07 (slight overperformance)
- Shots_per_90: 4.1
- Shot_Accuracy: 46%

**Analysis:**
✓ Elite positioning (0.61 xG/90)  
✓ Consistent finishing (slight overperformance = repeatable)  
✓ High volume and accuracy  

**Scouting Verdict:** ELITE (but likely priced accordingly)  
**Reasoning:** Both metrics elite; no hidden gem opportunity. Already on radar of major clubs.

---

## Data Quality Checks

Before trusting a prospect profile, verify:

1. **Sample Size:** >10 full matches played
2. **League Tier:** Top 5 European leagues only
3. **Recency:** Data from current season
4. **Competition:** Exclude cup competitions (distorted metrics)
5. **Outliers:** Verify extreme metrics aren't one-match anomalies

---

## Seasonal Adjustments

**Early Season (Matches 1–8):** High variance; wait for stabilization  
**Mid-Season (Matches 9–20):** Most reliable data; use for decisions  
**Late Season (Matches 21+):** Apply fatigue consideration; monitor form  

---

## The Moneyball Advantage

**Traditional Scouting:** "That player looks good on film"  
→ Subjective, expensive (scouts worldwide), slow  

**Analytics Scouting:** "High xG/90 + negative finishing = regression opportunity"  
→ Objective, scalable (script runs globally), actionable  

**The Gap:** Best players identified late in season → wait for late-summer availability → buy at discount

---

## Key Takeaways

1. **Find High xG/90 Players** = Superior positioning (repeatable skill)
2. **Find Negative Finishing_Efficiency** = Underperforming (temporary)
3. **Combine Both** = Hidden gem with high regression probability
4. **Age 22–24** = Sweet spot (young + proven)
5. **>0.5 npxG/90 + < -0.3 Efficiency** = Strongest signal

---

## Template: Personal Prospect Tracker

```
PROSPECT ANALYSIS TEMPLATE
═══════════════════════════════════════════

Name: ________________
Club: ________________
Age: ___ | Position: _____ | League: _____

METRICS:
├─ npxG/90: _____ (Target: >0.45)
├─ Goals/90: _____ (Actual output)
├─ Finishing_Efficiency: _____ (Target: < -0.2)
├─ Shot_Accuracy: _____ (Target: >40%)
└─ Shots_per_90: _____ (Activity level)

QUADRANT: [ ] Elite [ ] Outperformer [ ] Hidden Gem [ ] Struggles

CONVICTION SCORE: ___/10

NEXT ACTION:
[ ] Monitor next 5 matches
[ ] Add to priority shortlist
[ ] Deep dive film review
[ ] Contact club

NOTES:
```

---

**Generated by Moneyball Football Scouting Tool v1.0**
