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

    lyrics = """
        I pour it out for you, my baby, I'm a fool
        Our love is new, I speak, I speak like you
        No matter who you are, I imitate you
        Cut my body open, bleed me dry
        I’m a slaughtered pig and I'm happy to die

        So sit down, let's eat
        Fill your plate all up with meat
        Crossing hands and touching feet

        When you said I’m good in a bad, bad place
        Eyes roll back from yours as I hid my pale face
        Like marbles rolling around the brain
        Like marbles again and again and again

        I feel, I feel a new thing coming on
        My love, my blood is blue

        Black coffee
        Sour taste on my tongue
        I write funny and I can't relate
        It's no fun

        I feel, I feel a new thing coming on
        My love, my blood is blue
        """
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
