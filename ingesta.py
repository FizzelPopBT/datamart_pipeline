import pandas as pd
import os
import logging
from datetime import datetime


def configurar_log():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/ingesta.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
        force=True
    )


def ejecutar_ingesta(ruta_archivo="ventas_datamart.csv"):
    configurar_log()

    print("=== ETAPA 1: INGESTA ===")

    try:
        df = pd.read_csv(ruta_archivo)

        print("\nShape del dataset:")
        print(df.shape)

        print("\nTipos de datos:")
        print(df.dtypes)

        print("\nInformación general:")
        print(df.info())

        print("\nConteo de nulos por columna:")
        print(df.isnull().sum())

        os.makedirs("data/raw", exist_ok=True)

        ruta_raw = "data/raw/ventas_raw.csv"
        df.to_csv(ruta_raw, index=False, encoding="utf-8")

        logging.info("Archivo cargado: %s", ruta_archivo)
        logging.info("Registros totales: %s", df.shape[0])
        logging.info("Columnas totales: %s", df.shape[1])
        logging.info("Copia raw guardada en: %s", ruta_raw)
        logging.info("Fecha de carga: %s", datetime.now())

        print("\nArchivo raw guardado correctamente en:", ruta_raw)
        print("Ingesta finalizada correctamente.")

        return df

    except Exception as e:
        logging.error("Error durante la ingesta: %s", e)
        print("Error durante la ingesta:", e)
        return None


if __name__ == "__main__":
    ejecutar_ingesta()