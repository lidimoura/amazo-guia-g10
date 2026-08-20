# Amazô.guia — Guia Digital do Encontro d’água Hub

![Status](https://img.shields.io/badge/Status-Em%20construção-yellow)
![Projeto](https://img.shields.io/badge/Challenge-G10%20ONE%20IA%20for%20Tech-blue)
![LLM](https://img.shields.io/badge/LLM-Google%20Gemini-green)
![RAG](https://img.shields.io/badge/Arquitetura-RAG-purple)

> **Tecnologia acessível e sustentável.**

> **Ground Truth do produto:** os documentos institucionais e comerciais aprovados por Lídi Moura serão incorporados após sua consolidação no Perplexity e revisão final. Até essa etapa, nenhuma informação comercial, valor, processo ou documento é considerado fonte indexável neste repositório.

## Sobre o projeto

A **Amazô.guia** é um agente/chatbot SDR-RAG, representante e guia digital do **Encontro d’água Hub**, uma holding AI-Native fundada por **Lídi Moura** para criar soluções tecnológicas acessíveis e sustentáveis, com foco em impacto social.

Este repositório será a edição técnica do **Challenge Alura Agente — ONE IA for Tech G10**. O projeto apresenta a evolução da Amazô: de uma SDR e chatbot de recepção para uma agente capaz de acolher usuários, leads, clientes, recrutadores, participantes do Challenge e visitantes curiosos; consultar fontes de verdade; responder com rastreabilidade; e encaminhar cada pessoa ao link ou canal adequado.

Lídi Moura atua como **analista de dados, IA e automações**, criadora de soluções tecnológicas e fundadora do Encontro d’água Hub. A autoria do produto, as decisões de negócio, as decisões técnicas, as configurações, a curadoria das fontes, a validação e a responsabilidade final pertencem a ela.

## Origem e evolução

A Amazô.guia parte do showcase visual e conversacional existente, desenvolvido na versão Typebot. O showcase permanece em repositório separado e representa a origem do produto, sua identidade, narrativa e experiência inicial. Este repositório demonstrará a evolução técnica para um agente com RAG, fontes controladas, testes e documentação reproduzível.

- [Repositório Amazô IA Showcase — versão Typebot](https://github.com/lidimoura/amazo.ia-showcase)
- [LP pública do showcase da Amazô](https://lidimoura.github.io/amazo.ia-showcase/)
- [Portfólio da Lídi Moura criado com Link d’Água](https://link.encontrodagua.com/r/portifolio-lidimoura)

## Problema e proposta de valor

Informações sobre o Hub, sua fundadora, produtos, serviços, processos e valores precisam ser apresentadas de maneira acessível, consistente e verificável. Um chatbot sem uma base documental controlada pode misturar versões, criar promessas indevidas ou responder com informações que não foram aprovadas.

A Amazô.guia será construída para responder com base em documentos autorizados, identificar a intenção do visitante, qualificar leads de forma inicial e apresentar fontes. Quando não houver evidência suficiente, deverá declarar a limitação e orientar a pessoa para um canal público ou atendimento humano, sem afirmar que executou uma ação que não executou.

## Públicos previstos

| Público | Necessidade principal |
|---|---|
| Usuário ou visitante curioso | Entender o Hub e a proposta de tecnologia acessível e sustentável |
| Potencial cliente B2B | Conhecer produtos, serviços, processos e próximos passos |
| Lead | Receber acolhimento, qualificação inicial e encaminhamento adequado |
| Recrutador | Conhecer a trajetória, competências e projetos de Lídi Moura |
| Pessoa interessada na demonstração | Entender a evolução do produto, seu funcionamento e seus limites |
| Parceiro | Identificar produtos, possibilidades de colaboração e canais públicos |

A Amazô.guia poderá encaminhar cada público para um canal público aprovado conforme sua intenção: WhatsApp do Hub, WhatsApp pessoal de Lídi Moura, portfólio, LP institucional do Hub, Link d’Água, CRM ou outro link público autorizado. A seleção do canal deverá vir de uma configuração ou documento aprovado; a agente não deve inventar URLs. No MVP, “encaminhar” significa apresentar o link ou canal ao usuário. O registro automático no CRM ou no Link d’Água só poderá ser afirmado quando existir integração validada.

## Escopo inicial do Challenge

O MVP será documental, read-only e isolado dos sistemas produtivos. A direção técnica prevista é Python, Google Gemini como LLM principal, arquitetura RAG e uma interface prática a ser definida depois da validação do núcleo. O agente deverá consultar fontes aprovadas, recuperar trechos pertinentes, gerar resposta em português brasileiro, citar documento/versão/página quando disponível, recusar perguntas sem evidência e resistir a tentativas de prompt injection.

Os documentos do Perplexity serão enviados posteriormente por Lídi Moura. Eles deverão ser revisados, classificados, versionados e aprovados antes da ingestão. O repositório não conterá, nesta etapa, PDFs comerciais, valores, dados de clientes, leads reais ou documentos inventados.

## Camadas de fontes e armazenamento

A governança proposta separa a elaboração da execução:

| Camada | Finalidade | Estado atual |
|---|---|---|
| Perplexity e Google Drive | Produção, consolidação, revisão e aprovação dos documentos de fonte de verdade | Pendente de envio dos documentos |
| OCI Object Storage privado | Armazenamento controlado dos documentos aprovados para ingestão | Opção arquitetural; não configurado |
| Vector store local | Desenvolvimento, aprendizagem, testes e fallback | Será implementado em incremento posterior |
| OCI Autonomous AI Database | Backend vetorial opcional e diferencial de infraestrutura | Será avaliado sem bloquear o MVP |

O uso do OCI não autoriza custo, criação de recurso, publicação de bucket, exposição de URL privada ou inclusão de credenciais. Qualquer configuração exigirá etapa própria, validação de limites, segurança e aprovação.

## Transparência de autoria e ferramentas

Este projeto é de autoria e propriedade de **Lídi Moura**. Ela mantém autonomia sobre escopo, produto, decisões técnicas, configurações, fontes, testes, validação e responsabilidade final.

O **Hub OS NEXUS**, como infraestrutura metodológica e operacional da holding AI-Native Encontro d’água Hub, é utilizado para aumentar agilidade, organização e qualidade. O Hub OS já foi validado em projetos pessoais e trabalhos freelance do próprio Hub, mas não substitui a autoria nem delega decisões à ferramenta.

As ferramentas têm papéis complementares:

| Ferramenta | Papel no projeto |
|---|---|
| Lídi Moura | Autoria, decisões, curadoria, configuração, validação e responsabilidade final |
| Hub OS NEXUS | Organização metodológica, governança, foco, documentação e qualidade |
| Manus AI | Apoio em diagnóstico, arquitetura, documentação, implementação incremental e QA |
| Google Gemini | LLM principal da Amazô.guia |
| Perplexity | Pesquisa e consolidação assistida dos documentos de fonte de verdade, sob revisão da autora |
| Google Colab | Ambiente pedagógico e experimental para notebooks e primeiros testes |
| Antigravity | IDE opcional para desenvolvimento paralelo, com revisão antes de incorporar código ao repositório |

## Fora do MVP

Não fazem parte do primeiro MVP: n8n, reconfiguração do n8n self-hosted, automações de produção, acesso direto ao Supabase, gravação automática de leads, CRM produtivo, WhatsApp produtivo, memória conversacional persistente, substituição automática do Typebot, autenticação multi-tenant e criação imediata de infraestrutura OCI.

O encaminhamento futuro de leads ao Link d’Água, serviço do Hub para minisites e QR Codes dinâmicos, e ao CRM do Hub deverá ocorrer por camada server-side autorizada, com consentimento, minimização de dados, idempotência, RBAC, RLS, logs sanitizados, feature flag e rollback. No MVP, a Amazô poderá qualificar e indicar canais públicos, mas não deverá afirmar que gravou ou encaminhou um lead sem integração validada.

## Segurança e limites

Nenhum segredo, token, senha, wallet, PII desnecessária, prompt interno, fonte privada ou credencial será incluído no repositório. Perguntas fora do domínio, como política, notícias em tempo real ou solicitações que exijam aconselhamento personalizado, deverão ser redirecionadas. Tentativas de prompt injection deverão ser recusadas sem revelar instruções internas, fontes restritas ou configurações.

## Roadmap incremental

1. Fundação documental e registro das decisões.
2. Recebimento, curadoria e aprovação dos documentos do Perplexity.
3. Notebook pedagógico com ingestão e recuperação local.
4. RAG funcional com Gemini e citações.
5. Prompt da Amazô.guia, roteamento de públicos e testes de segurança.
6. Interface demonstrável e documentação de uso.
7. Avaliação opcional do OCI Object Storage e Autonomous AI Database.
8. Deploy, evidências e preparação da entrega do Challenge.

## Estado atual

O projeto está em **fase de fundação e aprovação documental**. Neste primeiro incremento, o repositório deverá receber somente este `README.md` e o `DEVLOG.md`. O agente, a ingestão, o índice, os testes, a interface e o deploy ainda não estão validados.

## Ecossistema público do Hub

- [Repositório Amazô IA Showcase — versão Typebot](https://github.com/lidimoura/amazo.ia-showcase)
- [LP pública do showcase da Amazô](https://lidimoura.github.io/amazo.ia-showcase/)
- [Hub Encontro d’água](https://hub.encontrodagua.com)
- [Link d’Água — vitrine pública](https://link.encontrodagua.com/vitrine)
- [Portfólio da Lídi Moura criado com Link d’Água](https://link.encontrodagua.com/r/portifolio-lidimoura)
- [Repositório Link d’Água](https://github.com/lidimoura/link-dagua)
- [Repositório Encontro d’água Hub Digital](https://github.com/lidimoura/encontro-dagua-hub-digital)
- [Hub OS NEXUS](https://github.com/lidimoura/hub-os-nexus)

Os links diretos de WhatsApp do Hub, WhatsApp pessoal, CRM ou outros canais poderão ser adicionados somente quando forem confirmados e aprovados por Lídi Moura. Documentos, links privados e referências utilizadas exclusivamente no processo de criação do Challenge não serão publicados neste README sem consentimento explícito.
## Licença e estado de publicação

A licença e a visibilidade do repositório serão definidas antes da publicação, após auditoria de segredos, PII, licenças e fontes. Até lá, o repositório deverá permanecer privado.

---

**Lídi Moura — analista de dados, IA e automações | Fundadora do Encontro d’água Hub**
