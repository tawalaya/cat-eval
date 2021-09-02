
.PHONY: build
BUILD:
	npm install
	zip "build-$(git rev-parse --short HEAD).zip" package.json *.js node_modules/*
	rm -rf node_modules

.PHONY: gcf
GCF: BUILD
	gcloud functions deploy prime --memory 200 --runtime=nodejs14 --allow-unauthenticated --source "build-$(git rev-parse --short HEAD).zip" --entry-point http

.PHONY: aws
AWS: BUILD
	aws lambda create-function --function-name prime --runtime nodejs14.x --handler aws --memory-size 200 --zip-file "build-$(git rev-parse --short HEAD).zip"

clean:
	aws lambda delete-function --function-name prime
	gcloud functions delete prime