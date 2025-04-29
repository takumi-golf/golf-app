from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional
import os
from pydantic import BaseModel, Field
import pickle
import numpy as np
from contextlib import contextmanager
from app.schemas.club import ClubRecommendation

# ユーザープロファイルのモデル
class UserProfile(BaseModel):
    height: float = Field(..., gt=0, le=250, description="身長（cm）")
    weight: float = Field(..., gt=0, le=200, description="体重（kg）")
    age: int = Field(..., gt=0, le=120, description="年齢")
    gender: str = Field(..., description="性別")
    handicap: Optional[float] = Field(None, ge=0, le=54, description="ハンディキャップ")
    head_speed: Optional[float] = Field(None, ge=0, le=200, description="ヘッドスピード（m/s）")
    ball_speed: Optional[float] = Field(None, ge=0, le=300, description="ボールスピード（m/s）")
    launch_angle: Optional[float] = Field(None, ge=0, le=90, description="打ち出し角（度）")
    swing_issue: Optional[str] = Field(None, description="スイングの課題")
    budget: Optional[float] = Field(None, ge=0, description="予算（円）")

# データベース接続情報
DB_CONFIG = {
    "dbname": "golf_db",
    "user": "postgres",
    "password": "WecA4JagjpsziLi2_N9g",
    "host": "localhost",
    "port": "5432",
    "cursor_factory": RealDictCursor
}

@contextmanager
def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

# モデルの読み込み
try:
    with open('models/flex_model.pkl', 'rb') as f:
        flex_model = pickle.load(f)
    with open('models/flex_label_encoder.pkl', 'rb') as f:
        flex_label_encoder = pickle.load(f)
    with open('models/flex_scaler.pkl', 'rb') as f:
        flex_scaler = pickle.load(f)
    with open('models/loft_model.pkl', 'rb') as f:
        loft_model = pickle.load(f)
except Exception as e:
    print(f"Warning: Failed to load models: {e}")
    flex_model = None
    flex_label_encoder = None
    flex_scaler = None
    loft_model = None

app = FastAPI(
    title="SwingFitPro API",
    description="ゴルフクラブ推奨システムのAPI",
    version="1.0.0"
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静的ファイルの設定
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    return FileResponse("app/templates/index.html")

@app.get("/api/manufacturers", response_model=List[Dict[str, Any]])
async def get_manufacturers():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM manufacturers")
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データベースエラー: {str(e)}")

@app.get("/api/clubs", response_model=List[ClubRecommendation])
async def get_clubs():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        c.id,
                        m.name as manufacturer,
                        c.model,
                        c.head_volume,
                        c.price,
                        c.features,
                        l.loft,
                        s.shaft,
                        f.flex
                    FROM clubs c
                    JOIN manufacturers m ON c.manufacturer_id = m.id
                    LEFT JOIN lofts l ON c.id = l.club_id
                    LEFT JOIN shafts s ON c.id = s.club_id
                    LEFT JOIN flexes f ON c.id = f.club_id
                """)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データベースエラー: {str(e)}")

@app.get("/api/lofts")
async def get_lofts():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT l.id, c.model, l.loft
            FROM lofts l
            JOIN clubs c ON l.club_id = c.id
            ORDER BY c.model, l.loft
        """)
        lofts = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": l[0], "model": l[1], "loft": l[2]} for l in lofts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/shafts")
async def get_shafts():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id, c.model, s.shaft
            FROM shafts s
            JOIN clubs c ON s.club_id = c.id
            ORDER BY c.model, s.shaft
        """)
        shafts = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": s[0], "model": s[1], "shaft": s[2]} for s in shafts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/flexes")
async def get_flexes():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT f.id, c.model, f.flex
            FROM flexes f
            JOIN clubs c ON f.club_id = c.id
            ORDER BY c.model, f.flex
        """)
        flexes = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": f[0], "model": f[1], "flex": f[2]} for f in flexes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def determine_flex(swing_speed: float) -> str:
    try:
        if flex_model is None or flex_label_encoder is None or flex_scaler is None:
            # モデルが利用できない場合はフォールバック
            if swing_speed < 80:
                return "SR"
            elif swing_speed < 90:
                return "R"
            elif swing_speed < 100:
                return "S"
            else:
                return "X"
        
        # 入力データを2次元配列に変換
        swing_speed_array = np.array([[swing_speed]])
        # データの標準化
        swing_speed_scaled = flex_scaler.transform(swing_speed_array)
        # 予測を実行
        predicted_flex = flex_model.predict(swing_speed_scaled)
        # ラベルを逆変換
        return flex_label_encoder.inverse_transform(predicted_flex)[0]
    except Exception as e:
        print(f"Warning: Flex prediction failed: {e}")
        return "R"  # デフォルト値

def determine_loft(spin_rate: float, launch_angle: float) -> float:
    try:
        if loft_model is None:
            # モデルが利用できない場合はフォールバック
            if spin_rate > 3000 and launch_angle < 10:
                return 9.0
            elif spin_rate > 3000 and launch_angle >= 10:
                return 10.5
            elif spin_rate <= 3000 and launch_angle < 10:
                return 10.5
            else:
                return 12.0
        
        # 入力データを2次元配列に変換
        features = np.array([[spin_rate, launch_angle]])
        # 予測を実行
        predicted_loft = loft_model.predict(features)
        return float(predicted_loft[0])
    except Exception as e:
        print(f"Warning: Loft prediction failed: {e}")
        return 10.5  # デフォルト値

def determine_club_type(miss_shot: str, shot_shape: str, handicap: int) -> str:
    if handicap > 20:
        return "MAX"  # 初心者向けの最大寛容性
    
    if miss_shot == "スライス":
        return "SFT" if handicap > 15 else "LST"  # 上級者には低スピンタイプを推奨
    elif miss_shot == "フック":
        return "LST"
    elif shot_shape == "低弾道":
        return "HL"
    elif handicap < 10:
        return "LST"  # 上級者向けの低スピンタイプ
    else:
        return "MAX"

@app.post("/api/recommend", response_model=ClubRecommendation)
async def recommend_clubs(profile: UserProfile):
    try:
        # 推奨パラメータの決定
        flex = determine_flex(profile.head_speed if profile.head_speed else 40.0)
        loft = determine_loft(profile.ball_speed or 0.0, profile.launch_angle or 0.0)
        club_type = determine_club_type(profile.swing_issue or "なし", "", profile.handicap or 28)
        
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # ドライバーの検索
                cur.execute("""
                    SELECT DISTINCT
                        c.id,
                        m.name as manufacturer,
                        c.model,
                        c.head_volume,
                        c.price,
                        c.features,
                        l.loft,
                        s.shaft,
                        f.flex,
                        'driver' as club_type
                    FROM clubs c
                    JOIN manufacturers m ON c.manufacturer_id = m.id
                    LEFT JOIN lofts l ON c.id = l.club_id
                    LEFT JOIN shafts s ON c.id = s.club_id
                    LEFT JOIN flexes f ON c.id = f.club_id
                    WHERE c.type = 'driver'
                    AND c.price <= %s
                    AND (f.flex = %s OR f.flex IS NULL)
                    AND (ABS(l.loft - %s) <= 1.5 OR l.loft IS NULL)
                    ORDER BY c.price DESC
                    LIMIT 1
                """, (profile.budget or 1000000, flex, loft))
                
                driver = cur.fetchone()

                # その他のクラブの検索（woods, utilities, irons, wedges, putter）
                club_types = ['wood', 'utility', 'iron', 'wedge', 'putter']
                results = {}
                
                for club_type in club_types:
                    cur.execute("""
                        SELECT DISTINCT
                            c.id,
                            m.name as manufacturer,
                            c.model,
                            c.head_volume,
                            c.price,
                            c.features,
                            l.loft,
                            s.shaft,
                            f.flex,
                            %s as club_type
                        FROM clubs c
                        JOIN manufacturers m ON c.manufacturer_id = m.id
                        LEFT JOIN lofts l ON c.id = l.club_id
                        LEFT JOIN shafts s ON c.id = s.club_id
                        LEFT JOIN flexes f ON c.id = f.club_id
                        WHERE c.type = %s
                        AND c.price <= %s
                        AND (f.flex = %s OR f.flex IS NULL)
                        ORDER BY c.price DESC
                        LIMIT 3
                    """, (club_type, club_type, profile.budget or 1000000, flex))
                    
                    results[club_type + 's'] = cur.fetchall()

        # 結果の整形
        total_price = (driver['price'] if driver else 0) + \
                     sum(club['price'] for clubs in results.values() for club in clubs)
        
        confidence_score = 0.85  # モックの信頼度スコア

        return {
            "driver": driver or {},
            "woods": results.get('woods', []),
            "utilities": results.get('utilities', []),
            "irons": results.get('irons', []),
            "wedges": results.get('wedges', []),
            "putter": results.get('putters', [])[-1] if results.get('putters') else {},
            "total_price": total_price,
            "confidence_score": confidence_score
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推奨処理エラー: {str(e)}")

@app.get("/api/debug/database")
async def debug_database():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # メーカーテーブルの内容を確認
                cur.execute("SELECT * FROM manufacturers")
                manufacturers = cur.fetchall()
                
                # クラブテーブルの内容を確認
                cur.execute("SELECT * FROM clubs")
                clubs = cur.fetchall()
                
                # ロフトテーブルの内容を確認
                cur.execute("SELECT * FROM lofts")
                lofts = cur.fetchall()
                
                # シャフトテーブルの内容を確認
                cur.execute("SELECT * FROM shafts")
                shafts = cur.fetchall()
                
                # フレックステーブルの内容を確認
                cur.execute("SELECT * FROM flexes")
                flexes = cur.fetchall()
                
                return {
                    "manufacturers": manufacturers,
                    "clubs": clubs,
                    "lofts": lofts,
                    "shafts": shafts,
                    "flexes": flexes
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データベースデバッグエラー: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003) 