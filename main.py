from usuarios import menu2, login, cadastrar_usuario, add_usuario
from locadoras import menu3, cadastrar_locadora, add_locadora, login_locadora
from util import menuOptions, clear_screen, print_vermelho, print_verde
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
            print("============================")
            print("1. Cadastro de Usuário")
            print("2. Cadastro de Locadora")
            print("3. Voltar")
            print("============================")
            tipo_cadastro = input("Escolha uma opção: ")
            if tipo_cadastro == "1":
                usuario = cadastrar_usuario(arquivo_usuario)
                add_usuario(usuario, arquivo_usuario)
            elif tipo_cadastro == "2":
                locadora = cadastrar_locadora(
                    arquivo_locadora)
                add_locadora(locadora, arquivo_locadora)
            elif tipo_cadastro == "3":
                clear_screen()
                print("===========")
                print("Voltando...")
                print("===========")
                sleep(2)
            else:
                clear_screen()
                print("================================")
                print_vermelho("Opção inválida. Tente novamente.")
                print("================================")
                sleep(2)

        elif opcao == "2":
            while True:
                clear_screen()
                print("============================")
                print("1. Login de Usuário")
                print("2. Login de Locadora")
                print("3. Voltar")
                print("============================")
                tipo_login = input("Escolha uma opção: ")
                if tipo_login == "1":
                    usuario_logado, dados_usuario = login(arquivo_usuario)
                    if usuario_logado:
                        clear_screen()
                        print("================================================")
                        print(f"Bem-vindo(a), {dados_usuario['Nome']}!")
                        print("================================================")
                        menu2(usuario_logado, dados_usuario)
                elif tipo_login == "2":
                    locadora_logada, dados_locadora = login_locadora(
                        arquivo_locadora)
                    if locadora_logada:
                        usuario_logado = locadora_logada
                        clear_screen()
                        print("=================================================")
                        print(f"Bem-vindo(a), {dados_locadora['Nome']}!")
                        print("=================================================")
                        menu3(locadora_logada, dados_locadora)
                elif tipo_login == "3":
                    clear_screen()
                    print("============")
                    print("Voltando...")
                    print("============")
                    sleep(2)
                    break
                else:
                    clear_screen()
                    print("================================")
                    print_vermelho("Opção inválida. Tente novamente.")
                    print("================================")
                    sleep(2)

        elif opcao == "3":
            clear_screen()
            print("========================================")
            print("Obrigado por usar o CarBooker. Até logo!")
            print("========================================")
            break

        else:
            clear_screen()
            print("====================================================")
            print_vermelho(
                "Opção inválida. Por favor, escolha uma opção válida")
            print("====================================================")
            sleep(2)


if __name__ == "__main__":
    main()
