"""
Figura 5.6 - Curva do erro E(τ) e saldo de sofrimento S(τ).

Modelo:
    E(τ) = L(τ) · [1 − M(τ)]
    S(τ) = ∫₀^τ [g(τ') − c(τ')] dτ'

As funções L, M, g e c são PROVISÓRIAS (o capítulo não as define).
Ajuste-as nas funções abaixo ou pela linha de comando.

Uso no terminal do VS Code:
    python figura_5_6.py
    python figura_5_6.py --kg 0.9 --kc 1.4
    python figura_5_6.py --tau_M 5 --tau_max 16
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


# ---------- Funções do modelo (provisórias) ----------

def liberdade(tau, tau_L):
    """L(τ): cresce cedo e satura. L = 1 − e^(−τ/τ_L)."""
    return 1.0 - np.exp(-tau / tau_L)


def maturidade(tau, tau_M, s):
    """M(τ): cresce tarde, em forma de S. M = 1 / (1 + e^(−(τ − τ_M)/s))."""
    return 1.0 / (1.0 + np.exp(-(tau - tau_M) / s))


def erro(L, M):
    """E(τ) = L(τ) · [1 − M(τ)]."""
    return L * (1.0 - M)


def geracao_debito(E, kg):
    """g(τ): débito gerado pelo erro, proporcional a E. g = k_g · E."""
    return kg * E


def quitacao_caridade(M, kc):
    """c(τ): quitação pela caridade, cresce com a maturidade. c = k_c · M²."""
    return kc * M ** 2


# ---------- Ferramentas numéricas ----------

def integral_acumulada(y, x):
    """Integral de y em relação a x, pela regra do trapézio, desde x[0]."""
    dx = np.diff(x)
    areas = (y[1:] + y[:-1]) / 2.0 * dx
    return np.concatenate(([0.0], np.cumsum(areas)))


def primeiro_zero_descendente(x, f, inicio):
    """Primeiro τ, a partir do índice 'inicio', em que f passa de > 0 para ≤ 0."""
    for i in range(inicio, len(x) - 1):
        if f[i] > 0 and f[i + 1] <= 0:
            # interpolação linear para estimar o ponto exato do cruzamento
            return x[i] + (0 - f[i]) * (x[i + 1] - x[i]) / (f[i + 1] - f[i])
    return None


# ---------- Figura ----------

def desenhar(tau_max, tau_L, tau_M, s, kg, kc):
    tau = np.linspace(0.0, tau_max, 2000)

    L = liberdade(tau, tau_L)
    M = maturidade(tau, tau_M, s)
    E = erro(L, M)
    g = geracao_debito(E, kg)
    c = quitacao_caridade(M, kc)
    S = integral_acumulada(g - c, tau)

    # Pico do erro
    i_pico = int(np.argmax(E))
    tau_pico, E_pico = tau[i_pico], E[i_pico]

    # Início da Regeneração: g = c depois do pico do erro
    tau_reg = primeiro_zero_descendente(tau, g - c, i_pico)
    i_reg = int(np.argmin(np.abs(tau - tau_reg))) if tau_reg is not None else None

    # Máximo do saldo S e retorno a zero
    i_smax = int(np.argmax(S))
    tau_smax, S_max = tau[i_smax], S[i_smax]
    tau_zero = primeiro_zero_descendente(tau, S, i_smax)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6))

    # ---------- Painel A: E(τ) ----------
    ax1.plot(tau, E, color="tab:blue", linewidth=2.2, label="E(τ) = L(τ)·[1 − M(τ)]")
    ax1.plot(tau, L, "--", color="gray", linewidth=1, alpha=0.7, label="L(τ) (liberdade)")
    ax1.plot(tau, M, ":", color="tab:orange", linewidth=1.4, alpha=0.9, label="M(τ) (maturidade)")
    ax1.plot(tau_pico, E_pico, "o", color="red", markersize=9, zorder=5,
             label=f"Pico do erro: τ ≈ {tau_pico:.2f}")
    ax1.set_xlabel("Tempo evolutivo τ (adimensional)")
    ax1.set_ylabel("Intensidade (adimensional)")
    ax1.set_title("(A) Curva do erro E(τ)")
    ax1.grid(alpha=0.3)
    ax1.legend(loc="upper right", fontsize=9)

    # ---------- Painel B: g(τ) e c(τ) ----------
    ax2.plot(tau, g, color="tab:red", linewidth=2, label="g(τ): geração de débito")
    ax2.plot(tau, c, color="tab:green", linewidth=2, label="c(τ): quitação pela caridade")
    if tau_reg is not None:
        ax2.axvline(tau_reg, color="purple", linestyle="--", linewidth=1.2)
        ax2.plot(tau_reg, g[i_reg], "o", color="purple", markersize=9, zorder=5,
                 label=f"Início da Regeneração: τ ≈ {tau_reg:.2f}")
    ax2.set_xlabel("Tempo evolutivo τ (adimensional)")
    ax2.set_ylabel("Taxa (adimensional)")
    ax2.set_title("(B) Débito gerado × débito quitado")
    ax2.grid(alpha=0.3)
    ax2.legend(loc="upper right", fontsize=9)

    # ---------- Painel C: S(τ) ----------
    ax3.plot(tau, S, color="tab:purple", linewidth=2.2, label="S(τ): saldo de sofrimento")
    ax3.axhline(0, color="black", linewidth=0.8)
    ax3.plot(tau_smax, S_max, "o", color="red", markersize=9, zorder=5,
             label=f"Máximo: τ ≈ {tau_smax:.2f}, S ≈ {S_max:.2f}")
    if tau_zero is not None:
        ax3.plot(tau_zero, 0, "s", color="green", markersize=9, zorder=5,
                 label=f"Retorno a zero: τ ≈ {tau_zero:.2f}")
    ax3.set_xlabel("Tempo evolutivo τ (adimensional)")
    ax3.set_ylabel("Saldo acumulado (adimensional)")
    ax3.set_title("(C) Saldo de sofrimento S(τ)")
    ax3.grid(alpha=0.3)
    ax3.legend(loc="upper right", fontsize=9)

    fig.suptitle("Figura 5.6 - Erro, débito e reparação ao longo do tempo evolutivo "
                 f"(k_g = {kg:g}, k_c = {kc:g}, τ_M = {tau_M:g})", fontsize=12)
    fig.tight_layout()

    nome = f"figura_5_6_kg_{str(kg).replace('.', '_')}_kc_{str(kc).replace('.', '_')}.png"
    fig.savefig(nome, dpi=200)
    print(f"Figura salva como: {nome}")

    # Resumo no terminal
    print("\nResultados numéricos:")
    print(f"  Pico do erro:            τ ≈ {tau_pico:.2f}   (E_max ≈ {E_pico:.3f})")
    if tau_reg is not None:
        print(f"  Início da Regeneração:   τ ≈ {tau_reg:.2f}   (g = c)")
    else:
        print("  Início da Regeneração:   não ocorreu no intervalo; aumente --tau_max ou k_c")
    print(f"  Máximo de S:             τ ≈ {tau_smax:.2f}   (S_max ≈ {S_max:.3f})")
    if tau_zero is not None:
        print(f"  Retorno de S a zero:     τ ≈ {tau_zero:.2f}")
    else:
        print("  Retorno de S a zero:     não ocorreu no intervalo; aumente --tau_max ou k_c")
    return fig


def main():
    parser = argparse.ArgumentParser(description="Figura 5.6: E(τ) e S(τ).")
    parser.add_argument("--tau_max", type=float, default=14.0,
                        help="Fim do intervalo de tempo τ (padrão: 14)")
    parser.add_argument("--tau_L", type=float, default=1.5,
                        help="Escala de crescimento da liberdade L (padrão: 1.5)")
    parser.add_argument("--tau_M", type=float, default=6.0,
                        help="Ponto de inflexão da maturidade M (padrão: 6)")
    parser.add_argument("--s", type=float, default=1.2,
                        help="Largura da transição de M (padrão: 1.2)")
    parser.add_argument("--kg", type=float, default=0.8,
                        help="Constante de geração de débito k_g (padrão: 0.8)")
    parser.add_argument("--kc", type=float, default=1.0,
                        help="Constante de quitação pela caridade k_c (padrão: 1.0)")
    args = parser.parse_args()

    for nome, valor in [("tau_max", args.tau_max), ("tau_L", args.tau_L),
                        ("s", args.s), ("kg", args.kg), ("kc", args.kc)]:
        if valor <= 0:
            raise ValueError(f"{nome} deve ser positivo.")

    desenhar(args.tau_max, args.tau_L, args.tau_M, args.s, args.kg, args.kc)

    if TEM_TELA:
        plt.show()
    else:
        print("\nAviso: ambiente gráfico não encontrado. O PNG foi salvo, mas a janela não abriu.")


if __name__ == "__main__":
    main()
