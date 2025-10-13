import streamlit as st
import pymongo
import bcrypt
import re
from pymongo import MongoClient
import random 


USAR_BANCO = False  

if USAR_BANCO:
    client = MongoClient("mongodb+srv://<usuario>:<senha>@cluster0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.get_database()  
    usuarios_collection = db.usuarios 

def verificar_senha(senha_digitada, senha_armazenada):
    senha_digitada_bytes = senha_digitada.encode('utf-8') 
    if isinstance(senha_armazenada, str):
        senha_armazenada_bytes = senha_armazenada.encode('utf-8')
    else:
        senha_armazenada_bytes = senha_armazenada
    # st.write(bcrypt.hashpw(senha_digitada_bytes, bcrypt.gensalt()).decode('utf-8'))
    # st.write(senha_armazenada_bytes)
    return bcrypt.checkpw(senha_digitada_bytes, senha_armazenada_bytes)


def autenticar(usuario, senha):
    if USAR_BANCO:
        usuario_db = usuarios_collection.find_one({"usuario": usuario})
        
        if usuario_db and verificar_senha(senha, usuario_db['senha']):
            return True
    else:
        usuarios_validos = {
            'admin': '$2b$12$0KAriYRof2by7h1.0mlkeeMTUliZcKv6L05houe4JE8JSIkw5Khii',  
            'jogador': '$2b$12$0KAriYRof2by7h1.0mlkeeMTUliZcKv6L05houe4JE8JSIkw5Khii',
        }
        
        if usuario in usuarios_validos and verificar_senha(senha, usuarios_validos[usuario]):
            return True

    return False

def criar_usuario(usuario, senha):
    senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    
    if USAR_BANCO:
        usuarios_collection.insert_one({"usuario": usuario, "senha": senha_criptografada})
        st.success(f"UsuÃ¡rio {usuario} criado com sucesso no banco de dados!")
    else:
        st.success(f"UsuÃ¡rio {usuario} criado com sucesso (mas nÃ£o salvo no banco de dados).")

def validar_senha(senha):
    if len(senha) < 8:
        return False, "A senha deve ter no mÃ­nimo 8 caracteres."
    if not re.search(r'[A-Z]', senha):
        return False, "A senha deve conter pelo menos uma letra maiÃºscula."
    if not re.search(r'[0-9]', senha):
        return False, "A senha deve conter pelo menos um nÃºmero."
    if not re.search(r'[@$!%*?&]', senha):
        return False, "A senha deve conter pelo menos um caractere especial (@, $, !, %, *, ?, &)."
    return True, "Senha vÃ¡lida"

def tela_login():
    st.title('Tela de Login')
    
    usuario = st.text_input('UsuÃ¡rio')
    senha = st.text_input('Senha', type='password')
    
    if st.button('Entrar'):
        if usuario and senha:
            if autenticar(usuario, senha):
                st.session_state['usuario'] = usuario
                st.success(f'Bem-vindo, {usuario}!')
                return True
            else:
                st.error('UsuÃ¡rio ou senha incorretos!')
        else:
            st.warning('Por favor, preencha ambos os campos!')
    
    return False

def tela_registro():
    st.title('Registro de UsuÃ¡rio')
    
    novo_usuario = st.text_input('Nome de usuÃ¡rio')
    nova_senha = st.text_input('Senha', type='password')
    confirmar_senha = st.text_input('Confirmar Senha', type='password')
    
    if st.button('Criar Conta'):
        if novo_usuario and nova_senha and confirmar_senha:
            senha_valida, mensagem = validar_senha(nova_senha)
            if senha_valida:
                if nova_senha == confirmar_senha:
                    if USAR_BANCO and usuarios_collection.find_one({"usuario": novo_usuario}):
                        st.error("UsuÃ¡rio jÃ¡ existe. Escolha outro nome.")
                    else:
                        criar_usuario(novo_usuario, nova_senha)
                else:
                    st.error("As senhas nÃ£o coincidem!")
            else:
                st.error(mensagem)
        else:
            st.warning("Preencha todos os campos!")

def main():
    
    if 'autenticado' not in st.session_state:
        st.session_state['autenticado'] = False
    if 'Atributos' not in st.session_state:
        st.session_state['Atributos'] = None
    if 'usuario' not in st.session_state:
        st.session_state['usuario'] = None
        
    st.sidebar.title("Opções")
    
    if st.session_state['autenticado'] == False:
        escolha = st.sidebar.radio("Escolha uma opção", ("Login", "Registrar"))
        tipo = ""
    else:
        st.sidebar.write(f"Logado como: {st.session_state['usuario']}")
        tipo =  st.sidebar.radio("O que deseja ver?", ("Monstros","Ficha"))
        if st.sidebar.button("Sair"):
            st.session_state['autenticado'] = False
            st.session_state['Atributos'] = None
            st.session_state['usuario'] = None
            st.rerun()
        escolha = "Área Protegida"
    if tipo == "Monstros":
        from TelaMonstros import Monstros
        st.write("monstros")
    elif escolha == "Login":
        if not st.session_state['autenticado'] or st.session_state['autenticado'] == False:
            if tela_login():
                st.session_state['autenticado'] = True
                st.rerun()
    elif escolha == "Registrar":
            tela_registro()
    elif escolha == "Área Protegida":
        if st.session_state['autenticado']:
            st.title('Área Protegida - Criação de Personagem')

        if st.session_state['autenticado']:
            if 'Atributos' not in st.session_state or st.session_state['Atributos'] == None:
                st.session_state['Atributos'] = None
                
                from dadosPersonagem import gerar_valores_aleatorios

                NomePersonagem = st.text_input('Nome do Personagem', key='NomePersonagem')
                if NomePersonagem:
                    Raca = st.selectbox("Raca", ['None','Draconato', 'Elfo', 'Humano', 'Anao', 'Orc'], index=0, key='RacaPersonagem')
                    if Raca != 'None':
                        Classe = st.selectbox('Classe', ['None','Guerreiro', 'Mago', 'Ferreiro', 'Arqueiro'], index=0, key='ClassePersonagem')
                        if Classe != 'None':
                            Atributos = gerar_valores_aleatorios(NomePersonagem, Classe, Raca)
                            if Atributos != None: 
                                if (st.button("Salvar")):
                                    Atributos['Inventario'] = []
                                    st.session_state['Atributos'] = Atributos
                                    st.write(Atributos)
                                    print("Atributos front ")
                                    print(Atributos)
                                    st.rerun()
            else :
                from ExibirPersonagemCriado import exibir_personagem_criado
                exibir_personagem_criado()


if __name__ == "__main__":
    main()
