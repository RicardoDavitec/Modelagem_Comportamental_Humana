"""
Figura 5.5 - Arco histórico da justiça: ρ′ por etapa.

Modelo:
    ρ′ = ρ0 · (1 − κ)

Os valores de κ por etapa são PROVISÓRIOS (o capítulo não os fornece).
Ajuste a lista ETAPAS para calibrar o gráfico.

Uso no terminal do VS Code:
    python figura_5_5.py
    python figura_5_5.py --rho0 1.2
"""

import argparse
import os

import matplotlib

TEM_TELA = bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
if not TEM_TELA:
    # Sem ambiente gráfico: salva apenas o PNG
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

# (nome da etapa, atributo da consciência, κ provisório, observação)
ETAPAS = [
    ("1. Talião",           "Senso de justiça",     0.00, "Teto: ρ′ = ρ0"),
    ("2. Proporcionalidade", "+ Razão",              0.15, "Ajusta a medida"),
    ("3. Equidade",          "+ Sentimento (início)", 0.35, "Considera a intenção"),
    ("4. Reparação",         "Quase completo",       0.00, "Atua sobre D₀, não sobre ρ"),
    ("5. Caridade",          "Completo",             0.60, "Reduz ρ"),
]


def rho_linha(rho0, kappa):
    """ρ′ = ρ0 · (1 − κ). Com κ = 0, ρ′ = ρ0; com κ = 1, ρ′ = 0."""
    return rho0 * (1.0 - kappa)


def desenhar(rho0):
    nomes = [e[0] for e in ETAPAS]
    kappas = [e[2] for e in ETAPAS]
    valores = [rho_linha(rho0, k) for k in kappas]
    cores = ["tab:red" if v >= 1.0 else "tab:green" for v in valores]

    fig, ax = plt.subplots(figsize=(12, 7))
    x = np.arange(len(ETAPAS))
    barras = ax.bar(x, valores, color=cores, edgecolor="black", width=0.6, zorder=3)

    # Linha tracejada no limiar ρ = 1
    ax.axhline(1.0, color="gray", linestyle="--", linewidth=1.8,
               label="Limiar ρ′ = 1", zorder=4)

    # Valor numérico sobre cada barra
    for barra, v in zip(barras, valores):
        ax.text(barra.get_x() + barra.get_width() / 2, v + 0.02, f"{v:.2f}",
                ha="center", va="bottom", fontsize=11, fontweight="bold")

    # Rótulos do eixo x: nome, atributo, κ e observação
    rotulos = [f"{e[0]}\n{e[1]}\nκ = {e[2]:.2f}\n{e[3]}" for e in ETAPAS]
    ax.set_xticks(x)
    ax.set_xticklabels(rotulos, fontsize=8.5)

    ax.set_ylim(0, max(1.3, rho0 * 1.15))
    ax.set_ylabel("Coeficiente de reverberação efetivo ρ′ (adimensional)")
    ax.set_title("Figura 5.5 - Arco histórico da justiça: ρ′ por etapa\n"
                 f"ρ0 = {rho0:g} (ofensa sem reação)   |   ρ′ = ρ0 · (1 − κ)",
                 fontsize=12)
    ax.grid(axis="y", alpha=0.3, zorder=0)
    ax.legend(loc="upper right")

    fig.tight_layout()

    nome = f"figura_5_5_rho0_{str(round(rho0, 2)).replace('.', '_')}.png"
    fig.savefig(nome, dpi=200)
    print(f"Figura salva como: {nome}")
    return fig


def main():
    parser = argparse.ArgumentParser(description="Figura 5.5: ρ′ por etapa do arco da justiça.")
    parser.add_argument("--rho0", type=float, default=1.0,
                        help="Coeficiente inicial ρ0 sem reação (padrão: 1.0)")
    args = parser.parse_args()

    if args.rho0 <= 0:
        raise ValueError("ρ0 deve ser positivo.")

    print("Etapa                  | κ     | ρ′      | Regime")
    for nome, _, kappa, _ in ETAPAS:
        v = rho_linha(args.rho0, kappa)
        regime = "Amplificador (ρ′ ≥ 1)" if v >= 1 else "Convergente (ρ′ < 1)"
        print(f"{nome:<22} | {kappa:<5.2f} | {v:<7.3f} | {regime}")

    desenhar(args.rho0)

    if TEM_TELA:
        plt.show()
    else:
        print("\nAviso: ambiente gráfico não encontrado. O PNG foi salvo, mas a janela não abriu.")


if __name__ == "__main__":
    main()
