import time
import fdb
import configparser
import script
from bottle import get, post, route, run, debug, template, request, static_file, error

cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

@route('/')
def start():
    dados_conexao = fdb.connect(host='localhost', database=cfg['DEFAULT']['NomeBanco'], user='sysdba', port=3050,
                                password='masterkey')
    cur = dados_conexao.cursor()

    dados_conexao_2 = fdb.connect(host='localhost', database=cfg['DEFAULT']['NomeBanco_2'], user='sysdba', port=3050,
                                password='masterkey')
    cur_2 = dados_conexao_2.cursor()

    comandos = script.scripts
    # while True:
    for comando in comandos:
        print('Arquivo: ' + comando + ' iniciado em ' + time.strftime("%d/%m/%y %H:%M:%S"))
        cur.execute(comandos[comando])
        result = cur.fetchall()

        arquivo = open(cfg['DEFAULT']['DiretorioArquivos'] + comando + '_' + cfg['DEFAULT']['CodEntidade'] + '.txt', "w", newline='', encoding='ANSI')

        #Layout coluna dados --> posição 1= num nota fiscal      2 = km atual    3 = qtde litros    4 = valor    5 = cod fornecedor     6 = razão social fornecedor   7 = tipo combustivel

        for inf in result:
            sequencia = str(inf[0]).split('|')[1]
            cur.execute(f'select a.dados, a.dadosveiculo, a.sequencia from fromovc a where a.TIPO = 6 and a.sequencia = {sequencia}')
            result_1 = cur.fetchall()

            dado = str(result_1[0][0]).split('|')
            dados_veiculo = str(result_1[0][1]).split('|')

            CodProduto_Nome = dado[6].replace(':', '|').replace(' ','').strip()
            NrCodigoMotorista = dados_veiculo[0]
            VlUnitario = round(float(str(result_1[0][0]).split('|')[3].replace('.', '').replace(',', '.').replace('R$ ', '')) / float(str(result_1[0][0]).split('|')[2].replace('.', '').replace(',', '.').replace('R$ ', '')),4)  # valor unitario
            NrLitrosAbastecimento = dado[2].replace(',', '.')
            VlAbastecimento = dado[3].replace(',', '.')
            NrNotaFiscal = dado[0]
            CodFornecedor = dado[4]

            try:
                if CodFornecedor == '0':
                    CodFornecedor = '13'
                    cur_2.execute(f""" select f.NUMCNPJPESQ from FINPESC f where codigo = {CodFornecedor}""")
                    result_2 = cur_2.fetchall()
                    Cnpj = result_2[0][0]

                else:
                    cur_2.execute(f""" select f.NUMCNPJPESQ from FINPESC f where codigo = {CodFornecedor}""")
                    result_2 = cur_2.fetchall()
                    Cnpj = result_2[0][0]

            except: CodFornecedor = '13'

            # arquivo.write(str(inf[0]).replace('$CodProduto$|$Nome$', CodProduto_Nome).replace('$NrCodigoMotorista$', NrCodigoMotorista).replace('$VlUnitario$', str(VlUnitario)).replace('$NrLitrosAbastecimento$', NrLitrosAbastecimento).replace('$VlAbastecimento$',VlAbastecimento).replace('$NrNotaFiscal$',NrNotaFiscal).replace('$CodFornecedor$', CodFornecedor).replace('$Cnpj$',Cnpj).replace('.',',')+'\n')
            linha = (str(inf[0]).replace(
                            '$CodProduto$|$Nome$', CodProduto_Nome).replace(
                            '$NrCodigoMotorista$', NrCodigoMotorista).replace(
                            '$VlUnitario$', str(VlUnitario)).replace(
                            '$NrLitrosAbastecimento$', NrLitrosAbastecimento).replace(
                            '$VlAbastecimento$', VlAbastecimento).replace(
                            '$NrNotaFiscal$', NrNotaFiscal).replace(
                            '$CodFornecedor$', CodFornecedor).replace(
                            '$Cnpj$', Cnpj).replace('.', ',').replace(
                            '$CodPessoa$', '').replace(
                            '$CodLocal$', '').replace(
                            '$NrInterno$', '').replace(
                            '$CodEntidadeLiquidacao$', '').replace(
                            '$ExercicioLiquidacao$', '').replace(
                            '$NrLiquidacao$', '').replace(
                            '$ExLiquidacao$', '').replace(
                            '$CodEntidadeOrigemLiquidacao$', '').replace(
                            '$CodEntidadeEmpenho$', '').replace(
                            '$ExercicioEmpenho$', '').replace(
                            '$NrEmpenho$', '').replace(
                            '$ExEmpenho$', '').replace(
                            '$CodEntidadeOrigemEmpenho$', '').replace(
                            'b''', '').replace(
                            "'", '')
                             + '\n')

            arquivo.write(linha)

        print('Arquivo: ' + comando + ' finalizado em ' + time.strftime("%d/%m/%y %H:%M:%S") + '\n')

    print('Arquivos gerados com sucesso.', cfg['DEFAULT']['NomeEntidade'].replace("'", ''))

    resp = "Arquivos gerados com sucesso!"

    return template('template/index', mensagem='Arquivos gerados com sucesso para ' + cfg['DEFAULT']['NomeEntidade'].replace("'", '') +' \nCaminho '+ cfg['DEFAULT']['DiretorioArquivos'], dados=resp )


run(port=6969, reloader=True)

# pyinstaller --name export_sinopsys_frotas --onefile --noconsole main.py