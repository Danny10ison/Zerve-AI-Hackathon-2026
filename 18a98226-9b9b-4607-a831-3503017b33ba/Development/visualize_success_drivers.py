import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create comprehensive visualizations of key success drivers
print("📊 GENERATING SUCCESS DRIVER VISUALIZATIONS")
print("=" * 80)

# Zerve color palette
bg_color = '#1D1D20'
text_primary = '#fbfbff'
text_secondary = '#909094'
colors = ['#A1C9F4', '#FFB482', '#8DE5A1', '#FF9F9B', '#D0BBFF', '#1F77B4', '#9467BD', '#8C564B']
highlight = '#ffd400'

# Set style
plt.rcParams['figure.facecolor'] = bg_color
plt.rcParams['axes.facecolor'] = bg_color
plt.rcParams['text.color'] = text_primary
plt.rcParams['axes.labelcolor'] = text_primary
plt.rcParams['xtick.color'] = text_primary
plt.rcParams['ytick.color'] = text_primary
plt.rcParams['axes.edgecolor'] = text_secondary

# 1. Success Tier Distribution
tier_dist_fig = plt.figure(figsize=(10, 6))
tier_counts = user_segments['success_tier'].value_counts().reindex(['Power Users', 'Active Users', 'Regular Users', 'Casual Users', 'Trial Users'])
bars = plt.bar(range(len(tier_counts)), tier_counts.values, color=colors[:5], edgecolor=text_secondary, linewidth=1.5)
plt.xticks(range(len(tier_counts)), tier_counts.index, rotation=0, fontsize=11)
plt.ylabel('Number of Users', fontsize=12, color=text_primary)
plt.title('User Distribution by Success Tier', fontsize=14, fontweight='bold', color=text_primary, pad=20)
plt.grid(axis='y', alpha=0.2, color=text_secondary)
for _i, (tier, count_val) in enumerate(tier_counts.items()):
    plt.text(_i, count_val + 50, f'{count_val:,}', ha='center', va='bottom', color=text_primary, fontsize=10)
plt.tight_layout()
print("✓ Created success tier distribution chart")

# 2. Correlation Heatmap - Early Behaviors vs Success
early_corr_fig = plt.figure(figsize=(10, 6))
early_metrics_list = ['avg_events_per_day', 'unique_event_types', 'execution_event_rate', 
                      'tool_invocation_count', 'sessions_with_diverse_events', 'unique_canvases']
success_metrics_list = ['composite_success_score', 'days_active', 'total_credits_used']
corr_matrix = user_segments[early_metrics_list + success_metrics_list].corr().loc[early_metrics_list, success_metrics_list]

# Plot heatmap
im = plt.imshow(corr_matrix.values, cmap='RdYlGn', aspect='auto', vmin=-0.5, vmax=1.0)
plt.xticks(range(len(success_metrics_list)), ['Success Score', 'Days Active', 'Credits Used'], rotation=0, fontsize=11)
plt.yticks(range(len(early_metrics_list)), 
           ['Activity Intensity', 'Event Types', 'Execution Rate', 'Tool Usage', 'Complete Sessions', 'Canvas Exploration'], 
           fontsize=10)
plt.title('Early Behavior Predictors of Success', fontsize=14, fontweight='bold', color=text_primary, pad=20)
cbar = plt.colorbar(im, label='Correlation (r)')
cbar.ax.yaxis.label.set_color(text_primary)
cbar.ax.tick_params(colors=text_primary)
for _i in range(len(early_metrics_list)):
    for _j in range(len(success_metrics_list)):
        text_val = plt.text(_j, _i, f'{corr_matrix.values[_i, _j]:.2f}',
                       ha="center", va="center", color='black' if abs(corr_matrix.values[_i, _j]) > 0.6 else text_primary, fontsize=9)
plt.tight_layout()
print("✓ Created correlation heatmap")

# 3. Credit Usage Impact on Success
credit_impact_fig = plt.figure(figsize=(11, 6))
credit_categories_ordered = ['Zero Credits', 'Low (<1)', 'Medium (1-10)', 'High (10-50)', 'Very High (50+)']
credit_success_by_cat = user_segments_credit.groupby('credit_category')['composite_success_score'].mean().reindex(credit_categories_ordered)
bars = plt.bar(range(len(credit_success_by_cat)), credit_success_by_cat.values, color=[colors[0], colors[1], colors[2], colors[3], highlight], edgecolor=text_secondary, linewidth=1.5)
plt.xticks(range(len(credit_success_by_cat)), ['Zero\nCredits', 'Low\n(<1)', 'Medium\n(1-10)', 'High\n(10-50)', 'Very High\n(50+)'], fontsize=10)
plt.ylabel('Average Success Score', fontsize=12, color=text_primary)
plt.title('Credit Usage as Success Indicator', fontsize=14, fontweight='bold', color=text_primary, pad=20)
plt.grid(axis='y', alpha=0.2, color=text_secondary)
for _i, score_val in enumerate(credit_success_by_cat.values):
    plt.text(_i, score_val + 5, f'{score_val:.1f}', ha='center', va='bottom', color=text_primary, fontsize=10)
plt.tight_layout()
print("✓ Created credit usage impact chart")

# 4. Key Metrics by Success Tier
metrics_by_tier_fig = plt.figure(figsize=(12, 7))
tier_order_viz = ['Power Users', 'Active Users', 'Regular Users', 'Casual Users', 'Trial Users']
metrics_to_plot = ['days_active', 'unique_event_types', 'tool_invocation_count', 'execution_event_count']
metric_labels = ['Days Active', 'Event Types', 'Tool Invocations', 'Executions']

tier_metric_data = user_segments.groupby('success_tier')[metrics_to_plot].mean().reindex(tier_order_viz)

x_pos = np.arange(len(tier_order_viz))
bar_width = 0.2

for idx, (metric, label) in enumerate(zip(metrics_to_plot, metric_labels)):
    values_normalized = tier_metric_data[metric].values / tier_metric_data[metric].max() * 100
    plt.bar(x_pos + idx * bar_width, values_normalized, bar_width, label=label, color=colors[idx], edgecolor=text_secondary, linewidth=0.5)

plt.xlabel('Success Tier', fontsize=12, color=text_primary)
plt.ylabel('Normalized Score (% of Max)', fontsize=12, color=text_primary)
plt.title('Key Behavioral Metrics Across Success Tiers', fontsize=14, fontweight='bold', color=text_primary, pad=20)
plt.xticks(x_pos + bar_width * 1.5, ['Power', 'Active', 'Regular', 'Casual', 'Trial'], fontsize=11)
plt.legend(loc='upper right', framealpha=0.9, facecolor=bg_color, edgecolor=text_secondary)
plt.grid(axis='y', alpha=0.2, color=text_secondary)
plt.tight_layout()
print("✓ Created metrics by tier comparison")

# 5. Session Completeness Distribution
session_complete_fig = plt.figure(figsize=(10, 6))
workflow_category_bins = [0, 1, 2, 3, 10]
workflow_labels = ['0-1 Categories', '2 Categories', '3 Categories', '4+ Categories']
session_event_patterns['workflow_bin'] = pd.cut(session_event_patterns['workflow_categories'], 
                                                  bins=workflow_category_bins, 
                                                  labels=workflow_labels, 
                                                  include_lowest=True)
workflow_dist = session_event_patterns['workflow_bin'].value_counts().reindex(workflow_labels)

bars = plt.bar(range(len(workflow_dist)), workflow_dist.values, color=colors[:4], edgecolor=text_secondary, linewidth=1.5)
plt.xticks(range(len(workflow_dist)), workflow_labels, rotation=15, fontsize=11, ha='right')
plt.ylabel('Number of Sessions', fontsize=12, color=text_primary)
plt.title('Workflow Completeness per Session', fontsize=14, fontweight='bold', color=text_primary, pad=20)
plt.grid(axis='y', alpha=0.2, color=text_secondary)
for _i, count_val in enumerate(workflow_dist.values):
    pct = count_val / workflow_dist.sum() * 100
    plt.text(_i, count_val + 100, f'{count_val:,}\n({pct:.1f}%)', ha='center', va='bottom', color=text_primary, fontsize=9)
plt.tight_layout()
print("✓ Created session completeness distribution")

# 6. Composite Score Components
score_components_fig = plt.figure(figsize=(10, 6))
component_scores = user_segments.groupby('success_tier')[['sustained_usage_score', 'workflow_depth_score', 'serious_usage_score']].mean().reindex(tier_order_viz)
component_labels = ['Sustained Usage', 'Workflow Depth', 'Serious Engagement']

x_pos = np.arange(len(tier_order_viz))
bar_width = 0.25

for idx, label in enumerate(component_labels):
    col_name = ['sustained_usage_score', 'workflow_depth_score', 'serious_usage_score'][idx]
    plt.bar(x_pos + idx * bar_width, component_scores[col_name].values, bar_width, 
            label=label, color=colors[idx], edgecolor=text_secondary, linewidth=0.5)

plt.xlabel('Success Tier', fontsize=12, color=text_primary)
plt.ylabel('Average Score', fontsize=12, color=text_primary)
plt.title('Success Score Components by Tier', fontsize=14, fontweight='bold', color=text_primary, pad=20)
plt.xticks(x_pos + bar_width, ['Power', 'Active', 'Regular', 'Casual', 'Trial'], fontsize=11)
plt.legend(loc='upper right', framealpha=0.9, facecolor=bg_color, edgecolor=text_secondary)
plt.grid(axis='y', alpha=0.2, color=text_secondary)
plt.tight_layout()
print("✓ Created score components breakdown")

print(f"\n✅ Generated 6 comprehensive visualizations of success drivers")
print(f"   All charts use Zerve design system and are presentation-ready")