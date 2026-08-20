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
