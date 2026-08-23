"""
Amazô.guia — Módulo de embeddings.

Responsabilidade: inicializar o modelo de embeddings que transforma
texto em vetores numéricos para busca semântica.

Decisão técnica: utilizamos o `sentence-transformers/all-MiniLM-L6-v2`
como modelo padrão para o MVP. Justificativa:
- Leve (~80 MB), compatível com o free tier do Streamlit Cloud (1 GB RAM)
- Excelente performance para português e inglês em tarefas de recuperação
- Roda localmente sem necessidade de chave de API adicional

O código está preparado para swap para `mxbai-embed-large-v1` via
variável de configuração, caso seja necessário maior precisão semântica
em versões futuras com infraestrutura mais robusta.
"""

import os
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import EMBEDDING_MODEL


def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Inicializa e retorna o modelo de embeddings.

    O modelo é baixado automaticamente do HuggingFace Hub na primeira
    execução e fica em cache local. Execuções subsequentes usam o cache.

    Returns:
        Instância de HuggingFaceEmbeddings pronta para uso.
    """
    model_name = os.getenv("EMBEDDING_MODEL", EMBEDDING_MODEL)

    print(f"[embeddings] Carregando modelo: {model_name}")

    # Nota: model_kwargs={"device": "cpu"} removido — causa NotImplementedError
    # no PyTorch 2.13 com meta tensors. sentence-transformers 3.4.x gerencia
    # o device automaticamente, sem necessidade de especificar explicitamente.
    embed_model = HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs={"normalize_embeddings": True},
    )

    print("[embeddings] Modelo carregado com sucesso.")
    return embed_model
