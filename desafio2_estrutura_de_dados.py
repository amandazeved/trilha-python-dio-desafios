import datetime
import textwrap   

def exibir_menu():
    menu = """
        [1] Depositar
        [2] Sacar
        [3] Extrato
        [4] Cadastrar Usuário
        [5] Criar Conta Corrente
        [6] Remover Conta Corrente
        [7] Listar Contas Correntes
        [8] Sair

        => """
    return int(input(textwrap.dedent(menu)))

# Função precisa ter argumentos do tipo keyword only para fins de aprendizagem
def sacar(*,saldo, numero_saques, limite_de_saques, limite_valor):
    if numero_saques >= limite_de_saques:
        print("\n=> Não é mais permitido fazer saques hoje.")
    else:
        saque = 0
        while True:
            saque = input("\nInsira o valor do saque:\n")

            if saque.isnumeric():
                saque = float(saque)
                if saque <= limite_valor and saque <= saldo:
                    break
                else:
                    print(f"=> Valor inválido: saque maior que R$ {limite_valor} ou saldo insuficiente\n")
            else:
                print("=> Valor inválido.\n")

        
        return saque, {"valor": saque, "data_hora": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}
    
    return 0, None

# Função precisa ter argumentos do tipo positional only para fins de aprendizagem
def depositar(saldo, historico_deposito, /):
    deposito = 0
    while True:
        deposito = input("\nInsira o valor que deseja depositar: \n")

        if deposito.isnumeric():
            deposito = float(deposito)
            if deposito > 0:
                break
            else:
                print("\n=> Valor inválido.\n")
        else:
            print("\n=> Valor inválido.\n")
    
    if deposito != 0:
            historico_deposito.append({"valor": deposito, "data_hora": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")})
            saldo += deposito
            print("\n=> Depósito realizado com sucesso.\n")

    return saldo

# Função precisa ter argumentos do tipo positional only e keyword only para fins de aprendizagem
def extrato(saldo,/,*, historico_deposito, historico_saque):
    if len(historico_deposito) == 0 and len(historico_saque) == 0:
        print("\n=> Não foram realizados movimenteções.")
    else: 
        print(f"\n-----------------------------\nDepósitos:")
        
        for d in historico_deposito:
            print(f"R$ {d['valor']:.2f}  Horário: {d['data_hora']}")
        
        print(f"\n-----------------------------\nSaques:")
        
        for s in historico_saque:
            print(f"R$ {s['valor']:.2f}  Horário: {s['data_hora']}")

        print(f"""\n-----------------------------\nSaldo:\nR$ {saldo:.2f}""")

def adicionar_usuario(usuarios):
    cpf = input("Insira seu CPF: ")
    if cpf in usuarios:
        print("\n=> Operação inválida: CPF já cadastrado.")
    else:
        nome = input("Nome: ")
        data_nasc = input("Data de nascimento (dd-mm-aaaa): ")
        endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        usuarios[cpf] = {"nome": nome, "data_nasc": data_nasc, "endereco": endereco}
        print(f"\n=> Usuário de CPF: {cpf} cadastrado com sucesso.\n")

def adicionar_conta_corrente(contas, proximo_numero_conta, usuarios, numero_agencia):
    cpf = input("Informe CPF: ")

    if cpf not in usuarios:
        print("\n=> Operação inválida: Usuário não cadastrado.\n")
        return 0
    else:
        if proximo_numero_conta not in contas:
            contas[proximo_numero_conta] = {"cpf": cpf, "numero_agencia": numero_agencia, "saldo": 0, "saques_feitos_hoje": 0, "historico_deposito": [], "historico_saque": []}
            aux_numero_conta = proximo_numero_conta
            proximo_numero_conta +=1
            if proximo_numero_conta != len(contas)+1:
                proximo_numero_conta = len(contas)+1

        else:
            proximo_numero_conta = len(contas)+1
            contas[proximo_numero_conta] = {"cpf": cpf, "numero_agencia": numero_agencia, "saldo": 0, "saques_feitos_hoje": 0, "historico_deposito": [], "historico_saque": []}
            aux_numero_conta = proximo_numero_conta
            proximo_numero_conta +=1

        print(f"\n=> Cadastro de conta corrente de número: {aux_numero_conta} para o CPF {cpf} realizado com sucesso.\n")
        return proximo_numero_conta

def remover_conta_corrente(contas):
    numero_conta = input("Informe o número da conta: ")

    if numero_conta not in contas:
        print("\n=> Operação inválida: Número da conta não existe.\n")
        return 0
    else:
        del contas[numero_conta]
        print(f"\n=> Deletado conta {numero_conta} com sucesso.\n")
        return numero_conta
        
def exibir_contas(contas):
    if len(contas) == 0:
        print("\n=> Sem contas.")
        return 
    
    for k, i in contas.items():
        print(f"Conta: {k} Agência: {i['numero_agencia']} CPF: {i['cpf']}")

def main():
    LIMITE_SAQUES = 3
    NUMERO_AGENCIA = "0001"

    usuarios = {}
    contas = {}
    
    limite_valor_saque = 500
    proximo_numero_conta = 1

    while True:
        opcao = exibir_menu()

        if opcao == 1:
            numero_conta = int(input("Informe o número da conta: "))
            if numero_conta in contas:
                saldo = depositar(contas[numero_conta]["saldo"], contas[numero_conta]["historico_deposito"])
                contas[numero_conta]["saldo"] = saldo

            else:
                print("\n=> Operação inválida: Número da conta não existe.")
                

        elif opcao == 2:
            numero_conta = int(input("Informe o número da conta: "))
            if numero_conta in contas:
                saque, historico = sacar(saldo=contas[numero_conta]["saldo"], numero_saques=contas[numero_conta]["saques_feitos_hoje"], limite_de_saques=LIMITE_SAQUES, limite_valor=limite_valor_saque)
                if saque != 0:
                    contas[numero_conta]["historico_saque"].append(historico)
                    contas[numero_conta]["saques_feitos_hoje"] += 1
                    contas[numero_conta]["saldo"] -= saque
                    print("\n=> Saque realizado com sucesso.\n")
            else:
                print("\n=> Operação inválida: Número da conta não existe.")


        elif opcao == 3:
            numero_conta = int(input("Informe o número da conta: "))
            if numero_conta in contas:
                extrato(contas[numero_conta]["saldo"], historico_deposito=contas[numero_conta]["historico_deposito"], historico_saque=contas[numero_conta]["historico_saque"])
            else:
                print("\n=> Operação inválida: Número da conta não existe.")
            

        elif opcao == 4:
            adicionar_usuario(usuarios)
        
        elif opcao == 5:
            numero_conta = adicionar_conta_corrente(contas,proximo_numero_conta,usuarios, NUMERO_AGENCIA)
            if numero_conta !=0:
                proximo_numero_conta = numero_conta

        elif opcao == 6:
            numero_conta = remover_conta_corrente(contas)
            if numero_conta !=0:
                proximo_numero_conta = numero_conta

        elif opcao == 7:
            exibir_contas(contas)

        elif opcao == 8:
            break

        else:
            print("\n=> Operação inválida, por favor selecione novamente a operação desejada.")

main()
