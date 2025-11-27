
PACKAGE = langchain_demo
.PHONY: install clean format lock build run

install:
	poetry install

lock:
	poetry lock
	
clean:
	poetry env remove --all

format:
	poetry run ruff format $(PACKAGE)

build:
	docker build -t $(PACKAGE):latest .

run:
	docker run -i -p 8080:5000 $(PACKAGE):latest