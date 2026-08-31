
import os
import subprocess
from pathlib import Path

import psycopg
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "ZAGI",
    "user": os.getenv("DATACONTRACT_POSTGRES_USERNAME"),
    "password": os.getenv("DATACONTRACT_POSTGRES_PASSWORD"),
}


CONTRACT_FILE = BASE_DIR / "datacontract.yaml"

PRODUCT_TABLE = "oper_zagi.Produto"
SUPPLIER_TABLE = "oper_zagi.Fornecedor"
CATEGORY_TABLE = "oper_zagi.Categoria"

FK_SUPPLIER = "produto_fornid_fkey"
FK_CATEGORY = "produto_categid_fkey"


def get_connection():
    return psycopg.connect(**DB_CONFIG)


def execute_sql(sql_file):
    """Executa um arquivo SQL no PostgreSQL."""

    sql = Path(sql_file).read_text(encoding="utf-8")

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

        conn.commit()


def execute_sql_string(sql):
    """Executa uma string SQL no PostgreSQL."""

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

        conn.commit()


def run_datacontract():
    """Executa o teste do Data Contract."""

    result = subprocess.run(
        [
            "datacontract",
            "test",
            str(CONTRACT_FILE),
            "--server",
            "ambiente_zagi",
        ],
        capture_output=True,
        text=True,
    )

    print(result.stdout)

    if result.stderr:
        print(result.stderr)

    return result.returncode


def print_section(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)
    print()


def cleanup_test_data():
    """Remove todos os registros criados pelos cenários."""

    print_section("LIMPANDO DADOS DOS TESTES")

    sql = """
    DELETE FROM oper_zagi.Produto
    WHERE ProdID IN (999999, 999998, 999997);
    """

    execute_sql_string(sql)


def baseline_test():
    """Testa o banco em estado normal."""

    print_section("BASELINE - BANCO CONFORME AO CONTRATO")

    return run_datacontract()


def break_price():
    """Cria um produto com preço inválido."""

    print_section("CENÁRIO 1 - PREÇO INVÁLIDO")

    execute_sql_string(
        """
        INSERT INTO oper_zagi.Produto
            (ProdID, ProdNome, ProdPreco, FornID, CategID)
        VALUES
            (999999, 'Produto com preço inválido', 0.00, 1, 1);
        """
    )

    return run_datacontract()


def disable_supplier_fk():
    """Remove temporariamente a FK Produto -> Fornecedor."""

    print_section("DESABILITANDO FK DE FORNECEDOR")

    execute_sql_string(
        f"""
        ALTER TABLE oper_zagi.Produto
        DROP CONSTRAINT IF EXISTS {FK_SUPPLIER};
        """
    )


def restore_supplier_fk():
    """Restaura a FK Produto -> Fornecedor."""

    print_section("RESTAURANDO FK DE FORNECEDOR")

    execute_sql_string(
        f"""
        ALTER TABLE oper_zagi.Produto
        ADD CONSTRAINT {FK_SUPPLIER}
        FOREIGN KEY (FornID)
        REFERENCES oper_zagi.Fornecedor(FornID);
        """
    )


def break_supplier():
    """Cria um produto apontando para fornecedor inexistente."""

    print_section("CENÁRIO 2 - FORNECEDOR INEXISTENTE")

    disable_supplier_fk()

    execute_sql_string(
        """
        INSERT INTO oper_zagi.Produto
            (ProdID, ProdNome, ProdPreco, FornID, CategID)
        VALUES
            (999998, 'Produto com fornecedor inválido', 100.00, 999999, 1);
        """
    )

    result = run_datacontract()

    cleanup_test_data()

    restore_supplier_fk()

    return result


def disable_category_fk():
    """Remove temporariamente a FK Produto -> Categoria."""

    print_section("DESABILITANDO FK DE CATEGORIA")

    execute_sql_string(
        f"""
        ALTER TABLE oper_zagi.Produto
        DROP CONSTRAINT IF EXISTS {FK_CATEGORY};
        """
    )


def restore_category_fk():
    """Restaura a FK Produto -> Categoria."""

    print_section("RESTAURANDO FK DE CATEGORIA")

    execute_sql_string(
        f"""
        ALTER TABLE oper_zagi.Produto
        ADD CONSTRAINT {FK_CATEGORY}
        FOREIGN KEY (CategID)
        REFERENCES oper_zagi.Categoria(CategID);
        """
    )


def break_category():
    """Cria um produto apontando para categoria inexistente."""

    print_section("CENÁRIO 3 - CATEGORIA INEXISTENTE")

    disable_category_fk()

    execute_sql_string(
        """
        INSERT INTO oper_zagi.Produto
            (ProdID, ProdNome, ProdPreco, FornID, CategID)
        VALUES
            (999997, 'Produto com categoria inválida', 100.00, 1, 999999);
        """
    )

    result = run_datacontract()

    cleanup_test_data()

    restore_category_fk()

    return result

def main():

    # Garante que não existem resíduos de execuções anteriores.
    cleanup_test_data()

    # 1. Banco deve estar íntegro.
    baseline_result = baseline_test()

    if baseline_result != 0:
        print(
            "\nERRO: o banco não está conforme ao contrato antes "
            "dos cenários de quebra."
        )

        print(
            "\nExecute os checks manualmente e corrija o banco "
            "antes de continuar."
        )

        return

    # 2. Quebra de preço.
    cleanup_test_data()
    break_price()
    cleanup_test_data()

    # 3. Quebra de fornecedor.
    cleanup_test_data()
    break_supplier()
    cleanup_test_data()

    # 4. Quebra de categoria.
    cleanup_test_data()
    break_category()
    cleanup_test_data()

    # Garantia final de integridade.
    cleanup_test_data()

    print_section("EXPERIMENTO FINALIZADO")

    print("Banco restaurado ao estado original.")


if __name__ == "__main__":
    main()