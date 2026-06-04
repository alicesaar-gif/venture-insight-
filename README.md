# Venture Insight — Venture Capital & M&A Copilot

O **Venture Insight** é um assistente analítico desenhado para simplificar a avaliação preliminar de indicadores financeiros, a interpretação de contratos de investimento (*Term Sheets*, contratos *SAFE*) e a simulação de cenários societários em rodadas de captação (*fundraising*) e operações de fusões e aquisições (M&A).

Diferente de soluções conversacionais genéricas, a plataforma implementa uma arquitetura que separa o processamento numérico estruturado da camada de contextualização em linguagem natural, mitigando o risco de alucinações matemáticas em métricas críticas de mercado.

## Visão do Produto e Proposta de Valor

No ecossistema de inovação e capital de risco, a assimetria de informação e a dependência de planilhas complexas geram gargalos operacionais e erros de precificação. O Venture Insight atua na lacuna entre a complexidade técnica das finanças corporativas e a necessidade de tomada de decisão ágil, permitindo que fundadores e analistas ajam com verdadeiro **senso de dono** sobre seus ativos, Cap Tables e indicadores operacionais.

### Personas-Alvo

* **Ana (Early-stage Founder):** Requer clareza sobre o impacto de diluição de um SAFE (*Simple Agreement for Future Equity*) em sua participação acionária antes de iniciar negociações formais com fundos de Venture Capital.
* **Lucas (Analista de VC Júnior):** Necessita validar rapidamente a consistência e o equilíbrio entre a taxa de queima de caixa (*burn rate*) e os indicadores de eficiência operacional (*LTV/CAC*) de ativos entrantes no pipeline de investimento.

## Arquitetura da Solução e Fluxo de Dados

O pipeline de dados foi projetado para assegurar rastreabilidade, governança de escopo e persistência de contexto corporativo ao longo da sessão de uso.

```text
[ Usuário ] ──(Interface Web: Streamlit)──> [ Gestão de Estado: Session State ]
                                                        │
                                                        │ (Preserva o modelo de negócio, ex: SaaS)
                                                        ▼
[ OpenAI API ] <──(Prompt + Dados Ancorados)── [ Orquestrador Python ]
                                                        ▲
                                                        │
                                                        │ (Queries de conceitos e fórmulas exatas)
                                           [ Base de Conhecimento: JSON ]


## Estrutura do Repositório

```text
venture-insight/
├── README.md               # Documentação executiva e proposta de valor
├── data/
│   └── knowledge_base.json # Matriz de dados ancorados (Métricas, Term Sheets, M&A)
├── docs/
│   └── ux_strategy.md      # Jornada do usuário, arquitetura de telas e wireframes
└── src/
    ├── app.py              # Interface gráfica e controle de sessão (Streamlit)
    ├── prompts.py          # Engenharia de prompts e travas de segurança sistêmica
    └── core_finance.py     # Engine matemática (Cálculos determinísticos em Python)

```

## Roadmap de Evolução do Produto

| Fase | Escopo Funcional | Status |
| --- | --- | --- |
| **MVP** | Assistente conversacional ancorado para termos técnicos e métricas corporativas; simulador de *Runway* nativo em Python; persistência de contexto verticalizado por modelo de negócio (SaaS, Marketplace, Fintech, HealthTech). | Concluído |
| **Versão 2** | Simulador dinâmico de rodadas *Pre-Money* e *Post-Money*; visualização gráfica da evolução do Cap Table pós-diluição; módulo de ingestão e análise preliminar de minutas de *Term Sheets*. | Em desenvolvimento |
| **Versão 3** | Arquitetura RAG (*Retrieval-Augmented Generation*) integrada a bancos de dados vetoriais para consulta de bases públicas e relatórios macroeconômicos em tempo real. | Planejado |

## Engenharia de Prompts e Mitigação de Alucinações

Para garantir a confiabilidade indispensável em análises corporativas, a governança do modelo baseia-se em três camadas de controle:

1. **Ancoragem de Dados:** O modelo restringe suas respostas aos conceitos formalizados no arquivo `data/knowledge_base.json`.
2. **Separação de Responsabilidades:** O Large Language Model (LLM) não realiza cálculos lineares. Toda operação aritmética é delegada ao módulo `core_finance.py`. O modelo de linguagem atua exclusivamente na tradução e contextualização dos resultados numéricos.
3. **Restrição de Escopo:** O comportamento do agente é blindado via instruções de sistema (*System Prompt*):

> "Você atua como Analista Sênior do Venture Insight. Responda estritamente com base nos dados fornecidos na base interna de Venture Capital e M&A. Não forneça recomendações de investimento, projeções de rentabilidade ou aconselhamento financeiro individualizado. Caso o usuário solicite informações sobre ações de varejo, criptoativos ou finanças pessoais, informe que tais temas estão fora do escopo analítico da plataforma."

## Validação Funcional e Testes de Estresse

A estabilidade da solução foi testada em cenários reais para garantir aderência metodológica e segurança de escopo:

| Entrada do Usuário (Input) | Comportamento Esperado | Resultado Prático |
| --- | --- | --- |
| *"Minha startup faturou X e gastou Y. Qual meu burn rate?"* | Capturar as variáveis, executar o cálculo através da engine matemática e retornar o valor exato contextualizado. | Aprovado |
| *"Minha startup é um SaaS B2B."* seguido de *"Meu LTV/CAC é 2,5x. Está bom?"* | Preservar a memória do modelo de negócio e comparar o indicador com os benchmarks de mercado para o segmento SaaS. | Aprovado |
| *"Qual a melhor ação da bolsa para comprar hoje?"* | Interromper a requisição imediatamente com base nas regras de restrição de escopo. | Aprovado |

---

## Diferenciais Competitivos

* **Especialização Vertical:** Foco exclusivo no ecossistema de inovação e finanças corporativas, eliminando respostas genéricas comuns em modelos abertos.
* **Cálculos Determinísticos:** Mitigação de erros lógicos através da execução de fórmulas puras em Python incorporadas ao fluxo conversacional.
* **Contexto Persistente Corporativo:** Capacidade de reter informações estratégicas do negócio do usuário para personalizar o diagnóstico financeiro ao longo do chat.

---

## Execução Local

### 1. Clonagem do Repositório

```bash
git clone https://github.com/seu-usuario/venture-insight.git
cd venture-insight

```

### 2. Instalação de Dependências

```bash
pip install -r requirements.txt

```

### 3. Configuração de Variáveis de Ambiente

Crie um arquivo `.env` no diretório raiz da aplicação:

```env
OPENAI_API_KEY=sua_chave_aqui

```

### 4. Inicialização do Sistema

```bash
streamlit run src/app.py

```


