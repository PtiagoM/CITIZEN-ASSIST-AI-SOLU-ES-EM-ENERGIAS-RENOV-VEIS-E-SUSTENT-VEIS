# Representa como objeto Python uma orientação carregada do JSON.
class Orientacao:
    def __init__(self, dados: dict) -> None: # Recebe o dicionário e guarda seus campos no objeto.
        self.id = dados["id"]
        self.categoria = dados["categoria"]
        self.titulo = dados["titulo"]
        self.palavras_chave = dados["palavras_chave"]
        self.resposta = dados["resposta"]
        self.documentos = dados["documentos"]
        self.onde = dados["onde"]
        self.fonte = dados["fonte"]
        self.verificado_em = dados["verificado_em"]

    def exibir(self) -> str: # Monta e devolve o texto formatado da orientação.
        documentos = ""
        for documento in self.documentos: # Formata cada documento como um item de lista.
            if documentos:
                documentos += "\n"
            documentos += f"- {documento}"
        # Junta os campos em um único texto para quem chamou o método exibir.
        texto_exibido = self.titulo + "\n\n"
        texto_exibido += self.resposta + "\n\n"
        texto_exibido += "Documentos:\n" + documentos + "\n\n"
        texto_exibido += "Onde: " + self.onde + "\n"
        texto_exibido += "Fonte: " + self.fonte + "\n"
        texto_exibido += "Verificado em: " + self.verificado_em + "\n\n"
        texto_exibido += "Este assistente não é canal oficial."

        return texto_exibido
