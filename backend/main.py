from fastapi import FastAPI
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
import os
app = FastAPI()



# ======================================================
# CORS POLICY
# ======================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Allow All Frontends
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, PUT, DELETE
    allow_headers=["*"]
)

# -------------------- DB Connection --------------------
conn = mysql.connector.connect(
    host=os.getenv("db_host"),
    user=os.getenv("db_user"),
    password=os.getenv("db_password"),
    database=os.getenv("db_name"),
    port=int(os.getenv("db_port"))
)

cursor = conn.cursor(dictionary=True)



# -------------------- Create Table --------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200),
    amount FLOAT,
    category VARCHAR(100),
    payment_method VARCHAR(100),
    expense_date DATE,
    description TEXT
)
""")

conn.commit()

@app.get("/")
def home():

    return {
        "message": "API Running Successfully"
    }

# -------------------- Add Expense --------------------
@app.post("/add_expense")
def add_expense(payload: dict):

    query = """
    INSERT INTO expenses
    (title, amount, category, payment_method, expense_date, description)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    values = (
        data["title"],
        data["amount"],
        data["category"],
        data["payment_method"],
        data["expense_date"],
        data["description"]
    )

    cursor.execute(query, values)
    conn.commit()

    return {
        "message": "Expense Added Successfully"
    }


# -------------------- Get All Expenses --------------------
@app.get("/get_expenses")
def get_expenses():

    query = """
    SELECT *
    FROM expenses
    ORDER BY expense_id DESC
    """

    cursor.execute(query)

    data = cursor.fetchall()

    return {
        "expenses": data
    }


