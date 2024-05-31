import json
from time import sleep
from util import clear_screen
from tabulate import tabulate


def menu_locadora(dadosLocadora):
    arquivo_json = "carros.json"
    while True:
        clear_screen()
        print("\n=================================")
        print("1. Cadastrar Carro")
        print("2. Visualizar Carros")
        print("3. Atualizar informações do Carro")
        print("4. Deletar Carro")
        print("5. Voltar")
        print("=================================")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            carro = cadastrar_carro(dadosLocadora)
            add_carro(carro, arquivo_json)
        elif opcao == "2":
            visualizar_carro_locadora(arquivo_json)
        elif opcao == "3":
            atualizar_carro(arquivo_json)
        elif opcao == "4":
            deletar_carro(arquivo_json)
        elif opcao == "5":
            break
        else:
            clear_screen()
            print("\n====================================")
            print("Opção inválida! Tente novamente\n")
            print("====================================")
            sleep(2)


def contem_numero(s):
    return any(char.isdigit() for char in s)


def contem_letra(s):
    return any(char.isalpha() for char in s)


def cadastrar_carro(locadora):

    campos = ["Modelo", "Marca", "ID Chassis", "Numero de portas", "Ano", "Categoria",
              "Placa", "Capacidade mala", "Capacidade combustivel", "Capacidade passageiro",
              "Quilometragem", "Cambio", "Cor", "Tipo combustivel"]

    carro = {}
    carro["Locadora"] = locadora["Nome"]
    carro["CNPJ da locadora"] = locadora["CNPJ"]

    for campo in campos:
        dados_carro = input(f"Digite o(a) {campo}: ")

        if campo == "Numero de portas" or campo == "Ano" or campo == "Capacidade mala" or campo == "Capacidade combustivel" or campo == "Capacidade passageiro" or campo == "Quilometragem":
            while not dados_carro.isdigit():
                print(f"{campo} deve conter apenas números.")
                dados_carro = input(f"Digite o {campo}: ")

        elif campo == "Modelo" or campo == "Marca" or campo == "Categoria" or campo == "Tipo combustivel" or campo == "Cambio" or campo == "Cor":
            while not dados_carro.isalpha():
                print(f"{campo} deve conter apenas letras.")
                dados_carro = input(f"Digite o {campo}: ")

        elif campo == "ID Chassis" or campo == "Placa":
            while not contem_letra(dados_carro) or not contem_numero(dados_carro):
                print(f"{campo} deve conter letras e números.")
                dados_carro = input(f"Digite o {campo}: ")

        carro["Status reserva"] = "Disponivel"
        carro[campo] = dados_carro

    return carro


def add_carro(carro, arquivo):
    try:
        with open(arquivo, "r") as f:
            dados = json.load(f)
    except FileNotFoundError:
        dados = {}
    except Exception as e:
        print("Ocorreu um erro: ", e)

    numero_carros = len(dados) + 1
    nome_carro = f"Carro {numero_carros}"
    dados[nome_carro] = carro

    try:
        with open(arquivo, "w") as f:
            json.dump(dados, f, indent=4)
        print(f"Carro {numero_carros} cadastrado com sucesso!")
    except Exception as e:
        print("Ocorreu um erro: ", e)


def visualizar_carro_usuario(arquivo):
    try:
        with open(arquivo, "r") as f:
            carros = json.load(f)
            modelo = input("Digite o modelo do carro que deseja visualizar: ")
            carro_encontrado = False
            tabela = []

            for nome_carro, info in carros.items():
                if info["Modelo"] == modelo:
                    carro_encontrado = True
                    tabela.append(("Nome do Carro", nome_carro))
                    for chave, valor in info.items():
                        tabela.append((chave, valor))
                    break

        if carro_encontrado:
            print(tabulate(tabela, headers=[
                  "Campo", "Informação"], tablefmt="rounded_grid"))
            input("Pressione Enter para continuar.")
        if not carro_encontrado:
            clear_screen()
            print("\n=====================")
            print("Carro não encontrado.")
            print("=====================")
            sleep(2)
    except FileNotFoundError:
        print("Arquivo não encontrado")
        sleep(2)
    except Exception as e:
        print("Ocorreu um erro:", e)
        sleep(2)


def visualizar_carro_locadora(arquivo):
    try:
        with open(arquivo, "r") as f:
            carros = json.load(f)

        placa = input("Digite a placa do carro que deseja visualizar: ")
        carro_encontrado = False
        tabela = []

        for nome_carro, info in carros.items():
            if info["Placa"] == placa:
                carro_encontrado = True
                tabela.append(("Nome do Carro", nome_carro))
                for chave, valor in info.items():
                    tabela.append((chave, valor))
                break

        if carro_encontrado:
            print(tabulate(tabela, headers=[
                  "Campo", "Informação"], tablefmt="rounded_grid"))
            input("Pressione Enter para continuar.")
        if not carro_encontrado:
            print("\n=====================")
            print("Carro não encontrado.\n")
            print("=====================")
            sleep(2)
    except FileNotFoundError:
        clear_screen()
        print("======================")
        print("Arquivo não encontrado")
        print("======================")
        input("Pressione Enter para continuar.")
    except Exception as e:
        clear_screen()
        print("======================================================")
        print("Ocorreu um erro:", e)
        print("======================================================")
        input("Pressione Enter para continuar.")


def atualizar_carro(arquivo):
    try:
        with open(arquivo, "r+") as f:
            carros = json.load(f)
            placa = input("Digite a Placa do Carro que deseja atualizar: ")
            carro_encontrado = False

            for info in carros.values():
                if info["Placa"] == placa:
                    carro_encontrado = True
                    chaves_editaveis = list(info.keys())
                    chaves_mapeadas = {idx + 1: chave for idx,
                                       chave in enumerate(chaves_editaveis)}

                    tabela = [(idx, chave, info[chave])
                              for idx, chave in chaves_mapeadas.items()]

                    print(tabulate(tabela, headers=[
                          "Número", "Campo", "Informação"], tablefmt="rounded_grid"))

                    chave_num_str = input(
                        "Digite o número da chave que deseja atualizar ou pressione enter para voltar: ")
                    if chave_num_str == "":
                        clear_screen()
                        print("\n============")
                        print("Voltando...")
                        print("============")
                        sleep(2)
                        return

                    try:
                        chave_num = int(chave_num_str)
                        if chave_num not in chaves_mapeadas:
                            raise ValueError("Número inválido.")
                    except ValueError:
                        clear_screen()
                        print("\n================")
                        print("Número inválido.")
                        print("================")
                        sleep(2)
                        return

                    chave = chaves_mapeadas[chave_num]
                    valor = input(f"Digite a nova informação para {chave}: ")
                    info[chave] = valor

                    f.seek(0)
                    f.truncate()
                    json.dump(carros, f, indent=4)
                    clear_screen()
                    print("\n=============================")
                    print("Carro atualizado com sucesso!")
                    print("=============================")
                    sleep(2)
                    return

            if not carro_encontrado:
                clear_screen()
                print("=====================")
                print("Carro não encontrado.")
                print("=====================")
                sleep(2)
    except FileNotFoundError:
        clear_screen()
        print("\n======================")
        print("Arquivo não encontrado")
        print("======================")
        sleep(2)
    except json.JSONDecodeError:
        clear_screen()
        print("\n==================================")
        print("Erro ao ler o arquivo de carros.")
        print("==================================")
        sleep(2)
    except Exception as e:
        clear_screen()
        print("\n=============================================")
        print(f"Ocorreu um erro: {e}")
        print("=============================================")
        sleep(2)


def deletar_carro(arquivo):
    try:
        with open(arquivo, "r+") as f:
            carros = json.load(f)
            placa = input("Digite a Placa do carro que deseja deletar: ")
            carro_encontrado = False

            for info_carro, info in list(carros.items()):
                if info["Placa"] == placa:
                    carro_encontrado = True

                    chaves_mapeadas = {idx + 1: chave for idx,
                                       chave in enumerate(info.keys())}
                    tabela = [(idx, chave, info[chave])
                              for idx, chave in chaves_mapeadas.items()]

                    print(tabulate(tabela, headers=[
                          "Número", "Campo", "Informação"], tablefmt="grid"))

                    conf = input(
                        "Você realmente deseja deletar este carro? (S ou N) -> ")
                    if conf.lower() == "s":
                        del carros[info_carro]
                        clear_screen()
                        print("===========================")
                        print("Carro deletado com sucesso!")
                        print("===========================")
                        input("Pressione Enter para continuar.")
                    else:
                        clear_screen()
                        print("============================")
                        print("Exclusão do carro cancelada!")
                        print("============================")
                        input("Pressione Enter para continuar.")

                    f.seek(0)
                    f.truncate()
                    json.dump(carros, f, indent=4)
                    break

            if not carro_encontrado:
                clear_screen()
                print("=====================")
                print("Carro não encontrado.")
                print("=====================")
                input("Pressione Enter para continuar.")
    except FileNotFoundError:
        clear_screen()
        print("======================")
        print("Arquivo não encontrado")
        print("======================")
        input("Pressione Enter para continuar.")
    except Exception as e:
        clear_screen()
        print("===========================================================")
        print("Ocorreu um erro:", e)
        print("===========================================================")
        input("Pressione Enter para continuar.")
