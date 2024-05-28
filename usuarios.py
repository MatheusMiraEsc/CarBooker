import json
import os
from time import sleep
from datetime import datetime
from validação import validar_nome, validar_sobrenome, validar_data_nascimento, validar_cpf, validar_cnh, validar_genero, validar_telefone, validar_email, validar_senha
from util import clear_screen
from carros import visualizar_carro_usuario
from reserva import fazerReserva, checar_reserva, alterar_reserva, cancelar_reserva, menu_usuario_reserva
from endereço import cadastro_endereço_usuario


def menu2(usuario_logado, dados_usuario):
    arquivo_usuario = "usuarios.json"
    arquivo_carros = "carros.json"
    arquivo_reservas = "reservas.json"
    while True:
        clear_screen()
        print("\n=================================")
        print(f"Bem-vindo(a), {dados_usuario['Nome']}!")
        print("1. Visualizar usuário")
        print("2. Atualizar informações do usuário")
        print("3. Carros")
        print("4. Deletar usuário")
        print("5. Voltar")
        print("=================================")
        opcao1 = input("Escolha uma opção: ")
        if opcao1 == "1":
            visualizar_usuario(usuario_logado, arquivo_usuario)
        elif opcao1 == "2":
            atualizar_usuario(arquivo_usuario, usuario_logado, dados_usuario)
        elif opcao1 == "3":
            menu_usuario_reserva(usuario_logado, dados_usuario)
        elif opcao1 == "4":
            usuario_deletado = deletar_usuario(
                arquivo_usuario, usuario_logado, dados_usuario)
            if usuario_deletado:
                break
        elif opcao1 == "5":
            break
        else:
            print("Opção inválida! Tente novamente\n")
            sleep(2)


def login(arquivo):
    try:
        with open(arquivo, "r") as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        print("Arquivo de usuários não encontrado.")
        return None, None
    while True:
        email = input("Digite seu Email ou aperte enter para voltar: ")
        if email == "":
            return None, None
        email_encontrado = False
        for chaves_usuario, dados in usuarios.items():
            if dados["Email"] == email:
                email_encontrado = True
                senha = input("Digite a sua senha: ")
                if dados["Senha"] == senha:
                    print("Login bem-sucedido!")
                    sleep(2)
                    return chaves_usuario, dados
                else:
                    print("Senha incorreta.")
                    break
        if not email_encontrado:
            print("CPF incorreto ou não cadastrado.")
    return None, None


def cadastrar_usuario(arquivo, arquivo_end):
    chaves = ["Nome", "Sobrenome", "Data de nascimento",
              "CPF", "CNH", "Genero", "Telefone", "Email", "Senha"]
    validadores = {
        "Nome": validar_nome,
        "Sobrenome": validar_sobrenome,
        "Data de nascimento": validar_data_nascimento,
        "CPF": lambda cpf: validar_cpf(cpf, arquivo),
        "CNH": validar_cnh,
        "Genero": validar_genero,
        "Telefone": validar_telefone,
        "Email": lambda email: validar_email(email, arquivo),
        "Senha": validar_senha
    }

    usuarios = {}
    verificar_endereço = False
    for chave in chaves:
        while True:
            if chave == "Senha" and verificar_endereço == False:
                user = usuarios["CPF"]
                cadastro_endereço_usuario(arquivo_end, user)
                verificar_endereço = True
            dados_usuario = input(f"Digite seu(sua) {chave}: ")
            valido, mensagem = validadores[chave](dados_usuario)
            if valido:
                usuarios[chave] = dados_usuario
                break
            else:
                print(f"Entrada inválida para {chave}: {mensagem}")
    return usuarios


def add_usuario(usuario, arquivo):
    try:
        with open(arquivo) as f:
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


def visualizar_usuario(usuario_logado, arquivo):
    with open(arquivo) as f:
        usuario = json.load(f)
    for user, valores in usuario.items():
        if user == usuario_logado:
            print("\n==============================\n")
            for chaves, info in valores.items():
                print(f"{chaves}: {info}")
            print("\n==============================\n")
    input("Pressione Enter para continuar.")


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
