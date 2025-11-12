import numpy as np
from FlagEmbedding import BGEM3FlagModel

from core.embedder import logger


class EmbeddingModel:
    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
        use_fp16: bool = True,
        max_length: int = 256,
    ):
        self.model = BGEM3FlagModel(model_name, use_fp16=use_fp16)
        self.max_length = max_length

    def embed_text(self, text: str, normalize: bool = True) -> np.ndarray:
        """
        Embed a single string.
        """
        vec = np.array(
            self.model.encode([text], max_length=self.max_length, return_dense=True)[
                "dense_vecs"
            ][0],
            dtype=np.float32,
        )
        if normalize:
            vec /= np.linalg.norm(vec).clip(min=1e-12)
        return vec

    def embed_texts(
        self, texts: list[str], batch_size: int = 256, normalize: bool = True
    ) -> np.ndarray:
        """
        Embed a list of strings efficiently in batches.
        """
        all_vecs = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            logger.info(f"Embedding batch {i}-{i + len(batch)}")
            batch_vecs = np.array(
                self.model.encode(batch, max_length=self.max_length, return_dense=True)[
                    "dense_vecs"
                ],
                dtype=np.float32,
            )

            if normalize:
                batch_vecs /= np.linalg.norm(batch_vecs, axis=1, keepdims=True).clip(
                    min=1e-12
                )
            all_vecs.append(batch_vecs)

        return np.vstack(all_vecs)
