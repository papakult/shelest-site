#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Мгновенная переиндексация: уведомляет Яндекс (и Bing) о новых или обновлённых
страницах по протоколу IndexNow. Ключ уже лежит в корне сайта.

Использование:
    python3 indexnow_ping.py                          # пингует все URL из sitemap.xml
    python3 indexnow_ping.py /articles/novaya.html    # пингует конкретные страницы
"""
import json
import re
import sys
import urllib.request

SITE = "https://shelestfit.com"
KEY = "2b7719f7ccf852b8b6e29eacac90747b"
ENDPOINTS = [
    "https://yandex.com/indexnow",
    "https://api.indexnow.org/indexnow",
]


def urls_from_sitemap() -> list:
    xml = open("sitemap.xml", encoding="utf-8").read()
    return re.findall(r"<loc>(.*?)</loc>", xml)


def ping(urls: list) -> None:
    body = json.dumps(
        {
            "host": "shelestfit.com",
            "key": KEY,
            "keyLocation": f"{SITE}/{KEY}.txt",
            "urlList": urls,
        }
    ).encode("utf-8")
    for endpoint in ENDPOINTS:
        req = urllib.request.Request(
            endpoint, data=body, headers={"Content-Type": "application/json"}, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                print(f"{endpoint}: HTTP {resp.status}")
        except Exception as exc:
            print(f"{endpoint}: {exc}")


if __name__ == "__main__":
    args = sys.argv[1:]
    urls = [SITE + a if a.startswith("/") else a for a in args] or urls_from_sitemap()
    print(f"пингую {len(urls)} URL")
    ping(urls)
