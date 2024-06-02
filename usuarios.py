import json
from time import sleep
from validação import validar_nome, validar_sobrenome, validar_data_nascimento, validar_cpf, validar_cnh, validar_telefone, validar_email, validar_senha
from util import clear_screen, cadastro_endereço, print_vermelho, print_verde
from reserva import menu_usuario_reserva
from tabulate import tabulate


def menu2(usuario_logado, dados_usuario):
    arquivo_usuario = "usuarios.json"
    while True:
        clear_screen()
        print("\n=================================")
        print(f"Bem-vindo(a), {dados_usuario['Nome']}!")
        print("=================================")
        print("1. Visualizar usuário")
        print("2. Atualizar informações do usuário")
        print("3. Carros e reserva")
        print("4. Deletar usuário")
        print("5. Voltar")
        print("=================================")
        opcao1 = input("Escolha uma opção: ")
        if opcao1 == "1":
            visualizar_usuario(
                usuario_logado, arquivo_usuario)
        elif opcao1 == "2":
            atualizar_usuario(
                arquivo_usuario, usuario_logado)
            sleep(2)
        elif opcao1 == "3":
            menu_usuario_reserva(dados_usuario)
        elif opcao1 == "4":
            usuario_deletado = deletar_usuario(
                arquivo_usuario, usuario_logado, dados_usuario)
            if usuario_deletado:
                break
        elif opcao1 == "5":
            break
        else:
            clear_screen()
            print("================================")
            print_vermelho("Opção inválida! Tente novamente")
            print("================================")
            sleep(2)


def login(arquivo):
    try:
        with open(arquivo, "r") as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        clear_screen()
        print("===================================")
        print_vermelho("Arquivo de usuários não encontrado.")
        print("===================================")
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
                    clear_screen()
                    print("===================")
                    print_verde("Login bem-sucedido!")
                    print("===================")
                    sleep(2)
                    return chaves_usuario, dados
                else:
                    print("\n================")
                    print_vermelho("Senha incorreta.")
                    print("================\n")
                    break
        if not email_encontrado:
            clear_screen()
            print("================================")
            print_vermelho("Email incorreto ou não cadastrado.")
            print("================================")
    return None, None


def cadastrar_usuario(arquivo):
    chaves = ["Nome", "Sobrenome", "Data de nascimento",
              "CPF", "CNH", "Telefone", "Email", "Senha"]

    usuarios = {}
    for chave in chaves:
        while True:
            dados_usuario = input(f"Digite seu(sua) {chave}: ")
            validadores = {
                "Nome": validar_nome,
                "Sobrenome": validar_sobrenome,
                "Data de nascimento": validar_data_nascimento,
                "CPF": lambda cpf: validar_cpf(cpf, arquivo),
                "CNH": validar_cnh,
                "Telefone": validar_telefone,
                "Email": lambda email: validar_email(email, arquivo),
                "Senha": validar_senha
            }
            valido, mensagem = validadores[chave](dados_usuario)

            if valido:
                usuarios[chave] = dados_usuario
                break
            else:
                print("\n=========================================")
                print_vermelho(f"Entrada inválida para {chave}: {mensagem}")
                print("=========================================")
    enderecos = []
    while True:
        enderecos.append(cadastro_endereço())
        opcao = input(
            "Voçê deseja cadastrar mais um endereço? S ou N")
        if opcao.lower() == "s":
            continue
        else:
            break

    usuarios["Enderecos"] = enderecos

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
        clear_screen()
        print("============================================")
        print_verde(f"Usuário {numero_usuarios} cadastrado com sucesso!")
        print("============================================")
    except Exception as e:
        clear_screen()
        print("============================================================")
        print_vermelho("Ocorreu um erro: ", e)
        print("============================================================")


def visualizar_usuario(usuario_logado, arquivo):
    with open(arquivo) as f:
        usuarios = json.load(f)

    if usuario_logado in usuarios:
        dados_usuario = usuarios[usuario_logado]
        tabela = []

        for chave, valor in dados_usuario.items():
            if chave == "Enderecos":
                for i, endereco in enumerate(valor, 1):
                    tabela.append((f"Endereço {i}", ""))
                    for end_chave, end_valor in endereco.items():
                        tabela.append((f"  {end_chave}", end_valor))
            else:
                tabela.append((chave, valor))
        clear_screen()
        print(tabulate(tabela, headers=[
              "Campo", "Informação"], tablefmt="rounded_grid"))
        input("Pressione Enter para continuar.")


def atualizar_usuario(arquivo, usuario_logado):
    try:
        with open(arquivo, "r+") as f:
            usuarios = json.load(f)

            if usuario_logado not in usuarios:
                clear_screen()
                print("=======================")
                print_vermelho("Usuário não encontrado.")
                print("=======================")
                return

            usuario_atual = usuarios[usuario_logado]
            tabela = []
            idx = 1
            chave_map = {}

            for chave, valor in usuario_atual.items():
                if chave == "Enderecos":
                    for i, endereco in enumerate(valor, 1):
                        tabela.append((idx, f"Endereço {i}", ""))
                        chave_map[idx] = (
                            usuario_atual["Enderecos"], i-1, None)
                        idx += 1
                        for end_chave, end_valor in endereco.items():
                            tabela.append((idx, f"  {end_chave}", end_valor))
                            chave_map[idx] = (
                                usuario_atual["Enderecos"][i-1], end_chave)
                            idx += 1
                else:
                    tabela.append((idx, chave, valor))
                    chave_map[idx] = (usuario_atual, chave)
                    idx += 1

            print(tabulate(tabela, headers=[
                  "", "Campo", "Informação"], tablefmt="rounded_grid"))

            chave_num = int(
                input("Digite o número da chave que deseja atualizar: "))
            if chave_num not in chave_map:
                clear_screen()
                print("\n================")
                print_vermelho("Número inválido.")
                print("================")
                return

            obj, chave = chave_map[chave_num]
            if chave is None:
                clear_screen()
                print("\n================")
                print_vermelho(
                    "Você selecionou um título, não pode ser atualizado.")
                print("================")
                return

            valor = input(f"Digite a nova informação para {chave}: ")

            # Função para fazer validação de input aqui (se necessário)
            obj[chave] = valor

            f.seek(0)
            f.truncate()
            json.dump(usuarios, f, indent=4)
            clear_screen()
            print("==================================")
            print_verde("Informação atualizada com sucesso.")
            print("==================================")

    except FileNotFoundError:
        clear_screen()
        print("A======================")
        print_vermelho("Arquivo não encontrado.")
        print("=======================")
    except json.JSONDecodeError:
        clear_screen()
        print("===================================")
        print_vermelho("Erro ao decodificar o arquivo JSON.")
        print("===================================")
    except KeyError as e:
        clear_screen()
        print_vermelho(f"Chave não encontrada: {e}")
    except Exception as e:
        clear_screen()
        print("========================================================")
        print_vermelho("Ocorreu um erro:", e)
        print("========================================================")


def deletar_usuario(arquivo, usuario_logado, dados_usuario):
    try:
        with open(arquivo) as f:
            usuarios = json.load(f)

        if usuario_logado in usuarios:
            dados_usuario = usuarios[usuario_logado]
            tabela = []
            idx = 1
            for chave, valor in dados_usuario.items():
                if chave == "Enderecos":
                    for i, endereco in enumerate(valor, 1):
                        tabela.append((f"Endereço {i}", ""))
                        for end_chave, end_valor in endereco.items():
                            tabela.append((f"  {end_chave}", end_valor))
                else:
                    tabela.append((chave, valor))

            print(tabulate(tabela, headers=[
                  "Campo", "Informação"], tablefmt="rounded_grid"))
            input("Pressione Enter para continuar.")

            conf = input(
                "Você realmente deseja deletar seu perfil? (S ou N) -> ")
            if conf.lower() == "s":
                del usuarios[usuario_logado]
                with open(arquivo, "w") as f:
                    json.dump(usuarios, f, indent=4)
                clear_screen()
                print("=============================")
                print_verde("Usuário deletado com sucesso!")
                print("=============================")
                return True
            else:
                clear_screen()
                print("===============================")
                print("Deletação do usuário cancelada!")
                print("===============================")
                return False
    except FileNotFoundError:
        clear_screen()
        print("=======================")
        print_vermelho("Arquivo não encontrado.")
        print("=======================")
    except Exception as e:
        clear_screen()
        print("===========================================================")
        print_vermelho("Ocorreu um erro:", e)
        print("===========================================================")
    return False
