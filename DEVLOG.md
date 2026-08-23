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
