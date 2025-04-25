#!/bin/bash

CWD=$(dirname $0)

# Docker cleanup
docker container prune -f
docker image prune -f

# Build
docker build -t power-reporter .

# Deploy
export IMAGE_TAG=$(docker images -q power-reporter)
docker tag "power-reporter" "srvu:5000/power-reporter:$IMAGE_TAG"
docker push "srvu:5000/power-reporter:$IMAGE_TAG"
envsubst < "$CWD/deployment.yaml" | kubectl apply -f -

echo "Deployment completed"
