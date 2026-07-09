import pandas as pd
import os
import logging


def configurar_log():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/validacion.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
        force=True
    )


def ejecutar_validacion(ruta_entrada="data/clean/ventas_clean.csv"):
    configurar_log()

    print("=== ETAPA 3: VALIDACIÓN ===")

    try:
        df = pd.read_csv(ruta_entrada)

        errores = []

        estados_validos = ["pendiente", "despachado", "entregado", "cancelado"]

        for indice, fila in df.iterrows():
            lista_errores = []

            # Validaciones estructurales
            if pd.isna(fila["id_pedido"]):
                lista_errores.append("id_pedido nulo")

            if pd.isna(fila["cantidad"]) or fila["cantidad"] <= 0:
                lista_errores.append("cantidad inválida")

            if pd.isna(fila["precio_unitario"]) or fila["precio_unitario"] <= 0:
                lista_errores.append("precio_unitario inválido")

            if pd.isna(fila["descuento_pct"]) or fila["descuento_pct"] < 0 or fila["descuento_pct"] > 100:
                lista_errores.append("descuento_pct fuera de rango")

            if pd.isna(fila["estado_pedido"]) or fila["estado_pedido"] not in estados_validos:
                lista_errores.append("estado_pedido fuera de dominio")

            if pd.isna(fila["fecha_pedido"]):
                lista_errores.append("fecha_pedido inválida")

            # Validaciones semánticas
            if fila["estado_pedido"] == "entregado" and pd.isna(fila["fecha_despacho"]):
                lista_errores.append("pedido entregado sin fecha de despacho")

            if pd.isna(fila["region"]):
                lista_errores.append("cliente sin región asignada")

            if len(lista_errores) > 0:
                errores.append({
                    "indice": indice,
                    "id_pedido": fila["id_pedido"],
                    "errores": "; ".join(lista_errores)
                })

        df_errores = pd.DataFrame(errores)

        if len(df_errores) > 0:
            indices_invalidos = df_errores["indice"].tolist()
            df_invalidos = df.loc[indices_invalidos].copy()
            df_invalidos["motivo_error"] = df_errores["errores"].values
        else:
            indices_invalidos = []
            df_invalidos = pd.DataFrame(columns=list(df.columns) + ["motivo_error"])

        df_validos = df.drop(index=indices_invalidos).copy()

        os.makedirs("data/validated", exist_ok=True)
        os.makedirs("data/errors", exist_ok=True)

        ruta_validos = "data/validated/ventas_validas.csv"
        ruta_invalidos = "data/errors/ventas_invalidas.csv"
        ruta_log_errores = "data/errors/detalle_errores_validacion.csv"

        df_validos.to_csv(ruta_validos, index=False, encoding="utf-8")
        df_invalidos.to_csv(ruta_invalidos, index=False, encoding="utf-8")
        df_errores.to_csv(ruta_log_errores, index=False, encoding="utf-8")

        logging.info("Registros totales evaluados: %s", len(df))
        logging.info("Registros válidos: %s", len(df_validos))
        logging.info("Registros inválidos: %s", len(df_invalidos))

        if len(df_invalidos) > 0:
            conteo_errores = df_invalidos["motivo_error"].value_counts()
            logging.info("Conteo de errores por tipo:")
            logging.info("\n%s", conteo_errores)

        print("Registros totales:", len(df))
        print("Registros válidos:", len(df_validos))
        print("Registros inválidos:", len(df_invalidos))
        print("Archivo de válidos:", ruta_validos)
        print("Archivo de inválidos:", ruta_invalidos)
        print("Validación finalizada correctamente.")

        return df_validos, df_invalidos

    except Exception as e:
        logging.error("Error durante la validación: %s", e)
        print("Error durante la validación:", e)
        return None, None


if __name__ == "__main__":
    ejecutar_validacion()