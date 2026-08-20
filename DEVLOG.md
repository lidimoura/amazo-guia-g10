# DEVLOG — Amazô.guia do Encontro d’água Hub

## Registro 001 — Fundação documental do repositório

**Data:** 20 de agosto de 2026  
**Status:** Rascunho para aprovação da autora; ainda não incorporado ao repositório oficial.

### Objetivo

Preparar a fundação documental do repositório do Challenge Alura Agente — ONE IA for Tech G10, apresentando a evolução da Amazô para **Amazô.guia do Encontro d’água Hub**.

### Autoria e responsabilidade

O projeto é de autoria e propriedade de **Lídi Moura**, analista de dados, IA e automações, criadora de soluções tecnológicas e fundadora do Encontro d’água Hub. Lídi mantém autonomia sobre produto, escopo, decisões técnicas, configurações, curadoria das fontes, validação e responsabilidade final.

O Hub OS NEXUS, utilizado no contexto da holding AI-Native Encontro d’água Hub, atua como infraestrutura metodológica e operacional para aumentar agilidade, organização e qualidade. O Hub OS já foi validado em projetos pessoais e trabalhos freelance do próprio Hub, mas não substitui a autoria da Lídi nem toma decisões autônomas sobre o produto.

### Decisões aprovadas até aqui

| Tema | Decisão |
|---|---|
| Produto | Amazô.guia do Encontro d’água Hub |
| Posicionamento | Agente/chatbot SDR-RAG, representante e guia digital |
| Pitch | “Tecnologia acessível e sustentável.” |
| Origem | Evolução do showcase Typebot da Amazô |
| LLM | Google Gemini, configurado por variável de ambiente |
| Fontes de verdade | Documentos institucionais e comerciais a serem enviados após consolidação no Perplexity |
| Curadoria | Perplexity/Google Drive para preparação e revisão; Lídi aprova antes da indexação |
| Armazenamento futuro | OCI Object Storage privado como opção controlada |
| Backend vetorial | Local para aprendizado/fallback; OCI Autonomous AI Database como opção posterior |
| Integrações | Link d’Água e CRM somente como roadmap; nenhum acesso produtivo no MVP |
| Automação | n8n fora do MVP |
| Ambiente pedagógico | Colab/local; Antigravity pode ser usado como IDE auxiliar sob revisão |
| Meta de entrega | Até 22 de agosto de 2026, usando o dia 24 como prazo oficial informado a reconfirmar |

### Escopo deste primeiro incremento

O primeiro incremento oficial deverá conter **somente dois arquivos reais**:

- `README.md`, com identidade, origem, proposta, fontes, escopo, segurança, transparência e roadmap;
- `DEVLOG.md`, com o registro das decisões e do método incremental.

Não serão criados neste incremento `.gitignore`, `.env.example`, `requirements.txt`, pastas, notebooks, módulos Python, fixtures, PDFs, índices, imagens, documentos de tradução ou arquivos auxiliares.

### Fontes do RAG

Os documentos de fonte de verdade ainda serão enviados por Lídi Moura. Eles não serão inventados, substituídos ou indexados antecipadamente. Antes de qualquer ingestão, deverão ser revisados quanto a autoria, versão, vigência, visibilidade, PII, valores, processos, permissões e aprovação.

O Google Drive/Perplexity será documentado como camada de elaboração e curadoria. O OCI Object Storage privado poderá ser adotado depois como camada de armazenamento controlado e reprodutível. A criação do bucket, configuração de IAM, upload, eventual URL pré-autenticada, custos e integração com o Autonomous AI Database serão tarefas separadas e dependerão de validação e aprovação.

### Showcase de origem

O repositório [amazo.ia-showcase](https://github.com/lidimoura/amazo.ia-showcase) e sua [LP pública](https://lidimoura.github.io/amazo.ia-showcase/) serão citados como origem da evolução da Amazô. Eles não serão copiados para este repositório nem apresentados como se já contivessem a implementação RAG do Challenge.

### Roteamento para canais públicos

A Amazô.guia poderá apresentar o canal adequado conforme a intenção do visitante: WhatsApp do Hub, WhatsApp pessoal de Lídi Moura, portfólio, LP institucional do Hub, Link d’Água, CRM ou outro link público aprovado. Os links deverão vir de configuração ou documento autorizado. O MVP poderá exibir o canal, mas não deverá afirmar que registrou ou encaminhou automaticamente um lead enquanto não existir uma integração validada.

### Transparência sobre ferramentas

A documentação informará que Manus AI, Gemini, Perplexity, Google Colab e Antigravity são ferramentas complementares do processo. Cada ferramenta tem uma função de apoio; a autoria, as decisões, as configurações, a curadoria, os testes e a responsabilidade final permanecem com Lídi Moura.

### Segurança e limites

O projeto seguirá tolerância zero a hardcode de segredos. Não serão incluídos tokens, senhas, wallets, credenciais, PII desnecessária, prompts internos, fontes privadas ou dados de produção. O agente deverá ser testado contra prompt injection, perguntas fora do escopo e tentativas de extração de instruções internas.

### Método de trabalho

Cada incremento será pequeno e acompanhado por escopo, justificativa, diff, teste, resultado, limitação e aprovação. Nenhum arquivo será criado apenas para preencher uma estrutura futura. A ordem pedagógica priorizará entendimento e autonomia: fontes aprovadas, ingestão, chunking, embeddings, recuperação, geração com Gemini, citações, testes, interface e somente depois infraestrutura ou integrações.

### Referências públicas e privacidade documental

O README e o DEVLOG manterão apenas links públicos do ecossistema do Hub e do showcase que tenham sido autorizados. Links privados, documentos internos e referências usadas exclusivamente para o processo de criação do Challenge não serão publicados sem consentimento explícito de Lídi Moura.

### Próxima etapa pendente de aprovação

Após a aprovação deste conteúdo, criar o repositório privado do Challenge e incorporar somente `README.md` e `DEVLOG.md`. Antes do primeiro commit, apresentar o diff e confirmar que não existem outros arquivos ou artefatos no escopo oficial.
