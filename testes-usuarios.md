# Testes e ajustes

## Verificação técnica em 17 e 18/11/2026

O teste rodou no Python 3.14, pelo terminal e com `unittest`. Esta seção registra verificações técnicas do programa.

| Situação testada | Resultado esperado e verificado |
| --- | --- |
| Consumo e LED | Cálculo de 36,00 kWh para lâmpadas antigas, 5,40 kWh com LED e redução de R$ 24,16 na parcela do exemplo. |
| Solar, com e sem saldo para crédito | O balanço de energia fecha e o custo modelado respeita o piso. Com menos sol, a parcela aumenta e o saldo restante fica em zero. |
| Perguntas em linguagem comum | As consultas da suíte abriram o assunto esperado e apresentaram o trecho calculado ou o benefício, com fonte. |
| Conta alta e aparelhos | As perguntas sobre conta alta, chuveiro, geladeira e ar-condicionado abrem as orientações correspondentes. No exemplo do chuveiro, o cálculo confere 13,75 kWh poupados em 30 dias. |
| Gerador para baixar a conta | As perguntas sobre gerador abrem a orientação sobre reserva e segurança. O preço hipotético do combustível por kWh é calculado em R$ 3,60. |
| Entrada com e-mail fictício ou oito dígitos separados | Entrada recusada. O programa fica disponível para outra consulta. |
| Pergunta fora do catálogo | O assistente informa que não encontrou orientação suficiente e aponta o menu. |

Na verificação inicial, a pergunta “Tenho direito ao desconto na conta de luz?” abriu a leitura da fatura e algumas comparações caíram em respostas de uma única alternativa. O catálogo passou a reconhecer expressões como “desconto na conta de luz”, “comparar LED” e “LED ou placa solar”. Esses exemplos foram incluídos nos testes de regressão.

Em 18/11/2026, a interface Streamlit foi conferida no servidor local. A comparação pelo menu e as consultas sobre fatura, aparelhos, placas solares e gerador pelo chat apresentaram as orientações esperadas. As duas avaliações de demonstração foram gravadas em um CSV de teste com origem, código da orientação e Sim/Não. A entrada bloqueada ficou fora da conversa exibida e do CSV.

Na revisão das palavras-chave, comparei a versão anterior com a versão atual em 56 perguntas técnicas, com pelo menos quatro por orientação. O total de resultados corretos em primeiro lugar, com pelo menos três pontos e sem empate, passou de 45 para 56. O catálogo passou de 152 para 122 entradas únicas após normalização. A busca manteve os pesos do PCA. Por exemplo, a pergunta “Meu telhado serve para painéis fotovoltaicos?” aciona telhado, painéis e fotovoltaicos, somando 9 pontos para energia solar.

## Sessões com usuários — pendentes

O enunciado pede verificação de compreensão e utilidade, comentários e ajustes realizados (p. 2). Convidar pessoas que querem reduzir a conta de energia de casa para usar o programa sem dar a resposta antes. O roteiro pode ser repetido com três participantes identificados apenas por códigos. Usar dados fictícios quando a tarefa mencionar uma fatura.

| Tarefa | Como observar compreensão e utilidade |
| --- | --- |
| Encontrar o que significa kWh | Pedir que a pessoa explique onde olharia na conta e o que o número mede. |
| Escolher uma ação com pouco dinheiro | Pedir que encontre uma opção e diga o que verificaria antes de comprar uma lâmpada. |
| Comparar LED e solar | Pedir que diga qual exige mais investimento e cite um fator que muda a estimativa solar. |
| Investigar a conta alta e o gasto do chuveiro | Pedir que a pessoa diferencie aumento de consumo e aumento de tarifa. Em seguida, pedir que explique quanto o chuveiro pode poupar no exemplo e quais dados mudariam o valor na casa dela. |
| Avaliar se um gerador reduz gastos | Pedir que identifique que valores precisa obter para comparar o combustível com a tarifa da rede e em que situação o gerador serve como reserva. |
| Verificar um possível desconto na conta | Pedir que encontre um canal oficial e explique se qualquer residência recebe o benefício. |

Após cada tarefa, perguntar **“O que ficou claro?”**, **“Isso ajudaria na sua casa?”** e **“Onde você precisou de ajuda?”**. Registrar a resposta em linguagem neutra, sem nome, endereço, renda, documentos ou cópias da fatura.

| Código | Tarefa | Compreendeu sem ajuda? | Considerou útil? | Comentário anônimo | Decisão ou ajuste |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

Depois da rodada, preencher apenas com observações reais, atualizar a orientação que gerou dificuldade e verificar novamente a tarefa afetada.
