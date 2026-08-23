"""
Amazô.guia — Módulo de Vector Store.

Responsabilidade: receber os documentos processados pelo ingest.py,
vetorizá-los com o modelo de embeddings e armazená-los em memória
para recuperação semântica.

Decisão técnica: InMemoryVectorStore da LangChain foi escolhido por:
- Simplicidade máxima para o MVP: sem banco externo, sem configuração
- Read-only e stateless: adequado ao contexto do Challenge (sem escrita)
- Performance suficiente para a base atual (~10 docs, ~50-80 chunks)

Roadmap: substituição por ChromaDB (local) ou Oracle Autonomous AI
Database (vetorial gerenciado na OCI) em versões futuras.
"""

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import Embeddings

from src.config import RETRIEVER_K


def build_vector_store(
    documents: list[Document],
    embed_model: Embeddings,
) -> InMemoryVectorStore:
    """
    Constrói o vector store a partir da lista de documentos.

    Args:
        documents: Lista de Document gerada pelo ingest.py,
                   com page_content e metadata preservados.
        embed_model: Modelo de embeddings já instanciado.

    Returns:
        InMemoryVectorStore pronto para busca semântica.

    Log de auditoria: imprime o número de vetores armazenados,
    útil como evidência técnica no Challenge.
    """
    print(f"[vector_store] Vetorizando {len(documents)} chunks...")

    vector_store = InMemoryVectorStore.from_documents(
        documents=documents,
        embedding=embed_model,
    )

    print("[vector_store] Base vetorial construída com sucesso.")
    return vector_store


def get_retriever(vector_store: InMemoryVectorStore):
    """
    Retorna um retriever configurado a partir do vector store.

    O parâmetro k define quantos chunks serão recuperados por consulta.
    Um k=4 equilibra contexto suficiente com controle do tamanho do prompt.
    """
    return vector_store.as_retriever(
        search_kwargs={"k": RETRIEVER_K}
    )
