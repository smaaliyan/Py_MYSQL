import pandas as pd
import pymysql

# Database credentials
db_host = "localhost"
db_user = "root"
db_password = ""
db_name = "user_uploading"

def connect_to_database():
    try:
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        print("Connected to the database.")
        return connection
    except pymysql.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def read_from_csv_and_insert(connection, csv_filename):
    try:
        data_frame = pd.read_csv(csv_filename)
        
        with connection.cursor() as cursor:
            for index, row in data_frame.iterrows():
                insert_query = "INSERT INTO user_data(first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
                data = (row['first_name'], row['last_name'], row['email'], row['password'])
                cursor.execute(insert_query, data)
            connection.commit()  # Commit the changes
        
        print("Data inserted from CSV using Pandas successfully.")
    except (pymysql.Error, FileNotFoundError, pd.errors.PandasError) as e:
        print(f"Error inserting data from CSV using Pandas: {e}")

def main():
    csv_filename = "user_data.csv"  # Replace with the actual CSV file name
    connection = connect_to_database()
    if connection:
        read_from_csv_and_insert(connection, csv_filename)
        connection.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
