import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import random

plt.style.use('fivethirtyeight')

st.title("Monte Carlo Simulations")
st.caption("Look at this High Roller")

# Inputs
P = st.number_input("What is the initial Investment?  ", step= 1000.00, min_value=0.0, value=10000.0)
P = float(P)
r = st.number_input("What are you expecting for a return rate?  (%)", min_value=0.0, value=7.0)
r = float(r)
sd = st.number_input("Enter a REASONABLE standard deviation percentage", step = 1.0, min_value=1.0, value= 15.0)
compound_period = st.radio("Compound Frequency", options=['Monthly', 'Annually'] )
t = st.number_input("How Many Years are we looking at? ", min_value=0, value=30)
t = int(t)
additions = st.number_input("Do you plan to make an annual or monthly contribution?", step= 100.0, min_value=0.0, value=0.0)

beat_return = st.number_input("What return output are you trying to beat?  ", step = 0.5, min_value = 1.0)
beat_dollar = st.number_input("Is there a dollar amount you ar trying to beat? ", step = 1000.0)

def calculate_compound_interest(P, r, sd, t, additions):
    data = []
    amount = P
    r = r/100
    sd = sd/100

    for year in range(1, t + 1):
        # Generate random return rate
        annual_r = norm.rvs(loc=r, scale=sd)
        #annual_r = random.normalvariate(r,sd)
    
        #annual_r = norm(loc=r, scale=sd)/100
        # Compound the amount for the current year
        amount = amount * (1 + annual_r)
        # Add contributions for the current year
        amount += additions
        # Calculate interest
        interest = amount - (P + additions * year)
        data.append({
            "Year": year,
            "Amount": round(amount, 2),
            "Interest": round(interest, 2),
            "Return": round(annual_r, 4)
        })
    return data

if st.button("Calculate"):
    if compound_period == 'Monthly':
        n = 12
    else:
        n = 1
    
    # Generate the data for each year
    data = calculate_compound_interest(P, r, n, t, additions)

    sim_list = []
    for i in range(0,1000):
        sim = calculate_compound_interest(P,r,n,t,additions)
        outcome = sim[-1]
        sim_list.append(outcome)

    
    sim_df=pd.DataFrame(sim_list)

    hist = sim_df['Amount'].plot.hist(bins=100)

    fig1, ax1 = plt.subplots()
    ax1.tick_params(axis='x', labelsize=8) 
    ax1.hist(sim_df['Amount'], bins=100)
    plt.xticks(rotation=45) 
    plt.show()

  
    fig2,ax2 = plt.subplots()
   # fig2, ax2 = plt.subplots()
    ax2.tick_params(axis='x', labelsize=8) 
    ax2.hist(sim_df['Return'], bins=100)
    plt.xticks(rotation=45) 
    plt.show()

    
    percentiles = [i/20 for i in range (1,20)]

    dollar_success = (sim_df['Amount'] >= beat_dollar).astype(int).mean()
    st.write(f"You have a {dollar_success} \\% change of success")

    probs = pd.DataFrame(sim_df['Amount'].quantile(percentiles))

    

    st.table(probs)


    st.write(sim_df['Amount'].describe())

    st.write(fig2)

    st.write(fig1)


    # Create a pandas DataFrame
    df = pd.DataFrame(data)

    st.write(f"## Your investment will have grown to \${df.iloc[-1]['Amount']:,.2f} by end of all this")

    df['YOY Growth'] = df["Amount"] - df['Amount'].shift(1)
    df['% YOY Growth'] = round(df['YOY Growth']/df['Amount'].shift(1) ,2)
    df['% YOY Growth'] = df['% YOY Growth'].apply(lambda x: f"{x *100:,.2f}%")

    df['Cumulative Growth'] =  df['Amount'] - df.iloc[0]['Amount']
    df['% Cumulative'] = round(df['Cumulative Growth']/df.iloc[0]['Amount'] ,2)
    df['% Cumulative'] = df['% Cumulative'].apply(lambda x: f"{x * 100:.2f}%")

    st.write("Compound Interest Growth Over Time:")


     # Total Interest Earned
    total_interest_earned = df.iloc[-1]['Interest']
    st.write(f"## Total Interest Earned: \${total_interest_earned:,.2f}")
    
    st.dataframe(df)

    st.table(sim_df)
    # Display the DataFrame
   
    
  

else:
    st.write("Enter the values and click 'Calculate' to see the results.")

    
