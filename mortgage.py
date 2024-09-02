import sqlite3

def mortgage_calc():
    home_price = int(input("What do you want to spend? "))
    downPMT = int(input('What percent downpayment? ')) / 100
    loan = home_price - (downPMT * home_price)
    interest_rate = float(input("What do you expect for an interest rate? "))
    loan_term = 30
    pmt = ((interest_rate / 100 / 12) * loan) / (1 - ((1 + (interest_rate / 100 / 12)) ** (-30 * 12)))
    property_tax = .0087 / 12
    insurance = round(2300 / 12, 2)
    pmi = round((.0046 * loan) / 12, 2)
    
    if downPMT >= .2:
        total_pmt = round(pmt + property_tax + insurance, 2)
        downstatus = "You are not paying PMI"
    else:
        total_pmt = round(pmt + property_tax + insurance + pmi,2)
        downstatus = f"You would be paying PMI, which would be about ${pmi}/month."
    
    mortgage_results = {
        'home_price': home_price,
        'loan': loan,
        'interest_rate': interest_rate,
        'total_pmt': total_pmt,
        'downpayment': downPMT,
        'downpayment_amt': downPMT * home_price,
        'PMI': pmi,
        'Insurance': insurance
    }
    
    # Save results to the database
    save_to_db(mortgage_results)

def save_to_db(mortgage_results):
    conn = sqlite3.connect('mortgage_results.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mortgage_results (
        home_price INTEGER,
        loan REAL,
        interest_rate REAL,
        total_pmt REAL,
        downpayment REAL,
        downpayment_amt REAL,
        PMI REAL,
        Insurance REAL
    )
    ''')
    
    # Insert new result
    cursor.execute('''
    INSERT INTO mortgage_results (home_price, loan, interest_rate, total_pmt, downpayment, downpayment_amt, PMI, Insurance)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (mortgage_results['home_price'], mortgage_results['loan'], mortgage_results['interest_rate'], mortgage_results['total_pmt'], mortgage_results['downpayment'], mortgage_results['downpayment_amt'], mortgage_results['PMI'], mortgage_results['Insurance']))
    
    conn.commit()
    conn.close()

# Run the calculator
mortgage_calc()
