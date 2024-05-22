import json
import os
import validação
from time import sleep


import json
from time import sleep


def clear_screen():
    print("\033c", end="")


def menu_locadora():
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
            carro = cadastrar_carro()
            add_carro(carro, arquivo_json)
        elif opcao == "2":
            visualizar_carro(arquivo_json)
        elif opcao == "3":
            atualizar_carro(arquivo_json)
        elif opcao == "4":
            deletar_carro(arquivo_json)
        elif opcao == "5":
            break
        else:
            print("\n====================================")
            print("Opção inválida! Tente novamente\n")
            print("====================================")
            sleep(2)


def contem_numero(s):
    return any(char.isdigit() for char in s)


def contem_letra(s):
    return any(char.isalpha() for char in s)


def cadastrar_carro():

    campos = ["Modelo", "Marca", "ID Chassis", "Numero de portas", "Ano", "Categoria",
              "Placa", "Capacidade mala", "Capacidade combustivel", "Capacidade passageiro",
              "Quilometragem", "Cambio", "Cor", "Tipo combustivel"]

    carro = {}
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
            continue
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


def visualizar_carro(arquivo):
    try:
        with open(arquivo, "r") as f:
            carros = json.load(f)
            modelo = input("Digite o modelo do carro que deseja visualizar: ")
            carro_encontrado = False
            for nome_carro, info in carros.items():
                if info == modelo:
                    carro_encontrado = True
                    print("\n==============================\n")
                    print(nome_carro)
                    for chave, valor in info.items():
                        print(f"{chave}: {valor}")
                    print("\n==============================\n")
                    break
            if not carro_encontrado:
                print("\n=====================")
                print("Carro não encontrado.\n")
                print("=====================")
                sleep(2)
    except FileNotFoundError:
        print("Arquivo não encontrado")
    except Exception as e:
        print("Ocorreu um erro:", e)


def atualizar_carro(arquivo):
    try:
        with open(arquivo, "r+") as f:
            carros = json.load(f)
            nome = input("Digite o nome do Carro que deseja atualizar: ")
            carro_encontrado = False
            for nome_carro, info in carros.items():
                if nome_carro == nome:
                    carro_encontrado = True
                    print("\n==============================\n")
                    print(nome_carro)
                    for chave, valor in info.items():
                        print(f"{chave}: {valor}")
                    print("\n==============================\n")
                    chave = input("Digite a chave que deseja atualizar: ")
                    valor = input("Digite a Informação a ser atualizada: ")
                    info[chave] = valor
                    f.seek(0)
                    json.dump(carros, f, indent=4)
                    print("Carro atualizado com sucesso!")
                    break
            if not carro_encontrado:
                print("Carro não encontrado.")
    except FileNotFoundError:
        print("Arquivo não encontrado")
    except Exception as e:
        print("Ocorreu um erro:", e)


def deletar_carro(arquivo):
    try:
        with open(arquivo, "r+") as f:
            carros = json.load(f)
            nome = input("Digite o nome do carro que deseja deletar: ")
            carro_encontrado = False
            for nome_carro, info in list(carros.items()):
                if nome_carro == nome:
                    carro_encontrado = True
                    print("\n==============================\n")
                    print(nome_carro)
                    for chave, valor in info.items():
                        print(f"{chave}: {valor}")
                    print("\n==============================\n")
                    conf = input(
                        "Você realmente deseja deletar este carro? (S ou N) -> ")
                    if conf.lower() == "s":
                        del carros[nome_carro]
                        print("Carro deletado com sucesso!")
                    else:
                        print("Exclusão do carro cancelada!")
                    f.seek(0)
                    json.dump(carros, f, indent=4)
                    break
            if not carro_encontrado:
                print("Carro não encontrado.")
    except FileNotFoundError:
        print("Arquivo não encontrado")
    except Exception as e:
        print("Ocorreu um erro:", e)
