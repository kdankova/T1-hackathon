import requests
from langchain.embeddings.base import Embeddings
from concurrent.futures import ThreadPoolExecutor, as_completed


class BGEM3Embeddings(Embeddings):
    def __init__(self, api_key: str, base_url: str = "https://llm.t1v.scibox.tech/v1",
                 model: str = "bge-m3", batch_size: int = 64, max_workers: int = 8, timeout: int = 120):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/") + "/embeddings"
        self.model = model
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate"
        })

    def _post_batch(self, texts):
        payload = {"model": self.model, "input": texts}
        resp = self.session.post(self.base_url, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        return [d["embedding"] for d in data["data"]]

    def _embed(self, texts):
        batches = [texts[i:i+self.batch_size] for i in range(0, len(texts), self.batch_size)]
        embeddings = [None] * len(batches)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._post_batch, batches[i]): i for i in range(len(batches))}
            for fut in as_completed(futures):
                idx = futures[fut]
                embeddings[idx] = fut.result()

        return [vec for batch in embeddings for vec in batch]

    def embed_documents(self, texts):
        return self._embed(texts)

    def embed_query(self, text):
        return self._embed([text])[0]


