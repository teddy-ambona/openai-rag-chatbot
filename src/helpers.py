# Extract embedding from text using OpenAI
def embed(texts: list, openai_client: object, openai_engine: str = "text-embedding-3-small") -> list[list]:
    """Convert raw text to embedding using OpenAI API."""
    response = openai_client.embeddings.create(input=texts, model=openai_engine)

    res = [x.embedding for x in response.data]
    return res
