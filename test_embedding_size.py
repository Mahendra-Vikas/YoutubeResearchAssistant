from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

# Map GEMINI_API_KEY to what LangChain expects
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Initialize the embedding model
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Test text
test_text = "This is a test sentence to check embedding dimensions"

# Get embedding
embedding = embedding_model.embed_query(test_text)

print(f"Embedding dimension: {len(embedding)}")
print(f"First few values: {embedding[:5]}") 