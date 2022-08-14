# Run the payment plan based off summary_transaction_2020 from step 7, after creation. Change selection to 2019 in Nayana's code.
import questionary
from db_utils import get_debt_free_db_engine, get_transaction_for_user_year

def payment_plan(user):
    # Pulls the data based on the user information.
    engine = get_debt_free_db_engine()
    transaction_2019 = get_transaction_for_user_year(engine, user, '2019')
    
    # Calculates the sum of the total debt.
    sumofdebt = transaction_2019["amount"].sum()
    
    # Prints out information to the user along with choice selection.
    print(f"Thank you, {user}, for choosing to consolidate your debt with our payment plan.")
    print(f"Your current total debt is ${sumofdebt}.")
    print("We currently have an APR on our payment plan of 5%.")
    print("This will offer you easy to pay monthly payments.")
    print("We have 4 options for our payment plan, please choose one of our plans listed below.")
    print("Or Quit to return to our main menu.")
    
    cli_running = True

    # A loop for the running of the payment plan, if they wish to view more than 1 option.
    while cli_running:
        choice = questionary.select("Which option works best for you?",
            choices=["6 Months", "1 Year", "3 Year", "5 Year", "Quit"]).ask()

        if choice == "6 Months":
            payment_time = 6
            cli_running = payment_plan_option(sumofdebt, payment_time)
                
        elif choice == "1 Year":
            payment_time = 12
            cli_running = payment_plan_option(sumofdebt, payment_time)
            
            
        elif choice == "3 Year":
            payment_time = 36
            cli_running = payment_plan_option(sumofdebt, payment_time)
            
        elif choice == "5 Year":
            payment_time = 60
            cli_running = payment_plan_option(sumofdebt, payment_time)
        
        elif choice == "Quit":
            cli_running = False
            print("You will be returned to the main menu.")
    
    
def payment_plan_option(total, time):
    # Reads in the total and the time and applies the APR to calculate the amount they will need to pay to be debt free by chosen time.
    APR = 0.05 / 12
    
    payment = total * ((APR*(pow((1+APR), time)))/(pow((1 + APR), time) - 1))
    print(f"Your payment amount would be ${payment_amount} over {payment_time} months.")
    cli_running = payment_works()

    return cli_running

def payment_works():
    # Checks if the customer is happy with their plan.
    
    yes_no = questionary.select("Will this payment plan work for you?", choices=["Yes", "No"]).ask()
            
    if yes_no == "Yes":
        cli_running = False
        print("We thank you for choosing our consolidated payment plan.")
        print("We appreciate you as a customer.")
              
    elif yes_no == "No":
        print("We are sorry this plan doesn't work.")
        print("Please choose a different plan or choose to quit.")
        print("Or, if you'd like to set your own payment,")
        print("   please use our projection plan from our main menu.")
        cli_running = True
    
    return cli_running