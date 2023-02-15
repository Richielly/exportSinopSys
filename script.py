import configparser
cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

nomeBanco = cfg['DEFAULT']['NomeBanco']
codEntidade = cfg['DEFAULT']['CodEntidade']
nomeEntidade = cfg['DEFAULT']['NomeEntidade']
motorista = cfg['DEFAULT']['Motorista']

scripts = {

'Abastecimento' : f""" SELECT
                    a.dados,
                    a.dadosveiculo
                    FROM FROMOVC a
                    left join FROVEIC v on (v.IDFROTA = a.IDFROTA)
                    join FROROTC r on (r.CODIGO = a.CODROTEIRO)
                    where a.TIPO = 6
                    order by a.SEQUENCIA desc """
}