from colorama import init, Fore, Style
import requests
from validação import validar_cep


def menuOptions():
    print("\n============================")
    print("Bem-vindo(a) ao CarBooker!!")
    print("============================")
    print("1. Cadastro")
    print("2. Login")
    print("3. Sair")
    print("============================")


def cadastro_endereço():
    chaves = ["CEP", "Rua", "Complemento", "Bairro", "Cidade", "UF"]
    endereço = {}

    while True:
        cep = input(
            "Digite o CEP (apenas números, 8 dígitos) ou aperte enter para continuar: ")
        if cep == "":
            pulou_cep = True
            break
        if not validar_cep(cep):
            clear_screen()
            print("===============================================================")
            print_vermelho(
                "CEP inválido. Por favor, insira um CEP com 8 dígitos numéricos.")
            print("===============================================================")
            continue

        dados_cep = buscar_cep(cep)

        if "error" in dados_cep:
            clear_screen()
            print("==================")
            print_vermelho(dados_cep["error"])
            print("==================")
            retry = input("Deseja tentar novamente? (S/N): ")
            if retry.lower() == 'n':
                continue
        else:
            endereço["CEP"] = cep
            endereço["Rua"] = dados_cep.get("logradouro", "")
            endereço["Bairro"] = dados_cep.get("bairro", "")
            endereço["Cidade"] = dados_cep.get("localidade", "")
            endereço["UF"] = dados_cep.get("uf", "")
            complemento = input("Digite o Complemento: ")
            endereço["Complemento"] = complemento
            return endereço
    if pulou_cep:
        chaves.remove("CEP")
        for chave in chaves:
            info_endereço = input(f"Digite o(a) {chave}: ")
            endereço["CEP"] = ""
            endereço[chave] = info_endereço
        return endereço


def clear_screen():
    print("\033c", end="")


def print_verde(texto):
    print(Fore.GREEN + texto + Style.RESET_ALL)


def print_vermelho(texto):
    print(Fore.RED + texto + Style.RESET_ALL)


def buscar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "CEP não encontrado ou erro na requisição"}
