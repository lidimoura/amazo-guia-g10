"""
Amazô.guia — Interface Streamlit.

Decisão técnica: Streamlit foi escolhido pela agilidade de prototipação,
deploy nativo em cloud e suporte a histórico de chat via session_state.
A interface não compete com o backend — ela é uma janela limpa para
a inteligência do agente.

Identidade visual: inspirada no showcase amazo-g10-showcase, com
DNA de "caderno de campo amazônico" — verde profundo, tipografia
editorial e elementos que evocam floresta e tecnologia.

@st.cache_resource é usado para carregar o modelo de embeddings e o
vector store uma única vez por sessão de servidor — evita reprocessamento
a cada interação do usuário e reduz o tempo de resposta.
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Carrega .env local (ignorado em produção, onde st.secrets prevalece)
load_dotenv()

# === Configuração da página (deve ser o primeiro comando Streamlit) ===
st.set_page_config(
    page_title="Amazô.guia — Encontro d'Água Hub",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="expanded",
)

# === Estilo CSS customizado ===
# Extendemos o tema do config.toml com tipografia e microanimações
# que reforçam a identidade visual do showcase.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Manrope:wght@400;500;600;700&display=swap');

/* Tipografia principal — mesma do showcase */
html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}

h1, h2, h3 {
    font-family: 'DM Serif Display', serif;
}

/* Header da sidebar */
.sidebar-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: #A3C944;
    margin-bottom: 0.2rem;
}

.sidebar-subtitle {
    font-size: 0.8rem;
    color: #A3C944;
    opacity: 0.7;
    margin-bottom: 1.5rem;
}

/* Chat: avatar do usuário */
.stChatMessage[data-testid="stChatMessageUser"] {
    background-color: rgba(163, 201, 68, 0.08);
    border-radius: 12px;
}

/* Badge de fonte citada */
.fonte-badge {
    display: inline-block;
    background-color: rgba(163, 201, 68, 0.15);
    color: #A3C944;
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 4px;
    margin-top: 8px;
    font-family: 'Manrope', sans-serif;
}

/* Linha divisória sutil */
hr {
    border-color: rgba(163, 201, 68, 0.2);
}

/* Input de chat */
.stChatInputContainer {
    border-top: 1px solid rgba(163, 201, 68, 0.2);
}

/* Links: cor temática (verde-lima) em vez do azul padrão */
a, a:visited, a:hover, a:active,
.stMarkdown a, .stMarkdown a:visited {
    color: #A3C944 !important;
    text-decoration: none;
}
a:hover {
    opacity: 0.85;
    text-decoration: underline !important;
}

/* Descrição do projeto na sidebar */
.projeto-desc {
    font-size: 0.82rem;
    line-height: 1.5;
    color: #A3C944;
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)


# === Carregamento do pipeline RAG (cacheado) ===
# cache_version: incrementar para forçar rebuild após mudanças de configuração
CACHE_VERSION = "v3.2-groq-no-fallback"

@st.cache_resource(show_spinner="🌿 Iniciando a Amazô.guia...")
def carregar_pipeline(cache_version=CACHE_VERSION):
    """
    Carrega e cacheia o pipeline completo: ingestão → embeddings → vector store → agente.

    O decorator @st.cache_resource garante que esse processo pesado
    ocorra apenas uma vez por sessão de servidor, independente de
    quantas interações o usuário faça.

    Returns:
        Agente LangGraph compilado e pronto para receber mensagens.
    """
    from src.ingest import load_documents
    from src.embeddings import get_embedding_model
    from src.vector_store import build_vector_store, get_retriever
    from src.agent import build_agent

    # Garante que a API key está disponível
    # Streamlit Cloud: usa st.secrets; local: usa .env via load_dotenv()
    groq_api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
    if not groq_api_key:
        st.error("GROQ_API_KEY nao encontrada. Configure nos Secrets do Streamlit.")
        st.stop()

    groq_api_key = groq_api_key.strip()
    if len(groq_api_key) < 20:
        st.error(f"GROQ_API_KEY parece invalida ({len(groq_api_key)} chars). Verifique nos Secrets.")
        st.stop()

    os.environ["GROQ_API_KEY"] = groq_api_key

    docs = load_documents()
    embed_model = get_embedding_model()
    vector_store = build_vector_store(docs, embed_model)
    retriever = get_retriever(vector_store)
    agent = build_agent(retriever)

    return agent, len(docs)


# === Sidebar ===
with st.sidebar:
    st.markdown('<div class="sidebar-title">Amazô.guia</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Agente SDR-RAG · Encontro d\'Água Hub</div>', unsafe_allow_html=True)

    st.image("assets/amazo-guia-avatar-g10.png", use_container_width=True)

    st.markdown("---")
    st.markdown(
        '<div class="projeto-desc">'
        'Agente inteligente RAG que consulta fontes autorizadas do '
        'Encontro d\'Água Hub e responde em linguagem natural com '
        'rastreabilidade de fonte.<br><br>'
        '<strong>Challenge G10 — Alura Agente</strong><br>'
        'ONE · Oracle Next Education'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("**Projeto**")
    st.markdown("""
- [Repositório GitHub](https://github.com/lidimoura/amazo-guia-g10)
- [Showcase do Challenge](https://lidimoura.github.io/amazo-g10-showcase/)
""")

    st.markdown("---")

    # Botão de limpar chat — reseta o histórico sem recarregar o pipeline
    if st.button("Limpar conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<small style='opacity:0.5'>Challenge G10 · Hub OS · Lídi Moura</small>",
        unsafe_allow_html=True
    )


# === Carrega o pipeline ===
agent, n_chunks = carregar_pipeline()


# === Cabeçalho principal ===
st.markdown(
    "<h1 style='font-family: DM Serif Display, serif; color: #A3C944; margin-bottom: 0;'>Amazô.guia</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='color: #A3C944; opacity: 0.7; margin-top: 0;'>Guia digital do Encontro d'Água Hub</p>",
    unsafe_allow_html=True
)
st.markdown("---")


# === Histórico de mensagens ===
if "messages" not in st.session_state:
    st.session_state.messages = []

    # Mensagem de boas-vindas automática
    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "Olá! 🌿 Sou a **Amazô.guia**, representante digital do Encontro d'Água Hub.\n\n"
            "Posso te contar sobre a **Lídi Moura**, os **produtos e serviços** do Hub, "
            "responder suas dúvidas ou te conectar ao canal certo.\n\n"
            "Como posso te ajudar hoje?"
        ),
    })


# === Renderiza histórico ===
for msg in st.session_state.messages:
    avatar = "assets/amazo-guia-avatar-g10.png" if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# === Input do usuário ===
if prompt := st.chat_input("Fale com a Amazô.guia..."):
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera resposta do agente
    with st.chat_message("assistant", avatar="assets/amazo-guia-avatar-g10.png"):
        with st.spinner("🌿"):
            # Converte histórico para formato LangGraph
            history = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[:-1]  # exclui a última (atual)
            ]

            try:
                resultado = agent.invoke({
                    "messages": history + [{"role": "user", "content": prompt}]
                })
                resposta = resultado["messages"][-1].content
            except Exception as e:
                tipo = type(e).__name__
                msg_curta = str(e)[:300]
                # Log tecnico nos logs do servidor (visivel em Manage App -> Logs)
                print(f"[agent-error] {tipo}: {msg_curta}")
                resposta = (
                    "Desculpe, tive um problema t\u00e9cnico ao processar sua pergunta. "
                    "Por favor, tente novamente em alguns instantes."
                )

        st.markdown(resposta)

    # Salva resposta no histórico
    st.session_state.messages.append({"role": "assistant", "content": resposta})
