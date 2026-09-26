import json
import os

PRODUCT_FILE = "products.json"
EXPENSE_FILE = "expenses.json"
SALES_FILE = "sales.json"


def load_data(filename, default):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print(f"Could not load {filename}. Starting fresh.")

    return default


def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


products = load_data(PRODUCT_FILE, {})
expenses = load_data(EXPENSE_FILE, [])
sales = load_data(SALES_FILE, [])


def add_product():
    name = input("Enter product name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = float(input("Enter price: "))
        quantity = int(input("Enter quantity: "))
    except ValueError:
        print("Invalid price or quantity.")
        return

    if price < 0 or quantity < 0:
        print("Price and quantity cannot be negative.")
        return

    products[name] = {
        "price": price,
        "quantity": quantity
    }

    save_data(PRODUCT_FILE, products)

    print("Product added and saved successfully!")


def view_products():
    if not products:
        print("\nNo products available.")
        return

    print("\n--- PRODUCTS ---")

    for name, data in products.items():
        print(
            f"{name} | "
            f"Price: ₹{data['price']:.2f} | "
            f"Stock: {data['quantity']}"
        )


def sell_product():
    name = input("Enter product name: ").strip()

    if name not in products:
        print("Product not found.")
        return

    try:
        quantity = int(input("Enter quantity sold: "))
    except ValueError:
        print("Invalid quantity.")
        return

    if quantity <= 0:
        print("Quantity must be greater than zero.")
        return

    if quantity > products[name]["quantity"]:
        print("Not enough stock.")
        return

    products[name]["quantity"] -= quantity

    total = quantity * products[name]["price"]

    sales.append({
        "product": name,
        "quantity": quantity,
        "total": total
    })

    save_data(PRODUCT_FILE, products)
    save_data(SALES_FILE, sales)

    print(f"Sale recorded. Total = ₹{total:.2f}")
    print(f"Remaining stock = {products[name]['quantity']}")


def add_expense():
    name = input("Enter expense name: ").strip()

    try:
        amount = float(input("Enter expense amount: "))
    except ValueError:
        print("Invalid amount.")
        return

    if amount < 0:
        print("Expense cannot be negative.")
        return

    expenses.append({
        "name": name,
        "amount": amount
    })

    save_data(EXPENSE_FILE, expenses)

    print("Expense saved successfully!")


def view_expenses():
    if not expenses:
        print("\nNo expenses recorded.")
        return

    print("\n--- EXPENSES ---")

    total = 0

    for expense in expenses:
        print(
            f"{expense['name']} | "
            f"₹{expense['amount']:.2f}"
        )
        total += expense["amount"]

    print("----------------")
    print(f"Total expenses: ₹{total:.2f}")


def view_profit():
    total_sales = sum(sale["total"] for sale in sales)
    total_expenses = sum(expense["amount"] for expense in expenses)

    profit = total_sales - total_expenses

    print("\n--- PROFIT REPORT ---")
    print(f"Total sales:    ₹{total_sales:.2f}")
    print(f"Total expenses: ₹{total_expenses:.2f}")
    print("-------------------------")
    print(f"Profit:         ₹{profit:.2f}")


def main():
    while True:
        print("\n==============================")
        print("     SMART SHOP MANAGER")
        print("==============================")
        print("1. Add product")
        print("2. View products")
        print("3. Sell product")
        print("4. Add expense")
        print("5. View expenses")
        print("6. View profit")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_product()

        elif choice == "2":
            view_products()

        elif choice == "3":
            sell_product()

        elif choice == "4":
            add_expense()

        elif choice == "5":
            view_expenses()

        elif choice == "6":
            view_profit()

        elif choice == "7":
            print("Thank you!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()