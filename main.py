from dadosCliente import buscarDadosMonday
from dadosClientesRodados import buscarDadosClientesRodados
from listarOrdens import listarOrdens

tokenJWT = 'JWT eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0Mjk2ZDBjNS1jMWE0LTQ4YWUtYTZmZS0yYTk2NjZjY2IxNTkiLCJzdWIiOiJhMTE1NTY1Mzk2MzAiLCJ0eXBlIjoiZXh0ZXJuYWwiLCJwcm9maWxlVHlwZSI6IkVYVCIsInByb2ZpbGVJZCI6Ijk5NTViOGFjLTZkOTMtNGNmZC04NTIxLTg2ZWI2Y2JjZGYxZCIsInVzZXJQcm9maWxlSWQiOiI0MDNlOGY4Ny0zMDljLTRlMzgtODllNC05NjVlNDNhOWE3MTQiLCJtb2JpbGUiOmZhbHNlLCJraWQiOiIzZWZjOTk4ZTY3ODRhN2IzZWM5ZTQzMjBmOTVkMTNmYTI0YjAxODhiIiwiaXNzIjoiYnRnX2FnZW50ZXNfcm1hZG1pbiIsInR0bCI6IjE0NDAwMDAwIiwiaWF0IjoxNzEyMDY2Nzc0LCJleHAiOjE3MTIxMDk5NzR9.VujgrQ-ysTPVLUldy3ZGEtlg_5X5edbjilTIuB9tk7qI_YUG4rMHtqRsi1VLTMHtrVmzRaltxgKzG7t-3johlV9nlq66sEMn7TVP-0OKfUD4kjRS7rWz-5TcUMggFHGl3l2zZPhX1MinuAE84bYiX1LyxtsLlsNHTjNuSI2qrsxQXz9l_H4PapHpyBwtCb1UIKsETUJHQeE0C-62YKkh2StCBEk8qeHG-soqUuGlITwCOYwA-gpy39yWF1WJ1Wm46Ojn84ERRcWEUKoCdgCsu71EljfNVqt4MbKV0IdT3qVwjBgBohmt6XgJnK7Z3FAbCOQhKbxLg59FU8BeV2y0JQ'

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