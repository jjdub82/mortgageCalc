
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



st.title("Compound Interest Calculator")

P = st.number_input("What is the initial Investment?  ")
P = float(P)
r = st.number_input("What are you expecting for a return rate?  ")/100
r = float(r)
compound_period = st.radio("Compound Frequency",options=['Monthly', 'Annually'])
t = st.number_input("How Many Years are we looking at? ")


if compound_period == 'Monthly':
    n = 12
else:
    n = 1
    
A = round((P*(1+(r/n))**(n*t)),2)
st.write(f"# {A}")