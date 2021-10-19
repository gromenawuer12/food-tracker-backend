#!/bin/bash

docker run --rm -it --network=python -v ~/.aws:/root/.aws -v ~/workspace/food-tracker/backend:/root/ amazon/aws-cli dynamodb create-table --cli-input-json file:///root/food-tracker.json --endpoint-url http://dynamodb:8000
docker run --rm -it --network=python -v ~/.aws:/root/.aws -v ~/workspace/food-tracker/backend:/root/ amazon/aws-cli dynamodb batch-write-item --request-items file:///root/testdata.json --endpoint-url http://dynamodb:8000