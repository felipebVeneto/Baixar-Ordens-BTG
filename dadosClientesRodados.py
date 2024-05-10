
import pandas as pd

def buscarDadosClientesRodados():

    diretorio = 'Bases/'
    clientesRodados = pd.read_excel(f'{diretorio}Clientes Rodados.xlsx', dtype={'CONTA': str})
    numLinhas = clientesRodados.shape[0]
    print(numLinhas)

    listaClientes = {}

    if numLinhas > 0:
        
        ultLin = clientesRodados.iloc[-1].name

        for lin in range(ultLin + 1):
            conta = clientesRodados.loc[lin, "CONTA"]
            ultAtual = clientesRodados.loc[lin, "ULT. ATUALIZAÇÃO"]

            listaClientes[conta] = ultAtual

    return listaClientes