"""Leitura e validação dos arquivos CSV do levantamento."""

import csv
import unicodedata


CAMPOS_OBRIGATORIOS = ("PONTO", "ESTE", "NORTE", "DESCRICAO", "SOLUCAO")
CAMPOS_SAIDA = (
    "PONTO", "ESTE", "NORTE", "COTA", "DESCRICAO",
    "SOLUCAO", "PDOP", "SATELITES", "DATA_HORA",
)


def _sem_acentos(texto):
    normalizado = unicodedata.normalize("NFKD", texto)
    return normalizado.encode("ascii", "ignore").decode("ascii")


def _normalizar_cabecalho(nome):
    nome = _sem_acentos((nome or "").strip()).upper()
    # Também aceita cabeçalhos visualmente danificados, como DESCRI��O.
    if nome.startswith("DESCRI"):
        return "DESCRICAO"
    if nome.startswith("SOLU"):
        return "SOLUCAO"
    return nome


def numero(texto):
    """Converte número escrito com ponto ou vírgula decimal para float."""
    return float(texto.strip().replace(",", "."))


def _numero_opcional(texto):
    texto = (texto or "").strip()
    if not texto:
        return ""
    try:
        return numero(texto)
    except ValueError:
        return ""


def _abrir_com_codificacao(caminho):
    """Abre primeiro como UTF-8 e usa Latin-1 quando necessário."""
    try:
        arquivo = open(caminho, "r", encoding="utf-8-sig", newline="")
        arquivo.read()
        arquivo.seek(0)
        return arquivo
    except UnicodeDecodeError:
        arquivo.close()
        return open(caminho, "r", encoding="latin-1", newline="")


def ler_levantamento(caminho):
    """Lê o CSV e devolve os pontos válidos e os registros descartados."""
    pontos_validos = []
    descartes = []

    with _abrir_com_codificacao(caminho) as arquivo:
        primeira_linha = arquivo.readline()
        arquivo.seek(0)
        delimitador = ";" if primeira_linha.count(";") > primeira_linha.count(",") else ","
        leitor = csv.DictReader(arquivo, delimiter=delimitador)

        if leitor.fieldnames is None:
            raise ValueError("O arquivo CSV não possui cabeçalho.")

        mapa_campos = {
            nome_original: _normalizar_cabecalho(nome_original)
            for nome_original in leitor.fieldnames
        }

        campos_encontrados = set(mapa_campos.values())
        faltantes = set(CAMPOS_OBRIGATORIOS) - campos_encontrados
        if faltantes:
            raise ValueError(
                "Faltam colunas obrigatórias: " + ", ".join(sorted(faltantes))
            )

        for linha_original in leitor:
            linha = {
                mapa_campos.get(chave, chave): valor
                for chave, valor in linha_original.items()
                if chave is not None
            }

            if not any((valor or "").strip() for valor in linha.values()):
                continue

            ponto = (linha.get("PONTO") or "").strip()
            incompleta = any(
                not (linha.get(campo) or "").strip()
                for campo in CAMPOS_OBRIGATORIOS
            )
            if incompleta:
                descartes.append({
                    "LINHA": leitor.line_num,
                    "PONTO": ponto or "SEM_IDENTIFICACAO",
                    "MOTIVO": "linha incompleta",
                })
                continue

            solucao = linha["SOLUCAO"].strip().upper()
            if solucao != "FIX":
                descartes.append({
                    "LINHA": leitor.line_num,
                    "PONTO": ponto,
                    "MOTIVO": f"solução {solucao}; esperado FIX",
                })
                continue

            try:
                este = numero(linha["ESTE"])
                norte = numero(linha["NORTE"])
            except ValueError:
                descartes.append({
                    "LINHA": leitor.line_num,
                    "PONTO": ponto,
                    "MOTIVO": "coordenada ESTE ou NORTE inválida",
                })
                continue

            pontos_validos.append({
                "PONTO": ponto,
                "ESTE": este,
                "NORTE": norte,
                "COTA": _numero_opcional(linha.get("COTA")),
                "DESCRICAO": linha["DESCRICAO"].strip().upper(),
                "SOLUCAO": solucao,
                "PDOP": _numero_opcional(linha.get("PDOP")),
                "SATELITES": _numero_opcional(linha.get("SATELITES")),
                "DATA_HORA": (linha.get("DATA_HORA") or "").strip(),
            })

    return pontos_validos, descartes


def selecionar_poligonal(pontos_validos):
    """Seleciona somente os pontos LIMITE, preservando a ordem do arquivo."""
    return [
        ponto for ponto in pontos_validos
        if ponto["DESCRICAO"].strip().upper() == "LIMITE"
    ]
