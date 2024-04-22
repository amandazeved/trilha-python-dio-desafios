from abc import ABC, abstractmethod
from datetime import datetime
import datetime
import textwrap 

class Conta:
    def __init__(self, numero, cliente, agencia="0001"):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()
    
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
        
    @classmethod
    def nova_conta(cls, numero, cliente, agencia="0001"):
        return cls(numero, cliente, agencia)
    
    def sacar(self, valor):
        if valor > self._saldo:
            print("=> Operação Falhou: Saldo insuficiente.")
            return False
        elif valor < 0:
            print("=> Operação Falhou: valor de saque negativo.")
            return False

        self._saldo -= valor
        print("=> Saque realizado com sucesso.")
        return True
    
    def depositar(self, valor):
        if valor < 0:
            print("=> Operação Falhou: valor de depósito negativo.")
            return False
    
        self._saldo += valor
        print("=> Depósito realizado com sucesso.")
        return True
    
    def __str__(self):
        return textwrap.dedent(f"""
            Conta:
                Agência: {self.agencia}
                C/C: {self.numero}
                Titular: {self.cliente.nome}
        """)


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, agencia="0001", limite=500, limite_saque=3):
        super().__init__(numero, cliente, agencia)
        self._limite = limite
        self._limite_saque = limite_saque

    def sacar(self, valor):
        saques_feitos = 0
        if "Saque" in self.historico.transacoes:
            saques_feitos = len([transacoes for transacoes in self.historico.transacoes["Saque"]])
        
        if valor > self._saldo:
            print("=> Operação Falhou: Saldo insuficiente.")
            return False
        elif valor > self._limite:
            print(f"=> Operação Falhou: valor de saque maior que o limte de R$ {self._limite:.2f}")
            return False
        elif valor < 0:
            print(f"=> Operação Falhou: valor de saque negativo.")
            return False
        elif saques_feitos+1 > self._limite_saque:
            print(f"=> Operação Falhou: limite de {self._limite_saque} saques no dia excedeu.")
            return False

        self._saldo -= valor
        print("=> Saque realizado com sucesso.")
        return True

class Historico:
    def __init__(self) -> None:
        self._transacoes = {}

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao, tipo):
        if tipo not in self._transacoes:
            self._transacoes[tipo] = []

        self._transacoes[tipo].append(transacao)

    def __str__(self):
        if len(self._transacoes) == 0:
            return "Não houve transações."
        return f"{self.__class__.__name__}:\n" + '\n'.join([str(item) for valor in self._transacoes.values() for item in valor])
        
    
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta): 
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.datetime.now()
    
    @property
    def valor(self):
        return self._valor
    
    @property
    def data(self):
        return self._data
    
    def registrar(self, conta):
        tipo = "Deposito"
        transacao = conta.depositar(self._valor)
        
        if transacao:
            conta.historico.adicionar_transacao(self, tipo)

        
        
    def __str__(self):
        return f"Depósito: R$ {self._valor:.2f} {self._data.strftime('%d/%m/%Y %H:%M')}"

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.datetime.now()

    @property
    def valor(self):
        return self._valor
    
    @property
    def data(self):
        return self._data
    
    def registrar(self, conta):
        tipo = "Saque"
        transacao = conta.sacar(self._valor)
        
        if transacao:
            conta.historico.adicionar_transacao(self, tipo)
        
    def __str__(self) -> str:
        return f"Saque: R$ {self._valor:.2f} {self._data.strftime('%d/%m/%Y %H:%M')}"
    

class Cliente:
    def __init__(self, endereco) -> None:
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf =cpf
        self.data_nascimento = data_nascimento

    def __str__(self):
        return textwrap.dedent(f"""
            Nome: {self.nome}
            CPF: {self.cpf}
            Data de nascimento: {self.data_nascimento}
            Endereço: {self._endereco}
        """)
    


