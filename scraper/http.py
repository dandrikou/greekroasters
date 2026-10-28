"""Polite HTTP client: one shared session, robots.txt checks, retries and a delay between requests."""
import time
import urllib.robotparser
from urllib.parse import urlsplit

import requests

USER_AGENT = "greekroasters-price-tracker/1.0 (+https://github.com/dandrikou/greekroasters)"
DELAY_SECONDS = 1.0
TIMEOUT_SECONDS = 30


class RobotsDisallowed(Exception):
    pass


class Client:
    def __init__(self, delay=DELAY_SECONDS):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "en,el;q=0.8"})
        self.delay = delay
        self._robots = {}
        self._last = 0.0

    def _allowed(self, url):
        parts = urlsplit(url)
        root = f"{parts.scheme}://{parts.netloc}"
        if root not in self._robots:
            parser = urllib.robotparser.RobotFileParser()
            try:
                resp = self.session.get(root + "/robots.txt", timeout=TIMEOUT_SECONDS)
                parser.parse(resp.text.splitlines() if resp.status_code == 200 else [])
            except requests.RequestException:
                parser.parse([])
            self._robots[root] = parser
        return self._robots[root].can_fetch(USER_AGENT, url)

    def get(self, url, params=None):
        if not self._allowed(url):
            raise RobotsDisallowed(url)
        for attempt in range(3):
            wait = self.delay - (time.monotonic() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.monotonic()
            try:
                resp = self.session.get(url, params=params, timeout=TIMEOUT_SECONDS)
            except requests.RequestException:
                if attempt == 2:
                    raise
                time.sleep(2 ** (attempt + 1))
                continue
            if resp.status_code in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(2 ** (attempt + 2))
                continue
            resp.raise_for_status()
            return resp
        raise RuntimeError(f"unreachable: {url}")

    def get_json(self, url, params=None):
        return self.get(url, params=params).json()

    def get_text(self, url, params=None):
        return self.get(url, params=params).text
