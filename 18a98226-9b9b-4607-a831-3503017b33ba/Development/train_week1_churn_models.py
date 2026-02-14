import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve

print("🎯 EARLY CHURN DETECTION MODEL TRAINING")
print("=" * 80)

# Prepare features and target
feature_cols = [col for col in churn_data.columns if col.startswith('w1_')]
X = churn_data[feature_cols]
y = churn_data['churned']

print(f"\n📊 DATASET DETAILS:")
print(f"  Total samples: {len(X):,}")
print(f"  Features: {len(feature_cols)}")
print(f"  Churn rate: {y.mean()*100:.1f}%")

# Train-test split (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"\n✂️ SPLIT:")
print(f"  Training: {len(X_train):,} samples")
print(f"  Testing: {len(X_test):,} samples")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\n🤖 TRAINING TWO MODELS:")
print(f"  1. Random Forest Classifier")
print(f"  2. Gradient Boosting Classifier")
print("=" * 80)

# ==================== RANDOM FOREST ====================
print(f"\n🌲 RANDOM FOREST CLASSIFIER")
print("-" * 80)

rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train_scaled, y_train)

# Predictions
rf_train_pred = rf_model.predict(X_train_scaled)
rf_test_pred = rf_model.predict(X_test_scaled)
rf_test_proba = rf_model.predict_proba(X_test_scaled)[:, 1]

# Metrics
rf_train_acc = (rf_train_pred == y_train).mean()
rf_test_acc = (rf_test_pred == y_test).mean()
rf_auc = roc_auc_score(y_test, rf_test_proba)

print(f"✅ Training Accuracy: {rf_train_acc*100:.2f}%")
print(f"✅ Testing Accuracy: {rf_test_acc*100:.2f}%")
print(f"✅ ROC-AUC Score: {rf_auc:.4f}")

print(f"\n📋 CLASSIFICATION REPORT:")
print(classification_report(y_test, rf_test_pred, target_names=['Retained', 'Churned']))

# ==================== GRADIENT BOOSTING ====================
print(f"\n⚡ GRADIENT BOOSTING CLASSIFIER")
print("-" * 80)

gb_model = GradientBoostingClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    random_state=42
)

gb_model.fit(X_train_scaled, y_train)

# Predictions
gb_train_pred = gb_model.predict(X_train_scaled)
gb_test_pred = gb_model.predict(X_test_scaled)
gb_test_proba = gb_model.predict_proba(X_test_scaled)[:, 1]

# Metrics
gb_train_acc = (gb_train_pred == y_train).mean()
gb_test_acc = (gb_test_pred == y_test).mean()
gb_auc = roc_auc_score(y_test, gb_test_proba)

print(f"✅ Training Accuracy: {gb_train_acc*100:.2f}%")
print(f"✅ Testing Accuracy: {gb_test_acc*100:.2f}%")
print(f"✅ ROC-AUC Score: {gb_auc:.4f}")

print(f"\n📋 CLASSIFICATION REPORT:")
print(classification_report(y_test, gb_test_pred, target_names=['Retained', 'Churned']))

# ==================== MODEL COMPARISON ====================
print(f"\n🏆 MODEL COMPARISON")
print("=" * 80)
comparison = pd.DataFrame({
    'Model': ['Random Forest', 'Gradient Boosting'],
    'Train_Accuracy': [rf_train_acc*100, gb_train_acc*100],
    'Test_Accuracy': [rf_test_acc*100, gb_test_acc*100],
    'ROC_AUC': [rf_auc, gb_auc]
})
print(comparison.to_string(index=False))

# Best model
best_model_name = 'Gradient Boosting' if gb_auc > rf_auc else 'Random Forest'
best_model = gb_model if gb_auc > rf_auc else rf_model
best_auc = max(gb_auc, rf_auc)

print(f"\n🥇 BEST MODEL: {best_model_name} (ROC-AUC: {best_auc:.4f})")

# Store results
model_results = {
    'rf_model': rf_model,
    'gb_model': gb_model,
    'best_model': best_model,
    'best_model_name': best_model_name,
    'scaler': scaler,
    'feature_cols': feature_cols,
    'X_test': X_test,
    'y_test': y_test,
    'rf_test_proba': rf_test_proba,
    'gb_test_proba': gb_test_proba,
    'comparison': comparison
}

print(f"\n💾 Models trained and stored for evaluation")
