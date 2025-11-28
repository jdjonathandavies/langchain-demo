
PACKAGE = langchain_demo
.PHONY: install clean format lint lock build run

install:
	poetry install

lock:
	poetry lock
	
clean:
	poetry env remove --all

format:
	poetry run ruff check --select I --fix $(PACKAGE)
	poetry run ruff format $(PACKAGE)

lint:
	poetry run ruff check --fix $(PACKAGE)
	poetry run mypy $(PACKAGE)

build:
	docker build -t $(PACKAGE):latest .

run:
	docker run -i -p 8080:5000 $(PACKAGE):latest