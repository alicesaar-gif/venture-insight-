"""
Módulo Core Finance - Venture Insight
Engine matemática determinística para simulações de Venture Capital e M&A.
"""

def calcular_burn_rate(gastos_totais: float, receita_operacional: float) -> float:
    """Calcula a queima de caixa mensal (Burn Rate)."""
    return max(0.0, gastos_totais - receita_operacional)


def calcular_runway(caixa_atual: float, burn_rate: float) -> float:
    """
    Calcula o tempo de sobrevida do caixa em meses (Runway).
    Retorna float('inf') se o burn rate for zero ou negativo (empresa autossustentável).
    """
    if burn_rate <= 0:
        return float('inf')
    return max(0.0, caixa_atual / burn_rate)


def calcular_cac(investimento_marketing_vendas: float, novos_clientes: int) -> float:
    """Calcula o Custo de Aquisição de Cliente (CAC)."""
    if novos_clientes <= 0:
        raise ValueError("O número de novos clientes deve ser maior que zero.")
    return max(0.0, investimento_marketing_vendas / novos_clientes)


def calcular_ltv(ticket_medio: float, recorrencia_anual: float, lifespan_anos: float) -> float:
    """Calcula o Lifetime Value (LTV) bruto estimado do cliente."""
    return max(0.0, ticket_medio * recorrencia_anual * lifespan_anos)


def calcular_ltv_cac(ltv: float, cac: float) -> float:
    """Calcula a relação de eficiência LTV/CAC."""
    if cac <= 0:
        return 0.0
    return max(0.0, ltv / cac)


def simular_rodada_investimento(pre_money_valuation: float, aporte: float) -> dict:
    """
    Simula os impactos patrimoniais de uma rodada de investimento primária.
    Retorna um dicionário com Post-Money Valuation e a diluição percentual gerada.
    """
    if pre_money_valuation <= 0 or aporte <= 0:
        raise ValueError("Valuation e Aporte devem ser maiores que zero.")
        
    post_money_valuation = pre_money_valuation + aporte
    participacao_investidor = aporte / post_money_valuation
    participacao_original_pos_diluicao = pre_money_valuation / post_money_valuation
    
    return {
        "post_money_valuation": post_money_valuation,
        "participacao_investidor_percentual": participacao_investidor * 100,
        "diluicao_sócios_atuais_percentual": (1 - participacao_original_pos_diluicao) * 100
    }
