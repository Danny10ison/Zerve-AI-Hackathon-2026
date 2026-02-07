import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Analyze credit usage thresholds that separate serious vs casual users
print("💳 CREDIT USAGE THRESHOLD ANALYSIS")
print("=" * 80)

# Segment by credit usage
user_segments_credit = user_segments.copy()

# Categorize by credit usage
def categorize_credit_usage(credits):
    if credits == 0:
        return 'Zero Credits'
    elif credits < 1:
        return 'Low (<1)'
    elif credits < 10:
        return 'Medium (1-10)'
    elif credits < 50:
        return 'High (10-50)'
    else:
        return 'Very High (50+)'

user_segments_credit['credit_category'] = user_segments_credit['total_credits_used'].apply(categorize_credit_usage)

# Analyze relationship between credits and success
credit_analysis = user_segments_credit.groupby('credit_category').agg({
    'user_id': 'count',
    'composite_success_score': ['mean', 'median', 'std'],
    'days_active': 'mean',
    'total_events': 'mean',
    'tool_invocation_count': 'mean',
    'execution_event_count': 'mean',
    'unique_event_types': 'mean'
}).round(2)

credit_analysis.columns = ['_'.join(col).strip('_') for col in credit_analysis.columns]
credit_analysis = credit_analysis.rename(columns={'user_id_count': 'user_count'})

# Reorder by credit level
credit_order = ['Zero Credits', 'Low (<1)', 'Medium (1-10)', 'High (10-50)', 'Very High (50+)']
credit_analysis = credit_analysis.reindex(credit_order)

print("\n📊 USER BEHAVIOR BY CREDIT USAGE LEVEL:")
print("=" * 80)
print(credit_analysis.to_string())

# Calculate success tier distribution by credit usage
credit_tier_crosstab = pd.crosstab(
    user_segments_credit['credit_category'],
    user_segments_credit['success_tier'],
    normalize='index'
) * 100

credit_tier_crosstab = credit_tier_crosstab.reindex(credit_order)
tier_col_order = ['Power Users', 'Active Users', 'Regular Users', 'Casual Users', 'Trial Users']
credit_tier_crosstab = credit_tier_crosstab[[col for col in tier_col_order if col in credit_tier_crosstab.columns]]

print("\n\n🎯 SUCCESS TIER DISTRIBUTION BY CREDIT USAGE (%):")
print("=" * 80)
print(credit_tier_crosstab.round(1).to_string())

# Find optimal threshold
users_with_credits = user_segments_credit[user_segments_credit['total_credits_used'] > 0]
percentiles = [10, 25, 50, 75, 90, 95]

print(f"\n\n📈 CREDIT USAGE PERCENTILES (Users with Credits > 0):")
print("=" * 80)
print(f"Total users with credits > 0: {len(users_with_credits):,} ({len(users_with_credits)/len(user_segments_credit)*100:.1f}%)")
print(f"\nPercentile Distribution:")

threshold_stats = []
for p in percentiles:
    threshold = users_with_credits['total_credits_used'].quantile(p/100)
    users_above = (users_with_credits['total_credits_used'] >= threshold).sum()
    avg_success_above = users_with_credits[users_with_credits['total_credits_used'] >= threshold]['composite_success_score'].mean()
    avg_days_above = users_with_credits[users_with_credits['total_credits_used'] >= threshold]['days_active'].mean()
    
    print(f"  {p:3d}th percentile: {threshold:8.2f} credits ({users_above:4,} users above, avg success score: {avg_success_above:.2f})")
    
    threshold_stats.append({
        'percentile': p,
        'threshold': threshold,
        'users_above': users_above,
        'avg_success_score': avg_success_above,
        'avg_days_active': avg_days_above
    })

threshold_df = pd.DataFrame(threshold_stats)

# Identify key threshold that separates serious from casual users
# Look at where success score significantly increases
print(f"\n\n🎪 KEY CREDIT USAGE THRESHOLDS:")
print("=" * 80)

# Compare zero credits vs any credits
zero_credit_success = user_segments_credit[user_segments_credit['total_credits_used'] == 0]['composite_success_score'].mean()
any_credit_success = user_segments_credit[user_segments_credit['total_credits_used'] > 0]['composite_success_score'].mean()

print(f"\nZero Credits:")
print(f"  Users: {(user_segments_credit['total_credits_used'] == 0).sum():,}")
print(f"  Avg Success Score: {zero_credit_success:.2f}")
print(f"  Avg Days Active: {user_segments_credit[user_segments_credit['total_credits_used'] == 0]['days_active'].mean():.2f}")

print(f"\nAny Credits (>0):")
print(f"  Users: {(user_segments_credit['total_credits_used'] > 0).sum():,}")
print(f"  Avg Success Score: {any_credit_success:.2f}")
print(f"  Avg Days Active: {users_with_credits['days_active'].mean():.2f}")
print(f"  Success Score Lift: {((any_credit_success - zero_credit_success) / zero_credit_success * 100):.1f}%")

# Analyze 1 credit threshold
one_credit_success = user_segments_credit[user_segments_credit['total_credits_used'] >= 1]['composite_success_score'].mean()
one_credit_users = (user_segments_credit['total_credits_used'] >= 1).sum()

print(f"\n≥1 Credit (Serious Usage Threshold):")
print(f"  Users: {one_credit_users:,}")
print(f"  Avg Success Score: {one_credit_success:.2f}")
print(f"  Avg Days Active: {user_segments_credit[user_segments_credit['total_credits_used'] >= 1]['days_active'].mean():.2f}")
print(f"  Success Score Lift vs Zero: {((one_credit_success - zero_credit_success) / zero_credit_success * 100):.1f}%")

# Analyze 10 credit threshold (high engagement)
ten_credit_success = user_segments_credit[user_segments_credit['total_credits_used'] >= 10]['composite_success_score'].mean()
ten_credit_users = (user_segments_credit['total_credits_used'] >= 10).sum()

print(f"\n≥10 Credits (Power User Threshold):")
print(f"  Users: {ten_credit_users:,}")
print(f"  Avg Success Score: {ten_credit_success:.2f}")
print(f"  Avg Days Active: {user_segments_credit[user_segments_credit['total_credits_used'] >= 10]['days_active'].mean():.2f}")
print(f"  Success Score Lift vs Zero: {((ten_credit_success - zero_credit_success) / zero_credit_success * 100):.1f}%")

# Correlation between credits and other metrics
print(f"\n\n📉 CREDIT USAGE CORRELATIONS:")
print("=" * 80)

correlations = {
    'Days Active': user_segments_credit['total_credits_used'].corr(user_segments_credit['days_active']),
    'Total Events': user_segments_credit['total_credits_used'].corr(user_segments_credit['total_events']),
    'Tool Invocations': user_segments_credit['total_credits_used'].corr(user_segments_credit['tool_invocation_count']),
    'Unique Event Types': user_segments_credit['total_credits_used'].corr(user_segments_credit['unique_event_types']),
    'Composite Success': user_segments_credit['total_credits_used'].corr(user_segments_credit['composite_success_score'])
}

for metric, corr in correlations.items():
    print(f"  {metric:25s}: r = {corr:.3f}")

print(f"\n💾 Output: credit_analysis with credit usage segmentation")
print(f"   Output: threshold_df with {len(threshold_df)} threshold analyses")