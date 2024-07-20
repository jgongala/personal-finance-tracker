import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    # Constants for the CSV file and its columns
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    DATE_FORMAT = "%d-%m-%Y"  # Format for date strings
    
    @classmethod
    def initialize_csv(cls):
        """
        Initializes the CSV file with the specified columns if it does not exist.
        """
        try:
            # Attempt to read the CSV file
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            # Create an empty DataFrame with the specified columns and save it
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
    
    @classmethod
    def add_entry(cls, date, amount, category, description):
        """
        Adds a new entry to the CSV file.
        
        :param date: The date of the transaction
        :param amount: The amount of the transaction
        :param category: The category of the transaction (e.g., 'Income', 'Expense')
        :param description: A description of the transaction
        """
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        
        # Open the CSV file in append mode and write the new entry
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        
        print("Entry added successfully")
    
    @classmethod
    def get_transactions(cls, start_date, end_date):
        """
        Retrieves transactions within a specified date range and provides a summary.
        
        :param start_date: The start date for the range
        :param end_date: The end date for the range
        :return: A DataFrame containing the filtered transactions
        """
        # Read the CSV file into a DataFrame
        data_frame = pd.read_csv(cls.CSV_FILE)
        # Convert the 'date' column to datetime objects
        data_frame["date"] = pd.to_datetime(data_frame["date"], format=CSV.DATE_FORMAT)
        
        # Convert start and end dates to datetime objects
        start_date = datetime.strptime(start_date, CSV.DATE_FORMAT)
        end_date = datetime.strptime(end_date, CSV.DATE_FORMAT)
        
        # Filter the DataFrame based on the date range
        mask = (data_frame["date"] >= start_date) & (data_frame["date"] <= end_date)
        filtered_data_frame = data_frame.loc[mask]
        
        if filtered_data_frame.empty:
            print("No transaction found in given date range.")
        else: 
            print(f"Transactions from {start_date.strftime(CSV.DATE_FORMAT)} to {end_date.strftime(CSV.DATE_FORMAT)}")
            print(filtered_data_frame.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.DATE_FORMAT)}))
            
            # Calculate total income and expenses
            total_income = filtered_data_frame[filtered_data_frame["category"] == "Income"]["amount"].sum()
            total_expense = filtered_data_frame[filtered_data_frame["category"] == "Expense"]["amount"].sum()
            
            print("\nSummary:")
            print(f"Total Income: £{total_income:.2f}")
            print(f"Total Expense: £{total_expense:.2f}")
            print(f"Net Savings: £{(total_income - total_expense):.2f}")
            
            return filtered_data_frame

def add():
    """
    Prompts the user to enter transaction details and adds the entry to the CSV file.
    """
    # Initialize the CSV file if it does not exist
    CSV.initialize_csv()
    
    # Get transaction details from the user
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    
    # Add the entry to the CSV file
    CSV.add_entry(date, amount, category, description)

def plot_transactions(data_frame):
    """
    Plots income and expense transactions over time.
    
    :param data_frame: A DataFrame containing the transactions to plot
    """
    # Set 'date' as the index and resample by day
    data_frame.set_index("date", inplace=True)
    income_data_frame = data_frame[data_frame["category"] == "Income"].resample("D").sum().reindex(data_frame.index, fill_value=0)
    expense_data_frame = data_frame[data_frame["category"] == "Expense"].resample("D").sum().reindex(data_frame.index, fill_value=0)
    
    # Plot the income and expense data
    plt.figure(figsize=(10, 5))
    plt.plot(income_data_frame.index, income_data_frame["amount"], label="Income", color="g")    
    plt.plot(expense_data_frame.index, expense_data_frame["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses over time")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    """
    Main function to display the menu and handle user choices.
    """
    while True:
        print("\n1. Add a new transaction.")
        print("2. View transactions and a summary within a date range.")
        print("3. Exit")
        
        # Get the user's choice
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            add()
        elif choice == "2":
            # Get date range from user
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            
            # Retrieve and display transactions
            data_frame = CSV.get_transactions(start_date, end_date)
            
            # Plot the transactions if requested
            if input("Do you want to see a plot (y/n): ").lower() == "y":
                plot_transactions(data_frame)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3")
            
if __name__ == "__main__":
    main()
