while True:
    print("1. Add Expense")
    print("2. View Expense")
    print("3. Delete Expense")
    print("4. Total Spendings")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        expense_name = input("Enter Expense name: ")
        amount = int(input("Enter Amount: "))

        with open("expenses.txt", "a") as file:
            file.write(f"{expense_name},{amount}\n")
        print("Expense added successfully!")

    elif choice == "2":

        try:
            with open("expenses.txt", "r") as file:
                lines = file.readlines()

                if len(lines) == 0:
                    print("No expense found.")
                else:
                    print("\n --- Expense List ---\n")
                    for line in lines:
                        expense_name, amount = line.strip().split(",")
                        print(f"{expense_name} - ₹{amount}")
        except FileNotFoundError:
            print("No expenses file found. Add expenses first.")

    elif choice == "3":

        try:
            with open("expenses.txt", "r") as file:
                lines = file.readlines()
        
            if len(lines) == 0:
                print("No expenses to delete.")
            else:
                print("\n--- Expenses ---\n")
                
                for i, line in enumerate(lines):
                    expense_name, amount = line.strip().split(",")
                    print(f"{i+1}. {expense_name} - ₹{amount}")
                
                index = int(input("\nEnter number to delete: ")) - 1
                
                if 0 <= index < len(lines):
                    lines.pop(index)
                    
                    with open("expenses.txt", "w") as file:
                        file.writelines(lines)

                    print("Expense deleted successfully!")
                else:
                    print("Invalid choice.")

        except FileNotFoundError:
            print("No file found.")

    elif choice == "4":
        try:
            with open("expenses.txt", "r") as file:
                lines = file.readlines()

            if len(lines) == 0:
                print("No exenses found.")
            else:
                print("\n--- Exense List ---\n")
            
                total = 0

                for line in lines:
                    expense_name, amount = line.strip().split(",")
                    total = total + int(amount)

                print(f"\nTotal Spending: ₹{total}")

        except FileNotFoundError:
            print("No expenses found.")

    elif choice == "4":
        print("Exit")
        break