import configparser
cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

nomeBanco = cfg['DEFAULT']['NomeBanco']
codEntidade = cfg['DEFAULT']['CodEntidade']
nomeEntidade = cfg['DEFAULT']['NomeEntidade']
motorista = cfg['DEFAULT']['Motorista']

scripts = {

'Abastecimento' : f""" SELECT 
{codEntidade} ||'|'||
a.SEQUENCIA ||'|'||
coalesce(v.CODIGO,'') ||'|'||
coalesce(v.NUMTOMBAMENTO,'') ||'|'||
'$CodProduto$' ||'|'||
'$Nome$' ||'|'||
'$NrCodigoMotorista$' ||'|'||
'$VlUnitario$' ||'|'||
substring(a.data from 9 for 2) ||'/'|| substring(a.data from 6 for 2) ||'/'|| substring(a.data from 1 for 4) ||'|'||
'$NrLitrosAbastecimento$' ||'|'||
'$VlAbastecimento$' ||'|'||
'1' ||'|'||
'$NrNotaFiscal$' ||'|'||
coalesce(a.OBSERVACAO, '') ||'|'||
'$CodFornecedor$' ||'|'||
'$Cnpj$' ||'|'||
'$CodPessoa$' ||'|'||
'$CodLocal$' ||'|'||
'$NrInterno$' ||'|'||
1  ||'|'||
'$CodEntidadeLiquidacao$' ||'|'||
'$ExercicioLiquidacao$' ||'|'||
'$NrLiquidacao$' ||'|'||
'$ExLiquidacao$' ||'|'||
'$CodEntidadeOrigemLiquidacao$' ||'|'||
'$CodEntidadeEmpenho$' ||'|'||
'$ExercicioEmpenho$' ||'|'||
'$NrEmpenho$' ||'|'||
'$ExEmpenho$' ||'|'||
'$CodEntidadeOrigemEmpenho$' ||'|'
FROM FROMOVC a 
left join FROVEIC v on (v.IDFROTA = a.IDFROTA)
join FROROTC r on (r.CODIGO = a.CODROTEIRO)
where a.TIPO = 6
order by a.SEQUENCIA desc """
}