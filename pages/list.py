import streamlit as st
import mysql.connector
import pandas as pd


mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)

st.header("Get service report")
col1, col2 = st.columns(2)
with col1:
    from_date = st.date_input("From Date", value=None)
with col2:
    to_date = st.date_input("To Date", value=None)

submit = st.button("Get report")    
if submit:
    mycursor = mydb.cursor()
    mycursor.execute("SELECT name, phone_number, address, vehicle_type, brand, model, km_reading, service_date, service_type, payment_mode, amount, remarks   FROM customer_details, service_details WHERE customer_details.customer_id = service_details.customer_id and service_date between %s and %s order by service_date", (from_date, to_date))
    response = mycursor.fetchall()
    total_amount = 0
    for data in response:
        total_amount += int(data[10])
    
    df = pd.DataFrame(response, columns = ['Name', 'Phone Number', 'Address', 'Vehicle Type', 'Brand', 'Model', 'KM Reading', 'Service Date', 'Service Type', 'Payment Mode', 'Amount', 'Remarks'])
    st.dataframe(df, use_container_width=True)
    st.write(f"Total Amount: {total_amount}")
