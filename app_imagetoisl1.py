# Takes an image, reads the text (word) in it and displays the corresponding ISL video for the word
# Cannot be done for multiple words (yet)

import os
import time
import cv2
from paddleocr import PaddleOCR
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import shutil

app = FastAPI()

# Path to media files
MEDIA_DIR = "/home/sakshi/Documents/sakshi_SIH/isl"  # Update with your actual path

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Set language to English

def preprocess_text(text):
    """Preprocess the input text by capitalizing the first letter and removing punctuation."""
    text = text.lower().strip()
    words = text.split()
    words = [word.capitalize() for word in words]  # Capitalize the first letter of each word
    return words
    
def media_exists(media_name):
    """Check if the media file exists in the dataset."""
    file_path = os.path.join(MEDIA_DIR, f"{media_name}.mp4")
    return os.path.isfile(file_path)

def display_video(video_path):
    """Play a video using OpenCV."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise HTTPException(status_code=404, detail=f"Error: Could not open video {video_path}")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def detect_text(image_path):
    """Detect and recognize text in an image using PaddleOCR."""
    result = ocr.ocr(image_path, cls=True)
    detected_text = []
    for line in result:
        for word_info in line:
            text = word_info[1][0]
            detected_text.append(text)
    return ' '.join(detected_text)

def process_text(text):
    words = preprocess_text(text)
    media_sequence = []
    for word in words:
        if media_exists(word):
            media_sequence.append(os.path.join(MEDIA_DIR, f"{word}.mp4"))
        else:
            capitalized_letters = [letter.upper() for letter in word]
            for letter in capitalized_letters:
                if media_exists(letter):
                    media_sequence.append(os.path.join(MEDIA_DIR, f"{letter}.mp4"))
    return media_sequence

@app.post("/upload_image/")
async def upload_image(file: UploadFile = File(...)):
    # Save the uploaded file
    upload_dir = "/home/sakshi/Documents/sakshi_SIH"  # Temporary upload path
    image_path = os.path.join(upload_dir, file.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Detect text from image
    detected_text = detect_text(image_path)

    # Get corresponding ISL videos
    media_sequence = process_text(detected_text)

    if not media_sequence:
        return JSONResponse(status_code=404, content={"message": "No videos found for the detected text."})

    # Return the paths of the videos (or handle displaying them)
    return {"detected_text": detected_text, "videos": media_sequence}

