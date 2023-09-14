import os
import sys
import subprocess

try:
    import arxiv
except ImportError: 
    subprocess.check_call([sys.executable, "-m", "pip", "install", "arxiv"])
    import arxiv

from Extensions import Extensions

class Arxiv(Extensions):

    def __init__(self, WORKING_DIRECTORY: str = "./WORKSPACE", **kwargs):
        self.WORKING_DIRECTORY = WORKING_DIRECTORY 
        self.commands = {
            "Search Arxiv": self.search,
            "Download Arxiv PDF": self.download_pdf
        }

    async def search(self, query: str) -> list:
        search = arxiv.Search(
            query=query,
            sort_by=arxiv.SortCriterion.SubmittedDate  
        )
        
        results = []
        for result in search.results():
            results.append(result.title)

        return results

    async def download_pdf(self, article_id: str) -> str:
        search = arxiv.Search(id_list=[article_id])
        result = next(search.results())
        
        filename = f"{result.get_short_id()}.pdf"
        filepath = os.path.join(self.WORKING_DIRECTORY, filename)
        
        try:
            result.download_pdf(filepath)
            return f"Downloaded {filename} to {self.WORKING_DIRECTORY}"
        except Exception as e:
            return f"Error downloading PDF: {e}"
