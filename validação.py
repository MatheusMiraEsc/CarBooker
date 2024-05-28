import re
import json
from datetime import datetime
# from package_viacep import viacep


def validar_nome(nome):
    if len(nome) == 0:
        return False, "Nome não pode ficar vazio."
    elif not nome.isalpha():
        return False, "Nome deve ser composto apenas por letras."
    return True, ""


def validar_sobrenome(sobrenome):
    if not sobrenome.isalpha() and sobrenome != "":
        return False, "Sobrenome deve ser composto apenas por letras ou pode ficar vazio."
    return True, ""


def validar_data_nascimento(data):
    try:
        datetime.strptime(data, '%d/%m/%Y')
        dia, mes, ano = map(int, data.split('/'))
        if not (1 <= dia <= 30):
            return False, "Dia deve estar entre 1 e 30."
        elif not (1 <= mes <= 12):
            return False, "Mês deve estar entre 1 e 12."
        elif not (1930 <= ano <= 2005):
            return False, "Ano deve estar entre 1930 e 2004."
    except ValueError:
        return False, "Data de nascimento deve estar no formato dd/mm/yyyy."
    return True, ""


def validar_cep(cep):
    if len(cep) == 8:
        padrao_cep = re.compile(r'(\d){5}(\d){3}')

        match = padrao_cep.match(cep)

        return True


def validar_cpf(cpf, arquivo):
    if not cpf.isdigit():
        return False, "CPF deve ser composto apenas por números."
    elif len(cpf) != 11:
        return False, "CPF deve ter exatamente 11 caracteres."
    try:
        with open(arquivo, "r") as f:
            dados = json.load(f)
            for usuario in dados.values():
                if usuario["CPF"] == cpf:
                    return False, "CPF já cadastrado."
    except FileNotFoundError:
        pass
    return True, ""


def validar_cnpj(cnpj):
    if not cnpj.isdigit():
        return False, "CPF deve ser composto apenas por números."
    elif len(cnpj) != 12:
        return False, "CPF deve ter exatamente 12 caracteres."
    return True, ""


def validar_cnh(cnh):
    if not cnh.isdigit():
        return False, "CNH deve ser composta apenas por números."
    elif len(cnh) != 9:
        return False, "CNH deve ter exatamente 9 caracteres."
    return True, ""


def validar_genero(genero):
    if not genero.isalpha():
        return False, "Gênero deve ser composto apenas por letras."
    return True, ""


def validar_telefone(telefone):
    if not telefone.isdigit():
        return False, "Telefone deve ser composto apenas por números."
    elif len(telefone) != 11:
        return False, "Telefone deve ter exatamente 11 caracteres."
    elif telefone[2] != '9':
        return False, "Telefone deve começar com um 9."
    return True, ""


def validar_email(email, arquivo):
    if '@' not in email:
        return False, "Email deve conter '@'."
    elif len(email) == 0:
        return False, "Email não pode ficar vazio."
    try:
        with open(arquivo, "r") as f:
            dados = json.load(f)
            for usuario in dados.values():
                if usuario["Email"] == email:
                    return False, "Email já cadastrado."
    except FileNotFoundError:
        pass
    return True, ""


def validar_senha(senha):
    if len(senha) == 0:
        return False, "Senha não pode ficar vazia."
    has_upper = any(c.isupper() for c in senha)
    has_lower = any(c.islower() for c in senha)
    has_digit = any(c.isdigit() for c in senha)
    has_symbol = any(not c.isalnum() for c in senha)
    if not has_upper:
        return False, "Senha deve conter pelo menos uma letra maiúscula."
    elif not has_lower:
        return False, "Senha deve conter pelo menos uma letra minúscular."
    elif not has_digit:
        return False, "Senha deve conter pelo menos um número."
    elif not has_symbol:
        return False, "Senha deve conter pelo menos um símbolo."
    return True, ""


def validar_cnpj(cnpj):
    if not len(cnpj) != 14:
        return False, "CNPJ deve conter 14 dígitos."
    elif len(cnpj) == 0:
        return False, "CNPJ não pode ficar vazio"
    elif not cnpj.isdigit():
        return False, "CNPJ deve conter apenas números"
    else:
        print("CNPJ inválido. Por favor, insira um CNPJ válido.")
        return False
