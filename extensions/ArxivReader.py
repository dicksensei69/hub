import os
import json

try:
    import arxiv
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "arxiv"])
    import arxiv

from agixt_actions import read_file_content
from Extensions import Extensions


class ArxivReader(Extensions):

    def __init__(self, WORKING_DIRECTORY="./WORKSPACE"):
        self.WORKING_DIRECTORY = WORKING_DIRECTORY
        self.commands = {
            "Search Arxiv": self.search_arxiv_articles, 
            "Download Arxiv Articles": self.download_arxiv_articles
        }

    async def search_arxiv_articles(self, query: str, max_articles: int = 5) -> List[str]:

        search = arxiv.Search(
            query=query,
            max_results=max_articles,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        summaries = []
        for result in search.results():
            summary = f"{result.title} - {result.id}"
            summaries.append(summary)

        return summaries

    async def download_arxiv_articles(self, article_ids: str) -> str:
        ids = [id.strip() for id in article_ids.split(",")]

        pdf_paths = []
        for id in ids:
            filename = f"{id}.pdf"
            pdf_path = os.path.join(self.WORKING_DIRECTORY, filename)
            
            # Download PDF
            result = arxiv.query(id_list=[id])[0]
            result.download_pdf(self.WORKING_DIRECTORY, filename)
            
            pdf_paths.append(pdf_path)

        # Read PDF contents
        for path in pdf_paths:
            await read_file_content(path)
            
        return f"Downloaded {len(pdf_paths)} PDFs"
