"""
Amazô.guia — Configurações centrais do projeto.

Define caminhos, paleta de cores, constantes do modelo e parâmetros
de recuperação utilizados por todos os módulos do pipeline RAG.
"""

import os
from pathlib import Path

# === Caminhos ===
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCES_PUBLIC_DIR = PROJECT_ROOT / "data" / "sources" / "public"
ASSETS_DIR = PROJECT_ROOT / "assets"
AVATAR_PATH = ASSETS_DIR / "amazo-guia-avatar-g10.png"

# === Paleta amazônica ===
COLORS = {
    "marrom_profundo": "#2C1B12",
    "verde_folha": "#2D4F1E",
    "verde_lima": "#A3C944",
    "rosa_terra": "#D48166",
    "vinho_escuro": "#3E2128",
}

# === Modelos (Groq) ===
# llama-3.1-70b-versatile → primário: alta qualidade, free tier Groq
# llama-3.1-8b-instant → fallback: rápido e leve
PRIMARY_LLM_MODEL = "llama-3.1-70b-versatile"
FALLBACK_LLM_MODEL = "llama-3.1-8b-instant"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# === Retriever ===
RETRIEVER_K = 4  # Número de chunks retornados por consulta

# === Camadas de ingestão ===
# Camada 1: atendimento público (prioridade na ingestão)
LAYER_1_DOCS = [
    "01-perfil-lidi-moura.md",
    "02-encontro-dagua-hub.md",
    "03-catalogo-produtos-servicos.md",
    "04-canais-e-roteamento.md",
    "05-amazo-guia.md",
]

# Camada 2: complementar
LAYER_2_DOCS = [
    "01b-trajetoria-ampliada-lidi-moura.md",
    "08-faq-publico.md",
    "09-formacao-ferramentas.md",
    "10-projetos-portfolio.md",
]
