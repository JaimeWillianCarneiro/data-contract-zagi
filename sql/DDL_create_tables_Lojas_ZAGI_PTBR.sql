----   v 01/09/2026

-- isso é um comentário em linha

/* isso é um
   comentário em bloco
*/

DROP SCHEMA IF EXISTS oper_zagi CASCADE;
CREATE SCHEMA oper_zagi;

SET search_path = oper_zagi;


-- =========================================================
-- FORNECEDOR
-- =========================================================

CREATE TABLE Fornecedor
(
  FornID INT NOT NULL,
  FornNome VARCHAR(100) NOT NULL,
  PRIMARY KEY (FornID)
);


-- =========================================================
-- CLIENTE
-- =========================================================

CREATE TABLE Cliente
(
  ClienteID INT NOT NULL,
  ClienteNome VARCHAR(255) NOT NULL,
  ClienteCPF VARCHAR(11) NOT NULL,
  ClienteEmail VARCHAR(255) NOT NULL,
  ClienteCEP VARCHAR(8) NOT NULL,

  PRIMARY KEY (ClienteID),
  UNIQUE (ClienteCPF),
  UNIQUE (ClienteEmail)
);


-- =========================================================
-- REGIÃO
-- =========================================================

CREATE TABLE Regiao
(
  RegiaoID INT NOT NULL,
  RegiaoNome VARCHAR(100) NOT NULL,

  PRIMARY KEY (RegiaoID)
);


-- =========================================================
-- CATEGORIA
-- =========================================================

CREATE TABLE Categoria
(
  CategID INT NOT NULL,
  CategNome VARCHAR(100) NOT NULL,

  PRIMARY KEY (CategID)
);


-- =========================================================
-- PRODUTO
-- =========================================================

CREATE TABLE Produto
(
  ProdID INT NOT NULL,
  ProdNome VARCHAR(100) NOT NULL,
  ProdPreco money NOT NULL,
  FornID INT NOT NULL,
  CategID INT NOT NULL,

  PRIMARY KEY (ProdID),

  FOREIGN KEY (FornID)
    REFERENCES Fornecedor(FornID),

  FOREIGN KEY (CategID)
    REFERENCES Categoria(CategID)
);


-- =========================================================
-- LOJA
-- =========================================================

CREATE TABLE Loja
(
  LojaID INT NOT NULL,
  LojaEndereco VARCHAR(255) NOT NULL,
  LojaCEP VARCHAR(8) NOT NULL,
  RegiaoID INT NOT NULL,

  PRIMARY KEY (LojaID),

  FOREIGN KEY (RegiaoID)
    REFERENCES Regiao(RegiaoID)
);


-- =========================================================
-- TRANSAÇÃO DE VENDA
-- =========================================================

CREATE TABLE Trans_de_Venda
(
  TRNVendaID INT NOT NULL,
  TRNVendaData DATE NOT NULL,
  LojaID INT NOT NULL,
  ClienteID INT NOT NULL,

  PRIMARY KEY (TRNVendaID),

  FOREIGN KEY (LojaID)
    REFERENCES Loja(LojaID),

  FOREIGN KEY (ClienteID)
    REFERENCES Cliente(ClienteID)
);


-- =========================================================
-- ITENS DA VENDA
-- =========================================================

CREATE TABLE Incluido_em
(
  QTDProdTransV INT NOT NULL,
  ProdID INT NOT NULL,
  TRNVendaID INT NOT NULL,

  PRIMARY KEY (ProdID, TRNVendaID),

  FOREIGN KEY (ProdID)
    REFERENCES Produto(ProdID),

  FOREIGN KEY (TRNVendaID)
    REFERENCES Trans_de_Venda(TRNVendaID)
);