import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
import warnings
warnings.filterwarnings('ignore')

# ── 데이터 로드 ───────────────────────────────────────────────────
df = pd.read_csv('/home/claude/model_dataset.csv', encoding='utf-8-sig')

feature_cols = [
    'visitor_count', 'visitor_lag1', 'visitor_lag2', 'visitor_lag3',
    'visitor_mom_growth', 'visitor_3m_avg', 'visitor_6m_avg',
    'visitor_vs_3m_avg', 'visitor_rolling_std', 'country_share',
    'buzz_volume', 'engagement', 'potential_exposure',
    'buzz_mom_growth', 'engagement_mom_growth', 'exposure_mom_growth',
    'engagement_per_visitor', 'buzz_per_visitor', 'buzz_vs_3m_avg',
    'positive_pct', 'negative_pct',
    'month', 'quarter', 'is_peak_season',
    'exchange_rate', 'oil_price',
]

X = df[feature_cols]
y = df['priority_label']

# 라벨 인코딩
le = LabelEncoder()
y_enc = le.fit_transform(y)
print(f"클래스: {le.classes_}")

# ── Train/Test Split (80/20) ──────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
)
print(f"Train: {X_train.shape}, Test: {X_test.shape}")

# ── 1. Random Forest ──────────────────────────────────────────────
rf = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight='balanced')
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

print("\n" + "="*50)
print("Random Forest 결과")
print("="*50)
print(f"Accuracy: {accuracy_score(y_test, y_pred_rf):.4f}")
print(classification_report(y_test, y_pred_rf, target_names=le.classes_))

# Cross-validation
cv_scores = cross_val_score(rf, X, y_enc, cv=5, scoring='accuracy')
print(f"5-Fold CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# Feature Importance
feat_imp = pd.DataFrame({
    'feature': feature_cols,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)
print("\nTop 10 Feature Importance:")
print(feat_imp.head(10).to_string(index=False))

# ── 2. Logistic Regression (비교) ────────────────────────────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
lr.fit(X_train_scaled, y_train)
y_pred_lr = lr.predict(X_test_scaled)

print("\n" + "="*50)
print("Logistic Regression 결과")
print("="*50)
print(f"Accuracy: {accuracy_score(y_test, y_pred_lr):.4f}")
print(classification_report(y_test, y_pred_lr, target_names=le.classes_))

# ── 저장 ─────────────────────────────────────────────────────────
os.makedirs('/home/claude/model', exist_ok=True)
with open('/home/claude/model/rf_model.pkl', 'wb') as f:
    pickle.dump(rf, f)
with open('/home/claude/model/label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)
with open('/home/claude/model/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
with open('/home/claude/model/feature_cols.pkl', 'wb') as f:
    pickle.dump(feature_cols, f)
feat_imp.to_csv('/home/claude/model/feature_importance.csv', index=False, encoding='utf-8-sig')

print("\n✅ 모델 저장 완료")

import os
