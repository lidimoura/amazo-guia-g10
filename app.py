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
</style>
""", unsafe_allow_html=True)


# === Carregamento do pipeline RAG (cacheado) ===
@st.cache_resource(show_spinner="🌿 Iniciando a Amazô.guia...")
def carregar_pipeline():
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
    google_api_key = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
    if not google_api_key:
        st.error("⚠️ GOOGLE_API_KEY não encontrada. Configure nos Secrets do Streamlit ou no .env local.")
        st.stop()

    # Validação básica do formato da key (keys Google AI Studio começam com "AIza")
    google_api_key = google_api_key.strip()
    if not google_api_key.startswith("AIza") or len(google_api_key) < 30:
        st.error(
            f"⚠️ GOOGLE_API_KEY parece inválida (comprimento: {len(google_api_key)} chars). "
            "Verifique se está completa e sem espaços extras nos Secrets."
        )
        st.stop()

    os.environ["GOOGLE_API_KEY"] = google_api_key

    docs = load_documents()
    embed_model = get_embedding_model()
    vector_store = build_vector_store(docs, embed_model)
    retriever = get_retriever(vector_store)
    agent = build_agent(retriever)

    return agent, len(docs)


# === Sidebar ===
with st.sidebar:
    st.markdown('<div class="sidebar-title">🌿 Amazô.guia</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Agente SDR-RAG · Encontro d\'Água Hub</div>', unsafe_allow_html=True)

    st.image("assets/amazo-guia-avatar-g10.png", use_container_width=True)

    st.markdown("---")
    st.markdown("**🔗 Links do Hub**")
    st.markdown("""
- [🌐 Hub](https://hub.encontrodagua.com/)
- [🔗 Link d'Água](https://link.encontrodagua.com/)
- [💼 Portfólio Lídi](https://link.encontrodagua.com/r/portifolio-lidimoura)
- [💬 WhatsApp](https://wa.me/5541992557600?text=Ol%C3%A1%2C+vim+pela+Amaz%C3%B4.guia)
""")

    st.markdown("---")

    # Botão de limpar chat — reseta o histórico sem recarregar o pipeline
    if st.button("🗑️ Limpar conversa", use_container_width=True):
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

            resultado = agent.invoke({
                "messages": history + [{"role": "user", "content": prompt}]
            })
            resposta = resultado["messages"][-1].content

        st.markdown(resposta)

    # Salva resposta no histórico
    st.session_state.messages.append({"role": "assistant", "content": resposta})
