# Finds the word in the ISL folder and plays the video corresponding to the word found
# Cannot play multiple word videos one after another in FASTAPI its tricky

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os

app = FastAPI()

# Path to media directory (replace with your actual path)
MEDIA_DIR = '/home/sakshi/Documents/sakshi_SIH/isl'

class TextInput(BaseModel):
    text: str  # Expecting a field called 'text' in the JSON request

def get_media_file(word: str) -> str:
    """Return the media file path if the word matches a video name."""
    # Construct the file path using the exact word provided by the user
    media_path = os.path.join(MEDIA_DIR, f"{word}.mp4")
    
    # DEBUG: Print the file path to make sure it's being constructed correctly
    print(f"Looking for file at: {media_path}")

    if os.path.isfile(media_path):
        print(f"File found: {media_path}")
        return media_path
    else:
        print(f"File not found: {media_path}")
        return None

@app.post("/play_video/")
async def play_video(input: TextInput):
    # Use the exact text as provided in the JSON body
    word = input.text

    # Get the matching media file path
    media_file = get_media_file(word)

    # If no media file is found, return a 404 error
    if not media_file:
        raise HTTPException(status_code=404, detail=f"No video found for the word '{word}'")

    # Stream the video file using StreamingResponse
    return StreamingResponse(open(media_file, "rb"), media_type="video/mp4")


