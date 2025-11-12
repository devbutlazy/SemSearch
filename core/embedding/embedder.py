import numpy as np

from FlagEmbedding import BGEM3FlagModel

from core.database.repositories.message import MessageRepository
from core.embedding import logger

class Embedder:
    def __init__(self, max_length: int = 256, batch_size: int = 256) -> None:
        self.model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
        self.max_length = max_length
        self.batch_size = batch_size

    def _embed_text(self, text: str, normalize: bool = True) -> np.ndarray:
        """
        Embed a single string and return its vector,
        """
        out = self.model.encode([text], max_length=self.max_length, return_dense=True)
        vec = np.array(out["dense_vecs"][0], dtype=np.float32)
        if normalize:
            vec /= np.linalg.norm(vec).clip(min=1e-12)
        return vec
    
    def _embed_texts(
        self,
        texts: list[str],
        normalize: bool = True,
    ) -> np.ndarray:
        """
        Embed a list of strings in batches for efficiency.
        Returns a numpy array of shape (len(texts), vector_dim).
        """

        all_vecs = []

        for index in range(0, len(texts), self.batch_size):
            batch = texts[index:index+self.batch_size]
            logger.info(f"Embedding batch {index} to {index + len(batch)}")

            out = self.model.encode(batch, max_length=self.max_length, return_dense=True)
            batch_vecs = np.array(out["dense_vecs"], dtype=np.float32)

            if normalize:
                batch_vecs /= np.linalg.norm(batch_vecs, axis=1, keepdims=True).clip(min=1e-12)

            all_vecs.append(batch_vecs)

        return np.vstack(all_vecs)

    async def run(self) -> None:
        """
        Fetch all messages without embeddings, generate embeddings in batches,
        and update the database with the new vectors.
        """
        logger.info("Starting embedding run...")

        async with MessageRepository() as repository:
            messages = await repository.get_unembedded_messages()
            if not messages:
                logger.info("No messages to embed.")
                return None

            logger.info(f"Fetched {len(messages)} messages without embeddings.")

            texts = [msg.message_text or "" for msg in messages]

            for i in range(0, len(texts), self.batch_size):
                batch_msgs = messages[i:i + self.batch_size]
                batch_texts = texts[i:i + self.batch_size]

                logger.info(f"Processing batch {i} to {i + len(batch_texts)}")
                batch_vecs = self._embed_texts(batch_texts) 

                for msg, vec in zip(batch_msgs, batch_vecs):
                    msg.embedding = vec.tolist()  

                await repository.add_messages_bulk(batch_msgs)
                logger.info(f"Updated embeddings for batch {i} to {i + len(batch_texts)}")
        
        logger.info("Embedding cycle completed.")
