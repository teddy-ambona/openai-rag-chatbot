# Extract embedding from text using OpenAI
def embed(text: str, openai_client: object, openai_engine: str = "text-embedding-3-small") -> list:
    """Convert raw text to embedding using OpenAI API."""
    response = openai_client.embeddings.create(input=text, model=openai_engine)
    return response.data[0].embedding
