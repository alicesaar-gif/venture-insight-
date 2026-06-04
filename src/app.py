import streamlit as st

from utils import carregar_base_conhecimento
from prompts import (
    SYSTEM_PROMPT,
    formatar_contexto_base,
    construir_prompt_usuario
)

from llm_service import gerar_resposta
