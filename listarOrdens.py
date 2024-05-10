import locale
import pandas as pd
import requests
import time
from datetime import datetime , date
from downloadOrdens import baixarOrdem

# Baixou 79 arquivos em 4m15s

def listarOrdens(cliente, tokenJWT, dataInicio):

    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

    dataAtual = date.today()
    dataFormatada = dataAtual.strftime('%Y-%m-%d')
    contaCliente = cliente['conta']
    cpfCliente = cliente['cpf']
    cpfCliente = cpfCliente.replace('.', '').replace('‐', '').replace('-', '').replace('/', '')
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
        "startDate": f"{dataInicio}T00:00:00.000Z",
        "endDate": f"{dataAtual}T00:00:00.000Z"
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

        # Atualiza a base de clientes Baixados
        clientesBaixados = pd.read_excel('Bases/Clientes Baixados.xlsx', dtype={'CONTA': str})
        numLinhas = clientesBaixados.shape[0]

        if numLinhas > 0:
            lin = numLinhas + 1
        else:
            lin = 1

        clienteExiste = clientesBaixados.loc[clientesBaixados['CONTA'] == contaCliente]
        
        
        if clienteExiste.empty:
            clientesBaixados.loc[lin, "CLIENTE"] = nomeCliente
            clientesBaixados.loc[lin, "CONTA"] = contaCliente
            clientesBaixados.loc[lin, "NOTAS TOTAIS"] = numOrdens
            clientesBaixados.loc[lin, "NOTAS BAIXADAS"] = 0
            notasBaixadasAtuais = 0
        else:
            linhaConta = clienteExiste.index[0]
            
            if dataAtual != dataInicio:
                numOrdensAtual = clientesBaixados.loc[linhaConta, "NOTAS TOTAIS"]
                numOrdens = numOrdensAtual + numOrdens
                clientesBaixados.loc[linhaConta, "NOTAS TOTAIS"] = numOrdens

            notasBaixadasAtuais = clientesBaixados.loc[linhaConta, "NOTAS BAIXADAS"]
        
        clientesBaixados.to_excel('Bases/Clientes Baixados.xlsx', index=False)

        # Atualiza a base de Clientes Rodados
        clientesRodados = pd.read_excel('Bases/Clientes Rodados.xlsx', dtype={'CONTA': str})

        numLinhas = clientesRodados.shape[0]

        if numLinhas > 0:
            lin = numLinhas + 1
        else:
            lin = 1

        clienteExiste = clientesRodados.loc[clientesRodados['CONTA'] == contaCliente]

        if clienteExiste.empty:
            clientesRodados.loc[lin, "NOME"] = nomeCliente
            clientesRodados.loc[lin, "CONTA"] = contaCliente
            clientesRodados.loc[lin, "STATUS"] = 'RODADO'
            clientesRodados.loc[lin, "ULT. ATUALIZAÇÃO"] = dataAtual
        else:
            linhaConta = clienteExiste.index[0]
            clientesRodados.loc[linhaConta, "STATUS"] = 'RODADO'
            clientesRodados.loc[linhaConta, "ULT. ATUALIZAÇÃO"] = dataAtual

        clientesRodados.to_excel('Bases/Clientes Rodados.xlsx', index=False)

           
        notasBaixadasCliente = 0

        logDownloads = pd.read_excel('Bases/logDownloads.xlsx', dtype={'CONTA': str})

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

            logDownloads.to_excel(f'Bases/logDownloads - {dataAtual}.xlsx', index=False)

            linLog +=1
            
            clientesBaixados = pd.read_excel('Bases/Clientes Baixados.xlsx', dtype={'CONTA': str})

            linhaConta = clientesBaixados.loc[clientesBaixados['CONTA'] == contaCliente]
            linhaConta = linhaConta.index[0]

            clientesBaixados.loc[linhaConta, "NOTAS BAIXADAS"] = notasBaixadasAtuais + notasBaixadasCliente
            
            clientesBaixados.to_excel('Bases/Clientes Baixados.xlsx', index=False)

            time.sleep(5) 
    else:
        if response.status_code == 404:
            print('----------------')
            print(f'Não foram encontrados notas de corretagem para o cliente {nomeCliente} - {contaCliente}')

            clientesSemNota = pd.read_excel('Bases/Clientes Sem Nota.xlsx', dtype={'CONTA': str})

            numLinSemNota = clientesSemNota.shape[0]
    
            if numLinSemNota > 0:
                linSemNota = numLinSemNota + 1
            else:
                linSemNota = 1

            clientesSemNota.loc[linSemNota, "CLIENTE"] = nomeCliente
            clientesSemNota.loc[linSemNota, "CONTA"] = contaCliente
            
            clientesSemNota.to_excel('Bases/Clientes Sem Nota.xlsx', index=False)

            # Atualiza a base de Clientes Rodados
            clientesRodados = pd.read_excel('Bases/Clientes Rodados.xlsx', dtype={'CONTA': str})

            numLinhas = clientesRodados.shape[0]

            if numLinhas > 0:
                lin = numLinhas + 1
            else:
                lin = 1

            clienteExiste = clientesRodados.loc[clientesRodados['CONTA'] == contaCliente]

            if clienteExiste.empty:
                clientesRodados.loc[lin, "NOME"] = nomeCliente
                clientesRodados.loc[lin, "CONTA"] = contaCliente
                clientesRodados.loc[lin, "STATUS"] = 'SEM NOTA'
                clientesRodados.loc[lin, "ULT. ATUALIZAÇÃO"] = dataAtual
            else:
                linhaConta = clienteExiste.index[0]
                clientesRodados.loc[linhaConta, "STATUS"] = 'SEM NOTA'
                clientesRodados.loc[linhaConta, "ULT. ATUALIZAÇÃO"] = dataAtual

            clientesRodados.to_excel('Bases/Clientes Rodados.xlsx', index=False)
        else:
            print('----------------')
            print(f'Ocorreu um erro ao solicitar as notas do {nomeCliente} - {contaCliente} - Response: {response}')

            logErros = pd.read_excel('Bases/logErros.xlsx', dtype={'CONTA': str})

            numLinLogErros = logErros.shape[0]
    
            if numLinLogErros > 0:
                linLogErros = numLinLogErros + 1
            else:
                linLogErros = 1

            logErros.loc[linLogErros, "CLIENTE"] = nomeCliente
            logErros.loc[linLogErros, "CONTA"] = contaCliente
            logErros.loc[linLogErros, "ERRO"] = response.status_code
            logErros.loc[linLogErros, "HORA"] = dataAtual

            logErros.to_excel(f'Bases/logErros - {dataAtual}.xlsx', index=False)

                        # Atualiza a base de Clientes Rodados
            clientesRodados = pd.read_excel('Bases/Clientes Rodados.xlsx', dtype={'CONTA': str})

            numLinhas = clientesRodados.shape[0]

            if numLinhas > 0:
                lin = numLinhas + 1
            else:
                lin = 1

            clienteExiste = clientesRodados.loc[clientesRodados['CONTA'] == contaCliente]

            if clienteExiste.empty:
                clientesRodados.loc[lin, "NOME"] = nomeCliente
                clientesRodados.loc[lin, "CONTA"] = contaCliente
                clientesRodados.loc[lin, "STATUS"] = 'ERRO'
                clientesRodados.loc[lin, "ULT. ATUALIZAÇÃO"] = dataAtual
            else:
                linhaConta = clienteExiste.index[0]
                clientesRodados.loc[linhaConta, "STATUS"] = 'ERRO'
                clientesRodados.loc[linhaConta, "ULT. ATUALIZAÇÃO"] = dataAtual

            clientesRodados.to_excel('Bases/Clientes Rodados.xlsx', index=False)
