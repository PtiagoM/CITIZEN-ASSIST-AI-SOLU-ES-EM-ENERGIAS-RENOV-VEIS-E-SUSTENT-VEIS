import json
from pathlib import Path
import unittest

from energia import calcular
from main import carregar_assistente


class TestEnergia(unittest.TestCase):
    def setUp(self):
        arquivo = Path(__file__).resolve().parents[1] / "data" / "cenario.json"
        self.cenario = json.loads(arquivo.read_text(encoding="utf-8"))

    def test_led(self):
        resultado = calcular(self.cenario)
        self.assertAlmostEqual(resultado["consumo_antigas"], 36)
        self.assertAlmostEqual(resultado["consumo_led"], 5.4)
        self.assertAlmostEqual(resultado["consumo_casa_led"], 149.4)
        self.assertAlmostEqual(resultado["economia_led_rs"], 24.155028)

    def test_exemplos_de_chuveiro_e_gerador(self):
        resultado = calcular(self.cenario)
        self.assertAlmostEqual(resultado["economia_chuveiro_kwh"], 13.75)
        self.assertAlmostEqual(resultado["economia_chuveiro_rs"], 10.853975)
        self.assertAlmostEqual(resultado["gerador_custo_combustivel_kwh"], 3.60)

    def test_solar_com_e_sem_credito_restante(self):
        resultado = calcular(self.cenario)
        self.assertAlmostEqual(resultado["geracao_solar"], 167.688)
        self.assertAlmostEqual(resultado["uso_direto"] + resultado["injecao"], 167.688)
        self.assertAlmostEqual(resultado["uso_direto"] + resultado["importacao"], 180)
        self.assertAlmostEqual(resultado["custo_solar"], 23.6814)
        self.assertAlmostEqual(resultado["economia_solar_rs"], 118.407)
        self.assertGreater(resultado["credito_restante"], 0)

        menos_sol = self.cenario | {"solar_irradiacao_wh_m2_dia": 4090}
        resultado = calcular(menos_sol)
        self.assertGreater(resultado["custo_solar"], resultado["custo_minimo"])
        self.assertAlmostEqual(resultado["credito_restante"], 0)


class TestAssistente(unittest.TestCase):
    def setUp(self):
        self.assistente = carregar_assistente()

    def test_perguntas_abrem_o_assunto_e_mostram_os_resultados(self):
        casos = [
            ("O que é kWh na fatura?", "E01", "180 kWh"),
            ("Como trocar lâmpadas por LED?", "E02", "R$ 24,16"),
            ("Posso instalar placas solares?", "E03", "167,69 kWh"),
            ("Quero comparar LED e energia solar", "E04", "R$ 118,41"),
            ("LED ou placa solar?", "E04", "30,60 kWh"),
            ("O que é melhor, lâmpadas de LED ou placas solares?", "E04", "30,60 kWh"),
            ("Tenho direito ao desconto na conta de luz?", "A19", "80 kWh"),
            ("Como baixar a conta de luz?", "E05", "kWh por dia"),
            ("Como reduzir minha conta de luz?", "E05", "kWh por dia"),
            ("Minha conta de luz está muito alta", "E05", "kWh por dia"),
            ("Quero economizar com meu chuveiro elétrico", "E06", "13,75 kWh"),
            ("Como economizar energia com a geladeira?", "E07", "kWh por mês"),
            ("Qual ar-condicionado gasta menos?", "E08", "kWh por ano"),
            ("Gerador a gasolina compensa para baixar a conta de luz?", "E09", "R$ 3,60 por kWh"),
            ("Gerador ou placa solar para economizar energia?", "E09", "Monóxido de carbono"),
            ("Gerador solar vale a pena?", "E09", "bateria armazena energia"),
        ]
        for pergunta, id_esperado, trecho in casos:
            with self.subTest(pergunta=pergunta):
                pontos, orientacao = self.assistente.base_conhecimento.buscar(pergunta)[0]
                self.assertGreaterEqual(pontos, 3)
                self.assertEqual(orientacao.id, id_esperado)
                resposta = self.assistente.responder(pergunta)
                self.assertIn(trecho, resposta)
                self.assertIn("https://", resposta)
                self.assertNotIn("{", resposta)

    def test_variacoes_de_pergunta_abrem_a_orientacao_sem_empate(self):
        perguntas_por_assunto = {
            "E01": [
                "Onde fica a leitura do medidor na fatura?",
                "Entender o consumo da conta de luz",
                "O que significa quilowatt-hora?",
                "A bandeira explica a cobrança da minha fatura?",
            ],
            "E02": [
                "LED de mais lúmens gasta menos?",
                "Como escolho o brilho de uma lâmpada?",
                "Ainda tenho incandescentes no corredor",
                "O soquete serve para LED?",
            ],
            "E03": [
                "Meu telhado serve para painéis fotovoltaicos?",
                "Como funcionam os créditos da energia solar?",
                "O que é o Fio B na geração?",
                "Será que posso pôr placas solares no telhado?",
            ],
            "E04": [
                "Compare LED e solar para a minha casa",
                "Solar ou LED?",
                "LED versus energia solar",
                "Lâmpadas ou painéis solares, qual compensa?",
            ],
            "A19": [
                "CadÚnico dá direito à tarifa social?",
                "Quem tem BPC pode conseguir desconto?",
                "O que é o Luz do Povo?",
                "Família de baixa renda pode ter gratuidade?",
            ],
            "E05": [
                "Como faço para gastar menos com eletricidade?",
                "Minha conta de energia veio alta",
                "Quais eletrodomésticos devo olhar primeiro?",
                "Como economizar energia e reduzir o desperdício?",
            ],
            "E06": [
                "Quanto gasto num banho quente de dez minutos?",
                "Dá para gastar menos usando a ducha por menos tempo?",
                "Meu chuveiro pesa muito na conta de luz",
                "Se eu encurtar os banhos, economizo quanto?",
            ],
            "E07": [
                "Vale trocar meu refrigerador?",
                "Onde vejo o gasto em kWh do freezer?",
                "A vedação da geladeira influencia o consumo?",
                "Uma geladeira frost free gasta muito?",
            ],
            "E08": [
                "Como comparar dois modelos de ar-condicionado?",
                "Meu split aumenta a conta de energia?",
                "Comparo o consumo de aparelhos de 9000 BTUs como?",
                "Qual a diferença no gasto do ar inverter?",
            ],
            "E09": [
                "Quanto custa o combustível para um gerador?",
                "Gerador ou painel solar como reserva?",
                "Dá para usar gasolina em um gerador em caso de apagão?",
                "Geradores a diesel baixam a fatura?",
            ],
        }
        for assunto, perguntas in perguntas_por_assunto.items():
            for pergunta in perguntas:
                with self.subTest(pergunta=pergunta):
                    resultados = self.assistente.base_conhecimento.buscar(pergunta)
                    self.assertTrue(resultados)
                    pontos, orientacao = resultados[0]
                    self.assertEqual(orientacao.id, assunto)
                    self.assertGreaterEqual(pontos, 3)
                    if len(resultados) > 1:
                        self.assertGreater(pontos, resultados[1][0])


    def test_protecao_de_dados_e_falta_de_resultado(self):
        for pergunta in ["exemplo@test.invalid", "1234-5678"]:
            self.assertIn("Por segurança", self.assistente.responder(pergunta))
        self.assertIn("confiança suficiente", self.assistente.responder("Receita de bolo"))
