# lasik-openai-rag &middot; ![ci](https://github.com/teddy-ambona/openai-rag-chatbot/actions/workflows/cicd.yml/badge.svg)


Demo LLM (RAG pipeline) web app running locally using docker-compose. LLM and embedding models are consumed from OpenAI.

## 1 - Target setup

A Retrieval Augmented Generation (RAG) pipeline is a NLP framework that combines information retrieval with text generation to produce responses or generate text. It uses a retriever to find relevant information and a generator to create responses based on that information.


The app architecture is presented below:

<img src="./docs/diagrams/rag-architecture.png" width="850"/>

Sequence diagram:

```mermaid
sequenceDiagram
    User->>Langserve API: query
    Note right of User:  Is there a contraindication <br/>for computer programmers <br/>to get LASIK?
    Langserve API->>OpenAI Embeddings: user query
    OpenAI Embeddings-->>Langserve API: embedding
    Langserve API->>MilvusDB: documents retrieval (vector search)
    MilvusDB-->>Langserve API: relevant documents
    Note right of Langserve API:  Prompt<br/>Engineering...
    Langserve API->>OpenAI LLM: enriched prompt
    OpenAI LLM-->>Langserve API: generated answer
```

UX:

<img src="./docs/img/ui.png" width="850"/>


## 2 - Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- An [OpenAI key](https://openai.com/)(account should be provisioned with $5, which is the minimum amount allowed)

## 3 - Quickstart

Build app Docker image:

```bash
make app-build
```

Set your OpenAI API key as environment variable

```bash
export OPENAI_API_KEY=<your-api-key>
```

Spin up Milvus DB:

```bash
make db-up
```

Populate DB with the LASIK eye surgery complications dataset:

```bash
make db-populate
```

<img src="./docs/img/db_populate.png" width="850"/>

Spin-up API:

```bash
make app-run
```

<img src="./docs/img/app_run.png" width="850"/>

The chatbot is now available at [http://localhost:8000/lasik_complications/playground/](http://localhost:8000/lasik_complications/playground/)

<insert image>


Display all available commands with:

```bash
make help
```

<img src="./docs/img/make_help.png" width="850"/>

Clean up

```bash
make clean
```

## 4 - Project file structure

## Milvus

[Milvus](https://github.com/milvus-io/milvus) is an open-source vector database engine developed by Zilliz, designed to store and manage large-scale vector data, such as embeddings, features, and high-dimensional data. It provides efficient storage, indexing, and retrieval capabilities for **vector similarity search tasks**.

## LLMOps

## 5 - Langchain

## 6 - Prompt Engineering

## 7 - Langserve

