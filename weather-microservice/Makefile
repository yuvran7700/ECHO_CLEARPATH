.PHONY: build-collection build-weather deploy-collection deploy-weather deploy-all clean

REGION = us-east-1
ACCOUNT_ID = 669155637430

clean:
    rm -rf package collection_lambda.zip weather_lambda.zip

build-collection:
    rm -rf package collection_lambda.zip
    pip install -r requirements.txt -t ./package
    cd package && zip -r ../collection_lambda.zip . && cd ..
    zip -r collection_lambda.zip src/

build-weather:
    rm -rf package weather_lambda.zip
    pip install -r requirements.txt -t ./package
    cd package && zip -r ../weather_lambda.zip . && cd ..
    zip -r weather_lambda.zip src/

deploy-collection: build-collection
    aws lambda update-function-code \
        --function-name collection-lambda \
        --zip-file fileb://collection_lambda.zip \
        --region $(REGION)

deploy-weather: build-weather
    aws lambda update-function-code \
        --function-name weather-lambda \
        --zip-file fileb://weather_lambda.zip \
        --region $(REGION)

deploy-all: build-collection build-weather
    aws lambda update-function-code \
        --function-name collection-lambda \
        --zip-file fileb://collection_lambda.zip \
        --region $(REGION)
    aws lambda update-function-code \
        --function-name weather-lambda \
        --zip-file fileb://weather_lambda.zip \
        --region $(REGION)
