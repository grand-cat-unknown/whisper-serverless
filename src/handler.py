""" Example handler file. """

import os
import shutil

import urllib3
import runpod
import dotenv
import stable_whisper
import json
import boto3

dotenv.load_dotenv()
s3 = boto3.client('s3', aws_access_key_id=os.environ.get('AWS_S3_ACCESS_ID'), aws_secret_access_key=os.environ.get('AWS_S3_ACCESS_KEY'))

def handler(job):
    """ Handler function that will be used to process jobs. """
    job_input = job['input']
    song_name = job_input['song_name']

    print("Downloading song from s3")
    s3.download_file('auto-karaoke', f'{song_name}/vocals.mp3', 'vocals.mp3')
    s3.download_file('auto-karaoke', f'{song_name}/lyrics.txt', 'lyrics.txt')

    with open('lyrics.txt', 'r') as f:
        lyrics = f.read()

    result = model.align('vocals.mp3', lyrics, 'English')
    # audio = stable_whisper.load_audio("vocals.mp3")
    # print("transcribing audio")
    # result = stable_whisper.transcribe(model, audio, language="en")
    # print("Transcription complete")

    print("Saving result to file")
    # with open(f"timestamps.json", "w") as f:
    #     json.dump(result, f, indent=2, ensure_ascii=False)
    result.save_as_json('timestamps.json')
    s3.upload_file(f"timestamps.json", 'auto-karaoke', f'{song_name}/timestamps.json')

    return "DONE!"

if not os.environ.get("DEV", False):
    model = stable_whisper.load_model("large-v3")
    runpod.serverless.start({"handler": handler})
else:
    # serve this using fastapi
    import uvicorn
    from fastapi import FastAPI
    import json
    
    model = stable_whisper.load_model("tiny")
    app = FastAPI()

    @app.get("/")
    def test_handler():
        # read json from file
        with open("test_job.json", "r") as f:
            job = json.load(f)
        return handler(job)
    
    # run uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=81)
