import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fredapi import Fred 
import datetime as dt
import streamlit as st

pd.set_option('display.max_rows', 300)

plt.style.use('fivethirtyeight')

api_key = '3a746e21f01402deac293eb18069b69d'

start = dt.date(2020,7,1)

fred = Fred(api_key=api_key)

home_price_index = fred.get_series('CSUSHPINSA', start)
hpi= pd.DataFrame(home_price_index)
hpi.columns = ['Home Price Index']

existing_home_sales = fred.get_series('EXHOSLUSM495S', dt.date(2023,7,1))
existing_df = pd.DataFrame(existing_home_sales)
#existing_df.columns = ["Homes Sold"]
existing_df.rename(columns={'0': 'Home Sales'})






b_permits = fred.get_series('PERMIT', start)
permits_df= pd.DataFrame(b_permits)
permits_df.columns=['Building Permits']


mortgage_rates= fred.get_series('MORTGAGE30US', start)
mortgage_rate_df= pd.DataFrame(mortgage_rates)
mortgage_rate_df.columns=['Mortgage Rates']

# Mortgage Rates
fig1, ax1 = plt.subplots()
ax1.plot(mortgage_rate_df)

# Set y-axis limits (adjust these values to fit your data range)
ax1.set_ylim(2, 8)

# Set labels and title
ax1.set_xlabel("Date")
plt.xticks(rotation=45)
ax1.set_ylabel("Mortgage Rate")
ax1.set_title("Mortgage Rates Over Time")

#HPI
fig2, ax2 = plt.subplots()
ax2.plot(hpi)

# Set y-axis limits (adjust these values to fit your data range)
ax2.set_ylim(175, 400)

# Set labels and title
ax2.set_xlabel("Date")
plt.xticks(rotation=45)
ax2.set_ylabel("Index Value")
ax2.set_title("Housing Price Index")


fig3, ax3 = plt.subplots()
ax3.plot(existing_df)

# Set y-axis limits (adjust these values to fit your data range)
ax3.set_ylim(3500000, 4500000)
ax3.set_xlim(dt.date(2023,7,1))

# Set labels and title
ax3.set_xlabel("Date")
plt.xticks(rotation=45)
ax3.set_ylabel("Houses Sold")
ax3.set_title("Existing Home Sales")


fig4, ax4 = plt.subplots()
ax4.plot(b_permits)

# Set y-axis limits (adjust these values to fit your data range)
ax4.set_ylim(1200, 2000)


# Set labels and title
ax4.set_xlabel("Date")
plt.xticks(rotation=45)
ax4.set_ylabel("Permits Issued")
ax4.set_title("Building Permits")

st.title("Economic Indicators")

col1, col2 = st.columns([1,1])

hpi_plot = plt.plot(hpi['Home Price Index'])

col1.html("<br><br>")
col2.write("## Home Price Index")
col2.caption("Description: Tracks changes in the prices of single-family homes in various metropolitan areas.")
col1.write(hpi)
#col2.line_chart (hpi)
col2.pyplot(fig2)
col1.html("<br><br>")
col1.divider()


col2.html("<br><br><br><br><br> ")
col2.write("## Existing Home Sales")
col2.caption("Description: Provides data on the number of existing homes sold in the U.S., which can indicate market activity.")
col1.table(existing_home_sales)
#col2.line_chart(existing_home_sales)
col2.pyplot(fig3)
col1.divider()
col2.html("<br>")


col2.html("<br><br><br><br><BR>")
col2.write("## Building Permits")
col2.caption("Description: Indicates the number of permits issued for new housing units, a leading indicator of future construction.")
col1.html("<br><br>")
col1.write(permits_df)
#col2.line_chart(permits_df)
col2.pyplot(fig4)
col1.html("<br><br>")


col1.html("<br><br><br>")
col2.html("<br><br>")
col2.html("<br><br>")
col2.write("## Mortgage Rates")
col2.caption("#### Description: Provides information on average mortgage rates for a 30-year fixed mortgage, which impacts affordability and market conditions.")
col1.write(mortgage_rate_df)
#col2.line_chart(mortgage_rates)
col2.pyplot(fig1)
