.PHONY: install clean lock

install:
	poetry install

lock:
	poetry lock
	
clean:
	poetry env remove --all