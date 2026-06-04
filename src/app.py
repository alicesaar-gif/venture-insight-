import streamlit as st
import json
import os

# Caminho para o seu arquivo de dados
JSON_PATH = os.path.join("data", "knowledge_base.json")

# Função para carregar os dados salvos
@st.cache_data
def load_knowledge():
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Se o arquivo existir mas estiver vazio ou corrompido, retorna uma lista vazia
            return []
    return []

# Carrega os dados na inicialização do app
dados_salvos = load_knowledge()

# --- INTERFACE DO USUÁRIO ---
st.title("💡 Venture Insight")
st.write("Bem-vindo ao seu painel de inteligência de mercado.")

# 1. FORMULÁRIO DE INPUT (Onde você perguntou!)
with st.expander("➕ Adicionar Novo Insight / Startup"):
    with st.form("new_insight"):
        name = st.text_input("Nome da Empresa/Setor")
        insight = st.text_area("Insight de Mercado")
        submitted = st.form_submit_with_button("Salvar no Sistema")
        
        if submitted:
            if name and insight:  # Garante que os campos não estão vazios
                
                # LÓGICA REAL PARA SALVAR NO JSON:
                # 1. Ler o que já existe no arquivo (sem usar cache)
                if os.path.exists(JSON_PATH):
                    try:
                        with open(JSON_PATH, "r", encoding="utf-8") as f:
                            lista_atual = json.load(f)
                    except json.JSONDecodeError:
                        lista_atual = []
                else:
                    lista_atual = []

                # Garante que o arquivo é uma lista
                if not isinstance(lista_atual, list):
                    lista_atual = []

                # 2. Criar o novo dicionário com os dados do formulário
                novo_item = {
                    "nome": name,
                    "insight": insight
                }
                
                # 3. Adicionar o novo item à lista existente
                lista_atual.append(novo_item)
                
                # 4. Salvar a lista atualizada de volta no JSON
                with open(JSON_PATH, "w", encoding="utf-8") as f:
                    json.dump(lista_atual, f, indent=4, ensure_ascii=False)
                
                # 5. Limpar o cache do Streamlit para forçar o app a ler o arquivo atualizado
                st.cache_data.clear()
                
                st.success(f"Insight sobre '{name}' salvo com sucesso!")
                st.rerun()  # Recarrega a página para exibir o novo dado imediatamente
            else:
                st.error("Por favor, preencha todos os campos antes de salvar.")

# --- VISUALIZAÇÃO DOS DADOS ---
st.divider()
st.subheader("📊 Insights Cadastrados")

if dados_salvos:
    # Exibe cada insight salvo no JSON em um formato de "card"
    for item in dados_salvos:
        with st.container():
            st.markdown(f"### 🏢 {item.get('nome')}")
            st.write(item.get('insight'))
            st.caption("---")
else:
    st.info("Nenhum insight cadastrado ainda. Use o formulário acima para começar!")
