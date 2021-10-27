import requests
import os
import argparse

from urllib.parse import urlparse
from dotenv import load_dotenv
from pathlib import Path



def shorten_link(bitlink_token, link):
    payload = {"long_url": link}
    headers = {"Authorization": "Bearer {}".format(bitlink_token)}
    url = "https://api-ssl.bitly.com/v4/shorten"
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    shorten_link = response.json()["id"]
    return shorten_link


def count_clicks(bitlink_token, link):
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary".format(
        link)
    headers = {"Authorization": "Bearer {}".format(bitlink_token)}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()["total_clicks"]
    return clicks_count


def is_bitlink(bitlink_token, link):
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}".format(link)
    headers = {"Authorization": "Bearer {}".format(bitlink_token)}
    response = requests.get(url, headers=headers)
    return response.ok


if __name__ == "__main__":
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    bitlink_token = os.getenv("BITLINK_TOKEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("link", help="Ссылка на сайт")
    args = parser.parse_args()
    link = args.link
    bitlink = urlparse(link)
    bitlink = "{}{}".format(bitlink.netloc,bitlink.path)
    try:
        if is_bitlink(bitlink_token, bitlink):
            print("Клики", count_clicks(bitlink_token, bitlink))
        else:
            print(shorten_link(bitlink_token, link))
    except requests.exceptions.HTTPError:
        print("Ссылка введена неверно!")
