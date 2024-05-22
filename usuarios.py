import json
import os
from time import sleep
from datetime import datetime
from validação import validar_nome, validar_sobrenome, validar_data_nascimento, validar_cpf, validar_cnh, validar_genero, validar_telefone, validar_email, validar_senha


import json


def clear_screen():
    print("\033c", end="")


'''def menu2():
    arquivo_json = "usuarios.json"
    while True:
        clear_screen()
        print("\n=================================")
        print("1. Visualizar usuário")
        print("2. Atualizar informações do usuário")
        print("3. Deletar usuário")
        print("4. Voltar")
        print("=================================")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            visualizar_usuario(arquivo_json)
        elif opcao == "2":
            atualizar_usuario(arquivo_json)
        elif opcao == "3":
            deletar_usuario(arquivo_json)
        elif opcao == "4":
            break
        else:
            print("Opção inválida! Tente novamente\n")'''


def menu2(usuario_logado, dados_usuario):
    arquivo_json = "usuarios.json"
    while True:
        clear_screen()
        print("\n=================================")
        print(f"Bem-vindo(a), {dados_usuario['Nome']}!")
        print("1. Visualizar usuário")
        print("2. Atualizar informações do usuário")
        print("3. Deletar usuário")
        print("4. Voltar")
        print("=================================")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            visualizar_usuario(dados_usuario)
        elif opcao == "2":
            atualizar_usuario(arquivo_json, usuario_logado, dados_usuario)
        elif opcao == "3":
            deletar_usuario(arquivo_json, usuario_logado, dados_usuario)
            break
        elif opcao == "4":
            break
        else:
            print("Opção inválida! Tente novamente\n")
            sleep(2)


# def login_usuario(arquivo):
#     try:
#         with open(arquivo, "r") as f:
#             usuarios = json.load(f)
#     except FileNotFoundError:
#         print("Arquivo de usuários não encontrado.")
#         return None

#     cpf = input("Digite seu CPF: ")

#     for nome_usuario, dados in usuarios.items():
#         if dados["CPF"] == cpf:
#             senha = input("Digite sua senha: ")
#             if dados["Senha"] == senha:
#                 print("Login bem-sucedido!")
#                 return nome_usuario, dados
#             print("Senha incorreta, tente novamente")
#     print("CPF incorreto ou usuário não cadastrado.")
#     sleep(2)
#     return None, None

def login(arquivo):
    try:
        with open(arquivo, "r") as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        print("Arquivo de usuários não encontrado.")
        return None

    cpf = input("Digite seu CPF: ")
    for nome_usuario, dados in usuarios.items():
        if dados["CPF"] == cpf:
            senha = input("Digite a sua senha: ")
            if dados["Senha"] == senha:
                print("Login bem-sucedido!")
            return nome_usuario, dados
    print("CPF ou senha incorretos.")
    return None, None

# def cadastrar_usuario():
#     chaves = ["Nome", "Sobrenome", "Data de nascimento",
#               "CPF", "CNH", "Genero", "Telefone", "Email", "Senha"]
#     validadores = {
#         "Nome": validar_nome,
#         "Sobrenome": validar_sobrenome,
#         "Data de nascimento": validar_data_nascimento,
#         "CPF": validar_cpf,
#         "CNH": validar_cnh,
#         "Genero": validar_genero,
#         "Telefone": validar_telefone,
#         "Email": validar_email,
#         "Senha": validar_senha
#     }

#     usuarios = {}
#     for chave in chaves:
#         while True:
#             dados_usuario = input(f"Digite seu(sua) {chave}: ")
#             valido, mensagem = validadores[chave](dados_usuario)
#             if valido:
#                 usuarios[chave] = dados_usuario
#                 break
#             else:
#                 print(f"Entrada inválida para {chave}: {mensagem}")
#     return usuarios


def cadastrar_usuario():
    chaves = ["Nome", "Sobrenome", "Data de nascimento",
              "CPF", "CNH", "Genero", "Telefone", "Email", "Senha"]
    validadores = {
        "Nome": validar_nome,
        "Sobrenome": validar_sobrenome,
        "Data de nascimento": validar_data_nascimento,
        "CPF": validar_cpf,
        "CNH": validar_cnh,
        "Genero": validar_genero,
        "Telefone": validar_telefone,
        "Email": validar_email,
        "Senha": validar_senha
    }

    usuarios = {}
    for chave in chaves:
        while True:
            dados_usuario = input(f"Digite seu(sua) {chave}: ")
            valido, mensagem = validadores[chave](dados_usuario)
            if valido:
                usuarios[chave] = dados_usuario
                break
            else:
                print(f"Entrada inválida para {chave}: {mensagem}")
    return usuarios


# def add_usuario(usuario, arquivo):
#     try:
#         with open(arquivo, "r") as f:
#             dados = json.load(f)
#     except FileNotFoundError:
#         dados = {}

#     numero_usuarios = len(dados) + 1
#     nome_usuario = f"Usuario {numero_usuarios}"
#     dados[nome_usuario] = usuario

#     try:
#         with open(arquivo, "w") as f:
#             json.dump(dados, f, indent=4)
#         print(f"Usuário {numero_usuarios} cadastrado com sucesso!")
#     except Exception as e:
#         print("Ocorreu um erro: ", e)


def add_usuario(usuario, arquivo):
    try:
        with open(arquivo, "r") as f:
            dados = json.load(f)
    except FileNotFoundError:
        dados = {}

    numero_usuarios = len(dados) + 1
    nome_usuario = f"Usuario {numero_usuarios}"
    dados[nome_usuario] = usuario

    try:
        with open(arquivo, "w") as f:
            json.dump(dados, f, indent=4)
        print(f"Usuário {numero_usuarios} cadastrado com sucesso!")
    except Exception as e:
        print("Ocorreu um erro: ", e)


# def visualizar_usuario(arquivo):
#     try:
#         with open(arquivo, "r") as f:
#             usuario = json.load(f)
#         cpf = input("Digite o CPF do usuário que deseja visualizar: ")
#         usuario_encontrado = False
#         for dados, info in usuario.items():
#             if info["CPF"] == cpf:
#                 senha = input("Digite a sua senha: ")
#                 if info["Senha"] == senha:
#                     usuario_encontrado = True
#                     print("\n==============================\n")
#                     print(dados)
#                     for chave, valor in info.items():
#                         print(f"{chave}: {valor}")
#                     print("\n==============================\n")
#                     opcao = input("Digite 1 para voltar-->")
#                     if opcao == "1":
#                         break
#                     else:
#                         break
#         if not usuario_encontrado:
#             print("Usuário não encontrado ou senha incorreta.")
#     except FileNotFoundError:
#         print("Arquivo não encontrado")
#     except Exception as e:
#         print("Ocorreu um erro:", e)

def visualizar_usuario(dados_usuario):
    with open("usuarios.json", "r") as f:
        dados_usuario = json.load(f)
    print("\n==============================\n")
    for dados, info in dados_usuario.items():
        for chave, valor in info.items():
            print(f"{chave}: {valor}")
        print("\n==============================\n")
        opcao = input("Digite 1 para voltar-->")
        if opcao == "1":
            break
        break

# def atualizar_usuario(arquivo):
#     try:
#         with open(arquivo, "r+") as f:
#             usuarios = json.load(f)
#             cpf = input("Digite o CPF do usuário que deseja atualizar: ")
#             valido, mensagem = validar_cpf(cpf)
#             if not valido:
#                 print(mensagem)
#                 return

#             usuario_encontrado = False

#             for nome_usuario, usuario_atual in usuarios.items():
#                 if usuario_atual["CPF"] == cpf:
#                     senha = input("Digite a sua senha: ")
#                     if usuario_atual["Senha"] == senha:
#                         usuario_encontrado = True
#                         print("\n==============================\n")
#                         print(nome_usuario)
#                         for idx, (chave, valor) in enumerate(usuario_atual.items(), 1):
#                             print(f"{idx}. {chave}: {valor}")
#                         print("\n==============================\n")

#                         chave_num = int(
#                             input("Digite o número da chave que deseja atualizar: "))
#                         if chave_num < 1 or chave_num > len(usuario_atual):
#                             print("Número inválido.")
#                             return

#                         chave = list(usuario_atual.keys())[chave_num - 1]
#                         valor = input(
#                             f"Digite a nova informação para {chave}: ")

#                         usuario_atual[chave] = valor

#                         f.seek(0)
#                         f.truncate()
#                         json.dump(usuarios, f, indent=4)
#                         print("Informação atualizada com sucesso.")
#                         break

#             if not usuario_encontrado:
#                 print("Usuário não encontrado ou senha incorreta.")
#     except FileNotFoundError:
#         print("Arquivo não encontrado.")
#     except json.JSONDecodeError:
#         print("Erro ao decodificar o arquivo JSON.")
#     except Exception as e:
#         print("Ocorreu um erro:", e)


def atualizar_usuario(arquivo, usuario_logado, dados_usuario):
    try:
        with open(arquivo, "r+") as f:
            usuarios = json.load(f)

            usuario_atual = usuarios[usuario_logado]
            print("\n==============================\n")
            for idx, (chave, valor) in enumerate(usuario_atual.items(), 1):
                print(f"{idx}. {chave}: {valor}")
            print("\n==============================\n")

            chave_num = int(
                input("Digite o número da chave que deseja atualizar: "))
            if chave_num < 1 or chave_num > len(usuario_atual):
                print("Número inválido.")
                return

            chave = list(usuario_atual.keys())[chave_num - 1]
            valor = input(f"Digite a nova informação para {chave}: ")

            usuario_atual[chave] = valor

            f.seek(0)
            f.truncate()
            json.dump(usuarios, f, indent=4)
            print("Informação atualizada com sucesso.")
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON.")
    except Exception as e:
        print("Ocorreu um erro:", e)


# def deletar_usuario(arquivo):
#     try:
#         with open(arquivo, "r+") as f:
#             usuarios = json.load(f)
#             cpf = input("Digite o CPF do usuário que deseja deletar: ")
#             usuario_encontrado = False
#             for dados, info in list(usuarios.items()):
#                 if info["CPF"] == cpf:
#                     senha = input("Digite a sua senha: ")
#                     if info["Senha"] == senha:
#                         usuario_encontrado = True
#                         print("\n==============================\n")
#                         print(dados)
#                         for chave, valor in info.items():
#                             print(f"{chave}: {valor}")
#                         print("\n==============================\n")
#                         conf = input(
#                             "Você realmente deseja deletar seu perfil? (S ou N) -> ")
#                         if conf.lower() == "s":
#                             del usuarios[dados]
#                             print("Usuário deletado com sucesso!")
#                         else:
#                             print("Deletação do usuário cancelada!")
#                             break
#                     f.seek(0)
#                     json.dump(usuarios, f, indent=4)
#                     break
#         if not usuario_encontrado:
#             print("Usuário não encontrado.")
#         else:
#             with open(arquivo, "w") as f:
#                 json.dump(usuarios, f, indent=4)
#     except FileNotFoundError:
#         print("Arquivo não encontrado")
#     except Exception as e:
#         print("Ocorreu um erro:", e)

def deletar_usuario(arquivo, usuario_logado, dados_usuario):
    try:
        with open(arquivo, "r+") as f:
            usuarios = json.load(f)

            print("\n==============================\n")
            for chave, valor in dados_usuario.items():
                print(f"{chave}: {valor}")
            print("\n==============================\n")

            conf = input(
                "Você realmente deseja deletar seu perfil? (S ou N) -> ")
            if conf.lower() == "s":
                del usuarios[usuario_logado]
                print("Usuário deletado com sucesso!")
                f.seek(0)
                f.truncate()
                json.dump(usuarios, f, indent=4)
                return True
            else:
                print("Deletação do usuário cancelada!")
                return False
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print("Ocorreu um erro:", e)
    return False
