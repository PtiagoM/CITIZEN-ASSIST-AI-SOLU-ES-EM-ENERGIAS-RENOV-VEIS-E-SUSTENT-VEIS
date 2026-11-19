from base_conhecimento import BaseConhecimento


class Assistente:
    def __init__(self, base_conhecimento: BaseConhecimento) -> None:
        self.base_conhecimento = base_conhecimento

    @staticmethod
    def pergunta_valida(pergunta: str) -> bool:
        quantidade_digitos = 0
        for caractere in pergunta:
            if caractere.isdigit():
                quantidade_digitos += 1

        if "@" in pergunta:
            return False
        if quantidade_digitos >= 8:
            return False
        return True

    def responder(self, pergunta: str) -> str:
        if not self.pergunta_valida(pergunta):
            return "Por segurança, não envie e-mail nem informe 8 ou mais algarismos no total, mesmo separados. Faça outra pergunta sem esses dados."

        resultados = self.base_conhecimento.buscar(pergunta)

        if len(resultados) == 0 or resultados[0][0] < 3:
            resposta = "Não encontrei uma orientação com confiança suficiente. Tente perguntar com outras palavras."
            resposta += "\nOu escolha um assunto no menu."
            return resposta.rstrip()

        melhor_resultado = resultados[0]
        pontos = melhor_resultado[0]
        orientacao = melhor_resultado[1]

        if pontos >= 6:
            confianca = "alta"
        else:
            confianca = "média"

        resposta = "Encontrei uma orientação com confiança " + confianca
        resposta += " (" + str(pontos) + " pontos).\n\n"
        resposta += orientacao.exibir()

        alternativas = []
        indice = 1
        while indice < len(resultados) and len(alternativas) < 2 and resultados[indice][0] >= 3:
            alternativas.append(resultados[indice])
            indice += 1

        if len(alternativas) > 0:
            resposta += "\n\nOutras orientações que também podem ajudar:\n"
            for alternativa in alternativas:
                pontos_alternativa = alternativa[0]
                orientacao_alternativa = alternativa[1]
                resposta += "- " + str(pontos_alternativa) + ": "
                resposta += orientacao_alternativa.titulo + "\n"

        return resposta.rstrip()
