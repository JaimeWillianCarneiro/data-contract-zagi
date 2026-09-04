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
CLIENT_TABLE = "oper_zagi.Cliente"

FK_SUPPLIER = "produto_fornid_fkey"
FK_CATEGORY = "produto_categid_fkey"
UNIQUE_CLIENTE_CPF = "cliente_clientecpf_key"

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

def ensure_freshness():
    """
    Garante que exista uma transação recente o suficiente para
    satisfazer a SLA de freshness de 24 horas.
    """

    print_section("VERIFICANDO SLA DE FRESHNESS")

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    MAX(TRNVendaData),
                    CURRENT_DATE,
                    CURRENT_DATE - MAX(TRNVendaData)
                FROM oper_zagi.Trans_de_Venda;
                """
            )

            ultima_venda, data_atual, diferenca = cursor.fetchone()

    print(f"Última venda: {ultima_venda}")
    print(f"Data atual:   {data_atual}")
    print(f"Diferença:    {diferenca} dia(s)")

    if ultima_venda is None or diferenca >= 1:
        print("\nFreshness fora do limite. Atualizando a venda mais recente...")

        execute_sql_string(
            """
            UPDATE oper_zagi.Trans_de_Venda
            SET TRNVendaData = CURRENT_DATE
            WHERE TRNVendaID = (
                SELECT TRNVendaID
                FROM oper_zagi.Trans_de_Venda
                ORDER BY TRNVendaData DESC
                LIMIT 1
            );
            """
        )

        print("SLA de freshness preparada para o teste.")

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


# ============================================================
# LIMPEZA
# ============================================================

def cleanup_test_data():
    """Remove todos os registros criados pelos cenários."""

    print_section("LIMPANDO DADOS DOS TESTES")

    sql = """
    DELETE FROM oper_zagi.Produto
    WHERE ProdID IN (999999, 999998, 999997);
    """

    execute_sql_string(sql)


# ============================================================
# BASELINE
# ============================================================

def baseline_test():
    """Testa o banco em estado normal."""

    print_section("BASELINE - BANCO CONFORME AO CONTRATO")

    return run_datacontract()


# ============================================================
# CENÁRIO 1 - PREÇO
# ============================================================

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


# ============================================================
# CENÁRIO 2 - FORNECEDOR
# ============================================================

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

    try:
        execute_sql_string(
            """
            INSERT INTO oper_zagi.Produto
                (ProdID, ProdNome, ProdPreco, FornID, CategID)
            VALUES
                (999998, 'Produto com fornecedor inválido', 100.00, 999999, 1);
            """
        )

        return run_datacontract()

    finally:
        cleanup_test_data()
        restore_supplier_fk()


# ============================================================
# CENÁRIO 3 - CATEGORIA
# ============================================================

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

    try:
        execute_sql_string(
            """
            INSERT INTO oper_zagi.Produto
                (ProdID, ProdNome, ProdPreco, FornID, CategID)
            VALUES
                (999997, 'Produto com categoria inválida', 100.00, 1, 999999);
            """
        )

        return run_datacontract()

    finally:
        cleanup_test_data()
        restore_category_fk()


# ============================================================
# CENÁRIO 4 - FORMATO DE STRING
# ============================================================

def break_cpf_format():
    """
    Altera temporariamente o CPF de um cliente para um valor
    que não corresponde ao padrão definido no contrato.
    """

    print_section("CENÁRIO 4 - CPF COM FORMATO INVÁLIDO")

    original_cpf = "12345678901"

    execute_sql_string(
        """
        UPDATE oper_zagi.Cliente
        SET ClienteCPF = '12345ABC789'
        WHERE ClienteID = 1;
        """
    )

    try:
        return run_datacontract()

    finally:
        execute_sql_string(
            f"""
            UPDATE oper_zagi.Cliente
            SET ClienteCPF = '{original_cpf}'
            WHERE ClienteID = 1;
            """
        )


# ============================================================
# CENÁRIO 5 - UNICIDADE
# ============================================================
def break_cpf_uniqueness():
    """
    Remove temporariamente a constraint UNIQUE do CPF,
    cria dois clientes com o mesmo CPF e verifica se o
    Data Contract detecta a duplicidade.
    """

    print_section("CENÁRIO 5 - CPF DUPLICADO")

    original_cpf_cliente_2 = "23456789012"

    # Remove temporariamente a constraint UNIQUE
    execute_sql_string(
        f"""
        ALTER TABLE oper_zagi.Cliente
        DROP CONSTRAINT IF EXISTS {UNIQUE_CLIENTE_CPF};
        """
    )

    try:
        # Cria a duplicidade
        execute_sql_string(
            """
            UPDATE oper_zagi.Cliente
            SET ClienteCPF = '12345678901'
            WHERE ClienteID = 2;
            """
        )

        return run_datacontract()

    finally:
        # Restaura o CPF original
        execute_sql_string(
            f"""
            UPDATE oper_zagi.Cliente
            SET ClienteCPF = '{original_cpf_cliente_2}'
            WHERE ClienteID = 2;
            """
        )

        # Restaura a constraint UNIQUE
        execute_sql_string(
            f"""
            ALTER TABLE oper_zagi.Cliente
            ADD CONSTRAINT {UNIQUE_CLIENTE_CPF}
            UNIQUE (ClienteCPF);
            """
        )


# ============================================================
# CENÁRIO 6 - TIPAGEM
# ============================================================

def break_type():
    """
    Altera temporariamente o tipo físico de ClienteCPF,
    fazendo o banco divergir do tipo declarado no contrato.
    """

    print_section("CENÁRIO 6 - TIPAGEM INCORRETA")

    execute_sql_string(
        """
        ALTER TABLE oper_zagi.Cliente
        ALTER COLUMN ClienteCPF TYPE TEXT;
        """
    )

    try:
        return run_datacontract()

    finally:
        execute_sql_string(
            """
            ALTER TABLE oper_zagi.Cliente
            ALTER COLUMN ClienteCPF TYPE VARCHAR(11);
            """
        )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # Limpeza inicial
    # --------------------------------------------------------

    cleanup_test_data()

    # --------------------------------------------------------
    # Baseline
    # --------------------------------------------------------
    ensure_freshness()
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

    # --------------------------------------------------------
    # Cenário 1 - Preço
    # --------------------------------------------------------

    cleanup_test_data()
    break_price()
    cleanup_test_data()

    # --------------------------------------------------------
    # Cenário 2 - Fornecedor
    # --------------------------------------------------------

    cleanup_test_data()
    break_supplier()
    cleanup_test_data()

    # --------------------------------------------------------
    # Cenário 3 - Categoria
    # --------------------------------------------------------

    cleanup_test_data()
    break_category()
    cleanup_test_data()

    # --------------------------------------------------------
    # Cenário 4 - Formato de string
    # --------------------------------------------------------

    break_cpf_format()

    # --------------------------------------------------------
    # Cenário 5 - Unicidade
    # --------------------------------------------------------

    break_cpf_uniqueness()

    # --------------------------------------------------------
    # Cenário 6 - Tipagem
    # --------------------------------------------------------

    break_type()

    # --------------------------------------------------------
    # Garantia final
    # --------------------------------------------------------

    cleanup_test_data()

    print_section("EXPERIMENTO FINALIZADO")

    print("Banco restaurado ao estado original.")


if __name__ == "__main__":
    main()