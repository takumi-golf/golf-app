from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Club, Base
from config import DATABASE_URL
from datetime import datetime

def insert_sample_data():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # サンプルデータの作成
        sample_clubs = [
            # ドライバー
            Club(
                brand="Titleist",
                model="TSi3",
                type="driver",
                loft=9.5,
                shaft="Diamana",
                shaft_flex="S",
                price=50000,
                features="低スピン設計で安定した飛距離を実現",
                trajectory="中弾道",
                spin="低スピン",
                forgiveness="中"
            ),
            Club(
                brand="Callaway",
                model="Epic Max",
                type="driver",
                loft=10.5,
                shaft="Project X",
                shaft_flex="R",
                price=48000,
                features="AI設計による最適化されたヘッド形状",
                trajectory="高弾道",
                spin="中スピン",
                forgiveness="高"
            ),
            Club(
                brand="TaylorMade",
                model="SIM2",
                type="driver",
                loft=9.0,
                shaft="Fujikura",
                shaft_flex="S",
                price=52000,
                features="スピードポケットによる高初速",
                trajectory="中弾道",
                spin="低スピン",
                forgiveness="中"
            ),
            # フェアウェイウッド
            Club(
                brand="Titleist",
                model="TSi2",
                type="wood",
                loft=15.0,
                shaft="Diamana",
                shaft_flex="S",
                price=40000,
                features="高弾道で着地性が良い",
                trajectory="高弾道",
                spin="中スピン",
                forgiveness="高"
            ),
            Club(
                brand="Callaway",
                model="Epic Speed",
                type="wood",
                loft=15.0,
                shaft="Project X",
                shaft_flex="R",
                price=38000,
                features="ジャストミートで高初速",
                trajectory="中弾道",
                spin="低スピン",
                forgiveness="中"
            ),
            Club(
                brand="TaylorMade",
                model="SIM2 Max",
                type="wood",
                loft=15.0,
                shaft="Fujikura",
                shaft_flex="S",
                price=42000,
                features="高慣性モーメントで安定性抜群",
                trajectory="高弾道",
                spin="中スピン",
                forgiveness="高"
            ),
            # ユーティリティ
            Club(
                brand="Titleist",
                model="U505",
                type="utility",
                loft=21.0,
                shaft="Dynamic Gold",
                shaft_flex="S",
                price=35000,
                features="アイアンライクな打感で使いやすい",
                trajectory="中弾道",
                spin="中スピン",
                forgiveness="中"
            ),
            Club(
                brand="Callaway",
                model="Apex UW",
                type="utility",
                loft=21.0,
                shaft="Project X",
                shaft_flex="R",
                price=33000,
                features="高弾道で着地性が良い",
                trajectory="高弾道",
                spin="中スピン",
                forgiveness="高"
            ),
            # アイアン
            Club(
                brand="Titleist",
                model="T200",
                type="iron",
                loft=24.0,
                shaft="Dynamic Gold",
                shaft_flex="S",
                price=120000,
                features="フォルジングで打感が良い",
                trajectory="中弾道",
                spin="中スピン",
                forgiveness="中"
            ),
            Club(
                brand="Callaway",
                model="Apex 21",
                type="iron",
                loft=24.0,
                shaft="Project X",
                shaft_flex="R",
                price=110000,
                features="AI設計による最適化されたヘッド形状",
                trajectory="高弾道",
                spin="中スピン",
                forgiveness="高"
            ),
            Club(
                brand="TaylorMade",
                model="P790",
                type="iron",
                loft=24.0,
                shaft="Dynamic Gold",
                shaft_flex="S",
                price=115000,
                features="スピードフォイルによる高初速",
                trajectory="中弾道",
                spin="低スピン",
                forgiveness="中"
            ),
            # ウェッジ
            Club(
                brand="Titleist",
                model="Vokey SM8",
                type="wedge",
                loft=46.0,
                shaft="Dynamic Gold",
                shaft_flex="S",
                price=20000,
                features="スピン性能が高い",
                trajectory="中弾道",
                spin="高スピン",
                forgiveness="低"
            ),
            Club(
                brand="Callaway",
                model="Jaws MD5",
                type="wedge",
                loft=46.0,
                shaft="Project X",
                shaft_flex="R",
                price=18000,
                features="グローブスピンでコントロール性が高い",
                trajectory="中弾道",
                spin="高スピン",
                forgiveness="低"
            ),
            # パター
            Club(
                brand="Scotty Cameron",
                model="Special Select",
                type="putter",
                loft=3.0,
                shaft="Steel",
                shaft_flex="-",
                price=50000,
                features="安定したストロークが可能",
                trajectory="ロー",
                spin="ロー",
                forgiveness="中"
            ),
            Club(
                brand="Odyssey",
                model="White Hot OG",
                type="putter",
                loft=3.0,
                shaft="Steel",
                shaft_flex="-",
                price=35000,
                features="ホワイトホットインサートで安定した打感",
                trajectory="ロー",
                spin="ロー",
                forgiveness="高"
            )
        ]

        # データベースに挿入
        for club in sample_clubs:
            db.add(club)
        
        db.commit()
        print("サンプルデータの挿入が完了しました。")

    finally:
        db.close()

if __name__ == "__main__":
    insert_sample_data() 