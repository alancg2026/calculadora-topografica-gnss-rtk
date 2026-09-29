"""Funções de geometria para a poligonal do levantamento."""

from math import hypot


def distancia_horizontal(ponto_a, ponto_b):
    """Calcula a distância plana entre dois pontos UTM."""
    diferenca_este = ponto_b["ESTE"] - ponto_a["ESTE"]
    diferenca_norte = ponto_b["NORTE"] - ponto_a["NORTE"]
    return hypot(diferenca_este, diferenca_norte)


def calcular_perimetro(poligonal):
    """Soma as distâncias entre vértices consecutivos e fecha a poligonal."""
    if len(poligonal) < 2:
        return 0.0

    perimetro = 0.0
    for i in range(len(poligonal)):
        ponto_atual = poligonal[i]
        ponto_seguinte = poligonal[(i + 1) % len(poligonal)]
        perimetro += distancia_horizontal(ponto_atual, ponto_seguinte)
    return perimetro


def calcular_area_gauss(poligonal):
    """Retorna a área com sinal e a área absoluta pela fórmula de Gauss."""
    if len(poligonal) < 3:
        return 0.0, 0.0

    somatorio_gauss = 0.0
    for i in range(len(poligonal)):
        ponto_atual = poligonal[i]
        ponto_seguinte = poligonal[(i + 1) % len(poligonal)]
        somatorio_gauss += (
            ponto_atual["ESTE"] * ponto_seguinte["NORTE"]
            - ponto_seguinte["ESTE"] * ponto_atual["NORTE"]
        )

    area_com_sinal = somatorio_gauss / 2
    return area_com_sinal, abs(area_com_sinal)
