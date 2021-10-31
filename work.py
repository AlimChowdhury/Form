import mysql.connector as mysql
import pandas as pd
import time
from datetime import datetime
from PIL import Image
import json
import base64
import yagmail
import re
from re import search

import streamlit as st
import streamlit.components.v1 as components
from streamlit import caching

import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sqlalchemy import create_engine
from mysql.connector.constants import ClientFlag
#from db_connection import get_database_connection
# from search_members import get_all_members


st.set_page_config(
    page_title="Payslip Distribution",
    page_icon=":dolphin:",
    layout="wide",
    initial_sidebar_state="expanded",
)

def get_database_connection():
     db = mysql.connect( host = "localhost",
                        user = "root",
                       passwd = "1234",
                       database = "PayslipDB",
                       auth_plugin='mysql_native_password')
     cursor = db.cursor()

     cursor.execute("SHOW DATABASES")
     databases=cursor.fetchall()
     print(databases)
    # st.write(databases)

     return cursor, db

cursor, db = get_database_connection()
cursor.execute("SHOW DATABASES")
databases=cursor.fetchall()

#cursor.execute('''CREATE TABLE members (id int AUTO_increment PRIMARY KEY,
#                                     name varchar(255),
#                                      nickname varchar(255),
#                                       email varchar(255),
#                                       dept varchar(255),
#                                       status varchar(255),
#                                       joining_date date,
#                                       account_number varchar(255),
#                                       gross_salary int)''')

cursor.execute("show tables from PayslipDB")
tables = cursor.fetchall()
st.write(tables)

def member_register():
    with st.form(key='member_form'):
        name = st.text_input('Full Name')
        email = st.text_input('Email')
        status = st.selectbox('Status', ('Probationary', 'Permanent'))
        joining_date = st.date_input('Joining Date')
        account_number = st.text_input('Account Number')
        gross_salary = st.text_input('Gross Salary')
        
        if st.form_submit_button('Submit'):
            member_query = '''INSERT INTO members (name, email, status, 
                                            joining_date, account_number, gross_salary) 
                                    VALUES (%s, %s, %s, %s, %s, %s)'''
            member_values = (name, email, status, joining_date, account_number, gross_salary)
            cursor.execute(member_query, member_values)
            db.commit()
            st.success(f'{name} info inserted successfully')
            
    
    member_select_option = st.selectbox('Search Member', ('----------','All Member List', 'Search a single member?'))
    
    if member_select_option == 'Search a single member?':
        search_member = st.text_input('Enter the employee full name')
        
        cursor.execute("Select name, status, gross_salary from members")
        members = cursor.fetchall()

        member_found_flag = False
        
        for m in members:
            if search_member == m[0]:
                st.success('Hurrah! the employee is already registered')
                st.write(m)
                member_found_flag = True
                break

        if member_found_flag == False:
            st.warning('Sorry, not available.')

        # st.write(members)

    elif member_select_option == 'All Member List':
        cursor.execute('SELECT id, name, email, status, gross_salary from members')
        all_members = cursor.fetchall()

        st.write(all_members)


def driver():
     st.write('pain')

username = st.sidebar.text_input('Username','Enter Your E-mail',key='user')
password = st.sidebar.text_input("Enter a password",type="password",key='pass')

st.session_state.login = st.sidebar.checkbox('Log In')

if st.session_state.login:
      if username.split('@')[-1] == "gmail.com" and password == "12":
         driver()
         st.sidebar.warning('ok')

      else:
         member_register()
         st.sidebar.warning('error')
