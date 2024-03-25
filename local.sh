# build docker 
docker build -t whisper-serverless-docker .
#  remove any docker container with the same name IF Exists
/usr/local/bin/docker rm -f whisper-serverless-docker-container || true
# run docker container
/usr/local/bin/docker  run -d --name whisper-serverless-docker -p 81:81 -e DEV=True whisper-serverless-docker