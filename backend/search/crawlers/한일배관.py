import requests
import pandas as pd
from datetime import datetime

from search.crawlers.base import crawler_settings


def get_product_info(product_name):
    CLIENT_ID, CLIENT_SECRET = crawler_settings()
    
    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    params = {
        "query": f"hanilpipe {product_name}",  # 스토어명과 상품 ID로 검색
        "display": 10
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise ValueError(f"ERROR: {response.status_code}")
    
    data = response.json()
    items = data.get('items', [])
    print(items)
    
    if not items:
        raise ValueError("상품을 찾을 수 없습니다.")
    
    # 모든 검색 결과를 리스트로 변환
    products_list = []

    for item in items:
        product_info = {
            '검색일자': datetime.now().strftime('%Y-%m-%d'),
            '제품명': item.get('title'),
            '현재가격': item.get('lprice'),
            '정가': item.get('hprice'),
            # '할인율': f"{int((1 - int(item.get('lprice')) / int(item.get('hprice'))) * 100)}%" if item.get('hprice') != '0' else "할인 없음",
            '배송비': "배송비 정보는 API에서 제공하지 않습니다",
            '상품링크': item.get('link'),
            '쇼핑몰명': item.get('mallName')
        }
        products_list.append(product_info)
    
    # DataFrame 생성 및 CSV 저장
    df = pd.DataFrame(products_list)
    filename = f'search/crawlers/data/product_data_{datetime.now().strftime("%Y%m%d")}.csv'
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    return products_list

def 한일배관():
    product_name = "PB 엘보 15 A"
    
    try:
        products = get_product_info(product_name)
        print(f"\n총 {len(products)}개의 제품 정보를 저장했습니다.")
    except ValueError as e:
        print(f"에러 발생: {str(e)}")
    except Exception as e:
        print(f"예상치 못한 에러 발생: {str(e)}")

if __name__ == "__main__":
    한일배관()