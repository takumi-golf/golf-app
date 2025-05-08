from sqlalchemy.orm import Session
from ..models.club import Club

def init_db(db: Session):
    # ドライバー
    db.add(Club(
        name="TSR2",
        brand="Titleist",
        club_type="driver",
        loft=9.0,
        length=45.5,
        lie=58.5,
        shaft_flex="Regular",
        shaft_material="Graphite",
        grip_type="Golf Pride Tour Velvet",
        price=65000,
        description="高反発で飛距離が出る最新モデル",
        image_url="https://example.com/tsr2.jpg"
    ))

    # フェアウェイウッド
    db.add(Club(
        name="SIM2 Max 3-Wood",
        brand="TaylorMade",
        club_type="fairway",
        loft=15.0,
        length=43.0,
        lie=58.0,
        shaft_flex="Regular",
        shaft_material="Graphite",
        grip_type="Golf Pride Tour Velvet",
        price=45000,
        description="高反発フェアウェイウッド。ティーショットとセカンドショットの両方で使用可能。",
        image_url="https://example.com/sim2_3w.jpg"
    ))

    db.add(Club(
        name="SIM2 Max 5-Wood",
        brand="TaylorMade",
        club_type="fairway",
        loft=18.0,
        length=42.0,
        lie=58.5,
        shaft_flex="Regular",
        shaft_material="Graphite",
        grip_type="Golf Pride Tour Velvet",
        price=45000,
        description="高反発フェアウェイウッド。セカンドショットやロングアプローチに最適。",
        image_url="https://example.com/sim2_5w.jpg"
    ))

    # ユーティリティ
    db.add(Club(
        name="SIM2 Max Rescue",
        brand="TaylorMade",
        club_type="utility",
        loft=21.0,
        length=40.0,
        lie=59.0,
        shaft_flex="Regular",
        shaft_material="Graphite",
        grip_type="Golf Pride Tour Velvet",
        price=35000,
        description="高反発ユーティリティ。ロングアイアンの代替として使用可能。",
        image_url="https://example.com/sim2_rescue.jpg"
    ))

    # アイアン
    db.add(Club(
        name="T200",
        brand="Titleist",
        club_type="iron",
        loft=30.0,
        length=37.5,
        lie=62.0,
        shaft_flex="Regular",
        shaft_material="Steel",
        grip_type="Golf Pride Tour Velvet",
        price=45000,
        description="初心者でも扱いやすいアイアン",
        image_url="https://example.com/t200.jpg"
    ))

    # ウェッジ
    db.add(Club(
        name="Vokey SM9",
        brand="Titleist",
        club_type="wedge",
        loft=56.0,
        length=35.5,
        lie=64.0,
        shaft_flex="Regular",
        shaft_material="Steel",
        grip_type="Golf Pride Tour Velvet",
        price=35000,
        description="高いスピン性能を持つウェッジ",
        image_url="https://example.com/sm9.jpg"
    ))

    # パター
    db.add(Club(
        name="Scotty Cameron",
        brand="Titleist",
        club_type="putter",
        loft=3.0,
        length=34.0,
        lie=70.0,
        shaft_flex="Regular",
        shaft_material="Steel",
        grip_type="Scotty Cameron Pistolero",
        price=55000,
        description="プロも使用する高級パター",
        image_url="https://example.com/scotty.jpg"
    ))

    db.commit() 