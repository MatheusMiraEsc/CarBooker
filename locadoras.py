
import json
from validação import validar_nome, validar_cnpj, validar_telefone, validar_email, validar_senha
from util import clear_screen
from carros import menu_locadora
from time import sleep
from endereço import cadastro_endereço_locadora


def cadastrar_locadora(arquivo, arquivoEnd):
    chaves = ["Nome", "CNPJ", "Telefone", "Email", "Senha"]
    validadores = {
        "Nome": validar_nome,
        "CNPJ": lambda cnpj: validar_cnpj(cnpj, arquivo),
        "Telefone": validar_telefone,
        "Email": lambda email: validar_email(email, arquivo),
        "Senha": validar_senha
    }

    locadora = {}
    for chave in chaves:
        while True:
            if chave == "Senha":
                user = locadora["CNPJ"]
                cadastro_endereço_locadora(arquivoEnd, user)
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
    while True:
        email = input(
            "Digite o Email da locadora ou aperte enter para voltar: ")
        if email == "":
            return None, None
        email_encontrado = False
        for nome_locadora, dados in locadoras.items():
            if dados["Email"] == email:
                email_encontrado = True
                senha = input("Digite a senha da locadora: ")
                if dados["Senha"] == senha:
                    print("Login bem-sucedido!")
                    sleep(2)
                    return nome_locadora, dados
                else:
                    print("Senha incorreta.")
                    break
        if not email_encontrado:
            print("CNPJ incorreto ou não cadastrado.")
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
            visualizar_locadora(locadora_logada, arquivo_json)
        elif opcao == "2":
            atualizar_locadora(arquivo_json, locadora_logada, dados_locadora)
        elif opcao == "3":
            menu_locadora(dados_locadora)
        elif opcao == "4":
            if deletar_locadora(arquivo_json, locadora_logada, dados_locadora):
                return
        elif opcao == "5":
            break
        else:
            print("Opção inválida! Tente novamente\n")


def visualizar_locadora(locadora_logada, arquivo):
    with open(arquivo) as f:
        locadora = json.load(f)
    for user, valores in locadora.items():
        if user == locadora_logada:
            print("\n==============================\n")
            for chaves, info in valores.items():
                print(f"{chaves}: {info}")
            print("\n==============================\n")
    input("Pressione Enter para continuar.")


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
