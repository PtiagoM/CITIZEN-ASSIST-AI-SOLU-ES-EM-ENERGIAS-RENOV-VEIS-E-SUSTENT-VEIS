"""Calcula o cenário de referência usado nas orientações de energia."""


def calcular(cenario: dict) -> dict:
    dias = cenario["dias"]
    consumo_base = cenario["consumo_base_kwh"]
    tarifa = cenario["te_rs_por_kwh"] + cenario["tusd_rs_por_kwh"]
    custo_base = consumo_base * tarifa

    horas_lampadas = cenario["quantidade_lampadas"] * cenario["horas_por_dia"] * dias
    consumo_antigas = cenario["potencia_antiga_w"] * horas_lampadas / 1000
    consumo_led = cenario["potencia_led_w"] * horas_lampadas / 1000
    economia_led_kwh = consumo_antigas - consumo_led
    consumo_casa_led = consumo_base - economia_led_kwh
    economia_led_rs = economia_led_kwh * tarifa
    custo_led = cenario["quantidade_lampadas"] * cenario["preco_led_unitario_rs"]

    # A irradiação diária dividida por 1000 W/m² vira horas de sol pleno.
    fator_mensal_solar = cenario["solar_potencia_kwp"] * cenario["solar_fator_desempenho"] * dias
    geracao_solar = fator_mensal_solar * cenario["solar_irradiacao_wh_m2_dia"] / 1000
    geracao_menor = fator_mensal_solar * cenario["solar_irradiacao_menor_wh_m2_dia"] / 1000
    geracao_maior = fator_mensal_solar * cenario["solar_irradiacao_maior_wh_m2_dia"] / 1000
    uso_direto = min(cenario["solar_autoconsumo_kwh"], geracao_solar, consumo_base)
    importacao = consumo_base - uso_direto
    injecao = geracao_solar - uso_direto

    fio_b_cobrado = cenario["fio_b_rs_por_kwh"] * cenario["fio_b_fracao_2026"]
    valor_credito = tarifa - fio_b_cobrado
    custo_minimo = cenario["solar_disponibilidade_kwh"] * tarifa
    custo_sem_creditos = importacao * tarifa
    # Só se usam créditos até alcançar o piso da ligação monofásica.
    limite_compensacao = max(0, custo_sem_creditos - custo_minimo) / valor_credito
    compensacao = min(injecao, importacao, limite_compensacao)
    custo_solar = max(custo_minimo, custo_sem_creditos - compensacao * valor_credito)
    economia_solar_rs = custo_base - custo_solar

    horas_poupadas_no_chuveiro = cenario["chuveiro_minutos_poupados_dia"] * dias / 60
    economia_chuveiro_kwh = cenario["chuveiro_potencia_w"] / 1000 * horas_poupadas_no_chuveiro

    gerador_potencia_kw = cenario["gerador_potencia_w"] / 1000
    gerador_custo_por_hora = cenario["gerador_consumo_l_h"] * cenario["gerador_preco_litro_rs"]
    gerador_custo_combustivel_kwh = gerador_custo_por_hora / gerador_potencia_kw

    return {
        "tarifa": tarifa,
        "economia_chuveiro_kwh": economia_chuveiro_kwh,
        "economia_chuveiro_rs": economia_chuveiro_kwh * tarifa,
        "gerador_custo_combustivel_kwh": gerador_custo_combustivel_kwh,
        "custo_base": custo_base,
        "consumo_antigas": consumo_antigas,
        "consumo_led": consumo_led,
        "consumo_casa_led": consumo_casa_led,
        "custo_casa_led": consumo_casa_led * tarifa,
        "economia_led_kwh": economia_led_kwh,
        "economia_led_rs": economia_led_rs,
        "custo_led": custo_led,
        "retorno_led_meses": custo_led / economia_led_rs,
        "geracao_solar": geracao_solar,
        "geracao_menor": geracao_menor,
        "geracao_maior": geracao_maior,
        "uso_direto": uso_direto,
        "importacao": importacao,
        "injecao": injecao,
        "fio_b_cobrado": fio_b_cobrado,
        "compensacao": compensacao,
        "credito_restante": injecao - compensacao,
        "custo_minimo": custo_minimo,
        "custo_solar": custo_solar,
        "economia_solar_rs": economia_solar_rs,
        "retorno_solar_anos": cenario["solar_custo_rs"] / economia_solar_rs / 12,
    }
