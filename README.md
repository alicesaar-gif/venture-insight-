# Venture Insight — Venture Capital & M&A Copilot

O Venture Insight é um copiloto analítico projetado para simplificar a avaliação preliminar de indicadores financeiros, a consolidação de inteligência competitiva e a interpretação de dinâmicas societárias em rodadas de captação (*fundraising*) e operações de fusões e aquisições (M&A).

Abaixo está a estruturação do projeto conforme os 6 passos exigidos pelo Laboratório de Inteligência Artificial da DIO.

---

## 1. Documentação do Agente

### Objetivo e Comportamento
O Venture Insight atua na lacuna entre a complexidade técnica das finanças corporativas e a necessidade de tomada de decisão ágil no mercado de capitais. O agente tem como objetivo sanar dúvidas conceituais, triar notícias de transações recentes e analisar o panorama de inovação.

### Personas-Alvo e Escopo
* **Ana (Early-stage Founder):** Requer clareza sobre o impacto de diluição de rodadas e necessita mapear mecanismos de fomento não dilutivo locais.
* **Lucas (Analista de VC Júnior):** Necessita monitorar com agilidade o fluxo de transações nacionais e internacionais para relatórios internos.

### Diretrizes de Restrição (Guardrails)
Para mitigar o risco de alucinações factuais e matemáticas comuns em modelos conversacionais puros, o sistema opera sob três camadas hierárquicas:
1. **Ancoragem Dinâmica:** O assistente prioriza estritamente as informações contidas na matriz local normalizada.
2. **Separação de Responsabilidades:** Toda operação aritmética complexa é direcionada a funções determinísticas em Python no módulo `core_finance.py`, eliminando a necessidade de o modelo de linguagem realizar cálculos lineares.
3. **Trava de Escopo Temático:** O agente é instruído a não emitir recomendações individuais de trading de ativos regulados de varejo, criptoativos ou finanças pessoais.

---

## 2. Base de Conhecimento

A base de conhecimento do agente é persistida localmente no arquivo `data/knowledge_base.json`. O pipeline de dados realiza o *parsing* automatizado de estruturas estáveis e a classificação geográfica automática dos seguintes endpoints integrados:

* **Escopo Global:** VentureBeat Deals Channel (aportes em infraestrutura de IA), EU-Startups (*scaleups* europeias), Sifted (teses de capital de risco) e Tech in Asia (liquidez asiática).
* **Escopo Nacional:** Startupi (rodadas do anjo ao Series B), Distrito (consolidação de *valuations* domésticos) e Baguete Diário (operações de M&A e *Corporate Venture Capital* via sitemaps XML).
* **Escopo Regional (Rio de Janeiro):** FAPERJ (editais de subvenção), Invest.Rio (atração de capital), Porto Maravalley/CCPAR (editais de ocupação do hub físico), AgeRio (crédito produtivo) e DATA.RIO (APIs abertas de dados demográficos).

### Fundamentação Teórica da Base
A atratividade de um ecossistema de inovação ($U_e$) é modelada na base de conhecimento pela adaptação da Lei de Metcalfe para redes complexas:

$$U_e = \alpha \cdot N^2 - \beta \cdot C_t$$

Onde:
* $N$ representa o número de agentes ativos;
* $\alpha$ representa o coeficiente de sinergia ou eficiência relacional do hub;
* $C_t$ representa o custo transacional ou de barreira de entrada operacional e de infraestrutura imobiliária;
* $\beta$ é o fator de fricção regulatória do ambiente de negócios.

Esta formulação justifica o foco analítico da plataforma no distrito tecnológico do Porto Maravalley e nos editais de subvenção da FAPERJ, que atuam minimizando o custo $C_t$ e validando ativos de Deep Tech antes de rodadas privadas.

---

## 3. Prompts do Agente

As instruções de sistema (*System Prompts*) que governam a camada de raciocínio da inteligência artificial foram parametrizadas conforme a seguinte estrutura de controle:

```text
Contexto: Você atua como Copiloto Analítico do Venture Insight.
Regra Geral: Responda estritamente com base nos dados reais fornecidos no arquivo local. Se a informação não constar na base, acione o fallback geográfico ou informe os limites do conhecimento atual.
Regra Especial (Rio de Janeiro): Caso o usuário solicite dados específicos do ecossistema fluminense/carioca e o feed factual esteja vazio, ative a inteligência estrutural nativa mapeando os principais pólos estratégicos locais (Porto Maravalley e Parque Tecnológico da UFRJ).
Bloqueio: Não forneça recomendações diretas de compra de ativos ou aconselhamento financeiro regulado.