# Data Contract — ZAGI

Projeto de implementação e validação de um **Data Contract** para o banco de dados da ZAGI, utilizando PostgreSQL e a ferramenta [`datacontract-cli`](https://datacontract.com/).

O projeto define o contrato das tabelas `Fornecedor`, `Categoria` e `Produto`, incluindo estrutura, tipos de dados, chaves primárias, relacionamentos e regras de qualidade dos dados.

## Estrutura do projeto

```text
data-contract-zagi/
├── datacontract.yaml
├── main.py
├── DDL_create_tables_Lojas_ZAGI_PTBR.sql
├── DML_insert_Lojas_ZAGI_PTBR.sql
├── .gitignore
└── README.md
```

## Requisitos

* Python 3.10+
* PostgreSQL
* Git
* `datacontract-cli`

## 1. Clonar o repositório

```bash
git clone https://github.com/JaimeWillianCarneiro/data-contract-zagi.git
cd data-contract-zagi
```

## 2. Criar e ativar o ambiente virtual

No Linux/Arch Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Após ativar, o terminal deverá apresentar algo semelhante a:

```text
(.venv) [usuario@archlinux data-contract-zagi]$
```

## 3. Instalar as dependências

Instale o Data Contract CLI:

```bash
pip install datacontract-cli
```

Para verificar a instalação:

```bash
datacontract --version
```

## 4. Configurar o PostgreSQL

O projeto utiliza um banco chamado:

```text
ZAGI
```

e um schema:

```text
oper_zagi
```

Crie o banco:

```sql
CREATE DATABASE "ZAGI";
```

Depois conecte-se ao banco `ZAGI` e crie o schema:

```sql
CREATE SCHEMA oper_zagi;
```

Por exemplo, utilizando o `psql`:

```bash
psql -U postgres
```

Dentro do PostgreSQL:

```sql
CREATE DATABASE "ZAGI";
\c "ZAGI"
CREATE SCHEMA oper_zagi;
```

## 5. Criar as tabelas

Execute o script DDL:

```bash
psql -U postgres -d ZAGI -f DDL_create_tables_Lojas_ZAGI_PTBR.sql
```

Esse script cria as tabelas utilizadas pelo Data Contract.

## 6. Inserir os dados

Execute o script DML:

```bash
psql -U postgres -d ZAGI -f DML_insert_Lojas_ZAGI_PTBR.sql
```

Para verificar as tabelas:

```bash
psql -U postgres -d ZAGI
```

E:

```sql
SET search_path TO oper_zagi;

\dt
```

## 7. Configurar as credenciais

As credenciais do PostgreSQL **não devem ser versionadas no GitHub**.

Configure as variáveis de ambiente necessárias para o Data Contract:

```bash
export DATACONTRACT_POSTGRES_USERNAME="postgres"
export DATACONTRACT_POSTGRES_PASSWORD="sua_senha"
```

Caso utilize outro usuário:

```bash
export DATACONTRACT_POSTGRES_USERNAME="seu_usuario"
export DATACONTRACT_POSTGRES_PASSWORD="sua_senha"
```

Você também pode utilizar um arquivo `.env` local, desde que ele permaneça no `.gitignore`.

## 8. Configuração do Data Contract

O arquivo `datacontract.yaml` define a conexão com o PostgreSQL:

```yaml
servers:
  - server: ambiente_zagi
    type: postgres
    environment: dev
    host: localhost
    port: 5432
    database: ZAGI
    schema: oper_zagi
```

O contrato descreve as seguintes tabelas:

### Fornecedor

* `FornID`
* `FornNome`

### Categoria

* `CategID`
* `CategNome`

### Produto

* `ProdID`
* `ProdNome`
* `ProdPreco`
* `FornID`
* `CategID`

Também são definidos relacionamentos entre produtos, fornecedores e categorias.

## 9. Validar o Data Contract

Antes de testar os dados do banco, valide a estrutura do arquivo YAML:

```bash
datacontract lint datacontract.yaml
```

O resultado esperado é:

```text
🟢 data contract is valid.
```

## 10. Executar os testes

Com o PostgreSQL executando e as tabelas criadas:

```bash
datacontract test datacontract.yaml --server ambiente_zagi
```

Os testes verificam, entre outras coisas:

* existência das colunas;
* tipos físicos das colunas;
* valores nulos;
* unicidade das chaves primárias;
* preços válidos;
* existência dos fornecedores referenciados;
* existência das categorias referenciadas.

Um resultado bem-sucedido deverá terminar com:

```text
🟢 data contract is valid.
```

## 11. Executar pelo Python

O projeto também possui o arquivo `main.py`, que pode ser utilizado para executar as operações do Data Contract através do Python.

Com o ambiente virtual ativado:

```bash
python main.py
```

## Fluxo completo

Depois de clonar o projeto, o fluxo básico é:

```bash
# 1. Entrar no projeto
cd data-contract-zagi

# 2. Criar ambiente virtual
python -m venv .venv

# 3. Ativar
source .venv/bin/activate

# 4. Instalar dependência
pip install datacontract-cli

# 5. Configurar credenciais
export DATACONTRACT_POSTGRES_USERNAME="postgres"
export DATACONTRACT_POSTGRES_PASSWORD="sua_senha"

# 6. Criar banco/tabelas e inserir dados
psql -U postgres -d ZAGI -f DDL_create_tables_Lojas_ZAGI_PTBR.sql
psql -U postgres -d ZAGI -f DML_insert_Lojas_ZAGI_PTBR.sql

# 7. Validar o contrato
datacontract lint datacontract.yaml

# 8. Testar o contrato contra o PostgreSQL
datacontract test datacontract.yaml --server ambiente_zagi

# 9. Executar o programa Python
python main.py
```

## Segurança

**Não faça commit de credenciais.**

O arquivo `.env` está incluído no `.gitignore` e não deve ser enviado ao GitHub.

Caso credenciais tenham sido expostas publicamente, elas devem ser alteradas imediatamente.

## Autor

**Jaime Willian Carneiro da Silva**

Projeto acadêmico — ZAGI
