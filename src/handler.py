""" Example handler file. """

import os
import shutil

import urllib3
import runpod
import dotenv
import whisper_timestamped as whisper
import json
import boto3

dotenv.load_dotenv()
s3 = boto3.client('s3', aws_access_key_id=os.environ.get('AWS_S3_ACCESS_ID'), aws_secret_access_key=os.environ.get('AWS_S3_ACCESS_KEY'))
model = whisper.load_model("tiny")

def handler(job):
    """ Handler function that will be used to process jobs. """
    job_input = job['input']
    song_name = job_input['song_name']

    print("Downloading song from s3")
    s3.download_file('auto-karaoke', f'{song_name}/vocals.mp3', 'vocals.mp3')
    audio = whisper.load_audio("vocals.mp3")
    result = whisper.transcribe(model, audio, language="en")
    print(json.dumps(result, indent = 2, ensure_ascii = False))

    return "DONE!"
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
