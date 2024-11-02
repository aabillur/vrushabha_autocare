import streamlit as st
import mysql.connector
import pandas as pd


mydb = mysql.connector.connect(
  host="vrushabhaautocare.cl8kaee80img.eu-north-1.rds.amazonaws.com",
  user="vrushabha",
  password="vrushabhaautocare",
  database="vrushabhaautocare"
)

def insert_customer_details(name, phone_number, email, address, notification):
    mycursor = mydb.cursor()
    sql = "INSERT INTO customer_details (name, phone_number, email, address, notification) VALUES (%s, %s, %s, %s, %s)"
    val = (name, phone_number, email, address, notification)
    mycursor.execute(sql, val)
    mydb.commit()
    return mycursor.lastrowid

st.header("Vrushabha Auto care")

def insert_service_details(customer_id, vehicle_type, brand, model, km_reading, service_date, service_type, payment_mode, amount, remarks = "NA"):
    mycursor = mydb.cursor()
    sql = "INSERT INTO service_details (customer_id, vehicle_type, brand, model, km_reading, service_date, service_type, payment_mode, amount, remarks) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (customer_id, vehicle_type, brand, model, km_reading, service_date, service_type, payment_mode, amount, remarks)
    mycursor.execute(sql, val)
    mydb.commit()
    return mycursor.lastrowid


with st.form("my_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input('Customer Name')
        brand = st.selectbox(
            "Car Brand",
            ("FORD", "TATA", "TOYOTA", "HONDA", "HYUNDAI", "MARUTI", "MAHINDRA", "RENAULT", "VOLKSWAGEN", "SKODA", "NISSAN", "KIA", "MG", "JEEP", "BMW", "AUDI", "MERCEDES", "JAGUAR", "LAND ROVER", "PORSCHE", "LEXUS", "VOLVO", "TESLA", "ROLLS ROYCE", "BENTLEY", "ASTON MARTIN", "FERRARI", "LAMBORGHINI", "BUGATTI", "MASERATI", "ALFA ROMEO", "MCLAREN", "LOTUS", "KOENIGSEGG", "SSC", "PAGANI", "ZENVO"),
            index=None,
            placeholder="Select car brand...",
        )
        service_type = st.selectbox(
            "Service Type",
            ("Washing", "Wheel Alignment", "Wheel Balancing", "Type Exchange", "Nitrogen Air", "Car Accessories", "Others"),
            index=None,
            placeholder="Select service type...",
        )
        payment_mode = st.selectbox(
            "Payment Mode",
            ("Cash", "Card", "UPI", "Others"),
            index=None,
            placeholder="Select payment mode...",
        )

    with col2:
        phonenumber = st.text_input('Phone number')
        car_model = st.text_input('Select Car Model')
        remarks = st.text_input('Remarks')
        amount = st.number_input('Amount', value=0)

    with col3:
        address = st.text_input('Address')
        km_reading = st.text_input('KM Reading')
        service_date = st.date_input("Service Date", value=None)
        
    # send message and email to owner
    send_whatsapp_message = st.toggle("Send Whatsapp Message")
    st.toggle("Notify Owner")

    submitted = st.form_submit_button("Submit")
    if submitted:
        customer_id = insert_customer_details(name, phonenumber, "NA", "NA", send_whatsapp_message)
        service_id = insert_service_details(customer_id, "CAR", brand, car_model, km_reading, service_date, service_type, payment_mode, amount, remarks)
        st.write("Service details added successfully", service_id)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT name, phone_number, address, vehicle_type, brand, model, km_reading, service_date, service_type, payment_mode, amount, remarks   FROM customer_details, service_details WHERE customer_details.customer_id = service_details.customer_id order by service_date desc limit 1")
        myresult = mycursor.fetchall()
        df = pd.DataFrame(myresult, columns = ['Name', 'Phone Number', 'Address', 'Vehicle Type', 'Brand', 'Model', 'KM Reading', 'Service Date', 'Service Type', 'Payment Mode', 'Amount', 'Remarks'])
        st.dataframe(df, use_container_width=True)
    

# preview = st.button('Preview')     
# st.button('Send daily report')      
# if preview:
#     mycursor = mydb.cursor()
#     mycursor.execute("SELECT name, phone_number, address, vehicle_type, brand, model, km_reading, service_date, service_type, payment_mode, amount, remarks   FROM customer_details, service_details WHERE customer_details.customer_id = service_details.customer_id order by service_date desc 1")
#     myresult = mycursor.fetchall()
#     df = pd.DataFrame(myresult, columns = ['Name', 'Phone Number', 'Address', 'Vehicle Type', 'Brand', 'Model', 'KM Reading', 'Service Date', 'Service Type', 'Payment Mode', 'Amount', 'Remarks'])
#     st.dataframe(df, use_container_width=True)
#     # for x in myresult:
    #     st.write(x)
