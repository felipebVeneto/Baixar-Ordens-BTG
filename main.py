from atualizarClientesNovos import atualizarClientesNovos
from dadosCliente import buscarDadosMonday
from dadosClientesBaixados import buscarDadosClientesBaixados
from dadosClientesRodados import buscarDadosClientesRodados
from listarOrdens import listarOrdens

tokenJWT = 'JWT .eyJqdGkiOiJhM2JjYzQ3Yi01OGJjLTQ5MzktODY1ZS0wZWU5OTA3ZDZmMTMiLCJzdWIiOiJhMTE1NTY1Mzk2MzAiLCJ0eXBlIjoiZXh0ZXJuYWwiLCJwcm9maWxlVHlwZSI6IkVYVCIsInByb2ZpbGVJZCI6Ijk5NTViOGFjLTZkOTMtNGNmZC04NTIxLTg2ZWI2Y2JjZGYxZCIsInVzZXJQcm9maWxlSWQiOiI0MDNlOGY4Ny0zMDljLTRlMzgtODllNC05NjVlNDNhOWE3MTQiLCJtb2JpbGUiOmZhbHNlLCJraWQiOiIzZWZjOTk4ZTY3ODRhN2IzZWM5ZTQzMjBmOTVkMTNmYTI0YjAxODhiIiwiaXNzIjoiYnRnX2FnZW50ZXNfcm1hZG1pbiIsInR0bCI6IjE0NDAwMDAwIiwiaWF0IjoxNzE1MDkwMTUyLCJleHAiOjE3MTUxMzMzNTJ9.Uy7UsVEisCptQWPw3vYNrpVLrKhRsPhxW38_6ST5E0-5ec6o9Hf65etO4DqaIdYVnp0nZwbBNQGEZ3SjQjRDUZybu5YOzkYZbs2bsj1V5weUQiHfbv33oNFsJYJFDqKQe5920QBgfp_LdfNn0Vb7Ty-Kj2iWOhvrbrUb8h89m_npJnsNfVJ5P-X5BHJBcfbaPMwtZLyw7k020v3AOkBYaCP_b-By1-b-CQqy9hTOvDVBCbGe1G-GQusC51LWz4Ij7YKinqCZ21Ob_JX6RKYsAwZ5Y1cMVzDW7tGV7Aa-3EwRdwBu7FOpRKmtsecuPV09SH0we-YhjfeVIHBnEmCWBg'

listaClientesNovos = []

# Pega a lista de clientes do Monday
listaClientesMonday = buscarDadosMonday()
# Pega a lista de clientes que ja foram rodados pelomenos uma vez
listaClientesRodados = buscarDadosClientesRodados()
# Pega a lista de clientes que tem notas baixadas
listaClientesBaixados = buscarDadosClientesBaixados()

# Determina os clientes nunca foram rodados
for cliente in listaClientesMonday:
    contaCliente = cliente['conta']
    if contaCliente not in listaClientesRodados:
        listaClientesNovos.append(contaCliente)
    else:
        cliente['ultAtualizacao'] = listaClientesRodados[contaCliente]

# atualizarClientesNovos(listaClientesNovos)

nClientes = 0

for cliente in listaClientesMonday:

    contaCliente = cliente['conta']
    nomeCliente = cliente['nome']

    nClientes += 1
    
    print('----------------')
    print(f'Cliente Numero {nClientes}')
    
    # if contaCliente in listaClientesNovos:
    #     print(f'O cliente {nomeCliente} nunca foi rodado antes. Serão baixados arquivos desde o ano de 2019.')
    #     dataInicio = '2019-04-01'
    # else:
    #     dataInicio = cliente['ultAtualizacao']
    #     dataInicio = dataInicio.strftime('%Y-%m-%d')
        
    dataInicio = cliente['ultAtualizacao']
    dataInicio = dataInicio.strftime('%Y-%m-%d')    

    print('----------------')
    print(f'Baixando arquivos do cliente {nomeCliente}')

    listarOrdens(cliente, tokenJWT, dataInicio)

print('PROCESSO FINALIZADO')
