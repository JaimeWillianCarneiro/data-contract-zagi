ALTER TABLE oper_zagi.Produto
ALTER COLUMN ProdPreco TYPE numeric
USING ProdPreco::numeric;