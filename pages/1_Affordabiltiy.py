import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt

st.title("My Mortgage Calculator App")

col1, col2 = st.columns([1,1])

col1.write("## Income")
# Slider for home price
income = col1.slider("Annual Salary", 100000, 175000, 250000)
col1.write(f"Annual: ${income:,.2f} ")
col1.write(f"Monthly: ${income/12:,.2f}")
twenty_eight = (income/12)*.28
col1.write(f"You can afford up to \\${twenty_eight:,.2f} per month according to the 28\\% Rule")
# Initialize the list in session state if it doesn't exist yet
if "data_list" not in st.session_state:
    st.session_state.data_list = []

# Streamlit input fields
title = col1.text_input("What's your debt?:")
value = col1.number_input("What does it cost per month?:")

# Add input to the list when button is clicked
if col1.button("Save"):
    if title and value:
        st.session_state.data_list.append({"Debt": title, "Value": value})
        col1.write("Data saved!")

# Convert the list to a DataFrame
if st.session_state.data_list:
    debt_df = pd.DataFrame(st.session_state.data_list)
    col1.write(debt_df)

    # Calculate the total debt value
    total_debt = debt_df["Value"].sum()
    col1.write(f"Total Monthly Debt: ${total_debt:,.2f}")
else:
    col1.write("No debt data available.")

col2.write("## House Payment")
home_price = col2.slider("Price", 300000, 700000, 400000)
col2.write(f"Home Price: ${home_price:,.2f}")

# Text input for down payment percentage
downPMT = col2.text_input("What Percent Downpayment do you want to make? (Enter whole number)", "20")
try:
    down_pct = float(downPMT) / 100
except ValueError:
    col2.error("Please enter a valid number for down payment percentage.")
    down_pct = 0

# Calculate total down payment
total_down = round(home_price * down_pct, 2)
col2.write(f"Down Payment: ${total_down:,.2f}")

# Text input for interest rate
interest_rate = col2.text_input("What do you think the interest rate will be? (Enter whole number)", "5")
col2.write(f"Interest Rate: {interest_rate}%")

try:
    interest_rate = float(interest_rate)
except ValueError:
    col2.error("Please enter a valid number for interest rate.")
    interest_rate = 0

loan = float(home_price - (home_price * down_pct))
downPay_sum = f"${float(down_pct * home_price):,.2f}"
pmt = ((interest_rate / 100 / 12) * loan) / (1 - ((1 + (interest_rate / 100 / 12)) ** (-30 * 12)))
pmt = round(pmt, 2)
property_tax = .0087 / 12
insurance = round(2300 / 12, 2)
pmi = round((.0046 * loan) / 12, 2)
pmi_limit = home_price * .8

if down_pct >= .2:
    total_pmt = round(pmt + property_tax + insurance, 2)
    downstatus = "You are not paying PMI"
else:
    total_pmt = round(pmt + property_tax + insurance + pmi, 2)
    downstatus = f"You would be paying PMI, which would be about \\${pmi:,.2f} per month.  You can stop paying PMI after you have \\${pmi_limit:,.2f} remaining on the mortgage"

total_paid = pmt * 30 * 12
total_interest = f"\${total_paid - loan:,.2f}"
col2.write(f"You can expect to pay somewhere around ${total_pmt}")
col2.write(downstatus)

mortgage_results = {
    'Home Price': f"${home_price:,.2f}",
    'Loan Amount': f"${loan:,.2f}",
    'Interest Rate': f"{interest_rate}%",
    'Downpayment %': f"{downPMT}%",
    'Principal': f"${pmt:,.2f}",
    'Downpayment Total': downPay_sum,
    'PMI': f"{pmi:,.2f}",
    'Insurance': f"${insurance:,.2f}",
    'Property Tax': f"${property_tax:,.2f}",
    'Total Payment': f"${total_pmt:,.2f}"
}

def create_df():
    # Create DataFrame with dictionary keys as index
    df = pd.DataFrame(list(mortgage_results.items()), columns=['Feature', 'Value'])
    df.set_index('Feature', inplace=True)
    col2.write(df)

# Button to show details
if col2.button("Show Details"):
    create_df()

st.write(f"# Your total monthly payment would be \\${total_pmt} if you put \{downPay_sum} down and interest rates are at {interest_rate}%")

st.write(f"### In total you would spend \\${total_paid:,.2f} on principal and interest through the life of the loan.  Of that amount, {total_interest} would be spent on interest")

sum_debts = total_debt+total_pmt
percent_sum_debt = sum_debts/(income/12)
st.write(f"Your total monthly debts would be \\${sum_debts:,.2f} which is {percent_sum_debt:,.2f}\\% of your monthly income")

if (income/12) * .36 > sum_debts:
    st.write("You can Afford this according to the 36% Rule")

else:
    st.write("Bitch you broke according to the 36% Rule")


