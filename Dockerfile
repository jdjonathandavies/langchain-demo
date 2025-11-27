FROM python:3.13-slim

RUN pip install poetry

WORKDIR /langchain-demo/

COPY .env /langchain-demo/
COPY langchain_demo /langchain-demo/langchain_demo/
COPY poetry.lock /langchain-demo/
COPY pyproject.toml /langchain-demo/
COPY Makefile /langchain-demo/
COPY README.md /langchain-demo/

#RUN make install
RUN poetry install
EXPOSE 5000

ENTRYPOINT ["poetry", "run", "python", "langchain_demo/server.py"]