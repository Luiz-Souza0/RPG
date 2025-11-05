# dados personagem
import random 
import streamlit as st
def gerar_valores_aleatorios(nome, Classe, RacaEscolhida):
    Nome = nome
    Atk   = random.randint(1, 18)
    Des   = random.randint(1, 18)
    Car   = random.randint(1, 18)
    Int   = random.randint(1, 18)
    Sab   = random.randint(1, 18)
    Const = random.randint(1, 18)
    
    Atributos = {"Nome":  Nome}
    Atributos["Classe"] = Classe
    Atributos["Raca"] = RacaEscolhida
    Atributos.update({"Atk": Atk, "Des": Des, "Car": Car, "Int": Int, "Sab": Sab, "Const": Const})
    return Raca(Atributos)


def Raca(Atributos):
    if(Atributos["Raca"] == "Draconato"):
        Atributos["Atk"] += 2
        Atributos["Car"] += 2
        return Classes(Atributos)
    if(Atributos["Raca"] == "Elfo"):
        Atributos["Des"] += 2
        Atributos["Sab"] += 2
        return Classes(Atributos)
    if(Atributos["Raca"] == "Humano"):
        EscolhaAtributo = st.selectbox('Escolha Qual Atributo Deseja Aumentar', [None,'Atk','Des', 'Car', 'Int', 'Sab', 'Const'], index=0)
        if EscolhaAtributo != None:
            print("Atributos antes da escolha")
            print(Atributos)
            Atributos[EscolhaAtributo] += 2 
            print(EscolhaAtributo)
            return Classes(Atributos)
    if(Atributos["Raca"] == "Anão"):
        Atributos["Const"] += 2
        # Atributos["3"] += 2 Rever
        return Classes(Atributos)
    if(Atributos["Raca"] == "Orc"):
        Atributos["Atk"] += 2
        Atributos["Const"] += 1
        return Classes(Atributos)


def Classes(Atributos):
    if(Atributos["Classe"] == "Guerreiro"):
        Atributos["Atk"] += 2
        Atributos["Car"] += 2
    if(Atributos["Classe"] == "Elfo"):
        Atributos["Des"] += 2
        Atributos["Sab"] += 2
    # if(Classe == "Humano"):
        # EscolhaAtributo = input("Escolha o atributo que deseja Somar 2 Pontos") Select
        # Atributos["1"] += 2 Rever
    if(Atributos["Classe"] == "Anao"):
        Atributos["Const"] += 2
        # Atributos["3"] += 2 Rever
    if(Atributos["Classe"] == "Orc"):
        Atributos["Atk"] += 2
        Atributos["Const"] += 1

    Nivel = 1
    Atributos.update({"Nivel": Nivel })        
    print("Atributos")
    print(Atributos)
    return Atributos

# # gerar_valores_aleatorios("luiz")
# Classes()
