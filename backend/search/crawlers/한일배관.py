import requests

from search.crawlers.base import crawler_settings


def 한일배관():
    CLIENT_ID, CLIENT_SECRET = crawler_settings()

    url = f"https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    params = {
        "query": "한일배관",
        "display": 100
    }

    responses = requests.get(url, headers=headers, params=params)

    if not responses.status_code == 200:
        raise ValueError(f"ERROR: {responses.status_code()}")

    data = responses.json()
    items = data.get('items')

    for item in items:
        print(item['title'])


한일배관()