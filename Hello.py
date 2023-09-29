import streamlit as st
import mysql.connector
import pandas as pd
import requests
import re

def is_valid_email(email):
    # Implemente sua própria validação de formato de e-mail aqui, se necessário
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None
#

def is_phone_number_exists(number, cursor):
    sql = "SELECT * FROM users WHERE number = %s"
    val = (number,)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    return result is not None

def add_userdata(name, email, number, password):
    sql = "INSERT INTO users (name, email, number, problema,cod_matricula) VALUES (%s, %s, %s, %s, %s)"
    val = (name, email, number, problema, cod_matricula)
    cursor.execute(sql, val)
    con.commit()

con = mysql.connector.connect(
    host=st.secrets["db"]["host"],
    user=st.secrets["db"]["user"],
    password=st.secrets["db"]["password"],
    database=st.secrets["db"]["database"],
)

cursor = con.cursor()

st.markdown("""
    <style>
    body {
        background-color: #000000;
    }
    .stTextInput input {
        transition: all 0.3s ease;
    }
    .stTextInput input:focus {
        border-color: #4d90fe;
        box-shadow: inset 0 1px 1px rgba(0,0,0,0.075),0 0 8px rgba(77,144,254,0.6);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Registro de dados Cliente Technos")
name = st.text_input('Nome')
email = st.text_input('Email')
number = st.text_input('Numero')
problema = st.text_input('Problema')
cod_matricula = st.text_input('Cod. Matricula')


#hunter_api_key = "YOUR_HUNTER_API_KEY"  # Substitua pelo seu Hunter API Key

if st.button('Enviar dados'):
    if not name or not email or not number or not problema or not cod_matricula:
        st.error("Preencha todos os campos")
    elif not is_valid_email(email):
        st.error("Please enter a valid email address.")
    #elif not is_email_valid_hunter(email, hunter_api_key):
     #   st.error("The email address does not exist.")
    elif is_phone_number_exists(number, cursor):
        st.error("The phone number already exists.")
    else:
        try:
            add_userdata(name, email, number, problema)
            st.success("registro concluido")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def get_all_data():
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    return result

if st.checkbox('Ver todos os dados enviados'):
    try:
        data = get_all_data()
        if data:
            for row in data:
                st.write(f'ID: {row[0]}, Nome: {row[1]}, Email: {row[2]}, Numero: {row[3]}, Problema: {row[4]}, Cod. Matricula: {row[5]}')
        else:
            st.write("Nenhum dado enviado ainda.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")

def delete_user_by_id(user_id):
    sql = "DELETE FROM users WHERE id = %s"
    val = (user_id,)
    cursor.execute(sql, val)
    con.commit()

user_id_to_delete = st.text_input('ID do usuário para deletar')

if st.button('Deletar usuário'):
    if not user_id_to_delete:
        st.error("Por favor, insira um ID de usuário")
    else:
        try:
            delete_user_by_id(user_id_to_delete)
            st.success("Usuário deletado com sucesso")
        except Exception as e:
            st.error(f"Ocorreu um erro: {str(e)}")

if st.button('Gerar planilha'):
    try:
        data = get_all_data()
        if data:
            # Criando um DataFrame com os dados
            df = pd.DataFrame(data, columns=['ID', 'Nome', 'Email', 'Numero', 'Problema', 'Cod. Matricula'])
            # Salvando o DataFrame como um arquivo .csv
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download da planilha",
                data=csv,
                file_name='users.csv',
                mime='text/csv',
            )
            st.success("Planilha gerada com sucesso")
        else:
            st.write("Nenhum dado enviado ainda.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")

con.close()
