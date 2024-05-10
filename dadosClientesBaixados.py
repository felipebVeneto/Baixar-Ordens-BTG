
import pandas as pd

def buscarDadosClientesBaixados():
    diretorio = 'Bases/'
    clientesBaixados = pd.read_excel(f'{diretorio}Clientes Baixados.xlsx', dtype={'CONTA': str})
    numLinhas = clientesBaixados.shape[0]
    print(numLinhas)

    listaClientes = []

    if numLinhas > 0:
        
        ultLin = clientesBaixados.iloc[-1].name

        for lin in range(ultLin + 1):
            conta = clientesBaixados.loc[lin, "CONTA"]
            listaClientes.append(conta)


    # clientesSemNota = pd.read_excel('Clientes Sem Nota.xlsx', dtype={'CONTA': str})
    # numLinNota = clientesSemNota.shape[0]
    # print(numLinNota)

    # if numLinNota > 0:
    

    #     for lin in range(numLinNota):
    #         conta = clientesSemNota.loc[lin, "CONTA"]
    #         listaClientes.append(conta)

    return listaClientes
        

    