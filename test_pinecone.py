import os
from dotenv import load_dotenv
from pinecone_client import list_indexes, upsert_data, query_data
from agent.memory import store_memory, retrieve_memory
from agent.agent import embedding_model

# Load environment variables
load_dotenv()

def test_pinecone_setup():
    """Test basic Pinecone functionality"""
    print("\n1. Testing Pinecone Setup:")
    print("-" * 50)
    
    # Test listing indexes
    indexes = list_indexes()
    print(f"Available indexes: {indexes}")
    
    # Verify our index exists
    index_name = os.getenv("PINECONE_INDEX")
    assert index_name in indexes, f"Index {index_name} not found!"
    print(f"✅ Index '{index_name}' exists")

def test_memory_operations():
    """Test memory storage and retrieval"""
    print("\n2. Testing Memory Operations:")
    print("-" * 50)
    
    # Test storing a memory
    test_text = "This is a test memory about YouTube content creation"
    test_metadata = {
        "type": "test",
        "category": "testing",
        "importance": "high"
    }
    
    print("Storing test memory...")
    store_memory(
        text=test_text,
        metadata=test_metadata,
        embedding_model=embedding_model
    )
    print("✅ Memory stored successfully")
    
    # Test retrieving the memory
    print("\nRetrieving similar memories...")
    results = retrieve_memory(
        query="YouTube content creation",
        embedding_model=embedding_model,
        top_k=3
    )
    
    print(f"\nFound {len(results)} similar memories:")
    for i, doc in enumerate(results, 1):
        print(f"\nMemory {i}:")
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}")

def test_agent_memory():
    """Test the agent's memory integration"""
    print("\n3. Testing Agent Memory Integration:")
    print("-" * 50)
    
    # Test storing a conversation
    user_query = "What are some trending topics for tech YouTube channels?"
    agent_response = "Based on current trends, AI tools, coding tutorials, and tech reviews are popular topics."
    
    print("Storing conversation...")
    store_memory(
        text=user_query,
        metadata={"type": "user_query", "response": agent_response},
        embedding_model=embedding_model
    )
    
    store_memory(
        text=agent_response,
        metadata={"type": "agent_response", "query": user_query},
        embedding_model=embedding_model
    )
    print("✅ Conversation stored successfully")
    
    # Test retrieving the conversation
    print("\nRetrieving conversation context...")
    results = retrieve_memory(
        query="tech YouTube channels trending topics",
        embedding_model=embedding_model,
        top_k=2
    )
    
    print(f"\nFound {len(results)} relevant memories:")
    for i, doc in enumerate(results, 1):
        print(f"\nMemory {i}:")
        print(f"Content: {doc.page_content}")
        print(f"Type: {doc.metadata.get('type', 'unknown')}")

if __name__ == "__main__":
    print("🧪 Starting Pinecone Integration Tests")
    print("=" * 50)
    
    try:
        test_pinecone_setup()
        test_memory_operations()
        test_agent_memory()
        print("\n✅ All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}") 