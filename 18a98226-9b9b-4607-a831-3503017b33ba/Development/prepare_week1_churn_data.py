import pandas as pd
import numpy as np

# Create week-1 only features for early churn detection
# Filter df_features to only include events from first 7 days for each user

print("🎯 PREPARING EARLY CHURN DETECTION DATASET")
print("=" * 80)

# Sort by user and timestamp
df_sorted = df_features.sort_values(['user_id', 'timestamp']).copy()

# Get first event timestamp for each user
user_first_event = df_sorted.groupby('user_id')['timestamp'].min().to_dict()

# Add days_since_first_event column
df_sorted['days_since_first'] = df_sorted.apply(
    lambda row: (row['timestamp'] - user_first_event[row['user_id']]).total_seconds() / 86400,
    axis=1
)

# Filter to week 1 only (first 7 days)
week1_events = df_sorted[df_sorted['days_since_first'] <= 7].copy()

print(f"\n📊 DATA SCOPE:")
print(f"  Total events: {len(df_sorted):,}")
print(f"  Week-1 events: {len(week1_events):,}")
print(f"  Total users: {df_sorted['user_id'].nunique():,}")
print(f"  Users with week-1 activity: {week1_events['user_id'].nunique():,}")

# Engineer week-1 features
week1_features = []

for user_id, user_df in week1_events.groupby('user_id'):
    features = {'user_id': user_id}
    
    # Activity volume
    features['w1_total_events'] = len(user_df)
    features['w1_days_active'] = user_df['timestamp'].dt.date.nunique()
    features['w1_unique_sessions'] = user_df['prop_$session_id'].fillna(user_df['prop_session_id']).nunique()
    
    # Event diversity
    features['w1_unique_event_types'] = user_df['event'].nunique()
    event_counts = user_df['event'].value_counts()
    event_probs = event_counts / event_counts.sum()
    features['w1_event_diversity'] = -np.sum(event_probs * np.log2(event_probs + 1e-10))
    
    # Execution behavior
    execution_keywords = ['run', 'execute', 'block_', 'agent_']
    execution_events = user_df[user_df['event'].str.contains('|'.join(execution_keywords), case=False, na=False)]
    features['w1_execution_count'] = len(execution_events)
    features['w1_execution_rate'] = len(execution_events) / max(len(user_df), 1)
    
    # Canvas engagement
    features['w1_unique_canvases'] = user_df['prop_$pathname'].nunique()
    features['w1_avg_events_per_canvas'] = len(user_df) / max(features['w1_unique_canvases'], 1)
    
    # Tool usage (serious engagement indicator)
    features['w1_credits_used'] = user_df['prop_credits_used'].sum()
    features['w1_tool_invocations'] = user_df['prop_tool_name'].notna().sum()
    features['w1_messages'] = user_df['prop_message_id'].notna().sum()
    
    # Session depth
    session_counts = user_df[user_df['prop_$session_id'].notna()].groupby('prop_$session_id').size()
    features['w1_avg_events_per_session'] = session_counts.mean() if len(session_counts) > 0 else 0
    features['w1_max_events_per_session'] = session_counts.max() if len(session_counts) > 0 else 0
    
    # Time-based patterns
    first_event = user_df['timestamp'].min()
    last_event = user_df['timestamp'].max()
    features['w1_time_span_days'] = (last_event - first_event).total_seconds() / 86400
    features['w1_avg_events_per_day'] = len(user_df) / max(features['w1_days_active'], 1)
    
    week1_features.append(features)

week1_df = pd.DataFrame(week1_features)

# Replace inf/nan
week1_df = week1_df.replace([np.inf, -np.inf], np.nan).fillna(0)

print(f"\n✅ WEEK-1 FEATURE ENGINEERING COMPLETE")
print(f"  Users: {len(week1_df):,}")
print(f"  Features: {len(week1_df.columns) - 1}")

# Merge with final outcomes from user_segments
# Define churn: users who did not become Active/Power Users (i.e., stayed Trial/Casual/Regular)
churn_data = week1_df.merge(
    user_segments[['user_id', 'success_tier', 'composite_success_score', 'days_active', 'total_events']], 
    on='user_id', 
    how='inner'
)

# Define churn target: 1 = churned (Trial/Casual), 0 = retained (Regular/Active/Power)
churn_data['churned'] = churn_data['success_tier'].isin(['Trial Users', 'Casual Users']).astype(int)

print(f"\n🎯 CHURN DEFINITION:")
print(f"  Churned (0): Trial Users, Casual Users")
print(f"  Retained (1): Regular Users, Active Users, Power Users")

print(f"\n📊 CHURN DISTRIBUTION:")
churn_counts = churn_data['churned'].value_counts()
print(f"  Retained: {churn_counts[0]:,} users ({churn_counts[0]/len(churn_data)*100:.1f}%)")
print(f"  Churned: {churn_counts[1]:,} users ({churn_counts[1]/len(churn_data)*100:.1f}%)")

print(f"\n📋 WEEK-1 FEATURES SUMMARY:")
print(churn_data.iloc[:, 1:18].describe().T.round(2))

print(f"\n💾 Output: churn_data with {len(churn_data):,} users, {len(week1_df.columns)-1} week-1 features, and churn target")
