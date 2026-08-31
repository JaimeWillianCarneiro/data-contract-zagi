ALTER TABLE oper_zagi.Produto
DROP CONSTRAINT IF EXISTS produto_categid_fkey;

INSERT INTO oper_zagi.Produto
    (ProdID, ProdNome, ProdPreco, FornID, CategID)
VALUES
    (999997, 'Produto com categoria inválida', 10.00, 1, 999999);