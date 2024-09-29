import re
import requests
from bs4 import BeautifulSoup
import json
import html

# TikTok video downloader
def get_data(link):
    url = 'https://snaptik.gg/check/'
    payload = {'url': link}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        r = requests.post(url, data=payload, headers=headers)
        r.raise_for_status()  # Raises an error for HTTP error responses

        try:
            response_json = json.loads(r.text)
            raw_html = response_json.get("html", "")
            clean_html = html.unescape(raw_html)
        except json.JSONDecodeError:
            clean_html = r.text

        soup = BeautifulSoup(clean_html, 'lxml')

        # Extracting download links
        dl_container = soup.find('div', class_='down-right')
        if not dl_container:
            return {"error": "Download container not found."}

        dl_links = dl_container.find_all('a')
        if len(dl_links) < 2:
            return {"error": "Insufficient download links found."}

        download_links = [i['href'] for i in dl_links[:2]]

        # Extracting user data
        username = soup.find('div', class_='user-username')
        full_name = soup.find('div', class_='user-fullname')
        image = soup.find('div', class_='user-avatar')

        if not username or not full_name or not image:
            return {"error": "User information missing from the response."}

        username = username.text.strip()
        full_name = full_name.text.strip()
        image_url = image.img['src']

        # Format output as a dictionary
        output = {
            "username": username,
            "full_name": full_name,
            "image": image_url,
            "download_server1": download_links[0],
            "download_server2": download_links[1]
        }
        return output

    except requests.RequestException as e:
        return {"error": f"Request error: {str(e)}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
