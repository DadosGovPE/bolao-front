import streamlit as st
import requests

# URL do backend Django
BASE_URL = 'http://10.238.75.122:8888/api/'

# Função para criar novo usuário
def criar_usuario():
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

# Função para autenticação do usuário
def autenticar_usuario():
    st.header('Autenticação do Usuário')
    username = st.text_input('Auth Username')
    password = st.text_input('Auth Password', type='password')
    
    if st.button('Autenticar'):
        auth_response = requests.post(
            BASE_URL + 'token/',
            json={'username': username, 'password': password}
        )
        if auth_response.status_code == 200:
            token = auth_response.json().get('access')
            st.session_state['auth_token'] = token
            st.session_state['authenticated'] = True
            st.session_state['username'] = username  # Guardar username na sessão
            st.success('Autenticado com sucesso!')
        else:
            st.error('Erro na autenticação: ' + auth_response.text)

# Função para listar jogos e fazer apostas
def pagina_de_apostas():
    st.header('Página de Apostas')
    
    if 'auth_token' not in st.session_state:
        st.error('Você precisa estar autenticado para ver esta página.')
        return
    
    token = st.session_state['auth_token']
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Obter apostas existentes do usuário
    bets_response = requests.get(BASE_URL + 'bets/', headers=headers)
    if bets_response.status_code == 200:
        existing_bets = bets_response.json()
        # Filtrar apostas pelo usuário logado
        bets_dict = {bet['game']['id']: bet for bet in existing_bets if bet['user']['username'] == st.session_state['username']}
    else:
        bets_dict = {}
        st.error('Erro ao carregar apostas: ' + bets_response.text)
    
    # Listar jogos
    games_response = requests.get(BASE_URL + 'games/', headers=headers)
    if games_response.status_code == 200:
        games = games_response.json()
        st.subheader('Jogos Disponíveis')
        for game in games:
            game_id = game['id']
            team1_score = 0
            team2_score = 0
            button_class = "secondary"

            # Preencher os campos se a aposta já existir para o usuário logado
            if game_id in bets_dict:
                existing_bet = bets_dict[game_id]
                team1_score = existing_bet['team1_score']
                team2_score = existing_bet['team2_score']
                button_class = "primary"

            cols = st.columns([3, 1, 1, 3, 3, 5], vertical_alignment='center')
            with cols[0]:
                st.markdown(f"<div style='text-align: right;'>{game['team1']['name']}</div>", unsafe_allow_html=True)
            with cols[1]:

                team1_score_input = st.number_input(label=" ", min_value=0, step=1, value=team1_score, key=f"{game['id']}_team1", label_visibility="collapsed")
            with cols[2]:
                team2_score_input = st.number_input(label=" ", min_value=0, step=1, value=team2_score, key=f"{game['id']}_team2", label_visibility="collapsed")
            with cols[3]:
                st.markdown(f"<div style='text-align: left;'>{game['team2']['name']}</div>", unsafe_allow_html=True)
            with cols[4]:
                st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
                if st.button('Apostar', type=button_class, key=f"{game['id']}_button"):
                    bet_response = requests.post(
                        BASE_URL + 'bets/',
                        headers=headers,
                        json={
                            'game_id': game['id'],
                            'team1_score': team1_score_input,
                            'team2_score': team2_score_input
                        }
                    )
                    if bet_response.status_code == 201 or bet_response.status_code == 200:
                        with cols[5]:
                            st.success('Palpite salvo com sucesso!')
                    else:
                        with cols[5]:
                            st.error('Erro ao salvar palpite: ' + bet_response.text)
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error('Erro ao carregar jogos: ' + games_response.text)

# Menu de navegação
st.sidebar.title('Navegação')
pagina = st.sidebar.radio('Ir para', ['Autenticação', 'Criar Usuário', 'Página de Apostas'])

# Controle de navegação
if pagina == 'Autenticação':
    autenticar_usuario()
elif pagina == 'Criar Usuário':
    criar_usuario()
elif pagina == 'Página de Apostas':
    pagina_de_apostas()
