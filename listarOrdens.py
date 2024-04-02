import locale
import pandas as pd
import requests
import time
from datetime import datetime
from downloadOrdens import baixarOrdem

# Baixou 79 arquivos em 4m15s

def listarOrdens(cliente, tokenJWT):

    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

    contaCliente = cliente['conta']

    cpfCliente = cliente['cpf']
    cpfCliente = cpfCliente.replace('.', '').replace('-', '')

    nomeCliente = cliente['nome']

    officer = cliente['officer']

    url = f'https://access.btgpactualdigital.com/op/api/history/accounts/{contaCliente}/reports'

    # payload = {
    #     "period": "30",
    #     "reportTypes": [
    #         "RF_REPORT",
    #         "DERIVATIVES_REPORT",
    #         "CONTRATO_CAMBIO",
    #         "PREVIDENCIA_CERTIFICADO",
    #         "CRIPTOATIVOS_REPORT",
    #         "COE_REPORT"
    #     ]
    # }

    payload = {
        "dateRange":
        {
        "startDate": "2019-04-01T00:00:00.000Z",
        "endDate": "2024-03-29T00:00:00.000Z"
        },
        "reportTypes": [
            "RF_REPORT",
            "DERIVATIVES_REPORT",
            "CONTRATO_CAMBIO",
            "PREVIDENCIA_CERTIFICADO",
            "CRIPTOATIVOS_REPORT",
            "COE_REPORT"
        ]
    }

    headers = {
        "Authorization": tokenJWT,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "X-System-From": "RMADMIN"

    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        ordens = response.json()

        numOrdens = len(ordens)

        clientesRodados = pd.read_excel('Clientes Rodados.xlsx', dtype={'CONTA': str})
        numLinhas = clientesRodados.shape[0]

        if numLinhas > 0:
            lin = numLinhas + 1
        else:
            lin = 1

        clienteExiste = clientesRodados.loc[clientesRodados['CONTA'] == contaCliente]
        
        if clienteExiste.empty:
            clientesRodados.loc[lin, "CLIENTE"] = nomeCliente
            clientesRodados.loc[lin, "CONTA"] = contaCliente
            clientesRodados.loc[lin, "NOTAS TOTAIS"] = numOrdens
            clientesRodados.loc[lin, "NOTAS BAIXADAS"] = 0
        
        clientesRodados.to_excel('Clientes Rodados.xlsx', index=False)

        notasBaixadasCliente = 0

        logDownloads = pd.read_excel('logDownloads.xlsx', dtype={'CONTA': str})

        numLinhasLog = logDownloads.shape[0]
 
        if numLinhasLog > 0:
            linLog = numLinhasLog + 1
        else:
            linLog = 1

        for ordem in ordens:
            nomeOrdem = ordem['description']

            #Formata a data
            data = ordem['publicationDate']
            dataStr = datetime.strptime(data, '%Y-%m-%dT%H:%M:%S.%f%z')
            dataFormatada = dataStr.strftime('%d.%m.%Y')
            
            idOrdem = ordem['fileId']
                
            nomeArq = f'{nomeOrdem} - {dataFormatada} - {idOrdem}.pdf'

            log = baixarOrdem(idOrdem, cpfCliente, contaCliente, nomeCliente, officer, headers, nomeArq, dataStr)

            logDownloads.loc[linLog, "CLIENTE"] = nomeCliente
            logDownloads.loc[linLog, "CONTA"] = contaCliente
            logDownloads.loc[linLog, "ORDEM"] = nomeArq

            if log == 'Baixado':
                notasBaixadasCliente += 1
                logDownloads.loc[linLog, "LOG"] = log

            else:
                logDownloads.loc[linLog, "LOG"] = log

            logDownloads.to_excel('logDownloads.xlsx', index=False)

            linLog +=1
            
            clientesRodados = pd.read_excel('Clientes Rodados.xlsx', dtype={'CONTA': str})

            linhaConta = clientesRodados.loc[clientesRodados['CONTA'] == contaCliente]
            linhaConta = linhaConta.index[0]

            clientesRodados.loc[linhaConta, "NOTAS BAIXADAS"] = notasBaixadasCliente
                
            clientesRodados.to_excel('Clientes Rodados.xlsx', index=False)

            time.sleep(5) 
    else:
        if response.status_code == 404:
            print(f'Não foram encontrados notas de corretagem para o cliente {nomeCliente} - {contaCliente}')

            clientesSemNota = pd.read_excel('Clientes Sem Nota.xlsx', dtype={'CONTA': str})

            numLinSemNota = clientesSemNota.shape[0]
    
            if numLinSemNota > 0:
                linSemNota = numLinSemNota + 1
            else:
                linSemNota = 1

            clientesSemNota.loc[linSemNota, "CLIENTE"] = nomeCliente
            clientesSemNota.loc[linSemNota, "CONTA"] = contaCliente
            
            clientesSemNota.to_excel('Clientes Sem Nota.xlsx', index=False)
        else:
            print(response)
