import pandas as pd
import numpy as np
from collections import Counter

# Analyze event sequence patterns to identify end-to-end workflows
print("🔄 EVENT SEQUENCE PATTERN ANALYSIS")
print("=" * 80)

# Get event data with timestamps for sequence analysis
# Focus on power users and active users who show complete workflows
active_power_users = user_segments[
    user_segments['success_tier'].isin(['Power Users', 'Active Users'])
]['user_id'].tolist()

# Get event sequences from original data for these users
user_event_sequences = df_features[df_features['user_id'].isin(active_power_users)].copy()
user_event_sequences = user_event_sequences.sort_values(['user_id', 'timestamp'])

print(f"Analyzing {len(active_power_users):,} high-performing users")
print(f"Total events: {len(user_event_sequences):,}")

# Extract common event patterns (2-grams and 3-grams)
sequence_patterns = []

for user_id, user_events in user_event_sequences.groupby('user_id'):
    events = user_events['event'].tolist()
    
    # Skip users with very few events
    if len(events) < 3:
        continue
    
    # 2-gram patterns
    for _i in range(len(events) - 1):
        sequence_patterns.append((events[_i], events[_i + 1]))

# Count pattern frequencies
pattern_counts = Counter(sequence_patterns)
top_patterns = pattern_counts.most_common(30)

print(f"\n🎯 TOP 30 EVENT SEQUENCE PATTERNS (2-grams):")
print("=" * 80)
print(f"{'Rank':<6}{'Event 1':<40}{'Event 2':<40}{'Count':>8}")
print("-" * 80)

for rank, (pattern, count) in enumerate(top_patterns, 1):
    event1, event2 = pattern
    # Truncate long event names
    e1 = event1[:37] + '...' if len(event1) > 40 else event1
    e2 = event2[:37] + '...' if len(event2) > 40 else event2
    print(f"{rank:<6}{e1:<40}{e2:<40}{count:>8,}")

# Identify workflow indicators
workflow_keywords = {
    'data_loading': ['load', 'import', 'read', 'fetch', 'query'],
    'transformation': ['transform', 'clean', 'process', 'filter', 'merge'],
    'analysis': ['analyze', 'compute', 'calculate', 'aggregate'],
    'visualization': ['plot', 'chart', 'visualize', 'graph'],
    'model': ['train', 'predict', 'model', 'fit'],
    'execution': ['run', 'execute', 'block_run', 'agent_'],
    'export': ['export', 'save', 'write', 'output']
}

# Categorize events
def categorize_event(event_name):
    event_lower = event_name.lower()
    for category, keywords in workflow_keywords.items():
        for keyword in keywords:
            if keyword in event_lower:
                return category
    return 'other'

user_event_sequences['event_category'] = user_event_sequences['event'].apply(categorize_event)

# Analyze workflow completeness - users who show end-to-end patterns
workflow_progression_patterns = []

for user_id, user_events in user_event_sequences.groupby('user_id'):
    categories = user_events['event_category'].unique()
    workflow_progression_patterns.append({
        'user_id': user_id,
        'has_execution': 'execution' in categories,
        'has_visualization': 'visualization' in categories,
        'has_analysis': 'analysis' in categories,
        'category_count': len([c for c in categories if c != 'other']),
        'categories': set(categories)
    })

workflow_df = pd.DataFrame(workflow_progression_patterns)

# Calculate workflow completeness scores
complete_workflows = workflow_df[
    (workflow_df['has_execution']) & 
    (workflow_df['category_count'] >= 2)
]

print(f"\n\n📋 WORKFLOW COMPLETENESS ANALYSIS:")
print("=" * 80)
print(f"Users with execution events: {workflow_df['has_execution'].sum():,} ({workflow_df['has_execution'].mean()*100:.1f}%)")
print(f"Users with visualization: {workflow_df['has_visualization'].sum():,} ({workflow_df['has_visualization'].mean()*100:.1f}%)")
print(f"Users with analysis patterns: {workflow_df['has_analysis'].sum():,} ({workflow_df['has_analysis'].mean()*100:.1f}%)")
print(f"Users with complete workflows (execution + 2+ categories): {len(complete_workflows):,} ({len(complete_workflows)/len(workflow_df)*100:.1f}%)")

# Common workflow combinations
workflow_combinations = workflow_df['categories'].apply(lambda x: tuple(sorted([c for c in x if c != 'other'])))
combination_counts = Counter(workflow_combinations)

print(f"\n🔗 COMMON WORKFLOW CATEGORY COMBINATIONS:")
print("-" * 80)
for combo, count in combination_counts.most_common(15):
    if len(combo) > 0:
        combo_str = ' + '.join(combo)
        pct = count / len(workflow_df) * 100
        print(f"{combo_str:50s}: {count:5,} users ({pct:5.1f}%)")

# Session-level analysis - events per session patterns
session_event_patterns = user_event_sequences[
    user_event_sequences['prop_$session_id'].notna()
].groupby(['user_id', 'prop_$session_id']).agg({
    'event': ['count', 'nunique'],
    'event_category': lambda x: len(set(x) - {'other'})
}).reset_index()

session_event_patterns.columns = ['user_id', 'session_id', 'event_count', 'unique_events', 'workflow_categories']

print(f"\n\n📊 SESSION-LEVEL WORKFLOW PATTERNS:")
print("=" * 80)
print(f"Sessions analyzed: {len(session_event_patterns):,}")
print(f"\nEvents per session:")
print(f"  Mean: {session_event_patterns['event_count'].mean():.1f}")
print(f"  Median: {session_event_patterns['event_count'].median():.1f}")
print(f"  75th percentile: {session_event_patterns['event_count'].quantile(0.75):.0f}")
print(f"  90th percentile: {session_event_patterns['event_count'].quantile(0.90):.0f}")

print(f"\nWorkflow categories per session:")
print(f"  Mean: {session_event_patterns['workflow_categories'].mean():.2f}")
print(f"  Sessions with 2+ categories: {(session_event_patterns['workflow_categories'] >= 2).sum():,} ({(session_event_patterns['workflow_categories'] >= 2).mean()*100:.1f}%)")
print(f"  Sessions with 3+ categories: {(session_event_patterns['workflow_categories'] >= 3).sum():,} ({(session_event_patterns['workflow_categories'] >= 3).mean()*100:.1f}%)")

print(f"\n💾 Output: workflow_df with {len(workflow_df):,} user workflow patterns")
print(f"   Output: session_event_patterns with {len(session_event_patterns):,} session analyses")