import logging
import os

import langchain
from langchain_community.vectorstores import Milvus
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Enable logging the full prompt
langchain.debug = True


def format_docs(docs):
    global texts
    texts = [d.page_content for d in docs]
    return "\n\n".join([d.page_content for d in docs])


# Instantiate embedding function object
embedding_function = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"], model="text-embedding-3-small")

# Instantiate Milvus retriever object based on previously populated collection
vector_db = Milvus(
    collection_name="lasik_complications_db",
    embedding_function=embedding_function,
    connection_args={"host": "127.0.0.1", "port": "19530"},
    vector_field="embedding",
    text_field="text",
)
retriever = Milvus.as_retriever(vector_db, search_kwargs=dict(k=3, score_threshold=0.8))

# Instantiate LLM
llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")

# Prompt engineering
template = """Answer the question based only on the following context, be very verbose, refer to the below context only using the word "data":

{context}

Question: {question}
"""  # noqa: E501

prompt = ChatPromptTemplate.from_template(template)

chain = {"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()

# query = "How can I reduce my risk of complications before LASIK surgery?"
query = "Is there a contraindication for computer programmers to get LASIK?"

# query = "is there possible loss of sight for LASIK according to data?"

logging.info("Query: {query}")

response = chain.invoke(query)
