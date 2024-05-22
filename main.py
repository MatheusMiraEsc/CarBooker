'''from usuarios import menu2, clear_screen, login_usuario, cadastrar_usuario, add_usuario
from locadoras import menu3, cadastrar_locadora, add_locadora, login_locadora
from carros import menu4
import os
import json
from time import sleep


def main():
    usuario_logado = None
    tipo_logado = None
    while True:
        clear_screen()
        print("\n============================")
        print("Bem-vindo(a) ao CarBooker!!")
        print("============================")
        print("1. Cadastro")
        print("2. Login")
        print("3. Usuário")
        print("4. Locadora")
        print("5. Carros")
        print("6. Sair")
        print("============================")
        arquivo_usuario = "usuarios.json"
        arquivo_locadora = "locadoras.json"
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\n1. Cadastro de Usuário")
            print("2. Cadastro de Locadora")
            tipo_cadastro = input("Escolha uma opção: ")
            if tipo_cadastro == "1":
                usuario = cadastrar_usuario()
                add_usuario(usuario, arquivo_usuario)
            elif tipo_cadastro == "2":
                locadora = cadastrar_locadora()
                add_locadora(locadora, arquivo_locadora)
            else:
                print("Opção inválida. Tente novamente.")
                sleep(2)

        elif opcao == "2":
            print("\n1. Login de Usuário")
            print("2. Login de Locadora")
            tipo_login = input("Escolha uma opção: ")
            if tipo_login == "1":
                usuario_logado, dados_usuario = login_usuario(arquivo_usuario)
                if usuario_logado:
                    tipo_logado = "usuario"
                    print(f"Bem-vindo(a), {dados_usuario['Nome']}!")
                    sleep(2)
            elif tipo_login == "2":
                usuario_logado, dados_locadora = login_locadora(
                    arquivo_locadora)
                if usuario_logado:
                    tipo_logado = "locadora"
                    print(f"Bem-vindo(a), {dados_locadora['Nome']}!")
                    sleep(2)
            else:
                print("Opção inválida. Tente novamente.")
                sleep(2)

        elif opcao == "3":
            if usuario_logado and tipo_logado == "usuario":
                menu2()
            else:
                print("Por favor, faça login como usuário primeiro.")
                sleep(2)

        elif opcao == "4":
            if usuario_logado and tipo_logado == "locadora":
                menu3()
            else:
                print("Por favor, faça login como locadora primeiro.")
                sleep(2)

        elif opcao == "5":
            if usuario_logado:
                menu4()
            else:
                print("Por favor, faça login primeiro.")
                sleep(2)

        elif opcao == "6":
            print("Obrigado por usar o CarBooker. Até logo!")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            sleep(2)


if __name__ == "__main__":
    main()
'''
from usuarios import menu2, clear_screen, login, cadastrar_usuario, add_usuario
from locadoras import menu3, cadastrar_locadora, add_locadora, login_locadora
from carros import menu_locadora, visualizar_carro
import os
import json
from time import sleep


def main():
    usuario_logado = None
    tipo_logado = None
    dados_usuario = None
    dados_locadora = None
    while True:
        clear_screen()
        print("\n============================")
        print("Bem-vindo(a) ao CarBooker!!")
        print("============================")
        print("1. Cadastro")
        print("2. Login")
        print("3. Usuário")
        print("4. Locadora")
        print("5. Carros")
        print("6. Sair")
        print("============================")
        arquivo_usuario = "usuarios.json"
        arquivo_locadora = "locadoras.json"
        arquivo_carros = "carros.json"
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\n1. Cadastro de Usuário")
            print("2. Cadastro de Locadora")
            tipo_cadastro = input("Escolha uma opção: ")
            if tipo_cadastro == "1":
                usuario = cadastrar_usuario()
                add_usuario(usuario, arquivo_usuario)
            elif tipo_cadastro == "2":
                locadora = cadastrar_locadora()
                add_locadora(locadora, arquivo_locadora)
            else:
                print("Opção inválida. Tente novamente.")
                sleep(2)

        elif opcao == "2":
            print("\n1. Login de Usuário")
            print("2. Login de Locadora")
            tipo_login = input("Escolha uma opção: ")
            if tipo_login == "1":
                usuario_logado, dados_usuario = login(arquivo_usuario)
                if usuario_logado:
                    tipo_logado = "usuario"
                    print(f"Bem-vindo(a), {dados_usuario['Nome']}!")
                    sleep(2)
            elif tipo_login == "2":
                locadora_logada, dados_locadora = login_locadora(
                    arquivo_locadora)
                if locadora_logada:
                    usuario_logado = locadora_logada
                    tipo_logado = "locadora"
                    print(f"Bem-vindo(a), {dados_locadora['Nome']}!")
                    sleep(2)
            else:
                print("Opção inválida. Tente novamente.")
                sleep(2)

        elif opcao == "3":
            if usuario_logado and tipo_logado == "usuario":
                menu2(usuario_logado, dados_usuario)
            else:
                print("Por favor, faça login como usuário primeiro.")
                sleep(2)

        elif opcao == "4":
            if usuario_logado and tipo_logado == "locadora":
                menu3(usuario_logado, dados_locadora)
            else:
                print("Por favor, faça login como locadora primeiro.")
                sleep(2)

        elif opcao == "5":
            if usuario_logado and tipo_logado == "locadora":
                menu_locadora()
            elif usuario_logado and tipo_logado == "usuario":
                visualizar_carro(arquivo_carros)
            else:
                print("Por favor, faça login primeiro.")
                sleep(2)

        elif opcao == "6":
            print("Obrigado por usar o CarBooker. Até logo!")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida")
            sleep(2)


if __name__ == "__main__":
    main()
