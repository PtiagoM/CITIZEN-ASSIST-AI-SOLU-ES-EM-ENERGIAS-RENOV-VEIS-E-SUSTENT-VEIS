import csv
from importlib.util import find_spec
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory
import unittest


@unittest.skipUnless(find_spec("streamlit"), "Instale requirements.txt para testar a interface gráfica.")
class TestStreamlit(unittest.TestCase):
    def test_chat_menu_e_feedback_anonimo(self):
        from streamlit.testing.v1 import AppTest

        origem = Path(__file__).resolve().parents[1] / "streamlit_app.py"
        with TemporaryDirectory() as temporaria:
            pasta = Path(temporaria)
            (pasta / "data").mkdir()
            app = pasta / origem.name
            copyfile(origem, app)
            pagina = AppTest.from_file(str(app), default_timeout=30).run()
            self.assertEqual(pagina.title[0].value, "Como baixar a conta de luz?")
            self.assertFalse(pagina.exception)

            pagina.selectbox[0].select("Decisão e benefícios").run()
            pagina.selectbox[1].select("Comparar lâmpadas LED e energia solar").run()
            self.assertTrue(any("R$ 118,41" in texto.value for texto in pagina.markdown))
            pagina.radio(key="feedback_menu_E04").set_value("Sim").run()
            self.assertTrue(pagina.radio(key="feedback_menu_E04").proto.disabled)

            chat = pagina.chat_input(key="pergunta_chat")
            chat.set_value("Posso instalar placas solares?").run()
            textos = [texto.value for texto in pagina.markdown]
            self.assertIn("167,69 kWh", "\n".join(textos))
            pagina.radio(key="feedback_chat_2").set_value("Não").run()

            pagina.chat_input(key="pergunta_chat").set_value("exemplo@test.invalid").run()
            self.assertIn("Por segurança", pagina.warning[0].value)
            self.assertEqual(len(pagina.text), 1)
            pagina.run()
            self.assertFalse(pagina.exception)

            pagina.selectbox[0].select("Consumo e eficiência").run()
            pagina.selectbox[1].select("Reduzir o gasto do chuveiro elétrico").run()
            self.assertTrue(any("13,75 kWh" in texto.value for texto in pagina.markdown))
            pagina.chat_input(key="pergunta_chat").set_value("Gerador a gasolina vale a pena?").run()
            self.assertTrue(any("R$ 3,60 por kWh" in texto.value for texto in pagina.markdown))
            self.assertFalse(pagina.exception)

            with (pasta / "data" / "feedback.csv").open(encoding="utf-8", newline="") as arquivo:
                self.assertEqual(list(csv.reader(arquivo)), [
                    ["origem", "id_orientacao", "ajudou"],
                    ["categoria", "E04", "Sim"],
                    ["pergunta", "E03", "Não"],
                ])
