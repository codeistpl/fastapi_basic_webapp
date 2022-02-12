run:
	uvicorn main:app --reload

test:
	pytest

format:
	black .

lint:
	flake8 .
