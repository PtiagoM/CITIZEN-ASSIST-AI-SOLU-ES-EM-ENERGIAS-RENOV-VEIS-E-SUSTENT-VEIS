import json
from pathlib import Path

from assistente import Assistente
from base_conhecimento import BaseConhecimento
from energia import calcular


def carregar_assistente() -> Assistente:
    pasta_dados = Path(__file__).resolve().parent / "data"
    base = BaseConhecimento(pasta_dados / "base_conhecimento.json")
    if not base.orientacoes:
        raise ValueError("A base de orientações está vazia.")

    with (pasta_dados / "cenario.json").open(encoding="utf-8") as arquivo:
        cenario = json.load(arquivo)

    valores = cenario | calcular(cenario)
    separadores = str.maketrans(",.", ".,")
    for chave, valor in valores.items():
        if isinstance(valor, float):
            valores[chave] = f"{valor:,.2f}".translate(separadores)

    for orientacao in base.orientacoes:
        orientacao.resposta = orientacao.resposta.format_map(valores)
    return Assistente(base)


def main() -> None:
    try:
        assistente = carregar_assistente()
    except (OSError, ValueError, KeyError, TypeError, ZeroDivisionError):
        print("Não foi possível abrir o catálogo ou calcular o cenário. Confira os arquivos da pasta data.")
        return

    print("Citizen Assist AI | Energia em casa")
    print("Quer gastar menos na conta de luz? Escolha um assunto ou escreva sua pergunta.")
    print("Evite enviar dados pessoais ou copiar a sua fatura.")
    opcoes = {}
    for numero, orientacao in enumerate(assistente.base_conhecimento.orientacoes, start=1):
        opcoes[str(numero)] = orientacao
        print(f"{numero}. {orientacao.titulo}")
    print("0. Sair")

    while True:
        try:
            pedido = input("\nNúmero do assunto ou pergunta (0 para sair): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return

        if pedido == "0":
            return
        if not pedido:
            print("Digite um número do menu ou uma pergunta curta.")
        elif pedido in opcoes:
            print("\n" + opcoes[pedido].exibir())
        elif pedido.isdecimal() and assistente.pergunta_valida(pedido):
            print("Esse número não está no menu. Escolha um dos assuntos exibidos.")
        else:
            print("\n" + assistente.responder(pedido))


if __name__ == "__main__":
    main()
