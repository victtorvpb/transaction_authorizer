SHELL=/bin/bash
IMAGE_NAME=transaction_authorizer

build:
	docker build -t $(IMAGE_NAME) .

test:
	docker run  -i --rm  --name teste   $(IMAGE_NAME) python -m unittest discover -v -b

run:
	docker run  -i --rm  --name teste   $(IMAGE_NAME) python transaction_authorizer.py < $(input_file)