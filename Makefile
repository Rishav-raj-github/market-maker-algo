.PHONY: test run install

install:
	pip install -r requirements.txt

test:
	python -m unittest discover tests/

run:
	python main.py

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
