import json
import datetime
from time import sleep
from util import clear_screen
from carros import visualizar_carro_usuario


def menu_usuario_reserva(usuario_logado, dados_usuario):
    arquivo_usuario = "usuarios.json"
    arquivo_carros = "carros.json"
    arquivo_reservas = "reservas.json"
    while True:
        clear_screen()
        print("============================")
        print("1. Carros disponíveis")
        print("2. Fazer reserva")
        print("3. Checar reserva")
        print("4. Alterar reserva")
        print("5. Cancelar reserva")
        print("6. Voltar")
        print("============================")
        opcao2 = input("Escolha uma opção: ")
        if opcao2 == "1":
            visualizar_carro_usuario(arquivo_carros)
        elif opcao2 == "2":
            fazerReserva(arquivo_reservas,
                         dados_usuario, arquivo_carros)
            sleep(2)
        elif opcao2 == "3":
            checar_reserva(arquivo_reservas, dados_usuario)
        elif opcao2 == "4":
            alterar_reserva(arquivo_reservas, dados_usuario)
            sleep(2)
        elif opcao2 == "5":
            cancelar_reserva(arquivo_reservas, arquivo_carros, usuario_logado,
                             dados_usuario)
            sleep(2)
        elif opcao2 == "6":
            break
        else:
            print("Opção inválida! Tente novamente\n")
            sleep(2)


def menu_locadora_reserva(locadora_logada, dados_locadora):
    arquivo_usuario = "usuarios.json"
    arquivo_carros = "carros.json"
    arquivo_reservas = "reservas.json"
    while True:
        clear_screen()
        print("============================")
        print("1. Checar reservas")
        print("2. Cancelar reserva")
        print("3. Voltar")
        print("============================")
        opcao2 = input("Escolha uma opção: ")
        if opcao2 == "1":
            checar_reservas_locadora(arquivo_reservas, dados_locadora)
        elif opcao2 == "2":
            cancelar_reserva(arquivo_reservas, arquivo_carros, locadora_logada,
                             dados_locadora)
            sleep(2)
        elif opcao2 == "3":
            break
        else:
            clear_screen()
            print("Opção inválida! Tente novamente\n")
            sleep(2)


def confirmacao_reserva(arquivo, usuario):
    try:
        with open(arquivo) as f:
            reservas = json.load(f)
    except FileNotFoundError:
        return True, ""
    except json.JSONDecodeError:
        return True, ""

    for chave in reservas.keys():
        if chave == usuario["CPF"]:
            return False, "Usuário já fez reserva"
    return True, ""


def fazerReserva(arquivo, usuario, arquivoCarros):
    confirmado, mensagem = confirmacao_reserva(arquivo, usuario)
    if not confirmado:
        print(mensagem)
        sleep(2)
        return

    info_reservas = ["Data da retirada", "Data da devolucao",
                     "Horario da retirada", "Horario da devolucao",]
    placa = input("Digite a placa do carro que deseja reservar: ")
    reserva = {}
    nome_usuario = usuario["Nome"]
    id_usuario = usuario["CPF"]

    with open(arquivoCarros, "r+") as f:
        try:
            dados_carro = json.load(f)
        except json.JSONDecodeError:
            dados_carro = {}

        carro_encontrado = False
        for chave, carro in dados_carro.items():
            if carro["Placa"] == placa and carro["Status reserva"] == "Disponivel":
                for chave, dados in dados_carro.items():
                    print("\n==============================\n")
                    for chaves, info in dados.items():
                        print(f"{chaves}: {info}")
                    print("\n==============================\n")
                    print("1. Confirmar reserva")
                    print("2.  Escolher outro carro")
                conf = input("Escolha uma opção: ")
                if conf == "1":
                    carro["Status reserva"] = "Reservado"
                    reserva["Carro"] = carro["Placa"]
                    reserva["Locadora"] = carro["Locadora"]
                    reserva["CNPJ da Locadora"] = carro["CNPJ da locadora"]
                    carro_encontrado = True
                    break
                elif conf == "2":
                    return
                else:
                    print("Opção inválida!")

        with open(arquivoCarros, "r+") as f:
            f.seek(0)
            f.truncate()
            json.dump(dados_carro, f, indent=4)

    if not carro_encontrado:
        print("Carro não encontrado ou já reservado")
        return

    reserva["Nome usuario"] = nome_usuario
    reserva["Data da reserva"] = datetime.datetime.now().strftime("%d/%m/%Y")
    reserva["Horario da reserva"] = datetime.datetime.now().strftime("%H:%M")

    for info in info_reservas:
        dados_reserva = input(f"Digite o(a) {info}: ")
        reserva[info] = dados_reserva

    try:
        with open(arquivo, "r") as f:
            reservation = json.load(f)
    except FileNotFoundError:
        reservation = {}
    except json.JSONDecodeError:
        reservation = {}

    reservation[id_usuario] = reserva

    try:
        with open(arquivo, "w") as f:
            json.dump(reservation, f, indent=4)
        print("Reserva realizada com sucesso!")
    except Exception as e:
        print("Ocorreu um erro ao salvar a reserva: ", e)


def checar_reserva(arquivo, usuario):
    try:
        with open(arquivo) as f:
            reserva = json.load(f)
    except FileNotFoundError:
        reserva = {}

    for chave, dados in reserva.items():
        if chave == usuario["CPF"]:
            print("\n==============================\n")
            for chaves, info in dados.items():
                print(f"{chaves}: {info}")
            print("\n==============================\n")
    input("Pressione Enter para continuar.")


def checar_reservas_locadora(arquivo, dados_locadora):
    try:
        with open(arquivo, "r") as f:
            reservas = json.load(f)
    except FileNotFoundError:
        print("Arquivo de reservas não encontrado.")
        return
    except json.JSONDecodeError:
        print("Erro ao ler o arquivo de reservas.")
        return

    reservas_encontradas = False
    for chave, dados in reservas.items():
        if dados.get("CNPJ da locadora") == dados_locadora.get("CNPJ"):
            if not reservas_encontradas:
                print("\n==============================")
                print("Reservas feitas:")
                reservas_encontradas = True

            print("\n==============================\n")
            for chaves, info in dados.items():
                print(f"{chaves}: {info}")
            print("\n==============================\n")

    if not reservas_encontradas:
        print("Nenhuma reserva encontrada.")

    input("Pressione Enter para continuar.")


def alterar_reserva(arquivoReservas, usuario):
    try:
        with open(arquivoReservas) as f:
            reserva = json.load(f)

            for chave, dados in reserva.items():
                if chave == usuario["CPF"]:
                    chaves_editaveis = [
                        "Data da retirada", "Data da devolucao", "Horario da retirada", "Horario da devolucao"]
            chaves_mapeadas = {idx + 1: chave for idx,
                               chave in enumerate(chaves_editaveis)}

            print("\n==============================\n")
            for idx, chave in chaves_mapeadas.items():
                if chave in dados:
                    print(f"{idx}. {chave}: {dados[chave]}")
            print("\n==============================\n")

            chave_num = input(
                "Digite o número da chave que deseja atualizar ou pressione enter para voltar: ")
            if chave_num == "":
                print("Voltando...")
                return
            if chave_num.int() not in chaves_mapeadas:
                print("Número inválido.")
                return

            chave = chaves_mapeadas[chave_num.int()]
            valor = input(f"Digite a nova informação para {chave}: ")

            dados[chave] = valor

            with open(arquivoReservas, "w") as f:
                f.seek(0)
                f.truncate()
                json.dump(reserva, f, indent=4)
                print("Reserva alterada com sucesso.")

            if usuario["CPF"] not in dados:
                print("Usuário não tem reserva feita")
    except FileNotFoundError:
        print("Arquivo de reservas não encontrado.")
    except json.JSONDecodeError:
        print("Erro ao ler o arquivo de reservas.")
    except Exception as e:
        print("Ocorreu um erro:", e)


def cancelar_reserva(arquivo_reservas, arquivo_carros, usuario_logado, dados_usuario):
    try:
        with open(arquivo_reservas, "r+") as f_reservas:
            try:
                reservas = json.load(f_reservas)
            except json.JSONDecodeError:
                reservas = {}

            data = None
            for key, reserva in reservas.items():
                if key == dados_usuario["CPF"]:
                    print("\n==============================\n")
                    for chave, valor in reserva.items():
                        print(f"{chave}: {valor}")
                    print("\n==============================\n")
                    data = reserva
                    break

            if data is None:
                print("Nenhuma reserva encontrada para este usuário.")
                return False

            conf = input(
                "Você realmente deseja cancelar sua reserva? (S ou N) -> ")
            if conf.lower() == "s":
                with open(arquivo_carros, "r+") as f_carros:
                    try:
                        dados_carro = json.load(f_carros)
                    except json.JSONDecodeError:
                        dados_carro = {}

                    for chave, valor in dados_carro.items():
                        if valor["Placa"] == data["Carro"]:
                            valor["Status reserva"] = "Disponivel"
                            f_carros.seek(0)
                            f_carros.truncate()
                            json.dump(dados_carro, f_carros, indent=4)
                            break

                del reservas[dados_usuario["CPF"]]
                print("Reserva cancelada com sucesso!")
                f_reservas.seek(0)
                f_reservas.truncate()
                json.dump(reservas, f_reservas, indent=4)
                return True
            else:
                return False
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print("Ocorreu um erro:", e)
    return False
