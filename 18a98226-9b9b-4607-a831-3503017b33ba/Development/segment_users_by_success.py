import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Define composite success score based on key metrics
# Weights based on domain knowledge of what indicates platform success
success_metrics = user_success_df.copy()

# Create normalized composite score (0-100 scale)
# Key success indicators: sustained usage, workflow depth, serious engagement
success_metrics['sustained_usage_score'] = (
    success_metrics['days_active'] * 0.4 + 
    success_metrics['weeks_active'] * 0.3 + 
    (success_metrics['time_span_days'] / success_metrics['time_span_days'].max() * 10) * 0.3
)

success_metrics['workflow_depth_score'] = (
    success_metrics['unique_event_types'] * 0.5 + 
    success_metrics['event_diversity_score'] * 2 +
    (success_metrics['sessions_with_diverse_events'] / success_metrics['sessions_with_diverse_events'].max() * 10) * 0.5
)

success_metrics['serious_usage_score'] = (
    np.log1p(success_metrics['total_credits_used']) * 2 +
    success_metrics['tool_invocation_count'] / 10 +
    success_metrics['execution_event_count'] / 10
)

# Composite success score
success_metrics['composite_success_score'] = (
    success_metrics['sustained_usage_score'] * 0.35 +
    success_metrics['workflow_depth_score'] * 0.35 +
    success_metrics['serious_usage_score'] * 0.30
)

# Define success tiers using percentiles
percentile_20 = success_metrics['composite_success_score'].quantile(0.20)
percentile_50 = success_metrics['composite_success_score'].quantile(0.50)
percentile_80 = success_metrics['composite_success_score'].quantile(0.80)
percentile_95 = success_metrics['composite_success_score'].quantile(0.95)

def categorize_success(score):
    if score >= percentile_95:
        return 'Power Users'
    elif score >= percentile_80:
        return 'Active Users'
    elif score >= percentile_50:
        return 'Regular Users'
    elif score >= percentile_20:
        return 'Casual Users'
    else:
        return 'Trial Users'

success_metrics['success_tier'] = success_metrics['composite_success_score'].apply(categorize_success)

# Calculate tier statistics
tier_stats = success_metrics.groupby('success_tier').agg({
    'user_id': 'count',
    'composite_success_score': ['mean', 'min', 'max'],
    'days_active': 'mean',
    'total_events': 'mean',
    'unique_event_types': 'mean',
    'total_credits_used': 'mean',
    'execution_event_count': 'mean',
    'weeks_active': 'mean'
}).round(2)

tier_stats.columns = ['_'.join(col).strip('_') for col in tier_stats.columns]
tier_stats = tier_stats.rename(columns={'user_id_count': 'user_count'})

# Order tiers logically
tier_order = ['Power Users', 'Active Users', 'Regular Users', 'Casual Users', 'Trial Users']
tier_stats = tier_stats.reindex(tier_order)

print("🎯 USER SUCCESS TIER SEGMENTATION")
print("=" * 80)
print(f"\nTier Definitions:")
print(f"  • Power Users (Top 5%): Score ≥ {percentile_95:.2f}")
print(f"  • Active Users (80-95%): Score {percentile_80:.2f} - {percentile_95:.2f}")
print(f"  • Regular Users (50-80%): Score {percentile_50:.2f} - {percentile_80:.2f}")
print(f"  • Casual Users (20-50%): Score {percentile_20:.2f} - {percentile_50:.2f}")
print(f"  • Trial Users (Bottom 20%): Score < {percentile_20:.2f}")
print(f"\n{'='*80}")
print(f"\n📊 TIER STATISTICS:")
print(tier_stats.to_string())

# Distribution by tier
tier_distribution = success_metrics['success_tier'].value_counts().reindex(tier_order)
print(f"\n📈 USER DISTRIBUTION:")
for tier, count in tier_distribution.items():
    pct = (count / len(success_metrics)) * 100
    print(f"  {tier:20s}: {count:5,} users ({pct:5.1f}%)")

print(f"\n💾 Output: success_metrics DataFrame with {len(success_metrics):,} users segmented into 5 tiers")

# Store segmented data
user_segments = success_metrics