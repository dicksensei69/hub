import os
import youtube_dl

from Extensions import Extensions
from agixt_actions import read_file_content

class YouTubeSubtitles(Extensions):

    def __init__(self, WORKING_DIRECTORY="./WORKSPACE"):
        self.WORKING_DIRECTORY = WORKING_DIRECTORY
        self.commands = {
            "Download YouTube Subtitles": self.download_subtitles
        }

    async def download_subtitles(self, video_url: str) -> str:
        try:
            ydl_opts = {
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['en'],
                'skip_download': True,
                'outtmpl': os.path.join(self.WORKING_DIRECTORY, 'subtitles.vtt')
            }
        
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            vtt_path = os.path.join(self.WORKING_DIRECTORY, 'subtitles.vtt')
            txt_path = vtt_path.replace('.vtt', '.txt')
        
            # Convert .vtt to .txt
            with open(vtt_path, 'r') as vtt_file:
                with open(txt_path, 'w') as txt_file:
                    for line in vtt_file:
                        if line.startswith('WEBVTT'):
                            continue
                        txt_file.write(line)
        
            # Read .txt subtitles into memory        
            with open(txt_path, 'r') as f:
                subtitles = f.read()
        
            await read_file_content(subtitles)
        
            return f"Downloaded subtitles from {video_url}"
        except youtube_dl.utils.DownloadError as e:
            return f"Error downloading subtitles: {str(e)}"
        
        except FileNotFoundError as e:
            return f"Error reading subtitles file: {str(e)}"
            
        except Exception as e:
            return f"Unexpected error: {str(e)}"
