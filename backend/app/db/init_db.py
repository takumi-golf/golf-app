from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..models.club import Brand, ClubModel, ClubSpecification, Shaft
from ..db.database import Base, engine
import os
import logging
from sqlalchemy.sql import func

logger = logging.getLogger(__name__)

def init_db():
    """データベースの初期化"""
    try:
        # 既存のテーブルを削除
        Base.metadata.drop_all(bind=engine)
        logger.info("既存のテーブルを削除しました。")
        
        # テーブルの作成
        Base.metadata.create_all(bind=engine)
        logger.info("データベースのテーブルを作成しました。")
        
        # セッションの作成
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # シードデータの投入
        init_seed_data(db)
        
    except Exception as e:
        logger.error(f"データベースの初期化中にエラーが発生しました: {str(e)}")
        raise
    finally:
        db.close()

def seed_brands(db: Session):
    """ブランドのシードデータ投入"""
    brands = [
        Brand(
            name="Titleist",
            logo_path="/images/brands/titleist.png",
            created_at=func.now(),
            updated_at=func.now()
        ),
        Brand(
            name="TaylorMade",
            logo_path="/images/brands/taylormade.png",
            created_at=func.now(),
            updated_at=func.now()
        ),
        Brand(
            name="PING",
            logo_path="/images/brands/ping.png",
            created_at=func.now(),
            updated_at=func.now()
        ),
        Brand(
            name="Callaway",
            logo_path="/images/brands/callaway.png",
            created_at=func.now(),
            updated_at=func.now()
        )
    ]
    
    for brand in brands:
        db.add(brand)
    db.commit()
    print("ブランドデータを投入しました。")

def seed_club_models(db: Session):
    """クラブモデルのシードデータ投入"""
    titleist = db.query(Brand).filter(Brand.name == "Titleist").first()
    if not titleist:
        print("Titleistブランドが見つかりません。")
        return
    
    models = [
        ClubModel(
            name="TSR3",
            brand_id=titleist.id,
            release_year=2023,
            type="driver",
            category="player"
        ),
        ClubModel(
            name="T200",
            brand_id=titleist.id,
            release_year=2023,
            type="iron",
            category="game_improvement"
        )
    ]
    
    for model in models:
        db.add(model)
    db.commit()
    print("クラブモデルデータを投入しました。")

def seed_shafts(db: Session):
    """シャフトのシードデータ投入"""
    shafts = [
        Shaft(
            brand="Fujikura",
            model="Ventus Red",
            flex="S",
            weight=65.0,
            torque=4.2,
            kick_point="mid",
            description="中弾道で安定した方向性を実現するシャフト"
        ),
        Shaft(
            brand="True Temper",
            model="Dynamic Gold",
            flex="X100",
            weight=130.0,
            torque=2.0,
            kick_point="low",
            description="低弾道で安定性の高いスチールシャフト"
        )
    ]
    
    for shaft in shafts:
        db.add(shaft)
    db.commit()
    print("シャフトデータを投入しました。")

def seed_club_specifications(db: Session):
    """クラブスペックのシードデータ投入"""
    # 既存のデータを確認
    existing_specs = db.query(ClubSpecification).all()
    if existing_specs:
        print("既存のクラブスペックデータが存在します。スキップします。")
        return

    # TSR3ドライバーのスペック
    tsr3 = db.query(ClubModel).filter(ClubModel.name == "TSR3").first()
    if not tsr3:
        print("TSR3モデルが見つかりません。")
        return

    ventus_red = db.query(Shaft).filter(Shaft.model == "Ventus Red").first()
    if not ventus_red:
        print("Ventus Redシャフトが見つかりません。")
        return
    
    # T200アイアンのスペック
    t200 = db.query(ClubModel).filter(ClubModel.name == "T200").first()
    if not t200:
        print("T200モデルが見つかりません。")
        return

    dynamic_gold = db.query(Shaft).filter(Shaft.model == "Dynamic Gold").first()
    if not dynamic_gold:
        print("Dynamic Goldシャフトが見つかりません。")
        return
    
    specifications = [
        # TSR3ドライバースペック
        ClubSpecification(
            club_model_id=tsr3.id,
            club_type="driver",
            club_number="1W",
            loft=9.0,
            lie_angle=58.5,
            length=45.5,
            head_weight=195.0,
            swing_weight="D3",
            shaft_id=ventus_red.id,
            face_angle=0.0,
            offset=None,
            bounce_angle=None
        ),
        ClubSpecification(
            club_model_id=tsr3.id,
            club_type="driver",
            club_number="1W",
            loft=10.5,
            lie_angle=58.5,
            length=45.5,
            head_weight=195.0,
            swing_weight="D3",
            shaft_id=ventus_red.id,
            face_angle=0.0,
            offset=None,
            bounce_angle=None
        ),
        # T200アイアンスペック
        ClubSpecification(
            club_model_id=t200.id,
            club_type="iron",
            club_number="7i",
            loft=30.0,
            lie_angle=63.0,
            length=37.0,
            head_weight=262.0,
            swing_weight="D2",
            shaft_id=dynamic_gold.id,
            face_angle=0.0,
            offset=3.5,
            bounce_angle=4.0
        )
    ]
    
    for spec in specifications:
        db.add(spec)
    db.commit()
    print("クラブスペックデータを投入しました。")

def init_seed_data(db: Session):
    """全てのシードデータを投入"""
    try:
        # 既存のデータを確認
        existing_brands = db.query(Brand).first()
        if existing_brands:
            logger.info("既存のデータが存在するため、シードデータの投入をスキップします。")
            return
        
        # シードデータの投入
        seed_brands(db)
        seed_club_models(db)
        seed_shafts(db)
        seed_club_specifications(db)
        
    except Exception as e:
        logger.error(f"シードデータの投入中にエラーが発生しました: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("データベースを初期化しています...")
    init_db()
    logger.info("データベースの初期化が完了しました。") 