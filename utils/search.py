import os
import openai
import json
from typing import List, Tuple
from bs4 import BeautifulSoup
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")

# Load scraped data
with open("data/discourse.json") as f:
    discourse_data = json.load(f)

def embed_text(text):
    resp = openai.Embedding.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return np.array(resp["data"][0]["embedding"])

# Cache embeddings
discourse_embeddings = [(item["content"], embed_text(BeautifulSoup(item["content"], "html.parser").get_text())) for item in discourse_data]

def search_similar(text, k=3):
    query_vec = embed_text(text)
    sims = [(doc, cosine_similarity([query_vec], [vec])[0][0]) for doc, vec in discourse_embeddings]
    return sorted(sims, key=lambda x: x[1], reverse=True)[:k]

def answer_question(question: str, image_base64: str = None) -> Tuple[str, List[dict]]:
    top_docs = search_similar(question)
    context = "\n".join([BeautifulSoup(doc[0], "html.parser").get_text() for doc, _ in top_docs])
    
    prompt = f"Use the context to answer the question:\nContext:\n{context}\n\nQuestion: {question}"
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = resp["choices"][0]["message"]["content"]
    
    links = [{"url": discourse_data[i]["url"], "text": discourse_data[i]["topic"]} for i in range(len(top_docs))]
    return answer, links
