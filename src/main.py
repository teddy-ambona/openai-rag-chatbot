from helpers import embed
from pymilvus import MilvusClient


# Search the database based on input text
def search(text, milvus_client):
    # Search parameters for the index
    search_params = {"metric_type": "L2"}

    results = milvus_client.search(
        collection_name="lasik_complications_db",
        data=[embed(text)],  # Embeded search value
        anns_field="embedding",  # Search across embeddings
        param=search_params,
        limit=5,  # Limit to five results per search
        output_fields=["title"],  # Include title field in result
    )

    ret = []
    for hit in results[0]:
        row = [hit.id, hit.score, hit.entity.get("title")]  # Get the timestamp, text, keywords for the results
        ret.append(row)
    return ret


# Set up a Milvus client
client = MilvusClient(uri="http://localhost:19530")

search_terms = ["self-improvement", "landscape"]

for x in search_terms:
    print("Search term:", x)
    for result in search(x):
        print(result)
    print()
