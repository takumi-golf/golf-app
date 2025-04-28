import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# データの読み込み
df = pd.read_csv("golf_fitting_data.csv")

# 性別をエンコード
le = LabelEncoder()
df['gender_encoded'] = le.fit_transform(df['gender'])

# 特徴量と目標変数の設定
features = [
    'height', 'weight', 'age', 'gender_encoded', 
    'handicap', 'head_speed', 'ball_speed', 'launch_angle'
]

targets = [
    'recommended_driver_loft',
    'recommended_shaft_flex'
]

X = df[features]
y_loft = df['recommended_driver_loft']
y_flex = df['recommended_shaft_flex']

# データの分割
X_train, X_test, y_loft_train, y_loft_test = train_test_split(
    X, y_loft, test_size=0.2, random_state=42
)

# ロフト角予測モデルのトレーニング
loft_model = RandomForestRegressor(n_estimators=100, random_state=42)
loft_model.fit(X_train, y_loft_train)

# シャフトフレックス予測用のラベルエンコーディング
le_flex = LabelEncoder()
y_flex_encoded = le_flex.fit_transform(y_flex)

# シャフトフレックス予測モデルのトレーニング
X_train, X_test, y_flex_train, y_flex_test = train_test_split(
    X, y_flex_encoded, test_size=0.2, random_state=42
)

flex_model = RandomForestRegressor(n_estimators=100, random_state=42)
flex_model.fit(X_train, y_flex_train)

# モデルの評価
loft_score = loft_model.score(X_test, y_loft_test)
flex_score = flex_model.score(X_test, y_flex_test)

print(f"ロフト角予測モデルのR2スコア: {loft_score:.3f}")
print(f"シャフトフレックス予測モデルのR2スコア: {flex_score:.3f}")

# モデルの保存
os.makedirs("models", exist_ok=True)
joblib.dump(loft_model, "models/loft_model.pkl")
joblib.dump(flex_model, "models/flex_model.pkl")
joblib.dump(le_flex, "models/flex_label_encoder.pkl")

print("\nモデルを保存しました。")
print("- models/loft_model.pkl")
print("- models/flex_model.pkl")
print("- models/flex_label_encoder.pkl") 