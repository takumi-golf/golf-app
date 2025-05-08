from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from ..database.database import Base

class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String, index=True)
    club_type = Column(String, index=True)
    loft = Column(Float)  # ロフト角
    length = Column(Float)  # シャフト長
    lie = Column(Float)
    shaft_flex = Column(String)
    shaft_material = Column(String)
    grip_type = Column(String)
    price = Column(Integer)  # 価格
    description = Column(String)  # 説明
    image_url = Column(String, nullable=True)  # 画像URL 