import os

import langchain
from fastapi import FastAPI
from langchain_community.vectorstores import Milvus
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langserve import add_routes

from config import CONFIG

# Enable logging the full prompt
langchain.debug = True


def format_docs(docs):
    """Extract necessary information from the retrieved documents."""
    return "\n\n".join([d.page_content for d in docs])


# Instantiate embedding function object
embedding_function = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"], model="text-embedding-3-small")

# Instantiate Milvus retriever object based on previously populated collection
vector_db = Milvus(
    collection_name=CONFIG["COLLECTION_NAME"],
    embedding_function=embedding_function,
    connection_args={"host": CONFIG["MILVUS_HOST"], "port": CONFIG["MILVUS_PORT"]},
    vector_field="embedding",
    text_field="text",
)
retriever = Milvus.as_retriever(vector_db, search_kwargs=dict(k=3, score_threshold=0.8))

# Instantiate LLM, "temperature" controls the level of creativity of the model
llm = ChatOpenAI(temperature=0.7, model_name=CONFIG["LLM_MODEL"])

# Prompt engineering
template = """Answer the question based only on the following context, be very verbose, refer to the below context only using the word "data":

{context}

Question: {question}
"""  # noqa: E501

prompt = ChatPromptTemplate.from_template(template)

# Build chain
chain = {"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

add_routes(
    app,
    chain,
    path="/lasik_complications",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=CONFIG["API_HOST"], port=CONFIG["API_PORT"])
