ALTER TABLE oper_zagi.Produto
DROP CONSTRAINT IF EXISTS produto_fornid_fkey;

INSERT INTO oper_zagi.Produto
    (ProdID, ProdNome, ProdPreco, FornID, CategID)
VALUES
    (999998, 'Produto com fornecedor inválido', 10.00, 999999, 1);