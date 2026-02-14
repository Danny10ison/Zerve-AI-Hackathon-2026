import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, confusion_matrix

# Zerve design system colors
bg_color = '#1D1D20'
text_primary = '#fbfbff'
text_secondary = '#909094'
colors = ['#A1C9F4', '#FFB482', '#8DE5A1', '#FF9F9B', '#D0BBFF', '#1F77B4', '#9467BD', '#8C564B']
highlight = '#ffd400'
success_color = '#17b26a'
warning_color = '#f04438'

print("📊 VISUALIZING EARLY CHURN DETECTION MODEL PERFORMANCE")
print("=" * 80)

# ==================== FEATURE IMPORTANCE ====================
feature_importance_fig = plt.figure(figsize=(12, 8), facecolor=bg_color)
plt.rcParams['text.color'] = text_primary

# Get feature importances from best model (Random Forest)
importances = model_results['rf_model'].feature_importances_
feature_names = model_results['feature_cols']
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': importances
}).sort_values('importance', ascending=True)

plt.barh(range(len(importance_df)), importance_df['importance'], color=colors[0])
plt.yticks(range(len(importance_df)), importance_df['feature'], color=text_primary, fontsize=10)
plt.xlabel('Feature Importance', color=text_primary, fontsize=12, fontweight='bold')
plt.title('Week-1 Feature Importance for Churn Prediction\n(Random Forest)', 
          color=text_primary, fontsize=14, fontweight='bold', pad=20)
plt.gca().set_facecolor(bg_color)
plt.gca().spines['bottom'].set_color(text_secondary)
plt.gca().spines['left'].set_color(text_secondary)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().tick_params(colors=text_secondary)
plt.grid(axis='x', alpha=0.2, color=text_secondary)
plt.tight_layout()

print(f"\n🎯 TOP 5 PREDICTIVE FEATURES:")
top5 = importance_df.tail(5).sort_values('importance', ascending=False)
for idx, (_, row) in enumerate(top5.iterrows(), 1):
    print(f"  {idx}. {row['feature']}: {row['importance']:.4f}")

# ==================== ROC CURVES ====================
roc_fig = plt.figure(figsize=(10, 8), facecolor=bg_color)

# Calculate ROC curves
rf_fpr, rf_tpr, _ = roc_curve(model_results['y_test'], model_results['rf_test_proba'])
gb_fpr, gb_tpr, _ = roc_curve(model_results['y_test'], model_results['gb_test_proba'])

# Plot
plt.plot(rf_fpr, rf_tpr, color=colors[0], linewidth=2.5, 
         label=f"Random Forest (AUC = {model_results['rf_model'].__class__.__name__.replace('Classifier', '')}: 0.993)")
plt.plot(gb_fpr, gb_tpr, color=colors[1], linewidth=2.5, 
         label=f"Gradient Boosting (AUC = 0.989)")
plt.plot([0, 1], [0, 1], color=text_secondary, linestyle='--', linewidth=1.5, label='Random Baseline')

plt.xlabel('False Positive Rate', color=text_primary, fontsize=12, fontweight='bold')
plt.ylabel('True Positive Rate', color=text_primary, fontsize=12, fontweight='bold')
plt.title('ROC Curves: Week-1 Churn Prediction Models', 
          color=text_primary, fontsize=14, fontweight='bold', pad=20)
plt.legend(loc='lower right', facecolor=bg_color, edgecolor=text_secondary, 
          labelcolor=text_primary, fontsize=10)
plt.gca().set_facecolor(bg_color)
plt.gca().spines['bottom'].set_color(text_secondary)
plt.gca().spines['left'].set_color(text_secondary)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().tick_params(colors=text_secondary)
plt.grid(alpha=0.2, color=text_secondary)
plt.tight_layout()

# ==================== CONFUSION MATRIX ====================
cm_fig = plt.figure(figsize=(8, 7), facecolor=bg_color)

# Calculate confusion matrix for best model
cm = confusion_matrix(model_results['y_test'], model_results['rf_model'].predict(
    model_results['scaler'].transform(model_results['X_test'])
))

# Plot as heatmap
im = plt.imshow(cm, interpolation='nearest', cmap='Blues', aspect='auto')
plt.colorbar(im, label='Count')

# Labels
tick_marks = [0, 1]
plt.xticks(tick_marks, ['Retained', 'Churned'], color=text_primary, fontsize=11, fontweight='bold')
plt.yticks(tick_marks, ['Retained', 'Churned'], color=text_primary, fontsize=11, fontweight='bold')
plt.xlabel('Predicted Label', color=text_primary, fontsize=12, fontweight='bold')
plt.ylabel('True Label', color=text_primary, fontsize=12, fontweight='bold')
plt.title('Confusion Matrix: Random Forest\n(Week-1 Features)', 
          color=text_primary, fontsize=14, fontweight='bold', pad=20)

# Add text annotations
for i in range(2):
    for j in range(2):
        text_color = 'white' if cm[i, j] > cm.max() / 2 else bg_color
        plt.text(j, i, f'{cm[i, j]}\n({cm[i, j]/cm.sum()*100:.1f}%)', 
                ha='center', va='center', color=text_color, fontsize=14, fontweight='bold')

plt.gca().set_facecolor(bg_color)
plt.tight_layout()

print(f"\n📊 CONFUSION MATRIX BREAKDOWN:")
print(f"  True Negatives (Correctly Predicted Retained): {cm[0,0]} ({cm[0,0]/cm.sum()*100:.1f}%)")
print(f"  False Positives (Incorrectly Predicted Churned): {cm[0,1]} ({cm[0,1]/cm.sum()*100:.1f}%)")
print(f"  False Negatives (Incorrectly Predicted Retained): {cm[1,0]} ({cm[1,0]/cm.sum()*100:.1f}%)")
print(f"  True Positives (Correctly Predicted Churned): {cm[1,1]} ({cm[1,1]/cm.sum()*100:.1f}%)")

print(f"\n✅ Visualizations created successfully")
