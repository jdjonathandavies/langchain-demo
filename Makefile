.PHONY: install clean lock build run

install:
	poetry install

lock:
	poetry lock
	
clean:
	poetry env remove --all

build:
	docker build -t langchain_demo:latest .

run:
	docker run -i -p 8080:5000 langchain_demo:latest