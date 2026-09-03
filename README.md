# Data Contract — ZAGI

Projeto de implementação e validação de um **Data Contract** para o banco de dados da ZAGI, utilizando PostgreSQL e a ferramenta [`datacontract-cli`](https://datacontract.com/).

O projeto define o contrato das tabelas do banco de dados, incluindo **estrutura, tipos de dados, chaves primárias, unicidade, relacionamentos e regras de qualidade dos dados**.

Além da validação do banco em seu estado normal, o projeto possui um programa em Python que cria propositalmente diferentes violações no banco para verificar se o Data Contract é capaz de identificá-las.

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

e o schema:

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

> **Observação:** o script DDL também contém a criação do schema e pode ser utilizado para recriar toda a estrutura do banco.

## 5. Criar as tabelas

Execute o script DDL:

```bash
psql -U postgres -d ZAGI -f DDL_create_tables_Lojas_ZAGI_PTBR.sql
```

O script cria as tabelas utilizadas pelo Data Contract:

* `Fornecedor`
* `Categoria`
* `Produto`
* `Cliente`
* `Regiao`
* `Loja`
* `Trans_de_Venda`
* `Incluido_em`

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

O `main.py` utiliza as seguintes variáveis de ambiente:

```text
DATACONTRACT_POSTGRES_USERNAME
DATACONTRACT_POSTGRES_PASSWORD
```

No Linux, elas podem ser configuradas com:

```bash
export DATACONTRACT_POSTGRES_USERNAME="postgres"

export DATACONTRACT_POSTGRES_PASSWORD="sua_senha"
```

Caso utilize outro usuário:

```bash
export DATACONTRACT_POSTGRES_USERNAME="seu_usuario"

export DATACONTRACT_POSTGRES_PASSWORD="sua_senha"
```

Também é possível utilizar um arquivo `.env` local:

```text
DATACONTRACT_POSTGRES_USERNAME=postgres
DATACONTRACT_POSTGRES_PASSWORD=sua_senha
```

O arquivo `.env` deve permanecer no `.gitignore`.

## 8. Estrutura do Data Contract

O arquivo `datacontract.yaml` utiliza a versão `3.1.0` do padrão de Data Contract e define a conexão com o PostgreSQL:

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

O contrato descreve as seguintes tabelas.

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

### Cliente

* `ClienteID`
* `ClienteNome`
* `ClienteCPF`
* `ClienteEmail`
* `ClienteCEP`

### Regiao

* `RegiaoID`
* `RegiaoNome`

### Loja

* `LojaID`
* `LojaEndereco`
* `LojaCEP`
* `RegiaoID`

### Trans_de_Venda

* `TRNVendaID`
* `TRNVendaData`
* `LojaID`
* `ClienteID`

### Incluido_em

* `QTDProdTransV`
* `ProdID`
* `TRNVendaID`

Também são definidos os relacionamentos entre as tabelas, incluindo:

```text
Produto.FornID          → Fornecedor.FornID
Produto.CategID         → Categoria.CategID
Loja.RegiaoID           → Regiao.RegiaoID
Trans_de_Venda.LojaID   → Loja.LojaID
Trans_de_Venda.ClienteID → Cliente.ClienteID
Incluido_em.ProdID      → Produto.ProdID
Incluido_em.TRNVendaID  → Trans_de_Venda.TRNVendaID
```

A tabela `Incluido_em` possui uma chave primária composta por:

```text
(ProdID, TRNVendaID)
```

## 9. Regras de qualidade dos dados

O Data Contract também define regras para verificar a qualidade dos dados.

Entre as principais regras estão:

### Produto

* `ProdPreco` não pode ser menor que `0.01`;
* `FornID` deve referenciar um fornecedor existente;
* `CategID` deve referenciar uma categoria existente;
* `ProdID` deve ser único;
* campos obrigatórios não podem ser nulos.

### Cliente

* `ClienteCPF` deve possuir exatamente 11 dígitos;
* `ClienteCPF` deve ser único;
* `ClienteEmail` deve possuir formato válido;
* `ClienteEmail` deve ser único;
* `ClienteCEP` deve possuir exatamente 8 dígitos;
* campos obrigatórios não podem ser nulos.

### Loja

* `LojaCEP` deve possuir exatamente 8 dígitos;
* `RegiaoID` deve referenciar uma região existente;
* campos obrigatórios não podem ser nulos.

### Trans_de_Venda

* `LojaID` deve referenciar uma loja existente;
* `ClienteID` deve referenciar um cliente existente;
* `TRNVendaID` deve ser único;
* campos obrigatórios não podem ser nulos.

### Incluido_em

* `QTDProdTransV` deve ser maior que zero;
* `ProdID` deve referenciar um produto existente;
* `TRNVendaID` deve referenciar uma transação existente;
* `(ProdID, TRNVendaID)` deve ser único.

## 10. Validar o Data Contract

Antes de testar os dados do banco, valide a estrutura do arquivo YAML:

```bash
datacontract lint datacontract.yaml
```

O resultado esperado é:

```text
🟢 data contract is valid.
```

O `lint` verifica se o contrato está estruturalmente válido antes de sua execução contra o banco de dados.

## 11. Executar os testes diretamente

Com o PostgreSQL executando e as tabelas criadas:

```bash
datacontract test datacontract.yaml --server ambiente_zagi
```

Os testes verificam, entre outras coisas:

* existência das tabelas;
* existência das colunas;
* tipos físicos das colunas;
* valores nulos;
* unicidade das chaves;
* formato dos campos;
* preços válidos;
* existência dos fornecedores referenciados;
* existência das categorias referenciadas;
* existência das regiões referenciadas;
* existência dos clientes e lojas referenciados;
* integridade dos relacionamentos.

Um banco conforme ao contrato deverá apresentar resultado de sucesso.

## 12. Executar o experimento automatizado

O arquivo `main.py` automatiza a validação do Data Contract.

Execute:

```bash
python main.py
```

O programa primeiro verifica se o banco está em conformidade com o contrato. Em seguida, executa uma sequência de cenários em que viola propositalmente diferentes regras.

### Cenário 1 — Preço inválido

Cria um produto com preço igual a `0.00`, violando a regra definida para `ProdPreco`.

```text
Produto → ProdPreco = 0.00
```

O Data Contract deve identificar a violação.

### Cenário 2 — Fornecedor inexistente

Cria um produto cujo `FornID` não existe na tabela `Fornecedor`.

```text
Produto.FornID → Fornecedor inexistente
```

A FK do PostgreSQL é temporariamente removida para permitir a criação do dado inconsistente. Após o teste, a FK é restaurada.

### Cenário 3 — Categoria inexistente

Cria um produto cujo `CategID` não existe na tabela `Categoria`.

```text
Produto.CategID → Categoria inexistente
```

Assim como no cenário anterior, a FK é temporariamente removida e restaurada após o teste.

### Cenário 4 — CPF com formato inválido

Altera temporariamente o CPF de um cliente para um valor contendo caracteres que não são dígitos:

```text
12345ABC789
```

O Data Contract deve identificar a violação da expressão regular definida para `ClienteCPF`.

Após o teste, o CPF original é restaurado.

### Cenário 5 — CPF duplicado

Altera temporariamente o CPF de dois clientes para o mesmo valor.

```text
Cliente 1 → 12345678901
Cliente 2 → 12345678901
```

A constraint `UNIQUE` do PostgreSQL é temporariamente removida para permitir a criação da inconsistência.

O Data Contract deve identificar que `ClienteCPF` deixou de ser único.

Após o teste, o CPF original e a constraint `UNIQUE` são restaurados.

### Cenário 6 — Tipagem incorreta

Altera temporariamente o tipo físico de `ClienteCPF` no PostgreSQL, fazendo com que ele deixe de corresponder ao tipo definido no Data Contract.

O objetivo é verificar se o contrato consegue detectar uma incompatibilidade entre o tipo esperado e o tipo existente no banco.

Após o teste, o tipo original da coluna é restaurado.

## 13. Fluxo dos experimentos

O fluxo executado pelo `main.py` pode ser representado da seguinte forma:

```text
                 ┌──────────────────────┐
                 │ Banco PostgreSQL     │
                 │      ZAGI            │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Data Contract        │
                 │ datacontract.yaml    │
                 └──────────┬───────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    Baseline   │
                    └───────┬───────┘
                            │
                Banco conforme?
                       │
              ┌────────┴────────┐
             SIM                NÃO
              │                  │
              ▼                  ▼
      Executar cenários       Encerrar
              │
              ▼
     ┌────────────────────┐
     │ 1. Preço inválido  │
     ├────────────────────┤
     │ 2. FK fornecedor   │
     ├────────────────────┤
     │ 3. FK categoria    │
     ├────────────────────┤
     │ 4. CPF inválido    │
     ├────────────────────┤
     │ 5. CPF duplicado   │
     ├────────────────────┤
     │ 6. Tipo incorreto  │
     └─────────┬──────────┘
               │
               ▼
      Restaurar o banco
               │
               ▼
      ┌──────────────────┐
      │ Experimento      │
      │ finalizado       │
      └──────────────────┘
```

Os cenários que alteram constraints ou dados do banco possuem mecanismos de restauração para que o banco retorne ao estado original após o experimento.

## 14. Fluxo completo

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

# 6. Criar estrutura do banco
psql -U postgres -d ZAGI -f DDL_create_tables_Lojas_ZAGI_PTBR.sql

# 7. Inserir dados
psql -U postgres -d ZAGI -f DML_insert_Lojas_ZAGI_PTBR.sql

# 8. Validar o contrato
datacontract lint datacontract.yaml

# 9. Testar o contrato contra o PostgreSQL
datacontract test datacontract.yaml --server ambiente_zagi

# 10. Executar os cenários automatizados
python main.py
```


## Autores

* Bruno Ferreira Salvi
* Elisa de Oliveira Soares
* Gabrielle Scherer Mascarelo
* Jaime Willian Carneiro da Silva
* Luiz Eduardo Bravin
* Ximena Beatriz Gomez Flores
