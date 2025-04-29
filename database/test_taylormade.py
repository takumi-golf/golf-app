import requests
from bs4 import BeautifulSoup
import logging
import time

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_taylormade_scraping():
    """TaylorMadeのウェブサイトの構造を確認します。"""
    try:
        # ヘッダーの設定
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        # メインページにアクセス
        main_url = "https://www.taylormadegolf.com"
        logger.info(f"メインページにアクセス: {main_url}")
        response = requests.get(main_url, headers=headers)
        response.raise_for_status()
        main_soup = BeautifulSoup(response.text, 'html.parser')
        
        # ナビゲーションメニューからゴルフクラブのリンクを探す
        nav_links = main_soup.select('nav a')
        clubs_url = None
        for link in nav_links:
            if 'golf-clubs' in link.get('href', '').lower():
                clubs_url = link['href']
                if not clubs_url.startswith('http'):
                    clubs_url = f"https://www.taylormadegolf.com{clubs_url}"
                break
        
        if not clubs_url:
            logger.error("ゴルフクラブのリンクが見つかりませんでした")
            return
        
        logger.info(f"ゴルフクラブページにアクセス: {clubs_url}")
        response = requests.get(clubs_url, headers=headers)
        response.raise_for_status()
        clubs_soup = BeautifulSoup(response.text, 'html.parser')
        
        # ページの構造を確認
        logger.info("ページの構造を確認中...")
        
        # カテゴリーのリンクを探す
        category_links = clubs_soup.select('.category-link')
        logger.info(f"カテゴリーリンクの数: {len(category_links)}")
        for link in category_links:
            logger.info(f"カテゴリー: {link.text.strip()} - URL: {link.get('href')}")
        
        # 製品カードを探す
        product_cards = clubs_soup.select('.product-card')
        logger.info(f"製品カードの数: {len(product_cards)}")
        if product_cards:
            # 最初の製品カードの構造を確認
            first_card = product_cards[0]
            logger.info("最初の製品カードの構造:")
            logger.info(f"HTML: {first_card.prettify()}")
        
        # 製品詳細ページの構造を確認
        if product_cards:
            product_url = product_cards[0].select_one('a')['href']
            if not product_url.startswith('http'):
                product_url = f"https://www.taylormadegolf.com{product_url}"
            
            logger.info(f"製品詳細ページにアクセス: {product_url}")
            response = requests.get(product_url, headers=headers)
            response.raise_for_status()
            detail_soup = BeautifulSoup(response.text, 'html.parser')
            
            # 製品詳細ページの構造を確認
            logger.info("製品詳細ページの構造:")
            logger.info(f"HTML: {detail_soup.prettify()}")
        
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    test_taylormade_scraping() 