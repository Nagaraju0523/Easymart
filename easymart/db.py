import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=USER20\\MSSQLSERVER02;"
        "DATABASE=Easymart;"
        "Trusted_Connection=yes;"
    )
    return conn