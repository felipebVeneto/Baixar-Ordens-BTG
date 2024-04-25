from dadosCliente import buscarDadosMonday
from dadosClientesRodados import buscarDadosClientesRodados
from listarOrdens import listarOrdens

tokenJWT = 'JWT eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMjRmY2JkZS04YjBlLTRlOGUtODYyZi1iYTVkNmI1Nzk1ZDgiLCJzdWIiOiJhMTE1NTY1Mzk2MzAiLCJ0eXBlIjoiZXh0ZXJuYWwiLCJwcm9maWxlVHlwZSI6IkVYVCIsInByb2ZpbGVJZCI6Ijk5NTViOGFjLTZkOTMtNGNmZC04NTIxLTg2ZWI2Y2JjZGYxZCIsInVzZXJQcm9maWxlSWQiOiI0MDNlOGY4Ny0zMDljLTRlMzgtODllNC05NjVlNDNhOWE3MTQiLCJtb2JpbGUiOmZhbHNlLCJraWQiOiIzZWZjOTk4ZTY3ODRhN2IzZWM5ZTQzMjBmOTVkMTNmYTI0YjAxODhiIiwiaXNzIjoiYnRnX2FnZW50ZXNfcm1hZG1pbiIsInR0bCI6IjE0NDAwMDAwIiwiaWF0IjoxNzEzMzYxMzc2LCJleHAiOjE3MTM0MDQ1NzZ9.SEd34Q_yN_qPVTAtKBKQQw3NUJpve5NwWft_xzpgyjZYo_ZMXfiKyhn-Sv_P46hfwv6frcU5GOh_KDVZM460JXVP5BtH2E2NUaFd9pjYvsu4c9zsX17aoxI0auaUPYZW-QVahOr02GcOw6i7FAwoGjfsquPUEaNkAbjQGFH54jWD1E3tTC7K38VDzHpWU7wLYqV8-8ppv2IJckjHFymzRza8i8oVdkxgUw_wIBgUOEvn09LnHBL5LNcyq83kmEBvo-SLo4Bl6MlGMY-5ic-2S9K8wr7Uh5Gew_SYAXtgDuJgb1E1kczoCRkRqESVjTtupjetidKxRgG8em4MBc3_Pw'

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