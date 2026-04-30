import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class RAGEngine:

    def __init__(self, rule_folder="rules"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.text_chunks = []
        self.index = None
        self.load_rules(rule_folder)

    def load_rules(self, folder):
        for file in os.listdir(folder):
            if file.endswith(".txt"):
                with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    self.text_chunks.append(content)

        embeddings = self.model.encode(self.text_chunks)
        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings))

    def retrieve(self, query, top_k=1):
        query_vec = self.model.encode([query])
        D, I = self.index.search(np.array(query_vec), top_k)
        return [self.text_chunks[i] for i in I[0]]