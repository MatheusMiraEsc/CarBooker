import json
import datetime
from time import sleep
from util import clear_screen, print_vermelho, print_verde
from carros import visualizar_carro_usuario
from tabulate import tabulate


def menu_usuario_reserva(dados_usuario):
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
        elif opcao2 == "3":
            checar_reserva(arquivo_reservas, dados_usuario)
        elif opcao2 == "4":
            alterar_reserva(arquivo_reservas, dados_usuario)
            sleep(2)
        elif opcao2 == "5":
            cancelar_reserva(arquivo_reservas, arquivo_carros,
                             dados_usuario)
            sleep(2)
        elif opcao2 == "6":
            break
        else:
            clear_screen()
            print("\n================================")
            print_vermelho("Opção inválida! Tente novamente")
            print("==================================")
            sleep(2)


def menu_locadora_reserva(dados_locadora):
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
            cancelar_reserva_locadora(
                arquivo_reservas, arquivo_carros, dados_locadora)
            sleep(2)
        elif opcao2 == "3":
            break
        else:
            clear_screen()
            print("\n================================")
            print_vermelho("Opção inválida! Tente novamente")
            print("==================================")
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
        clear_screen()
        print("\n==============================")
        print_vermelho(mensagem)
        print("================================")
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
        for carro in dados_carro.values():
            if carro["Placa"] == placa and carro["Status reserva"] == "Disponivel":
                clear_screen()
                tabela = [(chave, info) for chave, info in carro.items()]
                print(tabulate(tabela, headers=[
                      "Campo", "Informação"], tablefmt="rounded_grid"))
                print("\n1. Confirmar reserva")
                print("2. Escolher outro carro")

                conf = input("Escolha uma opção: ")
                if conf == "1":
                    carro["Status reserva"] = "Reservado"
                    reserva["Placa do carro"] = carro["Placa"]
                    reserva["Locadora"] = carro["Locadora"]
                    reserva["CNPJ da Locadora"] = carro["CNPJ da locadora"]
                    f.seek(0)
                    f.truncate()
                    json.dump(dados_carro, f, indent=4)
                    carro_encontrado = True
                    break
                elif conf == "2":
                    return
                else:
                    clear_screen()
                    print("\n===============")
                    print_vermelho("Opção inválida!")
                    print("=================")
                    sleep(2)

    if not carro_encontrado:
        clear_screen()
        print("====================================")
        print_vermelho("Carro não encontrado ou já reservado")
        print("====================================")
        sleep(2)
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
    except (FileNotFoundError, json.JSONDecodeError):
        reservation = {}

    reservation[id_usuario] = reserva

    try:
        with open(arquivo, "w") as f:
            json.dump(reservation, f, indent=4)
        clear_screen()
        print("==============================")
        print_verde("Reserva realizada com sucesso!")
        print("==============================")
        sleep(2)
    except Exception as e:
        clear_screen()
        print("=============================================================")
        print_vermelho("Ocorreu um erro ao salvar a reserva: ", e)
        print("=============================================================")
        sleep(2)


def checar_reserva(arquivo, dados_usuario):
    try:
        with open(arquivo, "r") as f:
            reservas = json.load(f)
    except FileNotFoundError:
        clear_screen()
        print("\n===================================")
        print_vermelho("Arquivo de reservas não encontrado.")
        print("=====================================")
        sleep(2)
        return
    except json.JSONDecodeError:
        clear_screen()
        print("\n==================================")
        print_vermelho("Erro ao ler o arquivo de reservas.")
        print("===================================")
        sleep(2)
        return
    cpf_usuario = dados_usuario["CPF"]

    if cpf_usuario in reservas:
        tabela = []
        for chaves, info in reservas[cpf_usuario].items():
            tabela.append((chaves, info))

        print(tabulate(tabela, headers=[
              "Campo", "Informação"], tablefmt="rounded_grid"))
    else:
        clear_screen()
        print("============================")
        print_vermelho(f"Nenhuma reserva encontrada.")
        print("=============================")

    input("Pressione Enter para continuar.")


def checar_reservas_locadora(arquivo, dados_locadora):
    try:
        with open(arquivo, "r") as f:
            reservas = json.load(f)
    except FileNotFoundError:
        clear_screen()
        print("\n===================================")
        print_vermelho("Arquivo de reservas não encontrado.")
        print("=====================================")
        sleep(2)
        return
    except json.JSONDecodeError:
        clear_screen()
        print("\n==================================")
        print_vermelho("Erro ao ler o arquivo de reservas.")
        print("====================================")
        sleep(2)
        return

    reservas_encontradas = False
    tabela = []

    for dados in reservas.values():
        if dados["CNPJ da Locadora"] == dados_locadora["CNPJ"]:
            if not reservas_encontradas:
                clear_screen()
                print("\n==============================")
                print("Reservas feitas:")
                reservas_encontradas = True

            for chaves, info in dados.items():
                tabela.append((chaves, info))
            tabela.append(("==============================",
                          "=============================="))

    if reservas_encontradas:
        print(tabulate(tabela, headers=[
              "Campo", "Informação"], tablefmt="rounded_grid"))
    else:
        clear_screen()
        print("============================")
        print_vermelho("Nenhuma reserva encontrada.")
        print("=============================")

    input("Pressione Enter para continuar.")


def alterar_reserva(arquivoReservas, usuario):
    try:
        with open(arquivoReservas) as f:
            reserva = json.load(f)
            confirmar_reserva = False
            dados_usuario = {}

            for chave, dados in reserva.items():
                if chave == usuario["CPF"]:
                    confirmar_reserva = True
                    dados_usuario = dados
                    chaves_editaveis = [
                        "Data da retirada", "Data da devolucao", "Horario da retirada", "Horario da devolucao"]
                    break

            if not confirmar_reserva:
                clear_screen()
                print("\n=============================")
                print_vermelho("Usuário não tem reserva feita")
                print("===============================")
                sleep(2)
                return

            chaves_mapeadas = {idx + 1: chave for idx,
                               chave in enumerate(chaves_editaveis)}

            tabela = [(idx, chave, dados_usuario[chave]) for idx,
                      chave in chaves_mapeadas.items() if chave in dados_usuario]
            clear_screen()
            print(tabulate(tabela, headers=[
                  "Número", "Campo", "Informação"], tablefmt="rounded_grid"))

            chave_num_str = input(
                "Digite o número da chave que deseja atualizar ou pressione enter para voltar: ")
            if chave_num_str == "":
                clear_screen()
                print("\n============")
                print("Voltando...")
                print("==============")
                sleep(2)
                return

            try:
                chave_num = int(chave_num_str)
                if chave_num not in chaves_mapeadas:
                    raise ValueError("Número inválido.")
            except ValueError:
                clear_screen()
                print("\n================")
                print_vermelho("Número inválido.")
                print("==================")
                sleep(2)
                return

            chave = chaves_mapeadas[chave_num]
            valor = input(f"Digite a nova informação para {chave}: ")

            dados_usuario[chave] = valor

            with open(arquivoReservas, "w") as f:
                json.dump(reserva, f, indent=4)

            clear_screen()
            print("\n=============================")
            print_verde("Reserva alterada com sucesso.")
            print("==============================")
            sleep(2)

    except FileNotFoundError:
        clear_screen()
        print("\n===================================")
        print_vermelho("Arquivo de reservas não encontrado.")
        print("=====================================")
        sleep(2)
    except json.JSONDecodeError:
        clear_screen()
        print("\n==================================")
        print_vermelho("Erro ao ler o arquivo de reservas.")
        print("====================================")
        sleep(2)
    except Exception as e:
        clear_screen()
        print("\n=============================================")
        print_vermelho(f"Ocorreu um erro: {e}")
        print("===============================================")
        sleep(2)


def cancelar_reserva(arquivo_reservas, arquivo_carros, dados_usuario):
    try:
        with open(arquivo_reservas, "r+") as f_reservas:
            try:
                reservas = json.load(f_reservas)
            except json.JSONDecodeError:
                reservas = {}

            reserva_usuario = reservas.get(dados_usuario["CPF"])
            if reserva_usuario is None:
                clear_screen()
                print("\n===========================")
                print_vermelho("Nenhuma reserva encontrada.")
                print("=============================")
                return False

            tabela = [(chave, valor)
                      for chave, valor in reserva_usuario.items()]
            print(tabulate(tabela, headers=[
                  "Campo", "Informação"], tablefmt="rounded_grid"))

            conf = input(
                "Você realmente deseja cancelar sua reserva? (S ou N) -> ")
            if conf.lower() == "s":
                with open(arquivo_carros, "r+") as f_carros:
                    try:
                        dados_carro = json.load(f_carros)
                    except json.JSONDecodeError:
                        dados_carro = {}

                    for _, valor in dados_carro.items():
                        if valor["Placa"] == reserva_usuario["Placa do carro"]:
                            valor["Status reserva"] = "Disponivel"
                            f_carros.seek(0)
                            f_carros.truncate()
                            json.dump(dados_carro, f_carros, indent=4)
                            break

                del reservas[dados_usuario["CPF"]]
                clear_screen()
                print("===============================")
                print_verde("Reserva cancelada com sucesso!")
                print("===============================")
                f_reservas.seek(0)
                f_reservas.truncate()
                json.dump(reservas, f_reservas, indent=4)
                return True
            else:
                return False
    except FileNotFoundError:
        clear_screen()
        print("=======================")
        print_vermelho("Arquivo não encontrado.")
        print("=======================")
    except Exception as e:
        clear_screen()
        print("==================================================")
        print_vermelho("Ocorreu um erro:", e)
        print("==================================================")
    return False


def cancelar_reserva_locadora(arquivo_reservas, arquivo_carros, dados_locadora):
    try:
        with open(arquivo_reservas, "r+") as f_reservas:
            try:
                reservas = json.load(f_reservas)
            except json.JSONDecodeError:
                reservas = {}

            placa_carro = input("Digite a placa do carro reservado: ")

            reservas_locadora = [key for key, reserva in reservas.items()
                                 if reserva.get("CNPJ da Locadora") == dados_locadora["CNPJ"] and
                                 reserva.get("Placa do carro") == placa_carro]

            if not reservas_locadora:
                clear_screen()
                print("\n===========================")
                print_vermelho("Nenhuma reserva encontrada.")
                print("============================")
                return False

            for key in reservas_locadora:
                reserva_locadora = reservas[key]
                tabela = [(chave, valor)
                          for chave, valor in reserva_locadora.items()]
                print(tabulate(tabela, headers=[
                      "Campo", "Informação"], tablefmt="grid"))

                conf = input(
                    "Você realmente deseja cancelar esta reserva? (S ou N) -> ")
                if conf.lower() == "s":
                    with open(arquivo_carros, "r+") as f_carros:
                        try:
                            dados_carro = json.load(f_carros)
                        except json.JSONDecodeError:
                            dados_carro = {}

                        for chave, valor in dados_carro.items():
                            if valor["Placa"] == placa_carro:
                                valor["Status reserva"] = "Disponível"
                                f_carros.seek(0)
                                f_carros.truncate()
                                json.dump(dados_carro, f_carros, indent=4)
                                break

                    del reservas[key]
                    clear_screen()
                    print("===============================")
                    print_verde("Reserva cancelada com sucesso!")
                    print("===============================")
                    f_reservas.seek(0)
                    f_reservas.truncate()
                    json.dump(reservas, f_reservas, indent=4)
                    return True
                else:
                    return False
    except FileNotFoundError:
        clear_screen()
        print("=======================")
        print_vermelho("Arquivo não encontrado.")
        print("=======================")
    except Exception as e:
        clear_screen()
        print("==================================================")
        print_vermelho("Ocorreu um erro:", e)
        print("==================================================")
    return False
