import json


def cadastro_endereço_usuario(arquivo_end, usuario):
    chaves = ["CEP", "Logradouro", "Complemento", "Bairro", "Localidade", "UF"]
    endereço = {}
    for chave in chaves:
        info_endereço = input(f"Digite o(a) {chave}:")
        endereço[chave] = info_endereço
    try:
        with open(arquivo_end) as f:
            dados_endereço = json.load(f)
    except FileNotFoundError:
        dados_endereço = {}

    cpf = usuario
    dados_endereço[cpf] = endereço

    try:
        with open(arquivo_end, "w") as f:
            json.dump(dados_endereço, f, indent=4)
    except Exception as e:
        print("Ocorreu um erro: ", e)


def cadastro_endereço_locadora(arquivo_end, locadora):
    chaves = ["CEP", "Logradouro", "Complemento", "Bairro", "Localidade", "UF"]
    endereço = {}
    for chave in chaves:
        info_endereço = input(f"Digite o(a) {chave}:")
        endereço[chave] = info_endereço
    try:
        with open(arquivo_end) as f:
            dados_endereço = json.load(f)
    except FileNotFoundError:
        dados_endereço = {}

    cnpj = locadora
    dados_endereço[cnpj] = endereço

    try:
        with open(arquivo_end, "w") as f:
            json.dump(dados_endereço, f, indent=4)
    except Exception as e:
        print("Ocorreu um erro: ", e)
