

from data_manager import registrar_movimiento, leer_movimientos, DEFAULT_PATH
from charts import grafico_torta, grafico_barras


def menu():
    print("\n===== GESTOR DE INGRESOS Y EGRESOS =====")
    print(f"Planilla en uso: {DEFAULT_PATH}\n")
    print("1. Registrar ingreso")
    print("2. Registrar egreso")
    print("3. Ver datos actuales")
    print("4. Generar gráfico de torta (por categoría)")
    print("5. Generar gráfico de barras (ingresos vs egresos por mes)")
    print("6. Salir")
    return input("\nElige una opción: ").strip()


def pedir_datos_movimiento():
    fecha = input("Fecha (YYYY-MM-DD, Enter para hoy): ").strip()
    categoria = input("Categoría (ej: Sueldo, Arriendo, Comida): ").strip()
    descripcion = input("Descripción: ").strip()
    while True:
        try:
            monto = float(input("Monto: ").strip())
            break
        except ValueError:
            print("Monto inválido, ingresa solo números.")
    return fecha, categoria, descripcion, monto


def main():
    while True:
        opcion = menu()

        if opcion == "1":
            fecha, categoria, descripcion, monto = pedir_datos_movimiento()
            registrar_movimiento("ingreso", fecha, categoria, descripcion, monto)
            print("✅ Ingreso registrado.")

        elif opcion == "2":
            fecha, categoria, descripcion, monto = pedir_datos_movimiento()
            registrar_movimiento("egreso", fecha, categoria, descripcion, monto)
            print("✅ Egreso registrado.")

        elif opcion == "3":
            hojas = leer_movimientos()
            for nombre, df in hojas.items():
                print(f"\n--- {nombre} ---")
                print(df.to_string(index=False) if not df.empty else "(sin datos)")

        elif opcion == "4":
            tipo = input("¿Torta de 'ingreso' o 'egreso'?: ").strip().lower()
            try:
                ruta = grafico_torta(tipo)
                print(f"✅ Gráfico guardado en: {ruta}")
            except ValueError as e:
                print(f"⚠️  {e}")

        elif opcion == "5":
            try:
                ruta = grafico_barras()
                print(f"✅ Gráfico guardado en: {ruta}")
            except ValueError as e:
                print(f"⚠️  {e}")

        elif opcion == "6":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    main()
