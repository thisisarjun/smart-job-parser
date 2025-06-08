#!/usr/bin/env python3
"""
Example script to test the Text Processing API
Run this after starting the API server
"""

import requests

BASE_URL = "http://localhost:8000"


def test_api_connection():
    """Test if the API is running"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API is running!")
            return True
        else:
            print(f"❌ API connection failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running.")
        return False


def test_process_text():
    """Test the text processing endpoint"""
    print("\n⚙️ Testing Text Processing (Split + Embed + Search)...")

    sample_text = (
        """
    Artificial Intelligence (AI) has revolutionized many aspects of modern life.
    From healthcare to transportation, AI systems are being deployed to solve
    complex problems and improve efficiency. Machine learning, a subset of AI,
    enables systems to learn and improve from experience without being explicitly
    programmed. Natural Language Processing (NLP) is another important area that
    allows computers to understand and generate human language. Deep learning
    techniques use neural networks to process data and make predictions.
    """
        * 2
    )

    payload = {
        "text": sample_text,
        "query": "What is machine learning?",
        "chunk_size": 200,
        "chunk_overlap": 40,
    }

    try:
        print("   Sending request...")
        response = requests.post(f"{BASE_URL}/text/process", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Processed text into {result['chunk_count']} chunks")
            print(f"   Original length: {result['original_length']} characters")
            print(f"   Found {len(result['search_results'])} relevant chunks")

            # Show search results
            for i, doc in enumerate(result["search_results"], 1):
                # Handle different document formats from LangChain
                content = (
                    doc.get("page_content", str(doc))
                    if isinstance(doc, dict)
                    else str(doc)
                )
                preview = content[:100] + "..." if len(content) > 100 else content
                print(f"   Result {i}: {preview}")

            return True
        else:
            print(f"❌ Process text failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing process text: {e}")
        return False


def run_interactive_test():
    """Run an interactive test with user input"""
    print("\n🎯 Interactive Test")
    print("Enter your own text and query to test the API:")

    user_text = input("Text to process: ").strip()
    if not user_text:
        print("No text provided, skipping interactive test.")
        return

    user_query = input("Query to search: ").strip()
    if not user_query:
        user_query = "What is this about?"
        print(f"No query provided, using default: '{user_query}'")

    try:
        chunk_size = int(input("Chunk size (default 200): ") or "200")
        overlap = int(input("Chunk overlap (default 50): ") or "50")
    except ValueError:
        chunk_size, overlap = 200, 50
        print("Using default values: chunk_size=200, overlap=50")

    payload = {
        "text": user_text,
        "query": user_query,
        "chunk_size": chunk_size,
        "chunk_overlap": overlap,
    }

    try:
        response = requests.post(f"{BASE_URL}/text/process", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Results:")
            print(f"   Chunks: {result['chunk_count']}")
            print(f"   Original length: {result['original_length']}")
            print(f"   Search results: {len(result['search_results'])}")

            print(f"\n   Top results for '{user_query}':")
            for i, doc in enumerate(result["search_results"], 1):
                content = (
                    doc.get("page_content", str(doc))
                    if isinstance(doc, dict)
                    else str(doc)
                )
                suffix = "..." if len(content) > 150 else ""
                print(f"\n   Result {i}: {content[:150]}{suffix}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run API test"""
    print("🧪 Text Processing API Test")
    print("=" * 40)

    # Test connection
    if not test_api_connection():
        print("\n💡 To start the API server, run: python start_api.py")
        return

    # Test the main endpoint
    if test_process_text():
        print("\n🎉 Test passed!")

        # Offer interactive test
        if (
            input("\nWould you like to run an interactive test? (y/n): ")
            .lower()
            .startswith("y")
        ):
            run_interactive_test()
    else:
        print("\n❌ Test failed. Check the API server logs.")


if __name__ == "__main__":
    main()
