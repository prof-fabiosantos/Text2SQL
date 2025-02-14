import streamlit as st
import os
from langchain.chains import create_sql_query_chain
from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase

# Configuração do Streamlit
st.title("Consulta de Banco de Dados via Linguagem Natural")
st.write("Faça upload de um banco de dados SQLite e faça perguntas usando linguagem natural.")

# Upload do banco de dados
uploaded_file = st.file_uploader("Faça o upload do banco de dados (.db)", type=["db"])

if uploaded_file is not None:
    # Salvar o banco de dados temporariamente
    db_path = os.path.join("db", uploaded_file.name)
    with open(db_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Conectar ao banco de dados
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    
    # Configurar o LLM
    llm = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")
    chain = create_sql_query_chain(llm, db)
    
    # Entrada do usuário
    user_question = st.text_input("Digite sua pergunta:")
    if st.button("Consultar"):
        if user_question:
            response = chain.invoke({"question": user_question})
            st.subheader("Resposta:")
            st.write(response)
        else:
            st.warning("Por favor, digite uma pergunta.")
