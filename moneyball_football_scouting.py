"""
Moneyball Football Scouting Tool
Identify high-performing, undervalued under-25 attackers in Europe's top leagues.

Tech Stack: Python (pandas, requests, BeautifulSoup, seaborn, matplotlib)
Author: Football Analytics
Date: 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import logging
from typing import Tuple, Optional
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ============================================================================
# SETUP & CONFIGURATION
# ============================================================================

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scouting_tool.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# FBref rate limiting: 20 requests per minute (respect robots.txt)
REQUEST_DELAY = 3  # seconds between requests
MAX_RETRIES = 3
BACKOFF_FACTOR = 1.5

# Target parameters
TARGET_AGE_MAX = 25
MIN_PLAYING_TIME = 10.0  # 90s minutes
TOP_5_LEAGUES = ['PL', 'LaLiga', 'Serie A', 'Bundesliga', 'Ligue 1']

# ============================================================================
# PHASE 1: DATA COLLECTION WITH ERROR HANDLING
# ============================================================================

def create_session_with_retries() -> requests.Session:
    """
    Create a requests session with retry logic and rate limiting.
    Handles temporary failures gracefully.
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    return session


def collect_shooting_stats(url: str) -> Optional[pd.DataFrame]:
    """
    Collect shooting statistics from FBref.
    
    Args:
        url: FBref shooting stats URL
        
    Returns:
        DataFrame with raw shooting data or None if collection fails
    """
    logger.info(f"Attempting to collect data from {url}")
    
    try:
        # Respect rate limiting
        time.sleep(REQUEST_DELAY)
        
        # Read HTML tables
        tables = pd.read_html(url, header=1)
        df_raw = tables[0]
        
        logger.info(f"✓ Successfully collected {df_raw.shape[0]} rows, {df_raw.shape[1]} columns")
        return df_raw
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during data collection: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error collecting data: {e}")
        return None


def collect_passing_stats(url: str) -> Optional[pd.DataFrame]:
    """
    Collect passing statistics from FBref.
    
    Args:
        url: FBref passing stats URL
        
    Returns:
        DataFrame with raw passing data or None if collection fails
    """
    logger.info(f"Attempting to collect passing data from {url}")
    
    try:
        time.sleep(REQUEST_DELAY)
        tables = pd.read_html(url, header=1)
        df_raw = tables[0]
        
        logger.info(f"✓ Successfully collected {df_raw.shape[0]} rows of passing data")
        return df_raw
        
    except Exception as e:
        logger.error(f"Error collecting passing data: {e}")
        return None


# ============================================================================
# PHASE 2: DATA CLEANING
# ============================================================================

def clean_football_data(df: pd.DataFrame, data_type: str = 'shooting') -> pd.DataFrame:
    """
    Clean raw football data from FBref.
    
    Args:
        df: Raw DataFrame from FBref
        data_type: 'shooting' or 'passing' to handle different column structures
        
    Returns:
        Cleaned DataFrame
    """
    logger.info(f"Starting data cleaning for {data_type} data...")
    
    try:
        df = df.copy()
        
        # 1. Remove duplicate header rows
        if 'Player' in df.columns:
            df = df[df['Player'] != 'Player']
        
        # 2. Drop rows with missing critical values
        critical_cols = ['Player', 'Age', 'Squad']
        for col in critical_cols:
            if col in df.columns:
                df = df[df[col].notna()]
        
        # 3. Clean Age column (FBref format: 'YY-DDD')
        if 'Age' in df.columns:
            df['Age'] = df['Age'].astype(str).str.split('-').str[0]
            df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
        
        # 4. Handle 90s (minutes played / 90)
        if '90s' in df.columns:
            df['90s'] = pd.to_numeric(df['90s'], errors='coerce')
        
        # 5. Convert numeric columns
        numeric_cols = [
            'Age', '90s', 'Gls', 'Sh', 'SoT', 'Dist', 'PK', 'xG', 'npxG',
            'Cmp', 'Att', 'Cmp%', 'PrgP', 'KP', 'xAG', 'xA'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 6. Fill NaN numeric values with 0
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        
        # 7. Remove rows with no Squad info (often footnotes)
        df = df[df['Squad'].notna()].copy()
        
        logger.info(f"✓ Data cleaning complete. {df.shape[0]} rows remaining.")
        return df
        
    except Exception as e:
        logger.error(f"Error during data cleaning: {e}")
        return pd.DataFrame()


# ============================================================================
# PHASE 3: FEATURE ENGINEERING & SCOUTING POOL
# ============================================================================

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create custom performance metrics for scouting analysis.
    
    Metrics created:
    - Shot_Accuracy: % of shots on target
    - Finishing_Efficiency: Actual goals - expected goals (over/underperformance)
    - Shots_per_90: Volume of shooting opportunities
    - npxG_per_90: Quality of chance creation
    - Goals_per_90: Raw goal-scoring rate
    - xA_per_90: Assists expected per 90
    
    Args:
        df: Cleaned DataFrame
        
    Returns:
        DataFrame with engineered features
    """
    logger.info("Engineering features...")
    
    try:
        df = df.copy()
        
        # Shot Accuracy (Shots on Target / Total Shots)
        if 'SoT' in df.columns and 'Sh' in df.columns:
            df['Shot_Accuracy'] = (df['SoT'] / df['Sh']).fillna(0)
            df['Shot_Accuracy'] = df['Shot_Accuracy'].clip(0, 1)  # Ensure 0-1 range
        
        # Finishing Efficiency: (Goals - PK) - npxG
        # Positive = outperforming expected; Negative = underperforming
        if 'Gls' in df.columns and 'npxG' in df.columns:
            pens = df['PK'].fillna(0)
            df['Finishing_Efficiency'] = (df['Gls'] - pens) - df['npxG']
        
        # Per-90 stats (normalize for playing time)
        if '90s' in df.columns:
            if 'Sh' in df.columns:
                df['Shots_per_90'] = (df['Sh'] / df['90s']).fillna(0)
            
            if 'npxG' in df.columns:
                df['npxG_per_90'] = (df['npxG'] / df['90s']).fillna(0)
            
            if 'Gls' in df.columns:
                df['Goals_per_90'] = (df['Gls'] / df['90s']).fillna(0)
            
            if 'xA' in df.columns:
                df['xA_per_90'] = (df['xA'] / df['90s']).fillna(0)
        
        # Pass completion % (already in data, but ensure numeric)
        if 'Cmp%' in df.columns:
            df['Cmp%'] = pd.to_numeric(df['Cmp%'], errors='coerce').fillna(0)
        
        logger.info(f"✓ Features engineered. Total columns: {df.shape[1]}")
        return df
        
    except Exception as e:
        logger.error(f"Error during feature engineering: {e}")
        return df


def create_scouting_pool(df: pd.DataFrame, 
                        age_max: int = TARGET_AGE_MAX,
                        min_90s: float = MIN_PLAYING_TIME) -> pd.DataFrame:
    """
    Filter for target scouting group: young players with substantial game time.
    
    Args:
        df: Engineered features DataFrame
        age_max: Maximum age (default 25)
        min_90s: Minimum 90-minute matches played
        
    Returns:
        Filtered DataFrame of prospects
    """
    logger.info(f"Creating scouting pool (Age <= {age_max}, 90s >= {min_90s})...")
    
    try:
        pool = df[
            (df['Age'] <= age_max) & 
            (df['90s'] >= min_90s)
        ].copy()
        
        # Sort by potential (npxG_per_90 + Goals_per_90)
        if 'npxG_per_90' in pool.columns and 'Goals_per_90' in pool.columns:
            pool['Combined_Score'] = pool['npxG_per_90'] + pool['Goals_per_90']
            pool = pool.sort_values('Combined_Score', ascending=False)
        
        logger.info(f"✓ Scouting pool created: {pool.shape[0]} prospects identified")
        return pool
        
    except Exception as e:
        logger.error(f"Error creating scouting pool: {e}")
        return pd.DataFrame()


# ============================================================================
# PHASE 4: DATA VISUALIZATION
# ============================================================================

def plot_xg_vs_finishing(scouting_pool: pd.DataFrame, output_path: str = None) -> None:
    """
    Scatter plot: Expected Goals Generation vs Finishing Efficiency
    
    Identifies four types of prospects:
    - Top Right: Elite (high xG + clinical finishing)
    - Top Left: Outperformers (lucky finishers)
    - Bottom Right: Hidden Gems (underperforming but repeatable positioning)
    - Bottom Left: Struggles (low chance creation + poor finishing)
    
    Args:
        scouting_pool: Filtered prospect DataFrame
        output_path: Optional file path to save plot
    """
    logger.info("Generating xG vs Finishing Efficiency plot...")
    
    try:
        if 'npxG_per_90' not in scouting_pool.columns or 'Finishing_Efficiency' not in scouting_pool.columns:
            logger.warning("Required columns missing for visualization")
            return
        
        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=(14, 9))
        
        # Main scatter plot
        scatter = sns.scatterplot(
            data=scouting_pool,
            x='npxG_per_90',
            y='Finishing_Efficiency',
            hue='Squad',
            size='90s',
            sizes=(60, 400),
            alpha=0.6,
            ax=ax
        )
        
        # Identify top outliers for annotation
        xg_threshold = scouting_pool['npxG_per_90'].quantile(0.85)
        eff_threshold = scouting_pool['Finishing_Efficiency'].quantile(0.85)
        
        top_prospects = scouting_pool[
            (scouting_pool['npxG_per_90'] > xg_threshold) | 
            (scouting_pool['Finishing_Efficiency'] > eff_threshold)
        ]
        
        # Annotate top 10 prospects
        for idx, (_, row) in enumerate(top_prospects.head(10).iterrows()):
            ax.annotate(
                row['Player'],
                xy=(row['npxG_per_90'], row['Finishing_Efficiency']),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=9,
                weight='semibold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=1)
            )
        
        # Add reference lines
        ax.axhline(0, color='red', linestyle='--', alpha=0.4, linewidth=2, label='Average Finishing')
        median_xg = scouting_pool['npxG_per_90'].median()
        ax.axvline(median_xg, color='blue', linestyle='--', alpha=0.4, linewidth=2, label='Median xG/90')
        
        # Labels and title
        ax.set_xlabel('Non-Penalty xG per 90 (Chance Quality)', fontsize=13, weight='semibold')
        ax.set_ylabel('Finishing Efficiency (Goals - npxG)', fontsize=13, weight='semibold')
        ax.set_title(
            'Moneyball Scout: Under-25 Attackers\nChance Generation vs. Finishing Efficiency',
            fontsize=15,
            weight='bold',
            pad=20
        )
        
        # Add quadrant annotations
        ax.text(0.98, 0.98, 'ELITE\n(High xG + Efficient)', 
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='green', alpha=0.2))
        ax.text(0.02, 0.98, 'OUTPERFORMERS\n(Lucky Finishers)', 
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='orange', alpha=0.2))
        ax.text(0.98, 0.02, 'HIDDEN GEMS\n(Underperforming)', 
                transform=ax.transAxes, fontsize=10, verticalalignment='bottom',
                horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='purple', alpha=0.2))
        
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        plt.tight_layout()
        
        # Save if path provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Plot saved to {output_path}")
        
        plt.show()
        
    except Exception as e:
        logger.error(f"Error generating plot: {e}")


def plot_shot_volume_vs_accuracy(scouting_pool: pd.DataFrame, output_path: str = None) -> None:
    """
    Scatter plot: Shot Volume vs Accuracy
    
    Identifies efficient shooters and high-volume finishers.
    
    Args:
        scouting_pool: Filtered prospect DataFrame
        output_path: Optional file path to save plot
    """
    logger.info("Generating Shot Volume vs Accuracy plot...")
    
    try:
        if 'Shots_per_90' not in scouting_pool.columns or 'Shot_Accuracy' not in scouting_pool.columns:
            logger.warning("Required columns missing for shot analysis")
            return
        
        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=(14, 9))
        
        scatter = sns.scatterplot(
            data=scouting_pool,
            x='Shots_per_90',
            y='Shot_Accuracy',
            hue='Squad',
            size='Goals_per_90' if 'Goals_per_90' in scouting_pool.columns else '90s',
            sizes=(60, 400),
            alpha=0.6,
            ax=ax
        )
        
        # Annotate top shooters
        top_volume = scouting_pool[
            scouting_pool['Shots_per_90'] > scouting_pool['Shots_per_90'].quantile(0.90)
        ]
        
        for _, row in top_volume.head(8).iterrows():
            ax.annotate(
                row['Player'],
                xy=(row['Shots_per_90'], row['Shot_Accuracy']),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=9,
                weight='semibold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.3),
            )
        
        # Reference lines
        median_shots = scouting_pool['Shots_per_90'].median()
        median_accuracy = scouting_pool['Shot_Accuracy'].median()
        ax.axvline(median_shots, color='blue', linestyle='--', alpha=0.4, label='Median Shots/90')
        ax.axhline(median_accuracy, color='orange', linestyle='--', alpha=0.4, label='Median Accuracy')
        
        ax.set_xlabel('Shots per 90 Minutes (Volume)', fontsize=13, weight='semibold')
        ax.set_ylabel('Shot Accuracy (SoT / Total Shots)', fontsize=13, weight='semibold')
        ax.set_title(
            'Shooting Efficiency Profile: Young Attackers\nVolume vs. Precision',
            fontsize=15,
            weight='bold',
            pad=20
        )
        
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Plot saved to {output_path}")
        
        plt.show()
        
    except Exception as e:
        logger.error(f"Error generating shooting plot: {e}")


def generate_scouting_report(scouting_pool: pd.DataFrame, top_n: int = 15) -> None:
    """
    Generate a text-based scouting report with key findings.
    
    Args:
        scouting_pool: Filtered prospect DataFrame
        top_n: Number of top prospects to highlight
    """
    logger.info("Generating scouting report...")
    
    print("\n" + "="*80)
    print("MONEYBALL FOOTBALL SCOUTING REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    print(f"\nTOTAL PROSPECTS IDENTIFIED: {len(scouting_pool)}")
    print(f"Average Age: {scouting_pool['Age'].mean():.1f} years")
    print(f"Average Game Time: {scouting_pool['90s'].mean():.1f} matches")
    
    # TOP PROSPECTS BY COMBINED SCORE
    print(f"\n{'TOP ' + str(top_n) + ' PROSPECTS (Overall Performance)':^80}")
    print("-"*80)
    
    if 'Combined_Score' in scouting_pool.columns:
        top_overall = scouting_pool.nlargest(top_n, 'Combined_Score')[
            ['Player', 'Squad', 'Age', '90s', 'Goals_per_90', 'npxG_per_90', 
             'Shot_Accuracy', 'Finishing_Efficiency']
        ]
    else:
        top_overall = scouting_pool.head(top_n)
    
    for idx, (_, player) in enumerate(top_overall.iterrows(), 1):
        print(f"\n{idx}. {player['Player']} ({player['Squad']}) - Age {int(player['Age'])}")
        print(f"   Playing Time: {player['90s']:.1f} matches | Shot Accuracy: {player['Shot_Accuracy']:.1%}")
        if 'Goals_per_90' in player.index:
            print(f"   Goals/90: {player['Goals_per_90']:.2f} | xG/90: {player['npxG_per_90']:.2f}")
        if 'Finishing_Efficiency' in player.index:
            eff_direction = "↑ OVERPERFORMING" if player['Finishing_Efficiency'] > 0 else "↓ UNDERPERFORMING"
            print(f"   Finishing Efficiency: {eff_direction} ({player['Finishing_Efficiency']:+.2f})")
    
    # HIDDEN GEMS ANALYSIS
    if 'npxG_per_90' in scouting_pool.columns and 'Finishing_Efficiency' in scouting_pool.columns:
        print(f"\n{'HIDDEN GEMS (High xG, Underperforming Finish)':^80}")
        print("-"*80)
        
        hidden_gems = scouting_pool[
            (scouting_pool['npxG_per_90'] > scouting_pool['npxG_per_90'].quantile(0.75)) &
            (scouting_pool['Finishing_Efficiency'] < 0)
        ].nlargest(5, 'npxG_per_90')
        
        for idx, (_, player) in enumerate(hidden_gems.iterrows(), 1):
            print(f"\n{idx}. {player['Player']} ({player['Squad']}) - Age {int(player['Age'])}")
            print(f"   xG/90: {player['npxG_per_90']:.2f} | Actual Goals/90: {player['Goals_per_90']:.2f}")
            print(f"   ⚠️  Underperforming by {abs(player['Finishing_Efficiency']):.2f} goals")
            print(f"   💡 INSIGHT: High positioning ability; finishing regression likely")
    
    print("\n" + "="*80 + "\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_full_pipeline(shooting_url: str, passing_url: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Execute complete scouting pipeline.
    
    Args:
        shooting_url: FBref shooting stats URL
        passing_url: FBref passing stats URL
        
    Returns:
        Tuple of (scouting_pool, all_data)
    """
    logger.info("="*80)
    logger.info("MONEYBALL FOOTBALL SCOUTING TOOL - STARTING PIPELINE")
    logger.info("="*80)
    
    # PHASE 1: Data Collection
    logger.info("\n[PHASE 1] DATA COLLECTION")
    df_shooting = collect_shooting_stats(shooting_url)
    
    if df_shooting is None or df_shooting.empty:
        logger.error("Failed to collect shooting data. Aborting.")
        return pd.DataFrame(), pd.DataFrame()
    
    df_passing = collect_passing_stats(passing_url)
    
    # PHASE 2: Data Cleaning
    logger.info("\n[PHASE 2] DATA CLEANING")
    df_shooting_clean = clean_football_data(df_shooting, 'shooting')
    df_passing_clean = clean_football_data(df_passing, 'passing') if df_passing is not None else pd.DataFrame()
    
    # Merge if both datasets available
    if not df_passing_clean.empty:
        merge_cols = ['Player', 'Squad', 'Age']
        df_merged = df_shooting_clean.merge(
            df_passing_clean,
            on=merge_cols,
            how='left',
            suffixes=('_shot', '_pass')
        )
        df_all = df_merged
    else:
        df_all = df_shooting_clean
    
    # PHASE 3: Feature Engineering
    logger.info("\n[PHASE 3] FEATURE ENGINEERING")
    df_engineered = engineer_features(df_all)
    scouting_pool = create_scouting_pool(df_engineered)
    
    # PHASE 4: Visualization & Reporting
    logger.info("\n[PHASE 4] VISUALIZATION & REPORTING")
    if not scouting_pool.empty:
        plot_xg_vs_finishing(scouting_pool, output_path='scouting_xg_finishing.png')
        plot_shot_volume_vs_accuracy(scouting_pool, output_path='scouting_shots_accuracy.png')
        generate_scouting_report(scouting_pool, top_n=15)
    else:
        logger.warning("Scouting pool is empty. No visualizations generated.")
    
    logger.info("\n[COMPLETE] Pipeline execution finished")
    logger.info("="*80 + "\n")
    
    return scouting_pool, df_all


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # FBref URLs for Big 5 European Leagues
    SHOOTING_URL = "https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats"
    PASSING_URL = "https://fbref.com/en/comps/Big5/passing/players/Big-5-European-Leagues-Stats"
    
    # Run the pipeline
    try:
        prospects, all_data = run_full_pipeline(SHOOTING_URL, PASSING_URL)
        
        # Optional: Save results to CSV for further analysis
        if not prospects.empty:
            prospects.to_csv('scouting_prospects.csv', index=False)
            logger.info("✓ Scouting prospects saved to scouting_prospects.csv")
            
            print("\n📊 Key Statistics:")
            print(f"Total Prospects: {len(prospects)}")
            print(f"Avg Goals/90: {prospects['Goals_per_90'].mean():.2f}")
            print(f"Avg xG/90: {prospects['npxG_per_90'].mean():.2f}")
            print(f"Avg Shot Accuracy: {prospects['Shot_Accuracy'].mean():.1%}")
        
    except KeyboardInterrupt:
        logger.warning("Pipeline interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error in pipeline: {e}")
        raise
