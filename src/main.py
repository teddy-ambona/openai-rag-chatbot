import logging
import os

from openai import OpenAI
from pymilvus import MilvusClient

from helpers import embed


# Search the database based on input text
def search(embedding, milvus_client):
    # Search parameters for the index
    search_params = {"metric_type": "L2"}

    results = milvus_client.search(
        collection_name="lasik_complications_db",
        data=[embedding],
        anns_field="embedding",  # Search across embeddings
        search_params=search_params,
        limit=5,  # Limit to five results per search
        output_fields=["timestamp", "text", "keywords"],  # Include ts, original text and keywords in result
    )

    ret = []
    for hit in results[0]:
        # Get the timestamp, text, keywords for the results
        ret.append(hit["entity"])
    return ret


# Set up a Milvus client
milvus_client = MilvusClient(uri="http://localhost:19530")
openai_client = OpenAI()
openai_client.api_key = os.environ["OPENAI_API_KEY"]  # Use your own Open AI API Key here

res = milvus_client.get_load_state(collection_name="lasik_complications_db")


# query = "How can I reduce my risk of complications before LASIK surgery?"
query = "loss of sight"

logging.info("Query: {query}")
embedding = embed([query], openai_client)[0]

results = search(embedding, milvus_client)

for result in results:
    print(result)

# llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")
# memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

# conversation_chain = ConversationalRetrievalChain.from_llm(
#     llm=llm,
#     chain_type="stuff",
#     retriever=vectorstore.as_retriever(),
#     memory=memory
# )
