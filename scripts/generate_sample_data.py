import pandas as pd
import numpy as np

# シード値を設定して再現性を確保
np.random.seed(42)

# サンプルデータの生成
n_samples = 1000

data = {
    'height': np.random.normal(170, 10, n_samples),  # 身長（cm）
    'weight': np.random.normal(65, 15, n_samples),   # 体重（kg）
    'age': np.random.randint(18, 70, n_samples),     # 年齢
    'gender': np.random.choice(['male', 'female'], n_samples),  # 性別
    'handicap': np.random.uniform(0, 36, n_samples),  # ハンディキャップ
    'head_speed': np.random.uniform(30, 60, n_samples),  # ヘッドスピード（m/s）
    'ball_speed': None,  # ボールスピード（後で計算）
    'launch_angle': np.random.uniform(8, 16, n_samples),  # 打ち出し角度（度）
}

# ボールスピードの計算（ヘッドスピードの約1.5倍）
data['ball_speed'] = data['head_speed'] * 1.5 + np.random.normal(0, 2, n_samples)

# 推奨クラブパラメータの生成
# ヘッドスピードとハンディキャップに基づいてロフト角を決定
def calculate_recommended_loft(head_speed, handicap):
    base_loft = 10.5
    # ヘッドスピードが遅いほど、ハンディキャップが高いほどロフト角を大きく
    speed_adjustment = (45 - head_speed) * 0.1
    handicap_adjustment = handicap * 0.05
    return base_loft + speed_adjustment + handicap_adjustment

data['recommended_driver_loft'] = [
    calculate_recommended_loft(hs, hc) 
    for hs, hc in zip(data['head_speed'], data['handicap'])
]

# シャフトフレックスの決定
def determine_shaft_flex(head_speed):
    if head_speed >= 50:
        return 'X'
    elif head_speed >= 45:
        return 'S'
    elif head_speed >= 40:
        return 'R'
    else:
        return 'A'

data['recommended_shaft_flex'] = [
    determine_shaft_flex(hs) for hs in data['head_speed']
]

# データフレームの作成と保存
df = pd.DataFrame(data)
df.to_csv("golf_fitting_data.csv", index=False)

print("サンプルデータを生成しました。")
print(f"データ件数: {len(df)}")
print("\nデータの概要:")
print(df.describe()) 