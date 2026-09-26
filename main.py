import json
import os

PRODUCT_FILE = "products.json"
EXPENSE_FILE = "expenses.json"
SALES_FILE = "sales.json"

LOW_STOCK_LIMIT = 5


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
        stock_warning = ""

        if data["quantity"] <= LOW_STOCK_LIMIT:
            stock_warning = " ⚠️ LOW STOCK"

        print(
            f"{name} | "
            f"Price: ₹{data['price']:.2f} | "
            f"Stock: {data['quantity']}"
            f"{stock_warning}"
        )


def find_product(search_name):
    search_name = search_name.strip().lower()

    for name in products:
        if name.lower() == search_name:
            return name

    return None


def sell_product():
    name = input("Enter product name: ").strip()

    product_name = find_product(name)

    if product_name is None:
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

    if quantity > products[product_name]["quantity"]:
        print("Not enough stock.")
        return

    products[product_name]["quantity"] -= quantity

    total = quantity * products[product_name]["price"]

    sales.append({
        "product": product_name,
        "quantity": quantity,
        "total": total
    })

    save_data(PRODUCT_FILE, products)
    save_data(SALES_FILE, sales)

    print(f"Sale recorded. Total = ₹{total:.2f}")
    print(f"Remaining stock = {products[product_name]['quantity']}")


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


def search_product():
    search_name = input("Enter product to search: ").strip().lower()

    found = False

    print("\n--- SEARCH RESULTS ---")

    for name, data in products.items():
        if search_name in name.lower():
            print(
                f"{name} | "
                f"Price: ₹{data['price']:.2f} | "
                f"Stock: {data['quantity']}"
            )
            found = True

    if not found:
        print("No matching product found.")


def low_stock_report():
    print("\n--- LOW STOCK REPORT ---")

    found = False

    for name, data in products.items():
        if data["quantity"] <= LOW_STOCK_LIMIT:
            print(
                f"⚠️ {name} | "
                f"Stock: {data['quantity']}"
            )
            found = True

    if not found:
        print("No products are low in stock.")


def dashboard():
    total_products = len(products)

    total_stock = sum(
        data["quantity"] for data in products.values()
    )

    total_sales = sum(
        sale["total"] for sale in sales
    )

    total_expenses = sum(
        expense["amount"] for expense in expenses
    )

    profit = total_sales - total_expenses

    low_stock_count = sum(
        1
        for data in products.values()
        if data["quantity"] <= LOW_STOCK_LIMIT
    )

    print("\n")
    print("====================================")
    print("          SHOP DASHBOARD")
    print("====================================")
    print(f" Products:        {total_products}")
    print(f" Total Stock:     {total_stock}")
    print("------------------------------------")
    print(f" Total Sales:     ₹{total_sales:.2f}")
    print(f" Expenses:        ₹{total_expenses:.2f}")
    print(f" Profit:          ₹{profit:.2f}")
    print("------------------------------------")
    print(f" ⚠️ Low Stock:     {low_stock_count}")
    print("====================================")


def main():
    while True:
        print("\n==============================")
        print("     SMART SHOP MANAGER")
        print("==============================")
        print("1. Dashboard")
        print("2. Add product")
        print("3. View products")
        print("4. Sell product")
        print("5. Add expense")
        print("6. View expenses")
        print("7. View profit")
        print("8. Search product")
        print("9. Low stock report")
        print("10. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            dashboard()

        elif choice == "2":
            add_product()

        elif choice == "3":
            view_products()

        elif choice == "4":
            sell_product()

        elif choice == "5":
            add_expense()

        elif choice == "6":
            view_expenses()

        elif choice == "7":
            view_profit()

        elif choice == "8":
            search_product()

        elif choice == "9":
            low_stock_report()

        elif choice == "10":
            print("Thank you!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()