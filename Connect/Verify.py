import streamlit as st
from supabase import create_client, Client
import bcrypt
import re

# ==============================================
# CONFIGURAÇÃO DO SUPABASE
# ==============================================
SUPABASE_URL = "https://rybuyxuxivizlfpxesoe.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ5YnV5eHV4aXZpemxmcHhlc29lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEzMjc0OTAsImV4cCI6MjA3NjkwMzQ5MH0.dYsT3jwJ7xvKNBAOGmRzxibAGzz776amwgfm-m4TSPA"
USAR_BANCO = True  # ativar Supabase

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if USAR_BANCO else None


# ==============================================
# FUNÇÕES DE AUTENTICAÇÃO
# ==============================================
def verificar_senha(senha_digitada, senha_armazenada):
    senha_digitada_bytes = senha_digitada.encode('utf-8')
    if isinstance(senha_armazenada, str):
        senha_armazenada_bytes = senha_armazenada.encode('utf-8')
    else:
        senha_armazenada_bytes = senha_armazenada
    return bcrypt.checkpw(senha_digitada_bytes, senha_armazenada_bytes)


def autenticar(usuario, senha):
    if USAR_BANCO:
        response = supabase.table("usuarios").select("*").eq("usuario", usuario).execute()
        dados = response.data
        if dados and verificar_senha(senha, dados[0]['senha']):
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
    senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    if USAR_BANCO:
        # Verifica se já existe
        ja_existe = supabase.table("usuarios").select("usuario").eq("usuario", usuario).execute()
        if ja_existe.data:
            st.error("Usuário já existe. Escolha outro nome.")
        else:
            supabase.table("usuarios").insert({"usuario": usuario, "senha": senha_criptografada}).execute()
            st.success(f"Usuário {usuario} criado com sucesso no Supabase!")
    else:
        st.success(f"Usuário {usuario} criado com sucesso (mas não salvo no banco).")


# ==============================================
# VALIDAÇÃO DE SENHA
# ==============================================
def validar_senha(senha):
    if len(senha) < 8:
        return False, "A senha deve ter no mínimo 8 caracteres."
    if not re.search(r'[A-Z]', senha):
        return False, "A senha deve conter pelo menos uma letra maiúscula."
    if not re.search(r'[0-9]', senha):
        return False, "A senha deve conter pelo menos um número."
    if not re.search(r'[@$!%*?&]', senha):
        return False, "A senha deve conter pelo menos um caractere especial (@, $, !, %, *, ?, &)."
    return True, "Senha válida"


# ==============================================
# TELAS STREAMLIT
# ==============================================
def tela_login():
    st.title('Tela de Login')

    usuario = st.text_input('Usuário')
    senha = st.text_input('Senha', type='password')

    if st.button('Entrar'):
        if usuario and senha:
            if autenticar(usuario, senha):
                st.session_state['usuario'] = usuario
                st.success(f'Bem-vindo, {usuario}!')
                return True
            else:
                st.error('Usuário ou senha incorretos!')
        else:
            st.warning('Por favor, preencha ambos os campos!')

    return False


def tela_registro():
    st.title('Registro de Usuário')

    novo_usuario = st.text_input('Nome de usuário')
    nova_senha = st.text_input('Senha', type='password')
    confirmar_senha = st.text_input('Confirmar Senha', type='password')

    if st.button('Criar Conta'):
        if novo_usuario and nova_senha and confirmar_senha:
            senha_valida, mensagem = validar_senha(nova_senha)
            if senha_valida:
                if nova_senha == confirmar_senha:
                    criar_usuario(novo_usuario, nova_senha)
                else:
                    st.error("As senhas não coincidem!")
            else:
                st.error(mensagem)
        else:
            st.warning("Preencha todos os campos!")
