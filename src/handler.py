""" Example handler file. """

import os
import shutil

import urllib3
import runpod
import dotenv
import whisper_timestamped as whisper
import json

dotenv.load_dotenv()
# If your handler runs inference on a model, load the model here.
# You will want models to be loaded into memory before starting serverless.

def handler(job):
    """ Handler function that will be used to process jobs. """
    job_input = job['input']
    name = job_input.get('name', 'World')

    print("Downloading example.mp3")
    url = "https://github.com/deezer/spleeter/raw/master/audio_example.mp3"
    destination_path = "example.mp3"
    http = urllib3.PoolManager()

    with http.request('GET', url, preload_content=False) as r, open(destination_path, 'wb') as out_file:
        shutil.copyfileobj(r, out_file)
    print("Downloaded example.mp3")

    audio = whisper.load_audio("example.mp3")
    model = whisper.load_model("tiny", device="cpu")
    result = whisper.transcribe(model, audio, language="en")

    print(json.dumps(result, indent = 2, ensure_ascii = False))

    return f"You are THE BEST <3, {name}!"

if not os.environ.get("DEV", False):
    runpod.serverless.start({"handler": handler})
else:
    # serve this using fastapi
    import uvicorn
    from fastapi import FastAPI
    import json
    
    app = FastAPI()

    @app.get("/")
    def test_handler():
        # read json from file
        with open("test_job.json", "r") as f:
            job = json.load(f)
        return handler(job)
    
    # run uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=81)
