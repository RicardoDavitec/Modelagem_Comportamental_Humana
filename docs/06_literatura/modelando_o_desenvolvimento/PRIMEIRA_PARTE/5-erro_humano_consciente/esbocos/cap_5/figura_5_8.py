"""
Figura 5.8 - O Grande Filtro: plano de velocidades e tempo de quitação T*.

Fronteira provisória (o capítulo não fornece valores numéricos):
    regeneração se  b < k · a
    colapso    se  b ≥ k · a

  a = velocidade de aprendizado pela dor  (eixo horizontal, equivale a c)
  b = alcance tecnológico do erro         (eixo vertical, equivale a g)

Tempo de quitação (seção XIII):
    T* = ln(K / C0) / (c − g),  finito somente se c > g

Uso no terminal do VS Code:
    python figura_5_8.py
    python figura_5_8.py --a 2.0 --b 1.2
    python figura_5_8.py --a 0.8 --b 1.5 --K 20 --C0 2 --k 1.2
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


def regeneracao(a, b, k):
    """True onde a caridade (a) supera o erro (b), pela fronteira b = k·a."""
    return b < k * a


def tempo_quitacao(K, C0, c, g):
    """T* = ln(K / C0) / (c − g). Devolve None quando c ≤ g (sem quitação finita)."""
    if c <= g:
        return None
    return np.log(K / C0) / (c - g)


def desenhar(a, b, K, C0, k, lim):
    # ---------- Painel A: plano (a, b) ----------
    eixo = np.linspace(0, lim, 400)
    AA, BB = np.meshgrid(eixo, eixo)
    Z = regeneracao(AA, BB, k).astype(float)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5))

    ax1.contourf(AA, BB, Z, levels=[-0.5, 0.5, 1.5],
                 colors=["#fadbd8", "#d5f5e3"])
    ax1.plot(eixo, k * eixo, "k--", linewidth=2, label="Separatriz: b = k·a")
    ax1.text(0.72 * lim, 0.18 * lim, "REGENERAÇÃO\n(atrator: c > g)",
             ha="center", fontsize=11, fontweight="bold", color="darkgreen")
    ax1.text(0.18 * lim, 0.72 * lim, "COLAPSO\n(separatriz cruzada)",
             ha="center", fontsize=11, fontweight="bold", color="darkred")

    ax1.plot(a, b, "o", color="black", markersize=10, zorder=5,
             label=f"Cenário escolhido: a = {a:g}, b = {b:g}")
    ax1.set_xlim(0, lim)
    ax1.set_ylim(0, lim)
    ax1.set_aspect("equal")
    ax1.set_xlabel("Velocidade de aprendizado pela dor (a)")
    ax1.set_ylabel("Alcance tecnológico do erro (b)")
    ax1.set_title("(A) O Grande Filtro: fronteira entre colapso e regeneração")
    ax1.legend(loc="upper left", fontsize=9)
    ax1.grid(alpha=0.3)

    # ---------- Painel B: T* em função de c ----------
    g = b
    if K <= C0:
        ax2.text(0.5, 0.5, "K ≤ C0: a caridade inicial já supera a dívida\n"
                 "T* ≤ 0 (quitação imediata)",
                 ha="center", va="center", transform=ax2.transAxes, fontsize=11)
    else:
        cs = np.linspace(g + 0.005, lim, 800)
        T = np.log(K / C0) / (cs - g)
        ax2.plot(cs, T, color="tab:blue", linewidth=2.2,
                 label=r"$T^{*} = \frac{\ln(K/C_0)}{c-g}$")
        ax2.axvline(g, color="gray", linestyle="--", label=f"c = g = {g:g} (assíntota)")

        t_atual = tempo_quitacao(K, C0, a, g)
        if t_atual is not None:
            ax2.plot(a, t_atual, "o", color="red", markersize=9, zorder=5,
                     label=f"Cenário escolhido: T* ≈ {t_atual:.2f}")
        ax2.set_ylim(0, 15)
    ax2.set_xlim(0, lim)
    ax2.set_xlabel("Taxa da caridade autocatalítica (c)")
    ax2.set_ylabel("Tempo de quitação T* (adimensional)")
    ax2.set_title("(B) Quitação finita somente se c > g")
    ax2.grid(alpha=0.3)
    ax2.legend(loc="upper right", fontsize=9)

    fig.suptitle(f"Figura 5.8 - O Grande Filtro (k = {k:g}, K = {K:g}, C₀ = {C0:g})",
                 fontsize=12)
    fig.tight_layout()

    nome = f"figura_5_8_a_{str(a).replace('.', '_')}_b_{str(b).replace('.', '_')}.png"
    fig.savefig(nome, dpi=200)
    print(f"Figura salva como: {nome}")
    return fig


def main():
    parser = argparse.ArgumentParser(description="Figura 5.8: o Grande Filtro.")
    parser.add_argument("--a", type=float, default=1.2,
                        help="Velocidade de aprendizado pela dor, c (padrão: 1.2)")
    parser.add_argument("--b", type=float, default=0.8,
                        help="Alcance tecnológico do erro, g (padrão: 0.8)")
    parser.add_argument("--K", type=float, default=10.0,
                        help="Dívida inicial K (padrão: 10)")
    parser.add_argument("--C0", type=float, default=1.0,
                        help="Ação caridosa inicial C0 (padrão: 1)")
    parser.add_argument("--k", type=float, default=1.0,
                        help="Fator da separatriz b = k·a (padrão: 1)")
    parser.add_argument("--lim", type=float, default=3.0,
                        help="Limite dos eixos do gráfico (padrão: 3)")
    args = parser.parse_args()

    if args.a < 0 or args.b < 0:
        raise ValueError("a e b devem ser não negativos.")
    if args.K <= 0 or args.C0 <= 0:
        raise ValueError("K e C0 devem ser positivos.")
    if args.k <= 0:
        raise ValueError("k deve ser positivo.")
    if args.b >= args.lim:
        raise ValueError("b deve ser menor que --lim para aparecer no gráfico.")

    regime = "Regeneração (atrator)" if regeneracao(args.a, args.b, args.k) else "Colapso (separatriz cruzada)"
    print(f"Cenário: a = {args.a:g}, b = {args.b:g}  ->  {regime}")

    T = tempo_quitacao(args.K, args.C0, args.a, args.b)
    if T is None:
        print("Tempo de quitação: não finito (c ≤ g).")
    else:
        print(f"Tempo de quitação: T* ≈ {T:.3f}")

    desenhar(args.a, args.b, args.K, args.C0, args.k, args.lim)

    if TEM_TELA:
        plt.show()
    else:
        print("\nAviso: ambiente gráfico não encontrado. O PNG foi salvo, mas a janela não abriu.")


if __name__ == "__main__":
    main()
