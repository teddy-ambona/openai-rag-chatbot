# lasik-openai-rag

Demo LLM (RAG pipeline) web app running locally using docker-compose

## 1 - Target setup

explain Retrieval Augmented Generation here

## 2 - Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- An [OpenAI key](https://openai.com/)(account should be provisioned with $5, which is the minimum amount allowed)

## 3 - Quickstart

Spin up Milvus DB:

```bash
make db-up
```

Build app Docker image:

```bash
make app-build
```

Set your OpenAI API key as environment variable

```bash
export OPENAI_API_KEY=<your-api-key>
```

Populate DB with the LASIK eye surgery complications dataset:

```bash
make db-populate
```

Spin-up API:

```bash
make app-run
```

The chatbot is now available at [http://localhost:8000/lasik_complications/playground/](http://localhost:8000/lasik_complications/playground/)

<insert image>


Display all available commands with:

```bash
make help
```

<insert screenshot>


## 4 - Project file structure

## 5 - Langchain

## 6 - Prompt Engineering

## 7 - Langserve

