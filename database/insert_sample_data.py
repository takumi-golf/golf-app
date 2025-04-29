import logging
from pathlib import Path
from db_manager import DatabaseManager
from db_connection import DatabaseConnection
import psycopg2
from psycopg2.extras import execute_values

def setup_logging():
    """ロギングの設定を行います。"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('database/insert_sample_data.log'),
            logging.StreamHandler()
        ]
    )

def insert_manufacturers(db_manager):
    """メーカーのサンプルデータを挿入します。"""
    manufacturers = [
        {
            'name': 'Titleist',
            'country': 'USA',
            'website': 'https://www.titleist.com',
            'established_year': 1932,
            'notes': 'プレミアムゴルフブランド'
        },
        {
            'name': 'Callaway',
            'country': 'USA',
            'website': 'https://www.callawaygolf.com',
            'established_year': 1982,
            'notes': '革新的なテクノロジーで知られる'
        },
        {
            'name': 'TaylorMade',
            'country': 'USA',
            'website': 'https://www.taylormadegolf.com',
            'established_year': 1979,
            'notes': 'ドライバーで有名'
        }
    ]
    
    for manufacturer in manufacturers:
        db_manager.insert_data('manufacturers', manufacturer)

def insert_series(db_manager):
    """シリーズのサンプルデータを挿入します。"""
    # メーカーIDを取得
    manufacturers = db_manager.execute_query("SELECT id, name FROM manufacturers")
    manufacturer_map = {m['name']: m['id'] for m in manufacturers}
    
    series = [
        {
            'manufacturer_id': manufacturer_map['Titleist'],
            'name': 'TSi Series',
            'release_year': 2021,
            'target_handicap_range': '0-20',
            'technology_description': 'ATI 425 Aerospace Titanium',
            'notes': '最新のドライバーシリーズ'
        },
        {
            'manufacturer_id': manufacturer_map['Callaway'],
            'name': 'Paradym Series',
            'release_year': 2023,
            'target_handicap_range': '0-25',
            'technology_description': 'AI-Designed Jailbreak',
            'notes': 'AIテクノロジー搭載'
        },
        {
            'manufacturer_id': manufacturer_map['TaylorMade'],
            'name': 'Stealth Series',
            'release_year': 2022,
            'target_handicap_range': '0-20',
            'technology_description': 'Carbonwood Technology',
            'notes': 'カーボン素材を採用'
        }
    ]
    
    for s in series:
        db_manager.insert_data('series', s)

def insert_models(db_manager):
    """モデルのサンプルデータを挿入します。"""
    # シリーズIDを取得
    series = db_manager.execute_query("""
        SELECT s.id, s.name, m.name as manufacturer_name 
        FROM series s
        JOIN manufacturers m ON s.manufacturer_id = m.id
    """)
    series_map = {(s['name'], s['manufacturer_name']): s['id'] for s in series}
    
    models = [
        {
            'series_id': series_map[('TSi Series', 'Titleist')],
            'name': 'TSi3',
            'club_type': 'Driver',
            'loft_range': '8.0-12.0',
            'length_range': '45.0-45.75',
            'weight_range': '305-315',
            'stock_shaft_options': 'Mitsubishi Tensei AV Raw Blue, Project X HZRDUS Smoke Black',
            'stock_grip_options': 'Golf Pride Tour Velvet',
            'msrp': 599.99,
            'release_year': 2021,
            'notes': '低スピン設計'
        },
        {
            'series_id': series_map[('Paradym Series', 'Callaway')],
            'name': 'Paradym',
            'club_type': 'Driver',
            'loft_range': '9.0-12.0',
            'length_range': '45.5-46.0',
            'weight_range': '300-310',
            'stock_shaft_options': 'Project X HZRDUS Silver, Mitsubishi Kai\'li White',
            'stock_grip_options': 'Golf Pride MCC',
            'msrp': 599.99,
            'release_year': 2023,
            'notes': 'AI最適化設計'
        },
        {
            'series_id': series_map[('Stealth Series', 'TaylorMade')],
            'name': 'Stealth Plus',
            'club_type': 'Driver',
            'loft_range': '8.0-12.0',
            'length_range': '45.5-46.0',
            'weight_range': '305-315',
            'stock_shaft_options': 'Fujikura Ventus Black, Mitsubishi Tensei 1K Black',
            'stock_grip_options': 'Golf Pride Z-Grip',
            'msrp': 599.99,
            'release_year': 2022,
            'notes': 'カーボンクラウン'
        }
    ]
    
    for model in models:
        db_manager.insert_data('models', model)

def insert_shafts(db_manager):
    """シャフトのサンプルデータを挿入します。"""
    # メーカーIDを取得
    manufacturers = db_manager.execute_query("SELECT id, name FROM manufacturers")
    manufacturer_map = {m['name']: m['id'] for m in manufacturers}
    
    shafts = [
        {
            'manufacturer_id': manufacturer_map['Mitsubishi Chemical'],
            'name': 'Tensei AV Raw Blue',
            'flex': 'S',
            'weight_range': '65-75',
            'material': 'グラファイト',
            'torque_range': '3.0-3.5',
            'kick_point': 'Mid',
            'notes': '中弾道設計'
        },
        {
            'manufacturer_id': manufacturer_map['Project X'],
            'name': 'HZRDUS Smoke Black',
            'flex': 'X',
            'weight_range': '60-70',
            'material': 'グラファイト',
            'torque_range': '2.5-3.0',
            'kick_point': 'Low',
            'notes': '低弾道設計'
        }
    ]
    
    for shaft in shafts:
        db_manager.insert_data('shafts', shaft)

def insert_grips(db_manager):
    """グリップのサンプルデータを挿入します。"""
    # メーカーIDを取得
    manufacturers = db_manager.execute_query("SELECT id, name FROM manufacturers")
    manufacturer_map = {m['name']: m['id'] for m in manufacturers}
    
    grips = [
        {
            'manufacturer_id': manufacturer_map['Golf Pride'],
            'name': 'Tour Velvet',
            'material': 'ラバー',
            'size_range': 'Standard, Midsize, Jumbo',
            'texture': 'スムース',
            'notes': 'クラシックなグリップ'
        },
        {
            'manufacturer_id': manufacturer_map['Golf Pride'],
            'name': 'MCC',
            'material': 'ラバー/コード',
            'size_range': 'Standard, Midsize, Jumbo',
            'texture': 'ハーフコード',
            'notes': '人気のハイブリッドグリップ'
        }
    ]
    
    for grip in grips:
        db_manager.insert_data('grips', grip)

def main():
    """サンプルデータの挿入を実行します。"""
    # ロギングの設定
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # データベースマネージャーの初期化
        db_manager = DatabaseManager()
        
        # サンプルデータの挿入
        logger.info("メーカーデータの挿入を開始します...")
        insert_manufacturers(db_manager)
        
        logger.info("シリーズデータの挿入を開始します...")
        insert_series(db_manager)
        
        logger.info("モデルデータの挿入を開始します...")
        insert_models(db_manager)
        
        logger.info("シャフトデータの挿入を開始します...")
        insert_shafts(db_manager)
        
        logger.info("グリップデータの挿入を開始します...")
        insert_grips(db_manager)
        
        logger.info("サンプルデータの挿入が完了しました。")
        
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        raise
    finally:
        # データベース接続のクローズ
        DatabaseConnection.close_connection()
        logger.info("データベース接続を閉じました。")

if __name__ == "__main__":
    main()

# データベース接続
conn = psycopg2.connect(
    dbname="golf_db",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

try:
    # メーカーデータの挿入
    cur.execute("INSERT INTO manufacturers (name) VALUES ('PING') RETURNING id")
    manufacturer_id = cur.fetchone()[0]

    # クラブデータの定義
    clubs_data = [
        {
            'model': 'G440 MAX',
            'head_volume': '460cc',
            'price': 107800,
            'features': ['8ポジション調整可能', 'Carbonfly Wrapクラウン'],
            'lofts': ['9°', '10.5°', '12°'],
            'shafts': [
                'ALTA J CB BLUE',
                'PING TOUR 2.0 CHROME',
                'PING TOUR 2.0 BLACK',
                'FUJIKURA SPEEDER NX GREY'
            ],
            'flexes': ['SR', 'R', 'S', 'X']
        },
        {
            'model': 'G440 SFT',
            'head_volume': '460cc',
            'price': 107800,
            'features': ['ドロー設計', '軽量バランス'],
            'lofts': ['9°', '10.5°'],
            'shafts': [
                'ALTA J CB BLUE',
                'PING TOUR 2.0 CHROME'
            ],
            'flexes': ['R', 'S']
        },
        {
            'model': 'G440 LST',
            'head_volume': '450cc',
            'price': 107800,
            'features': ['低スピン設計', '58°ライ角'],
            'lofts': ['9°', '10.5°'],
            'shafts': [
                'PING TOUR 2.0 CHROME 65',
                'FUJIKURA SPEEDER NX'
            ],
            'flexes': ['S', 'X']
        },
        {
            'model': 'G440 HL',
            'head_volume': '460cc',
            'price': 107800,
            'features': ['軽量設計（295g）', '高弾道'],
            'lofts': ['10.5°', '12°'],
            'shafts': [
                'ALTA J CB BLUE LITE',
                'PING TOUR 2.0 CHROME LITE'
            ],
            'flexes': ['SR', 'R']
        }
    ]

    # 各クラブのデータを挿入
    for club in clubs_data:
        # クラブ基本情報の挿入
        cur.execute("""
            INSERT INTO clubs (manufacturer_id, model, head_volume, price, features)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (manufacturer_id, club['model'], club['head_volume'], club['price'], club['features']))
        club_id = cur.fetchone()[0]

        # ロフト角の挿入
        execute_values(cur, """
            INSERT INTO lofts (club_id, loft)
            VALUES %s
        """, [(club_id, loft) for loft in club['lofts']])

        # シャフトの挿入
        execute_values(cur, """
            INSERT INTO shafts (club_id, shaft)
            VALUES %s
        """, [(club_id, shaft) for shaft in club['shafts']])

        # フレックスの挿入
        execute_values(cur, """
            INSERT INTO flexes (club_id, flex)
            VALUES %s
        """, [(club_id, flex) for flex in club['flexes']])

    # 変更をコミット
    conn.commit()
    print("データの挿入が完了しました")

except Exception as e:
    print(f"エラーが発生しました: {e}")
    conn.rollback()

finally:
    # 接続を閉じる
    cur.close()
    conn.close() 