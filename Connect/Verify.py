import streamlit as st
from supabase import create_client, Client
import bcrypt
import re

# ==============================================
# CONFIGURAÇÃO DO SUPABASE
# ==============================================
SUPABASE_URL = "https://rybuyxuxivizlfpxesoe.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ5YnV5eHV4aXZpemxmcHhlc29lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEzMjc0OTAsImV4cCI6MjA3NjkwMzQ5MH0.dYsT3jwJ7xvKNBAOGmRzxibAGzz776amwgfm-m4TSPA"
USAR_BANCO = True

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


def criar_usuario(usuario, senha, role="player"):
    senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    if USAR_BANCO:
        ja_existe = supabase.table("usuarios").select("usuario").eq("usuario", usuario).execute()
        if ja_existe.data:
            st.error("Usuário já existe. Escolha outro nome.")
        else:
            supabase.table("usuarios").insert({"usuario": usuario, "senha": senha_criptografada, "role" : role}).execute()
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
    cargo = ["player", "master"]
    novo_usuario = st.text_input('Nome de usuário')
    nova_senha = st.text_input('Senha', type='password')
    confirmar_senha = st.text_input('Confirmar Senha', type='password')
    if(st.text_input("senha de mestre da sala") == "RpgFichaLuAnd123"):
        cargo.append("admin")
    role = st.selectbox('Selecione o papel do usuário', cargo)

    if st.button('Criar Conta'):
        if novo_usuario and nova_senha and confirmar_senha:
            senha_valida, mensagem = validar_senha(nova_senha)
            if senha_valida:
                if nova_senha == confirmar_senha:
                    criar_usuario(novo_usuario, nova_senha, role=role)
                else:
                    st.error("As senhas não coincidem!")
            else:
                st.error(mensagem)
        else:
            st.warning("Preencha todos os campos!")

def insert_register(register: dict, table: str):
    """
    Insere um novo registro em uma tabela do Supabase.

    Args:
        register (dict): Dicionário com os dados a inserir. Ex: {"usuario": "joao", "senha": "1234"}
        table (str): Nome da tabela.
    """
    try:
        if not USAR_BANCO:
            st.warning("Banco de dados desativado. Registro não inserido.")
            return None

        response = supabase.table(table).insert(register).execute()

        if response.data:
            st.success(f"Registro inserido com sucesso na tabela '{table}'.")
            return response.data
        else:
            st.error(f"Falha ao inserir registro na tabela '{table}'.")
            return None
    except Exception as e:
        st.error(f"Erro ao inserir registro: {e}")
        return None


def alter_register(regid: int, updates: dict, table: str):
    """
    Altera um registro existente no Supabase.

    Args:
        regid (int): ID do registro a ser alterado.
        updates (dict): Dicionário com os campos e novos valores. Ex: {"senha": "nova_senha"}
        table (str): Nome da tabela.
    """
    try:
        if not USAR_BANCO:
            st.warning("Banco de dados desativado. Alteração não salva.")
            return None

        response = supabase.table(table).update(updates).eq("id", regid).execute()

        if response.data:
            st.success(f"Registro {regid} atualizado com sucesso na tabela '{table}'.")
            return response.data
        else:
            st.error(f"Nenhum registro encontrado com ID {regid} para atualizar.")
            return None
    except Exception as e:
        st.error(f"Erro ao atualizar registro: {e}")
        return None

def select_register(table: str, filter: dict = None, columns="*"):
    """
    Seleciona registros do Supabase aplicando filtros dinâmicos.

    Args:
        table (str): Nome da tabela.
        filter (dict, opcional): Dicionário com filtros. Chaves com valor False ou None são ignoradas.
        columns (list ou str, opcional): Lista de campos ou "*" para todos.
    
    Returns:
        list ou None: Lista de registros encontrados ou None se não existir.
    """
    try:
        if not USAR_BANCO:
            st.warning("Banco de dados desativado. Consulta não realizada.")
            return None

        # Se columns for lista, converte para string separada por vírgula
        if isinstance(columns, list):
            columns = ",".join(columns)

        query = supabase.table(table).select(columns)

        # Aplica filtros apenas se não forem False/None
        if filter:
            for key, value in filter.items():
                if value is not False and value is not None:
                    query = query.eq(key, value)

        response = query.execute()

        if response.data:
            st.success(f"{len(response.data)} registro(s) selecionado(s) na tabela '{table}'.")
            return response.data  # retorna lista de dicionários
        else:
            st.warning(f"Nenhum registro encontrado na tabela '{table}'.")
            return None

    except Exception as e:
        st.error(f"Erro ao consultar registro: {e}")
        return None

def delete_register(table: str, filter: dict):
    """
    Exclui registros do Supabase com base em filtros dinâmicos.

    Args:
        table (str): Nome da tabela.
        filter (dict): Dicionário com filtros. Ex: {"id": 5} ou {"usuario": "admin"}.

    Returns:
        list ou None: Lista de registros excluídos (se o Supabase retornar) ou None se nada for excluído.
    """
    try:
        if not USAR_BANCO:
            st.warning("Banco de dados desativado. Exclusão não realizada.")
            return None

        query = supabase.table(table).delete()

        # Aplica filtros (somente se tiverem valor válido)
        if filter:
            for key, value in filter.items():
                if value is not False and value is not None:
                    query = query.eq(key, value)

        response = query.execute()

        if response.data:
            st.success(f"{len(response.data)} registro(s) excluído(s) da tabela '{table}'.")
            return response.data
        else:
            st.warning(f"Nenhum registro encontrado na tabela '{table}' para exclusão.")
            return None

    except Exception as e:
        st.error(f"Erro ao excluir registro: {e}")
        return None

