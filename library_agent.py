import sqlite3
import re
import pandas as pd
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="LibraryGenie AI Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Dark High-Contrast Boxes & Blue Gradient Background ---
st.markdown("""
    <style>
    /* Main App Background - Deep Blue Gradient Accents */
    .stApp {
        background: linear-gradient(135deg, #040711 0%, #071022 50%, #0c1a36 100%);
        color: #f3f4f6;
    }
    
    /* Hero Banner - Vibrant Multi-Color Spectrum (Red, Orange, Gold, Purple) */
    .hero-card {
        background: linear-gradient(135deg, #7c3aed 0%, #dc2626 35%, #ea580c 70%, #f59e0b 100%);
        padding: 2.5rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 25px -5px rgba(234, 88, 12, 0.3);
        border: 2px solid #fbbf24;
    }
    .hero-card h1 {
        color: #ffffff;
        font-weight: 800;
        font-size: 2.4rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    .hero-card p {
        color: #fef3c7;
        font-size: 1.15rem;
    }

    /* Metric Containers - Very Dark & High Contrast for White Text */
    div[data-testid="metric-container"] {
        background-color: #080c14;
        border: 1px solid #1e293b;
        padding: 1rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.7);
    }
    div[data-testid="metric-container"] label {
        color: #f59e0b !important; /* Gold Label */
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #ffffff !important; /* Crisp Bright White Value */
    }
    
    /* Action Buttons - Fiery & Gold Gradient */
    .stButton>button {
        background: linear-gradient(135deg, #ea580c 0%, #dc2626 50%, #7c3aed 100%);
        color: white;
        border-radius: 0.5rem;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1rem;
        transition: all 0.25s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #c2410c 0%, #b91c1c 50%, #6d28d9 100%);
        color: #ffffff;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.5);
        transform: translateY(-2px);
    }

    /* Sidebar Styling - Deep Charcoal Black */
    section[data-testid="stSidebar"] {
        background-color: #04060b;
        border-right: 1px solid #111827;
    }
    
    /* Input Fields - Dark Box for High Contrast Text */
    .stTextInput>div>div>input {
        background-color: #080c14;
        color: #ffffff;
        border: 1px solid #1e293b;
        border-radius: 0.5rem;
        padding: 0.75rem;
    }
    .stTextInput>div>div>input:focus {
        border-color: #f59e0b;
        box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.25);
    }
    
    /* Expander Styling - Dark Neutral Box */
    .streamlit-expanderHeader {
        background-color: #080c14;
        border-radius: 0.5rem;
        border: 1px solid #1e293b;
        color: #fbbf24 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Configuration ---
st.sidebar.markdown("### ⚙️ System Configuration")
api_key_input = st.sidebar.text_input("Groq API Key", type="password", placeholder="gsk_...")

if api_key_input:
    client = Groq(api_key=api_key_input)
else:
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception:
        client = None

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 About LibraryGenie")
st.sidebar.info("LibraryGenie translates natural language (English & Roman Urdu) into secure, read-only SQL queries.")

def run_query(sql_query):
    conn = sqlite3.connect('library.db')
    try:
        df = pd.read_sql_query(sql_query, conn)
        return df, None
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()

def is_safe_query(sql_query):
    cleaned_query = sql_query.strip().lower()
    cleaned_query = re.sub(r"^```sql\s*", "", cleaned_query)
    cleaned_query = re.sub(r"^```\s*", "", cleaned_query)
    cleaned_query = re.sub(r"\s*```$", "", cleaned_query).strip()
    
    if not cleaned_query.startswith("select"):
        return False, "Only SELECT queries are allowed for security reasons."
    
    forbidden_keywords = ["insert", "update", "delete", "drop", "alter", "truncate", "create", "replace"]
    for word in forbidden_keywords:
        if re.search(r'\b' + word + r'\b', cleaned_query):
            return False, f"Unsafe operation detected: '{word}' is not permitted."
            
    return True, cleaned_query

def generate_sql_from_natural_language(user_prompt):
    schema_info = """
    Table Name: books
    Columns:
    - book_id (INTEGER, Primary Key)
    - title (TEXT)
    - author (TEXT)
    - category (TEXT) - Values: 'Science', 'Technology', 'Literature', 'History'
    - available_copies (INTEGER)
    - times_borrowed (INTEGER)
    """
    
    system_prompt = f"""
    You are an expert SQLite database assistant for a school library. 
    Translate the user's natural language question into a valid SQL SELECT query.
    Database Schema:\n{schema_info}
    Rules: 
    1. Return ONLY the raw SQL query without markdown code blocks or extra text. Strictly SELECT statements only.
    2. Capitalize category values properly (e.g., WHERE category = 'Science').
    """
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1
    )
    
    sql_text = response.choices[0].message.content.strip()
    sql_text = re.sub(r"^```sql\s*", "", sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r"^```\s*", "", sql_text)
    sql_text = re.sub(r"\s*```$", "", sql_text).strip()
    return sql_text

def generate_ai_explanation(user_prompt, sql_query, df_results):
    summary_data = df_results.head(10).to_string() if not df_results.empty else "No results found."
    
    system_prompt = """
    You are LibraryGenie, a friendly AI school library assistant. 
    Detect the language of the user's question:
    - If the user's question is in **English**, reply in professional **English**.
    - If the user's question is in **Roman Urdu**, reply strictly in **Roman Urdu** and always start your response with the greeting **"Salam!"**.
    Keep your explanation clear, polite, and concise.
    """
    
    user_content = f"""
    User Question: {user_prompt}
    SQL Executed: {sql_query}
    Result Summary:
    {summary_data}
    
    Provide a polite explanation matching the user's language style (English or Roman Urdu with "Salam!").
    """
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# --- Hero Header ---
st.markdown("""
    <div class="hero-card">
        <h1>📚 LibraryGenie AI Assistant</h1>
        <p>Explore your school library database effortlessly using natural language in English or Roman Urdu.</p>
    </div>
""", unsafe_allow_html=True)

if not client:
    st.warning("⚠️ Please input your **Groq API Key** in the sidebar to activate the assistant.")
else:
    try:
        conn = sqlite3.connect('library.db')
        total_books_df = pd.read_sql_query("SELECT COUNT(*) as total, SUM(times_borrowed) as borrows FROM books", conn)
        total_cat_df = pd.read_sql_query("SELECT COUNT(DISTINCT category) as cats FROM books", conn)
        conn.close()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Catalog Books", int(total_books_df['total'][0]))
        m2.metric("Total Lifetime Borrowings", int(total_books_df['borrows'][0]))
        m3.metric("Book Categories", int(total_cat_df['cats'][0]))
    except Exception:
        pass

    st.markdown("---")
    st.markdown("### ⚡ Quick Test Questions")
    col_q1, col_q2, col_q3 = st.columns(3)
    
    selected_preset = None
    if col_q1.button("📊 How many books are in the library?", use_container_width=True):
        selected_preset = "How many books are in the library?"
    if col_q2.button("🔥 Show the 5 most borrowed books.", use_container_width=True):
        selected_preset = "Show the 5 most borrowed books."
    if col_q3.button("🧪 Science category mein kitni books hain?", use_container_width=True):
        selected_preset = "Science category mein kitni books hain?"

    st.markdown("<br>", unsafe_allow_html=True)
    user_question = st.text_input("💬 Ask your library question:", value=selected_preset if selected_preset else "", placeholder="e.g., Which books have zero available copies?")

    if user_question:
        with st.spinner("✨ Genie is translating and querying the database..."):
            try:
                raw_sql = generate_sql_from_natural_language(user_question)
                is_safe, cleaned_sql = is_safe_query(raw_sql)
                
                if not is_safe:
                    st.error(f"❌ Safety Violation: {cleaned_sql}")
                else:
                    df_res, db_error = run_query(cleaned_sql)
                    
                    if db_error:
                        st.error(f"Database Error: {db_error}")
                    else:
                        explanation = generate_ai_explanation(user_question, cleaned_sql, df_res)
                        
                        st.markdown("### ✨ Results & Analysis")
                        st.info(f"**🤖 AI Explanation:**\n\n{explanation}")
                        st.markdown("#### 📋 Query Result Table")
                        st.dataframe(df_res, use_container_width=True)
                        
                        col_info, col_sql = st.columns([1, 1])
                        with col_info:
                            st.markdown("🏷️ **Source Label:** `books` table")
                        with col_sql:
                            with st.expander("🔍 Inspect Generated SQL Query"):
                                st.code(cleaned_sql, language="sql")
                                
            except Exception as e:
                st.error(f"An error occurred: {e}")

    st.markdown("---")
    st.markdown("### 📈 Library Analytics Hub")
    tab1, tab2 = st.tabs(["📊 Category Borrowings", "📦 Stock Availability"])
    
    conn = sqlite3.connect('library.db')
    try:
        with tab1:
            chart_df = pd.read_sql_query("SELECT category, SUM(times_borrowed) as total_borrowings FROM books GROUP BY category", conn)
            if not chart_df.empty:
                chart_df.set_index("category", inplace=True)
                st.bar_chart(chart_df, color="#ea580c")
        with tab2:
            stock_df = pd.read_sql_query("SELECT category, SUM(available_copies) as available_stock FROM books GROUP BY category", conn)
            if not stock_df.empty:
                stock_df.set_index("category", inplace=True)
                st.bar_chart(stock_df, color="#f59e0b")
    except Exception:
        st.info("Run create_library_db.py first.")
    finally:
        conn.close()