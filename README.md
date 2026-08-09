# 💰 Gestor de Ingresos y Egresos

Aplicación en Python que permite registrar ingresos y egresos en una
planilla Excel (con hojas separadas para cada uno), consultar los datos
guardados, y generar gráficos simples (torta y barras) para visualizar la
información.

Tiene **dos formas de uso**:
- 🖥️ **Interfaz gráfica (ventana)** — `src/gui.py` — recomendada para uso normal en tu computador.
- ⌨️ **Consola** — `src/main.py` — útil para servidores o entornos sin pantalla (ej. PythonAnywhere).

## Funcionalidades

1. **Ingreso de datos**: registra movimientos (ingreso o egreso) directamente
   desde la consola, que se guardan en `data/planilla.xlsx` (hojas
   "Ingresos" y "Egresos").
2. **Obtención de datos**: lee y muestra en pantalla todo lo registrado en la
   planilla.
3. **Gráficos**:
   - 🥧 **Torta**: distribución de ingresos o egresos por categoría.
   - 📊 **Barras**: comparación de ingresos vs egresos por mes.

Los gráficos se guardan como imágenes `.png` en la carpeta `output/`.

## Estructura del proyecto

```
gestor-finanzas/
├── data/
│   └── planilla.xlsx        # se crea automáticamente al primer uso
├── output/                  # gráficos generados (.png)
├── src/
│   ├── data_manager.py      # lectura/escritura de la planilla Excel
│   ├── charts.py            # generación de gráficos
│   ├── main.py              # menú de consola (punto de entrada)
│   └── gui.py               # interfaz gráfica con ventanas (Tkinter)
├── requirements.txt
└── README.md
```

## Instalación

```bash
git clone https://github.com/tu-usuario/gestor-finanzas.git
cd gestor-finanzas
python -m venv venv
source venv/bin/activate       # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Uso — Interfaz gráfica (recomendado)

```bash
python src/gui.py
```

Se abre una ventana con 3 pestañas:

- **Registrar**: formulario para agregar un ingreso o egreso (tipo, fecha mediante calendario desplegable, categoría, descripción, monto).
- **Ver datos**: tablas con todos los movimientos registrados, con botón de refrescar.
- **Gráficos**: botones para generar y ver directamente en la ventana el gráfico de torta (ingresos o egresos) y el de barras (ingresos vs egresos por mes).

> ⚠️ La interfaz gráfica necesita un entorno con pantalla (tu computador). No funciona en consolas remotas sin interfaz gráfica, como la consola Bash de PythonAnywhere en el plan gratuito — para eso usa la versión de consola.

## Uso — Consola

```bash
python src/main.py
```

Vas a ver un menú como este:

```
===== GESTOR DE INGRESOS Y EGRESOS =====
1. Registrar ingreso
2. Registrar egreso
3. Ver datos actuales
4. Generar gráfico de torta (por categoría)
5. Generar gráfico de barras (ingresos vs egresos por mes)
6. Salir
```

La primera vez que registres un movimiento, se crea automáticamente el
archivo `data/planilla.xlsx` con las hojas "Ingresos" y "Egresos".

## Formato de la planilla

Cada hoja (Ingresos / Egresos) tiene las columnas:

| Fecha       | Categoria  | Descripcion         | Monto  |
|-------------|------------|---------------------|--------|
| 2026-07-05  | Sueldo     | Sueldo mensual      | 900000 |

Puedes editar la planilla directamente en Excel/LibreOffice si prefieres
cargar datos masivamente, y la app los leerá igual.

## Próximas mejoras posibles

- Interfaz gráfica (Tkinter o web con Flask/Streamlit).
- Edición y eliminación de movimientos existentes.
- Filtros por rango de fechas.
- Exportar los gráficos directamente a un reporte PDF.

## Licencia

MIT
