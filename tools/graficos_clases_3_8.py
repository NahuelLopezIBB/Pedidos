#!/usr/bin/env python3
"""Gráficos del resumen de las clases 3 a 8 (estilo para pantalla e-ink en grises).

Uso: python3 tools/graficos_clases_3_8.py  ->  pedidos/img/clases-3-a-8/*.png
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "pedidos" / "img" / "clases-3-a-8"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.size": 13, "axes.titlesize": 14, "axes.labelsize": 13,
    "axes.linewidth": 1.2, "lines.linewidth": 2.4,
    "axes.spines.top": False, "axes.spines.right": False,
    "savefig.dpi": 110, "savefig.bbox": "tight", "savefig.facecolor": "white",
})
K, G, L = "black", "0.45", "0.75"   # negro, gris medio, gris claro


def ejes(ax, xl, yl, ticks=False):
    ax.set_xlabel(xl)
    ax.set_ylabel(yl)
    if not ticks:
        ax.set_xticks([])
        ax.set_yticks([])
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)


def guardar(fig, nombre):
    fig.savefig(OUT / f"{nombre}.png")
    plt.close(fig)


def fig(w=6.4, h=4.4):
    return plt.subplots(figsize=(w, h))


# ------------------------------------------------------------------ clase 3
def indiferencia():
    f, ax = fig()
    x = np.linspace(0.4, 10, 300)
    for u, c, lab, xl in [(4, L, "U1", 1.6), (8, G, "U2", 2.4), (14, K, "U3", 3.3)]:
        ax.plot(x, u / x, color=c)
        ax.text(xl + 0.1, u / xl + 0.1, lab)
    ax.annotate("más preferidas", xy=(5.5, 4.2), xytext=(2.2, 7.5),
                arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ejes(ax, "Bien x", "Bien y")
    ax.set_title("Mapa de indiferencia")
    guardar(f, "c3-indiferencia")


def equilibrio_consumidor():
    f, ax = fig()
    Y, px, py = 10, 1, 1
    x = np.linspace(0.3, 10, 300)
    ax.plot(x, Y / py - px / py * x, color=K, label="Recta de presupuesto")
    for u, c in [(12, L), (25, G), (40, L)]:
        ax.plot(x, u / x, color=c, ls="--" if u == 40 else "-")
    ax.plot(5, 5, "o", color=K, ms=8)
    ax.annotate("Equilibrio:\nRMS = Px/Py", xy=(5, 5), xytext=(6.3, 6.6),
                arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(0.2, 10.2, "Y/Py"); ax.text(9.6, 0.3, "Y/Px")
    ax.text(8.2, 5.2, "inalcanzable", color=G, fontsize=11)
    ax.set_xlim(0, 11); ax.set_ylim(0, 11)
    ejes(ax, "Bien x", "Bien y")
    ax.legend(loc="upper right", frameon=False)
    ax.set_title("Equilibrio del consumidor")
    guardar(f, "c3-equilibrio")


def demanda_mov_desp():
    f, ax = fig()
    q = np.linspace(0, 10, 100)
    ax.plot(q, 10 - q, color=K, label="D")
    ax.plot(q, 13 - q, color=G, ls="--", label="D1 (más ingreso)")
    ax.plot([3, 5], [7, 5], "o", color=K)
    ax.annotate("", xy=(5, 5), xytext=(3, 7), arrowprops=dict(arrowstyle="->", lw=2))
    ax.text(0.4, 4.6, "cambio de precio:\nmovimiento por D", fontsize=11)
    ax.annotate("", xy=(7, 6), xytext=(4.6, 5.9), arrowprops=dict(arrowstyle="->", lw=2, color=G))
    ax.text(7.4, 6.6, "desplazamiento\nde la curva", fontsize=11, color=G)
    ax.set_xlim(0, 12); ax.set_ylim(0, 13)
    ejes(ax, "Cantidad", "Precio")
    ax.legend(frameon=False)
    ax.set_title("Movimiento y desplazamiento")
    guardar(f, "c3-demanda")


def excedente_consumidor():
    f, ax = fig()
    q = np.linspace(0, 10, 100)
    ax.plot(q, 10 - q, color=K, label="Demanda")
    p0 = 4
    ax.fill_between(q[q <= 6], 10 - q[q <= 6], p0, color=L, label="Excedente del consumidor")
    ax.fill_between([0, 6], 0, p0, color="0.9", hatch="//", edgecolor=G, label="Gasto (p·q)")
    ax.axhline(p0, color=G, lw=1.2, xmax=0.6)
    ax.set_xlim(0, 10); ax.set_ylim(0, 11)
    ejes(ax, "Cantidad", "Precio")
    ax.text(-0.5, p0, "p", va="center")
    ax.legend(frameon=False)
    ax.set_title("Excedente del consumidor")
    guardar(f, "c3-excedente")


def elasticidad_ingreso_total():
    f, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 6.6), sharex=True)
    q = np.linspace(0, 10, 200)
    a1.plot(q, 10 - q, color=K)
    a1.plot(5, 5, "o", color=K)
    a1.text(1.3, 8.2, "e > 1 (elástica)"); a1.text(6.3, 1.6, "e < 1 (inelástica)")
    a1.text(5.3, 5.4, "e = 1")
    a1.set_ylabel("Precio"); a1.set_xticks([]); a1.set_yticks([])
    a1.set_ylim(0, 10.5); a1.set_title("Demanda lineal")
    a2.plot(q, q * (10 - q), color=K)
    a2.axvline(5, color=G, ls=":", lw=1.5)
    a2.text(5.2, 3, "IT máximo\ncon e = 1", fontsize=11)
    a2.set_ylabel("Ingreso total"); a2.set_xlabel("Cantidad")
    a2.set_xticks([]); a2.set_yticks([]); a2.set_ylim(0, 28)
    a2.set_title("Ingreso total (gasto)")
    guardar(f, "c3-elasticidad")


# ------------------------------------------------------------------ clase 4
L_TRAB = np.arange(0, 9)
Q_TRIGO = np.array([0, 19, 36, 51, 64, 75, 84, 91, 96])


def producto_total_marginal():
    f, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 3.9))
    a1.plot(L_TRAB, Q_TRIGO, "-o", color=K, ms=5)
    a1.set_title("Producto total (PT)")
    a1.set_xlabel("Trabajadores"); a1.set_ylabel("Trigo (fanegas)")
    a1.set_xlim(0, 8.5); a1.set_ylim(0, 105)
    pmg = np.diff(Q_TRIGO)
    a2.plot(L_TRAB[:-1] + 0.5, pmg, "-o", color=K, ms=5)
    a2.set_title("Producto marginal (PMgL)")
    a2.set_xlabel("Trabajadores"); a2.set_ylabel("Fanegas por trabajador")
    a2.set_xlim(0, 8.5); a2.set_ylim(0, 21)
    f.suptitle("Granja de George y Martha: rendimientos decrecientes", y=1.02)
    guardar(f, "c4-producto")


def costo_total():
    f, ax = fig()
    ct = 400 + 200 * L_TRAB
    ax.plot(Q_TRIGO, ct, "-o", color=K, ms=5, label="CT = CF + CV")
    ax.axhline(400, color=G, ls="--", lw=1.5, label="CF = 400 $")
    ax.set_xlim(0, 100); ax.set_ylim(0, 2100)
    ax.set_xlabel("Trigo (fanegas)"); ax.set_ylabel("Costo ($)")
    ax.legend(frameon=False, loc="upper left")
    ax.set_title("Costo total: cada vez más empinado")
    guardar(f, "c4-costo-total")


def costos_medios():
    q = np.arange(1, 11)
    cv = np.array([12, 48, 108, 192, 300, 432, 588, 768, 972, 1200])
    cf = 108
    cmg = np.diff(np.concatenate([[0], cv]))
    f, ax = fig(6.6, 4.6)
    ax.plot(q - 0.5, cmg, color=K, label="CMg")
    ax.plot(q, (cf + cv) / q, color=K, ls="--", label="CTMe")
    ax.plot(q, cv / q, color=G, label="CVMe")
    ax.plot(q, cf / q, color=L, label="CFMe")
    ax.plot(3, 72, "o", color=K, ms=8)
    ax.annotate("M: mínimo del CTMe\n(lo corta el CMg)", xy=(3, 72), xytext=(4.3, 150),
                arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 250)
    ax.set_xlabel("Cajas de salsa por día"); ax.set_ylabel("Costo por caja ($)")
    ax.legend(frameon=False, loc="upper left")
    ax.set_title("Familia de curvas de costo (Selena's)")
    guardar(f, "c4-costos-medios")


def largo_plazo():
    f, ax = fig()
    q = np.linspace(0.5, 10, 300)
    lp = 3 + 0.12 * (q - 5.5) ** 2
    ax.plot(q, lp, color=K, lw=3, label="CTMe a largo plazo")
    for q0 in [2.5, 5.5, 8.5]:
        cp = lp + 0.25 * (q - q0) ** 2
        m = (cp < 7.5)
        ax.plot(q[m], cp[m] + 0.02, color=G, lw=1.6)
    ax.text(0.9, 6.5, "Curvas de\ncorto plazo\n(una por planta)", color=G, fontsize=11)
    ax.text(1.3, 1.3, "economías\nde escala", fontsize=11)
    ax.text(7.4, 1.3, "deseconomías\nde escala", fontsize=11)
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 8)
    ejes(ax, "Cantidad", "Costo medio")
    ax.legend(frameon=False, loc="upper right")
    ax.set_title("Corto y largo plazo")
    guardar(f, "c4-largo-plazo")


# ------------------------------------------------------------------ clase 5
def firma_competitiva():
    f, ax = fig(6.6, 4.6)
    q = np.linspace(0.6, 10, 300)
    cvme = q ** 2 / 12 - q + 5
    ctme = cvme + 12 / q
    cmg = q ** 2 / 4 - 2 * q + 5
    m = q >= 2
    ax.plot(q[m], cmg[m], color=K, label="CMg (oferta)")
    ax.plot(q, ctme, color=K, ls="--", label="CTMe")
    ax.plot(q, cvme, color=G, label="CVMe")
    p = 7
    ax.axhline(p, color=K, lw=1.2)
    ax.text(9.2, p + 0.25, "p = IMg")
    qe = (2 + np.sqrt(4 + p - 5)) * 2
    ce = np.interp(qe, q, ctme)
    ax.fill_between([0, qe], ce, p, color=L, label="Beneficio")
    ax.plot(qe, p, "o", color=K)
    ax.plot(6, 2, "o", color=K)
    ax.annotate("punto de cierre\n(mínimo del CVMe)", xy=(6, 2), xytext=(6.9, 0.4),
                arrowprops=dict(arrowstyle="->", lw=1.3), fontsize=11)
    ax.set_xlim(0, 10); ax.set_ylim(0, 11)
    ejes(ax, "Cantidad", "Precio y costos")
    ax.legend(frameon=False, loc="upper center", fontsize=11)
    ax.set_title("Empresa en competencia perfecta: p = CMg")
    guardar(f, "c5-firma")


def equilibrio_mercado():
    f, ax = fig()
    p = np.linspace(0, 26, 100)
    ax.plot(20 - 0.75 * p, p, color=K, label="Demanda: x = 20 − 0,75p")
    ax.plot(4 + 0.25 * p, p, color=G, label="Oferta: x = 4 + 0,25p")
    ax.plot(8, 16, "o", color=K, ms=8)
    ax.plot([0, 8, 8], [16, 16, 0], ":", color=K, lw=1.3)
    ax.text(8.3, 16.6, "p = 16, x = 8")
    ax.plot([20 - 0.75 * 22, 4 + 0.25 * 22], [22, 22], color=L, lw=5)
    ax.text(5, 23, "excedente con p = 22", fontsize=11, color=G)
    ax.set_xlim(0, 16); ax.set_ylim(0, 27)
    ax.set_xlabel("Cantidad"); ax.set_ylabel("Precio")
    ax.legend(frameon=False, loc="lower right", fontsize=11)
    ax.set_title("Equilibrio de mercado (ejemplo del apunte)")
    guardar(f, "c5-mercado")


def monopolio():
    f, ax = fig(6.6, 4.6)
    x = np.linspace(0, 10, 200)
    ax.plot(x, 10 - x, color=K, label="Demanda (IMe)")
    ax.plot(x[x <= 5], 10 - 2 * x[x <= 5], color=K, ls="--", label="IMg")
    ax.plot(x, 1 + 0.8 * x, color=G, label="CMg")
    qm = 9 / 2.8; pm = 10 - qm
    qc = 9 / 1.8; pc = 10 - qc
    ax.fill([qm, qc, qm], [pm, pc, 1 + 0.8 * qm], color=L, label="Pérdida de excedente")
    ax.plot([0, qm, qm], [pm, pm, 0], ":", color=K, lw=1.3)
    ax.plot([0, qc, qc], [pc, pc, 0], ":", color=G, lw=1.3)
    ax.text(qm - 0.15, 0.25, "qm", ha="right"); ax.text(qc + 0.15, 0.25, "qc")
    ax.text(0.15, pm + 0.2, "pm"); ax.text(0.15, pc - 0.5, "pc")
    ax.plot(qm, pm, "o", color=K)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10.5)
    ejes(ax, "Cantidad", "Precio")
    ax.legend(frameon=False, loc="upper right", fontsize=11)
    ax.set_title("Monopolio: IMg = CMg")
    guardar(f, "c5-monopolio")


def impuestos_monopolio():
    f, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 3.9), sharey=True)
    x = np.linspace(0.3, 10, 200)
    for ax, tit in [(a1, "Impuesto específico"), (a2, "Impuesto fijo")]:
        ax.plot(x, 10 - x, color=K)
        ax.plot(x[x <= 5], 10 - 2 * x[x <= 5], color=K, ls="--")
        ax.set_title(tit); ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlim(0, 10); ax.set_ylim(0, 10.5); ax.set_xlabel("Cantidad")
    a1.plot(x, 1 + 0.8 * x, color=G, label="CMg")
    a1.plot(x, 2.5 + 0.8 * x, color=K, lw=1.6, label="CMg + impuesto")
    a1.text(0.5, 0.6, "sube el precio,\nbaja la cantidad", fontsize=11)
    a1.legend(frameon=False, fontsize=10, loc="upper right")
    a2.plot(x, 1 + 0.8 * x, color=G, label="CMg (no cambia)")
    a2.text(0.5, 0.6, "mismo precio y cantidad,\nmenos beneficio", fontsize=11)
    a2.legend(frameon=False, fontsize=10, loc="upper right")
    a1.set_ylabel("Precio")
    guardar(f, "c5-impuestos")


# ------------------------------------------------------------------ clase 6
def edgeworth():
    f, ax = fig(6, 5.4)
    W, H = 10, 8
    x = np.linspace(0.3, W - 0.3, 300)
    for tt in [0.35, 0.5, 0.65]:
        u = tt ** 2 * W * H
        y = u / x
        m = (y < H)
        ax.plot(x[m], y[m], color=K, lw=1.8)
        ub = (1 - tt) ** 2 * W * H
        yb = H - ub / (W - x)
        m = (yb > 0)
        ax.plot(x[m], yb[m], color=G, lw=1.8, ls="--")
        ax.plot(tt * W, tt * H, "o", color=K, ms=5)
    t = np.linspace(0, 1, 50)
    ax.plot(W * t, H * t, color=K, lw=3, alpha=0.6, label="Curva de contrato")
    ax.plot(2.2, 5.2, "o", color=K)
    ax.text(2.4, 5.4, "R (no óptimo)", fontsize=11)
    ax.text(-0.5, -0.5, "0A"); ax.text(W + 0.1, H + 0.1, "0B")
    ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ["top", "right"]:
        ax.spines[s].set_visible(True)
    ax.set_xlabel("Bien X"); ax.set_ylabel("Bien Y")
    ax.legend(frameon=False, loc="upper left", fontsize=11)
    ax.set_title("Caja de Edgeworth\nA: continuas, B: cortadas", pad=14)
    guardar(f, "c6-edgeworth")


def frontera_transformacion():
    f, ax = fig()
    t = np.linspace(0, np.pi / 2, 200)
    ax.plot(10 * np.cos(t), 10 * np.sin(t), color=K, label="Curva de transformación")
    x0 = 10 * np.cos(np.pi / 4); y0 = 10 * np.sin(np.pi / 4)
    xx = np.linspace(3, 11, 10)
    ax.plot(xx, y0 - (xx - x0), color=G, ls="--", label="Pendiente = RTP = Px/Py")
    ax.plot(x0, y0, "o", color=K)
    ax.plot(4, 4, "o", color=G)
    ax.text(4.2, 3.3, "ineficiente\n(recursos ociosos)", fontsize=11)
    ax.text(8.5, 9, "inalcanzable", color=G, fontsize=11)
    ax.set_xlim(0, 12); ax.set_ylim(0, 12)
    ejes(ax, "Bien k", "Bien j")
    ax.legend(frameon=False, loc="upper right", fontsize=11)
    ax.set_title("Óptimo general: RMS = RTP")
    guardar(f, "c6-transformacion")


def bienestar_social():
    f, ax = fig()
    t = np.linspace(0, np.pi / 2, 200)
    ax.plot(9 * np.cos(t), 9 * np.sin(t), color=K, label="Posibilidades de utilidad")
    u = np.linspace(1, 12, 200)
    for c, col in [(28, L), (40.5, G), (60, L)]:
        ax.plot(u, c / u, color=col, ls="--")
    p = 9 / np.sqrt(2)
    ax.plot(p, p, "o", color=K, ms=8)
    ax.text(p + 0.3, p + 0.3, "P: óptimo social")
    ax.plot(3, 3.5, "o", color=G)
    ax.text(1.3, 2.4, "M (no óptimo)", fontsize=11)
    ax.text(8.2, 1.8, "curvas de la\nfunción de bienestar", fontsize=10, color=G)
    ax.set_xlim(0, 12); ax.set_ylim(0, 12)
    ejes(ax, "Utilidad del individuo 1", "Utilidad del individuo 2")
    ax.legend(frameon=False, loc="upper right", fontsize=11)
    ax.set_title("Función social de bienestar")
    guardar(f, "c6-bienestar")


# ------------------------------------------------------------------ clase 7
def ciclo():
    f, ax = fig(7, 4)
    t = np.linspace(0, 10, 400)
    y = 1 + 0.25 * t + 0.6 * np.sin(1.4 * t)
    ax.plot(t, y, color=K)
    ax.plot(t, 1 + 0.25 * t, color=G, ls=":", lw=1.5, label="tendencia (crecimiento)")
    picos = [t[i] for i in range(1, 399) if y[i] > y[i - 1] and y[i] > y[i + 1]]
    valles = [t[i] for i in range(1, 399) if y[i] < y[i - 1] and y[i] < y[i + 1]]
    for i, (a, b) in enumerate(zip(picos, valles)):
        ax.axvspan(a, b, color=L, label="recesión" if i == 0 else None)
    ax.plot(picos[0], np.interp(picos[0], t, y), "o", color=K)
    ax.text(picos[0] - 0.3, np.interp(picos[0], t, y) + 0.25, "pico")
    ax.plot(valles[0], np.interp(valles[0], t, y), "o", color=K)
    ax.text(valles[0] - 0.3, np.interp(valles[0], t, y) - 0.45, "valle")
    ax.set_xlim(0, 10)
    ejes(ax, "Tiempo", "Producción / empleo")
    ax.legend(frameon=False, loc="upper left", fontsize=11)
    ax.set_title("El ciclo económico")
    guardar(f, "c7-ciclo")


def pib_nominal_real():
    f, ax = fig(6, 4)
    labels = ["Año 1", "Año 2\nnominal", "Año 2\nreal (precios año 1)"]
    vals = [1000, 1500, 1150]
    bars = ax.bar(labels, vals, color=[G, K, L], edgecolor=K)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 25, f"{v:,}".replace(",", "."), ha="center")
    ax.text(1, 750, "+50 %", ha="center", color="white", fontsize=14); ax.text(2, 575, "+15 %", ha="center", fontsize=14)
    ax.set_ylim(0, 1800); ax.set_yticks([])
    ax.set_ylabel("Millones de $")
    ax.set_title("PIB nominal y real (manzanas y naranjas)")
    guardar(f, "c7-pib")


def desempleo_estructural():
    f, ax = fig()
    L_ = np.linspace(0, 10, 100)
    ax.plot(L_, 10 - L_, color=K, label="Demanda de trabajo")
    ax.plot(L_, L_, color=G, label="Oferta de trabajo")
    ax.axhline(7, color=K, ls="--", lw=1.5)
    ax.text(0.2, 7.3, "salario mínimo (arriba del de equilibrio)", fontsize=11)
    ax.annotate("", xy=(7, 6.4), xytext=(3, 6.4), arrowprops=dict(arrowstyle="<->", lw=2))
    ax.text(3.4, 5.6, "desempleo estructural", fontsize=11)
    ax.plot(5, 5, "o", color=K)
    ax.text(5.3, 4.6, "WE")
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ejes(ax, "Cantidad de trabajo", "Salario")
    ax.legend(frameon=False, loc="lower right", fontsize=11)
    ax.set_title("Desempleo estructural")
    guardar(f, "c7-desempleo")


def crecimiento_desempleo():
    rng = np.random.default_rng(3)
    g = rng.uniform(-3, 7, 45)
    du = -0.45 * (g - 3) + rng.normal(0, 0.45, 45)
    f, ax = fig()
    ax.scatter(g, du, color=K, s=22)
    ax.axhline(0, color=G, lw=1); ax.axvline(3, color=G, lw=1, ls="--")
    ax.text(3.15, 2.7, "crecimiento\npromedio", fontsize=11, color=G)
    ax.set_xlabel("Crecimiento del PIB real (%)")
    ax.set_ylabel("Variación del desempleo (pp)")
    ax.set_title("Crecer más que el promedio baja el desempleo")
    ax.text(-2.9, -2.3, "datos ilustrativos", fontsize=10, color=G)
    guardar(f, "c7-okun")


# ------------------------------------------------------------------ clase 8
def produccion_agregada():
    f, ax = fig()
    k = np.linspace(0, 10, 200)
    ax.plot(k, 3 * np.sqrt(k), color=K, label="Tecnología inicial")
    ax.plot(k, 4.2 * np.sqrt(k), color=G, ls="--", label="Con progreso tecnológico")
    for a, b in [(1, 2), (8, 9)]:
        ax.plot([a, b, b], [3 * np.sqrt(a)] * 2 + [3 * np.sqrt(b)], color=K, lw=1.2)
    ax.text(2.1, 3.1, "gran aumento", fontsize=11)
    ax.text(6.4, 7.3, "aumento chico", fontsize=11)
    ax.set_xlim(0, 10); ax.set_ylim(0, 14)
    ejes(ax, "Capital físico por trabajador", "PIB real por trabajador")
    ax.legend(frameon=False, loc="upper left", fontsize=11)
    ax.set_title("Función de producción agregada")
    guardar(f, "c8-produccion")


def regla_70():
    f, ax = fig()
    t = np.arange(0, 51)
    for g, c, ls in [(1, L, "-"), (2, G, "-"), (3.5, K, "--"), (7, K, "-")]:
        ax.plot(t, (1 + g / 100) ** t, color=c, ls=ls, label=f"{str(g).replace('.', ',')} % anual: se duplica en ≈{70 / g:.0f} años")
    ax.axhline(2, color=G, lw=1, ls=":")
    ax.set_ylim(0, 8); ax.set_xlim(0, 50)
    ax.set_xlabel("Años"); ax.set_ylabel("Ingreso (inicio = 1)")
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    ax.set_title("Regla del 70")
    guardar(f, "c8-regla70")


if __name__ == "__main__":
    for fn in [indiferencia, equilibrio_consumidor, demanda_mov_desp, excedente_consumidor,
               elasticidad_ingreso_total, producto_total_marginal, costo_total, costos_medios,
               largo_plazo, firma_competitiva, equilibrio_mercado, monopolio, impuestos_monopolio,
               edgeworth, frontera_transformacion, bienestar_social, ciclo, pib_nominal_real,
               desempleo_estructural, crecimiento_desempleo, produccion_agregada, regla_70]:
        fn()
    print("OK:", len(list(OUT.glob("*.png"))), "gráficos en", OUT)
