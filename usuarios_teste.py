import json
import os


def menu2():
    arquivo_json = "usuarios.json"
    while True:
        print("\n=================================")
        print("1. Cadastrar usuário")
        print("2. Visualizar usuário")
        print("3. Atualizar informações do usuário")
        print("4. Deletar usuário")
        print("5. Voltar")
        print("=================================")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            usuario = cadastrar_usuario()
            add_usuario(usuario, arquivo_json)
        elif opcao == "2":
            visualizar_usuario(arquivo_json)
        elif opcao == "3":
            atualizar_usuario(arquivo_json)
        elif opcao == "4":
            deletar_usuario(arquivo_json)
        elif opcao == "5":
            break
        else:
            print("Opção inválida! Tente novamente\n")


def menu3():
    arquivo_json = "locadoras.json"
    while True:
        print("\n=================================")
        print("1. Cadastrar Locadora")
        print("2. Visualizar Locadora")
        print("3. Atualizar informações da Locadora")
        print("4. Deletar Locadora")
        print("5. Voltar")
        print("=================================")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            locadora = cadastrar_locadora()
            add_locadora(locadora, arquivo_json)
        elif opcao == "2":
            visualizar_locadora(arquivo_json)
        elif opcao == "3":
            atualizar_locadora(arquivo_json)
        elif opcao == "4":
            deletar_locadora(arquivo_json)
        elif opcao == "5":
            break
        else:
            print("Opção inválida! Tente novamente\n")


def cadastrar_usuario():
    chaves = ["Nome", "Sobrenome", "Data de nascimento",
              "CPF", "CNH", "Genero", "Telefone", "Email", "Senha"]
    usuarios = {}
    for chave in chaves:
        dados_usuario = input(f"Digite seu(sua) {chave}: ")
        usuarios[chave] = dados_usuario
    return usuarios





def visualizar_usuario(arquivo):
    try:
        with open(arquivo, "r") as f:
            usuario = json.load(f)
            numero_usuarios = len(usuario)
            nome_usuario = f"Usuário {numero_usuarios}"
        nome = input(
            "Digite o nome do usuário que deseja visualizar: ")
        senha = input("Digite a sua senha: ")
        usuario_encontrado = False
        for dados, info in usuario.items():
            if info["Nome"] == nome and info["Senha"] == senha:
                usuario_encontrado = True
                print("\n==============================\n")
                print(nome_usuario)
                for chave, valor in info.items():
                    print(f"{chave}: {valor}")
                print("\n==============================\n")
                break
        if not usuario_encontrado:
            print("Usuário não encontrado ou senha incorreta.")
    except FileNotFoundError:
        print("Arquivo não encontrado")
    except Exception as e:
        print("Ocorreu um erro:", e)


def atualizar_usuario(arquivo):
    try:
        with open(arquivo, "r+") as f:
            usuario = json.load(f)
            numero_usuarios = len(usuario)
            nome_usuario = f"Usuário {numero_usuarios}"
            nome = input(
                "Digite o nome do usuário que deseja atualizar: ")
            usuario_encontrado = False
            for dados, info in usuario.items():
                if info["Nome"] == nome:
                    senha = input("Digite a sua senha: ")
                    if info["Senha"] == senha:
                        usuario_encontrado = True
                        print("\n==============================\n")
                        print(nome_usuario)
                        for chave, valor in info.items():
                            print(f"{chave}: {valor}")
                        print("\n==============================\n")
                        chave = input("Digite a chave que deseja atualizar: ")
                        valor = input("Digite a informação a ser atualizada: ")
                        info[chave] = valor
                        f.seek(0)
                        json.dump(usuario, f, indent=4)
                        print("Usuário atualizado com sucesso!")
                        break
        if not usuario_encontrado:
            print("Usuário não encontrado ou senha incorreta.")
    except FileNotFoundError:
        print("Arquivo não encontrado")
    except Exception as e:
        print("Ocorreu um erro:", e)


def deletar_usuario(arquivo):
    try:
        with open(arquivo, "r+") as f:
            usuarios = json.load(f)
            numero_usuarios = len(usuarios)
            nome_usuario = f"Usuario {numero_usuarios}"
            nome = input(
                "Digite o nome do usuário que deseja deletar: ")
            usuario_encontrado = False
            for dados, info in list(usuarios.items()):
                if info["Nome"] == nome:
                    senha = input("Digite a sua senha: ")
                    if info["Senha"] == senha:
                        usuario_encontrado = True
                        print("\n==============================\n")
                        print(nome_usuario)
                        for chave, valor in info.items():
                            print(f"{chave}: {valor}")
                        print("\n==============================\n")
                        conf = input(
                            "Você realmente deseja deletar seu perfil? (S ou N) -> ")
                        if conf.lower() == "s":
                            del usuarios[dados]
                            print("Usuário deletado com sucesso!")
                        else:
                            print("Deletação do usuário cancelada!")
                            break
                    f.seek(0)
                    json.dump(usuarios, f, indent=4)
                    break
        if not usuario_encontrado:
            print("Usuário não encontrado ou senha incorreta.")
        else:
            with open(arquivo, "w") as f:
                json.dump(usuarios, f, indent=4)
    except FileNotFoundError:
        print("Arquivo não encontrado")
    except Exception as e:
        print("Ocorreu um erro:", e)

def cadastrar_locadora():
    chaves = ["Nome", "CNPJ","Email", "Telefone", "Senha"]
    locadoras = {}
    for chave in chaves:
        dados_locadora = input(f"Digite seu(sua) {chave}: ")
        locadoras[chave] = dados_locadora
    return locadoras

def add_usuario(usuario, arquivo):
    try:
        with open(arquivo, "r") as f:
            dados = json.load(f)
    except FileNotFoundError:
        print("Arquivo não encontrado")
    except Exception as e:
        print("Ocorreu um erro:", e)

    numero_usuarios = len(dados)+1
    nome_usuario = f"Usuario {numero_usuarios}"
    dados[nome_usuario] = usuario

    try:
        with open(arquivo, "w") as f:
            json.dump(dados, f, indent=4)
        print(f"Usuário {numero_usuarios} cadastrado com sucesso!")
    except Exception as e:
        print("Ocorreu um erro: ", e)

def add_locadora(locadora, arquivo):
    try:
        with open(arquivo, "r") as f:
            dados= json.load(f)
    except FileNotFoundError:
        print("Arquivo não encontrado")
    except Exception as e:
        print("Ocorreu um erro: ", e)

    numero_locadoras = len(dados)+1
    nome_locadora = f"  Locadora {numero_locadoras}"
    dados[nome_locadora] = locadora

    try:
        with open(arquivo, "w") as f:
            json.dump(dados, f, indent=4)
        print(f"Locadora {numero_locadoras} cadastrada com sucesso!")
    except Exception as e:
        print("Ocorreu um erro: ", e)

def visualizar_locadora(arquivo):
    try:
        with open(arquivo, "r") as f:
            locadora = json.load(f)
            numero_locadoras = len(locadora)
            nome_locadora = f"Locadora {numero_locadoras}"
        nome = input(
            "Digite o nome da locadora que deseja visualizar: ")
        locadora_encontrada = False
        for dados, info in locadora.items():
            if info["Nome"] == nome:
                senha = input("Digite a sua senha: ")
                if info["Senha"] == senha:
                    locadora_encontrada = True
                    print("\n==============================\n")
                    print(nome_locadora)
                    for chave, valor in info.items():
                        print(f"{chave}:{valor}")
                    print("\n==============================\n")
                    break
        if not locadora_encontrada:
            print("Locadora não encontrada ou senha incorreta.")
    except FileNotFoundError:
        print("Arquivo não encontrado")
    except Exception as e:
        print("Ocorreu um erro:", e)

def atualizar_locadora(arquivo):
    try:
        with open(arquivo, "r+") as f:
            locadora = json.load(f)
            numero_locadoras = len(locadora)
            nome_locadora = f"Locadora {numero_locadoras}"
            nome = input("Digite o nome da Locadora que dejesa atualizar: ")
            locadora_encontrada = False
            for dados, info in locadora.items():
                if info["Nome"] == nome:
                    senha = input("Digite a sua senha: ")
                    if info["Senha"] == senha:
                        locadora_encontrada = True
                        print("\n==============================\n")
                        print(nome_locadora)
                        for chave, valor in info.items():
                            print(f"{chave}: {valor}")
                        print("\n==============================\n")
                        chave = input("Digite a chave que deseja atualizar")
                        valor = input("Digite a Informação a ser atualizada")
                        info[chave] = valor
                        f.seek(0)
                        json.dump(locadora, f, indent=4)
                        print("Usuário atualizado com sucesso!")
                        break
        if not locadora_encontrada:
            print("Locadora não encontrada ou senha incorreta.")
    except FileNotFoundError:
        print("Arquivo não encontrado")
    except Exception as e:
        print("Ocorreu um erro:", e)

def deletar_locadora(arquivo):
    try:
        with open(arquivo, "r+") as f:
            locadora = json.load(f)
            numero_locadoras = len(locadora)
            nome_locadora = f"Locadora {numero_locadoras}"
            nome = input(
                "Digite o nome da locadora que deseja deletar: ")
            locadora_encontrada = False
            for dados, info in list(locadora.items()):
                if info["Nome"] == nome:
                    senha = input("Digite a sua senha: ")
                    if info["Senha"] == senha:
                        locadora_encontrada = True
                        print("\n==============================\n")
                        print(nome_locadora)
                        for chave, valor in info.items():
                            print(f"{chave}: {valor}")
                        print("\n==============================\n")
                        conf = input(
                            "Você realmente deseja deletar seu perfil? (S ou N) -> ")
                        if conf.lower() == "s":
                            del locadora[dados]
                            print("Locadora deletada com sucesso!")
                        else:
                            print("Exclusão da locadora cancelada!")
                            break
                    f.seek(0)
                    json.dump(locadora, f, indent=4)
                    break
        if not locadora_encontrada:
            print("Locadora não encontrada ou senha incorreta. ")
        else:
            with open(arquivo, "w") as f:
                json.dump(locadora, f, indent=4)
    except FileNotFoundError:
        print("Arquivo não encontrado")
    except Exception as e:
        print("Ocorreu um erro:", e)

def main():

    while True:
        print("\n============================")
        print("Bem vindo(a) ao CarBooker!! ")
        print("============================")
        print("1. Usuário")
        print("2. Locadora")
        print("3. Sair")
        print("============================")
        arquivo_json = "usuarios.json"
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            menu2()
        elif opcao == "2":
            menu3()
        else:
            break


if __name__ == "__main__":
    main()
