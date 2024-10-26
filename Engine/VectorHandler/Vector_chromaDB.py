import chromadb
from chromadb.utils import embedding_functions


class ContentDetectionSystem:
    def __init__(self, path="./persistent_chroma_db"):
        # Use BERT embeddings for better similarity scoring
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        # Initialize ChromaDB with the updated configuration
        self.client = chromadb.PersistentClient(path=path)

        try:
            self.collection = self.client.get_collection(
                name="CategoryBags",
            )
            print(f"Loaded existing collection with {self.collection.count()} entries")
        except ValueError:
            raise ValueError("The collection 'CategoryBags' does not exist. Please ensure it is loaded first.")

    def check_content(self, text, n_results=5):
        """Get similarity scores for input text across all categories."""
        if self.collection.count() == 0:
            raise ValueError("No categories loaded. Please run load() first.")

        results = self.collection.query(
            query_texts=[text],
            n_results=n_results
        )

        # Calculate average similarity per category
        category_scores = {}
        print(results["distances"])
        for i in range(len(results['metadatas'][0])):
            category = results['metadatas'][0][i]['category']
            # Convert distance to similarity score (0-100%)
            similarity = max(0, min(100, (1 - results['distances'][0][i]) * 100))

            if category in category_scores:
                category_scores[category].append(similarity)
            else:
                category_scores[category] = [similarity]

        # Average the scores for each category
        final_scores = {
            cat: sum(scores) / len(scores)
            for cat, scores in category_scores.items()
        }

        # Return the scores without sorting
        return final_scores
        # return category_scores


# Example usage
if __name__ == "__main__":
    # Initialize system
    try:
        system = ContentDetectionSystem()

        # Test the system
        test_text = """I see it it's in front of me, clear and loud
Is it open as the sky or grey as a cloud
It's the feeling I hold, I hold beyond control
Do I love her? Is the question, upon I stroll
when its me thinking she might be the one I lost
But I didn't love her right? 
We were not together under the same days of frost
Then why is it so it affects me to the deepest in the days and darkest at the night?
It's ok my eyes say, It's just overthinking says the brain 
My heart doubts the line of love and obsession 
As I sit and watch the rain
"""

        results = system.check_content(test_text)

        print(f"\nFor the Text:{test_text}")
        print("\nSimilarity Scores (Percentage):")
        for category, score in results.items():
            print(f"{category}: {score}%")

    except Exception as e:
        print(f"Error: {e}")
