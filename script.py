import pandas as pd # type: ignore
import sqlite3

# Step 1: Connect to the SQLite database
db_connection = sqlite3.connect('shipping_data.db')
cursor = db_connection.cursor()

# Step 2: Load the spreadsheets using pandas
spreadsheet_0 = pd.read_excel('spreadsheet_0.xlsx')
spreadsheet_1 = pd.read_excel('spreadsheet_1.xlsx')
spreadsheet_2 = pd.read_excel('spreadsheet_2.xlsx')

# Step 3: Insert data from Spreadsheet 0 into the database
def insert_spreadsheet_0():
    for _, row in spreadsheet_0.iterrows():
        cursor.execute('''
            INSERT INTO shipments (shipping_id, product_name, quantity, origin, destination)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['shipping_id'], row['product_name'], row['quantity'], row['origin'], row['destination']))
    db_connection.commit()

insert_spreadsheet_0()

# Step 4: Combine Spreadsheet 1 and 2 based on shipping identifier
combined_data = pd.merge(spreadsheet_1, spreadsheet_2, on='shipping_id', how='inner')

# Step 5: Insert data from combined spreadsheets into the database
def insert_combined_data():
    for _, row in combined_data.iterrows():
        cursor.execute('''
            INSERT INTO shipments (shipping_id, product_name, quantity, origin, destination)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['shipping_id'], row['product_name'], row['quantity'], row['origin'], row['destination']))
    db_connection.commit()

insert_combined_data()

# Step 6: Close the database connection
db_connection.close()
