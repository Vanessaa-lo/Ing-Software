from db_config import conectar_bd
from datetime import datetime

def prueba_insercion_ventas():
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()

        print("⏳ Insertando venta de prueba...")

        # --- Insertar en ventas ---
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M:%S")
        numero_mesa = 99
        estatus = "Activa"
        corte_id = 1  # ID de CorteCaja que ya exista

        cursor.execute("""
            INSERT INTO ventas (FechaVenta, HoraVenta, NumeroMesa, Estatus, CorteCaja_idCorteCaja)
            VALUES (%s, %s, %s, %s, %s)
        """, (fecha, hora, numero_mesa, estatus, corte_id))

        venta_id = cursor.lastrowid
        print(f"✅ Venta insertada con ID: {venta_id}")

        # --- Insertar en detalleventas ---
        subtotal = 100.0
        impuesto = subtotal * 0.16
        total = subtotal + impuesto

        cursor.execute(
            "INSERT INTO detalleventas (Subtotal, Impuesto, Descuento, Total, Ventas_IdVentas) VALUES (%s, %s, %s, %s, %s)",
            (subtotal, impuesto, descuento, total, venta_id))

        print("✅ Detalle de venta insertado")

        # --- Insertar en generarrecibo ---
        descripcion = f"Recibo de prueba para mesa {numero_mesa}"
        cursor.execute("""
            INSERT INTO generarrecibo (FechaRecibo, HoraRecibo, descripcion, Ventas_IdVentas)
            VALUES (%s, %s, %s, %s)
        """, (fecha, hora, descripcion, venta_id))
        print("✅ Recibo generado")

        # Confirmar cambios
        conexion.commit()

        # --- Eliminar registros para limpieza ---
        print("\n🧹 Eliminando registros de prueba...")
        cursor.execute("DELETE FROM generarrecibo WHERE Ventas_IdVentas = %s", (venta_id,))
        cursor.execute("DELETE FROM detalleventas WHERE Ventas_IdVentas = %s", (venta_id,))
        cursor.execute("DELETE FROM ventas WHERE id = %s", (venta_id,))
        conexion.commit()

        print("✅ Registros eliminados correctamente.")

        conexion.close()

    except Exception as e:
        print("❌ Error durante la prueba de inserción:")
        print(e)

if __name__ == "__main__":
    prueba_insercion_ventas()
