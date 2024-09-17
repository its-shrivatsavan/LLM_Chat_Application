# Imports
from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import json
from together import Together
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Together.ai client
client = Together(api_key=os.getenv("TOGETHER_TOKEN"))

# Constants
CHAT_HISTORY_FILE = "chat_history.json"
DB_FILE = "client.db"

# ========== Helper Functions ==========
def get_response(question):
    '''
    Function to get response from the LLaMA model using Together.ai
    '''
    model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": """
                    You are a customer support assistant for a retail analytics platform.
                    - For general questions or natural language queries, provide clear and relevant answers.
                    - When a query involves sales data, inventory, or products, create the SQL query for that task and return it.
                      Structure the SQL query so it doesn't contain any irrelevant characters before the statement.
                    - If no SQL query is needed, simply respond with relevant information based on the user's input. Don't pass any SQL statements after it.
                    - SQL database has the following columns: ProductID, ProductName, Category, Price, StockQuantity, SalesLastMonth, Description.
                """
            },
            {"role": "user", "content": question}
        ],
        max_tokens=512,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["</s>"],
    )
    return response.choices[0].message.content


def read_sql_query(sql, db):
    '''
    Function to execute SQL query on SQLite database 
    '''
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except sqlite3.OperationalError as e:
        print(f"SQL error: {e}")
        return None


def load_chat_history():
    '''
    Load chat history from JSON file
    JSONDecodeError -> empty json / decode error
    '''
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
        except Exception as e:
            print(f"Error loading chat history: {e}")
            return []
    return []


def save_chat_history(chat_history):
    '''
    Save chat history to JSON file
    '''
    try:
        with open(CHAT_HISTORY_FILE, "w") as file:
            json.dump(chat_history, file)
    except Exception as e:
        print(f"Error saving chat history: {e}")


def add_message(role, message, response=None):
    '''
    Add a message to the chat history and save it
    '''
    timestamp = datetime.now().isoformat()
    st.session_state.chat_history.append({
        "role": role,
        "message": message,
        "response": response,
        "timestamp": timestamp
    })
    save_chat_history(st.session_state.chat_history)

# ========== Streamlit App Setup ==========


st.set_page_config(page_title="Client's Personal Assistant", page_icon="🤖")
st.title("Client's Personal Assistant")
st.header("Powered by Meta AI")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = load_chat_history()

page = st.sidebar.selectbox("Select Page", ["Chat", "Search History"])

# ========== Chat Page ==========

if page == 'Chat':
    question = st.text_input("Input: ", key="input")
    submit = st.button("Ask")

    if submit:
        response_text = get_response(question)
        add_message('user', question, response_text)

        if response_text.lower().startswith("select"):
            data = read_sql_query(response_text, DB_FILE)

            if data:
                st.subheader("SQL Query Result:")
                for row in data:
                    st.text(row)
            else:
                st.error("No data returned or SQL query was invalid.")
        else:
            st.subheader("Response from Model:")
            st.text(response_text)

# ========== Search History Page ==========

else:
    with st.container():
        st.write("Click the button below to load chat history.")
        search = st.button("Get History")

        if search:
            history = load_chat_history()
            if history:
                st.subheader("Chat History")

                history.sort(key=lambda x: x['timestamp'], reverse=True)

                with st.container():
                    st.write(
                        "<div style='max-height: 400px; overflow-y: scroll;'>"
                        + "".join(
                            f"<div><b>Time</b>: {msg['timestamp']}<br>"
                            f"<b>User</b>: {msg['message']}<br>"
                            f"<b>Response</b>: {msg['response']}</div><br>"
                            for msg in history
                        )
                        + "</div>",
                        unsafe_allow_html=True
                    )

            else:
                st.info("No search history available.")
