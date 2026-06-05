# Venture Insight — Venture Capital and M&A Copilot

O Venture Insight é um copiloto analítico projetado para simplificar a avaliação preliminar de indicadores setoriais, a consolidação de inteligência competitiva e a interpretação de dinâmicas de fomento e liquidez em rodadas de captação (fundraising) e operações de fusões e aquisições (M&A).

Abaixo está a estruturação técnica do projeto atualizada conforme os 6 passos exigidos pelo Laboratório de Inteligência Artificial da DIO.

---

## 1. Documentação do Agente

### Objetivo e Comportamento
O Venture Insight atua na lacuna entre a complexidade técnica das finanças corporativas e a necessidade de tomada de decisão ágil no mercado de capitais. O agente tem como objetivo sanar dúvidas conceituais, triar movimentações de transações recentes e analisar o panorama macroeconômico de inovação.

### Personas-Alvo e Escopo
* **Ana (Early-stage Founder):** Requer clareza sobre o impacto de diluição de rodadas e necessita mapear mecanismos de fomento não dilutivo locais para reduzir seu custo de capital.
* **Lucas (Analista de VC Júnior):** Necessita monitorar com agilidade o fluxo de transações nacionais e internacionais para elaboração de relatórios internos de tese de investimento.

### Diretrizes de Restrição (Guardrails)
Para mitigar o risco de alucinações factuais comuns em modelos conversacionais puros, o sistema opera sob três camadas hierárquicas de controle:
* **Ancoragem Estrita por Metadados:** O assistente prioriza as informações contidas na matriz local normalizada através de chaves explícitas de região (`regiao == "Rio de Janeiro"`), isolando o contexto geográfico.
* **Separação de Responsabilidades:** Toda a triagem lógica, filtros regionais e rotinas de auditoria (como a exclusão segura de registros em tempo real via UUID) são executados diretamente por blocos determinísticos em Python no backend do aplicativo (`src/app.py`), eliminando a necessidade de o modelo de linguagem realizar inferências lineares sobre a base de dados.
* **Trava de Escopo Temático (Whitelist Tokens):** O agente utiliza uma lista restrita de chaves de permissão para validar a consulta do usuário. Caso a entrada fuja do escopo de Venture Capital ou configure recomendação de trading de varejo, criptoativos ou finanças pessoais, o sistema aciona de forma determinística um bloqueio regulatório.

---

## 2. Base de Conhecimento

A base de conhecimento do agente é persistida localmente no arquivo `data/knowledge_base.json`. O pipeline de dados integrado no módulo `src/scraper.py` realiza o parsing automatizado de estruturas estruturadas e a classificação geográfica das seguintes origens conectadas:
* **Escopo Global:** VentureBeat Deals Channel (aportes em infraestrutura), EU-Startups (scaleups europeias), Tech in Asia (liquidez asiática) e Sifted (teses de capital de risco da inteligência de mercado europeia).
* **Escopo Nacional:** Startupi (rodadas de investimento), Distrito (consolidação de valuations domésticos) e Baguete Diário (mapeamento de fusões, aquisições e Corporate Venture Capital).
* **Escopo Regional (Rio de Janeiro):** FAPERJ (editais de subvenção econômica), Invest.Rio (programas de internacionalização), Porto Maravalley / CCPAR (editais de ocupação espacial do hub tecnológico), AgeRio (linhas de crédito produtivo subsidiado) e DATA.RIO (endpoints de dados abertos demográficos e de infraestrutura).

### Fundamentação Teórica da Base
A atratividade de um ecossistema de inovação ($U_e$) é modelada na base de conhecimento pela adaptação da Lei de Metcalfe para redes complexas:

$$U_e = \alpha \cdot N^2 - \beta \cdot C_t$$

Onde:
* $N$ representa o número de agentes ativos (startups, fundos e corporações);
* $\alpha$ representa o coeficiente de sinergia ou eficiência relacional do hub;
* $C_t$ representa o custo transacional, de barreira de entrada operacional ou de infraestrutura imobiliária;
* $\beta$ é o fator de fricção regulatória do ambiente de negócios.

Esta formulação justifica o foco analítico da plataforma no distrito tecnológico do Porto Maravalley e nos editais de fomento da FAPERJ, que atuam minimizando o custo transacional ($C_t$) e funcionando como uma camada de pré-validação técnica de ativos altamente atraentes para fundos privados subsequentes.

---

## 3. Prompts do Agente

As instruções de sistema (System Prompts) que governam a camada de raciocínio da inteligência artificial foram parametrizadas conforme a seguinte estrutura de controle:
* **Contexto:** Você atua como Copiloto Analítico do Venture Insight, especializado em finanças corporativas e ecossistemas de inovação.
* **Regra Geral:** Responda estritamente com base nos dados reais fornecidos no arquivo local JSON. Se a informação não constar na base ou violar os tokens permitidos, acione a mensagem padrão de restrição do sistema.
* **Regra de Inteligência de Contexto Regional (Rio de Janeiro):** Caso o usuário execute uma consulta direcionada ao ecossistema fluminense, aplique a árvore de decisão conceitual para separar as demandas:
  1. Se a consulta for orientada a Fundos, VC ou Private Equity, ative o mapeamento estrutural de liquidez institucional, detalhando o papel do BNDES como cotista âncora de fundos (LP's LP), a atuação de gestoras tradicionais de Asset Management locais e fundos verticais de Corporate Venture Capital focados na cadeia de energia.
  2. Se a consulta for orientada a Editais, Fomento ou Setores, direcione o escopo estritamente para as subvenções não dilutivas da FAPERJ e polos de inovação física (Porto Maravalley e Parque Tecnológico da UFRJ), eliminando falsos positivos de outras praças através de correspondência por metatags regionais.
* **Bloqueio Regulatório:** Não forneça recomendações diretas de compra de ativos, carteiras recomendadas ou aconselhamento financeiro regulado por órgãos competentes.
