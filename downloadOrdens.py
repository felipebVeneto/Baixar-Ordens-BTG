import os
import time
import requests

def baixarOrdem(idOrdem, cpfCliente, contaCliente, nomeCliente, officer, headers, nomeOrdem, dataStr):
    url = f'https://access.btgpactualdigital.com/op/api/history/clients/{cpfCliente}/accounts/{contaCliente}/report-requests/download/{idOrdem}'

    diretorio = 'C:\\Users\\felipe.batista\\Desktop\\Ordens Baixadas BTG'

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        
        mes = dataStr.month
        ano = dataStr.year

        # Caminho completo para a pasta do cliente
        pastaOfficer = os.path.join(diretorio, officer)

        # Verificar se a pasta do officer já existe
        if not os.path.exists(pastaOfficer):
            os.makedirs(pastaOfficer)

        # Caminho completo para a pasta do cliente
        pastaCliente = os.path.join(pastaOfficer, nomeCliente)

        # Verificar se a pasta do cliente já existe
        if not os.path.exists(pastaCliente):
            os.makedirs(pastaCliente)

        # Caminho completo para a pasta do ano
        pastaAno = os.path.join(pastaCliente, str(ano))

        # Verificar se a pasta do ano já existe
        if not os.path.exists(pastaAno):
            os.makedirs(pastaAno)

        # Caminho completo para a pasta do mes
        pastaMes = os.path.join(pastaAno, str(mes))

        # Verificar se a pasta do mes já existe
        if not os.path.exists(pastaMes):
            os.makedirs(pastaMes)
            
        # Caminho completo para o arquivo PDF
        caminhoArq = os.path.join(pastaMes, nomeOrdem)

        # Verificar se o arquivo já existe
        if not os.path.exists(caminhoArq):
            # Se não existir, salvar o arquivo PDF
            with open(caminhoArq, 'wb') as pdf_file:
                pdf_file.write(response.content)
                return 'Baixado'
        else:
            # Se já existir, exibir uma mensagem ou fazer algo
            log = f'O arquivo {nomeOrdem} já existe na pasta do cliente.'
            print('--------------------------------')
            print(log)
            return log

    else:
        log = f'{response.status_code}, não foi possível realizar o download do arquivo {nomeOrdem}'
        print('--------------------------------')
        print(log)
        return log

