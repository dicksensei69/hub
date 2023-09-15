import os

try:
    import arxiv
except ImportError: 
    # Install arxiv if needed
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "arxiv"])
    import arxiv

from agixt_actions import read_file_content
from Extensions import Extensions

class Arxiv(Extensions):

    def __init__(self, WORKING_DIRECTORY='./WORKSPACE'):
        self.WORKING_DIRECTORY = WORKING_DIRECTORY
    
    async def search_and_download(self, query: str, max_articles: int = 5):

        search = arxiv.Search(
            query=query,
            max_results=max_articles,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        pdf_paths = []
        for result in search.results():
            filename = f"{result.get_short_id()}.pdf"
            pdf_path = os.path.join(self.WORKING_DIRECTORY, filename)
            
            # Download PDF
            result.download_pdf(self.WORKING_DIRECTORY, filename)  
            
            pdf_paths.append(pdf_path)

        # Read PDF contents
        for path in pdf_paths:
            await read_file_content(path)
            
        return f"Searched Arxiv for {query} and downloaded {len(pdf_paths)} PDFs"
