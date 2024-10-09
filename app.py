import os
import dotenv  
import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import WebBaseLoader

# Carregar variáveis de ambiente
dotenv.load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Configurar o modelo
chat = ChatGroq(model='llama-3.1-70b-versatile')

# Função para gerar a resposta do bot
def resposta_bot(mensagens, documento):
    mensagem_system = '''You're a friendly assistant called Margot.
    You use the following informations to create your anwsers: {informacoes}'''
    mensagens_modelo = [('system', mensagem_system)]
    mensagens_modelo += mensagens
    template = ChatPromptTemplate(mensagens_modelo)
    chain = template | chat
    return chain.invoke({'informacoes': documento}).content

# Função para carregar o conteúdo de um site
def carrega_site(url_site):
    loader = WebBaseLoader(url_site)
    lista_documentos = loader.load()
    documento = ''.join([doc.page_content for doc in lista_documentos])
    return documento

# Inicializar o estado das variáveis
if "documento" not in st.session_state:
    st.session_state.documento = ''
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Interface do Streamlit
st.title('Welcome to Margot!')

# Campo para inserir a URL do site
url_site = st.text_input('Type the URL of the website you want to chat with: ')

if st.button('Load site'):
    if url_site:
        st.session_state.documento = carrega_site(url_site)
        st.success('Loading successful! You can now chat with the bot.')
    else:
        st.error('Please, type the URL of the website you want to chat with.')

# Campo de mensagens para o usuário conversar com o bot, se o site já estiver carregado
if st.session_state.documento:
    pergunta = st.text_input('User:', key='pergunta')
    
    if st.button('Send'):
        if pergunta:
            # Adicionar a pergunta à lista de mensagens
            st.session_state.mensagens.append(('user', pergunta))
            # Gerar a resposta do bot
            resposta = resposta_bot(st.session_state.mensagens, st.session_state.documento)
            st.session_state.mensagens.append(('assistant', resposta))
            # Exibir a resposta do bot
            st.write(f'Margot: {resposta}')
