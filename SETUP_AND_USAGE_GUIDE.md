# Moneyball Football Scouting Tool - Setup & Usage Guide

## Overview

A production-grade Python tool for identifying undervalued, high-performing under-25 attackers in Europe's top 5 leagues (Premier League, La Liga, Serie A, Bundesliga, Ligue 1).

**Key Features:**
- ✓ Real FBref data collection with rate limiting
- ✓ Robust error handling & retry logic
- ✓ Feature engineering for scouting metrics
- ✓ Multiple data visualizations
- ✓ Detailed logging & reporting
- ✓ CSV export for further analysis

---

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Step 1: Install Required Packages

```bash
pip install pandas numpy matplotlib seaborn requests urllib3
```

### Step 2: Verify Installation

```bash
python -c "import pandas, matplotlib, seaborn; print('✓ All dependencies installed')"
```

### Step 3: Place the Script

Save `moneyball_football_scouting.py` in your working directory:

```bash
# Directory structure
your-project/
├── moneyball_football_scouting.py
└── README.md
```

---

## Quick Start (5 minutes)

### Run the Full Pipeline

```bash
python moneyball_football_scouting.py
```

**Expected Output:**
```
2026-05-19 10:30:45,123 - INFO - ================================================================================
2026-05-19 10:30:45,123 - INFO - MONEYBALL FOOTBALL SCOUTING TOOL - STARTING PIPELINE
2026-05-19 10:30:45,123 - INFO - ================================================================================

[PHASE 1] DATA COLLECTION
Successfully collected 2,847 rows of data.

[PHASE 2] DATA CLEANING
✓ Data cleaning complete. 2,411 rows remaining.

[PHASE 3] FEATURE ENGINEERING
✓ Features engineered. Total columns: 34

✓ Scouting pool created: 347 prospects identified

[PHASE 4] VISUALIZATION & REPORTING
Generating xG vs Finishing Efficiency plot...
✓ Plot saved to scouting_xg_finishing.png

MONEYBALL FOOTBALL SCOUTING REPORT
================================================================================
TOTAL PROSPECTS IDENTIFIED: 347
Average Age: 21.8 years
Average Game Time: 18.5 matches
...
```

**Generated Files:**
- `scouting_prospects.csv` - Complete prospect list
- `scouting_xg_finishing.png` - Visualization 1
- `scouting_shots_accuracy.png` - Visualization 2
- `scouting_tool.log` - Detailed logs

---

## Understanding the Scouting Framework

### The Four Prospect Quadrants

The main visualization plots **Chance Generation (xG/90)** vs **Finishing Efficiency**:

```
                    │ High xG/90
                    │
    OUTPERFORMERS   │  ELITE
    (Lucky Finish)  │  (Repeatable)
                    │
────────────────────┼────────────────────
                    │
    STRUGGLES       │  HIDDEN GEMS
    (Low Output)    │  (Buy-Low Targets)
                    │ Low xG/90
```

#### 🟢 **ELITE (Top Right)**
- High chance creation (xG/90) + Clinical finishing
- **Profile:** Already expensive; proven consistently
- **Action:** Monitor for market inefficiencies only

#### 🟡 **OUTPERFORMERS (Top Left)**
- Low chances but high finishing
- **Profile:** May be getting lucky; finishing regression risk
- **Action:** Verify sustainability; regression likely

#### 🟣 **HIDDEN GEMS (Bottom Right)**
- High chances but underperforming goals
- **Profile:** Strong positioning; temporary slump
- **Action:** PRIMARY BUY TARGETS — positioning repeats, finishing swings
- **Insight:** If a player gets into elite positions but scores below expected, they're likely undervalued

#### 🔴 **STRUGGLES (Bottom Left)**
- Low chances + poor finishing
- **Profile:** Development players or poor team fit
- **Action:** Skip (both metrics weak)

---

## Configuration & Customization

### Adjust Target Parameters

Edit these constants in the script (around line 31):

```python
TARGET_AGE_MAX = 25          # Maximum prospect age
MIN_PLAYING_TIME = 10.0       # Minimum 90-minute matches
REQUEST_DELAY = 3             # Seconds between API requests
TOP_5_LEAGUES = [...]         # Leagues to analyze
```

### Example: Scout Different Age Groups

```python
# Under-22 prospects only
prospects, _ = run_full_pipeline(SHOOTING_URL, PASSING_URL)
young_core = prospects[prospects['Age'] <= 22]

# Players 22-24 (peak value)
prime_age = prospects[(prospects['Age'] >= 22) & (prospects['Age'] <= 24)]
```

### Example: Filter by League

```python
# La Liga prospects only
la_liga_prospects = prospects[prospects['Squad'].str.contains('Real Madrid|Barcelona|Sevilla')]
```

### Example: Minimum Game Time Threshold

```python
# Players with at least 20 full matches
experienced = prospects[prospects['90s'] >= 20]
```

---

## Key Metrics Explained

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| **Goals/90** | Total Goals ÷ Matches (90s) | Raw goal-scoring rate |
| **xG/90** | Expected Goals ÷ Matches | Chance quality (contextual) |
| **npxG/90** | Non-Penalty xG ÷ Matches | xG excluding penalties |
| **Shot_Accuracy** | Shots on Target ÷ Total Shots | Shooting precision (%) |
| **Finishing_Efficiency** | (Goals - npxG) | Actual vs. Expected performance |
| **Shots_per_90** | Total Shots ÷ Matches | Volume of attempts |

**Pro Tips:**
- High **npxG_per_90** = Repeatable positioning skill
- High **Finishing_Efficiency** + Low **npxG** = Lucky or declining player
- High **Finishing_Efficiency** + High **npxG** = Elite prospect (likely already priced)
- Negative **Finishing_Efficiency** + High **npxG** = HIDDEN GEM (regression incoming)

---

## Error Handling & Troubleshooting

### Issue: "No data collected from FBref"

**Causes:**
- Network connectivity issue
- FBref website structure changed
- Rate limit exceeded

**Solutions:**
```bash
# 1. Check internet connection
ping fbref.com

# 2. Manually test FBref access
curl -I https://fbref.com

# 3. Increase retry attempts (edit line ~50)
MAX_RETRIES = 5  # Increase from 3

# 4. Increase delay between requests (line ~47)
REQUEST_DELAY = 5  # Increase from 3 seconds
```

### Issue: "Empty scouting pool (0 prospects)"

**Causes:**
- No players match age/playtime criteria
- Data collection succeeded but cleaning removed all rows

**Solutions:**
```python
# Relax filtering criteria
prospects = create_scouting_pool(df_engineered, age_max=27, min_90s=5)

# Check raw data
print(df_engineered.head(20))
print(df_engineered['Age'].describe())
print(df_engineered['90s'].describe())
```

### Issue: "Visualization won't display"

**Causes:**
- Matplotlib backend issue
- Missing data columns

**Solutions:**
```bash
# Force matplotlib to use non-interactive backend
export MPLBACKEND=Agg

# Or add to script top:
import matplotlib
matplotlib.use('Agg')
```

### Issue: "Rate limit exceeded / 429 error"

**Causes:**
- Too many rapid requests to FBref

**Solutions:**
```python
# Increase delay and retry strategy (lines 43-47)
REQUEST_DELAY = 5  # 5 seconds between requests
BACKOFF_FACTOR = 2.0  # Exponential backoff
```

---

## Advanced Usage: Custom Workflows

### Workflow 1: Identify Strikers with Best Finishing

```python
from moneyball_football_scouting import *

prospects, _ = run_full_pipeline(SHOOTING_URL, PASSING_URL)

# Top finishers (high efficiency, high volume)
finishers = prospects[
    (prospects['Finishing_Efficiency'] > 2) &
    (prospects['Shots_per_90'] > 3)
].sort_values('Goals_per_90', ascending=False)

print(finishers[['Player', 'Squad', 'Goals_per_90', 'Finishing_Efficiency']].head(10))
```

### Workflow 2: Defensive Metrics (if passing data added)

```python
# Complement with passing stats
prospects_passing = prospects[
    (prospects['xA_per_90'] > prospects['xA_per_90'].quantile(0.75))
]
print(f"Playmaking prospects: {len(prospects_passing)}")
```

### Workflow 3: League-by-League Comparison

```python
for league in ['PL', 'LaLiga', 'Serie A', 'Bundesliga', 'Ligue 1']:
    league_data = prospects[prospects['Comp'] == league]
    print(f"\n{league}:")
    print(f"  Prospects: {len(league_data)}")
    print(f"  Avg xG/90: {league_data['npxG_per_90'].mean():.2f}")
    print(f"  Avg Goals/90: {league_data['Goals_per_90'].mean():.2f}")
```

### Workflow 4: Export for Further Analysis

```python
# Save filtered subset to Excel
prospects.to_excel('hidden_gems.xlsx', index=False)

# Quick stats summary
print(prospects.describe())

# Correlation analysis
print(prospects[['npxG_per_90', 'Goals_per_90', 'Shot_Accuracy']].corr())
```

---

## Interpreting the Scouting Report

Sample output breakdown:

```
TOP 15 PROSPECTS (Overall Performance)
────────────────────────────────────────

1. João Felix (Atlético Madrid) - Age 20
   Playing Time: 24.3 matches | Shot Accuracy: 42.1%
   Goals/90: 0.68 | xG/90: 0.52
   Finishing Efficiency: ↑ OVERPERFORMING (+0.16)
   
   ➜ INTERPRETATION: Young elite prospect; clinical finisher
     with good positioning. Likely already expensive.

7. Rodrygo (Real Madrid) - Age 22
   Playing Time: 18.7 matches | Shot Accuracy: 38.5%
   Goals/90: 0.45 | xG/90: 0.62
   Finishing Efficiency: ↓ UNDERPERFORMING (-0.17)
   
   ➜ INTERPRETATION: HIDDEN GEM — Gets into elite positions
     (0.62 xG/90 is top tier) but finishing unlucky.
     Strong buy-low candidate as regression reverses.
```

---

## Data Interpretation Scenarios

### Scenario A: High xG/90, Positive Efficiency
- **Observation:** Player creates many chances AND finishes well
- **Verdict:** Elite performer (already expensive)
- **Action:** Monitor for injury/form changes

### Scenario B: High xG/90, Negative Efficiency
- **Observation:** Excellent positioning but missing chances
- **Verdict:** BEST BUYING OPPORTUNITY
- **Action:** Primary scouting target; finishing will regress positively

### Scenario C: Low xG/90, High Efficiency
- **Observation:** Few chances but converts them
- **Verdict:** Potentially unsustainable
- **Action:** Verify if actual elite finisher or temporarily lucky

### Scenario D: Low xG/90, Low Efficiency
- **Observation:** Few chances, poor conversion
- **Verdict:** Skip
- **Action:** Not ready for elite competition

---

## Performance Optimization

### For Large Datasets (10,000+ rows)

```python
# Use chunked processing
chunk_size = 500
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    chunk = engineer_features(chunk)
    # Process chunk...

# Use data types efficiently
df['Squad'] = df['Squad'].astype('category')  # Reduce memory
```

### Parallel Processing (Advanced)

```python
from multiprocessing import Pool

def process_league(league_url):
    return collect_shooting_stats(league_url)

with Pool(4) as p:
    results = p.map(process_league, [SHOOTING_URL, PASSING_URL])
```

---

## Output Files Reference

| File | Content | Use Case |
|------|---------|----------|
| `scouting_prospects.csv` | All 347+ prospects with metrics | Excel/BI tools |
| `scouting_xg_finishing.png` | Scatter plot (main chart) | Reports, presentations |
| `scouting_shots_accuracy.png` | Shot volume/accuracy chart | Shooting analysis |
| `scouting_tool.log` | Execution logs | Debugging, auditing |

---

## Next Steps & Enhancements

### Phase 2 Enhancements
- [ ] Integrate defensive metrics (tackles, interceptions)
- [ ] Add salary/transfer market data (Transfermarkt API)
- [ ] Compare across seasons for trend analysis
- [ ] Machine learning ranking (Random Forest feature importance)

### Integration Ideas
- Dashboard with Streamlit or Dash
- Automated weekly updates
- Slack/email alerts for breakout prospects
- Comparison to similar players (nearest neighbors)

---

## FAQ

**Q: Why only under-25?**
A: Peak trade value + long career ahead. Players 22-24 often represent best value; 25+ have more price inflation.

**Q: What's the "hidden gem" quadrant again?**
A: Bottom-right: High xG/90 (repeatable positioning) + Negative Finishing Efficiency (finishing underperformance). These revert positively as finishing regresses to mean.

**Q: Can I use other leagues (Serie A only, etc.)?**
A: Yes! Update FBref URLs to league-specific pages and adjust `TOP_5_LEAGUES` constant.

**Q: Why is my prospect list empty?**
A: Check age/playtime filters. Run with `age_max=27, min_90s=5` to relax constraints.

**Q: How often should I run this?**
A: Weekly (seasonally active) or monthly (more stable rankings).

---

## License & Attribution

Uses data from **FBref** (Sports Reference). Respect `robots.txt` and rate limits.
Inspired by "Moneyball" methodology applied to football analytics.

---

## Support & Updates

- Check logs in `scouting_tool.log` for errors
- Monitor FBref URL structure (may change seasonally)
- Test with small data samples before full pipeline
- Report data quality issues to FBref maintainers

Happy scouting! ⚽📊
