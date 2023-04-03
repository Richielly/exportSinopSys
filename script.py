import configparser
cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

nomeBanco = cfg['DEFAULT']['NomeBanco']
codEntidade = cfg['DEFAULT']['CodEntidade']
nomeEntidade = cfg['DEFAULT']['NomeEntidade']
motorista = cfg['DEFAULT']['Motorista']

scripts = {

'Cor' : f""" select DISTINCT
            UPPER(c.COR) ||'|' FROM FROVEIC c
            union all
            select distinct
            'CONVERSAO|' from FROVEIC """,

'Marca' : f""" SELECT distinct upper(m.fabricante) ||'|' FROM FROVEIC m """,

'Especie' : f""" SELECT distinct
                trim(case e.TIPONATUREZA
                    when '1  : Veiculos Passeio/Utilitario' then 'Veiculos Passeio/Utilitario'
                    when '1:Veiculos Passeio/Utilitario' then 'Veiculos Passeio/Utilitario'
                    when '5  : Motos' then 'Motos'
                    when '5:Motos' then 'Motos'
                    when '52 : Tratores Agricolas' then 'Tratores Agricolas'
                    when '52:Tratores Agricolas' then 'Tratores Agricolas'
                    when '99:Outros Equipamentos' then 'Outros Equipamentos' end) ||'|'||
                case e.TIPONATUREZA
                    when '1  : Veiculos Passeio/Utilitario' then 'B'
                    when '1:Veiculos Passeio/Utilitario' then 'B'
                    when '5  : Motos' then 'A'
                    when '5:Motos' then 'A'
                    when '52 : Tratores Agricolas' then 'D'
                    when '52:Tratores Agricolas' then 'D'
                    when '99:Outros Equipamentos' then 'E' end||'|'||
                e.TIPOMEDIDOR ||'|'||
                '' ||'|'||
                trim(case e.TIPONATUREZA
                    when '1  : Veiculos Passeio/Utilitario' then '1'
                    when '1:Veiculos Passeio/Utilitario' then '1'
                    when '5  : Motos' then '5'
                    when '5:Motos' then '5'
                    when '52 : Tratores Agricolas' then '52'
                    when '52:Tratores Agricolas' then '52'
                    when '99:Outros Equipamentos' then '99' end) ||'|'
                FROM FROVEIC e """,

'Modelo' : f""" select
                m.MODELO ||'|'||
                upper(m.FABRICANTE) ||'|'||
                trim(case m.TIPONATUREZA
                    when '1  : Veiculos Passeio/Utilitario' then 'Veiculos Passeio/Utilitario'
                    when '1:Veiculos Passeio/Utilitario' then 'Veiculos Passeio/Utilitario'
                    when '5  : Motos' then 'Motos'
                    when '5:Motos' then 'Motos'
                    when '52 : Tratores Agricolas' then 'Tratores Agricolas'
                    when '52:Tratores Agricolas' then 'Tratores Agricolas'
                    when '99:Outros Equipamentos' then 'Outros Equipamentos' end) ||'|'||
                trim(case m.DESCCOMBUSTIVEL
                    when '1:Gasolina' then '1'
                    when '3:Diesel' then '3'
                    when '26:Veículos FLEX e Assemelhado' then '26' end) ||'|'
                FROM FROVEIC m """,

'Motorista' : f""" SELECT
                {codEntidade} ||'|'||
                coalesce(m.CODIGO, '') ||'|'||
                '' ||'|'||
                '' ||'|'||
                replace(replace(m.cpf,'.',''),'-','') ||'|'||
                coalesce(m.cnh, '') ||'|'||
                1 ||'|'|| --Padrão 1-Com Foto
                substring(m.DATAEMISSAOCNH from 9 for 2) ||'/'|| substring(m.DATAEMISSAOCNH from 6 for 2) ||'/'|| substring(m.DATAEMISSAOCNH from 1 for 4) ||'|'||
                substring(m.DATAVALIDADECNH from 9 for 2) ||'/'|| substring(m.DATAVALIDADECNH from 6 for 2) ||'/'|| substring(m.DATAVALIDADECNH from 1 for 4) ||'|'||
                substring(m.DATAEMISSAOCNH from 9 for 2) ||'/'|| substring(m.DATAEMISSAOCNH from 6 for 2) ||'/'|| substring(m.DATAEMISSAOCNH from 1 for 4) ||'|'
                FROM FROMOTC m """,

'MotoristaCategoriaCnh' : f""" SELECT
                            distinct
                            {codEntidade} ||'|'||
                            m.codigo ||'|'||
                                case r.IDFROTA
                                when 1 then 'B'
                                when 2 then 'A'
                                when 3 then 'A'
                                when 4 then 'A' else 'A' end ||'|'
                            FROM FROMOTC m
                                left join FROROTC r on (r.MOTORISTA = m.CODIGO) """,

'MotoristaSituacaoCnh' : f""" SELECT
            distinct
            {codEntidade} ||'|'||
            m.codigo ||'|'||
            substring(current_date from 9 for 2) ||'/'|| substring(current_date from 6 for 2) ||'/'|| substring(current_date from 1 for 4) ||'|'||
            1 ||'|'|| -- 1=Normal
            0 ||'|'
            FROM FROMOTC m """,

'Veiculo' : f""" SELECT
            {codEntidade} ||'|'||
            v.CODIGO ||'|'||
            v.NUMTOMBAMENTO ||'|'||
            v.PLACA ||'|'||
            trim(case v.TIPONATUREZA
                when '1  : Veiculos Passeio/Utilitario' then 'Veiculos Passeio/Utilitario'
                when '1:Veiculos Passeio/Utilitario' then 'Veiculos Passeio/Utilitario'
                when '5  : Motos' then 'Motos'
                when '5:Motos' then 'Motos'
                when '52 : Tratores Agricolas' then 'Tratores Agricolas'
                when '52:Tratores Agricolas' then 'Tratores Agricolas'
                when '99:Outros Equipamentos' then 'Outros Equipamentos' end) ||'|'||
            v.MODELO ||'|'||
            v.cor ||'|'||
            v.RENAVAM ||'|'||
            v.CHASSI ||'|'||
            v.MOTOR ||'|'||
            v.ANOFABRICACAO ||'|'||
            v.ANOMODELO ||'|'||
            case v.TIPONATUREZA
                when '1  : Veiculos Passeio/Utilitario' then '1'
                when '1:Veiculos Passeio/Utilitario' then '1'
                when '5  : Motos' then '5'
                when '5:Motos' then '5'
                when '52 : Tratores Agricolas' then '52'
                when '52:Tratores Agricolas' then '52'
                when '99:Outros Equipamentos' then '99' end ||'|'||
            '' ||'|'||
            1 ||'|'|| -- 1=Sim
            case v.TIPOVINCULO
                when '1:PRÓPRIO' then '1'
                when '2:CEDIDO' then '2'
                when '1 : PRÓPRIO' then '1'
                when '2 : CEDIDO' then '2' end ||'|'||
            v.COMBUSTIVEL ||'|'||
            substring(v.DATACAD from 9 for 2) ||'/'|| substring(v.DATACAD from 6 for 2) ||'/'|| substring(v.DATACAD from 1 for 4) ||'|'||
            '1' ||'|'||--obrigatorio
            '1' ||'|'|| --obrigatorio
            '1' ||'|'|| --obrigatorio
            2 ||'|'||
            '' ||'|'
            FROM FROVEIC v """,

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
                    order by a.SEQUENCIA desc """,

'Acumulador' : f""" SELECT 
                {codEntidade} ||'|'||
                coalesce(v.CODIGO,'') ||'|'||
                coalesce(v.NUMTOMBAMENTO,'') ||'|'||
                substring(a.DATA from 9 for 2) ||'/'|| substring(a.DATA from 6 for 2) ||'/'|| substring(a.DATA from 1 for 4) ||' '||'00:00:' || lpad(substring(LPAD(a.SEQUENCIA,6,'0') from 6 for 1), 2, '0') ||'|'||
                2 ||'|'||  --2 - Abastecimento
                a.SEQUENCIA ||'|'||
                '$VlAcumulador$' ||'|'||
                '$TmpVlAcumulador$' ||'|'
                FROM FROMOVC a 
                left join FROVEIC v on (v.IDFROTA = a.IDFROTA)
                where a.TIPO = 6
                order by a.SEQUENCIA asc """,

'ControleSimAm' : f""" SELECT distinct
                    {codEntidade} ||'|'||
                    coalesce(v.CODIGO,'9') ||'|'||
                    '#seq#' ||'|'||
                    case when (SELECT 2 FROM FROROTC r2 where r2.DESTINO = 'Roteiro Anual' and r2.OBSDECLARADA != '.' and r2.OBSDECLARADA != '' and r2.CODIGO = r.CODIGO ) = 2 then 2 else 1 end ||'|'||
                    substring(r.DATARETORNO from 9 for 2) ||'/'|| substring(r.DATARETORNO from 6 for 2) ||'/'|| substring(r.DATARETORNO from 1 for 4) ||'|'||
                    case when r.KMDECLARADA != 0 then r.KMDECLARADA
                    when r.HORADECLARADA != 0 then r.HORADECLARADA else '' end ||'|'||
                    r.OBSDECLARADA ||'|'||
                    case when (SELECT 2 FROM FROROTC r2 where r2.DESTINO = 'Roteiro Anual' and r2.OBSDECLARADA != '.' and r2.OBSDECLARADA != '' and r2.CODIGO = r.CODIGO ) = 2 then 2 else 1 end ||'|'||
                    '' ||'|'||
                    coalesce(v.NUMTOMBAMENTO,'44') ||'|'||
                    coalesce(r.KMSAIDA,'0') ||'|'||
                    coalesce(r.KMRETORNO,'0') ||'|'
                    FROM FROROTC r
                    left join FROVEIC v on (v.IDFROTA = r.IDFROTA)
                    left join FROMOVC ab on (ab.CODROTEIRO = r.CODIGO)
                    where r.DESTINO = 'Roteiro Anual' and r.DATARETORNO < current_date
                    order by r.DATARETORNO, v.NUMTOMBAMENTO """

}