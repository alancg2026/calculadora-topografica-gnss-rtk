# Projeto do Capítulo 2 — Programação Aplicada ao Geoprocessamento

O programa lê levantamentos GNSS em CSV, valida os registros, seleciona os
pontos com descrição `LIMITE`, calcula o perímetro e a área da poligonal e
gera arquivos de saída. Ele usa somente a biblioteca padrão do Python, sem
dependências externas.

## Como executar

1. Execute o programa pelo arquivo `main.py` (pressione **F5** ou clique em
   **Run Python File**).
2. Na interface, escolha `levantamento_rtk.csv`, `levantamento_bruto.csv` ou
   use **Escolher outro arquivo CSV...** para selecionar outro CSV.
3. Veja o resultado na tela e no terminal.

Não é necessário instalar bibliotecas externas. O projeto usa somente a
biblioteca padrão do Python.

## Arquivos de saída

Os arquivos abaixo são criados na mesma pasta do CSV escolhido:

- `descartes.csv`: registros rejeitados e seus motivos;
- `pontos_validos.csv`: registros aprovados após a conversão;
- `poligonal_utm.geojson`: polígono fechado com coordenadas UTM.

## Resultados esperados

| Arquivo | Válidos | Descartados | Vértices | Perímetro | Área |
|---|---:|---:|---:|---:|---:|
| `levantamento_rtk.csv` | 47 | 3 | 10 | 586,829 m | 2,5559 ha |
| `levantamento_bruto.csv` | 46 | 5 | 10 | 586,829 m | 2,5559 ha |
