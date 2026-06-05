import streamlit as st
import json
import os
import uuid
from scraper import capturar_noticias_vc

st.set_page_config(page_title="Venture Insight - VC & M&A Copilot", layout="wide")

JSON_PATH = os.path.join("data", "knowledge_base.json")

@st.cache_data
def load_knowledge():
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

dados_salvos = load_knowledge()

with st.sidebar:
    st.header("Controle do Sistema")
    st.write("Gerenciamento automatizado de conexões e pipelines de dados.")
    if st.button("Sincronizar Bases de Dados (Web Scraping)"):
        with st.spinner("Executando varredura nos endpoints homologados..."):
            novos = capturar_noticias_vc()
            st.cache_data.clear()
        st.success(f"Operação concluída. {novos} registros adicionados à matriz local.")
        st.rerun()

col_painel, col_assistente = st.columns([0.55, 0.45], gap="large")

with col_painel:
    st.title("Venture Insight - Matriz de Dados")
    st.write("Camada de persistência, auditoria de integridade e inserção de teses.")

    with st.expander("Inserção Manual de Ativo ou Tese de Investimento"):
        with st.form("input_manual", clear_on_submit=True):
            nome = st.text_input("Identificador do Ativo / Título da Fonte")
            insight = st.text_area("Sumário Técnico / Análise Qualitativa")
            regiao_escolhida = st.selectbox("Escopo Geográfico", ["Brasil", "Global", "Rio de Janeiro"])
            submitted = st.form_submit_button("Gravar na Base Local")
            
            if submitted and nome and insight:
                if os.path.exists(JSON_PATH):
                    try:
                        with open(JSON_PATH, "r", encoding="utf-8") as f:
                            lista_atual = json.load(f)
                    except json.JSONDecodeError:
                        lista_atual = []
                else:
                    lista_atual = []

                lista_atual.append({
                    "id": str(uuid.uuid4()),
                    "nome": nome,
                    "insight": insight,
                    "regiao": regiao_escolhida,
                    "fonte": "Inserção Manual"
                })
                
                with open(JSON_PATH, "w", encoding="utf-8") as f:
                    json.dump(lista_atual, f, indent=4, ensure_ascii=False)
                st.cache_data.clear()
                st.rerun()

    st.divider()
    st.subheader("Registros e Insights Consolidados na Base Ativa")
    
    if dados_salvos:
        busca = st.text_input("Filtrar registros por palavra-chave:", placeholder="Ex: FAPERJ, Distrito, Deals...")
        
        for item in dados_salvos:
            if isinstance(item, dict):
                item_id = item.get('id')
                nome = item.get('nome', 'Identificador Ausente')
                insight_texto = item.get('insight', 'Conteúdo Ausente')
                regiao = item.get('regiao', 'Global')
                fonte_origem = item.get('fonte', 'Desconhecida')
                
                if busca.lower() not in nome.lower() and busca.lower() not in insight_texto.lower():
                    continue
                
                with st.container():
                    c_txt, c_btn = st.columns([0.88, 0.12])
                    with c_txt:
                        st.markdown(f"### [{regiao}] {nome}")
                        st.write(insight_texto)
                        st.caption(f"Fonte de extração: {fonte_origem}")
                    with c_btn:
                        st.write("")
                        if st.button("Remover", key=f"del_{item_id}", help="Deletar por UUID"):
                            with open(JSON_PATH, "r", encoding="utf-8") as f:
                                lista_atual = json.load(f)
                            lista_atual = [i for i in lista_atual if i.get('id') != item_id]
                            with open(JSON_PATH, "w", encoding="utf-8") as f:
                                json.dump(lista_atual, f, indent=4, ensure_ascii=False)
                            st.cache_data.clear()
                            st.rerun()
                    st.divider()
    else:
        st.info("Base de dados local sem registros. Acione o botão de sincronização na barra lateral.")

with col_assistente:
    st.title("Venture Insight - Copilot")
    st.write("Interface de inteligência conversacional orientada à análise de mercado.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if user_query := st.chat_input("Insira sua consulta de mercado ou tese regional:"):
        with st.chat_message("user"):
            st.write(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        resposta_ia = ""
        query_lower = user_query.lower()
        
        filtro_regiao = None
        if "brasil" in query_lower or "nacional" in query_lower:
            filtro_regiao = "Brasil"
        elif "global" in query_lower or "internacional" in query_lower or "mundo" in query_lower:
            filtro_regiao = "Global"
            
        foco_rio = "rio" in query_lower or "rj" in query_lower or "carioca" in query_lower

        for item in dados_salvos:
            if isinstance(item, dict):
                nome_empresa = item.get('nome', '').lower()
                if nome_empresa in query_lower and nome_empresa != "":
                    resposta_ia = f"Análise de Registro Local [{item.get('regiao')}]: Para o identificador **{item.get('nome')}**, a base registra:\n\n{item.get('insight')} (Fonte: {item.get('fonte', 'Mapeada')})"
                    break
        
        if not resposta_ia and any(p in query_lower for p in ["melhor", "investir", "recomendação", "destaque", "oportunidade", "notícias", "rio", "rj", "faperj"]):
            insights_importantes = []
            
            termos_chave = ["million", "billion", "raised", "funding", "seed", "series", 
                            "milhões", "bilhões", "aporte", "captou", "rodada", "investimento", 
                            "avaliação", "startup", "plataforma", "tecnologia", "tech", "inovação", "edital"]
            
            for item in dados_salvos:
                if isinstance(item, dict):
                    regiao_item = item.get('regiao', 'Global')
                    texto_completo = (item.get('nome', '') + " " + item.get('insight', '')).lower()
                    
                    if foco_rio:
                        if "rio" in texto_completo or "rj" in texto_completo or "carioca" in texto_completo or regiao_item == "Rio de Janeiro":
                            insights_importantes.append(item)
                    elif filtro_regiao and regiao_item == filtro_regiao:
                        if any(termo in texto_completo for termo in termos_chave):
                            insights_importantes.append(item)
                    elif not filtro_regiao:
                        if any(termo in texto_completo for termo in termos_chave):
                            insights_importantes.append(item)
            
            if not insights_importantes and dados_salvos and not foco_rio:
                insights_importantes = [d for d in dados_salvos if not filtro_regiao or d.get('regiao') == filtro_regiao]
            
            if insights_importantes:
                loc_titulo = " no ecossistema do Rio de Janeiro" if foco_rio else (f" no mercado {filtro_regiao}" if filtro_regiao else " consolidados")
                resposta_ia = f"Análise de Mercado Venture Insight: Com base nas movimentações estruturadas identificadas{loc_titulo}, destacam-se os seguintes ativos e relatórios:\n\n"
                
                for i, item in enumerate(insights_importantes[:3], 1):
                    regiao_exibida = item.get('regiao', 'Global')
                    resposta_ia += f"{i}. **{item.get('nome')}** (Origem: {regiao_exibida} | Fonte: {item.get('fonte', 'Mapeada')})\n   Análise Técnica: {item.get('insight')}\n\n"
                resposta_ia += "Recomendação Analítica: O direcionamento de capital ou fomento para estas verticais sinaliza tendências de consolidação regulatória ou mercadológica de curto prazo."
            
            elif foco_rio:
                resposta_ia = (
                    "Mapeamento Macroeconômico de Ecossistema - Rio de Janeiro:\n\n"
                    "Não há eventos de captação privada direta listados nas últimas 24 hours para o Rio de Janeiro, contudo, os fundamentos estruturais da região indicam:\n\n"
                    "1. Polos Tecnológicos Dinâmicos: O desenvolvimento de novos ativos está concentrado em distritos de inovação como o Porto Maravalley (integração corporativa e acadêmica via IMPA Tech) e o Parque Tecnológico da UFRJ, voltados à redução de fricção operacional e custos imobiliários transacionais.\n"
                    "2. Matriz de Fomento Não Dilutivo: A atuação da FAPERJ, por meio de subvenções como o edital HUB RJ STARTUP e programas de fomento à fixação de pesquisadores (Doutor Empreendedor), funciona como uma camada de pré-validação técnica de ativos altamente atraentes para fundos privados subsequentes.\n"
                    "3. Setores de Alta Densidade: Liderança histórica em Energytechs, Logtechs industriais e soluções B2B estruturadas para grandes corporações sediadas no estado."
                )
        
        if not resposta_ia:
            resposta_ia = "Instrução do Sistema: Os parâmetros solicitados encontram-se fora da base de dados ativa ou violam o escopo restrito do assistente. A plataforma não emite conselhos especulativos sobre ações de varejo, trading de curto prazo ou finanças pessoais. Atualize a captura de dados de Venture Capital e tente novamente."
            
        with st.chat_message("assistant"):
            st.write(resposta_ia)
        st.session_state.messages.append({"role": "assistant", "content": resposta_ia})