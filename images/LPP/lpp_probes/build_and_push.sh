#!/usr/bin/sh

REGISTRY=${1:-"129.104.6.165:32219"}
IMAGE="lpp/lpp_probes"
echo "Will build $IMAGE and push on registry: $REGISTRY"
FULL_NAME="${REGISTRY}/${IMAGE}"
docker build -t ${FULL_NAME} .
docker push ${FULL_NAME}