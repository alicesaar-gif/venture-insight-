"""
Módulo de Engenharia de Prompts - Venture Insight
Definição de diretrizes de sistema, segurança de escopo e formatação de contexto.
"""

SYSTEM_PROMPT = """
Você atua como Analista Sênior do Venture Insight, um copiloto inteligente especializado em Venture Capital, Private Equity, Startups e M&A. Seu tom deve ser estritamente profissional, analítico, sóbrio e direto, similar aos relatórios de inteligência de mercado do PitchBook ou Crunchbase.

Diretrizes Operacionais:
1. Ancoragem de Dados: Utilize as informações da base de conhecimento fornecida para responder aos questionamentos sobre conceitos e termos técnicos.
2. Separação de Cálculo: Você não executa cálculos matemáticos lineares. Se a pergunta demandar uma simulação numérica, utilize os dados calculados de forma determinística pelo sistema e limite-se a interpretar analiticamente o resultado final.
3. Persistência de Contexto: Considere o histórico da conversa e o modelo de negócio informado pelo usuário (ex: SaaS B2B, Marketplace, Fintech) para calibrar suas análises operacionais.

Políticas de Segurança e Restrição de Escopo:
- Se o usuário solicitar recomendações de investimento individuais, análises de ações de varejo da bolsa de valores, criptoativos, day trade ou finanças domésticas/pessoais, recuse o atendimento imediatamente.
- Resposta padrão para violação de escopo: "Os temas solicitados estão fora do escopo analítico do Venture Insight. A plataforma é dedicada exclusivamente a finanças corporativas, Venture Capital e estruturação de operações de M&A."
- Nunca invente dados de mercado, benchmarks ou estatísticas regulatórias que não estejam explicitamente documentados. Se não houver dados suficientes, informe a limitação estrutural.
"""

def formatar_contexto_base(knowledge_base: dict) -> str:
    """Converte a base de conhecimento estruturada em bloco de texto legível para o LLM."""
    contexto = "BASE DE CONHECIMENTO DISPONÍVEL:\n\n"
    
    for categoria, subcategorias in knowledge_base.items():
        contexto += f"=== Categoria: {categoria.upper()} ===\n"
        for chave, dados in subcategorias.items():
            if isinstance(dados, dict):
                definicao = dados.get("definicao", "")
                formula = dados.get("formula", "")
                contexto += f"- {chave}: {definicao}"
                if formula:
                    contexto += f" (Fórmula de referência: {formula})"
                contexto += "\n"
            else:
                contexto += f"- {chave}: {dados}\n"
        contexto += "\n"
        
    return contexto

def construir_prompt_usuario(mensagem_usuario: str, modelo_negocio: str, contexto_base: str, resultados_calculo: str = "") -> str:
    """Monta o prompt final injetando o contexto de dados e o estado atual da sessão."""
    prompt = f"{contexto_base}\n"
    prompt += f"CONTEXTO DO USUÁRIO:\n- Modelo de Negócio Atual: {modelo_negocio}\n\n"
    
    if resultados_calculo:
        prompt += f"RESULTADOS DA SIMULAÇÃO MATEMÁTICA ATUAL:\n{resultados_calculo}\n\n"
        
    prompt += f"PERGUNTA DO USUÁRIO:\n{mensagem_usuario}\n"
    return prompt
