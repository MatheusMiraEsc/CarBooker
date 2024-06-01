from colorama import init, Fore, Style


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
    for chave in chaves:
        info_endereço = input(f"Digite o(a) {chave}: ")
        endereço[chave] = info_endereço
    return endereço


def clear_screen():
    print("\033c", end="")


def print_verde(texto):
    print(Fore.GREEN + texto + Style.RESET_ALL)


def print_vermelho(texto):
    print(Fore.RED + texto + Style.RESET_ALL)
