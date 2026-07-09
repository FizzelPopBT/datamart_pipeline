import pandas as pd
import sqlite3
import os
import logging


def configurar_log():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/carga.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
        force=True
    )


def ejecutar_carga(ruta_entrada="data/validated/ventas_validas.csv"):
    configurar_log()

    print("=== ETAPA 4: CARGA A BASE DE DATOS ===")

    try:
        df = pd.read_csv(ruta_entrada)

        os.makedirs("database", exist_ok=True)
        os.makedirs("data/errors", exist_ok=True)

        conexion = sqlite3.connect("database/datamart.db")
        cursor = conexion.cursor()

        try:
            cursor.execute("DROP TABLE IF EXISTS pedidos")

            cursor.execute("""
                CREATE TABLE pedidos (
                    id_pedido INTEGER PRIMARY KEY,
                    fecha_pedido TEXT NOT NULL,
                    rut_cliente TEXT NOT NULL,
                    nombre_cliente TEXT NOT NULL,
                    region TEXT NOT NULL,
                    producto TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio_unitario REAL NOT NULL,
                    descuento_pct REAL NOT NULL,
                    estado_pedido TEXT NOT NULL,
                    fecha_despacho TEXT,
                    total_venta REAL NOT NULL,
                    segmento_precio TEXT NOT NULL
                )
            """)

            for _, fila in df.iterrows():
                cursor.execute("""
                    INSERT INTO pedidos (
                        id_pedido,
                        fecha_pedido,
                        rut_cliente,
                        nombre_cliente,
                        region,
                        producto,
                        categoria,
                        cantidad,
                        precio_unitario,
                        descuento_pct,
                        estado_pedido,
                        fecha_despacho,
                        total_venta,
                        segmento_precio
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    int(fila["id_pedido"]),
                    fila["fecha_pedido"],
                    fila["rut_cliente"],
                    fila["nombre_cliente"],
                    fila["region"],
                    fila["producto"],
                    fila["categoria"],
                    int(fila["cantidad"]),
                    float(fila["precio_unitario"]),
                    float(fila["descuento_pct"]),
                    fila["estado_pedido"],
                    fila["fecha_despacho"] if pd.notna(fila["fecha_despacho"]) else None,
                    float(fila["total_venta"]),
                    fila["segmento_precio"]
                ))

            conexion.commit()

            logging.info("Carga realizada correctamente.")
            logging.info("Registros cargados en BD: %s", len(df))

            print("Carga realizada correctamente.")
            print("Registros cargados en BD:", len(df))

            print("\nVentas totales por región:")
            consulta_region = pd.read_sql_query("""
                SELECT region, ROUND(SUM(total_venta), 2) AS ventas_totales
                FROM pedidos
                GROUP BY region
                ORDER BY ventas_totales DESC
            """, conexion)
            print(consulta_region)

            print("\nVentas totales por categoría:")
            consulta_categoria = pd.read_sql_query("""
                SELECT categoria, ROUND(SUM(total_venta), 2) AS ventas_totales
                FROM pedidos
                GROUP BY categoria
                ORDER BY ventas_totales DESC
            """, conexion)
            print(consulta_categoria)

            consulta_region.to_csv("data/validated/ventas_por_region.csv", index=False, encoding="utf-8")
            consulta_categoria.to_csv("data/validated/ventas_por_categoria.csv", index=False, encoding="utf-8")

            rechazados_bd = pd.DataFrame(columns=df.columns)
            rechazados_bd.to_csv("data/errors/rechazados_bd.csv", index=False, encoding="utf-8")

            logging.info("Consulta ventas por región exportada.")
            logging.info("Consulta ventas por categoría exportada.")
            logging.info("Rechazados BD exportados en data/errors/rechazados_bd.csv")

        except Exception as e:
            conexion.rollback()

            df.to_csv("data/errors/rechazados_bd.csv", index=False, encoding="utf-8")

            logging.error("Error durante la carga. Se ejecutó ROLLBACK: %s", e)
            print("Error durante la carga. Se ejecutó ROLLBACK:", e)

        finally:
            conexion.close()

    except Exception as e:
        logging.error("Error general durante la carga: %s", e)
        print("Error general durante la carga:", e)


if __name__ == "__main__":
    ejecutar_carga()