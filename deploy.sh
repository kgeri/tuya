#!/bin/bash

CWD=$(dirname $0)

# Docker cleanup
docker container prune -f
docker image prune -f

# Build
docker build -t power-reporter .

# Deploy
export IMAGE_TAG=$(docker images -q power-reporter)
docker tag "power-reporter" "docker.ogreg.org/power-reporter:$IMAGE_TAG"
docker push "docker.ogreg.org/power-reporter:$IMAGE_TAG"
envsubst < "$CWD/deployment.yaml" | kubectl apply -f -

echo "Deployment completed"
