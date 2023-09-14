import json
import sys
import subprocess

try:
    import arxiv
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "arxiv"])
    import arxiv

from Extensions import Extensions


class Arxiv(Extensions):

    def __init__(self, **kwargs):
        self.commands = {
            "Search Arxiv": self.search
        }

    async def search(self, query: str) -> str:
        results = []
        search = arxiv.Search(query=query, sort_by=arxiv.SortCriterion.Relevance, max_results=10)

        for i, result in enumerate(search.results()):
            article_id = result.get_short_id()
            summary = result.summary
            results.append({"article_id": article_id, "summary": summary})

        return json.dumps(results)
