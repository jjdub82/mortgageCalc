import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Compound Interest Calculator")

# Inputs
P = st.number_input("What is the initial Investment?  ", step= 1000.00, min_value=0.0, value=10000.0)
P = float(P)
r = st.number_input("What are you expecting for a return rate?  (%)", min_value=0.0, value=7.0) / 100
r = float(r)
compound_period = st.radio("Compound Frequency", options=['Monthly', 'Annually'])
t = st.number_input("How Many Years are we looking at? ", min_value=0, value=30)
t = int(t)
additions = st.number_input("Do you plan to make an annual or monthly contribution?", step= 100.0, min_value=0.0, value=0.0)

def calculate_compound_interest(P, r, n, t, additions):
    data = []
    amount = P
    for year in range(1, t + 1):
        # Compound the amount for the current year
        amount = amount * (1 + r/n) ** n
        # Add contributions for the current year
        amount += additions
        # Calculate interest
        interest = amount - (P + additions * year)
        data.append({"Year": year, "Amount": round(amount, 2), "Interest": round(interest, 2)})
    return data

if st.button("Calculate"):
    if compound_period == 'Monthly':
        n = 12
    else:
        n = 1
    
    # Generate the data for each year
    data = calculate_compound_interest(P, r, n, t, additions)

    # Create a pandas DataFrame
    df = pd.DataFrame(data)

    st.write(f"## Your investment will have grown to \${df.iloc[-1]['Amount']:,.2f} by end of all this")

    df['YOY Growth'] = df["Amount"] - df['Amount'].shift(1)
    df['% YOY Growth'] = round(df['YOY Growth']/df['Amount'].shift(1) ,2)
    df['% YOY Growth'] = df['% YOY Growth'].apply(lambda x: f"{x *100:,.2f}%")

    df['Cumulative Growth'] =  df['Amount'] - df.iloc[0]['Amount']
    df['% Cumulative'] = round(df['Cumulative Growth']/df.iloc[0]['Amount'] ,2)
    df['% Cumulative'] = df['% Cumulative'].apply(lambda x: f"{x * 100:.2f}%")


   
    

    # Display the DataFrame
    st.write("Compound Interest Growth Over Time:")
    st.dataframe(df)

    # Total Interest Earned
    total_interest_earned = df.iloc[-1]['Interest']
    st.write(f"## Total Interest Earned: \${total_interest_earned:,.2f}")

else:
    st.write("Enter the values and click 'Calculate' to see the results.")
