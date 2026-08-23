"""
Amazô.guia — Módulo do Agente RAG (chain simples).

Decisão técnica: substituída a arquitetura LangGraph ReAct por uma
chain RAG direta para maximizar confiabilidade no deploy.

Fluxo:
  1. Busca semântica na base vetorial (retriever)
  2. Formata contexto com metadados de fonte
  3. Chamada direta ao LLM com system prompt + contexto + pergunta
  4. Retorna resposta como string

Vantagem sobre ReAct: sem tool calling, sem bind_tools, sem grafo
de estado — menos pontos de falha e compatibilidade garantida com
qualquer modelo de chat (Groq, OpenAI, HuggingFace, etc.).
"""

import os
from langchain_groq import ChatGroq
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
        Chamado via run_agent() para manter a interface compatível com app.py.
    """
    groq_api_key = os.environ.get("GROQ_API_KEY")

    if groq_api_key:
        print(f"[agent] GROQ_API_KEY encontrada: {len(groq_api_key)} chars")
    else:
        raise ValueError("GROQ_API_KEY nao encontrada. Configure nos Secrets do Streamlit ou no .env local.")

    llm = ChatGroq(
        model=PRIMARY_LLM_MODEL,
        groq_api_key=groq_api_key,
        temperature=0.3,
    )

    print(f"[agent] LLM pronto: {PRIMARY_LLM_MODEL}")

    # Retorna um objeto simples que run_agent() sabe usar
    return {"llm": llm, "retriever": retriever}


def run_agent(agent, user_message: str, history: list = None) -> str:
    """
    Executa o pipeline RAG para uma mensagem do usuário.

    Args:
        agent: Dict com llm e retriever (retornado por build_agent).
        user_message: Mensagem de entrada do usuário.
        history: Histórico de mensagens (não utilizado nesta versão simples).

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

    # 4. Chamada ao LLM com fallback automático
    messages = [
        SystemMessage(content=system_com_contexto),
        HumanMessage(content=user_message),
    ]
    try:
        resposta = llm.invoke(messages)
        return resposta.content
    except Exception as exc:
        print(f"[agent] Erro com {PRIMARY_LLM_MODEL}: {exc}. Tentando fallback {FALLBACK_LLM_MODEL}...")
        groq_api_key = os.environ.get("GROQ_API_KEY")
        fallback_llm = ChatGroq(
            model=FALLBACK_LLM_MODEL,
            groq_api_key=groq_api_key,
            temperature=0.3,
        )
        resposta = fallback_llm.invoke(messages)
        return resposta.content

