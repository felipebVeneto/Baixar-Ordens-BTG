from dadosCliente import buscarDadosMonday
from dadosClientesRodados import buscarDadosClientesRodados
from listarOrdens import listarOrdens

tokenJWT = 'JWT '

listaClientesMonday = buscarDadosMonday()

listaClientesRodados = buscarDadosClientesRodados()

nClientes = 0

for cliente in listaClientesMonday:

    contaCliente = cliente['conta']
    nomeCliente = cliente['nome']

    nClientes += 1
    
    print('----------------')
    print(f'Cliente Numero {nClientes}')
    
    if contaCliente in listaClientesRodados:
        print(f'O cliente {nomeCliente} já se encontra na base de clientes rodados ou clientes sem nota.')
        continue
    
    print('----------------')
    print(f'Baixando arquivos do cliente {nomeCliente}')

    listarOrdens(cliente, tokenJWT)

print('PROCESSO FINALIZADO')
