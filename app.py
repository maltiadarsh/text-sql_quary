from dotenv import load_dotenv #type:ignore
import streamlit as st #type:ignore
import os
import sqlite3
import google.generativeai as genai #type:ignore

# ------------------------------------------------------------
# 1️⃣ Load environment variables
# ------------------------------------------------------------
load_dotenv()  # load .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ------------------------------------------------------------
# 2️⃣ Function: Generate SQL query using Gemini
# ------------------------------------------------------------
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

# ------------------------------------------------------------
# 3️⃣ Function: Execute SQL query and fetch results
# ------------------------------------------------------------
def read_sql_query(sql, db):
    try:
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
        return rows
    except sqlite3.Error as e:
        st.error(f"❌ Database error: {e}")
        return None

# ------------------------------------------------------------
# 4️⃣ Prompt for Gemini model
# ------------------------------------------------------------
prompt = [
    """
    You are an expert in converting natural language (English) questions into valid SQL queries.

    The SQL database name is STUDENT and it contains a single table called STUDENT 
    with the following columns:
    - NAME (VARCHAR)
    - CLASS (VARCHAR)
    - SECTION (VARCHAR)
    - MARKS (INTEGER)

    Rules:
    1. Always return only the SQL query — no explanations, comments, or extra text.
    2. Do not include the words 'SQL', 'Query', or code formatting symbols (like ```).
    3. Follow standard SQLite syntax.

    Examples:
    Example 1:
    Question: How many records are present?
    SQL: SELECT COUNT(*) FROM STUDENT;

    Example 2:
    Question: Tell me all the students studying in Data Science class.
    SQL: SELECT * FROM STUDENT WHERE CLASS = "Data Science";

    Example 3:
    Question: Show the names and marks of students with marks greater than 85.
    SQL: SELECT NAME, MARKS FROM STUDENT WHERE MARKS > 85;
    """
]

from dotenv import set_key #type:ignore

# ------------------------------------------------------------
# 5️⃣ Streamlit App UI (Enhanced with API Key Input)
# ------------------------------------------------------------
st.set_page_config(page_title="Gemini SQL Assistant", page_icon="🤖")
st.header("🤖 Gemini App to Retrieve SQL Data")

# --- API Key input section ---
st.subheader("🔑 Google API Key Configuration")

env_path = ".env"
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    st.success("✅ API key loaded from .env")
else:
    st.warning("⚠️ No API key found in .env. Please enter one below.")

# Input box for API key
user_api_key = st.text_input("Enter your Google API Key:", type="password")

# Button to save API key
if st.button("💾 Save API Key"):
    if user_api_key.strip():
        set_key(env_path, "GOOGLE_API_KEY", user_api_key.strip())
        os.environ["GOOGLE_API_KEY"] = user_api_key.strip()
        genai.configure(api_key=user_api_key.strip())
        st.success("✅ API key saved successfully to .env and configured!")
    else:
        st.error("Please enter a valid API key.")


# --- Option to generate a new key ---
st.markdown(
    """
    🔐 **Don't have a Google API key?**
    - You can generate one instantly from [Google AI Studio](https://aistudio.google.com/app/api-keys).
    - After generating it, copy and paste it above.
    """
)

st.markdown("---")

# --- SQL Assistant Section ---
st.subheader("💬 Ask your question about the Student database:")

question = st.text_input("For example:", placeholder="Show all students with marks above 85")

if st.button("🚀 Run Query"):
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Please configure your Google API key first.")
    elif not question.strip():
        st.warning("Please enter a question.")
    else:
        # Step 1: Generate SQL query using Gemini
        sql_query = get_gemini_response(question, prompt)
        st.subheader("🧠 Generated SQL Query")
        st.code(sql_query, language="sql")

        # Step 2: Execute the SQL query
        data = read_sql_query(sql_query, "student.db")

        # Step 3: Show results
        if data:
            st.subheader("📊 Query Results")
            for row in data:
                st.write(row)
        else:
            st.warning("No data found or invalid query.")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + Google Gemini + SQLite")



