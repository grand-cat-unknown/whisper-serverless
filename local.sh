# build docker 
docker build -t runpod-serverless-docker .
#  remove any docker container with the same name IF Exists
/usr/local/bin/docker rm -f runpod-serverless-docker-container || true
# run docker container
/usr/local/bin/docker  run -d --name runpod-serverless-docker-container -p 80:80 -e LOCAL=True runpod-serverless-docker