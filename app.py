import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

PRODUCT_FILE = "products.json"
EXPENSE_FILE = "expenses.json"
SALES_FILE = "sales.json"

LOW_STOCK_LIMIT = 5


# =========================
# DATA FUNCTIONS
# =========================

def load_data(filename, default):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except:
            return default
    return default


def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


products = load_data(PRODUCT_FILE, {})
expenses = load_data(EXPENSE_FILE, [])
sales = load_data(SALES_FILE, [])


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("Smart Shop Manager")
root.geometry("1000x650")
root.minsize(850, 550)


# =========================
# DASHBOARD
# =========================

def refresh_dashboard():

    total_products = len(products)

    total_stock = sum(
        item["quantity"] for item in products.values()
    )

    total_sales = sum(
        item["total"] for item in sales
    )

    total_expenses = sum(
        item["amount"] for item in expenses
    )

    profit = total_sales - total_expenses

    low_stock = sum(
        1
        for item in products.values()
        if item["quantity"] <= LOW_STOCK_LIMIT
    )

    products_value_label.config(
        text=str(total_products)
    )

    stock_value_label.config(
        text=str(total_stock)
    )

    sales_value_label.config(
        text=f"₹{total_sales:.2f}"
    )

    expenses_value_label.config(
        text=f"₹{total_expenses:.2f}"
    )

    profit_value_label.config(
        text=f"₹{profit:.2f}"
    )

    low_stock_value_label.config(
        text=str(low_stock)
    )


def clear_content():

    for widget in content.winfo_children():
        widget.destroy()


# =========================
# ADD PRODUCT
# =========================

def add_product_gui():

    window = tk.Toplevel(root)
    window.title("Add Product")
    window.geometry("400x350")

    tk.Label(
        window,
        text="Add New Product",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(
        window,
        text="Product Name"
    ).pack()

    name_entry = tk.Entry(
        window,
        width=30
    )

    name_entry.pack(pady=5)

    tk.Label(
        window,
        text="Price"
    ).pack()

    price_entry = tk.Entry(
        window,
        width=30
    )

    price_entry.pack(pady=5)

    tk.Label(
        window,
        text="Quantity"
    ).pack()

    quantity_entry = tk.Entry(
        window,
        width=30
    )

    quantity_entry.pack(pady=5)

    def add():

        name = name_entry.get().strip()

        if not name:

            messagebox.showerror(
                "Error",
                "Enter a product name."
            )

            return

        try:

            price = float(
                price_entry.get()
            )

            quantity = int(
                quantity_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter valid price and quantity."
            )

            return

        if price < 0 or quantity < 0:

            messagebox.showerror(
                "Error",
                "Price and quantity cannot be negative."
            )

            return

        products[name] = {
            "price": price,
            "quantity": quantity
        }

        save_data(
            PRODUCT_FILE,
            products
        )

        messagebox.showinfo(
            "Success",
            f"{name} added successfully!"
        )

        window.destroy()

        refresh_dashboard()

    tk.Button(
        window,
        text="ADD PRODUCT",
        command=add,
        width=20,
        height=2
    ).pack(pady=20)


# =========================
# RECORD SALE
# =========================

def record_sale_gui():

    if not products:

        messagebox.showwarning(
            "No Products",
            "Please add a product first."
        )

        return

    window = tk.Toplevel(root)
    window.title("Record Sale")
    window.geometry("450x350")

    tk.Label(
        window,
        text="Record Sale",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(
        window,
        text="Select Product"
    ).pack()

    product_names = list(
        products.keys()
    )

    product_box = ttk.Combobox(
        window,
        values=product_names,
        state="readonly",
        width=30
    )

    product_box.pack(pady=10)

    product_box.current(0)

    tk.Label(
        window,
        text="Quantity Sold"
    ).pack()

    quantity_entry = tk.Entry(
        window,
        width=30
    )

    quantity_entry.pack(pady=10)

    def record():

        product_name = product_box.get()

        if not product_name:

            messagebox.showerror(
                "Error",
                "Select a product."
            )

            return

        try:

            quantity = int(
                quantity_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Quantity must be a whole number."
            )

            return

        if quantity <= 0:

            messagebox.showerror(
                "Error",
                "Quantity must be greater than zero."
            )

            return

        available = products[
            product_name
        ]["quantity"]

        if quantity > available:

            messagebox.showerror(
                "Not Enough Stock",
                f"Only {available} units available."
            )

            return

        price = products[
            product_name
        ]["price"]

        total = price * quantity

        products[
            product_name
        ]["quantity"] -= quantity

        sales.append({
            "product": product_name,
            "quantity": quantity,
            "total": total
        })

        save_data(
            PRODUCT_FILE,
            products
        )

        save_data(
            SALES_FILE,
            sales
        )

        messagebox.showinfo(
            "Sale Recorded",
            f"Sale successful!\n\n"
            f"Product: {product_name}\n"
            f"Quantity: {quantity}\n"
            f"Total: ₹{total:.2f}\n\n"
            f"Remaining stock: "
            f"{products[product_name]['quantity']}"
        )

        window.destroy()

        refresh_dashboard()

    tk.Button(
        window,
        text="RECORD SALE",
        command=record,
        width=20,
        height=2
    ).pack(pady=20)


# =========================
# ADD EXPENSE
# =========================

def add_expense_gui():

    window = tk.Toplevel(root)
    window.title("Add Expense")
    window.geometry("400x300")

    tk.Label(
        window,
        text="Add Expense",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(
        window,
        text="Expense Name"
    ).pack()

    name_entry = tk.Entry(
        window,
        width=30
    )

    name_entry.pack(pady=8)

    tk.Label(
        window,
        text="Amount"
    ).pack()

    amount_entry = tk.Entry(
        window,
        width=30
    )

    amount_entry.pack(pady=8)

    def add():

        name = name_entry.get().strip()

        if not name:

            messagebox.showerror(
                "Error",
                "Enter an expense name."
            )

            return

        try:

            amount = float(
                amount_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Amount must be a number."
            )

            return

        if amount <= 0:

            messagebox.showerror(
                "Error",
                "Amount must be greater than zero."
            )

            return

        expenses.append({
            "name": name,
            "amount": amount
        })

        save_data(
            EXPENSE_FILE,
            expenses
        )

        messagebox.showinfo(
            "Success",
            f"Expense added!\n\n"
            f"{name}: ₹{amount:.2f}"
        )

        window.destroy()

        refresh_dashboard()

    tk.Button(
        window,
        text="ADD EXPENSE",
        command=add,
        width=20,
        height=2
    ).pack(pady=20)


# =========================
# DASHBOARD SCREEN
# =========================

def show_dashboard():

    clear_content()

    tk.Label(
        content,
        text="Dashboard",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    cards_frame = tk.Frame(content)

    cards_frame.pack(pady=20)

    create_card(
        cards_frame,
        "Products",
        products_value_label
    )

    create_card(
        cards_frame,
        "Total Stock",
        stock_value_label
    )

    create_card(
        cards_frame,
        "Sales",
        sales_value_label
    )

    second_frame = tk.Frame(content)

    second_frame.pack(pady=20)

    create_card(
        second_frame,
        "Expenses",
        expenses_value_label
    )

    create_card(
        second_frame,
        "Profit",
        profit_value_label
    )

    create_card(
        second_frame,
        "Low Stock",
        low_stock_value_label
    )

    refresh_dashboard()


def create_card(
    parent,
    title,
    value_label
):

    card = tk.Frame(
        parent,
        relief="solid",
        borderwidth=1,
        width=200,
        height=120
    )

    card.pack(
        side="left",
        padx=10
    )

    card.pack_propagate(False)

    tk.Label(
        card,
        text=title,
        font=("Arial", 13, "bold")
    ).pack(pady=10)

    value_label.pack()


# =========================
# PRODUCTS SCREEN
# =========================

def show_products():

    clear_content()

    tk.Label(
        content,
        text="Products",
        font=("Arial", 24, "bold")
    ).pack(pady=15)

    table = ttk.Treeview(
        content,
        columns=(
            "name",
            "price",
            "stock"
        ),
        show="headings"
    )

    table.heading(
        "name",
        text="Product"
    )

    table.heading(
        "price",
        text="Price"
    )

    table.heading(
        "stock",
        text="Stock"
    )

    table.column(
        "name",
        width=300
    )

    table.column(
        "price",
        width=150
    )

    table.column(
        "stock",
        width=150
    )

    table.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=10
    )

    for name, data in products.items():

        table.insert(
            "",
            "end",
            values=(
                name,
                f"₹{data['price']:.2f}",
                data["quantity"]
            )
        )


# =========================
# SALES SCREEN
# =========================

def show_sales():

    clear_content()

    tk.Label(
        content,
        text="Sales",
        font=("Arial", 24, "bold")
    ).pack(pady=15)

    table = ttk.Treeview(
        content,
        columns=(
            "product",
            "quantity",
            "total"
        ),
        show="headings"
    )

    table.heading(
        "product",
        text="Product"
    )

    table.heading(
        "quantity",
        text="Quantity"
    )

    table.heading(
        "total",
        text="Total"
    )

    table.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=10
    )

    for sale in sales:

        table.insert(
            "",
            "end",
            values=(
                sale["product"],
                sale["quantity"],
                f"₹{sale['total']:.2f}"
            )
        )


# =========================
# EXPENSE SCREEN
# =========================

def show_expenses():

    clear_content()

    tk.Label(
        content,
        text="Expenses",
        font=("Arial", 24, "bold")
    ).pack(pady=15)

    table = ttk.Treeview(
        content,
        columns=(
            "name",
            "amount"
        ),
        show="headings"
    )

    table.heading(
        "name",
        text="Expense"
    )

    table.heading(
        "amount",
        text="Amount"
    )

    table.column(
        "name",
        width=300
    )

    table.column(
        "amount",
        width=200
    )

    table.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=10
    )

    for expense in expenses:

        table.insert(
            "",
            "end",
            values=(
                expense["name"],
                f"₹{expense['amount']:.2f}"
            )
        )


# =========================
# PROFIT SCREEN
# =========================

def show_profit():

    clear_content()

    total_sales = sum(
        item["total"]
        for item in sales
    )

    total_expenses = sum(
        item["amount"]
        for item in expenses
    )

    profit = total_sales - total_expenses

    tk.Label(
        content,
        text="Profit Report",
        font=("Arial", 24, "bold")
    ).pack(pady=30)

    tk.Label(
        content,
        text=f"Total Sales: ₹{total_sales:.2f}",
        font=("Arial", 18)
    ).pack(pady=10)

    tk.Label(
        content,
        text=f"Total Expenses: ₹{total_expenses:.2f}",
        font=("Arial", 18)
    ).pack(pady=10)

    tk.Label(
        content,
        text=f"Profit: ₹{profit:.2f}",
        font=("Arial", 22, "bold")
    ).pack(pady=20)


# =========================
# LOW STOCK
# =========================

def show_low_stock():

    clear_content()

    tk.Label(
        content,
        text="Low Stock Products",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    found = False

    for name, data in products.items():

        if data["quantity"] <= LOW_STOCK_LIMIT:

            found = True

            tk.Label(
                content,
                text=(
                    f"⚠️ {name} — "
                    f"{data['quantity']} remaining"
                ),
                font=("Arial", 16)
            ).pack(pady=5)

    if not found:

        tk.Label(
            content,
            text="No low-stock products.",
            font=("Arial", 16)
        ).pack(pady=20)


# =========================
# SEARCH
# =========================

def search_product():

    search_window = tk.Toplevel(root)

    search_window.title(
        "Search Product"
    )

    search_window.geometry(
        "400x250"
    )

    tk.Label(
        search_window,
        text="Search Product",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    search_entry = tk.Entry(
        search_window,
        font=("Arial", 14),
        width=25
    )

    search_entry.pack(pady=10)

    result_label = tk.Label(
        search_window,
        text="",
        font=("Arial", 12)
    )

    result_label.pack(pady=10)

    def search():

        query = (
            search_entry
            .get()
            .lower()
            .strip()
        )

        results = []

        for name, data in products.items():

            if query in name.lower():

                results.append(
                    f"{name} | "
                    f"₹{data['price']:.2f} | "
                    f"Stock: {data['quantity']}"
                )

        if results:

            result_label.config(
                text="\n".join(results)
            )

        else:

            result_label.config(
                text="Product not found."
            )

    tk.Button(
        search_window,
        text="Search",
        command=search,
        width=15
    ).pack(pady=10)


# =========================
# DASHBOARD LABELS
# =========================

products_value_label = tk.Label(
    font=("Arial", 20, "bold")
)

stock_value_label = tk.Label(
    font=("Arial", 20, "bold")
)

sales_value_label = tk.Label(
    font=("Arial", 20, "bold")
)

expenses_value_label = tk.Label(
    font=("Arial", 20, "bold")
)

profit_value_label = tk.Label(
    font=("Arial", 20, "bold")
)

low_stock_value_label = tk.Label(
    font=("Arial", 20, "bold")
)


# =========================
# SIDEBAR
# =========================

sidebar = tk.Frame(
    root,
    width=200,
    relief="solid",
    borderwidth=1
)

sidebar.pack(
    side="left",
    fill="y"
)

tk.Label(
    sidebar,
    text="SMART SHOP",
    font=("Arial", 18, "bold")
).pack(pady=25)


def make_button(
    text,
    command
):

    tk.Button(
        sidebar,
        text=text,
        command=command,
        width=20,
        height=2
    ).pack(pady=5)


make_button(
    "📊 Dashboard",
    show_dashboard
)

make_button(
    "➕ Add Product",
    add_product_gui
)

make_button(
    "📦 Products",
    show_products
)

make_button(
    "🛒 Record Sale",
    record_sale_gui
)

make_button(
    "🛒 Sales",
    show_sales
)

make_button(
    "💸 Add Expense",
    add_expense_gui
)

make_button(
    "💸 Expenses",
    show_expenses
)

make_button(
    "📈 Profit",
    show_profit
)

make_button(
    "🔍 Search",
    search_product
)

make_button(
    "⚠️ Low Stock",
    show_low_stock
)


# =========================
# CONTENT
# =========================

content = tk.Frame(root)

content.pack(
    side="right",
    fill="both",
    expand=True
)


# Start application

show_dashboard()

root.mainloop()