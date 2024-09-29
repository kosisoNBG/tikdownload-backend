import re
import requests
from bs4 import BeautifulSoup
import json
import html


def get_data(link):
    url = 'https://snaptik.gg/check/'
    payload = {'url': link}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        r = requests.post(url, data=payload, headers=headers)

        try:
            response_json = json.loads(r.text)
            raw_html = response_json.get("html", "")
            clean_html = html.unescape(raw_html)
        except json.JSONDecodeError:
            clean_html = r.text

        soup = BeautifulSoup(clean_html, 'lxml')

        dl_container = soup.find('div', class_='down-right')
        dl_links = dl_container.find_all('a')
        download_links = [i['href'] for i in dl_links[:2]]

        username = soup.find('div', class_='user-username').text
        full_name = soup.find('div', class_='user-fullname').text
        image = soup.find('div', class_='user-avatar').img['src']

        output = {
            "username": username,
            "full_name": full_name,
            "image": image,
            "download_server1": download_links[0],
            "download_server2": download_links[1] or ""
        }
        return output
    except Exception as e:
        return None