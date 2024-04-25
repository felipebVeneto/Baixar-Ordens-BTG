
import pandas as pd

def buscarDadosClientesRodados():

    clientesRodados = pd.read_excel('Clientes Rodados.xlsx', dtype={'CONTA': str})
    numLinhas = clientesRodados.shape[0]
    print(numLinhas)

    listaClientes = []

    if numLinhas > 0:
        
        ultLin = clientesRodados.iloc[-1].name

        for lin in range(ultLin + 1):
            conta = clientesRodados.loc[lin, "CONTA"]
            listaClientes.append(conta)


    clientesSemNota = pd.read_excel('Clientes Sem Nota.xlsx', dtype={'CONTA': str})
    numLinNota = clientesSemNota.shape[0]
    print(numLinNota)

    if numLinNota > 0:
    

        for lin in range(numLinNota):
            conta = clientesSemNota.loc[lin, "CONTA"]
            listaClientes.append(conta)

    return listaClientes
        

    