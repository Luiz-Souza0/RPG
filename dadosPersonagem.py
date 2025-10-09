# dados personagem
import random 

def gerar_valores_aleatorios(nome):
    Nome = nome
    Atk   = random.randint(1, 18)
    Des   = random.randint(1, 18)
    Car   = random.randint(1, 18)
    Int   = random.randint(1, 18)
    Sab   = random.randint(1, 18)
    Const = random.randint(1, 18)
    
    Atributos = {"Nome":  Nome, "Atk":  Atk, "Des": Des, "Car": Car, "Int": Int, "Sab": Sab, "Const": Const}
    print(Atributos)
    return Raca("Draconato", Atributos)


def Raca(EscolhaRaca, Atributos):
    if(EscolhaRaca == "Draconato"):
        Atributos["Atk"] += 2
        Atributos["Car"] += 2
    if(EscolhaRaca == "Elfo"):
        Atributos["Des"] += 2
        Atributos["Sab"] += 2
    # if(EscolhaRaca == "Humano"):
        # EscolhaAtributo = input("Escolha o atributo que deseja Somar 2 Pontos") Select
        # Atributos["1"] += 2 Rever
    if(EscolhaRaca == "Anao"):
        Atributos["Const"] += 2
        # Atributos["3"] += 2 Rever
    if(EscolhaRaca == "Orc"):
        Atributos["Atk"] += 2
        Atributos["Const"] += 1

    return Atributos

# def Classes():
#     EscolhaClasse = input("assaas")

# # gerar_valores_aleatorios("luiz")
# Classes()
