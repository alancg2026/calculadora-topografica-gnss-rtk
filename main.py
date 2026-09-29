"""Programa principal do Projeto do Capítulo 2."""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from geometria import calcular_area_gauss, calcular_perimetro
from leitura import ler_levantamento, selecionar_poligonal
from saida import escrever_descartes, escrever_geojson, escrever_pontos_validos


def processar_arquivo(caminho_csv):
    """Processa um levantamento e grava os três arquivos de saída."""
    caminho_csv = Path(caminho_csv)
    pontos_validos, descartes = ler_levantamento(caminho_csv)
    poligonal = selecionar_poligonal(pontos_validos)

    if len(poligonal) < 3:
        raise ValueError("São necessários pelo menos três pontos LIMITE válidos.")

    perimetro = calcular_perimetro(poligonal)
    area_com_sinal, area_m2 = calcular_area_gauss(poligonal)
    pasta_saida = caminho_csv.parent

    escrever_descartes(pasta_saida / "descartes.csv", descartes)
    escrever_pontos_validos(pasta_saida / "pontos_validos.csv", pontos_validos)
    escrever_geojson(
        pasta_saida / "poligonal_utm.geojson",
        poligonal,
        perimetro,
        area_m2,
    )

    return {
        "arquivo": caminho_csv.name,
        "validos": len(pontos_validos),
        "descartados": len(descartes),
        "vertices": len(poligonal),
        "perimetro": perimetro,
        "area_com_sinal": area_com_sinal,
        "area_m2": area_m2,
        "area_ha": area_m2 / 10000,
    }


def formatar_resultado(resultado):
    return (
        f"Arquivo: {resultado['arquivo']}\n"
        f"Pontos válidos: {resultado['validos']}\n"
        f"Pontos descartados: {resultado['descartados']}\n"
        f"Vértices LIMITE: {resultado['vertices']}\n\n"
        f"Perímetro: {resultado['perimetro']:.3f} m\n"
        f"Área com sinal: {resultado['area_com_sinal']:.3f} m²\n"
        f"Área: {resultado['area_m2']:.3f} m²\n"
        f"Área: {resultado['area_ha']:.4f} ha\n\n"
        "Saídas criadas ao lado do CSV:\n"
        "- descartes.csv\n"
        "- pontos_validos.csv\n"
        "- poligonal_utm.geojson"
    )


def processar_com_interface(caminho, status):
    """Processa um arquivo sem fechar a janela se ocorrer algum erro."""
    try:
        resultado = processar_arquivo(caminho)
        texto = formatar_resultado(resultado)
        print(texto)
        status.set(f"Último processamento: {resultado['arquivo']} — concluído")
        messagebox.showinfo("Processamento concluído", texto)
    except FileNotFoundError:
        status.set("Arquivo não encontrado. Escolha outro arquivo.")
        messagebox.showerror("Arquivo não encontrado", "O arquivo selecionado não foi encontrado.")
    except PermissionError:
        status.set("Arquivo em uso. Feche-o no Excel e tente novamente.")
        messagebox.showerror(
            "Arquivo em uso",
            "Não foi possível gravar uma saída. Feche os arquivos no Excel e tente novamente.",
        )
    except (ValueError, KeyError, UnicodeError, OSError) as erro:
        status.set("O processamento falhou. Corrija ou escolha outro arquivo.")
        messagebox.showerror("Erro no processamento", str(erro))


def main():
    raiz = tk.Tk()
    raiz.title("Processamento de levantamento GNSS")
    raiz.geometry("540x360")
    raiz.resizable(False, False)

    pasta_projeto = Path(__file__).resolve().parent
    status = tk.StringVar(value="Escolha um levantamento para começar.")

    def processar_padrao(nome_arquivo):
        processar_com_interface(pasta_projeto / nome_arquivo, status)

    def escolher_outro():
        caminho = filedialog.askopenfilename(
            parent=raiz,
            title="Selecione o arquivo do levantamento",
            initialdir=pasta_projeto,
            filetypes=(("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")),
        )
        if caminho:
            processar_com_interface(caminho, status)
        else:
            status.set("Seleção cancelada. Escolha uma opção quando desejar.")

    tk.Label(
        raiz,
        text="Projeto do Capítulo 2",
        font=("Arial", 18, "bold"),
    ).pack(pady=(25, 5))

    tk.Label(
        raiz,
        text="Selecione o arquivo que deseja processar:",
        font=("Arial", 11),
    ).pack(pady=(0, 20))

    tk.Button(
        raiz,
        text="Processar levantamento RTK",
        width=34,
        height=2,
        command=lambda: processar_padrao("levantamento_rtk.csv"),
    ).pack(pady=5)

    tk.Button(
        raiz,
        text="Processar levantamento bruto",
        width=34,
        height=2,
        command=lambda: processar_padrao("levantamento_bruto.csv"),
    ).pack(pady=5)

    tk.Button(
        raiz,
        text="Escolher outro arquivo CSV...",
        width=34,
        command=escolher_outro,
    ).pack(pady=5)

    tk.Label(
        raiz,
        textvariable=status,
        wraplength=480,
        fg="#333333",
    ).pack(pady=15)

    tk.Button(raiz, text="Sair", width=12, command=raiz.destroy).pack()

    raiz.mainloop()


if __name__ == "__main__":
    main()
