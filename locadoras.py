import json
from validação import validar_nome, validar_cnpj, validar_telefone, validar_email, validar_senha
from util import clear_screen, cadastro_endereço
from carros import menu_locadora
from time import sleep
from reserva import menu_locadora_reserva
from tabulate import tabulate


def cadastrar_locadora(arquivo):
    chaves = ["Nome", "CNPJ", "Telefone", "Email", "Senha"]
    validadores = {
        "Nome": validar_nome,
        "CNPJ": lambda cnpj: validar_cnpj(cnpj),
        "Telefone": validar_telefone,
        "Email": lambda email: validar_email(email, arquivo),
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
                print("\n==========================================")
                print(f"Entrada inválida para {chave}: {mensagem}")
                print("==========================================")

    enderecos = []
    while True:
        enderecos.append(cadastro_endereço())
        opcao = input("Você deseja cadastrar mais um endereço? S ou N: ")
        if opcao.lower() == "s":
            continue
        else:
            break

    locadora["Enderecos"] = enderecos
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
        clear_screen()
        print("\n=========================================================")
        print(f"Locadora {numero_locadoras} cadastrada com sucesso!")
        print("=========================================================")
    except Exception as e:
        clear_screen()
        print("\n==============================================")
        print("Ocorreu um erro: ", e)
        print("==============================================")


def login_locadora(arquivo):
    try:
        with open(arquivo, "r") as f:
            locadoras = json.load(f)
    except FileNotFoundError:
        clear_screen()
        print("Arquivo de locadoras não encontrado.")
        locadoras = {}
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
                    clear_screen()
                    print("\n===================")
                    print("Login bem-sucedido!")
                    print("===================")
                    sleep(2)
                    return nome_locadora, dados
                else:
                    print("================")
                    print("Senha incorreta.")
                    print("================")
                    break
        if not email_encontrado:
            clear_screen()
            print("==================================")
            print("Email incorreto ou não cadastrado.")
            print("==================================")
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
        print("4. Reservas")
        print("5. Deletar locadora")
        print("6. Voltar")
        print("=================================")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            visualizar_locadora(locadora_logada, arquivo_json)
        elif opcao == "2":
            atualizar_locadora(arquivo_json, locadora_logada)
            sleep(2)
        elif opcao == "3":
            menu_locadora(dados_locadora)
        elif opcao == "4":
            menu_locadora_reserva(dados_locadora)
        elif opcao == "5":
            if deletar_locadora(arquivo_json, locadora_logada):
                sleep(2)
                return
        elif opcao == "6":
            break
        else:
            clear_screen()
            print("\n================================")
            print("Opção inválida! Tente novamente")
            print("================================")


def visualizar_locadora(locadora_logada, arquivo):
    with open(arquivo) as f:
        locadora = json.load(f)

    if locadora_logada in locadora:
        print("\n==============================\n")
        dados_locadora = locadora[locadora_logada]
        tabela = []

        for chave, valor in dados_locadora.items():
            if chave == "Enderecos":
                for i, endereco in enumerate(valor, 1):
                    tabela.append((f"Endereço {i}", ""))
                    for end_chave, end_valor in endereco.items():
                        tabela.append((f"  {end_chave}", end_valor))
            else:
                tabela.append((chave, valor))

        print(tabulate(tabela, headers=[
              "Campo", "Informação"], tablefmt="rounded_grid"))
        print("\n==============================\n")

    input("Pressione Enter para continuar.")


def atualizar_locadora(arquivo, locadora_logada):
    try:
        with open(arquivo, "r+") as f:
            locadoras = json.load(f)

            if locadora_logada not in locadoras:
                clear_screen()
                print("========================================================")
                print("Locadora não encontrada.")
                print("========================================================")
                return

            locadora_atual = locadoras[locadora_logada]
            tabela = []
            idx = 1
            chave_map = {}

            for chave, valor in locadora_atual.items():
                if chave == "Enderecos":
                    for i, endereco in enumerate(valor, 1):
                        tabela.append((idx, f"Endereço {i}", ""))
                        chave_map[idx] = (
                            locadora_atual["Enderecos"], i-1, None)
                        idx += 1
                        for end_chave, end_valor in endereco.items():
                            tabela.append((idx, f"  {end_chave}", end_valor))
                            chave_map[idx] = (
                                locadora_atual["Enderecos"][i-1], end_chave)
                            idx += 1
                else:
                    tabela.append((idx, chave, valor))
                    chave_map[idx] = (locadora_atual, chave)
                    idx += 1

            print("\n==============================\n")
            print(tabulate(tabela, headers=[
                  "#", "Campo", "Informação"], tablefmt="rounded_grid"))
            print("\n==============================\n")

            chave_num = int(
                input("Digite o número da chave que deseja atualizar: "))
            if chave_num not in chave_map:
                clear_screen()
                print("\n================")
                print("Número inválido.")
                print("================")
                return

            obj, chave = chave_map[chave_num]
            if chave is None:
                print("\n================")
                print("Você selecionou um título, não pode ser atualizado.")
                print("================")
                return

            valor = input(f"Digite a nova informação para {chave}: ")

            # Função para fazer validação de input aqui (se necessário)
            obj[chave] = valor

            f.seek(0)
            f.truncate()
            json.dump(locadoras, f, indent=4)
            clear_screen()
            print("==================================")
            print("Informação atualizada com sucesso.")
            print("==================================")

    except FileNotFoundError:
        clear_screen()
        print("A======================")
        print("Arquivo não encontrado.")
        print("=======================")
    except json.JSONDecodeError:
        clear_screen()
        print("===================================")
        print("Erro ao decodificar o arquivo JSON.")
        print("===================================")
    except ValueError:
        clear_screen()
        print("============================================")
        print("Entrada inválida.")
        print("============================================")
    except Exception as e:
        clear_screen()
        print("========================================================")
        print("Ocorreu um erro:", e)
        print("========================================================")


def deletar_locadora(arquivo, locadora_logada):
    try:
        with open(arquivo, "r+") as f:
            locadoras = json.load(f)

            if locadora_logada not in locadoras:
                clear_screen()
                print("========================================================")
                print("Locadora não encontrada.")
                print("========================================================")
                return

            locadora_atual = locadoras[locadora_logada]
            tabela = []
            idx = 1
            chave_map = {}

            for chave, valor in locadora_atual.items():
                if chave == "Enderecos":
                    for i, endereco in enumerate(valor, 1):
                        tabela.append((idx, f"Endereço {i}", ""))
                        chave_map[idx] = (
                            locadora_atual["Enderecos"], i-1, None)
                        idx += 1
                        for end_chave, end_valor in endereco.items():
                            tabela.append((idx, f"  {end_chave}", end_valor))
                            chave_map[idx] = (
                                locadora_atual["Enderecos"][i-1], end_chave)
                            idx += 1
                else:
                    tabela.append((idx, chave, valor))
                    chave_map[idx] = (locadora_atual, chave)
                    idx += 1

            print("\n==============================\n")
            print(tabulate(tabela, headers=[
                  "#", "Campo", "Informação"], tablefmt="rounded_grid"))
            print("\n==============================\n")

            conf = input(
                "Você realmente deseja deletar o perfil da locadora? (S ou N) -> ")
            if conf.lower() == "s":
                del locadoras[locadora_logada]
                clear_screen()
                print("==============================")
                print("Locadora deletada com sucesso!")
                print("==============================")
                f.seek(0)
                f.truncate()
                json.dump(locadoras, f, indent=4)
                return True
            else:
                clear_screen()
                print("================================")
                print("Deletação da locadora cancelada!")
                print("================================")
                return False
    except FileNotFoundError:
        clear_screen()
        print("=======================")
        print("Arquivo não encontrado.")
        print("=======================")
    except Exception as e:
        clear_screen()
        print("=======================================================")
        print("Ocorreu um erro:", e)
        print("=======================================================")
    return False
