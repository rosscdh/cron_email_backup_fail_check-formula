.PHONY: bundle_install tests virtualenv setup build login push

NAME     := rosscdh/cron_email_backup_fail_check
TAG      := $$(git log -1 --pretty=%h)
VERSION  := ${NAME}:${TAG}
LATEST   := ${NAME}:latest

BUILD_REPO_ORIGIN=$$(git config --get remote.origin.url)
BUILD_COMMIT_SHA1:=$$(git rev-parse --short HEAD)
BUILD_COMMIT_DATE:=$$(git log -1 --date=short --pretty=format:%ct)
BUILD_BRANCH:=$$(git symbolic-ref --short HEAD)
BUILD_DATE:=$$(date -u +"%Y-%m-%dT%H:%M:%SZ")


bundle_install:
	bundle install

virtualenv:
	virtualenv .venv
	.venv/bin/pip install -r requirements.txt

setup: bundle_install virtualenv

tests:
	bundle exec kitchen converge
	bundle exec kitchen verify all

build:
	docker build -t ${LATEST} -t ${LATEST} \
		--build-arg BUILD_COMMIT_SHA1=${BUILD_COMMIT_SHA1} \
		--build-arg BUILD_COMMIT_DATE=${BUILD_COMMIT_DATE} \
		--build-arg BUILD_BRANCH=${BUILD_BRANCH} \
		--build-arg BUILD_DATE=${BUILD_DATE} \
		--build-arg BUILD_REPO_ORIGIN=${BUILD_REPO_ORIGIN} \
		-f ./cron_email_backup_fail_check/files/Dockerfile ./cron_email_backup_fail_check/files

push:
	docker push ${LATEST}
