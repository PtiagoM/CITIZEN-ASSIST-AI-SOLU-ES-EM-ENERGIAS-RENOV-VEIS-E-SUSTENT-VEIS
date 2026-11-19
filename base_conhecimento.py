import json
import re
import unicodedata
from pathlib import Path

from orientacao import Orientacao


class BaseConhecimento:
    def __init__(self, caminho_arquivo: Path) -> None:
        self.orientacoes: list[Orientacao] = [] # Lista que guardará os objetos Orientacao carregados do JSON.
        self.carregar(caminho_arquivo)

    def carregar(self, caminho_arquivo: Path) -> None: # Lê o JSON e cria um objeto Orientacao para cada registro.
        self.orientacoes = []

        try:
            with caminho_arquivo.open(encoding="utf-8") as arquivo: # "as arquivo" dá um nome ao arquivo aberto para usá-lo no bloco.
                registros = json.load(arquivo) # Converte o conteúdo JSON em objetos Python.

            if isinstance(registros, list): # Confere se o conteúdo principal do JSON é uma lista.
                for registro in registros:
                    orientacao = Orientacao(registro) # registro é o dicionário atual; Orientacao cria o objeto correspondente.
                    self.orientacoes.append(orientacao) # Guarda a referência do objeto na lista desta instância.
        except (
            OSError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
        ): # Se a leitura ou conversão falhar, deixa a lista vazia.
            self.orientacoes = []

    def listar_categorias(self) -> list[str]: # Devolve uma lista com as categorias presentes na base.
        categorias = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in categorias: # Evita adicionar a mesma categoria mais de uma vez.
                categorias.append(orientacao.categoria) # Guarda a categoria ainda não listada.

        categorias.sort() # Ordena as categorias em ordem crescente pelo texto.
        return categorias

    @staticmethod # Não recebe self; a normalização só depende do texto recebido.
    def _normalizar(texto: str) -> str:
        texto = unicodedata.normalize("NFD", texto.casefold()) # Põe em minúsculas e separa os acentos das letras.
        texto_sem_acentos = ""
        for caractere in texto: # Percorre cada letra e sinal do texto normalizado.
            if not unicodedata.combining(caractere): # Ignora os sinais de acento separados acima.
                texto_sem_acentos += caractere

        texto_sem_pontuacao = re.sub(r"[^a-z0-9\s]", " ", texto_sem_acentos)
        palavras = texto_sem_pontuacao.split()

        texto_normalizado = ""
        for palavra in palavras:
            if texto_normalizado:
                texto_normalizado += " "
            texto_normalizado += palavra

        return texto_normalizado

    def buscar(self, pergunta: str) -> list[tuple[int, Orientacao]]: # Devolve pares com pontuação e orientação.
        pergunta_normalizada = self._normalizar(pergunta) # Prepara a pergunta para comparar palavras-chave e título.
        palavras_pergunta = pergunta_normalizada.split() # Divide a pergunta em palavras usando os espaços.
        palavras_pergunta_unicas = []
        for palavra in palavras_pergunta: # Percorre as palavras para manter apenas uma ocorrência de cada.
            if palavra not in palavras_pergunta_unicas:
                palavras_pergunta_unicas.append(palavra)

        resultados = []

        for orientacao in self.orientacoes:
            titulo = self._normalizar(orientacao.titulo)
            palavras_titulo = titulo.split()
            pontos = 0

            for palavra_chave in orientacao.palavras_chave:
                palavra_normalizada = self._normalizar(palavra_chave)
                if palavra_normalizada and f" {palavra_normalizada} " in f" {pergunta_normalizada} ":
                    pontos += 3

            for palavra in palavras_pergunta_unicas: # Percorre cada palavra única da pergunta.
                if len(palavra) >= 4 and palavra in palavras_titulo: # +1 por palavra única da pergunta com 4+ letras presente no título.
                    pontos += 1

            if pontos:
                resultados.append((pontos, orientacao))

        resultados.sort(key=self._pontuacao_do_resultado, reverse=True) # Ordena pela pontuação, da maior para a menor.
        return resultados

    @staticmethod
    def _pontuacao_do_resultado(resultado: tuple[int, Orientacao]) -> int:
        return resultado[0]
