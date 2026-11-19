import csv
from pathlib import Path
from threading import Lock

import streamlit as st

from main import carregar_assistente


CAMINHO_FEEDBACK = Path(__file__).resolve().parent / "data" / "feedback.csv"
OPCOES_FEEDBACK = ["Sim", "Não"]


@st.cache_resource
def trava_feedback():
    return Lock()


def registrar_feedback(chave: str, origem: str, id_orientacao: str) -> None:
    resposta = st.session_state[chave]
    if resposta not in OPCOES_FEEDBACK or chave in st.session_state.avaliacoes:
        return

    try:
        with trava_feedback(), CAMINHO_FEEDBACK.open("a", encoding="utf-8", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            if arquivo.tell() == 0:
                escritor.writerow(["origem", "id_orientacao", "ajudou"])
            escritor.writerow([origem, id_orientacao, resposta])
    except (OSError, csv.Error):
        st.session_state.erros_feedback.add(chave)
        st.session_state[chave] = None
        return

    st.session_state.avaliacoes[chave] = resposta
    st.session_state.erros_feedback.discard(chave)


def mostrar_feedback(rotulo: str, chave: str, origem: str, id_orientacao: str) -> None:
    avaliacao = st.session_state.avaliacoes.get(chave)
    st.radio(
        rotulo,
        OPCOES_FEEDBACK,
        index=None if avaliacao is None else OPCOES_FEEDBACK.index(avaliacao),
        horizontal=True,
        disabled=avaliacao is not None,
        key=chave,
        on_change=registrar_feedback,
        args=(chave, origem, id_orientacao),
    )
    if avaliacao is not None:
        st.caption("Obrigado pelo retorno. Avaliação registrada.")
    elif chave in st.session_state.erros_feedback:
        st.warning("Não foi possível registrar a avaliação. Tente novamente.")


st.set_page_config(
    page_title="Citizen Assist AI | Energia em casa",
    page_icon="🧭",
    layout="centered",
)

st.title("Como baixar a conta de luz?")
st.markdown("Pergunte sobre seus aparelhos, lâmpadas LED, energia solar, geradores ou descontos na conta.")
st.caption("Evite informar dados pessoais ou copiar a sua fatura.")
st.info("As respostas indicam as fontes e os limites das estimativas. Este assistente não é um canal oficial.")

try:
    assistente = carregar_assistente()
except (OSError, ValueError, KeyError, TypeError, ZeroDivisionError):
    st.error("Não foi possível abrir o catálogo ou calcular o cenário. Confira os arquivos da pasta data.")
    st.stop()

st.session_state.setdefault(
    "mensagens",
    [{"role": "assistant", "content": "Por onde você quer começar? Experimente perguntar “Meu chuveiro gasta muita energia?”."}],
)
st.session_state.setdefault("avaliacoes", {})
st.session_state.setdefault("erros_feedback", set())

with st.expander("Escolher uma orientação por categoria"):
    categoria = st.selectbox(
        "Categoria",
        assistente.base_conhecimento.listar_categorias(),
        index=None,
        placeholder="Selecione uma categoria",
        key="categoria_selecionada",
    )

    if categoria is not None:
        orientacoes = {}
        for orientacao in assistente.base_conhecimento.orientacoes:
            if orientacao.categoria == categoria:
                orientacoes[orientacao.titulo] = orientacao

        titulo = st.selectbox(
            "Orientação",
            list(orientacoes),
            index=None,
            placeholder="Selecione uma orientação",
            key="orientacao_" + categoria,
        )
        if titulo in orientacoes:
            orientacao = orientacoes[titulo]
            st.markdown(orientacao.exibir())
            mostrar_feedback("Esta orientação ajudou?", "feedback_menu_" + orientacao.id, "categoria", orientacao.id)

pergunta = st.chat_input("Escreva uma pergunta sobre energia", key="pergunta_chat")
mensagens = st.session_state.mensagens

if pergunta is not None:
    pergunta = pergunta.strip()
    if not pergunta:
        mensagens.append({"role": "assistant", "content": "Digite uma pergunta para continuar.", "aviso": True})
    elif not assistente.pergunta_valida(pergunta):
        mensagens.append({
            "role": "assistant",
            "content": "Por segurança, evite e-mails e oito ou mais algarismos. Envie uma pergunta sem esses dados.",
            "aviso": True,
        })
    else:
        resultados = assistente.base_conhecimento.buscar(pergunta)
        id_orientacao = ""
        if resultados and resultados[0][0] >= 3:
            id_orientacao = resultados[0][1].id

        mensagens.append({"role": "user", "content": pergunta})
        mensagens.append({
            "role": "assistant",
            "content": assistente.responder(pergunta),
            "id_orientacao": id_orientacao,
        })

for indice, mensagem in enumerate(mensagens):
    with st.chat_message(mensagem["role"]):
        if mensagem["role"] == "user":
            st.text(mensagem["content"])
        elif mensagem.get("aviso"):
            st.warning(mensagem["content"])
        else:
            st.markdown(mensagem["content"])
            if "id_orientacao" in mensagem:
                mostrar_feedback("Essa resposta ajudou?", f"feedback_chat_{indice}", "pergunta", mensagem["id_orientacao"])
