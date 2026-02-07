import pandas as pd
import numpy as np

# Parse timestamps
df_features = filtered_df.copy()
df_features['timestamp'] = pd.to_datetime(df_features['timestamp'], errors='coerce')
df_features['created_at'] = pd.to_datetime(df_features['created_at'], errors='coerce')

# Consolidate user ID - use person_id as primary identifier
df_features['user_id'] = df_features['person_id']

# Filter to users with valid user_id and timestamp
df_features = df_features[df_features['user_id'].notna() & df_features['timestamp'].notna()].copy()

print(f"🎯 ENGINEERING USER SUCCESS METRICS")
print(f"=" * 80)
print(f"Total events: {len(df_features):,}")
print(f"Unique users: {df_features['user_id'].nunique():,}")
print(f"\n📊 FEATURE CATEGORIES:")
print(f"  1. Sustained usage (days active, time span, weekly patterns)")
print(f"  2. Workflow depth (unique events, event diversity)")
print(f"  3. Reproducibility (execution frequency, canvas re-runs)")
print(f"  4. End-to-end workflows (events per session, completeness)")
print(f"  5. Serious usage (credits used, tool invocations)")
print(f"\n" + "=" * 80)

# ==================== FEATURE ENGINEERING ====================

# Group by user
user_features = []

for user_id, user_df in df_features.groupby('user_id'):
    features = {'user_id': user_id}
    
    # === 1. SUSTAINED USAGE ===
    # Days active
    features['days_active'] = user_df['timestamp'].dt.date.nunique()
    
    # Time span between first and last event (in days)
    first_event = user_df['timestamp'].min()
    last_event = user_df['timestamp'].max()
    features['time_span_days'] = (last_event - first_event).total_seconds() / 86400
    
    # Weekly activity pattern - number of unique weeks active
    user_df_copy = user_df.copy()
    user_df_copy['week'] = user_df_copy['timestamp'].dt.isocalendar().week
    user_df_copy['year'] = user_df_copy['timestamp'].dt.year
    features['weeks_active'] = len(user_df_copy.groupby(['year', 'week']).size())
    
    # Average events per active day
    features['avg_events_per_day'] = len(user_df) / max(features['days_active'], 1)
    
    # === 2. WORKFLOW DEPTH ===
    # Unique event types per user
    features['unique_event_types'] = user_df['event'].nunique()
    
    # Event diversity score (Shannon entropy)
    event_counts = user_df['event'].value_counts()
    event_probs = event_counts / event_counts.sum()
    features['event_diversity_score'] = -np.sum(event_probs * np.log2(event_probs + 1e-10))
    
    # Total events
    features['total_events'] = len(user_df)
    
    # === 3. REPRODUCIBILITY ===
    # Execution-related events (block runs, code execution)
    execution_keywords = ['run', 'execute', 'block_', 'agent_']
    execution_events = user_df[user_df['event'].str.contains('|'.join(execution_keywords), case=False, na=False)]
    features['execution_event_count'] = len(execution_events)
    features['execution_event_rate'] = len(execution_events) / max(len(user_df), 1)
    
    # Canvas re-runs (multiple events on same canvas)
    canvas_counts = user_df['prop_$pathname'].value_counts()
    features['max_canvas_revisits'] = canvas_counts.max() if len(canvas_counts) > 0 else 0
    features['unique_canvases'] = user_df['prop_$pathname'].nunique()
    
    # === 4. END-TO-END WORKFLOWS ===
    # Consolidate session ID
    user_df_session = user_df.copy()
    user_df_session['session_id'] = user_df_session['prop_$session_id'].fillna(user_df_session['prop_session_id'])
    
    # Events per session
    session_event_counts = user_df_session[user_df_session['session_id'].notna()].groupby('session_id').size()
    features['avg_events_per_session'] = session_event_counts.mean() if len(session_event_counts) > 0 else 0
    features['max_events_per_session'] = session_event_counts.max() if len(session_event_counts) > 0 else 0
    features['unique_sessions'] = user_df_session['session_id'].nunique()
    
    # Session completeness - sessions with multiple event types
    session_diversity = user_df_session[user_df_session['session_id'].notna()].groupby('session_id')['event'].nunique()
    features['sessions_with_diverse_events'] = (session_diversity > 3).sum()
    
    # === 5. SERIOUS USAGE ===
    # Total credits used
    features['total_credits_used'] = user_df['prop_credits_used'].sum()
    features['total_credit_amount'] = user_df['prop_credit_amount'].sum()
    
    # Tool invocation counts
    features['tool_invocation_count'] = user_df['prop_tool_name'].notna().sum()
    features['unique_tools_used'] = user_df['prop_tool_name'].nunique()
    
    # Message/interaction count
    features['message_count'] = user_df['prop_message_id'].notna().sum()
    
    user_features.append(features)

# Create feature dataframe
user_success_df = pd.DataFrame(user_features)

# Handle any NaN/inf values
user_success_df = user_success_df.replace([np.inf, -np.inf], np.nan)
user_success_df = user_success_df.fillna(0)

print(f"\n✅ FEATURE ENGINEERING COMPLETE")
print(f"=" * 80)
print(f"Users with features: {len(user_success_df):,}")
print(f"Features per user: {len(user_success_df.columns) - 1}")

print(f"\n📋 FEATURE SUMMARY:")
print(user_success_df.describe().T.round(2))

print(f"\n🎯 TOP 10 USERS BY ENGAGEMENT SCORE (total_events * days_active):")
user_success_df['engagement_score'] = user_success_df['total_events'] * user_success_df['days_active']
top_users = user_success_df.nlargest(10, 'engagement_score')[['user_id', 'total_events', 'days_active', 'engagement_score', 'total_credits_used']]
print(top_users.to_string(index=False))

print(f"\n💾 Output: user_success_df with {len(user_success_df):,} users and {len(user_success_df.columns)} columns")