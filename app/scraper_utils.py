from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time
import random
from typing import Optional, Callable, Any
from functools import wraps

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """失敗時にリトライするデコレータ"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        sleep_time = delay * (2 ** attempt) + random.uniform(0, 1)
                        time.sleep(sleep_time)
            raise last_exception
        return wrapper
    return decorator

class ScraperUtils:
    def __init__(self, driver):
        self.driver = driver

    @retry_on_failure()
    def wait_and_find_element(self, by: By, value: str, timeout: int = 10) -> Any:
        """要素が見つかるまで待機して取得"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"要素が見つかりません: {value}")

    @retry_on_failure()
    def wait_and_find_elements(self, by: By, value: str, timeout: int = 10) -> list:
        """複数の要素が見つかるまで待機して取得"""
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
            return elements
        except TimeoutException:
            raise TimeoutException(f"要素が見つかりません: {value}")

    @retry_on_failure()
    def wait_and_click(self, by: By, value: str, timeout: int = 10):
        """要素がクリック可能になるまで待機してクリック"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
        except TimeoutException:
            raise TimeoutException(f"要素がクリックできません: {value}")

    def safe_get_text(self, element) -> str:
        """要素のテキストを安全に取得"""
        try:
            return element.text.strip()
        except StaleElementReferenceException:
            return ""

    def safe_get_attribute(self, element, attribute: str) -> str:
        """要素の属性を安全に取得"""
        try:
            return element.get_attribute(attribute) or ""
        except StaleElementReferenceException:
            return ""

    def scroll_to_element(self, element):
        """要素までスクロール"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # スクロール後の安定を待つ

    def wait_for_page_load(self, timeout: int = 10):
        """ページの読み込み完了を待機"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            raise TimeoutException("ページの読み込みが完了しませんでした")

    def take_screenshot(self, filename: str):
        """スクリーンショットを保存"""
        try:
            self.driver.save_screenshot(filename)
        except Exception as e:
            print(f"スクリーンショットの保存に失敗しました: {str(e)}") 