"""
Amazô.guia — Módulo do Agente RAG (chain simples e resiliente).

Decisão técnica: arquitetura RAG direta com tripla camada de resiliência:
  1. Modelo Primário: Groq openai/gpt-oss-120b (alta precisão e raciocínio)
  2. Fallback Secundário: Groq openai/gpt-oss-20b (velocidade)
  3. Fallback Terciário: OpenAI gpt-4o-mini (quando OPENAI_API_KEY estiver configurada)

Fluxo:
  1. Busca semântica na base vetorial (retriever)
  2. Formata contexto com metadados de fonte
  3. Chamada direta ao LLM com system prompt + contexto + pergunta
  4. Retorna resposta como string
"""

import os
import logging
from langchain_core.messages import SystemMessage, HumanMessage

from src.config import PRIMARY_LLM_MODEL, FALLBACK_LLM_MODEL
from src.prompts import AMAZO_SYSTEM_PROMPT


def build_agent(retriever):
    """
    Constrói e retorna o agente RAG da Amazô.guia.

    Args:
        retriever: Retriever já instanciado pelo vector_store.py.

    Returns:
        Dict com llm, retriever e system_prompt prontos para uso.
    """
    groq_api_key = os.environ.get("GROQ_API_KEY")
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    if groq_api_key:
        from langchain_groq import ChatGroq
        logging.info(f"[agent] GROQ_API_KEY encontrada: {len(groq_api_key)} chars")
        llm = ChatGroq(
            model=PRIMARY_LLM_MODEL,
            groq_api_key=groq_api_key,
            temperature=0.3,
        )
        provider = "groq"
    elif openai_api_key:
        from langchain_openai import ChatOpenAI
        logging.info(f"[agent] OPENAI_API_KEY encontrada: {len(openai_api_key)} chars")
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=openai_api_key,
            temperature=0.3,
        )
        provider = "openai"
    else:
        raise ValueError(
            "Nenhuma chave de API encontrada. Configure GROQ_API_KEY ou OPENAI_API_KEY "
            "nos Secrets do Streamlit ou no .env local."
        )

    logging.info(f"[agent] LLM inicializado ({provider}): {PRIMARY_LLM_MODEL if provider == 'groq' else 'gpt-4o-mini'}")

    return {"llm": llm, "retriever": retriever, "provider": provider}


def run_agent(agent, user_message: str, history: list = None) -> str:
    """
    Executa o pipeline RAG para uma mensagem do usuário com fallback automático multi-provedor.

    Args:
        agent: Dict com llm, retriever e provider (retornado por build_agent).
        user_message: Mensagem de entrada do usuário.
        history: Histórico de mensagens (opcional).

    Returns:
        Resposta do LLM como string.
    """
    llm = agent["llm"]
    retriever = agent["retriever"]

    # 1. Busca semântica
    resultados = retriever.invoke(user_message)

    # 2. Formata contexto com fontes
    if resultados:
        partes = []
        for doc in resultados:
            fonte = doc.metadata.get("document_id", "documento")
            secao = doc.metadata.get("section", "")
            ref = f"[Fonte: {fonte} / {secao}]" if secao else f"[Fonte: {fonte}]"
            partes.append(f"{ref}\n{doc.page_content}")
        contexto = "\n\n---\n\n".join(partes)
    else:
        contexto = "Nenhuma informacao encontrada na base documental."

    # 3. Prompt com contexto injetado
    system_com_contexto = (
        AMAZO_SYSTEM_PROMPT
        + "\n\n## Contexto da base documental (use para embasar sua resposta):\n\n"
        + contexto
    )

    messages = [
        SystemMessage(content=system_com_contexto),
        HumanMessage(content=user_message),
    ]

    # 4. Chamada ao LLM com triplo fallback de resiliência
    try:
        resposta = llm.invoke(messages)
        return resposta.content
    except Exception as exc1:
        logging.warning(f"[agent] Falha no modelo primário ({exc1}). Tentando fallback Groq ({FALLBACK_LLM_MODEL})...")
        
        # Tenta fallback secundário (Groq 20b)
        groq_api_key = os.environ.get("GROQ_API_KEY")
        if groq_api_key:
            try:
                from langchain_groq import ChatGroq
                fallback_llm = ChatGroq(
                    model=FALLBACK_LLM_MODEL,
                    groq_api_key=groq_api_key,
                    temperature=0.3,
                )
                return fallback_llm.invoke(messages).content
            except Exception as exc2:
                logging.warning(f"[agent] Falha no fallback Groq ({exc2})...")

        # Tenta fallback terciário (OpenAI gpt-4o-mini)
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if openai_api_key:
            try:
                logging.warning("[agent] Tentando fallback OpenAI (gpt-4o-mini)...")
                from langchain_openai import ChatOpenAI
                openai_llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    api_key=openai_api_key,
                    temperature=0.3,
                )
                return openai_llm.invoke(messages).content
            except Exception as exc3:
                logging.error(f"[agent] Falha no fallback OpenAI ({exc3}).")
                raise exc3

        raise exc1
