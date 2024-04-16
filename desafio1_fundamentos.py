import datetime

menu = """

[D]epositar
[S]acar
[E]xtrato
S[a]ir

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

formato_data = "%d/%m/%Y %H:%M"

historico_deposito= []
historico_saque= []

while True:

    opcao = input(menu).upper()

    if opcao == "D":
        deposito = 0
        while True:
            deposito = input("\nInsira o valor que deseja depositar: \n")

            if deposito.isnumeric():
                deposito = float(deposito)
                if deposito > 0:
                    break
                else:
                    print("Valor inválido.\n")
            else:
                print("Valor inválido.\n")
        
        if deposito != 0:
            historico_deposito.append({"valor": deposito, "data_hora": datetime.datetime.now().strftime(formato_data)})
            saldo += deposito
            print("Depósito realizado com sucesso.\n")

    elif opcao == "S":
        if numero_saques >= 3:
            print("\nNão é mais permitido fazer saques hoje.")
        else:
            saque = 0
            while True:
                saque = input("\nInsira o valor do saque:\n")

                if saque.isnumeric():
                    saque = float(saque)
                    if saque <= 500 and saque <= saldo:
                        break
                    else:
                        print(f"Valor inválido: saque maior que R$ 500 ou saldo insuficiente\n")
                else:
                    print("Valor inválido.\n")

            if saque != 0:
                historico_saque.append({"valor": saque, "data_hora": datetime.datetime.now().strftime(formato_data)})
                numero_saques += 1
                saldo -= saque
                print("Saque realizado com sucesso.\n")

    elif opcao == "E":
        if len(historico_deposito) == 0 and len(historico_saque) == 0:
            print("\nNão foram realizados movimenteções.")
        else: 
            print(f"\n-----------------------------\nDepósitos:")
            
            for d in historico_deposito:
                print(f"R$ {d['valor']:.2f}  Horário: {d['data_hora']}")
            
            print(f"\n-----------------------------\nSaques:")
            
            for s in historico_saque:
                print(f"R$ {s['valor']:.2f}  Horário: {s['data_hora']}")

            print(f"""\n-----------------------------\nSaldo:\nR$ {saldo:.2f}""")


    elif opcao == "A":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
