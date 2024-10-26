import faiss
import numpy as np
import torch
from transformers import BertModel, BertTokenizer


# Text Embedding Model using BERT
class TextEmbeddingModel:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')

    def get_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).numpy()


# Vector Database using FAISS with Cosine Similarity
class MultiLabelVectorDatabase:
    def __init__(self, embedding_dim):
        # Each category has its own FAISS index for cosine similarity
        self.categories = {
            "sexually_explicit_material": faiss.IndexFlatIP(embedding_dim),  # Inner product = cosine similarity
            "child_exploitation_and_abuse": faiss.IndexFlatIP(embedding_dim),
            "self_harm_and_suicide": faiss.IndexFlatIP(embedding_dim),
            "violence_and_terrorism": faiss.IndexFlatIP(embedding_dim),
            "hate_speech_and_racial_slurs": faiss.IndexFlatIP(embedding_dim),
            "substance_abuse": faiss.IndexFlatIP(embedding_dim),
            "body_shaming_and_eating_disorders": faiss.IndexFlatIP(embedding_dim),
            "cyberbullying_and_harassment": faiss.IndexFlatIP(embedding_dim),
            "misinfo_and_fake_news": faiss.IndexFlatIP(embedding_dim)
        }
        self.embeddings = {category: [] for category in self.categories}

    def add_embedding(self, embedding, category):
        if category in self.categories:
            # Normalize the embedding for cosine similarity
            normalized_embedding = embedding / np.linalg.norm(embedding)
            self.embeddings[category].append(normalized_embedding)
            self.categories[category].add(np.array(self.embeddings[category]))

    def search_similar(self, query_embedding, top_k=1):
        # Normalize the query embedding for cosine similarity
        normalized_query = query_embedding / np.linalg.norm(query_embedding)
        similarities = {}
        for category, index in self.categories.items():
            distances, _ = index.search(np.array([normalized_query]), top_k)
            # Since we use inner product, higher distance means more similar
            if distances[0][0] != -float('inf'):  # Valid match found
                similarities[category] = distances[0][0]  # Cosine similarity directly from FAISS
        return similarities


# Main System Class for Multi-Label Content Detection
class ExplicitContentDetectionSystem:
    def __init__(self, text_model, vector_db):
        self.text_model = text_model
        self.vector_db = vector_db

    def add_explicit_content(self, content, category):
        # No preprocessing, directly pass the content to embedding generation
        embedding = self.text_model.get_embedding(content)
        self.vector_db.add_embedding(embedding, category)

    def check_content(self, content):
        # No preprocessing, directly pass the input content to embedding generation
        embedding = self.text_model.get_embedding(content)

        # Search for the most similar explicit category
        classification_scores = self.vector_db.search_similar(embedding, top_k=1)
        return classification_scores


# Usage

# Initialize models
text_model = TextEmbeddingModel()

# Vector database for 768-dim embeddings (BERT embeddings are 768-dim)
vector_db = MultiLabelVectorDatabase(embedding_dim=768)

# System
system = ExplicitContentDetectionSystem(text_model, vector_db)

# Add explicit content examples (Training phase)
system.add_explicit_content("This is sexually explicit material", category="sexually_explicit_material")
system.add_explicit_content("Violence and terrorism content example", category="violence_and_terrorism")

# Check new content (Inference phase)
test_text = "This text promotes violence and terrorism"
classification_scores = system.check_content(test_text)
print("Classification Scores:", classification_scores)
