"""
Figura 5.2 e 5.3 - A mesma pedra lançada em três águas, com o gráfico de D_total(ρ).

Modelo: a amplitude do anel de ordem n é a_n = ρ^n.
  ρ > 1  -> a onda cresce (amplificador)
  ρ = 1  -> a amplitude é constante (ressonante)
  ρ < 1  -> a onda se dissipa (dissipativo)

Dano total (série geométrica): D_total = D0 / (1 - ρ), válido para ρ < 1.

Uso no terminal do VS Code:
    python pedra_no_lago.py --rho 1.25
    python pedra_no_lago.py --rho 1 --animar
    python pedra_no_lago.py --rho 0.6 --raio 10 --animar
"""

import argparse
import os

import matplotlib

TEM_TELA = bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
if not TEM_TELA:
    # Sem ambiente gráfico: usa backend sem janela e salva só o PNG
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

D0 = 1.0  # dano primário, em unidades arbitrárias (D0 = 1 é a referência)


def classificar(rho):
    """Nome do regime de propagação para o valor de ρ."""
    if np.isclose(rho, 1.0):
        return "Ressonante (ρ = 1): amplitude constante"
    if rho > 1.0:
        return "Amplificador (ρ > 1): a onda cresce"
    return "Dissipativo (ρ < 1): a onda se dissipa"


def amplitude_maxima(rho, raio_max):
    """Maior valor da envoltória no intervalo, usado para fixar a escala."""
    return max(1.0, rho ** raio_max)


def desenhar(rho, raio_max):
    """Desenha os três painéis (mapa 2D, corte radial e D_total) e salva o PNG."""
    # Painel 1 e 2: malha 2D, Z = ρ^R · cos(2πR), com R = √(x² + y²)
    x = np.linspace(-raio_max, raio_max, 500)
    X, Y = np.meshgrid(x, x)
    R = np.sqrt(X ** 2 + Y ** 2)
    Z = (rho ** R) * np.cos(2 * np.pi * R)

    amp = amplitude_maxima(rho, raio_max)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6))

    # ---------- Painel 1: vista de cima ----------
    im = ax1.imshow(Z, extent=[-raio_max, raio_max, -raio_max, raio_max],
                    origin="lower", cmap="RdBu_r", vmin=-amp, vmax=amp)
    fig.colorbar(im, ax=ax1, label="Altura da água (adimensional)")
    ax1.plot(0, 0, "ko", markersize=5)  # ponto de impacto da pedra
    ax1.set_title("Vista de cima: vermelho = cristas, azul = vales")
    ax1.set_xlabel("x (distância em anéis)")
    ax1.set_ylabel("y (distância em anéis)")
    ax1.set_aspect("equal")

    # ---------- Painel 2: corte radial e envoltória ----------
    r = np.linspace(0, raio_max, 1000)
    envoltoria = rho ** r
    ax2.plot(r, envoltoria * np.cos(2 * np.pi * r), color="tab:blue",
             linewidth=1.5, label="Perfil da onda")
    ax2.plot(r, envoltoria, "--", color="tab:red", label="Envoltória +ρ^r")
    ax2.plot(r, -envoltoria, "--", color="tab:red", label="Envoltória −ρ^r")
    ax2.axhline(0, color="black", linewidth=0.8)
    ax2.set_ylim(-1.1 * amp, 1.1 * amp)
    ax2.set_xlabel("Raio r (em anéis)")
    ax2.set_ylabel("Amplitude (adimensional)")
    ax2.set_title("Corte radial da onda")
    ax2.grid(alpha=0.3)
    ax2.legend(loc="upper right")

    # ---------- Painel 3: D_total(ρ) = D0 / (1 − ρ) ----------
    rho_grade = np.linspace(0, 0.99, 500)   # a fórmula só vale para ρ < 1
    d_total_grade = D0 / (1 - rho_grade)
    ax3.plot(rho_grade, d_total_grade, color="tab:green", linewidth=2,
             label="D_total(ρ) = D₀ / (1 − ρ)")
    ax3.axvline(1.0, color="gray", linestyle="--", label="ρ = 1 (limiar)")
    ax3.set_xlim(0, 1.05)
    ax3.set_ylim(0, 20)
    ax3.set_xlabel("Coeficiente de reverberação ρ")
    ax3.set_ylabel("Dano total D_total / D₀")
    ax3.set_title("Dano total em função de ρ (Figura 5.3)")
    ax3.grid(alpha=0.3)

    if rho < 1:
        d_agora = D0 / (1 - rho)
        ax3.plot(rho, d_agora, "o", color="red", markersize=9, label="Caso atual")
        ax3.annotate(f"ρ = {rho:.2f}\nD_total/D₀ = {d_agora / D0:.2f}",
                     xy=(rho, d_agora),
                     xytext=(min(rho + 0.03, 0.75), min(d_agora + 2, 18)),
                     arrowprops=dict(arrowstyle="->", color="red"),
                     color="red")
        texto = f"D_total / D₀ = 1 / (1 − ρ) = {1 / (1 - rho):.2f}"
    else:
        ax3.text(0.5, 10, "ρ ≥ 1: a soma diverge\n(fora do domínio da fórmula)",
                 ha="center", color="red")
        texto = "D_total diverge (soma infinita sem limite)"
    ax3.legend(loc="upper left")

    fig.suptitle(f"A mesma pedra em três águas — ρ = {rho:.2f}\n"
                 f"{classificar(rho)}   |   {texto}", fontsize=12)
    fig.tight_layout()

    nome = f"figura_5_2_rho_{str(round(rho, 2)).replace('.', '_')}.png"
    fig.savefig(nome, dpi=200)
    print(f"Figura salva como: {nome}")
    return fig


def animar(rho, raio_max):
    """Animação: as cristas se afastam do centro ao longo do tempo."""
    r = np.linspace(0, raio_max, 800)
    envoltoria = rho ** r
    amp = amplitude_maxima(rho, raio_max)

    fig, ax = plt.subplots(figsize=(10, 5))
    linha, = ax.plot(r, envoltoria * np.cos(2 * np.pi * r),
                     color="tab:blue", linewidth=1.8)
    ax.plot(r, envoltoria, "--", color="tab:red", alpha=0.6)
    ax.plot(r, -envoltoria, "--", color="tab:red", alpha=0.6)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylim(-1.1 * amp, 1.1 * amp)
    ax.set_xlabel("Raio r (em anéis)")
    ax.set_ylabel("Amplitude (adimensional)")
    ax.set_title(f"Propagação da onda — ρ = {rho:.2f}")
    ax.grid(alpha=0.3)

    def atualizar(quadro):
        t = quadro / 30.0  # tempo em ciclos
        # y(r, t) = ρ^r · cos(2π(r − t))
        linha.set_ydata(envoltoria * np.cos(2 * np.pi * (r - t)))
        return (linha,)

    anim = FuncAnimation(fig, atualizar, frames=120, interval=40, blit=True)
    return anim


def main():
    parser = argparse.ArgumentParser(description="Figuras 5.2 e 5.3: a pedra em três águas.")
    parser.add_argument("--rho", type=float, default=None,
                        help="Coeficiente de reverberação ρ (ex.: 1.25, 1 ou 0.6)")
    parser.add_argument("--raio", type=float, default=8.0,
                        help="Raio máximo da figura, em anéis (padrão: 8)")
    parser.add_argument("--animar", action="store_true",
                        help="Abre também a animação da onda se propagando")
    args = parser.parse_args()

    rho = args.rho if args.rho is not None else float(input("Informe o valor de ρ: "))
    if rho <= 0:
        raise ValueError("ρ deve ser positivo.")

    print(f"Regime: {classificar(rho)}")
    print(" anel n | amplitude a_n = ρ^n")
    for k in range(6):
        print(f"   {k}   |   {rho ** k:.4f}")

    desenhar(rho, args.raio)

    # A referência 'anim' precisa existir até o fim, senão a animação some
    anim = animar(rho, args.raio) if args.animar else None

    if TEM_TELA:
        plt.show()
    else:
        print("\nAviso: ambiente gráfico não encontrado. O PNG foi salvo, mas a janela não abriu.")
        print("Verifique o WSLg com: echo $DISPLAY")


if __name__ == "__main__":
    main()
