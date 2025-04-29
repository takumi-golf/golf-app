import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle

# フレックスモデルの生成
def generate_flex_model():
    # サンプルデータの生成
    swing_speeds = np.array([40, 50, 60, 70, 75, 80, 85, 90, 95, 100, 105, 110, 120, 130]).reshape(-1, 1)
    flex_labels = ['L', 'L', 'A', 'SR', 'R', 'R', 'S', 'S', 'S', 'X', 'X', 'X', 'XX', 'XX']
    
    # データの標準化
    scaler = StandardScaler()
    swing_speeds_scaled = scaler.fit_transform(swing_speeds)
    
    # ラベルエンコーダーの生成
    label_encoder = LabelEncoder()
    flex_encoded = label_encoder.fit_transform(flex_labels)
    
    # モデルの生成（LogisticRegressionに変更）
    model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
    model.fit(swing_speeds_scaled, flex_encoded)
    
    # モデルの保存
    with open('models/flex_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # ラベルエンコーダーの保存
    with open('models/flex_label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    
    # スケーラーの保存
    with open('models/flex_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

# ロフトモデルの生成
def generate_loft_model():
    # サンプルデータの生成
    spin_rates = np.array([2000, 2500, 3000, 3500, 4000, 4500, 5000])
    launch_angles = np.array([8, 9, 10, 11, 12, 13, 14])
    lofts = np.array([9.0, 9.5, 10.5, 10.5, 12.0, 12.0, 12.0])
    
    # 特徴量の結合
    X = np.column_stack((spin_rates, launch_angles))
    
    # モデルの生成
    model = LinearRegression()
    model.fit(X, lofts)
    
    # モデルの保存
    with open('models/loft_model.pkl', 'wb') as f:
        pickle.dump(model, f)

if __name__ == '__main__':
    generate_flex_model()
    generate_loft_model()
    print("モデルの生成が完了しました。") 