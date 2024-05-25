import requests


def buscar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "CEP não encontrado ou erro na requisição"}


cep_info = buscar_cep("51190290")

if not ('error' in dict.keys(cep_info)):
    print(cep_info['cep'])
    print(cep_info['logradouro'])
    print(cep_info['complemento'])
else:
    print("Deu erro")
