

import os
import sys

import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt

from data_manager import resumen_por_categoria, resumen_mensual

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def _asegurar_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def grafico_torta(
    tipo: str,
    ruta_planilla: str = None,
    fecha_inicio: str = None,
    fecha_fin: str = None,
) -> str:
    """
    Genera un gráfico de torta con la distribución por categoría
    de "ingreso" o "egreso", mostrando monto y porcentaje.
    Permite filtrar por rango de fechas. Devuelve la ruta del archivo guardado.
    """
    _asegurar_output_dir()

    kwargs = {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin}
    if ruta_planilla:
        kwargs["ruta"] = ruta_planilla

    datos = resumen_por_categoria(tipo, **kwargs)

    if datos.empty:
        raise ValueError(f"No hay datos de {tipo} para graficar todavía.")

    etiqueta = "Ingresos" if tipo.lower().startswith("i") else "Egresos"

    def formato_valor_y_porcentaje(pct):
        valor = pct / 100 * datos.sum()
        valor_formateado = f"{valor:,.0f}".replace(",", ".")
        return f"${valor_formateado}\n({pct:.1f}%)"

    plt.figure(figsize=(6, 6))
    plt.pie(
        datos.values,
        labels=datos.index,
        autopct=formato_valor_y_porcentaje,
        startangle=90,
    )
    plt.title(f"Distribución de {etiqueta} por categoría")
    plt.axis("equal")

    nombre_archivo = os.path.join(OUTPUT_DIR, f"torta_{etiqueta.lower()}.png")
    plt.savefig(nombre_archivo, bbox_inches="tight")
    plt.close()

    return nombre_archivo


def grafico_barras(
    ruta_planilla: str = None,
    fecha_inicio: str = None,
    fecha_fin: str = None,
    categoria: str = None,
) -> str:
    """
    Genera un gráfico de barras comparando Ingresos vs Egresos por mes.
    Permite filtrar por rango de fechas y/o categoría.
    Devuelve la ruta del archivo guardado.
    """
    _asegurar_output_dir()

    kwargs = {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin, "categoria": categoria}
    if ruta_planilla:
        kwargs["ruta"] = ruta_planilla

    df = resumen_mensual(**kwargs)

    if df.empty:
        raise ValueError("No hay datos suficientes para graficar todavía.")

    ax = df.plot(kind="bar", figsize=(8, 5))
    ax.set_title("Ingresos vs Egresos por mes")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Monto")

    for contenedor in ax.containers:
        etiquetas = [
            f"${v:,.0f}".replace(",", ".") if v > 0 else ""
            for v in contenedor.datavalues
        ]
        ax.bar_label(contenedor, labels=etiquetas, fontsize=8, padding=2)

    plt.xticks(rotation=45)
    plt.tight_layout()

    nombre_archivo = os.path.join(OUTPUT_DIR, "barras_ingresos_egresos.png")
    plt.savefig(nombre_archivo, bbox_inches="tight")
    plt.close()

    return nombre_archivo
