----   v 01/09/2026
-- isso é um comentário em linha
/* isso é um
    comentário em bloco
*/

set search_path=oper_zagi;

-- =========================================================
-- FORNECEDORES
-- =========================================================

INSERT INTO fornecedor VALUES (1,'Pacifica Gear');
INSERT INTO fornecedor VALUES (2,'Mountain King');
INSERT INTO fornecedor VALUES (3,'DAMA');


-- =========================================================
-- CATEGORIAS
-- =========================================================

INSERT INTO categoria VALUES (1,'Camping');
INSERT INTO categoria VALUES (2,'Footwear');
INSERT INTO categoria VALUES (3,'Escritório');


-- =========================================================
-- PRODUTOS
-- =========================================================

INSERT INTO produto VALUES (1,'Zzz Bag',100,1,1);
INSERT INTO produto VALUES (2,'Easy Boot',70,2,2);
INSERT INTO produto VALUES (3,'Cosy Sock',15,1,2);
INSERT INTO produto VALUES (4,'Dura Boot',90,2,1);
INSERT INTO produto VALUES (5,'Tiny Tent',150,1,2);
INSERT INTO produto VALUES (6,'Biggy Tent',250,2,1);

/* 
   Para o caso de garantir um novo fornecedor de um novo produto
   de uma nova categoria sob uma mesma transação (mesma tela).
   
   Os registros 3, 3 e 7 já foram inseridos acima para manter
   o DML simples e evitar duplicidade.
*/


-- =========================================================
-- REGIÕES
-- =========================================================

INSERT INTO regiao VALUES (1,'Chicagoland');
INSERT INTO regiao VALUES (2,'Tristate');
INSERT INTO regiao VALUES (3,'Sudeste');

-- =========================================================
-- LOJAS
-- =========================================================
INSERT INTO loja VALUES
    (1,'Endereço da Loja 1','60600000',1);

INSERT INTO loja VALUES
    (2,'Endereço da Loja 2','60605000',1);

INSERT INTO loja VALUES
    (3,'Endereço da Loja 3','35400000',2);

-- Loja utilizada no exercício
INSERT INTO loja VALUES
    (4,'Praia de Botafogo, 190','22250040',3);
-- =========================================================
-- CLIENTES
-- =========================================================
-- ClienteID, ClienteNome, ClienteCPF, ClienteEmail, ClienteCEP

INSERT INTO cliente VALUES
    (1,'Tina','12345678901','tina@example.com','60137000');

INSERT INTO cliente VALUES
    (2,'Tony','23456789012','tony@example.com','60611000');

INSERT INTO cliente VALUES
    (3,'Pam','34567890123','pam@example.com','35401000');


-- =========================================================
-- TRANSAÇÕES DE VENDA
-- =========================================================
-- Como TRNVendaData é DATE, utilizamos somente a data.

INSERT INTO Trans_de_Venda VALUES
    (1,'2026-09-01',1,1);

INSERT INTO Trans_de_Venda VALUES
    (2,'2026-09-01',2,2);

INSERT INTO Trans_de_Venda VALUES
    (3,'2026-09-02',3,3);

INSERT INTO Trans_de_Venda VALUES
    (4,'2026-09-02',1,3);

INSERT INTO Trans_de_Venda VALUES
    (5,'2026-09-02',2,3);


-- =========================================================
-- ITENS DAS VENDAS
-- =========================================================
-- QTDProdTransV, ProdID, TRNVendaID

/* formato autodeclarado */
INSERT INTO Incluido_em
    (QTDProdTransV, ProdID, TRNVendaID)
VALUES
    (1,1,1);

INSERT INTO Incluido_em VALUES (1,2,2);
INSERT INTO Incluido_em VALUES (5,3,3);
INSERT INTO Incluido_em VALUES (1,1,3);
INSERT INTO Incluido_em VALUES (1,4,4);
INSERT INTO Incluido_em VALUES (2,2,4);
INSERT INTO Incluido_em VALUES (4,4,5);
INSERT INTO Incluido_em VALUES (2,5,5);
INSERT INTO Incluido_em VALUES (1,6,5);


/* =========================================================
   EXERCÍCIO

   1. Venda para você mesmo três xícaras do DAMA numa loja
      na Praia de Botafogo, 190, na região sudeste.

      Compre uma hoje e duas amanhã.
========================================================= */