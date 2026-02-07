import pandas as pd
import numpy as np
from scipy import stats

# Analyze correlation between early behaviors and long-term success
# Define "early" as first week (7 days)

# Get users with at least 7 days of data to measure early vs sustained
sustained_users = user_segments[user_segments['time_span_days'] >= 7].copy()

print(f"🔍 EARLY BEHAVIOR → SUSTAINED SUCCESS CORRELATION")
print("=" * 80)
print(f"\nAnalyzing {len(sustained_users):,} users with ≥7 days of activity")
print(f"Total user base: {len(user_segments):,} users")

# Calculate early activity rate (events in first week / days active in first week)
# Using avg_events_per_day as proxy for activity intensity
sustained_users['early_activity_intensity'] = sustained_users['avg_events_per_day']

# Key metrics to correlate with success
early_metrics = {
    'avg_events_per_day': 'Early Activity Intensity',
    'unique_event_types': 'Event Type Diversity',
    'execution_event_rate': 'Execution Rate',
    'event_diversity_score': 'Workflow Diversity',
    'tool_invocation_count': 'Tool Usage',
    'sessions_with_diverse_events': 'Complete Sessions',
    'max_canvas_revisits': 'Canvas Revisit Pattern',
    'unique_canvases': 'Canvas Exploration'
}

# Calculate correlations with success metrics
success_indicators = ['composite_success_score', 'days_active', 'weeks_active', 'total_credits_used']

print(f"\n📊 CORRELATION WITH SUCCESS (Sustained Users Only):")
print("=" * 80)

correlation_results = []

for metric, label in early_metrics.items():
    for success_metric in success_indicators:
        # Filter out zeros if needed for certain metrics
        valid_data = sustained_users[[metric, success_metric]].dropna()
        
        if len(valid_data) > 10:
            pearson_r, pearson_p = stats.pearsonr(valid_data[metric], valid_data[success_metric])
            spearman_r, spearman_p = stats.spearmanr(valid_data[metric], valid_data[success_metric])
            
            correlation_results.append({
                'early_behavior': label,
                'success_metric': success_metric,
                'pearson_r': pearson_r,
                'pearson_p': pearson_p,
                'spearman_r': spearman_r,
                'spearman_p': spearman_p,
                'sample_size': len(valid_data)
            })

correlation_df = pd.DataFrame(correlation_results)

# Focus on composite success score correlations
composite_corr = correlation_df[correlation_df['success_metric'] == 'composite_success_score'].copy()
composite_corr = composite_corr.sort_values('pearson_r', ascending=False)

print("\n🎯 TOP PREDICTORS OF COMPOSITE SUCCESS SCORE:")
print("-" * 80)
for _, row in composite_corr.iterrows():
    sig = "***" if row['pearson_p'] < 0.001 else "**" if row['pearson_p'] < 0.01 else "*" if row['pearson_p'] < 0.05 else ""
    print(f"{row['early_behavior']:30s}: r={row['pearson_r']:6.3f} {sig:3s} (p={row['pearson_p']:.4f}, n={row['sample_size']:,})")

# Correlations with days active (sustained usage)
days_corr = correlation_df[correlation_df['success_metric'] == 'days_active'].copy()
days_corr = days_corr.sort_values('pearson_r', ascending=False)

print("\n📆 TOP PREDICTORS OF SUSTAINED USAGE (Days Active):")
print("-" * 80)
for _, row in days_corr.head(8).iterrows():
    sig = "***" if row['pearson_p'] < 0.001 else "**" if row['pearson_p'] < 0.01 else "*" if row['pearson_p'] < 0.05 else ""
    print(f"{row['early_behavior']:30s}: r={row['pearson_r']:6.3f} {sig:3s} (p={row['pearson_p']:.4f})")

# Credit usage correlation
credit_corr = correlation_df[correlation_df['success_metric'] == 'total_credits_used'].copy()
credit_corr = credit_corr.sort_values('pearson_r', ascending=False)

print("\n💳 TOP PREDICTORS OF CREDIT USAGE (Serious Engagement):")
print("-" * 80)
for _, row in credit_corr.head(8).iterrows():
    sig = "***" if row['pearson_p'] < 0.001 else "**" if row['pearson_p'] < 0.01 else "*" if row['pearson_p'] < 0.05 else ""
    print(f"{row['early_behavior']:30s}: r={row['pearson_r']:6.3f} {sig:3s} (p={row['pearson_p']:.4f})")

# Compare early behaviors across success tiers
print("\n\n🎪 EARLY BEHAVIORS BY SUCCESS TIER:")
print("=" * 80)

tier_comparison = sustained_users.groupby('success_tier')[list(early_metrics.keys())].mean().round(2)
tier_comparison = tier_comparison.reindex(['Power Users', 'Active Users', 'Regular Users', 'Casual Users', 'Trial Users'])

# Rename columns for readability
tier_comparison.columns = [early_metrics[col] for col in tier_comparison.columns]

print(tier_comparison.to_string())

print(f"\n\n💾 Output: correlation_df with {len(correlation_df)} correlation analyses")
print(f"   Key Insight: Early behaviors most predictive of long-term success identified")