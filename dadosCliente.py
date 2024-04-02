import math

import pandas as pd

def buscarDadosMonday():

    monday = pd.read_excel('monday.xlsx', skiprows=(0, 1), dtype={'CONTA BTG': str})

    ultLin = monday.iloc[-1].name

    listaClientes = []

    lin = 2

    for lin in range(ultLin + 1):

        nbBTG = monday.loc[lin, "CONTA BTG"]

        if type(nbBTG) == float and math.isnan(nbBTG):
            nbBTG = "-"
        
        # Pega o nome
        nomeCliente = monday.loc[lin, "Name"]

        cpf = monday.loc[lin, "CPF / CNPJ"]

        # Pega o nome do Officer
        officer = monday.loc[lin, "FARMER"]
    
        if nbBTG != '-':

            cliente = {
                'nome': nomeCliente,
                'cpf': cpf,
                'officer':officer,
                'conta': nbBTG,
            }

            listaClientes.append(cliente)

    return listaClientes

