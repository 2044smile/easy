import requests, os
from datetime import datetime
import pandas as pd

from search.crawlers.base import crawler_settings


def get_product_info(product_name):
    CLIENT_ID, CLIENT_SECRET = crawler_settings()
    
    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }

    all_products = []
    start = 1
    display = 100

    while True:
        # 네이버 API는 최대 1000개까지만 결과를 제공
        if start > 1000:
            print("네이버 검색 API는 최대 1000개의 결과만 제공합니다.")
            break

        params = {
            "query": product_name,  # 한일배관
            "display": display,
            "start": start,
            "filter": "naverpay",
            "exclude": "used,rental,cbshop",
            "sort": "asc"
        }
    
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            raise ValueError(f"ERROR: {response.status_code}")
        
        data = response.json()
        items = data.get('items', [])
        
        if not items:  # 결과가 없으면 종료
            break

        for item in items:
            product_info = {
                '검색일자': datetime.now().strftime('%Y-%m-%d'),
                '제품명': item.get('title'),
                '현재가격': item.get('lprice'),
                '정가': item.get('hprice'),
                '배송비': "배송비 정보는 API에서 제공하지 않습니다",
                '상품링크': item.get('link'),
                '쇼핑몰명': item.get('mallName')
            }
            all_products.append(product_info)

        print(f"{start}~{start+len(items)-1}번째 상품 정보 수집 완료")
        start += display

    # DataFrame 생성 및 CSV 저장
    df = pd.DataFrame(all_products)
    filename = f'search/crawlers/data/product_data_{datetime.now().strftime("%Y%m%d")}.csv'
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    return all_products


get_product_info("한일배관")