# Citizen Assist AI | Energia em casa

Global Solution FIAP · Ciência da Computação · Soluções em Energias Renováveis e Sustentáveis

| Integrante | RM |
| --- | --- |
| Tiago Pimentel Muniz | 574148 |
| Gustavo Curis de Francisco | 569704 |
| Caio César Portela França | 573127 |

## Público e problema

O assistente atende **pessoas que querem gastar menos na conta de energia de casa**. Ele ajuda a entender se o consumo mudou, identificar quais aparelhos merecem atenção e avaliar mudanças de rotina, equipamentos mais eficientes, produção de energia solar e descontos. Essa necessidade aparece no levantamento da EPE sobre usos de energia nas residências brasileiras, que inclui refrigeração de alimentos, climatização e aquecimento de água entre os principais usos de eletricidade. [Atlas da Eficiência Energética 2024, setor residencial](https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-857/Atlas%20da%20Efici%C3%AAncia%20Energ%C3%A9tica%20Brasil%202024.pdf)

A comparação técnica usa uma residência de referência em São Paulo (SP), com **180 kWh em 30 dias**, para avaliar duas formas de reduzir o gasto de uma mesma casa preservando o brilho e o uso dos demais aparelhos. A cidade e a tarifa são premissas do exemplo. Use o consumo, os aparelhos e a tarifa da sua residência para avaliar as alternativas locais. O estudo se relaciona ao ODS 7, em especial às metas de energia renovável e eficiência energética.

## O que o assistente responde

| Pergunta de exemplo | Orientação |
| --- | --- |
| O que é kWh na fatura? | Como ler o consumo e estimar o gasto de um aparelho. |
| Como baixar a conta de luz? | Um roteiro para separar mudanças no consumo, na tarifa e nas outras cobranças e escolher uma ação. |
| Como economizar com o chuveiro? | Como reduzir desperdício e calcular a energia poupada em um exemplo. |
| Qual geladeira gasta menos? | Como comparar consumo em kWh por mês e escolher modelos equivalentes. |
| E o ar-condicionado? | Hábitos de uso e como ler o consumo anual na etiqueta. |
| Gerador a gasolina compensa para baixar a conta? | Custo do combustível por kWh, uso de reserva e cuidados de segurança. |
| Como trocar lâmpadas por LED? | Como preservar o brilho e reduzir o consumo. |
| Posso instalar placas solares? | Geração estimada, uso direto, fluxo de energia na rede e condições do imóvel. |
| Quero comparar LED e energia solar | Custo inicial, estimativas do mesmo período e por onde começar. |
| Tenho direito ao desconto na conta de luz? | Como verificar a Tarifa Social e o Desconto Social nos canais oficiais. |

O programa segue o núcleo de regras do Citizen Assist AI do PCA. A busca prioriza palavras curtas que identificam o assunto e expressões como “Tarifa Social”. As palavras-chave encontradas em uma mesma pergunta acumulam pontos para a orientação correspondente. A busca compara também os termos dos títulos e normaliza acentos e maiúsculas. Cada palavra-chave encontrada vale 3 pontos. Cada palavra distinta da pergunta, com pelo menos quatro letras e presente no título, vale 1 ponto. A partir de 3 pontos, o assistente apresenta a melhor orientação com fonte e data de verificação. A mesma orientação está disponível no menu.

Os valores que aparecem nas respostas são calculados ao iniciar o programa a partir de [data/cenario.json](data/cenario.json). O programa bloqueia entradas com `@` ou oito ou mais dígitos. No Streamlit, a conversa fica na sessão do navegador. Ao responder Sim ou Não, o arquivo local `data/feedback.csv` recebe apenas a origem da consulta, o código da orientação e a avaliação.

## Resultado do estudo — LED e solar

| Alternativa | Investimento estimado | Efeito em 30 dias | Redução estimada na parcela tarifária |
| --- | ---: | --- | ---: |
| Troca de cinco incandescentes por LED | R$ 50,00 | 30,60 kWh a menos no consumo | R$ 24,16 |
| Energia solar no telhado, 1,5 kWp | R$ 6.500,00 | 167,69 kWh gerados e 60 kWh usados no momento da geração | R$ 118,41 |

Para quem ainda usa lâmpadas antigas, a troca nos pontos mais usados tem o menor custo inicial. A opção solar depende de avaliação do telhado, do consumo, das regras da distribuidora e dos orçamentos. Para famílias elegíveis, vale conferir o benefício tarifário antes de assumir gastos. Os valores acima usam a tarifa residencial comum da Enel SP e excluem impostos, bandeiras, iluminação pública e benefícios. O cálculo solar considera a cobrança mínima da ligação monofásica e a compensação de energia do cenário de 2026. Cada alternativa parte da mesma conta de referência. Ao combinar as duas, refaça a estimativa com o novo consumo.

Hipóteses, fórmulas, comparação, sensibilidade, impactos ambientais e fontes estão na [análise técnica](analise-energetica.md). O [catálogo](data/base_conhecimento.json) contém as orientações e os links que o cidadão vê.

## Executar no PyCharm

1. Abra esta pasta como um projeto e selecione um interpretador Python 3.10 ou mais recente. A execução foi conferida no Python 3.14 e usa apenas a biblioteca padrão.
2. Abra `main.py` e selecione **Run 'main'**. Se preferir o terminal, execute `python main.py`. No Windows, use `py main.py` se `python` não abrir.
3. Digite **4** para abrir a comparação ou escreva **Quero comparar LED e energia solar**. Digite **0** para sair.

Para repetir os testes técnicos, execute `python -m unittest discover -s tests -v` ou `py -m unittest discover -s tests -v`.

## Abrir a interface Streamlit no PyCharm

No terminal do PyCharm, a partir da pasta deste projeto, execute:

```powershell
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py --server.port 8502
```

Abra [localhost:8502](http://localhost:8502). A página usa o chat, o menu por categoria e a avaliação Sim/Não do PCA. Experimente **Como baixar a conta de luz?**, **Meu chuveiro gasta muita energia?** ou **Gerador a gasolina compensa para baixar a conta?**. Para conferir o estudo, pergunte **Quero comparar LED e energia solar** ou selecione **Decisão e benefícios → Comparar lâmpadas LED e energia solar**.

Em outro computador, prepare o ambiente desta pasta com `py -m venv .venv` e instale com `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`. Para rodar todos os testes com Streamlit instalado, use `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`.

## Evidências e entrega

- A validação com usuários reais está pendente. O [roteiro de teste](testes-usuarios.md) contém as tarefas e a tabela para registrar as observações da rodada.
- [Roteiro da demonstração](apresentacao/roteiro.md). Vídeo local em `apresentacao/citizen-assist-energia.avi`, com 2min18s, texto na tela e demonstração do terminal. O link público de avaliação será inserido após o envio ao YouTube como não listado.
- [Modelo do TXT do Portal](entrega/portal.modelo.txt). O arquivo de entrega exige os dois links acessíveis, conforme o enunciado, p. 3.
