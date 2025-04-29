import logging
import time
from typing import Dict, List, Any
from sqlalchemy.orm import Query
from sqlalchemy import event
from sqlalchemy.engine import Engine

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('query_analysis.log'),
        logging.StreamHandler()
    ]
)

class QueryAnalyzer:
    def __init__(self):
        self.query_stats: Dict[str, Dict[str, Any]] = {}
        self.slow_queries: List[Dict[str, Any]] = []

    def analyze_query(self, query: Query, execution_time: float) -> None:
        """
        クエリの分析を行う
        :param query: SQLAlchemyのクエリオブジェクト
        :param execution_time: 実行時間（秒）
        """
        query_str = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
        query_key = self._get_query_key(query_str)

        if query_key not in self.query_stats:
            self.query_stats[query_key] = {
                'count': 0,
                'total_time': 0,
                'min_time': float('inf'),
                'max_time': 0,
                'last_execution': None
            }

        stats = self.query_stats[query_key]
        stats['count'] += 1
        stats['total_time'] += execution_time
        stats['min_time'] = min(stats['min_time'], execution_time)
        stats['max_time'] = max(stats['max_time'], execution_time)
        stats['last_execution'] = time.time()

        if execution_time > 1.0:  # 1秒以上かかるクエリを記録
            self.slow_queries.append({
                'query': query_str,
                'execution_time': execution_time,
                'timestamp': time.time()
            })
            logging.warning(f"Slow query detected: {query_str}")
            logging.warning(f"Execution time: {execution_time:.2f} seconds")

    def _get_query_key(self, query_str: str) -> str:
        """
        クエリのキーを生成
        :param query_str: SQLクエリ文字列
        :return: クエリのキー
        """
        # パラメータ値を無視してクエリの構造のみを比較
        return query_str.split('WHERE')[0] if 'WHERE' in query_str else query_str

    def get_query_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        クエリの統計情報を取得
        :return: クエリの統計情報
        """
        return self.query_stats

    def get_slow_queries(self) -> List[Dict[str, Any]]:
        """
        遅いクエリのリストを取得
        :return: 遅いクエリのリスト
        """
        return self.slow_queries

    def generate_report(self) -> str:
        """
        分析レポートを生成
        :return: レポート文字列
        """
        report = []
        report.append("Query Analysis Report")
        report.append("=" * 50)
        
        for query_key, stats in self.query_stats.items():
            avg_time = stats['total_time'] / stats['count']
            report.append(f"\nQuery: {query_key}")
            report.append(f"  Count: {stats['count']}")
            report.append(f"  Average Time: {avg_time:.2f} seconds")
            report.append(f"  Min Time: {stats['min_time']:.2f} seconds")
            report.append(f"  Max Time: {stats['max_time']:.2f} seconds")
        
        if self.slow_queries:
            report.append("\nSlow Queries:")
            for query in self.slow_queries:
                report.append(f"\nQuery: {query['query']}")
                report.append(f"Execution Time: {query['execution_time']:.2f} seconds")
                report.append(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(query['timestamp']))}")
        
        return "\n".join(report)

# グローバルインスタンス
query_analyzer = QueryAnalyzer()

# SQLAlchemyのイベントリスナー
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    execution_time = time.time() - context._query_start_time
    query_analyzer.analyze_query(statement, execution_time) 