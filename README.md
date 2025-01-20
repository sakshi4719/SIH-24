My contribution for the Smart India Hackathon 2024

**app_imagetoisl1.py**  
Takes an image, reads the text in it using PaddleOCR and displays the corresponding ISL video stored in a media directory (MEDIA_DIR).  
The system can handle only individual words or letters and retrieve the appropriate ISL video files for each.  
Users can upload images via a POST request.  
Server responds with detected text and corresponding ISL video paths.    

**app_texttoisl1.py**  
Streams videos corresponding to specific words in the ISL folder.  
Users send a POST request with a word, and the app finds and serves the matching .mp4 video.  
If the video for the given word is not found, the app returns a 404 error.  
Videos are streamed using FastAPI's StreamingResponse for efficient playback.  

**app_texttoisl2.py**  
Retrieves and serves multiple ISL video files corresponding to the words in a given text input.  
Users provide a sentence or phrase, and the app matches each word to its .mp4 video.  
The app returns a list of URLs for the videos, which clients can fetch and play individually.  
Videos are served through the /media/{media_name} endpoint using FastAPI's FileResponse.  
