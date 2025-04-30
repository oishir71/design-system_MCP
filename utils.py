import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SOFTREEF_BASE_URL=os.getenv("SOFTREEF_BASE_URL")

def get_csrf_token():
    url = f"{SOFTREEF_BASE_URL}/admin/login/?next=/admin/"

    with httpx.Client(follow_redirects=True) as client:
        response = client.get(url, timeout=30.0)
        response.raise_for_status()
        csrf_token = response.cookies.get('csrftoken')
        return csrf_token

if __name__ == "__main__":
    csrf_token = get_csrf_token()