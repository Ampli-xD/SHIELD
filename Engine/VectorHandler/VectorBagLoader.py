import json
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions


def load_categories(collection_name="CategoryBags",
                    category_bags_path="./CategoryBags",
                    db_path="./persistent_chroma_db"):
    """
    One-time loader for category data into ChromaDB.

    Args:
        collection_name (str): Name of the ChromaDB collection
        category_bags_path (str): Path to directory containing category JSON files
        db_path (str): Path to store ChromaDB files

    Returns:
        tuple: (ChromaDB collection, list of loaded categories)
    """

    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    client = chromadb.PersistentClient(path=db_path)

    existing_collections = client.list_collections()
    if collection_name not in [c.name for c in existing_collections]:
        collection = client.create_collection(
            name=collection_name,
            embedding_function=embedding_function,
            metadata={"hnsw:space": "cosine", "description": "Content categories with BERT embeddings"}
        )
        print("Created new collection")
    else:
        # Get the existing collection
        collection = client.get_collection(name=collection_name)
        print(f"Found existing collection with {collection.count()} entries")

    path = Path(category_bags_path)
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {category_bags_path}")

    try:
        collection.delete(ids=collection.get()['ids'])
        print("Cleared existing collection")
    except Exception as e:
        print(f"Could not clear collection: {e}")

    loaded_categories = []
    total_entries = 0

    batch_size = 1000
    for json_file in path.glob("*.json"):
        category_name = json_file.stem

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                words = json.load(f)

            if not isinstance(words, list):
                print(f"Warning: {category_name}.json should contain a list of words/phrases")
                continue

            for i in range(0, len(words), batch_size):
                batch = words[i:i + batch_size]
                ids = [f"{category_name}_{j}" for j in range(i, i + len(batch))]
                metadatas = [
                    {
                        "category": category_name,
                        "index": j,
                        "total_entries": len(words)
                    }
                    for j in range(i, i + len(batch))
                ]

                # Add the batch to the collection
                collection.add(
                    documents=batch,
                    metadatas=metadatas,
                    ids=ids
                )

            loaded_categories.append(category_name)
            total_entries += len(words)
            print(f"Loaded {len(words)} entries for category: {category_name}")

        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {json_file}")
        except Exception as e:
            print(f"Error loading {json_file}: {e}")

    print(f"\nSuccessfully loaded {len(loaded_categories)} categories with {total_entries} total entries")

    return collection, loaded_categories


if __name__ == "__main__":
    try:
        collection, categories = load_categories()
        print("\nCategory loading completed successfully!")
    except Exception as e:
        print(f"Error during category loading: {e}")
