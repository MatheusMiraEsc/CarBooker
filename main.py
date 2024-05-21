from usuarios import menu2, clear_screen
from locadoras import menu3
import os
import json
from time import sleep


def main():

    while True:
        clear_screen()
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
        elif opcao == "3":
            print("Obrigado por usar o CarBooker. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            sleep(3)


if __name__ == "__main__":
    main()
