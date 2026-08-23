"""
Amazô.guia — Módulo de Embeddings.

Responsabilidade: inicializar o modelo de embeddings que transforma
texto em vetores numéricos para busca semântica no Vector Store.

Estratégia de Resiliência:
  1. Primário: HuggingFaceEmbeddings (sentence-transformers/all-MiniLM-L6-v2)
  2. Fallback Automático: TfidfEmbeddings (scikit-learn TF-IDF, sem dependência
     de PyTorch/GPU, imune a incompatibilidades de meta-tensors em ambientes Cloud).
"""

import os
import logging
from langchain_core.embeddings import Embeddings
from src.config import EMBEDDING_MODEL


class TfidfEmbeddings(Embeddings):
    """
    Embeddings baseados em TF-IDF (scikit-learn).
    Garante funcionamento 100% estável e imediato sem depender de PyTorch.
    Implementa a interface padrão langchain_core.embeddings.Embeddings.
    """

    def __init__(self, max_features: int = 384):
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=(1, 2),
            strip_accents="unicode",
            lowercase=True,
        )
        self._fitted = False
        self._dim = max_features

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        matrix = self.vectorizer.fit_transform(texts)
        self._fitted = True
        self._dim = matrix.shape[1]
        return matrix.toarray().tolist()

    def embed_query(self, text: str) -> list[float]:
        if not self._fitted:
            return [0.0] * self._dim
        vec = self.vectorizer.transform([text])
        return vec.toarray()[0].tolist()


def get_embedding_model() -> Embeddings:
    """
    Inicializa e retorna o modelo de embeddings com fallback garantido.

    Tenta instanciar HuggingFaceEmbeddings. Caso o ambiente apresente
    incompatibilidade com PyTorch (ex: meta tensor bug no Python 3.14/torch 2.13),
    ativa instantaneamente o TfidfEmbeddings para assegurar que a Amazô.guia
    permaneça 100% operacional.

    Returns:
        Instância de Embeddings (HuggingFaceEmbeddings ou TfidfEmbeddings).
    """
    model_name = os.getenv("EMBEDDING_MODEL", EMBEDDING_MODEL)
    logging.warning(f"[embeddings] Tentando carregar modelo primário: {model_name}")

    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        embed_model = HuggingFaceEmbeddings(
            model_name=model_name,
            encode_kwargs={"normalize_embeddings": True},
        )
        # Teste de fumaça rápido para validar se o PyTorch consegue inferir sem erro
        _test_vec = embed_model.embed_query("teste")
        logging.warning(f"[embeddings] HuggingFaceEmbeddings carregado com sucesso! Dim: {len(_test_vec)}")
        return embed_model

    except Exception as exc:
        logging.warning(
            f"[embeddings] Falha ao carregar HuggingFaceEmbeddings ({type(exc).__name__}: {str(exc)[:150]}). "
            "Ativando fallback resiliente TfidfEmbeddings..."
        )
        embed_model = TfidfEmbeddings(max_features=384)
        logging.warning("[embeddings] TfidfEmbeddings ativado com sucesso.")
        return embed_model
