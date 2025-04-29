from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db, search_clubs, get_club_by_id, get_clubs_by_type, get_clubs_by_brand, update_club_popularity, get_popular_clubs
from ..schemas.club import ClubResponse, ClubSearch, ClubRecommendation, ClubSearchResponse
from ..models import Club
import json
from fastapi.templating import Jinja2Templates
from app.utils.templates import TemplateManager

router = APIRouter(
    prefix="/clubs",
    tags=["clubs"],
    responses={404: {"description": "Not found"}},
)

template_manager = TemplateManager()
templates = template_manager.get_templates()
analytics = template_manager.get_analytics()

@router.get("/", response_model=List[ClubResponse])
async def get_clubs(
    skip: int = 0,
    limit: int = 10,
    type: Optional[str] = None,
    brand: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """クラブ一覧を取得"""
    if type:
        clubs = get_clubs_by_type(db, type, skip, limit)
    elif brand:
        clubs = get_clubs_by_brand(db, brand, skip, limit)
    else:
        clubs = search_clubs(db, skip=skip, limit=limit)
    return clubs

@router.get("/{club_id}", response_model=ClubResponse)
async def get_club(club_id: str, db: Session = Depends(get_db)):
    """特定のクラブの詳細を取得"""
    club = get_club_by_id(db, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    # 人気度を更新
    update_club_popularity(db, club_id)
    return club

@router.get("/popular", response_model=List[ClubResponse])
async def get_popular_clubs_list(
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """人気のクラブ一覧を取得"""
    return get_popular_clubs(db, limit)

@router.post("/search", response_model=ClubSearchResponse)
async def search_clubs_endpoint(
    search: ClubSearch,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """条件に基づいてクラブを検索"""
    clubs = search_clubs(
        db,
        type=search.type,
        brand=search.brand,
        min_price=search.min_price,
        max_price=search.max_price,
        skip=skip,
        limit=limit
    )
    total_count = db.query(Club).count()
    return ClubSearchResponse(
        clubs=clubs,
        total_count=total_count,
        page=skip // limit + 1,
        per_page=limit
    )

@router.post("/recommend", response_model=List[ClubRecommendation])
async def recommend_clubs(
    search: ClubSearch,
    db: Session = Depends(get_db)
):
    """ユーザーの条件に基づいてクラブをレコメンド"""
    # 基本的なフィルタリング
    clubs = search_clubs(
        db,
        type=search.type,
        brand=search.brand,
        min_price=search.min_price,
        max_price=search.max_price
    )
    
    recommendations = []
    
    for club in clubs:
        # 特徴の解析
        features = json.loads(club.features)
        score = 0
        match_reasons = []
        
        # スイングスピードに基づくスコアリング
        if search.swing_speed:
            if features.get("trajectory") == "高弾道" and search.swing_speed < 40:
                score += 2
                match_reasons.append("スイングスピードに適合: 高弾道")
            elif features.get("trajectory") == "中弾道" and 40 <= search.swing_speed <= 45:
                score += 2
                match_reasons.append("スイングスピードに適合: 中弾道")
            elif features.get("trajectory") == "低弾道" and search.swing_speed > 45:
                score += 2
                match_reasons.append("スイングスピードに適合: 低弾道")
        
        # スピン特性に基づくスコアリング
        if search.spin_preference and features.get("spin") == search.spin_preference:
            score += 1
            match_reasons.append(f"スピン特性: {features.get('spin')}")
        
        # 容錯性に基づくスコアリング
        if search.forgiveness_preference and features.get("forgiveness") == search.forgiveness_preference:
            score += 1
            match_reasons.append(f"容錯性: {features.get('forgiveness')}")
        
        # 人気度をスコアに反映
        score += club.popularity_score
        
        recommendations.append({
            "club": club,
            "score": score,
            "match_reasons": match_reasons
        })
    
    # スコアでソート
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    
    return recommendations

@router.get("/")
async def list_clubs(
    request: Request,
    db: Session = Depends(get_db)
):
    """クラブ一覧を表示"""
    clubs = db.query(Club).all()
    
    # ページビューのトラッキング
    page_view_script = analytics.track_page_view("/clubs", "クラブ一覧")
    
    context = template_manager.get_template_context(
        request,
        clubs=clubs,
        page_view_script=page_view_script
    )
    
    return templates.TemplateResponse(
        "clubs/list.html",
        context
    )

@router.get("/search")
async def search_clubs(
    request: Request,
    query: str = "",
    db: Session = Depends(get_db)
):
    """クラブを検索"""
    clubs = db.query(Club).filter(Club.name.ilike(f"%{query}%")).all()
    
    # 検索イベントのトラッキング
    event_script = analytics.track_event(
        "club_search",
        {"query": query}
    )
    
    context = template_manager.get_template_context(
        request,
        clubs=clubs,
        query=query,
        event_script=event_script
    )
    
    return templates.TemplateResponse(
        "clubs/search.html",
        context
    )

@router.get("/{club_id}")
async def get_club(
    request: Request,
    club_id: int,
    db: Session = Depends(get_db)
):
    """クラブの詳細を表示"""
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        # エラーのトラッキング
        error_script = analytics.track_error(
            "club_not_found",
            f"Club ID {club_id} not found"
        )
        context = template_manager.get_template_context(
            request,
            error_script=error_script
        )
        return templates.TemplateResponse(
            "error.html",
            context,
            status_code=404
        )
    
    # クラブ詳細ページのトラッキング
    page_view_script = analytics.track_page_view(
        f"/clubs/{club_id}",
        f"{club.name} - 詳細"
    )
    
    context = template_manager.get_template_context(
        request,
        club=club,
        page_view_script=page_view_script
    )
    
    return templates.TemplateResponse(
        "clubs/detail.html",
        context
    ) 