# DEVLOG — Amazô.guia

## Registro 001 — Fundação documental

**Data:** 20 de agosto de 2026  
**Status:** Commit inicial realizado; revisão de concisão pendente.

### Decisão

Criar a Amazô.guia como evolução da Amazô Typebot: uma agente SDR-RAG, representante e guia digital do Encontro d’água Hub.

O projeto é de autoria e propriedade de **Lídi Moura**, analista de dados, IA e automações e fundadora do Hub. Ela mantém autonomia sobre escopo, produto, decisões técnicas, configurações, curadoria, testes e responsabilidade final.

O Hub OS NEXUS é utilizado como infraestrutura metodológica e operacional já validada em projetos pessoais e freelas do Hub, para aumentar agilidade e qualidade. Seu uso não substitui a autoria de Lídi nem delega decisões à ferramenta.

### Identidade visual

Foram aprovados dois ativos para o repositório: `assets/amazo-guia-avatar.jpeg`, nova ilustração da Amazô, e `assets/samambaia-amazonas.webp`, fotografia autoral de Lídi Moura no Amazonas. A paleta visual é `#391E13`, `#648D3C`, `#D7F993`, `#D9AAA1` e `#3E2128`, aplicada como referência para futuras interfaces e materiais do produto.

### Escopo aprovado

| Item | Decisão |
|---|---|
| LLM | Google Gemini por variável de ambiente |
| RAG | Primeiro com fontes aprovadas e execução local |
| Fontes | Documentos do Perplexity, ainda pendentes de envio e revisão |
| Armazenamento | OCI Object Storage privado como opção futura |
| Banco vetorial | Avaliação posterior do Autonomous AI Database |
| Canais | WhatsApp, portfólio, LP, Link d’Água, CRM ou outro link público aprovado |
| Integrações | Handoff automático somente no roadmap |
| n8n | Fora do MVP |
| Showcase | Repositório Typebot separado, citado como origem |

### Governança

Nenhum documento comercial, valor, dado de lead, credencial ou fonte privada será inventado ou indexado antes da aprovação de Lídi. O MVP não acessará Supabase, CRM ou dados produtivos diretamente. A agente poderá apresentar um canal público, mas não afirmará que registrou um lead sem integração validada.

### Método

A construção seguirá incrementos funcionais e pedagógicos, sem arquivos vazios: fontes, ingestão, RAG local, testes, interface, documentação e infraestrutura. Cada alteração será acompanhada por escopo, diff, validação e aprovação.

### Estado

O primeiro commit contém somente `README.md` e `DEVLOG.md`. Este incremento adiciona apenas os dois ativos visuais aprovados e atualiza os documentos para a versão concisa. Nenhum código de RAG, interface, notebook ou integração será criado nesta etapa.

---

## Registro 002 — Planejamento de execução e decisões técnicas

**Data:** 23 de agosto de 2026  
**Status:** Planejamento concluído; execução iniciada.

### Decisões técnicas

A fundação documental está completa. Dez fontes de verdade em Markdown (v2.1) foram curadas, versionadas e organizadas em `data/sources/public/`. O foco agora é materializar o código do MVP.

#### Stack definida

| Camada | Tecnologia | Justificativa |
|---|---|---|
| LLM | Gemini 2.0 Flash + fallback Gemini 1.5 Flash | Performance, custo zero e alinhamento com ecossistema Google do Challenge |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` | Leve, compatível com Streamlit Cloud free (1 GB RAM); swap para `mxbai-embed-large-v1` avaliado para versão futura |
| Vector Store | `InMemoryVectorStore` (LangChain) | Simplicidade e velocidade para MVP read-only |
| Orquestração | LangGraph com padrão ReAct | Capacidade de raciocínio + ação; agente decide quando consultar a base vetorial |
| Interface | Streamlit | Rapidez de prototipação, deploy nativo em cloud, histórico de chat via session_state |
| Deploy | Streamlit Cloud | Alternativa à OCI Free Tier (instâncias com capacidade insuficiente em AD-1 São Paulo); URL pública funcional como critério de sucesso |

#### Formato das fontes

Os documentos `.md` são a fonte de verdade primária do RAG: leves, versionáveis pelo Git e parseáveis com extração de metadados YAML frontmatter (`document_id`, `version`, `status`, `owner`, `audience`, `visibility`). Versões em PDF serão geradas como artefato de evidência para entrega do edital.

#### Documentos privados e OCI Object Storage

Os documentos `06-politica-da-informacao.md` e `07-processos.md` contêm políticas internas e não devem ser expostos no repositório público. A arquitetura aprovada utiliza **OCI Object Storage com Pre-Authenticated Requests (PAR)**: os arquivos ficam em bucket privado na OCI, as URLs PAR são cadastradas nos Secrets do Streamlit Cloud, e o código baixa os documentos em runtime. Essa abordagem demonstra uso prático da infraestrutura Oracle no contexto do Challenge, mantém a segurança das fontes internas e permite atualização sem alterar o código.

Para o MVP imediato, o RAG opera com os dez documentos públicos já disponíveis. A integração OCI PAR está mapeada como próximo incremento.

### Identidade visual

O avatar da Amazô.guia foi atualizado para `assets/amazo-guia-avatar-g10.png`, criado especificamente para o Challenge G10. A paleta de cores para a interface Streamlit foi definida:

| Elemento | Cor Hex | Aplicação |
|---|---|---|
| Marrom profundo | `#2C1B12` | Background principal |
| Verde folha | `#2D4F1E` | Sidebar e containers |
| Verde-lima | `#A3C944` | Fontes e destaques |
| Rosa-terra | `#D48166` | Botões de ação (primary) |

### Segurança

Chaves de API gerenciadas via `.env` (local, gitignored) e `st.secrets` (Streamlit Cloud). Arquivo `.env.example` público documenta as variáveis necessárias sem expor valores. O system prompt da Amazô inclui blindagem contra jailbreak, não-divulgação de instruções internas e recusa educada para perguntas fora de escopo.

### Estado

Estrutura de código (`src/`), dependências, configuração de tema e segurança sendo criados. Pipeline de ingestão, agente e interface em sequência.

---

## Registro 003 — Entrega do Challenge G10

**Data:** 23 de agosto de 2026  
**Status:** MVP funcional entregue. Deploy público ativo.

### Redesign da Sidebar

A sidebar foi redesenhada para focar no projeto e não duplicar o papel da Amazô:
- Removidos emojis dos links e botões
- Removidos links do Hub (a Amazô os fornece nas respostas — sidebar seria redundância)
- Adicionada descrição do projeto com referência ao Challenge G10 / ONE / Oracle Next Education
- Mantidos apenas links do Repositório GitHub e da LP Showcase
- CSS atualizado: links em verde temático `#A3C944` em vez do azul padrão do Streamlit

### Migração de LLM: Google Gemini → Groq

**Diagnóstico:** O erro `google.api_core.exceptions.NotFound` persistia mesmo após trocar os nomes dos modelos. A causa raiz foi identificada: a `GOOGLE_API_KEY` disponível começa com `AQ.Ab`, que é um **OAuth2 token**, não uma API key do Google AI Studio. Keys válidas do AI Studio começam com `AIza`. O `langchain_google_genai` não aceita OAuth2 tokens nesse contexto.

**Decisão:** Migrar para **Groq** como provedor LLM — mais rápido, free tier generoso, sem restrições regionais, sem dependência de tipo de credencial Google.

| Antes | Depois |
|---|---|
| `langchain-google-genai` | `langchain-groq` |
| `google-generativeai` | — (removido) |
| `gemini-2.0-flash` → `gemini-1.5-flash` | `llama-3.1-70b-versatile` |
| `gemini-1.5-flash` (fallback) | `llama-3.1-8b-instant` (fallback) |
| `GOOGLE_API_KEY` | `GROQ_API_KEY` |

**Arquivos alterados:** `requirements.txt`, `src/config.py`, `src/agent.py`, `app.py`, `.env.example`

### Documentação para entrega

| Artefato | Ação |
|---|---|
| README.md | URL de deploy, exemplos Q&A, badge "MVP Funcional", seção de evidências, menção aos PDFs |
| notebooks/amazo_sandbox.ipynb | Criado a partir do .py para visualização no GitHub e execução no Colab |
| data/sources/pdf/ | 9 PDFs gerados com Unicode + links clicáveis para atendimento ao edital |
| DEVLOG.md | Registro 003 adicionado |
| showcase-status.yml | Atualizado para `mvp_funcional`, deploy ativo, Groq como LLM |

> **Decisão:** O script de geração de PDFs (`scripts/generate_pdfs.py`) foi usado para gerar os artefatos e removido do repositório. PDFs são estáticos — pipeline automatizado não agrega valor no escopo do MVP. Código limpo > código inútil.

### Deploy

- **URL:** https://amazo-guia-g10.streamlit.app/
- **Plataforma:** Streamlit Cloud (aceita conforme a live do Challenge como alternativa à OCI)
- **Secrets configurados:** `GROQ_API_KEY` via `st.secrets`
- **Cache version:** `v3.0-groq-llama31`

---

## Registro 004 — Resiliência de Deploy & Estabilização Final

**Data:** 23 de agosto de 2026  
**Status:** Validação final e estabilização de produção 100% concluída.

### 1. Resolução do Bug PyTorch Meta Tensor / Streamlit Cloud
- **Causa:** O ambiente de deploy provisionava Python 3.14 + PyTorch 2.13 nightly, gerando `NotImplementedError` na movimentação de meta tensores do `sentence-transformers`.
- **Solução 1:** Criação do `.python-version` fixando o runtime em `3.11`.
- **Solução 2 (Fallback Blindado):** Implementação da classe `TfidfEmbeddings` em `src/embeddings.py` que herda de `langchain_core.embeddings.Embeddings`. Se o modelo HuggingFace/PyTorch falhar por qualquer incompatibilidade de ambiente ou falta de GPU, o fallback de TF-IDF é ativado instantaneamente sem interromper o serviço.

### 2. Calibração de Modelos Groq
- Os modelos anteriores (`llama-3.3-70b` e `gemma2-9b-it`) foram descontinuados/restringidos no tier do Groq.
- Ativação dos modelos de alto desempenho abertos hospedados na infraestrutura Groq LPU:
  - **Primário:** `openai/gpt-oss-120b` (raciocínio avançado, respostas acolhedoras e fundamentadas)
  - **Fallback:** `openai/gpt-oss-20b` (alta velocidade)
- Atualização do `.env.example` para documentar `OPENAI_API_KEY` como contingência adicional.

### 3. Validação Funcional
- Respostas testadas em produção com citações de fonte em conformidade com as diretrizes da Amazô.guia e Encontro d'Água Hub.

