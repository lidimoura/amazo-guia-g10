"""
Amazô.guia — Módulo de ingestão de documentos Markdown.

Responsabilidade: carregar os arquivos .md de data/sources/public/,
extrair o YAML frontmatter como metadados e dividir o conteúdo em
chunks por seção (## heading), preservando rastreabilidade por fonte.

Decisão técnica: usar Markdown em vez de PDF para máxima leveza e
controle sobre metadados. O frontmatter YAML de cada documento define
visibilidade, audiência e versão — informações críticas para que o
agente cite corretamente suas fontes.
"""

import re
from pathlib import Path
from typing import Optional

import yaml
from langchain_core.documents import Document

from src.config import SOURCES_PUBLIC_DIR, LAYER_1_DOCS, LAYER_2_DOCS


def _parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    Extrai o YAML frontmatter de um documento Markdown.

    Retorna uma tupla (metadata_dict, body_text).
    Se não houver frontmatter, retorna ({}, conteúdo completo).
    """
    pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
    match = pattern.match(content)

    if match:
        try:
            metadata = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            metadata = {}
        body = content[match.end():]
        return metadata, body

    return {}, content


def _split_by_sections(body: str, base_metadata: dict) -> list[dict]:
    """
    Divide o corpo do documento em chunks por seção (## heading).

    Cada chunk herda os metadados do documento e adiciona o título
    da seção, permitindo citações precisas como:
    'Segundo o documento X, seção Y...'
    """
    chunks = []
    # Divide por headings de nível 2 (##)
    sections = re.split(r"\n(##[^#].*?)\n", body)

    # Primeira parte: conteúdo antes do primeiro ## (intro/título)
    intro = sections[0].strip()
    if intro:
        chunks.append({
            "content": intro,
            "section": "introdução",
        })

    # Seções subsequentes: [heading, conteúdo, heading, conteúdo, ...]
    for i in range(1, len(sections) - 1, 2):
        heading = sections[i].strip().lstrip("#").strip()
        content = sections[i + 1].strip() if i + 1 < len(sections) else ""
        if content:
            chunks.append({
                "content": f"{sections[i]}\n{content}",
                "section": heading,
            })

    return chunks


def load_documents(
    include_layer_2: bool = True,
    sources_dir: Optional[Path] = None,
) -> list[Document]:
    """
    Carrega e processa todos os documentos das camadas de ingestão.

    Args:
        include_layer_2: Se True, inclui os documentos da Camada 2
                         (complementar) além da Camada 1 (atendimento público).
        sources_dir: Diretório de fontes. Usa o padrão de config se None.

    Returns:
        Lista de objetos Document com page_content e metadata preservados.

    Decisão pedagógica: processamos por camada para facilitar validação
    incremental — a Camada 1 deve funcionar sozinha antes de adicionar
    a Camada 2.
    """
    base_dir = sources_dir or SOURCES_PUBLIC_DIR
    doc_files = LAYER_1_DOCS + (LAYER_2_DOCS if include_layer_2 else [])

    documents = []
    loaded_count = 0
    skipped = []

    for filename in doc_files:
        filepath = base_dir / filename

        if not filepath.exists():
            skipped.append(filename)
            continue

        raw_text = filepath.read_text(encoding="utf-8")
        frontmatter, body = _parse_frontmatter(raw_text)
        chunks = _split_by_sections(body, frontmatter)

        for chunk in chunks:
            metadata = {
                # Metadados do frontmatter YAML
                "document_id": frontmatter.get("document_id", filename),
                "source": filename,
                "version": str(frontmatter.get("version", "")),
                "status": frontmatter.get("status", ""),
                "owner": frontmatter.get("owner", "Lídi Moura"),
                "audience": frontmatter.get("audience", ""),
                "visibility": frontmatter.get("visibility", "publico"),
                # Metadados de navegação
                "section": chunk["section"],
            }
            documents.append(
                Document(page_content=chunk["content"], metadata=metadata)
            )
            loaded_count += 1

    # Log de auditoria: fundamental para o Challenge (evidência de ingestão)
    print(f"[ingest] Documentos processados: {len(doc_files) - len(skipped)}")
    print(f"[ingest] Chunks gerados: {loaded_count}")
    if skipped:
        print(f"[ingest] Arquivos ausentes (ignorados): {skipped}")

    return documents
