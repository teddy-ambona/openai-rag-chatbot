import logging
import os

import pandas as pd
import tiktoken
from openai import OpenAI
from pymilvus import DataType, MilvusClient

from helpers import embed

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")

# Source: https://www.kaggle.com/datasets/shivamb/lasik-complications-dataset/data
FILE = "./data/laser_eye_surgery_complications.csv"
COLLECTION_NAME = "lasik_complications_db"  # Collection name
# Because the embedding process for a free OpenAI account is relatively time-consuming,
# we use a set of data small enough to reach a balance between the script executing time
# and the precision of the search results. You can change the COUNT constant to fit your needs.
COUNT = 10  # How many titles to embed and insert.
MILVUS_HOST = "localhost"  # Milvus server URI
MILVUS_PORT = "19530"

milvus_client = MilvusClient(uri=f"http://{MILVUS_HOST}:{MILVUS_PORT}")
openai_client = OpenAI()
openai_client.api_key = os.environ["OPENAI_API_KEY"]  # Use your own Open AI API Key here

# Make DB population script idempotent
if milvus_client.has_collection(COLLECTION_NAME):
    milvus_client.drop_collection(COLLECTION_NAME)


# Create collection
# Create schema
schema = milvus_client.create_schema(auto_id=False, enable_dynamic_field=True, description="LASIK complications collection")

# Add fields to schema
schema.add_field(field_name="id", datatype=DataType.INT64, descrition="Ids", is_primary=True, auto_id=False)
schema.add_field(field_name="timestamp", datatype=DataType.INT64, description="Date in a timestamp format")
schema.add_field(field_name="text", datatype=DataType.VARCHAR, description="original text", max_length=8000)
schema.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, description="Embedding vectors", dim=1536)
schema.add_field(field_name="keywords", datatype=DataType.VARCHAR, description="comma separated keywords", max_length=200)

# Add index
index_params = milvus_client.prepare_index_params()
index_params.add_index(field_name="embedding", index_type="IVF_FLAT", metric_type="L2", params={"nlist": 1024})

# Create a collection
milvus_client.create_collection(collection_name=COLLECTION_NAME, schema=schema, index_params=index_params)

df = pd.read_csv("data/laser_eye_surgery_complications.csv")
df["date"] = pd.to_datetime(df["date"])
df["timestamp"] = df["date"].astype(int)
df["keywords"] = df["keywords"].apply(lambda k: str(k) if not pd.isnull(k) else "")

# To get the tokeniser corresponding to a specific model in the OpenAI API:
enc = tiktoken.encoding_for_model("gpt-4")

# Check how many tokens we are requesting
df["token"] = df["text"].apply(enc.encode)
total_number_tokens = df["token"].apply(len).sum()
logging.info(f"Total number of tokens passed into the OpenAI API: {total_number_tokens}")

# Premium OpenAI account limited to 1'000'000 tokens per minute, dataset has less than 300'000 tokens
logging.info("Getting embeddings from OpenAI")

embeddings = embed(df["text"].to_list(), openai_client)
df["embedding"] = embeddings

logging.info(f"Inserting {len(df)} rows")
df_insert = df[["id", "timestamp", "text", "embedding", "keywords"]]

milvus_client.insert(collection_name=COLLECTION_NAME, data=df_insert.to_dict(orient="records"))

logging.info("Insertion finished")
