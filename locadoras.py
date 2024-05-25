# import json
# import os
# import locadoras
# from time import sleep


# def clear_screen():
#     print("\033c", end="")


# def menu3():
#     arquivo_json = "locadoras.json"
#     while True:
#         clear_screen()
#         print("\n=================================")
#         print("1. Visualizar Locadora")
#         print("2. Atualizar informações da Locadora")
#         print("3. Deletar Locadora")
#         print("4. Voltar")
#         print("=================================")
#         opcao = input("Escolha uma opção: ")
#         if opcao == "1":
#             visualizar_locadora(arquivo_json)
#         elif opcao == "2":
#             atualizar_locadora(arquivo_json)
#         elif opcao == "3":
#             deletar_locadora(arquivo_json)
#         elif opcao == "4":
#             break
#         else:
#             print("Opção inválida! Tente novamente\n")
#             sleep(4)


# def login_locadora(arquivo):
#     try:
#         with open(arquivo, "r") as f:
#             locadoras = json.load(f)
#     except FileNotFoundError:
#         print("Arquivo de locadoras não encontrado.")
#         return None

#     cnpj = input("Digite o CNPJ da locadora: ")

#     for nome_locadora, dados in locadoras.items():
#         if dados["CNPJ"] == cnpj:
#             senha = input("Digite a senha da locadora: ")
#             if dados["Senha"] == senha:
#                 print("Login bem-sucedido!")
#                 return nome_locadora, dados
#     print("CNPJ ou senha incorretos.")
#     return None, None


# def cadastrar_locadora():
#     chaves = ["Nome", "CNPJ", "Email", "Telefone", "Senha"]
#     locadoras = {}
#     for chave in chaves:
#         dados_locadora = input(f"Digite seu(sua) {chave}: ")
#         locadoras[chave] = dados_locadora
#     return locadoras


# def add_locadora(locadora, arquivo):
#     try:
#         with open(arquivo, "r") as f:
#             dados = json.load(f)
#     except FileNotFoundError:
#         print("Arquivo não encontrado")
#     except Exception as e:
#         print("Ocorreu um erro: ", e)

#     numero_locadoras = len(dados)+1
#     nome_locadora = f"  Locadora {numero_locadoras}"
#     dados[nome_locadora] = locadora

#     try:
#         with open(arquivo, "w") as f:
#             json.dump(dados, f, indent=4)
#         print(f"Locadora {numero_locadoras} cadastrada com sucesso!")
#     except Exception as e:
#         print("Ocorreu um erro: ", e)


# def visualizar_locadora(arquivo):
#     try:
#         with open(arquivo, "r") as f:
#             locadora = json.load(f)
#             numero_locadoras = len(locadora)
#             nome_locadora = f"Locadora {numero_locadoras}"
#         cnpj = input(
#             "Digite o CNPJ da locadora que deseja visualizar: ")
#         locadora_encontrada = False
#         for dados, info in locadora.items():
#             if info["CNPJ"] == cnpj:
#                 senha = input("Digite a sua senha: ")
#                 if info["Senha"] == senha:
#                     locadora_encontrada = True
#                     print("\n==============================\n")
#                     print(nome_locadora)
#                     for chave, valor in info.items():
#                         print(f"{chave}:{valor}")
#                     print("\n==============================\n")
#                     break
#         if not locadora_encontrada:
#             print("Locadora não encontrada.")
#     except FileNotFoundError:
#         print("Arquivo não encontrado")
#     except Exception as e:
#         print("Ocorreu um erro:", e)


# def atualizar_locadora(arquivo):
#     try:
#         with open(arquivo, "r+") as f:
#             locadora = json.load(f)
#             numero_locadoras = len(locadora)
#             nome_locadora = f"Locadora {numero_locadoras}"
#             nome = input("Digite o nome da Locadora que dejesa atualizar: ")
#             locadora_encontrada = False
#             for dados, info in locadora.items():
#                 if info["Nome"] == nome:
#                     senha = input("Digite a sua senha: ")
#                     if info["Senha"] == senha:
#                         locadora_encontrada = True
#                         print("\n==============================\n")
#                         print(nome_locadora)
#                         for chave, valor in info.items():
#                             print(f"{chave}: {valor}")
#                         print("\n==============================\n")
#                         chave = input("Digite a chave que deseja atualizar: ")
#                         valor = input("Digite a Informação a ser atualizada: ")
#                         info[chave] = valor
#                         f.seek(0)
#                         json.dump(locadora, f, indent=4)
#                         print("Usuário atualizado com sucesso!")
#                         break
#         if not locadora_encontrada:
#             print("Locadora não encontrada ou senha incorreta.")
#     except FileNotFoundError:
#         print("Arquivo não encontrado")
#     except Exception as e:
#         print("Ocorreu um erro:", e)


# def deletar_locadora(arquivo):
#     try:
#         with open(arquivo, "r+") as f:
#             locadora = json.load(f)
#             numero_locadoras = len(locadora)
#             nome_locadora = f"Locadora {numero_locadoras}"
#             nome = input(
#                 "Digite o nome da locadora que deseja deletar: ")
#             locadora_encontrada = False
#             for dados, info in list(locadora.items()):
#                 if info["Nome"] == nome:
#                     senha = input("Digite a sua senha: ")
#                     if info["Senha"] == senha:
#                         locadora_encontrada = True
#                         print("\n==============================\n")
#                         print(nome_locadora)
#                         for chave, valor in info.items():
#                             print(f"{chave}: {valor}")
#                         print("\n==============================\n")
#                         conf = input(
#                             "Você realmente deseja deletar seu perfil? (S ou N) -> ")
#                         if conf.lower() == "s":
#                             del locadora[dados]
#                             print("Locadora deletada com sucesso!")
#                         else:
#                             print("Exclusão da locadora cancelada!")
#                             break
#                     f.seek(0)
#                     json.dump(locadora, f, indent=4)
#                     break
#         if not locadora_encontrada:
#             print("Locadora não encontrada ou senha incorreta. ")
#         else:
#             with open(arquivo, "w") as f:
#                 json.dump(locadora, f, indent=4)
#     except FileNotFoundError:
#         print("Arquivo não encontrado")
#     except Exception as e:
#         print("Ocorreu um erro:", e)

import json
from validação import validar_nome, validar_cnpj, validar_telefone, validar_email, validar_senha
from util import clear_screen
from carros import menu_locadora


def cadastrar_locadora():
    chaves = ["Nome", "CNPJ", "Telefone", "Email", "Senha"]
    validadores = {
        "Nome": validar_nome,
        "CNPJ": validar_cnpj,
        "Telefone": validar_telefone,
        "Email": validar_email,
        "Senha": validar_senha
    }

    locadora = {}
    for chave in chaves:
        while True:
            dados_locadora = input(f"Digite o(a) {chave} da locadora: ")
            valido, mensagem = validadores[chave](dados_locadora)
            if valido:
                locadora[chave] = dados_locadora
                break
            else:
                print(f"Entrada inválida para {chave}: {mensagem}")
    return locadora


def add_locadora(locadora, arquivo):
    try:
        with open(arquivo, "r") as f:
            dados = json.load(f)
    except FileNotFoundError:
        dados = {}

    numero_locadoras = len(dados) + 1
    nome_locadora = f"Locadora {numero_locadoras}"
    dados[nome_locadora] = locadora

    try:
        with open(arquivo, "w") as f:
            json.dump(dados, f, indent=4)
        print(f"Locadora {numero_locadoras} cadastrada com sucesso!")
    except Exception as e:
        print("Ocorreu um erro: ", e)


def login_locadora(arquivo):
    try:
        with open(arquivo, "r") as f:
            locadoras = json.load(f)
    except FileNotFoundError:
        print("Arquivo de locadoras não encontrado.")
        return None

    cnpj = input("Digite o CNPJ da locadora: ")

    for nome_locadora, dados in locadoras.items():
        if dados["CNPJ"] == cnpj:
            senha = input("Digite a senha da locadora: ")
            if dados["Senha"] == senha:
                print("Login bem-sucedido!")
                return nome_locadora, dados
    print("CNPJ ou senha incorretos.")
    return None, None


def menu3(locadora_logada, dados_locadora):
    arquivo_json = "locadoras.json"
    while True:
        clear_screen()
        print("\n=================================")
        print(f"Bem-vindo(a), {dados_locadora['Nome']}!")
        print("1. Visualizar locadora")
        print("2. Atualizar informações da locadora")
        print("3. Carros")
        print("4. Deletar locadora")
        print("5. Voltar")
        print("=================================")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            visualizar_locadora(dados_locadora)
        elif opcao == "2":
            atualizar_locadora(arquivo_json, locadora_logada, dados_locadora)
        elif opcao == "3":
            menu_locadora()
        elif opcao == "4":
            if deletar_locadora(arquivo_json, locadora_logada, dados_locadora):
                return
        elif opcao == "5":
            break
        else:
            print("Opção inválida! Tente novamente\n")


def visualizar_locadora(dados_locadora):
    print("\n==============================\n")
    for chave, valor in dados_locadora.items():
        print(f"{chave}: {valor}")
    print("\n==============================\n")
    input("Digite 1 para voltar-->")


def atualizar_locadora(arquivo, locadora_logada, dados_locadora):
    try:
        with open(arquivo, "r+") as f:
            locadoras = json.load(f)

            locadora_atual = locadoras[locadora_logada]
            print("\n==============================\n")
            for idx, (chave, valor) in enumerate(locadora_atual.items(), 1):
                print(f"{idx}. {chave}: {valor}")
            print("\n==============================\n")

            chave_num = int(
                input("Digite o número da chave que deseja atualizar: "))
            if chave_num < 1 or chave_num > len(locadora_atual):
                print("Número inválido.")
                return

            chave = list(locadora_atual.keys())[chave_num - 1]
            valor = input(f"Digite a nova informação para {chave}: ")

            locadora_atual[chave] = valor

            f.seek(0)
            f.truncate()
            json.dump(locadoras, f, indent=4)
            print("Informação atualizada com sucesso.")
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON.")
    except Exception as e:
        print("Ocorreu um erro:", e)


def deletar_locadora(arquivo, locadora_logada, dados_locadora):
    try:
        with open(arquivo, "r+") as f:
            locadoras = json.load(f)

            print("\n==============================\n")
            for chave, valor in dados_locadora.items():
                print(f"{chave}: {valor}")
            print("\n==============================\n")

            conf = input(
                "Você realmente deseja deletar o perfil da locadora? (S ou N) -> ")
            if conf.lower() == "s":
                del locadoras[locadora_logada]
                print("Locadora deletada com sucesso!")
                f.seek(0)
                f.truncate()
                json.dump(locadoras, f, indent=4)
                return True
            else:
                print("Deletação da locadora cancelada!")
                return False
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print("Ocorreu um erro:", e)
    return False
