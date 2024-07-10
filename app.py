import streamlit as st
import requests

# URL do backend Django
BASE_URL = 'http://10.238.75.122:8888/api/'

st.title('Testando a API do Backend Django')

# Formulário para criar um novo usuário
st.header('Criar Novo Usuário')
username = st.text_input('Username')
email = st.text_input('Email')
password = st.text_input('Password', type='password')

if st.button('Criar Usuário'):
    response = requests.post(
        BASE_URL + 'users/',
        json={'username': username, 'email': email, 'password': password}
    )
    if response.status_code == 201:
        st.success('Usuário criado com sucesso!')
    else:
        st.error('Erro ao criar usuário: ' + response.text)

# Formulário para autenticação do usuário
st.header('Autenticação do Usuário')
auth_username = st.text_input('Auth Username')
auth_password = st.text_input('Auth Password', type='password')

if st.button('Autenticar'):
    auth_response = requests.post(
        BASE_URL + 'token/',
        json={'username': auth_username, 'password': auth_password}
    )
    if auth_response.status_code == 200:
        token = auth_response.json().get('access')
        st.success('Autenticado com sucesso!')
        st.write('Token de Acesso:', token)
    else:
        st.error('Erro na autenticação: ' + auth_response.text)
