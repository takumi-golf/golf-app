from sqlalchemy.orm import Query, joinedload, selectinload
from sqlalchemy import func, and_, or_, desc, asc
from typing import List, Optional, Any, Dict
import logging
from database import User, Club, Recommendation, Base

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('query_optimization.log'),
        logging.StreamHandler()
    ]
)

class QueryOptimizer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def optimize_user_query(query: Query) -> Query:
        """
        ユーザー関連のクエリを最適化
        :param query: 最適化するクエリ
        :return: 最適化されたクエリ
        """
        return query.execution_options(
            lazyload_relations=False,
            enable_eagerloads=True
        )

    @staticmethod
    def optimize_club_query(query: Query) -> Query:
        """
        クラブ関連のクエリを最適化
        :param query: 最適化するクエリ
        :return: 最適化されたクエリ
        """
        return query.execution_options(
            lazyload_relations=False,
            enable_eagerloads=True
        )

    @staticmethod
    def optimize_recommendation_query(query: Query) -> Query:
        """
        レコメンデーション関連のクエリを最適化
        :param query: 最適化するクエリ
        :return: 最適化されたクエリ
        """
        return query.execution_options(
            lazyload_relations=False,
            enable_eagerloads=True
        )

    @staticmethod
    def add_pagination(query: Query, page: int, page_size: int) -> Query:
        """
        ページネーションを追加
        :param query: クエリ
        :param page: ページ番号
        :param page_size: 1ページあたりのアイテム数
        :return: ページネーションされたクエリ
        """
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10
        return query.offset((page - 1) * page_size).limit(page_size)

    @staticmethod
    def add_filters(query: Query, filters: Dict[str, Any]) -> Query:
        """
        フィルターを追加
        :param query: クエリ
        :param filters: フィルター条件の辞書
        :return: フィルターされたクエリ
        """
        for field, value in filters.items():
            if value is not None:
                query = query.filter(getattr(query.entity_description.entity, field) == value)
        return query

    @staticmethod
    def add_search(query: Query, search_term: str, search_fields: List[str]) -> Query:
        """
        検索条件を追加
        :param query: クエリ
        :param search_term: 検索語
        :param search_fields: 検索対象のフィールドリスト
        :return: 検索条件が追加されたクエリ
        """
        if not search_term or not search_fields:
            return query

        search_conditions = []
        for field in search_fields:
            search_conditions.append(
                getattr(query.entity_description.entity, field).ilike(f"%{search_term}%")
            )
        return query.filter(or_(*search_conditions))

    @staticmethod
    def add_ordering(query: Query, order_by: str, descending: bool = False) -> Query:
        """
        並び順を追加
        :param query: クエリ
        :param order_by: ソート対象のフィールド
        :param descending: 降順かどうか
        :return: ソートされたクエリ
        """
        if not order_by:
            return query

        order_func = desc if descending else asc
        return query.order_by(order_func(getattr(query.entity_description.entity, order_by)))

    @staticmethod
    def optimize_complex_query(query: Query) -> Query:
        """
        複雑なクエリを最適化
        :param query: 最適化するクエリ
        :return: 最適化されたクエリ
        """
        # サブクエリの最適化
        if hasattr(query, '_entities') and len(query._entities) > 1:
            return query.from_self()

        # 不要なカラムの削除
        if hasattr(query, '_entities'):
            return query.with_entities(*[e for e in query._entities if e is not None])

        return query

    @staticmethod
    def explain_query(query: Query) -> str:
        """
        クエリの実行計画を取得
        :param query: 分析するクエリ
        :return: 実行計画の文字列
        """
        try:
            explanation = query.statement.compile(compile_kwargs={"literal_binds": True})
            logging.info(f"Query Explanation: {explanation}")
            return str(explanation)
        except Exception as e:
            logging.error(f"Failed to explain query: {str(e)}")
            return ""

    def optimize_query(self, query: Query, **kwargs) -> Query:
        """クエリを総合的に最適化"""
        # フィルター
        if filters := kwargs.get('filters'):
            query = self.add_filters(query, filters)

        # 検索
        if (search_term := kwargs.get('search_term')) and (search_fields := kwargs.get('search_fields')):
            query = self.add_search(query, search_term, search_fields)

        # ソート
        if order_by := kwargs.get('order_by'):
            query = self.add_ordering(query, order_by, kwargs.get('descending', False))

        # ページネーション
        if kwargs.get('page'):
            query = self.add_pagination(query, kwargs.get('page'), kwargs.get('per_page', 10))

        # 実行オプション
        query = query.execution_options(
            lazyload_relations=False,
            enable_eagerloads=True
        )

        return query

    def log_query_stats(self, query: Query) -> None:
        """クエリの統計情報をログに記録"""
        self.logger.info(f"SQL: {query.statement}")
        self.logger.info(f"Parameters: {query.parameters}") 