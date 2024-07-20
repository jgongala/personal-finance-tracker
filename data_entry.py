from datetime import datetime

# Define the date format to be used
date_format = "%d-%m-%Y"

# Define categories for transactions
CATEGORIES = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default=False):
    """
    Prompt the user to enter a date. If allow_default is True, 
    return today's date if no input is given. Validate the date format.
    """
    date_string = input(prompt)
    
    if allow_default and not date_string:
        return datetime.today().strftime(date_format)
    
    try:
        # Try to parse the date input by the user
        valid_date = datetime.strptime(date_string, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        # If the date format is invalid, notify the user and prompt again
        print("Invalid date format. Please enter the date in dd-mm-yyyy format.")
        return get_date(prompt, allow_default)
    

def get_amount():
    """
    Prompt the user to enter an amount. Validate that the amount 
    is a positive number.
    """
    try:
        amount = float(input("Enter the amount: "))
        
        if amount <= 0:
            raise ValueError("Amount must be a non-negative and non-zero value!")
        return amount
    
    except ValueError as e:
        # If the input is invalid, notify the user and prompt again
        print(e)
        return get_amount()
        

def get_category():
    """
    Prompt the user to enter a category. Validate that the input 
    is either 'I' for Income or 'E' for Expense.
    """
    category = input("Enter the category('I' for Income or 'E' for Expense): ").upper()
    
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    # If the input is invalid, notify the user and prompt again
    print("Invalid category. Please enter 'I' for Income or 'E' for Expense")
    return get_category()

def get_description():
    """
    Prompt the user to enter a description. This input is optional.
    """
    return input("Enter a description (optional). ")
