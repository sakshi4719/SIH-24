# Takes the text and finds the corresponding ISL videos for it
# Since it is difficult to play multiple videos one after another, it gets the paths of all the videos
# For example, "I Can Ask You" returns the 4 corresponding mp4 videos of ISL

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

app = FastAPI()

# Path to media directory (replace with your actual path)
MEDIA_DIR = '/home/sakshi/Documents/sakshi_SIH/isl'

class TextInput(BaseModel):
    text: str  # Expecting a field called 'text' in the JSON request

def get_media_file(word: str) -> str:
    """Return the media file path if the word matches a video name."""
    media_path = os.path.join(MEDIA_DIR, f"{word}.mp4")
    print(f"Looking for file at: {media_path}")
    if os.path.isfile(media_path):
        return media_path
    return None

@app.post("/play_videos/")
async def play_videos(input: TextInput):
    # Split the phrase into individual words
    words = input.text.split()

    # Create a list to hold the valid video paths
    media_files = []

    for word in words:
        media_file = get_media_file(word)
        if media_file:
            media_files.append(media_file)
        else:
            raise HTTPException(status_code=404, detail=f"No video found for the word '{word}'")

    if not media_files:
        raise HTTPException(status_code=404, detail="No videos found")

    # Return the list of media files as URLs for the client to fetch one by one
    media_urls = [f"http://127.0.0.1:8000/media/{os.path.basename(file)}" for file in media_files]
    return {"media_urls": media_urls}

@app.get("/media/{media_name}")
async def serve_media(media_name: str):
    media_path = os.path.join(MEDIA_DIR, media_name)
    
    if not os.path.exists(media_path):
        raise HTTPException(status_code=404, detail="Media not found")
    
    return FileResponse(media_path, media_type="video/mp4")
