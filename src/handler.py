""" Example handler file. """

import os
import runpod
import logging
# If your handler runs inference on a model, load the model here.
# You will want models to be loaded into memory before starting serverless.


def handler(job):
    """ Handler function that will be used to process jobs. """
    print(f"Received job: {job}")
    job_input = job['input']
    name = job_input.get('name', 'World')
    # LOG
    logging.info(f"Received job: {job}")
    return f"You are **whispering**, {name}!"

if not os.environ["LOCAL"]:
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
    uvicorn.run(app, host="0.0.0.0", port=80)
