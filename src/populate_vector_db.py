import logging
import os

import pandas as pd
import tiktoken
from helpers import embed
from openai import OpenAI
from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, connections, utility

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")

# Source: https://www.kaggle.com/datasets/shivamb/lasik-complications-dataset/data
FILE = "./data/laser_eye_surgery_complications.csv"
COLLECTION_NAME = "lasik_complications_db"  # Collection name
DIMENSION = 1536  # Embeddings size

# Because the embedding process for a free OpenAI account is relatively time-consuming,
# we use a set of data small enough to reach a balance between the script executing time
# and the precision of the search results. You can change the COUNT constant to fit your needs.
COUNT = 10  # How many titles to embed and insert.
MILVUS_HOST = "localhost"  # Milvus server URI
MILVUS_PORT = "19530"

openai_client = OpenAI()
openai_client.api_key = os.environ["OPENAI_API_KEY"]  # Use your own Open AI API Key here

# Connect to Milvus
connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

# Make DB population script idempotent
if utility.has_collection(COLLECTION_NAME):
    utility.drop_collection(COLLECTION_NAME)

# Create collection
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, descrition="Ids", is_primary=True, auto_id=False),
    FieldSchema(name="timestamp", dtype=DataType.INT64, description="Date in a timestamp format"),
    FieldSchema(name="text", dtype=DataType.VARCHAR, description="original text", max_length=2000),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, description="Embedding vectors", dim=DIMENSION),
    FieldSchema(name="keywords", dtype=DataType.VARCHAR, description="comma separated keywords", max_length=200),
]
schema = CollectionSchema(fields=fields, description="LASIK complications collection")
collection = Collection(name=COLLECTION_NAME, schema=schema)

# Create an index for the collection.
index_params = {"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 1024}}
collection.create_index(field_name="embedding", index_params=index_params)

df = pd.read_csv("data/laser_eye_surgery_complications.csv")
df["date"] = pd.to_datetime(df["date"])
df["ts"] = df["date"].astype(int)

# To get the tokeniser corresponding to a specific model in the OpenAI API:
enc = tiktoken.encoding_for_model("gpt-4")

# Check how many tokens we are requesting
df["token"] = df["text"].apply(enc.encode)
total_number_tokens = df["token"].apply(len).sum()
logging.info(f"Total number of tokens passed into the OpenAI API: {total_number_tokens}")

# Premium OpenAI account limited to 3000 RPM, dataset should have less rows than that
logging.info(f"Inserting {len(df)} rows")
for row in df.head(2).itertuples():
    # Insert is / timestamp / original text / text embedding / keywords
    ins = [[row.id], [row.ts], [row.text], [embed(row.text, openai_client)], [row.keywords]]
    collection.insert(ins)

logging.info("Insertion finished")


x = 1
