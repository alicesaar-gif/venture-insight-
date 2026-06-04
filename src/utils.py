import json


def carregar_base_conhecimento():

    with open(
        "data/knowledge_base.json",
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(arquivo)
