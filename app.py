import streamlit as st
import requests
import pandas as pd
server_loc="http://127.0.0.1:8000"
st.title("💰 Expense Tracker Application")
menu = st.sidebar.selectbox(
    "choose:",
    ["➕ Add_expenses", "📋view_expenses","✏️update_expenses","🗑️Delete_expenses",
     "🔍Search_expenses","📊Sort_expenses","🔽filter_expenses","📈Analyse_expenses"],
    key="menu"
)
if menu == "➕ Add_expenses":
    st.header("➕Add Expense")

    title = st.text_input("enter expense title")
    amount = st.number_input("enter amount", min_value=0.0, step=50.0)

    category = st.selectbox(
        "select category type",
        ["food", "travel", "shopping", "entertainment", "other"]
    )

    if st.button("add expense"):

        expense_data = {
            "title": title,
            "amount": amount,
            "category": category
        }

        response = requests.post(
            f"{server_loc}/add_expense",
            json=expense_data
        )

        st.write("STATUS:", response.status_code)
        st.write("TEXT:", response.text)

        if response.status_code == 200:
            st.success("Expense added successfully")

if menu=="📋view_expenses":
    if st.button("📋ViewExpenses"):
        response=requests.get(f"{server_loc}/ViewExpenses")
        all_expenses=response.json()
        pd_df=pd.DataFrame(all_expenses)
        st.dataframe(pd_df)
        if menu=="update_expenses":
           st.header("updateExpenses")
           expense_id = st.number_input("Enter Expense ID",min_value=1,step=1)

    title = st.text_input("Enter New Title")
    amount=st.number_input("enter amount",min_value=0.0,step=50.0)
    category=st.selectbox("select category type",["food","travel","shopping","entertainment","other"])

if menu=="✏️update_expenses":
    st.header("✏️updateExpenses")
    expense_id = st.number_input("Enter Expense ID",min_value=1,step=1)

    title = st.text_input("Enter New Title")
    amount=st.number_input("enter amount",min_value=0.0,step=50.0)
    category=st.selectbox("select category type",["food","travel","shopping","entertainment","other"])

    if st.button("updateExpenses"):
        expense_data={
            "title":title,
            "amount":amount,
            "category":category
        }
        response=requests.put(f"{server_loc}/update_expense/{expense_id}", json=expense_data)
        if response.status_code==200:
            st.success(response.json())
        else:
            st.error(response.text)
elif menu == "🗑️Delete_expenses":

    st.header("🗑️Delete Expenses")

    expense_id = st.number_input(
        "Enter Expense ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Expense"):

        response = requests.delete(
            f"{server_loc}/delete_expenses/{expense_id}"
        )

        if response.status_code == 200:
            st.success("Expense Deleted Successfully")

        else:
            st.error(response.text)
if menu=="🔍Search_expenses":
    st.header("s🔍earch expenses")
    category=st.selectbox("choose category:--",["food","travel","shopping","entertainment","other"])
    if st.button("search expense"):
       response= requests.get(f"{server_loc}/search_expenses?category={category}")
       if response.status_code==200:
           searched_data=response.json()
           pd_df=pd.DataFrame(searched_data)
           st.dataframe(pd_df)
       else:
           st.success(response.text)
if menu=="📊Sort_expenses":
    st.header("📊sort_expenses")
    order=st.selectbox("choose sorting_order:",["low_to_high","high_to_low"])
    if st.button("sort_order"):
      response=requests.get(f"{server_loc}/sort_expenses?order={order}")
      if response.status_code==200:
         sorted_data=response.json()
         pd_df=pd.DataFrame(sorted_data)
         st.dataframe(pd_df)
      else:
        st.success(response.text)
if menu=="🔽filter_expenses":
    st.header("🔽filter_expenses")
    amount=st.number_input("choose amount:-",min_value=0.0,step=20.0)
    if st.button("filter expenses"):
        response=requests.get(f"{server_loc}/filter_expenses?amount={amount}")
        if response.status_code==200:
            filtered_data=response.json()
            pd_df=pd.DataFrame(filtered_data)
            st.dataframe(pd_df)
        else:
            st.success(response.text)
if menu=="📈Analyse_expenses":
    st.header("📈Analysing_expenses")
    response=requests.get(f"{server_loc}/ViewExpenses")
    if response.status_code==200:
        all_expenses=response.json()
        pd_df=pd.DataFrame(all_expenses)
        st.dataframe(pd_df)

        st.line_chart( data=pd_df,y="amount")
    else:
        st.success(response.text)
    