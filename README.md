# Amazô.guia — Encontro d’água Hub

![Status](https://img.shields.io/badge/Status-Em%20construção-yellow)
![Projeto](https://img.shields.io/badge/Projeto-Amazô.guia-blue)
![LLM](https://img.shields.io/badge/LLM-Gemini-green)
![RAG](https://img.shields.io/badge/Arquitetura-RAG-purple)

> **Tecnologia acessível e sustentável.**

## Visão

A **Amazô.guia** é a evolução da Amazô, agente/chatbot SDR e de recepção, para uma **agente SDR-RAG, representante e guia digital** do Encontro d’água Hub — holding AI-Native fundada por **Lídi Moura**, analista de dados, IA e automações e criadora de soluções tecnológicas com foco em sustentabilidade e impacto social.

No Challenge G10, a agente deverá consultar fontes autorizadas, responder com rastreabilidade, qualificar inicialmente leads e direcionar usuários, clientes B2B, recrutadores e visitantes para o canal público adequado.

## Origem

Este projeto evolui o showcase Typebot da Amazô, mantido separadamente:

- [Repositório do showcase](https://github.com/lidimoura/amazo.ia-showcase)
- [LP pública](https://lidimoura.github.io/amazo.ia-showcase/)
- [Portfólio da Lídi com Link d’Água](https://link.encontrodagua.com/r/portifolio-lidimoura)

O showcase representa a origem visual e conversacional; este repositório representa a evolução técnica para RAG.

## Showcase do Challenge

A [LP pública do Showcase Amazô G10](https://lidimoura.github.io/amazo-g10-showcase/) apresenta a narrativa visual, a arquitetura proposta, o método de trabalho e as evidências em curadoria. Ela **não substitui** o código, as fontes autorizadas, os testes ou a documentação técnica deste repositório.

## Identidade visual

A identidade combina referências amazônicas, tecnologia acessível e sustentabilidade. A ilustração da Amazô é o avatar principal; a fotografia da samambaia, feita por Lídi Moura no Amazonas, representa território e autoria.

<p align="center">
  <img src="./assets/amazo-guia-avatar-g10.png" alt="Ilustração da Amazô.guia — Challenge G10" width="220">
</p>

| Cor | Hex | Uso |
|---|---|---|
| Marrom profundo | `#2C1B12` | Background principal |
| Verde folha | `#2D4F1E` | Sidebar e containers |
| Verde-lima | `#A3C944` | Fontes e destaques |
| Rosa-terra | `#D48166` | Botões de ação |
| Vinho escuro | `#3E2128` | Profundidade e contraste |

> Fotografia autoral: [samambaia-amazonas.webp](./assets/samambaia-amazonas.webp), registrada por Lídi Moura no Amazonas.


## Arquitetura

```
Usuário → Streamlit Chat → LangGraph ReAct Agent
                                ↓
                    [pega_contexto() tool]
                                ↓
                    InMemoryVectorStore
                                ↓
                    all-MiniLM-L6-v2 embeddings
                                ↓
                    data/sources/public/*.md (10 docs v2.1)

LLM: Gemini 2.0 Flash → fallback Gemini 1.5 Flash
```

## Stack

| Camada | Tecnologia | Justificativa |
|---|---|---|
| LLM | Gemini 2.0 Flash + fallback 1.5 Flash | Performance + custo zero + ecossistema Google |
| Embeddings | `all-MiniLM-L6-v2` (HuggingFace) | Leve (~80 MB), roda em CPU, free tier compatível |
| Vector Store | `InMemoryVectorStore` (LangChain) | Simplicidade para MVP read-only |
| Orquestração | LangGraph ReAct | Raciocínio + ação dinâmica com tool |
| Interface | Streamlit | Prototipação rápida e deploy em cloud |
| Deploy | Streamlit Cloud | URL pública funcional dentro do prazo |

## Fontes de verdade

10 documentos `.md` em `data/sources/public/`, organizados em duas camadas:

**Camada 1 — Atendimento público:**
`01-perfil`, `02-hub`, `03-catalogo`, `04-canais`, `05-amazo-guia`

**Camada 2 — Complementar:**
`01b-trajetoria`, `08-faq`, `09-formacao`, `10-portfolio`

> Documentos internos (06, 07) vão para OCI Object Storage via PAR — mapeado para próximo incremento.

## Como executar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/lidimoura/amazo-guia-g10
cd amazo-guia-g10

# 2. Crie o ambiente virtual e instale dependências
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. Configure a API key
cp .env.example .env
# Edite .env e adicione sua GOOGLE_API_KEY

# 4. Execute o app
streamlit run app.py
```

## Deploy — Streamlit Cloud

1. Faça push do repositório para o GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io) e conecte o repo
3. Em **Settings → Secrets**, adicione:
   ```toml
   GOOGLE_API_KEY = "sua-chave-aqui"
   ```
4. Aguarde o deploy — a URL pública estará disponível em poucos minutos

## Sandbox (Google Colab)

O arquivo [`notebooks/amazo_sandbox.py`](./notebooks/amazo_sandbox.py) contém o pipeline completo em células sequenciais para experimentação e aprendizagem no Colab. Cada célula inclui justificativas técnicas da tomada de decisão.

## Autoria e transparência

O projeto é de autoria e propriedade de **Lídi Moura**, que mantém autonomia sobre produto, escopo, decisões técnicas, configurações, fontes, testes e responsabilidade final.

O **Hub OS** é utilizado como infraestrutura metodológica e operacional da holding para aumentar agilidade, organização e qualidade. Seu uso, já validado em projetos pessoais e freelas do Hub, não substitui a autoria nem delega decisões à ferramenta.

## Segurança

Segredos gerenciados via `.env` (local, gitignored) e `st.secrets` (Streamlit Cloud). O system prompt inclui blindagem anti-jailbreak e recusa educada para perguntas fora do escopo do Hub.

## Ecossistema público

- [Encontro d'água Hub](https://hub.encontrodagua.com)
- [Link d'Água](https://link.encontrodagua.com/vitrine)
- [GitHub da Lídi Moura](https://github.com/lidimoura)
- [Showcase do Challenge G10](https://lidimoura.github.io/amazo-g10-showcase/)

---

**Lídi Moura — analista de dados, IA e automações | Fundadora do Encontro d'água Hub**
