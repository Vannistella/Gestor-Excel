
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry

from data_manager import (
    registrar_movimiento,
    leer_movimientos,
    leer_movimientos_filtrados,
    obtener_categorias,
    agregar_categoria,
)
from charts import grafico_torta, grafico_barras


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Ingresos y Egresos")
        self.geometry("950x650")
        self.minsize(750, 550)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_registrar = ttk.Frame(notebook)
        self.tab_datos = ttk.Frame(notebook)
        self.tab_graficos = ttk.Frame(notebook)

        notebook.add(self.tab_registrar, text="Registrar")
        notebook.add(self.tab_datos, text="Ver datos")
        notebook.add(self.tab_graficos, text="Gráficos")

        self._armar_tab_registrar()
        self._armar_tab_datos()
        self._armar_tab_graficos()

        self._refrescar_datos()


    def _armar_tab_registrar(self):
        frame = self.tab_registrar

        ttk.Label(
            frame, text="Registrar movimiento", font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(15, 20), padx=15, sticky="w")

        ttk.Label(frame, text="Tipo:").grid(row=1, column=0, sticky="e", padx=10, pady=6)
        self.tipo_var = tk.StringVar(value="ingreso")
        tipo_frame = ttk.Frame(frame)
        tipo_frame.grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(tipo_frame, text="Ingreso", variable=self.tipo_var, value="ingreso").pack(side="left")
        ttk.Radiobutton(tipo_frame, text="Egreso", variable=self.tipo_var, value="egreso").pack(side="left", padx=(15, 0))

        ttk.Label(frame, text="Fecha:").grid(row=2, column=0, sticky="e", padx=10, pady=6)
        self.fecha_entry = DateEntry(
            frame,
            width=27,
            date_pattern="yyyy-mm-dd",
            locale="es",
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.fecha_entry.grid(row=2, column=1, sticky="w", padx=10)

        ttk.Label(frame, text="Categoría:").grid(row=3, column=0, sticky="e", padx=10, pady=6)
        cat_frame = ttk.Frame(frame)
        cat_frame.grid(row=3, column=1, sticky="w", padx=10)
        self.categoria_var = tk.StringVar()
        self.categoria_combo = ttk.Combobox(
            cat_frame, textvariable=self.categoria_var, width=25,
            values=obtener_categorias(),
        )
        self.categoria_combo.pack(side="left")
        ttk.Button(cat_frame, text="+ Nueva", width=8, command=self._agregar_categoria).pack(
            side="left", padx=(5, 0)
        )

        ttk.Label(frame, text="Descripción:").grid(row=4, column=0, sticky="e", padx=10, pady=6)
        self.descripcion_entry = ttk.Entry(frame, width=40)
        self.descripcion_entry.grid(row=4, column=1, sticky="w", padx=10)

        ttk.Label(frame, text="Monto:").grid(row=5, column=0, sticky="e", padx=10, pady=6)
        self.monto_entry = ttk.Entry(frame, width=30)
        self.monto_entry.grid(row=5, column=1, sticky="w", padx=10)

        ttk.Button(frame, text="Guardar movimiento", command=self._guardar_movimiento).grid(
            row=6, column=0, columnspan=2, pady=25
        )

    def _agregar_categoria(self):
        nombre = simpledialog.askstring("Nueva categoría", "Nombre de la categoría:", parent=self)
        if nombre and nombre.strip():
            agregar_categoria(nombre.strip())
            self.categoria_combo["values"] = obtener_categorias()
            self.categoria_var.set(nombre.strip())

    def _guardar_movimiento(self):
        tipo = self.tipo_var.get()
        fecha = self.fecha_entry.get().strip()
        categoria = self.categoria_var.get().strip()
        descripcion = self.descripcion_entry.get().strip()
        monto_str = self.monto_entry.get().strip()

        if not categoria or not monto_str:
            messagebox.showwarning("Faltan datos", "La categoría y el monto son obligatorios.")
            return

        try:
            monto = float(monto_str)
        except ValueError:
            messagebox.showerror("Monto inválido", "El monto debe ser un número (ej: 15000 o 15000.50).")
            return

        registrar_movimiento(tipo, fecha, categoria, descripcion, monto)
        agregar_categoria(categoria)
        self.categoria_combo["values"] = obtener_categorias()
        messagebox.showinfo("Listo", f"{tipo.capitalize()} registrado correctamente.")

        self.categoria_var.set("")
        self.descripcion_entry.delete(0, tk.END)
        self.monto_entry.delete(0, tk.END)

        self._refrescar_datos()


    def _armar_tab_datos(self):
        frame = self.tab_datos

        filtro_frame = ttk.LabelFrame(frame, text="Filtros")
        filtro_frame.pack(fill="x", padx=10, pady=10)

        self.datos_usar_fecha_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            filtro_frame, text="Filtrar por fecha", variable=self.datos_usar_fecha_var
        ).grid(row=0, column=0, padx=5, pady=8)

        ttk.Label(filtro_frame, text="Desde:").grid(row=0, column=1, padx=5)
        self.datos_fecha_inicio = DateEntry(filtro_frame, width=12, date_pattern="yyyy-mm-dd", locale="es")
        self.datos_fecha_inicio.grid(row=0, column=2, padx=5)

        ttk.Label(filtro_frame, text="Hasta:").grid(row=0, column=3, padx=5)
        self.datos_fecha_fin = DateEntry(filtro_frame, width=12, date_pattern="yyyy-mm-dd", locale="es")
        self.datos_fecha_fin.grid(row=0, column=4, padx=5)

        ttk.Label(filtro_frame, text="Categoría:").grid(row=0, column=5, padx=5)
        self.datos_categoria_var = tk.StringVar(value="Todas")
        self.datos_categoria_combo = ttk.Combobox(
            filtro_frame, textvariable=self.datos_categoria_var, width=18,
            values=["Todas"] + obtener_categorias(), state="readonly",
        )
        self.datos_categoria_combo.grid(row=0, column=6, padx=5)

        ttk.Button(filtro_frame, text="Filtrar", command=self._refrescar_datos).grid(row=0, column=7, padx=5)
        ttk.Button(filtro_frame, text="Quitar filtro", command=self._quitar_filtro_datos).grid(row=0, column=8, padx=5)

        columnas = ("Fecha", "Categoria", "Descripcion", "Monto")

        ttk.Label(frame, text="Ingresos", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10)
        self.tabla_ingresos = ttk.Treeview(frame, columns=columnas, show="headings", height=7)
        for col in columnas:
            self.tabla_ingresos.heading(col, text=col)
            self.tabla_ingresos.column(col, width=150)
        self.tabla_ingresos.pack(fill="x", padx=10, pady=(0, 15))

        ttk.Label(frame, text="Egresos", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10)
        self.tabla_egresos = ttk.Treeview(frame, columns=columnas, show="headings", height=7)
        for col in columnas:
            self.tabla_egresos.heading(col, text=col)
            self.tabla_egresos.column(col, width=150)
        self.tabla_egresos.pack(fill="x", padx=10, pady=(0, 10))

    def _quitar_filtro_datos(self):
        self.datos_usar_fecha_var.set(False)
        self.datos_categoria_var.set("Todas")
        self._refrescar_datos()

    def _refrescar_datos(self):
        fecha_inicio = self.datos_fecha_inicio.get() if self.datos_usar_fecha_var.get() else None
        fecha_fin = self.datos_fecha_fin.get() if self.datos_usar_fecha_var.get() else None
        categoria = self.datos_categoria_var.get()

        hojas = leer_movimientos_filtrados(
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, categoria=categoria
        )

        for fila in self.tabla_ingresos.get_children():
            self.tabla_ingresos.delete(fila)
        for fila in self.tabla_egresos.get_children():
            self.tabla_egresos.delete(fila)

        for _, row in hojas["Ingresos"].iterrows():
            self.tabla_ingresos.insert("", "end", values=list(row))

        for _, row in hojas["Egresos"].iterrows():
            self.tabla_egresos.insert("", "end", values=list(row))


        self.datos_categoria_combo["values"] = ["Todas"] + obtener_categorias()


    def _armar_tab_graficos(self):
        frame = self.tab_graficos

        filtro_frame = ttk.LabelFrame(frame, text="Filtros")
        filtro_frame.pack(fill="x", padx=10, pady=10)

        self.graf_usar_fecha_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            filtro_frame, text="Filtrar por fecha", variable=self.graf_usar_fecha_var
        ).grid(row=0, column=0, padx=5, pady=8)

        ttk.Label(filtro_frame, text="Desde:").grid(row=0, column=1, padx=5)
        self.graf_fecha_inicio = DateEntry(filtro_frame, width=12, date_pattern="yyyy-mm-dd", locale="es")
        self.graf_fecha_inicio.grid(row=0, column=2, padx=5)

        ttk.Label(filtro_frame, text="Hasta:").grid(row=0, column=3, padx=5)
        self.graf_fecha_fin = DateEntry(filtro_frame, width=12, date_pattern="yyyy-mm-dd", locale="es")
        self.graf_fecha_fin.grid(row=0, column=4, padx=5)

        ttk.Label(filtro_frame, text="Categoría (solo gráfico de barras):").grid(row=0, column=5, padx=5)
        self.graf_categoria_var = tk.StringVar(value="Todas")
        self.graf_categoria_combo = ttk.Combobox(
            filtro_frame, textvariable=self.graf_categoria_var, width=18,
            values=["Todas"] + obtener_categorias(), state="readonly",
        )
        self.graf_categoria_combo.grid(row=0, column=6, padx=5)

        botones_frame = ttk.Frame(frame)
        botones_frame.pack(anchor="w", padx=10, pady=(0, 10))

        ttk.Button(
            botones_frame, text="Torta Ingresos",
            command=lambda: self._mostrar_grafico("torta_ingreso"),
        ).pack(side="left", padx=5)
        ttk.Button(
            botones_frame, text="Torta Egresos",
            command=lambda: self._mostrar_grafico("torta_egreso"),
        ).pack(side="left", padx=5)
        ttk.Button(
            botones_frame, text="Barras Ingresos vs Egresos",
            command=lambda: self._mostrar_grafico("barras"),
        ).pack(side="left", padx=5)

        self.canvas_frame = ttk.Frame(frame)
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas_widget = None

    def _mostrar_grafico(self, tipo):
        fecha_inicio = self.graf_fecha_inicio.get() if self.graf_usar_fecha_var.get() else None
        fecha_fin = self.graf_fecha_fin.get() if self.graf_usar_fecha_var.get() else None
        categoria = self.graf_categoria_var.get()

        try:
            if tipo == "torta_ingreso":
                ruta = grafico_torta("ingreso", fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
            elif tipo == "torta_egreso":
                ruta = grafico_torta("egreso", fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
            else:
                ruta = grafico_barras(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, categoria=categoria)
        except ValueError as e:
            messagebox.showwarning("Sin datos", str(e))
            return

        if self.canvas_widget is not None:
            self.canvas_widget.get_tk_widget().destroy()
            plt.close("all")

        img = plt.imread(ruta)
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.imshow(img)
        ax.axis("off")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas_widget = canvas


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
