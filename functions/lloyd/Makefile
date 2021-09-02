.EXPORT_ALL_VARIABLES:

OPSIZE ?= 2000
ITTER ?= 1000
DEPTH ?= 10
NAME ?= lloyd

.PHONY: build
BUILD:
	pip install --target ./vendor  -r requirements.txt
	envsubst < _main.py > main.py
	zip "build-$(git rev-parse --short HEAD).zip" main.py logging.py 
	cd vendor && zip -r ../"build-$(git rev-parse --short HEAD).zip" .
	rm -rf vendor
	rm main.py

.PHONY: gcf
GCF: BUILD
	gsutil mb "gs://$BUCKET"
	gcloud functions deploy $NAME" --memory 200 --runtime=python37 --allow-unauthenticated --source "build-$(git rev-parse --short HEAD).zip" --entry-point http

.PHONY: aws
AWS: BUILD
	aws s3 mb "s3://$BUCKET"
	aws lambda create-function --function-name "$NAME" --runtime python3.7 --handler aws --memory-size 200 --zip-file "build-$(git rev-parse --short HEAD).zip"

clean:
	aws lambda delete-function --function-name "$NAME"
	gcloud functions delete "$NAME"