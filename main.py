import time
import fdb
import time
import configparser
import script
import arquivoAbastecimentoAcumulador
from bottle import get, post, route, run, debug, template, request, static_file, error


cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

def cached_time():
    cached_time.counter += 1
    return time.strftime('%H:%M:%S', time.gmtime(cached_time.counter))

# Inicializa o contador com valor 0
cached_time.counter = 0

@route('/')
def start():
    dados_conexao = fdb.connect(host='localhost', database=cfg['DEFAULT']['NomeBanco'], user='sysdba', port=3050,
                                password='masterkey')
    cur = dados_conexao.cursor()

    comandos = script.scripts

    for comando in comandos:

        if comando not in ['Abastecimento', 'Acumulador']:

            cur.execute(comandos[comando])
            result = cur.fetchall()

            arquivo = open(cfg['DEFAULT']['DiretorioArquivos'] + comando + '_' + cfg['DEFAULT']['CodEntidade'] + '.txt', "w", newline='', encoding='ANSI')

            #Layout coluna dados --> posição 1= num nota fiscal      2 = km atual    3 = qtde litros    4 = valor    5 = cod fornecedor     6 = razão social fornecedor   7 = tipo combustivel
            print('Arquivo: ' + comando + ' iniciado em ' + time.strftime("%d/%m/%y %H:%M:%S"))

            sequencia = 0
            for inf in result:
                if comando == 'ControleSimAm':
                    sequencia = sequencia + 1
                    linha = str(inf[0]).replace('#seq#', str(sequencia))
                    arquivo.write(linha + '\n')
                else:
                    arquivo.write(inf[0] + '\n')

            print('Arquivo: ' + comando + ' finalizado em ' + time.strftime("%d/%m/%y %H:%M:%S") + '\n')

    arquivoAbastecimentoAcumulador.criar()

    print('Arquivos gerados com sucesso.', cfg['DEFAULT']['NomeEntidade'].replace("'", ''))

    resp = "Arquivos gerados com sucesso!"

    return template('template/index', mensagem='Arquivos gerados com sucesso para ' + cfg['DEFAULT']['NomeEntidade'].replace("'", '') +' \nCaminho '+ cfg['DEFAULT']['DiretorioArquivos'], dados=resp )

run(port=6969, reloader=True)

# pyinstaller --name export_sinopsys_frotas --onefile --noconsole main.py