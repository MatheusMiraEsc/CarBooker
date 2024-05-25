from usuarios import menu2, login, cadastrar_usuario, add_usuario
from locadoras import menu3, cadastrar_locadora, add_locadora, login_locadora
from carros import menu_locadora, visualizar_carro_usuario, visualizar_carro_locadora
from util import menuOptions, clear_screen
from time import sleep


def main():
    usuario_logado = None
    dados_usuario = None
    dados_locadora = None
    while True:
        clear_screen()
        menuOptions()

        arquivo_usuario = "usuarios.json"
        arquivo_locadora = "locadoras.json"
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            clear_screen()
            print("\n1. Cadastro de Usuário")
            print("2. Cadastro de Locadora")
            print("3. Voltar")
            print("============================")
            tipo_cadastro = input("Escolha uma opção: ")
            if tipo_cadastro == "1":
                usuario = cadastrar_usuario(arquivo_usuario)
                add_usuario(usuario, arquivo_usuario)
            elif tipo_cadastro == "2":
                locadora = cadastrar_locadora()
                add_locadora(locadora, arquivo_locadora)
            elif tipo_cadastro == "3":
                print("")
            else:
                print("Opção inválida. Tente novamente.")
                sleep(2)

        elif opcao == "2":
            clear_screen()
            print("============================")
            print("\n1. Login de Usuário")
            print("2. Login de Locadora")
            print("3. Voltar")
            print("============================")
            tipo_login = input("Escolha uma opção: ")
            if tipo_login == "1":
                usuario_logado, dados_usuario = login(arquivo_usuario)
                if usuario_logado:
                    print(f"Bem-vindo(a), {dados_usuario['Nome']}!")
                    menu2(usuario_logado, dados_usuario)
            elif tipo_login == "2":
                locadora_logada, dados_locadora = login_locadora(
                    arquivo_locadora)
                if locadora_logada:
                    usuario_logado = locadora_logada
                    print(f"Bem-vindo(a), {dados_locadora['Nome']}!")
                    menu3(locadora_logada, dados_locadora)
            elif tipo_login == "3":
                print("")
            else:
                print("Opção inválida. Tente novamente.")
                sleep(2)

        elif opcao == "3":
            print("Obrigado por usar o CarBooker. Até logo!")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida")
            sleep(2)


if __name__ == "__main__":
    main()
