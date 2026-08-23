# Sincronização com o Showcase Amazô G10

O repositório técnico `amazo-guia-g10` é a referência de implementação do Challenge. A LP `amazo-g10-showcase` traduz somente informações públicas, aprovadas e relevantes para a narrativa de acompanhamento. O código, a base documental, os testes e as decisões técnicas continuam neste repositório; a LP não substitui a documentação do MVP.

## Fonte operacional para a LP

O arquivo [`showcase-status.yml`](./showcase-status.yml) é o contrato público de sincronização. Ele deve ser atualizado junto com uma mudança relevante no estado do Challenge, sempre após a revisão da Lídi. A LP só pode refletir os campos desse manifesto ou documentos explicitamente marcados como públicos e aprovados.

| Campo | Uso no showcase | Limite |
|---|---|---|
| `project.phase` | Status narrativo do Challenge. | Não inventar marcos, deploys ou integração. |
| `rag.source_catalog_status` | Explica se a fonte de verdade está em curadoria, aprovada ou ativa. | Não listar arquivos antes de aprovação. |
| `rag.approved_document_groups` | Mostra os núcleos de fonte de verdade liberados. | Não incluir conteúdo, links privados ou dados pessoais. |
| `rag.ingestion_status` e `rag.test_status` | Atualiza arquitetura, QA e evidências. | Publicar somente após validação registrada. |
| `showcase.public_evidence` | Habilita prints, vídeos, logs sanitizados ou métricas aprovadas. | Nunca incluir PII, segredos ou dados de clientes. |

## Estado atual (23/08/2026)

| Item | Status |
|---|---|
| Deploy | ✅ Ativo — https://amazo-guia-g10.streamlit.app/ |
| LLM | ✅ Groq / Llama 3.1 70B (migrado de Gemini) |
| Fontes (.md) | ✅ 9 documentos aprovados e ingeridos |
| Fontes (PDF) | ✅ 9 PDFs gerados com links clicáveis |
| Notebook Colab | ✅ notebooks/amazo_sandbox.ipynb |
| QA / Prints | ⏳ Pendente validação e captura de evidências |
| Showcase LP | ⏳ Aguardando aprovação da CEO após QA |

## Regra de mudança

1. Atualize o manifesto e o DEVLOG técnico com o fato verificável.
2. Marque `showcase.update_required: true` e explique a razão em `showcase.update_reason`.
3. O pedido manual `sincronizar showcase com amazo-guia-g10` compara o manifesto com a LP.
4. A Lídi aprova o diff narrativo e visual antes de qualquer publicação no GitHub Pages.
5. Depois da publicação, o manifesto pode registrar o novo estado de sincronização em uma mudança posterior aprovada.

## Limites de segurança

Não usar este arquivo para fontes privadas, CRM, Supabase, leads, credenciais, prompts internos, dados financeiros, documentos em rascunho ou conteúdo protegido. Materiais e ferramentas de pesquisa são internos e não constituem fonte automática do RAG.
