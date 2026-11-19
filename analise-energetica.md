# Análise energética residencial

O cenário atende à seção **Requisitos técnicos mínimos** do enunciado de Energias Renováveis, p. 2. O desafio e a exigência de integrar a análise ao assistente estão na p. 1.

## 1. Necessidade e condições comuns

Consumidores residenciais precisam entender o que aumentou na conta de luz e decidir como gastar menos com eletricidade. A EPE identifica a conservação de alimentos, a climatização e o aquecimento de água entre os principais usos finais da eletricidade residencial no Brasil. Por isso, o assistente orienta sobre fatura, hábitos, aparelhos e alternativas de fornecimento. O público é qualquer pessoa que queira reduzir a conta de energia doméstica. [EPE, Atlas da Eficiência Energética 2024, setor residencial](https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-857/Atlas%20da%20Efici%C3%AAncia%20Energ%C3%A9tica%20Brasil%202024.pdf)

As duas alternativas principais avaliam **a redução da parcela tarifária da mesma casa, em 30 dias, com o mesmo nível de iluminação e uso dos demais aparelhos**. Usa-se uma residência hipotética em São Paulo (SP), com ligação monofásica e tarifa B1 convencional, sem benefício tarifário. São cinco pontos de luz com cerca de 800 lúmens cada, usados quatro horas por dia. Os demais usos somam 144 kWh. O LED reduz a energia necessária para iluminar. O solar mantém o consumo e fornece parte da energia usada. Cada alternativa é aplicada separadamente ao mesmo cenário. O endereço e o consumo representam as premissas do estudo, e os moradores adaptam a orientação com seus próprios dados.

## 2. Dados, unidades e premissas

| Entrada | Valor | Origem e justificativa |
| --- | ---: | --- |
| Período e consumo total inicial | 30 dias e 180 kWh | Cenário estimado. A ordem de grandeza é próxima de 178,4 kWh/mês por consumidor residencial no Brasil em dezembro de 2025, segundo a EPE. Esse valor nacional serve apenas de referência. [EPE, boletim nº 24, Figura 5](https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-483/topico-769/Boletim%20Trimestral%20de%20Consumo%20de%20Eletricidade%20ANO%20VI%20-%20N%C2%BA24.pdf) |
| Lâmpadas e uso | 5 lâmpadas × 4 h/dia | Estimativa de cinco pontos de uso regular em uma casa que ainda tem incandescentes. As horas equivalentes podem incluir usos em horários diferentes. |
| Potência e fluxo luminoso | Incandescente de 60 W e LED de 9 W, ambas com cerca de 800 lm | A potência indica a taxa de uso da energia. Os lúmens indicam a luz emitida. A comparação usa equivalência aproximada de brilho. O registro consultado inclui um LED de 9 W e 803 lm. [Signify, referência incandescente](https://www.assets.signify.com/is/content/PhilipsConsumer/PDFDownloads/United%20States/ODLI20160307_001-UPD-en_US_GR-1580BN-Basic_Bulb_with_Glass_TLED_Print.pdf) · [Inmetro, registro 001887/2024](https://registro.inmetro.gov.br/consulta/detalhe.aspx?NumeroRegistro=001887/2024&pag=1) |
| Custo unitário de LED | R$ 10,00 | Estimativa arredondada para compra avulsa, sem adaptação de luminária. Como referência de ordem de grandeza, o planejamento de Capão Bonito estimou R$ 8,55 por bulbo LED de 9 W em lote. [Prefeitura de Capão Bonito, PCA 2026, p. 330](https://licitacao.capaobonito.sp.gov.br/wp-content/uploads/2025/08/PCA-2026.pdf) |
| Tarifa convencional B1 | TE de R$ 0,31696/kWh + TUSD de R$ 0,47242/kWh | Dados publicados pela Enel SP, REH ANEEL 3.596/2026, aplicável a partir de 04/07/2026. A conversão de R$/MWh para R$/kWh divide os valores publicados por 1.000. A tarifa total é R$ 0,78938/kWh antes de tributos e bandeiras. [Enel SP, tabela B1](https://www.enel.com.br/pt-saopaulo/Para_Voce/tarifa-energia-eletrica.html) |
| Recurso solar | 4.658 Wh/m²/dia em média anual | Atlas do INPE, plano inclinado na latitude, célula 5622 (longitude −46,649°, latitude −23,6005°). Para ciclos padronizados de 30 dias, o menor e o maior valor mensal da célula são 4.090 em junho e 5.217 Wh/m²/dia em fevereiro. A célula representa a região e a posição real dos módulos precisa ser avaliada. [INPE/LABREN, Atlas, 2ª ed.](https://labren.ccst.inpe.br/atlas2_tables/SP_inc.html) |
| Potência solar e desempenho | 1,5 kWp e fator 0,80 | Estimativa dimensionada para gerar perto de 180 kWh no mês de referência. O fator agrega perdas de temperatura, sujeira, cabos, inversor e outras perdas. A referência NREL explica que perdas do sistema e conversão do inversor influenciam a geração. [NREL, manual PVWatts v5, seção System Losses](https://docs.nrel.gov/docs/fy14osti/62641.pdf) |
| Custo solar instalado | R$ 6.500,00 | Estimativa para módulos, inversor, estrutura, proteções, projeto e instalação, sem bateria ou reforço de telhado. A referência de escala é R$ 7.240 para 2 kWp em junho de 2026 (2.000 Wp × R$ 3,62/Wp). Adota-se um valor próximo pela parcela fixa da mão de obra, do projeto e da instalação. [Greener, Estudo Estratégico de Geração Distribuída 2S 2026, p. 46](https://greenerstorage.blob.core.windows.net/public/estudos/SED_2S_2026.pdf) |
| Uso direto de energia solar | 60 kWh no mês | Hipótese de 2 kWh/dia usados enquanto os painéis geram, por exemplo com geladeira e outros aparelhos em funcionamento de dia. O restante da geração vai para a rede. O cruzamento de geração e carga só pode ser medido ou estimado com dados horários reais. |
| Cobrança mínima e compensação | Piso de 30 kWh equivalentes e 60% do Fio B | Ligação monofásica e nova microgeração local enquadrada na transição do art. 27 em 2026. Para a simulação, usa-se valor arredondado **estimado** de R$ 0,21/kWh para o Fio B, logo R$ 0,126 por kWh compensado. Sem créditos de meses anteriores. [ANEEL, microgeração](https://www.gov.br/aneel/pt-br/assuntos/geracao-distribuida/) · [Lei 14.300, arts. 16 e 27](https://www.presidencia.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14300.htm) · [REN ANEEL 1.059/2023, art. 655-I incorporado à REN 1.000/2021](https://www2.aneel.gov.br/cedoc/ren20231059.pdf) |

Fontes consultadas em **17/11/2026**. Os valores calculáveis estão em [data/cenario.json](data/cenario.json) e são processados por [energia.py](energia.py).

## 3. Cálculos

### Referência sem intervenção

- Energia das lâmpadas. `5 × 60 W × 4 h/dia × 30 dias ÷ 1.000 = 36,00 kWh`.
- Consumo total. `36,00 + 144,00 = 180,00 kWh`.
- Parcela tarifária. `180,00 × R$ 0,78938 ≈ R$ 142,09`.

### Alternativa A — LED

- Potência total de iluminação. Cai de `5 × 60 W = 300 W` para `5 × 9 W = 45 W`, com brilho por lâmpada semelhante.
- Novo consumo de iluminação. `45 W × 4 h/dia × 30 dias ÷ 1.000 = 5,40 kWh`.
- Consumo da casa. `144 + 5,40 = 149,40 kWh`.
- Economia. `180 − 149,40 = 30,60 kWh`, 85% da energia das lâmpadas e 17% da energia total. `30,60 × R$ 0,78938 ≈ R$ 24,16`.
- Investimento e retorno simples. `5 × R$ 10 = R$ 50` e `R$ 50 ÷ R$ 24,155028/mês ≈ 2,1 meses` com uso e tarifa constantes.

### Alternativa B — solar fotovoltaica

- Horas de sol pleno. `4.658 Wh/m²/dia ÷ 1.000 W/m² = 4,658 h/dia`. Esse valor é a irradiação diária expressa em horas equivalentes a 1.000 W/m².
- Geração. `1,5 kWp × 4,658 h/dia × 30 dias × 0,80 ≈ 167,69 kWh`.
- Balanço. A casa continua usando 180 kWh, dos quais 60 kWh são usados diretamente da geração. Ela retira `180 − 60 = 120 kWh` da rede e injeta `167,688 − 60 = 107,688 kWh`.
- Compensação. Cada kWh compensado diminui a parcela modelada em `0,78938 − (0,60 × 0,21) = R$ 0,66338`. O piso é `30 × R$ 0,78938 ≈ R$ 23,68`. Antes da compensação, os 120 kWh da rede custam R$ 94,7256. Logo, a quantidade compensável no mês é o menor valor entre a injeção, o consumo da rede e o limite do piso: `(94,7256 − 23,6814) ÷ 0,66338 ≈ 107,09 kWh`. Sobram aproximadamente 0,59 kWh para crédito.
- Economia na parcela modelada. `R$ 142,0884 − R$ 23,6814 ≈ R$ 118,41`. Os créditos restantes não foram tratados como dinheiro. O retorno simples com as condições do mês repetidas por 12 meses a cada ano é `R$ 6.500 ÷ (12 × R$ 118,407) ≈ 4,6 anos`.

## 4. Comparação, viabilidade e impacto

| Critério, 30 dias | Referência | LED | Solar |
| --- | ---: | ---: | ---: |
| Brilho por ponto | ≈ 800 lm | ≈ 800 lm | ≈ 800 lm |
| Consumo total da casa | 180,00 kWh | 149,40 kWh | 180,00 kWh |
| Energia fisicamente retirada da rede | 180,00 kWh | 149,40 kWh | 120,00 kWh |
| Geração local / enviada à rede | 0 / 0 kWh | 0 / 0 kWh | 167,69 / 107,69 kWh |
| Investimento inicial estimado | R$ 0,00 | R$ 50,00 | R$ 6.500,00 |
| Parcela tarifária modelada | R$ 142,09 | R$ 117,93 | R$ 23,68 |
| Economia estimada | R$ 0,00 | R$ 24,16 | R$ 118,41 |

- **LED.** A troca em etapas facilita a compra para famílias com orçamento limitado. É preciso verificar encaixe, tensão e iluminação suficiente, especialmente em escadas e corredores. A redução de 30,60 kWh evita demanda da rede no período. A fabricação também usa materiais e as lâmpadas usadas precisam de descarte conforme a orientação municipal. [Prefeitura de São Paulo, descarte de resíduos especiais](https://prefeitura.sp.gov.br/web/saude/w/vigilancia_em_saude/saude_ambiental/353036)
- **Solar.** Gera eletricidade renovável no telhado e pode reduzir a energia que a casa retira da rede, com excedente injetado. A instalação exige espaço, estrutura em boas condições, avaliação de sombra e orientação, autorização do proprietário quando for o caso e conexão pela distribuidora. Os módulos e o inversor têm impactos de fabricação, transporte e destinação. A redução efetiva de emissões depende do sistema elétrico, do equipamento e da operação. A conta não converte créditos em redução de CO₂. [ANEEL, condições de adesão](https://www.gov.br/aneel/pt-br/assuntos/geracao-distribuida/) · [IEA PVPS, avaliação de ciclo de vida](https://iea-pvps.org/fact-sheets/fact-sheet-environmental-life-cycle-assessment-of-electricity-from-pv-systems/)
- **Decisão.** Priorizar LED nos pontos mais usados quando ainda houver lâmpadas antigas, devido ao investimento reduzido. Antes de estudar solar, verificar o consumo de 12 meses, reduzir desperdícios, consultar os benefícios aplicáveis e pedir propostas que mostrem geração, instalação, garantias e custo total. Se a casa instalar LED e solar, refazer o dimensionamento com o novo perfil. Somar as duas economias diretamente pode contar duas vezes a mesma energia. [MME, Luz do Povo](https://www.gov.br/mme/pt-br/luzdopovo/luzdopovo)

### Sensibilidade e limitações

| Variação isolada no cenário | Consequência |
| --- | --- |
| 2 h de iluminação por dia | LED poupa 15,30 kWh e R$ 12,08 no mês. Retorno simples de aproximadamente 4,1 meses. |
| Irradiação média de junho, com ciclo de 30 dias | Solar gera 147,24 kWh, resta uma parcela modelada de R$ 36,85 e a estimativa de economia cai para R$ 105,24. |
| Irradiação média de fevereiro, com ciclo padronizado de 30 dias | Solar gera 187,81 kWh. A parcela modelada permanece em R$ 23,68 e o saldo para crédito aumenta para 20,72 kWh. |
| Piso de 50 kWh equivalentes, com as outras hipóteses iguais | Parcela solar de R$ 39,47 e economia estimada de R$ 102,62 no mês. |

O mês de referência usa a irradiação média anual diária. A análise financeira exclui tributos, bandeiras, contribuição de iluminação pública, descontos sociais, juros, manutenção, troca de inversor, degradação e tarifas futuras. O prazo simples do cenário serve como comparação inicial. O art. 27 muda os percentuais depois de 2026, então um orçamento real requer projeção mensal e verificação com a distribuidora. [Lei 14.300, art. 27](https://www.presidencia.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14300.htm)

## 5. Aplicar a análise no dia a dia

- **Conta de luz.** Dividir os kWh faturados pelos dias do período ajuda a comparar contas com durações diferentes. Se o consumo por dia subir, investigar o tempo de uso e a potência dos aparelhos. Se o consumo por dia ficar parecido, conferir tarifa, bandeira e itens adicionais. [MME, potência e consumo](https://www.gov.br/mme/pt-br/assuntos/noticias/julho-26/potencia-e-consumo-de-energia-o-que-sao-e-como-impactam-na-conta-de-luz) · [ANEEL, ranking das tarifas](https://www.gov.br/aneel/pt-br/assuntos/tarifas/ranking-das-tarifas)
- **Chuveiro.** Exemplo complementar e estimado com chuveiro operando a 5.500 W e redução de cinco minutos de uso diário da casa durante 30 dias. A redução é `5,5 kW × (5/60 h) × 30 = 13,75 kWh`. Com a tarifa de referência, isso reduz aproximadamente `13,75 × R$ 0,78938 = R$ 10,85` da parcela tarifária. A potência efetiva e os minutos somados por todos os moradores mudam o resultado. [ANEEL, como calcular o consumo de aparelhos](https://www2.aneel.gov.br/aplicacoes_liferay/noticias_area/arquivo.cfm?idAreaNoticia=1&idNoticia=4101&tipo=PDF)
- **Geladeira e ar-condicionado.** Comparar equipamentos adequados ao mesmo uso pelo consumo indicado na etiqueta. Para geladeira, usar kWh/mês entre modelos de capacidade e função semelhantes. Para ar, usar kWh/ano entre modelos de capacidade equivalente, lembrando que o resultado do ensaio é padronizado. A rotina, a temperatura e a manutenção mudam o consumo real. [Inmetro, refrigeradores](https://www.gov.br/inmetro/pt-br/centrais-de-conteudo/noticias/2025/nova-etiqueta-do-inmetro-para-refrigeradores-entra-em-vigor-a-partir-de-1o-de-janeiro-de-2026/) · [Inmetro, condicionadores de ar](https://www.gov.br/inmetro/pt-br/assuntos/regulamentacao/avaliacao-da-conformidade/programa-brasileiro-de-etiquetagem/tabelas-de-eficiencia-energetica/condicionadores-de-ar)
- **Gerador a combustível.** Como referência de cálculo, estimar um equipamento consumindo 0,60 L/h ao entregar 1 kW, com combustível a R$ 6,00/L. O custo só de combustível é `(0,60 × 6,00) ÷ 1 = R$ 3,60/kWh`. Os três valores são hipotéticos. Para uma avaliação real, usar o preço local e a curva de consumo do fabricante na carga de interesse, acrescentando aquisição e manutenção. A operação emite gases e causa ruído. O gerador é tratado como recurso de reserva, com exigências de instalação segura, e o exemplo fica fora da comparação principal de economia residencial. [CPSC, segurança de geradores portáteis](https://www.cpsc.gov/s3fs-public/5123_SafetyAlert_PortableGenerators_102021.pdf)

## 6. Integração ao Citizen Assist AI

`main.py` combina o cenário com a função `calcular()` e preenche as respostas com cálculos no catálogo, inclusive os exemplos de chuveiro e gerador. O menu mostra esses mesmos textos e a busca os localiza por palavras-chave. A consulta A19 reaproveita o tema de Tarifa Social do PCA, com os critérios atuais e a relação com a comparação. O terminal e o Streamlit carregam os mesmos cálculos e orientações. Em ambos, a pergunta sobre placas solares retorna a geração calculada e indica as condições da estimativa.
