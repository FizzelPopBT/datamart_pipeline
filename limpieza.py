import pandas as pd
import os
import logging


def configurar_log():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/limpieza.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
        force=True
    )


def limpiar_fecha(columna):
    return pd.to_datetime(columna, errors="coerce", dayfirst=True).dt.strftime("%Y-%m-%d")


def limpiar_precio(valor):
    if pd.isna(valor):
        return None

    valor = str(valor)
    valor = valor.replace("$", "")
    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")
    valor = valor.strip()

    return pd.to_numeric(valor, errors="coerce")


def estandarizar_categoria(valor):
    if pd.isna(valor):
        return None

    valor = str(valor).strip().lower()

    if valor in ["tech", "technology", "tecnologia", "tecnología", "TECH".lower()]:
        return "Tecnologia"
    elif valor in ["hogar", "home"]:
        return "Hogar"
    elif valor in ["moda", "fashion"]:
        return "Moda"
    else:
        return valor.capitalize()


def segmento_precio(valor):
    if pd.isna(valor):
        return "sin_segmento"

    if valor < 10000:
        return "bajo"
    elif valor < 50000:
        return "medio"
    else:
        return "alto"


def ejecutar_limpieza(ruta_entrada="data/raw/ventas_raw.csv"):
    configurar_log()

    print("=== ETAPA 2: LIMPIEZA Y TRANSFORMACIÓN ===")

    try:
        df = pd.read_csv(ruta_entrada)

        registros_iniciales = len(df)

        # Eliminar duplicados exactos por id_pedido
        df = df.drop_duplicates(subset=["id_pedido"], keep="first")

        # Limpiar fechas
        df["fecha_pedido"] = limpiar_fecha(df["fecha_pedido"])
        df["fecha_despacho"] = limpiar_fecha(df["fecha_despacho"])

        # Limpiar texto
        df["rut_cliente"] = df["rut_cliente"].astype(str).str.strip()
        df["nombre_cliente"] = df["nombre_cliente"].astype(str).str.strip().str.title()
        df["region"] = df["region"].astype(str).str.strip().str.title()
        df["producto"] = df["producto"].astype(str).str.strip()
        df["estado_pedido"] = df["estado_pedido"].astype(str).str.strip().str.lower()

        # Corregir nulos que quedaron como texto
        df = df.replace(["nan", "None", "NaN", ""], pd.NA)

        # Estandarizar categoría
        df["categoria"] = df["categoria"].apply(estandarizar_categoria)

        # Limpiar precio
        df["precio_unitario"] = df["precio_unitario"].apply(limpiar_precio)

        # Convertir columnas numéricas
        df["id_pedido"] = pd.to_numeric(df["id_pedido"], errors="coerce")
        df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
        df["descuento_pct"] = pd.to_numeric(df["descuento_pct"], errors="coerce")

        # Crear columna total_venta
        df["total_venta"] = (
            df["cantidad"] *
            df["precio_unitario"] *
            (1 - df["descuento_pct"] / 100)
        )

        # Crear columna segmento_precio
        df["segmento_precio"] = df["precio_unitario"].apply(segmento_precio)

        os.makedirs("data/clean", exist_ok=True)

        ruta_salida = "data/clean/ventas_clean.csv"
        df.to_csv(ruta_salida, index=False, encoding="utf-8")

        logging.info("Registros iniciales: %s", registros_iniciales)
        logging.info("Registros después de eliminar duplicados: %s", len(df))
        logging.info("Archivo limpio guardado en: %s", ruta_salida)

        print("Registros iniciales:", registros_iniciales)
        print("Registros después de limpieza:", len(df))
        print("Archivo limpio guardado en:", ruta_salida)
        print("Limpieza finalizada correctamente.")

        return df

    except Exception as e:
        logging.error("Error durante la limpieza: %s", e)
        print("Error durante la limpieza:", e)
        return None


if __name__ == "__main__":
    ejecutar_limpieza()