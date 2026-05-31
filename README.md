# Vibe-Coded-Football-Data-Science-Project
# ⚽ Moneyball Football Scouting Tool

A production-grade Python analytics tool for identifying undervalued, high-performing under-25 attackers in Europe's top 5 leagues using the "Moneyball" approach. Scrapes data from FBref, engineers scouting metrics, and visualizes hidden gem prospects.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

## 🎯 Overview

This tool analyzes football player statistics to find **hidden gems** — young attackers who get into elite positions (high xG/90) but underperform their expected goals. When finishing regresses to the mean, these players significantly increase in value.

**Key Insight:** While traditional scouts look for established talents (expensive), this tool finds repeatable positioning ability + temporary finishing underperformance = high-conviction buy signals.

## 🔍 The Four Prospect Quadrants

```
                    │ High xG/90
                    │
    OUTPERFORMERS   │  ELITE ⭐
    (Lucky Finish)  │  (Repeatable)
                    │
────────────────────┼────────────────────
                    │
    STRUGGLES       │  HIDDEN GEMS ⭐⭐⭐
    (Low Output)    │  (Best Buy Signal)
                    │ Low xG/90
```

- **🟢 ELITE:** High chance creation + clinical finishing (already expensive)
- **🟡 OUTPERFORMERS:** Few chances but high finishing (regression risk)
- **🟣 HIDDEN GEMS:** High chances but underperforming (PRIMARY TARGET)
- **🔴 STRUGGLES:** Low chances + poor finishing (skip)

## ✨ Features

- ✅ **Real Data Collection** — Scrapes FBref with rate limiting & error handling
- ✅ **Smart Fallback** — Uses sample data if FBref blocks (continues pipeline)
- ✅ **Data Cleaning** — Removes headers, handles NaN, validates types
- ✅ **Feature Engineering** — 7+ custom metrics (npxG/90, Finishing_Efficiency, etc.)
- ✅ **Dual Visualizations** — xG vs finishing + shot volume/accuracy plots
- ✅ **Detailed Reporting** — Console output + CSV export + logging
- ✅ **Configurable** — Adjust age, playtime, league filters easily
- ✅ **Production-Ready** — Retry logic, rate limiting, comprehensive error handling

## 📊 Metrics Calculated

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| **Goals/90** | Total Goals ÷ Matches | Raw output rate |
| **npxG/90** | Non-Penalty xG ÷ Matches | Chance quality (repeatable) |
| **Shot_Accuracy** | Shots on Target ÷ Total Shots | Precision % |
| **Finishing_Efficiency** | (Goals - npxG) | Over/underperformance |
| **Shots_per_90** | Total Shots ÷ Matches | Activity level |

## 🚀 Quick Start

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/moneyball-football-scouting.git
cd moneyball-football-scouting

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the pipeline
python moneyball_football_scouting.py
```

### Output Files

```
scouting_prospects.csv              # All prospects with metrics
scouting_xg_finishing.png           # Main visualization (quadrant plot)
scouting_shots_accuracy.png         # Secondary visualization
scouting_tool.log                   # Detailed execution logs
```

## 📖 Usage

### Basic Pipeline

```python
from moneyball_football_scouting import run_full_pipeline

prospects, all_data = run_full_pipeline(
    shooting_url="https://fbref.com/en/comps/Big5/shooting/players/...",
    passing_url="https://fbref.com/en/comps/Big5/passing/players/..."
)

# View prospects
print(prospects[['Player', 'Squad', 'npxG_per_90', 'Finishing_Efficiency']].head(10))
```

### Filter for Hidden Gems

```python
hidden_gems = prospects[
    (prospects['npxG_per_90'] > 0.45) &
    (prospects['Finishing_Efficiency'] < -0.2) &
    (prospects['Age'] <= 24)
].sort_values('npxG_per_90', ascending=False)

print(hidden_gems[['Player', 'Squad', 'Age', 'npxG_per_90', 'Finishing_Efficiency']])
```

### League-Specific Analysis

```python
la_liga = prospects[prospects['Comp'] == 'La Liga']
print(f"La Liga prospects: {len(la_liga)}")
print(f"Average xG/90: {la_liga['npxG_per_90'].mean():.2f}")
```

### Export for External Tools

```python
# Save to Excel
prospects.to_excel('hidden_gems_analysis.xlsx', index=False)

# Summary statistics
print(prospects.describe())
```

## 🔧 Configuration

Edit constants in `moneyball_football_scouting.py` (lines 38-42):

```python
TARGET_AGE_MAX = 25          # Maximum prospect age
MIN_PLAYING_TIME = 10.0      # Minimum 90-minute matches
REQUEST_DELAY = 5            # Seconds between FBref requests
BACKOFF_FACTOR = 2.0         # Exponential backoff for retries
```

## 📚 Project Structure

```
moneyball-football-scouting/
├── moneyball_football_scouting.py       # Main script (all 4 phases)
├── SETUP_AND_USAGE_GUIDE.md             # Comprehensive guide
├── SCOUTING_QUADRANT_REFERENCE.md       # Decision framework
├── requirements.txt                      # Dependencies
├── .gitignore                           # Git ignore rules
├── README.md                            # This file
└── example_output/
    ├── scouting_prospects.csv           # Sample output
    ├── scouting_xg_finishing.png        # Sample visualization
    └── scouting_shots_accuracy.png      # Sample visualization
```

## 🎓 Understanding the Framework

### The Hidden Gem Signal

**Profile:** Age 22–24, high xG/90 (>0.5), negative Finishing_Efficiency (<-0.2)

**Why it works:**
- **Positioning is repeatable** — xG/90 reflects player's ability to get into elite positions
- **Finishing is cyclical** — Goal-scoring luck regresses to the mean
- **Both are young** — Long career ahead; finishing regression = significant value increase

**Timeline:** 6–12 months for finishing to normalize (3–5 additional goals/season)

### Real-World Example

| Metric | Player A | Player B |
|--------|----------|----------|
| Age | 23 | 23 |
| Goals/90 | 0.38 | 0.71 |
| xG/90 | 0.52 | 0.28 |
| Finishing_Eff | -0.14 | +0.43 |
| **Verdict** | 🟣 HIDDEN GEM | 🟡 CAUTION |
| **Action** | BUY | MONITOR |

**Reasoning:** Player A gets into elite positions but is temporarily unlucky. Player B is lucky and likely to regress.

## ⚙️ How It Works

### Phase 1: Data Collection
- Scrapes FBref using `pd.read_html()`
- Rate limits to 20 requests/minute (respects robots.txt)
- Fallback to sample data if FBref blocks

### Phase 2: Data Cleaning
- Removes duplicate header rows
- Handles missing values intelligently
- Converts columns to appropriate numeric types
- Removes outliers & footnotes

### Phase 3: Feature Engineering
- Normalizes stats to per-90-minute basis
- Creates efficiency metrics
- Calculates over/underperformance
- Filters for target age/playtime

### Phase 4: Visualization & Reporting
- Scatter plots with quadrant annotations
- Highlights top prospects by name
- Generates console scouting report
- Exports CSV for further analysis

## 🛠️ Troubleshooting

### "403 Forbidden" Error

FBref is blocking repeated requests from your IP.

**Solutions:**
```bash
# Option 1: Wait 10-15 minutes and retry
python moneyball_football_scouting.py

# Option 2: Use a VPN to get new IP
# (VPN tools vary by OS)

# Option 3: Script auto-loads sample data
# (run with --sample flag or wait for fallback)
```

### "No module named 'X'" Errors

```bash
# Reinstall all dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Empty Scouting Pool

Relax filtering criteria:

```python
# Instead of default age/playtime
prospects = create_scouting_pool(df_engineered, age_max=27, min_90s=5)
```

## 📦 Dependencies

- **pandas** — Data manipulation & HTML parsing
- **numpy** — Numerical computations
- **matplotlib** — Visualization
- **seaborn** — Statistical plotting
- **requests** — HTTP requests
- **urllib3** — Retry logic
- **lxml** — HTML/XML parsing

See `requirements.txt` for versions.

## 🔄 Workflow Recommendations

### Weekly Analysis
```bash
# Run every Monday to capture weekend matches
python moneyball_football_scouting.py

# Review emerging hidden gems
cat scouting_prospects.csv | grep "Hidden Gem"
```

### Seasonal Tracking
```bash
# Compare prospects across the season
# Store outputs with timestamps: scouting_prospects_2026_05_19.csv
```

### League-Specific Deep Dives
```python
# Focus on one league
bundesliga = prospects[prospects['Comp'] == 'Bundesliga']
bundesliga.to_csv('bundesliga_prospects.csv')
```

## 💡 Advanced Use Cases

- **Compare to market data** — Merge with Transfermarkt salary data
- **Machine learning ranking** — Train model on career outcomes
- **Time-series analysis** — Track prospect progression over season
- **Similar player finder** — KNN clustering by metrics
- **Automated alerts** — Slack/email notifications for breakout prospects

## 📊 Example Output

```
MONEYBALL FOOTBALL SCOUTING REPORT
================================================================================
TOTAL PROSPECTS IDENTIFIED: 347
Average Age: 21.8 years
Average Game Time: 18.5 matches

TOP 15 PROSPECTS (Overall Performance)
────────────────────────────────────────

1. João Félix (Atlético Madrid) - Age 23
   Playing Time: 24.3 matches | Shot Accuracy: 42.1%
   Goals/90: 0.68 | xG/90: 0.52
   Finishing Efficiency: ↑ OVERPERFORMING (+0.16)

7. Rodrygo (Real Madrid) - Age 22
   Playing Time: 18.7 matches | Shot Accuracy: 38.5%
   Goals/90: 0.45 | xG/90: 0.62
   Finishing Efficiency: ↓ UNDERPERFORMING (-0.17)
   💡 INSIGHT: High positioning ability; finishing regression likely
```

## 🎬 Getting Started Tips

1. **Start with sample data** — Test pipeline locally without FBref delays
2. **Review quadrant reference** — Understand the 4 prospect types
3. **Explore the CSV** — Open `scouting_prospects.csv` in Excel
4. **Modify filters** — Try different age/playtime combinations
5. **Deep dive prospects** — Use names from output for film review

## 📄 License

MIT License — See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Ideas:
- [ ] Add defensive metrics
- [ ] Integrate Transfermarkt salary data
- [ ] Machine learning ranking model
- [ ] Streamlit/Dash dashboard
- [ ] Multi-season trend analysis
- [ ] API integration for live data

## 📞 Support

- Check `SETUP_AND_USAGE_GUIDE.md` for detailed troubleshooting
- Review `SCOUTING_QUADRANT_REFERENCE.md` for metric explanations
- Check logs in `scouting_tool.log` for debugging

## 🙏 Acknowledgments

- **Data:** FBref (Sports Reference)
- **Methodology:** Inspired by "Moneyball" (Sabermetrics approach)
- **Community:** Football analytics community for insights

---

**Made with ⚽ by Football Analytics Enthusiasts**

*Moneyball Football Scouting Tool v1.0*
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/moneyball-football-scouting)
