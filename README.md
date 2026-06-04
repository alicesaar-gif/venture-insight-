# Venture Insight — Venture Capital & M&A CopilotO Venture Insight é um copiloto financeiro inteligente projetado para simplificar a análise preliminar de indicadores, a interpretação de contratos de investimentos e a simulação de cenários societários em rodadas de captação (fundraising) e operações de M&A.Diferente de assistentes conversacionais genéricos, a ferramenta mitiga o risco de alucinações matemáticas ao separar o processamento numérico estruturado (funções matemáticas puras) da camada de contextualização em linguagem natural.## 🎯 Visão do Produto & Proposta de ValorNo ecossistema de inovação, tempo é caixa e planilhas complexas geram fricção. O Venture Insight atua na lacuna entre a complexidade técnica das finanças corporativas e a necessidade de tomada de decisão ágil, permitindo que fundadores ajam com verdadeiro senso de dono sobre seu próprio Cap Table e suas métricas.### Personas AlvoAna (Early-stage Founder): Precisa entender o impacto de diluição de uma nota conversível (SAFE) em sua participação acionária antes de sentar à mesa com fundos de VC.Lucas (Analista de VC Júnior): Precisa validar rapidamente se o equilíbrio entre as métricas de queima de caixa (burn rate) e eficiência (LTV/CAC) de uma startup entrante no pipeline está saudável.## 🏗️ Arquitetura da Solução e Fluxo de DadosO ecossistema foi desenhado para garantir rastreabilidade, segurança e contexto persistente ao longo da sessão do usuário.Plaintext[ Usuário ] ──(Interface Web: Streamlit)──> [ Gestão de Estado (Session State) ]
                                                        │ (Mantém modelo de negócio ex: SaaS)
                                                        ▼
[ OpenAI API (LLM) ] <──(Prompt + Dados)─── [ Orquestrador Python ]
                                                        ▲
                                                        │ (Busca fórmulas e conceitos exatos)
                                            [ Base de Conhecimento (JSON) ]
## 🛠️ Estrutura do RepositórioPlaintextventure-insight/
├── README.md               # Documentação principal e Pitch do projeto
├── data/
│   └── knowledge_base.json # Base de dados ancorada (Métricas, Term Sheets, M&A)
├── docs/
│   └── ux_strategy.md      # Jornada do usuário, regras de explicabilidade e wireframes
└── src/
    ├── app.py              # Interface gráfica e gerenciamento de estado (Streamlit)
    ├── prompts.py          # Engenharia de Prompts (System Prompts e travas de segurança)
    └── core_finance.py     # Engine matemática (Cálculos de Runway, Diluição e LTV/CAC)
## 🚀 Funcionalidades Prioritárias (Roadmap)FaseFuncionalidadeStatusMVPConversação contextual sobre termos (SAFE, Cap Table) ancorada em JSON; simulador analítico de Runway na barra lateral; persistência do modelo de negócio (Ex: SaaS B2B vs Marketplace).ConcluídoVersão 2Simulador dinâmico de rodadas Pre e Post-Money com geração de gráfico de pizza do Cap Table; upload e análise rápida de PDFs (Term Sheets).Em DesenvolvimentoVersão 3Arquitetura RAG (Retrieval-Augmented Generation) com banco vetorial conectando dados macroeconômicos e de múltiplos mercados em tempo real.Planejado## 🛡️ Engenharia de Prompts e Mecanismos Anti-AlucinaçãoPara mitigar os riscos associados ao uso de Inteligência Artificial em ambientes financeiros, o Venture Insight adota três camadas de governança:Ancoragem em Base Privada: O modelo só responde a conceitos previamente mapeados e catalogados em data/knowledge_base.json.Separação de Preocupações (Separation of Concerns): A inteligência artificial não faz contas matemáticas. O processamento numérico é delegado ao módulo core_finance.py. A IA atua apenas traduzindo e interpretando os resultados gerados por código determinístico.Prompt de Bloqueio Sistêmico:"Você é o analista sênior do Venture Insight. Responda apenas com base nos dados fornecidos na base interna de Venture Capital e M&A. Se o usuário questionar sobre ativos de varejo (ações, criptoativos) ou finanças pessoais, recuse a resposta educadamente informando o limite do seu escopo."## 📊 Critérios de Validação e Testes de EstresseA qualidade do assistente foi avaliada sob três pilares de interação testados no ambiente de homologação:Entrada do Usuário (Input)Comportamento EsperadoResultado Prático"Minha startup faturou X e gastou Y. Qual meu burn rate?"Capturar dados, processar em core_finance.py e exibir o valor exato contextualizado.Aprovado"Minha startup é um SaaS B2B." e depois "Meu LTV/CAC é 2.5x. Está bom?"Lembrar que o modelo é SaaS e apontar que o mercado busca uma eficiência superior a 3.0x para esse setor.Aprovado"Qual a melhor ação da bolsa para comprar hoje?"Bloqueio imediato por escopo, preservando a segurança da marca e evitando aconselhamento informal.Aprovado## ⚙️ Como Executar o Projeto LocalmenteClone o repositório:Bashgit clone https://github.com/seu-usuario/venture-insight.git
cd venture-insight

2. **Instale as dependências:**
   ```bash
pip install -r requirements.txt
Configure suas chaves de ambiente:Crie um arquivo .env na raiz do projeto e insira sua credencial da API:Snippet de códigoOPENAI_API_KEY=seu_token_aqui

4. **Execute a aplicação:**
   ```bash
   streamlit run src/app.py
