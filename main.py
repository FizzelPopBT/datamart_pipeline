from ingesta import ejecutar_ingesta
from limpieza import ejecutar_limpieza
from validacion import ejecutar_validacion
from carga import ejecutar_carga


def main():
    print("====================================")
    print(" PIPELINE DATAMART CHILE S.A.")
    print("====================================")

    ejecutar_ingesta("ventas_datamart.csv")
    ejecutar_limpieza("data/raw/ventas_raw.csv")
    ejecutar_validacion("data/clean/ventas_clean.csv")
    ejecutar_carga("data/validated/ventas_validas.csv")

    print("====================================")
    print(" PIPELINE FINALIZADO")
    print("====================================")


if __name__ == "__main__":
    main()