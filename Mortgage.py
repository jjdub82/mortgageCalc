import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt

st.title("My Mortgage Calculator App")

# Slider for home price
home_price = st.slider("Price", 300000, 700000, 400000)
st.write(f"Home Price: ${home_price:,.2f}")

# Text input for down payment percentage
downPMT = st.text_input("What Percent Downpayment do you want to make? (Don't worry about the symbol, enter the whole number)", "20")
try:
    down_pct = float(downPMT) / 100
except ValueError:
    st.error("Please enter a valid number for down payment percentage.")
    down_pct = 0

# Calculate total down payment
total_down = round(home_price * down_pct, 2)
st.write(f"Down Payment: ${total_down:,.2f}")

# Text input for interest rate
interest_rate = st.text_input("What do you think the interest rate will be? (Just enter the whole number)", "5")
st.write(f"Interest Rate: {interest_rate}%")

try:
    interest_rate = float(interest_rate)
except ValueError:
    st.error("Please enter a valid number for interest rate.")
    interest_rate = 0

loan = float(home_price - (home_price * down_pct))
downPay_sum = f"${float(down_pct * home_price):,.2f}"
pmt = ((interest_rate / 100 / 12) * loan) / (1 - ((1 + (interest_rate / 100 / 12)) ** (-30 * 12)))
pmt = round(pmt, 2)
property_tax = .0087 / 12
insurance = round(2300 / 12, 2)
pmi = round((.0046 * loan) / 12, 2)


if down_pct >= .2:
    total_pmt = round(pmt + property_tax + insurance, 2)
    downstatus = "You are not paying PMI"
else:
    total_pmt = round(pmt + property_tax + insurance + pmi, 2)
    downstatus = f"You would be paying PMI, which would be about ${pmi}/month."

total_paid = pmt*30*12
total_interest = f"${total_paid - loan:,.2f}"
st.write(f"You can expect to pay somewhere around ${total_pmt}")
st.write(downstatus)

mortgage_results = {
    'Home Price': f"${home_price:,.2f}",
    'Loan Amont': f"${loan:,.2f}",
    'Interest Rate': f"{interest_rate}%",
    'Downpayment %': f"{downPMT}%",
    'Principal': f"${pmt:,.2f}",
    'Downpayment Total': downPay_sum,
    'PMI': f"{pmi:,.2f}",
    'Insurance': f"${insurance:,.2f}",
    'Propert Tax': f"${property_tax:,.2f}"
    'Total Payment': f"${total_pmt:,.2f}"
}

def create_df():
    # Create DataFrame with dictionary keys as index
    df = pd.DataFrame(list(mortgage_results.items()), columns=['Feature', 'Value'])
    df.set_index('Feature', inplace=True)
    st.write(df)

# Button to show details
if st.button("Show Details"):
    create_df()

st.write(f"# Your total monthly would be \${total_pmt} if you put \{downPay_sum} down and interest rates are at {interest_rate}%")

st.write(f"### In total you would spend \${total_paid:,.2f} on principal and interest through the life of the loan.  Of that amount, \{total_interest} would be spent on interest")

schedule = []
remaining_balance = loan
monthly_interest_rate = (interest_rate/100)/12

for i in range(1, 30*12 +1):
    interest_payment = remaining_balance *monthly_interest_rate
    principal_payment = pmt - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i/12)
    schedule.append(
        [
            i,
            pmt,
            principal_payment,
            interest_payment,
            remaining_balance,
            year
        ]
    )

schedule_df = pd.DataFrame(schedule, columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"])

st.write("### Payment Schedule")
payments_df = schedule_df[['Year', 'Remaining Balance']].groupby('Year').min()
st.line_chart(payments_df)
st.table(payments_df)
