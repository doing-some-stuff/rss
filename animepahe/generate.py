import requests
import json
import re
import os
from dotenv import load_dotenv as env

env()
idexclude = eval(os.getenv("Showswatching"))

def get_latest():
    link = 'https://animepahe.com/api?m=airing&page=1'

    response = requests.get(link, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}).json()

    allshowsreleased=[
        [
            '{}/{}'.format(x['anime_session'], x['session']),
            x['episode'],
            x['anime_title'],x['snapshot']
        ] for x in response['data']
    ]
    showsreleased=[]
    for entry in allshowsreleased:
        if entry[2] in idexclude:
            showsreleased.append(entry)
    return showsreleased


def generate_rss():
    rss = f"""
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">

<channel>
<title>AnimePahe - RSS Feed</title>
<link>https://github.com/doing-some-stuff/rss/tree/main</link>
<description>A simple RSS feed for animepahe!</description>
"""

    for item in get_latest():
        rss += """
<item>
    <title>{}</title>
    <link>{}</link>
    <imglink>{}</imglink>
    <description>{}</description>
</item>
""".format(f"{item[2]} - Episode {item[1]}", "https://animepahe.com/play/" + item[0], item[3] , f"Episode {item[1]} of {item[2]} is out!")

    rss += '\n</channel>\n</rss>'
    return rss


try:
    filename = f'./animepahe/animepahe-rss.xml'
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w') as f:
        f.write(generate_rss().strip())
except:
    print('Animepahe failed.')
