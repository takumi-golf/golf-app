import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import random

def scrape_golf_clubs():
    # 主要なゴルフブランドのウェブサイト
    brands = {
        "Titleist": "https://www.titleist.jp/",
        "Callaway": "https://www.callawaygolf.jp/",
        "TaylorMade": "https://www.taylormadegolf.jp/",
        "PING": "https://www.ping.com/",
        "Mizuno": "https://www.mizuno.jp/golf/",
        "Srixon": "https://www.srixon.jp/",
        "Honma": "https://www.honmagolf.co.jp/",
        "XXIO": "https://www.xxio.jp/"
    }

    clubs_data = []

    # 各ブランドのクラブ情報を収集
    for brand, url in brands.items():
        try:
            print(f"{brand}のクラブ情報を収集中...")
            
            # 実際のウェブサイトから情報を取得する代わりに、ダミーデータを生成
            if brand == "Titleist":
                clubs_data.extend([
                    {
                        "brand": "Titleist",
                        "model": "TSi3",
                        "loft": 9.5,
                        "shaft": "Diamana",
                        "shaft_flex": "S",
                        "price": 50000,
                        "features": "低スピン、高弾道",
                        "type": "driver"
                    },
                    {
                        "brand": "Titleist",
                        "model": "TSi2",
                        "loft": 15,
                        "shaft": "Diamana",
                        "shaft_flex": "S",
                        "price": 40000,
                        "features": "高弾道、高容錯性",
                        "type": "wood"
                    }
                ])
            elif brand == "Callaway":
                clubs_data.extend([
                    {
                        "brand": "Callaway",
                        "model": "Paradym",
                        "loft": 10.5,
                        "shaft": "Project X",
                        "shaft_flex": "S",
                        "price": 48000,
                        "features": "高弾道、高容錯性",
                        "type": "driver"
                    },
                    {
                        "brand": "Callaway",
                        "model": "Apex",
                        "loft": 27,
                        "shaft": "Project X",
                        "shaft_flex": "S",
                        "price": 28000,
                        "features": "高弾道、高容錯性",
                        "type": "iron"
                    }
                ])
            elif brand == "TaylorMade":
                clubs_data.extend([
                    {
                        "brand": "TaylorMade",
                        "model": "Stealth 2",
                        "loft": 9.0,
                        "shaft": "Fujikura",
                        "shaft_flex": "S",
                        "price": 52000,
                        "features": "低スピン、高弾道",
                        "type": "driver"
                    },
                    {
                        "brand": "TaylorMade",
                        "model": "P790",
                        "loft": 27,
                        "shaft": "Dynamic Gold",
                        "shaft_flex": "S",
                        "price": 29000,
                        "features": "高弾道、高容錯性",
                        "type": "iron"
                    }
                ])
            elif brand == "PING":
                clubs_data.extend([
                    {
                        "brand": "PING",
                        "model": "G430",
                        "loft": 10.5,
                        "shaft": "Alta CB",
                        "shaft_flex": "S",
                        "price": 49000,
                        "features": "高弾道、高容錯性",
                        "type": "driver"
                    },
                    {
                        "brand": "PING",
                        "model": "i230",
                        "loft": 27,
                        "shaft": "Dynamic Gold",
                        "shaft_flex": "S",
                        "price": 27000,
                        "features": "高弾道、高容錯性",
                        "type": "iron"
                    }
                ])
            elif brand == "Mizuno":
                clubs_data.extend([
                    {
                        "brand": "Mizuno",
                        "model": "ST-X",
                        "loft": 10.5,
                        "shaft": "KBS",
                        "shaft_flex": "S",
                        "price": 47000,
                        "features": "高弾道、高容錯性",
                        "type": "driver"
                    },
                    {
                        "brand": "Mizuno",
                        "model": "JPX923",
                        "loft": 27,
                        "shaft": "Dynamic Gold",
                        "shaft_flex": "S",
                        "price": 26000,
                        "features": "高弾道、高容錯性",
                        "type": "iron"
                    }
                ])
            elif brand == "Srixon":
                clubs_data.extend([
                    {
                        "brand": "Srixon",
                        "model": "ZX7",
                        "loft": 9.5,
                        "shaft": "Miyazaki",
                        "shaft_flex": "S",
                        "price": 46000,
                        "features": "高弾道、高容錯性",
                        "type": "driver"
                    },
                    {
                        "brand": "Srixon",
                        "model": "ZX5",
                        "loft": 27,
                        "shaft": "Dynamic Gold",
                        "shaft_flex": "S",
                        "price": 25000,
                        "features": "高弾道、高容錯性",
                        "type": "iron"
                    }
                ])
            elif brand == "Honma":
                clubs_data.extend([
                    {
                        "brand": "Honma",
                        "model": "TR20",
                        "loft": 10.5,
                        "shaft": "Vizard",
                        "shaft_flex": "S",
                        "price": 55000,
                        "features": "高弾道、高容錯性",
                        "type": "driver"
                    },
                    {
                        "brand": "Honma",
                        "model": "TR20X",
                        "loft": 27,
                        "shaft": "Vizard",
                        "shaft_flex": "S",
                        "price": 30000,
                        "features": "高弾道、高容錯性",
                        "type": "iron"
                    }
                ])
            elif brand == "XXIO":
                clubs_data.extend([
                    {
                        "brand": "XXIO",
                        "model": "X",
                        "loft": 10.5,
                        "shaft": "Mitsubishi Chemical",
                        "shaft_flex": "S",
                        "price": 60000,
                        "features": "高弾道、高容錯性",
                        "type": "driver"
                    },
                    {
                        "brand": "XXIO",
                        "model": "X",
                        "loft": 27,
                        "shaft": "Mitsubishi Chemical",
                        "shaft_flex": "S",
                        "price": 32000,
                        "features": "高弾道、高容錯性",
                        "type": "iron"
                    }
                ])

            # ウェブサイトへの負荷を考慮して遅延を入れる
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"{brand}の情報収集中にエラーが発生しました: {str(e)}")
            continue

    # 収集したデータをJSONファイルに保存
    with open("data/clubs.json", "w", encoding="utf-8") as f:
        json.dump(clubs_data, f, ensure_ascii=False, indent=2)

    print("クラブ情報の収集が完了しました。")
    return clubs_data

if __name__ == "__main__":
    scrape_golf_clubs() 