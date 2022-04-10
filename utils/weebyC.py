import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
WEEBY_API_KEY = os.environ.get("WEEBY_API_KEY")


def return_gif(arg):
    request = requests.get(f"https://weebyapi.xyz/gif/{arg}?token={str(WEEBY_API_KEY)}")
    rjson = json.loads(request.content)
    return rjson['url']
