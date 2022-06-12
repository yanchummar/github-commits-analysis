import requests
from config import GITHUB_TOKEN


HEADERS = {'Authorization': "token %s" % (GITHUB_TOKEN)}

BASE_URL = 'https://api.github.com'

def call_github_api(path, params=None, is_url=False):
  if is_url:
    url = path
  else:
    url = BASE_URL + path
  response = requests.request("GET", url, headers=HEADERS, params=params)
  return response.json()