import json
import os
from dotenv import load_dotenv
import httpx
import asyncio

load_dotenv()

SOFTREEF_TOKEN=os.getenv("SOFTREEF_TOKEN")
SOFTREEF_BASE_URL=os.getenv("SOFTREEF_BASE_URL")
SOFTREEF_DATASET_ID=os.getenv("SOFTREEF_DATASET_ID")

def get_csrf_token():
    url = f"{SOFTREEF_BASE_URL}/admin/login/?next=/admin/"

    with httpx.Client(follow_redirects=True) as client:
        response = client.get(url, timeout=30.0)
        response.raise_for_status()
        csrf_token = response.cookies.get('csrftoken')
        return csrf_token

csrf_token = get_csrf_token()

def main():
    url = f"{SOFTREEF_BASE_URL}/api/datarepository/datasets/{SOFTREEF_DATASET_ID}/records/aggregation/"
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
        "Authorization": f"Token {SOFTREEF_TOKEN}",
    }
    data={
        "aggregation": {
            "column": "0",
            "aggs": "max",
        }
    }

    with httpx.Client() as client:
        response = client.post(url, json=data, headers=headers, timeout=30.0)
        response.raise_for_status()
        response = response.json()
        print(response)
        print(response["results"])
        print(response["results"]['value'])
        print(json.dumps(response, indent=2))
        print(type(json.dumps(response, indent=2)))

def get_design_system(url: str) -> str:
    headers = {
        "Content-Type": "text/html",
    }
    with httpx.Client(follow_redirects=True) as client:
        response = client.get(url, headers=headers, timeout=20.0)
        response.raise_for_status()
        print(response.text)

if __name__ == "__main__":
    get_design_system(
        url="http://sb-aiso-pages.s3-website-ap-northeast-1.amazonaws.com/softreef/main/storybook/features/all-in-one-storybook/storybook-static/?path=/docs/@softreef/design-system_softreef-design-system-%E6%A6%82%E8%A6%81%E3%83%BB%E5%88%A9%E7%94%A8%E6%96%B9%E6%B3%95--docs"
    )
