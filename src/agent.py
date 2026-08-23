"""
Amazô.guia — Módulo do Agente LangGraph ReAct.

Responsabilidade: orquestrar o raciocínio e ação do agente utilizando
o padrão ReAct (Reasoning + Acting) via LangGraph.

Decisão técnica: LangGraph foi escolhido sobre chains lineares porque
permite que o agente decida dinamicamente quando usar a ferramenta
pega_contexto. O ciclo é:
  1. Recebe a mensagem do usuário (Raciocínio)
  2. Decide se precisa buscar na base vetorial (Decisão)
  3. Executa a busca via pega_contexto (Ação)
  4. Sintetiza a resposta final com os chunks recuperados (Geração)

Sistema de fallback: o LLM principal (Gemini 2.0 Flash) tem um fallback
para Gemini 1.5 Flash via .with_fallbacks(). Isso garante que o agente
continue operando mesmo durante instabilidades da API, sem expor erros
ao usuário final — prática essencial em sistemas produtivos.
"""

import os
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from src.config import PRIMARY_LLM_MODEL, FALLBACK_LLM_MODEL
from src.prompts import AMAZO_SYSTEM_PROMPT


def build_agent(retriever):
    """
    Constrói e retorna o agente ReAct da Amazô.guia.

    Args:
        retriever: Retriever já instanciado pelo vector_store.py.
                   Encapsulado como closure para a tool pega_contexto.

    Returns:
        Agente LangGraph compilado, pronto para receber mensagens.

    Nota pedagógica: a tool é definida dentro desta função para capturar
    o retriever via closure — padrão funcional que evita variáveis globais
    e torna o agente testável de forma isolada.
    """

    @tool
    def pega_contexto(query: str) -> str:
        """
        Busca informações oficiais na base documental da Amazô.guia.

        Use esta ferramenta sempre que precisar responder sobre Lídi Moura,
        o Encontro d'Água Hub, produtos, serviços, canais, preços ou FAQ.
        Retorna os trechos relevantes com metadados de fonte para citação.

        Args:
            query: A pergunta ou tema a ser buscado na base vetorial.

        Returns:
            String com o conteúdo dos chunks relevantes e suas fontes.
        """
        resultados = retriever.invoke(query)

        if not resultados:
            return "Nenhuma informação encontrada na base documental para essa consulta."

        # Formata o resultado incluindo metadados para citação rastreável
        partes = []
        for doc in resultados:
            fonte = doc.metadata.get("document_id", "documento")
            secao = doc.metadata.get("section", "")
            referencia = f"[Fonte: {fonte} / {secao}]" if secao else f"[Fonte: {fonte}]"
            partes.append(f"{referencia}\n{doc.page_content}")

        return "\n\n---\n\n".join(partes)

    # LLM principal com sistema de fallback
    # Decisão: fallback automático em vez de try/except manual —
    # o LangChain gerencia a troca de modelo de forma transparente
    primary_llm = ChatGoogleGenerativeAI(
        model=PRIMARY_LLM_MODEL,
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
    )
    fallback_llm = ChatGoogleGenerativeAI(
        model=FALLBACK_LLM_MODEL,
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
    )
    llm_with_fallback = primary_llm.with_fallbacks([fallback_llm])

    # Agente ReAct compilado pelo LangGraph
    agent = create_react_agent(
        model=llm_with_fallback,
        tools=[pega_contexto],
        prompt=AMAZO_SYSTEM_PROMPT,
    )

    print(f"[agent] Agente criado com {PRIMARY_LLM_MODEL} + fallback {FALLBACK_LLM_MODEL}")
    return agent


def run_agent(agent, user_message: str, history: list = None) -> str:
    """
    Executa o agente com uma mensagem do usuário.

    Args:
        agent: Agente LangGraph compilado pelo build_agent().
        user_message: Mensagem de entrada do usuário.
        history: Histórico de mensagens anteriores (opcional).
                 Formato: lista de dicts {"role": ..., "content": ...}

    Returns:
        Resposta final do agente como string.
    """
    messages = history or []
    messages.append({"role": "user", "content": user_message})

    resultado = agent.invoke({"messages": messages})

    # Extrai a última mensagem (resposta do agente)
    resposta = resultado["messages"][-1].content
    return resposta
