import subprocess
import sys
import time
import logging

try:
    import wikipedia
except ImportError: 
    subprocess.check_call([sys.executable, "-m", "pip", "install", "wikipedia"])
    import wikipedia

from Extensions import Extensions

class Wikipedia(Extensions):

    def __init__(self, **kwargs):
        self.commands = {
            "Wikipedia Search": self.search,
            "Wikipedia Page Summary": self.page_summary,
            "Wikipedia Page Content": self.get_page_content,
            "Wikipedia Page Links": self.get_page_links
        }
        self.last_request_time = time.time()
        self.rate_limit_delay = 1  # in seconds

    async def search(self, query: str) -> list:
        self._rate_limit()
        results = wikipedia.search(query)
        return [f"Title: {r}" for r in results]

    async def page_summary(self, title: str) -> str:
        self._rate_limit()
        try:
            page = wikipedia.page(title)
            return page.summary
        except wikipedia.exceptions.PageError:
            return "Page not found"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Disambiguation page found for {title}. Options: {e.options}"

    async def get_page_content(self, title: str) -> str:
        self._rate_limit()
        try:
            page = wikipedia.page(title)
            return page.content 
        except wikipedia.exceptions.PageError:
            return "Page not found"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Disambiguation page found for {title}. Options: {e.options}"

    async def get_page_links(self, title: str) -> list:
        self._rate_limit()
        try:
            page = wikipedia.page(title)
            return page.links
        except wikipedia.exceptions.PageError:
            return "Page not found"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Disambiguation page found for {title}. Options: {e.options}"

    def _rate_limit(self):
        now = time.time()
        elapsed_time = now - self.last_request_time
        if elapsed_time < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed_time)
        self.last_request_time = time.time()