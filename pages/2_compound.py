import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Compound Interest Calculator")

P = st.number_input("What is the initial Investment?  ")
P = float(P)
r = st.number_input("What are you expecting for a return rate?  ") / 100
r = float(r)
compound_period = st.radio("Compound Frequency", options=['Monthly', 'Annually'])
t = st.number_input("How Many Years are we looking at? ")
t = int(t)

def calculate_compound_interest(P, r, n, t):
    data = []
    for year in range(1, t + 1):
        amount = P * (1 + r/n) ** (n * year)
        interest = amount - P
        data.append({"Year": year, "Amount": round(amount, 2), "Interest": round(interest, 2)})
    return data

if st.button("Calculate"):
    if compound_period == 'Monthly':
        n = 12
    else:
        n = 1
    
    A = round((P * (1 + (r/n)) ** (n * t)), 2)
    st.write(f"# \${A:,.2f}")

    # Generate the data for each year
    data = calculate_compound_interest(P, r, n, t)

    # Create a pandas DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame
    st.write("Compound Interest Growth Over Time:")
    st.dataframe(df)

    total_interest_earned = df.iloc[-1]['Interest']
    st.write(f"## Total Interest Earned: \${total_interest_earned:,.2f}")

else:
    st.write("Enter the values and click 'Calculate' to see the results.")
