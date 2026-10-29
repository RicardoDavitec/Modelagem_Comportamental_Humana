"""
Figura 5.3 - Dano total em função do coeficiente de reverberação ρ.

Fórmula (série geométrica, válida para 0 <= ρ < 1):
    D_total(ρ) = D0 / (1 - ρ)

Uso no terminal do VS Code:
    python figura_5_3.py
    python figura_5_3.py --rho 0.7
    python figura_5_3.py --rho 0.7 --d0 2.5
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


def dano_total(rho, d0):
    """D_total = D0 / (1 - ρ). Só é finito para ρ < 1."""
    return d0 / (1.0 - rho)


def regime(rho):
    """Nome do regime da tabela do capítulo para um valor de ρ."""
    if rho >= 1.0:
        return "Amplificador"
    if rho >= 0.9:
        return "Ressonante"
    if rho >= 0.5:
        return "Condutor"
    if rho > 0.0:
        return "Amortecedor"
    return "Absorvente"


def desenhar(d0, rho_usuario=None):
    """Desenha a curva D_total(ρ) com as faixas dos regimes."""
    rho = np.linspace(0.0, 0.995, 800)   # ρ = 1 fica fora porque a soma diverge
    d = dano_total(rho, d0)
    y_max = 40 * d0                      # escala vertical: até 40 × D0

    fig, ax = plt.subplots(figsize=(11, 7))

    # Faixas coloridas dos regimes (mesmos intervalos da tabela)
    faixas = [
        (0.0, 0.5, "#d6eaf8", "Amortecedor\nATÉ 2×D₀\nPoucos anéis"),
        (0.5, 0.9, "#fdebd0", "Condutor\n2 a 10×D₀\nO rastro supera\no ato"),
        (0.9, 1.0, "#fadbd8", "Ressonante\n≥ 10×D₀\nO conflito sobrevive\nà ofensa"),
    ]
    for inicio, fim, cor, rotulo in faixas:
        ax.axvspan(inicio, fim, color=cor, alpha=0.8, zorder=0)
        ax.text((inicio + fim) / 2, y_max * 0.97, rotulo,
                ha="center", va="top", fontsize=8.5)

    # Região do amplificador (ρ ≥ 1): hachurada, sem valor finito
    ax.axvspan(1.0, 1.15, facecolor="#e8daef", alpha=0.8, zorder=0, hatch="//")
    ax.text(1.075, y_max * 0.97, "Amplificador\nIlimitado\nVendeta",
            ha="center", va="top", fontsize=8.5)

    # Curva principal
    ax.plot(rho, d, color="tab:green", linewidth=2.5,
            label=r"$D_{total}(\rho)=\frac{D_0}{1-\rho}$")
    ax.axvline(1.0, color="gray", linestyle="--", linewidth=1.2, label="ρ = 1 (limiar)")

    # Pontos de referência da tabela
    for p in (0.0, 0.5, 0.9):
        valor = dano_total(p, d0)
        ax.plot(p, valor, "o", color="black", markersize=6, zorder=5)
        ax.annotate(f"ρ = {p:g}\n{valor / d0:.0f} × D₀",
                    xy=(p, valor), xytext=(p + 0.03, valor + 0.06 * y_max),
                    fontsize=9, arrowprops=dict(arrowstyle="->", color="black"))

    # Caso escolhido pelo usuário no terminal
    if rho_usuario is not None and 0 <= rho_usuario < 1:
        valor = dano_total(rho_usuario, d0)
        ax.plot(rho_usuario, valor, "o", color="red", markersize=10, zorder=6,
                label=f"Caso escolhido: ρ = {rho_usuario:g}")
        ax.annotate(f"{valor / d0:.2f} × D₀", xy=(rho_usuario, valor),
                    xytext=(rho_usuario - 0.25, valor + 0.1 * y_max),
                    fontsize=10, color="red",
                    arrowprops=dict(arrowstyle="->", color="red"))

    ax.set_xlim(0, 1.15)
    ax.set_ylim(0, y_max)
    ax.set_xlabel("Coeficiente de reverberação ρ")
    ax.set_ylabel("Dano total D_total / D₀ (adimensional)")
    ax.set_title("Figura 5.3 - Dano total em função da reverberação\n"
                 "A curva cresce devagar no início e dispara perto de ρ = 1")
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.80), fontsize=9)
    ax.text(0.5, 1.5, "(a curva continua até o infinito; a escala foi limitada)",
            fontsize=8, color="gray", ha="center", transform=ax.transAxes)

    fig.tight_layout()

    nome = f"figura_5_3_d0_{str(round(d0, 2)).replace('.', '_')}.png"
    fig.savefig(nome, dpi=200)
    print(f"Figura salva como: {nome}")
    return fig


def main():
    parser = argparse.ArgumentParser(description="Figura 5.3: D_total(ρ) = D0 / (1 - ρ).")
    parser.add_argument("--rho", type=float, default=None,
                        help="Valor de ρ a destacar na curva (0 a 0,99)")
    parser.add_argument("--d0", type=float, default=1.0,
                        help="Dano primário D0 (padrão: 1.0)")
    args = parser.parse_args()

    if args.d0 <= 0:
        raise ValueError("D0 deve ser positivo.")
    if args.rho is not None and not (0 <= args.rho < 1):
        raise ValueError("ρ deve estar entre 0 e 1 (1 excluído), pois a soma diverge em ρ ≥ 1.")

    print("Tabela de referência (D_total / D0 = 1 / (1 - ρ)):")
    print("  ρ      | D_total/D0 | Regime")
    for p in [0.0, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]:
        print(f"  {p:<6} | {dano_total(p, 1.0):>10.2f} | {regime(p)}")

    desenhar(args.d0, args.rho)

    if TEM_TELA:
        plt.show()
    else:
        print("\nAviso: ambiente gráfico não encontrado. O PNG foi salvo, mas a janela não abriu.")


if __name__ == "__main__":
    main()
