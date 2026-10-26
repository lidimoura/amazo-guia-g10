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
from src.config import AVATAR_PATH

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

/* Botão oficial de Agendamento de Consultoria (#8E24AA) */
.btn-calendar-schedule {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 100%;
    padding: 11px 18px;
    background-color: #8E24AA !important;
    color: #FFFFFF !important;
    font-family: 'Manrope', sans-serif;
    font-weight: 700;
    font-size: 0.88rem;
    border-radius: 12px;
    text-decoration: none !important;
    box-shadow: 0 8px 22px rgba(142, 36, 170, 0.38);
    transition: transform 0.2s ease, opacity 0.2s ease;
    margin-bottom: 8px;
}
.btn-calendar-schedule:hover {
    opacity: 0.92 !important;
    transform: translateY(-1px);
    color: #FFFFFF !important;
    text-decoration: none !important;
}

.btn-wa-hub {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 100%;
    padding: 10px 16px;
    background-color: rgba(163, 201, 68, 0.16) !important;
    border: 1px solid rgba(163, 201, 68, 0.45);
    color: #A3C944 !important;
    font-family: 'Manrope', sans-serif;
    font-weight: 700;
    font-size: 0.83rem;
    border-radius: 12px;
    text-decoration: none !important;
    transition: background-color 0.2s ease;
}
.btn-wa-hub:hover {
    background-color: rgba(163, 201, 68, 0.26) !important;
    text-decoration: none !important;
}
</style>
""", unsafe_allow_html=True)
import logging
import streamlit.components.v1 as components

CALENDAR_EMBED_URL = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ39jIFaE98TdoKnOmL7sOYtM0lQHu7F-hcQm5JU8nYfeCbtzoUAJ7lQXXO9hHxYW-9hvOMejMAm?gv=true"
CALENDAR_SHORT_URL = "https://calendar.app.google/qztptMcM3QYkeo539"
WA_HUB_URL = "https://wa.me/5541992557600?text=Ol%C3%A1%20L%C3%ADdi%21%20%5BOrigem%3A%20Amaz%C3%B4.guia%20G10%20Streamlit%5D%20Conversei%20com%20a%20Amaz%C3%B4.guia%20e%20quero%20falar%20sobre%20as%20solu%C3%A7%C3%B5es%20do%20Encontro%20d%27%C3%81gua%20Hub."


@st.dialog("📅 Agende sua consultoria — Encontro d'Água Hub", width="large")
def abrir_modal_agendamento():
    st.markdown(
        "<p style='font-size:0.88rem; margin-bottom:10px;'>"
        "Escolha o melhor dia e horário para sua <strong>Consultoria Inicial / Diagnóstico (R$ 180 · 60 min no Google Meet)</strong> com <strong>Lídi Moura</strong>:"
        "</p>",
        unsafe_allow_html=True,
    )
    components.html(
        f"""
        <div style="background-color: #ffffff; color-scheme: light; border-radius: 16px; overflow: hidden; border: 2px solid #8E24AA; box-shadow: 0 12px 32px rgba(0,0,0,0.35);">
            <iframe
                src="{CALENDAR_EMBED_URL}"
                style="border: 0; width: 100%; height: 620px; background-color: #ffffff; color-scheme: light;"
                frameborder="0"
                scrolling="yes"
            ></iframe>
        </div>
        """,
        height=640,
        scrolling=False,
    )
    st.markdown(
        f"<div style='text-align:center; margin-top:6px;'>"
        f"<a href='{CALENDAR_SHORT_URL}' target='_blank' style='font-size:0.8rem;'>"
        f"↗ Preferir abrir em nova guia do Google Calendar</a></div>",
        unsafe_allow_html=True,
    )

# === Carregamento do pipeline RAG (cacheado por sessao via session_state) ===
def carregar_pipeline():
    """
    Carrega o pipeline completo: ingestao -> embeddings -> vector store -> agente.
    Cacheado em st.session_state para evitar reconstrucao a cada interacao.

    Returns:
        Tupla (agent_dict, n_docs) -- agent_dict com llm e retriever.
    """
    logging.warning("[pipeline] === INICIANDO CARGA DO PIPELINE ===")
    from src.ingest import load_documents
    from src.embeddings import get_embedding_model
    from src.vector_store import build_vector_store, get_retriever
    from src.agent import build_agent

    # Garante que as API keys estao disponiveis
    # Streamlit Cloud: usa st.secrets; local: usa .env via load_dotenv()
    try:
        groq_api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
    except Exception:
        groq_api_key = os.getenv("GROQ_API_KEY")

    try:
        openai_api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
    except Exception:
        openai_api_key = os.getenv("OPENAI_API_KEY")

    if not groq_api_key and not openai_api_key:
        st.error("Nenhuma chave de API encontrada. Configure GROQ_API_KEY ou OPENAI_API_KEY nos Secrets do Streamlit.")
        st.stop()

    if groq_api_key:
        groq_api_key = groq_api_key.strip()
        os.environ["GROQ_API_KEY"] = groq_api_key
        logging.warning(f"[pipeline] GROQ_API_KEY: {len(groq_api_key)} chars, prefixo={groq_api_key[:6]}")

    if openai_api_key:
        openai_api_key = openai_api_key.strip()
        os.environ["OPENAI_API_KEY"] = openai_api_key
        logging.warning(f"[pipeline] OPENAI_API_KEY ativa para fallback ({len(openai_api_key)} chars)")

    docs = load_documents()
    logging.warning(f"[pipeline] Docs carregados: {len(docs)}")
    embed_model = get_embedding_model()
    vector_store = build_vector_store(docs, embed_model)
    retriever = get_retriever(vector_store)
    agent = build_agent(retriever)
    logging.warning("[pipeline] Pipeline carregado com sucesso!")
    return agent, len(docs)


# === Sidebar ===
with st.sidebar:
    if AVATAR_PATH.exists():
        st.image(str(AVATAR_PATH), width=130)
        with st.popover("🔍 Ampliar ilustração"):
            st.image(
                str(AVATAR_PATH),
                caption="Amazô.guia — Ilustração Oficial (Challenge G10)",
                use_container_width=True,
            )
    st.markdown('<div class="sidebar-title">Amazô.guia</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Agente SDR-RAG · Encontro d\'Água Hub</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        '<div class="projeto-desc">'
        'Agente inteligente RAG que consulta fontes autorizadas do '
        'Encontro d\'Água Hub e responde em linguagem natural com '
        'rastreabilidade de fonte.<br><br>'
        '<strong><a href="https://alura-es-cursos.github.io/tech-builder-brasil/" target="_blank" style="color: #A3C944; text-decoration: none;">Challenge G10 — Tech Builder Brasil</a></strong><br>'
        '<a href="https://www.alura.com.br/" target="_blank" style="color: #A3C944; text-decoration: none;">Alura</a> · '
        '<a href="https://www.oracle.com/br/education/oracle-next-education/" target="_blank" style="color: #A3C944; text-decoration: none;">ONE (Oracle Next Education)</a>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("**Atendimento & Consultoria**")
    if st.button("📅 Agende sua consultoria", use_container_width=True, type="primary"):
        abrir_modal_agendamento()
    st.markdown(
        f'<a href="{WA_HUB_URL}" target="_blank" class="btn-wa-hub">'
        '💬 WhatsApp Business do Hub</a>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("**Links Oficiais**")
    st.markdown("""
- [Encontro d'Água Hub Digital](https://hub.encontrodagua.com/)
- [Link d'Água (Cartões & QR Dinâmico)](https://link.encontrodagua.com/)
- [Portfólio Lídi Moura](https://link.encontrodagua.com/r/portifolio-lidimoura)
- [Challenge G10 (Alura / Oracle)](https://alura-es-cursos.github.io/tech-builder-brasil/)
- [Repositório GitHub](https://github.com/lidimoura/amazo-guia-g10)
- [Showcase do Challenge](https://lidimoura.github.io/amazo-g10-showcase/)
""")

    st.markdown("---")

    # Botão de limpar chat — reseta o histórico sem recarregar o pipeline
    if st.button("Limpar conversa"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<small style='opacity:0.5'>Challenge G10 · Hub OS · Lídi Moura</small>",
        unsafe_allow_html=True
    )


# === Carrega o pipeline (uma vez por sessao) ===
if "agent" not in st.session_state:
    with st.spinner("🌿 Iniciando a Amazô.guia..."):
        st.session_state.agent, st.session_state.n_chunks = carregar_pipeline()

agent = st.session_state.agent
n_chunks = st.session_state.n_chunks


# === Cabeçalho principal ===
col_title, col_cta = st.columns([2.2, 1.3], vertical_alignment="center")
with col_title:
    st.markdown(
        "<h1 style='font-family: DM Serif Display, serif; color: #A3C944; margin-bottom: 0;'>Amazô.guia</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='color: #A3C944; opacity: 0.7; margin-top: 0; margin-bottom: 0;'>Guia digital SDR-RAG do Encontro d'Água Hub</p>",
        unsafe_allow_html=True
    )
with col_cta:
    if st.button("📅 Agende sua consultoria", key="header_cal_btn", use_container_width=True):
        abrir_modal_agendamento()
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
    avatar = "🌿" if msg["role"] == "assistant" else "💬"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# === Input do usuário ===
if prompt := st.chat_input("Fale com a Amazô.guia..."):
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="💬"):
        st.markdown(prompt)

    # Gera resposta do agente
    with st.chat_message("assistant", avatar="🌿"):
        with st.spinner("🌿"):
            # Converte histórico para formato LangGraph
            history = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[:-1]  # exclui a última (atual)
            ]

            try:
                from src.agent import run_agent
                resposta = run_agent(agent, prompt)
            except Exception as e:
                tipo = type(e).__name__
                msg_curta = str(e)[:300]
                logging.error(f"[agent-error] {tipo}: {msg_curta}")
                print(f"[agent-error] {tipo}: {msg_curta}")
                resposta = (
                    "Desculpe, tive um problema t\u00e9cnico ao processar sua pergunta. "
                    "Por favor, tente novamente em alguns instantes."
                )

        st.markdown(resposta)

    # Salva resposta no histórico
    st.session_state.messages.append({"role": "assistant", "content": resposta})
