import json
import os

DATA_FILE = "products.json"


def load_products():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Could not load saved data. Starting with empty stock.")

    return {}


def save_products():
    with open(DATA_FILE, "w") as file:
        json.dump(products, file, indent=4)


products = load_products()


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

    products[name] = {
        "price": price,
        "quantity": quantity
    }

    save_products()

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

    save_products()

    print(f"Sale recorded. Total = ₹{total:.2f}")
    print(f"Remaining stock = {products[name]['quantity']}")


def main():
    while True:
        print("\n==============================")
        print("     SMART SHOP MANAGER")
        print("==============================")
        print("1. Add product")
        print("2. View products")
        print("3. Sell product")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_product()

        elif choice == "2":
            view_products()

        elif choice == "3":
            sell_product()

        elif choice == "4":
            print("Thank you!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()