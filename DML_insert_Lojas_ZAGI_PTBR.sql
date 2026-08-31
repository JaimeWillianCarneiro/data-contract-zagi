----   v 23/9/22
-- isso é um comentário em linha
/* isso é um
    comentário em bloco
*/

set search_path=oper_zagi;

INSERT INTO fornecedor VALUES (1,'Pacifica Gear');
INSERT INTO fornecedor VALUES (2,'Mountain King');
INSERT INTO categoria VALUES (1,'Camping');
INSERT INTO categoria VALUES (2,'Footwear');

INSERT INTO produto VALUES (1,'Zzz Bag',100,1,1);
INSERT INTO produto VALUES (2,'Easy Boot',70,2,2);
INSERT INTO produto VALUES (3,'Cosy Sock',15,1,2);
INSERT INTO produto VALUES (4,'Dura Boot',90,2,1);
INSERT INTO produto VALUES (5,'Tiny Tent',150,1,2);
INSERT INTO produto VALUES (6,'Biggy Tent',250,2,1);

/* Para o caso de garantir um novo fornecedor de um novo produto de uma nova categoria sob uma mesma transação (mesma tela) */
BEGIN TRANSACTION;
INSERT INTO fornecedor VALUES (3,'DAMA');
INSERT INTO categoria VALUES (3,'Escritório');
INSERT INTO produto VALUES (7,'Xícara acorda estudante',80,3,3);
COMMIT;
/* Para o caso de garantir um novo fornecedor de um novo produto de uma nova categoria sob uma mesma transação (mesma tela) */

INSERT INTO regiao VALUES (1,'Chicagoland');
INSERT INTO regiao VALUES (2,'Tristate');
INSERT INTO loja VALUES (1,'60600',1);
INSERT INTO loja VALUES (2,'60605',1);
INSERT INTO loja VALUES (3,'35400',2);

INSERT INTO cliente VALUES (1,'Tina','60137');
INSERT INTO cliente VALUES (2,'Tony','60611');
INSERT INTO cliente VALUES (3,'Pam','35401');

INSERT INTO Trans_de_Venda VALUES (1,'2020-01-01 09:54:23',1,1);
INSERT INTO Trans_de_Venda VALUES (2,'2020-01-01 10:15:21',2,2);
INSERT INTO Trans_de_Venda VALUES (3,'2020-01-02 13:02:53',3,3);
INSERT INTO Trans_de_Venda VALUES (4,'2020-01-02 09:55:12',1,3);
INSERT INTO Trans_de_Venda VALUES (5,'2020-01-02 10:12:45',2,3);

/* outro formato válido, mais autodeclarado */
INSERT INTO Incluido_em (QTDProdTransV,ProdID,TRNVendaID) VALUES (1,1,1);
INSERT INTO Incluido_em VALUES (1,2,2);
INSERT INTO Incluido_em VALUES (5,3,3);
INSERT INTO Incluido_em VALUES (1,1,3);
INSERT INTO Incluido_em VALUES (1,4,4);
INSERT INTO Incluido_em VALUES (2,2,4);
INSERT INTO Incluido_em VALUES (4,4,5);
INSERT INTO Incluido_em VALUES (2,5,5);
INSERT INTO Incluido_em VALUES (1,6,5);

/* exercício
    1. Venda para você mesmo três xícaras do DAMA numa loja na Praia de Botafogo, 190, na região sudeste. 
    Compre uma hoje e duas amanhã.
*/
