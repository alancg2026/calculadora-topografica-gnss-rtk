"""Gravação dos produtos gerados pelo processamento."""

import csv
import json

from leitura import CAMPOS_SAIDA


def escrever_descartes(caminho, descartes):
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=("LINHA", "PONTO", "MOTIVO"),
            delimiter=";",
        )
        escritor.writeheader()
        escritor.writerows(descartes)


def escrever_pontos_validos(caminho, pontos):
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=CAMPOS_SAIDA,
            delimiter=";",
        )
        escritor.writeheader()
        escritor.writerows(pontos)


def escrever_geojson(caminho, poligonal, perimetro, area_m2):
    coordenadas = [[p["ESTE"], p["NORTE"]] for p in poligonal]
    if coordenadas:
        coordenadas.append(coordenadas[0])

    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "vertices": len(poligonal),
                    "perimetro_m": round(perimetro, 3),
                    "area_m2": round(area_m2, 3),
                    "area_ha": round(area_m2 / 10000, 4),
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coordenadas],
                },
            }
        ],
    }

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(geojson, arquivo, ensure_ascii=False, indent=2)
