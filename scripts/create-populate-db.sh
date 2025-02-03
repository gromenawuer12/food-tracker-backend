#!/bin/bash

DYNAMO_URL=http://dynamodb:8000

docker run --rm -it --network=python -e AWS_ACCESS_KEY_ID=X -e AWS_SECRET_ACCESS_KEY=X -v ${PWD}/data:/root/ amazon/aws-cli dynamodb delete-table --table-name food-tracker --region us-west-1 --endpoint-url $DYNAMO_URL
docker run --rm -it --network=python -e AWS_ACCESS_KEY_ID=X -e AWS_SECRET_ACCESS_KEY=X -v ${PWD}/data:/root/ amazon/aws-cli dynamodb create-table --cli-input-json file:///root/food-tracker.json --region us-west-1 --endpoint-url $DYNAMO_URL

for i in $(seq 1 44); do
  echo "Processing testdata-${i}.json"
  docker run --rm -it --network=python -e AWS_ACCESS_KEY_ID=X -e AWS_SECRET_ACCESS_KEY=X -v ${PWD}/data:/root/ amazon/aws-cli dynamodb batch-write-item --request-items file:///root/testdata-${i}.json --region us-west-1 --endpoint-url $DYNAMO_URL
done
