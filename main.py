from dadosCliente import buscarDadosMonday
from dadosClientesRodados import buscarDadosClientesRodados
from listarOrdens import listarOrdens

tokenJWT = 'JWT '

listaClientesMonday = buscarDadosMonday()

listaClientesRodados = buscarDadosClientesRodados()

for cliente in listaClientesMonday:

    contaCliente = cliente['conta']
    nomeCliente = cliente['nome']

    if contaCliente in listaClientesRodados:
        print(f'O cliente {nomeCliente} já se encontra na base de clientes rodados.')
        continue

    print(f'Baixando arquivos do cliente {nomeCliente}')

    listarOrdens(cliente, tokenJWT)

print('PROCESSO FINALIZADO')
