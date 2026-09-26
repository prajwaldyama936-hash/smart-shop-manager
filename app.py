import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

PRODUCT_FILE = "products.json"
EXPENSE_FILE = "expenses.json"
SALES_FILE = "sales.json"

LOW_STOCK_LIMIT = 5

# =========================================================
# DATA FUNCTIONS
# =========================================================

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


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("Smart Shop Manager")
root.geometry("1100x700")
root.minsize(950, 600)

BG = "#f4f6f8"
SIDEBAR = "#202938"
CARD = "#ffffff"
TEXT = "#1f2937"
MUTED = "#6b7280"

root.configure(bg=BG)


# =========================================================
# MAIN CONTENT
# =========================================================

content = tk.Frame(
    root,
    bg=BG
)

content.pack(
    side="right",
    fill="both",
    expand=True
)


def clear_content():
    for widget in content.winfo_children():
        widget.destroy()


# =========================================================
# DASHBOARD
# =========================================================

def get_dashboard_data():

    total_products = len(products)

    total_stock = sum(
        item["quantity"]
        for item in products.values()
    )

    total_sales = sum(
        item.get("total", 0)
        for item in sales
    )

    total_expenses = sum(
        item.get("amount", 0)
        for item in expenses
    )

    profit = total_sales - total_expenses

    low_stock = sum(
        1
        for item in products.values()
        if item["quantity"] <= LOW_STOCK_LIMIT
    )

    return (
        total_products,
        total_stock,
        total_sales,
        total_expenses,
        profit,
        low_stock
    )


def create_card(parent, title, value):

    card = tk.Frame(
        parent,
        bg=CARD,
        width=220,
        height=130,
        highlightbackground="#d9dde3",
        highlightthickness=1
    )

    card.pack(
        side="left",
        padx=10
    )

    card.pack_propagate(False)

    tk.Label(
        card,
        text=title,
        font=("Arial", 12),
        bg=CARD,
        fg=MUTED
    ).pack(
        pady=(20, 5)
    )

    tk.Label(
        card,
        text=value,
        font=("Arial", 22, "bold"),
        bg=CARD,
        fg=TEXT
    ).pack()


def show_dashboard():

    clear_content()

    (
        total_products,
        total_stock,
        total_sales,
        total_expenses,
        profit,
        low_stock
    ) = get_dashboard_data()

    header = tk.Frame(
        content,
        bg=BG
    )

    header.pack(
        fill="x",
        padx=35,
        pady=(30, 10)
    )

    tk.Label(
        header,
        text="Dashboard",
        font=("Arial", 28, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w"
    )

    tk.Label(
        header,
        text="Overview of your shop",
        font=("Arial", 12),
        bg=BG,
        fg=MUTED
    ).pack(
        anchor="w",
        pady=5
    )

    row1 = tk.Frame(
        content,
        bg=BG
    )

    row1.pack(
        pady=20
    )

    create_card(
        row1,
        "Products",
        str(total_products)
    )

    create_card(
        row1,
        "Total Stock",
        str(total_stock)
    )

    create_card(
        row1,
        "Total Sales",
        f"₹{total_sales:.2f}"
    )

    row2 = tk.Frame(
        content,
        bg=BG
    )

    row2.pack(
        pady=10
    )

    create_card(
        row2,
        "Expenses",
        f"₹{total_expenses:.2f}"
    )

    create_card(
        row2,
        "Profit",
        f"₹{profit:.2f}"
    )

    create_card(
        row2,
        "Low Stock",
        str(low_stock)
    )


# =========================================================
# ADD PRODUCT
# =========================================================

def add_product_gui():

    window = tk.Toplevel(root)
    window.title("Add Product")
    window.geometry("420x380")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="Add New Product",
        font=("Arial", 20, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        pady=25
    )

    tk.Label(
        window,
        text="Product Name",
        bg=BG
    ).pack()

    name_entry = tk.Entry(
        window,
        width=30,
        font=("Arial", 12)
    )

    name_entry.pack(
        pady=7
    )

    tk.Label(
        window,
        text="Price",
        bg=BG
    ).pack()

    price_entry = tk.Entry(
        window,
        width=30,
        font=("Arial", 12)
    )

    price_entry.pack(
        pady=7
    )

    tk.Label(
        window,
        text="Quantity",
        bg=BG
    ).pack()

    quantity_entry = tk.Entry(
        window,
        width=30,
        font=("Arial", 12)
    )

    quantity_entry.pack(
        pady=7
    )

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
                "Values cannot be negative."
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

        show_dashboard()

    tk.Button(
        window,
        text="ADD PRODUCT",
        command=add,
        width=22,
        height=2
    ).pack(
        pady=25
    )


# =========================================================
# EDIT PRODUCT
# =========================================================

def edit_product_gui():

    if not products:

        messagebox.showwarning(
            "No Products",
            "There are no products to edit."
        )

        return

    window = tk.Toplevel(root)

    window.title("Edit Product")

    window.geometry("450x430")

    window.configure(
        bg=BG
    )

    tk.Label(
        window,
        text="Edit Product",
        font=("Arial", 20, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        pady=25
    )

    tk.Label(
        window,
        text="Select Product",
        bg=BG
    ).pack()

    product_box = ttk.Combobox(
        window,
        values=list(products.keys()),
        state="readonly",
        width=30
    )

    product_box.pack(
        pady=10
    )

    product_box.current(0)

    tk.Label(
        window,
        text="New Price",
        bg=BG
    ).pack()

    price_entry = tk.Entry(
        window,
        width=30,
        font=("Arial", 12)
    )

    price_entry.pack(
        pady=8
    )

    tk.Label(
        window,
        text="New Quantity",
        bg=BG
    ).pack()

    quantity_entry = tk.Entry(
        window,
        width=30,
        font=("Arial", 12)
    )

    quantity_entry.pack(
        pady=8
    )

    def load_product(event=None):

        name = product_box.get()

        price_entry.delete(
            0,
            tk.END
        )

        quantity_entry.delete(
            0,
            tk.END
        )

        price_entry.insert(
            0,
            products[name]["price"]
        )

        quantity_entry.insert(
            0,
            products[name]["quantity"]
        )

    product_box.bind(
        "<<ComboboxSelected>>",
        load_product
    )

    load_product()

    def save_changes():

        name = product_box.get()

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
                "Enter valid values."
            )

            return

        if price < 0 or quantity < 0:

            messagebox.showerror(
                "Error",
                "Values cannot be negative."
            )

            return

        products[name]["price"] = price

        products[name]["quantity"] = quantity

        save_data(
            PRODUCT_FILE,
            products
        )

        messagebox.showinfo(
            "Success",
            f"{name} updated successfully!"
        )

        window.destroy()

        show_dashboard()

    tk.Button(
        window,
        text="SAVE CHANGES",
        command=save_changes,
        width=22,
        height=2
    ).pack(
        pady=25
    )


# =========================================================
# RESTOCK
# =========================================================

def restock_product_gui():

    if not products:

        messagebox.showwarning(
            "No Products",
            "Add a product first."
        )

        return

    window = tk.Toplevel(root)

    window.title(
        "Restock Product"
    )

    window.geometry(
        "430x350"
    )

    window.configure(
        bg=BG
    )

    tk.Label(
        window,
        text="Restock Product",
        font=("Arial", 20, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        pady=25
    )

    tk.Label(
        window,
        text="Select Product",
        bg=BG
    ).pack()

    product_box = ttk.Combobox(
        window,
        values=list(products.keys()),
        state="readonly",
        width=30
    )

    product_box.pack(
        pady=10
    )

    product_box.current(0)

    stock_label = tk.Label(
        window,
        text="",
        bg=BG,
        fg=MUTED
    )

    stock_label.pack(
        pady=5
    )

    def update_stock_label(event=None):

        name = product_box.get()

        stock_label.config(
            text=f"Current stock: {products[name]['quantity']}"
        )

    product_box.bind(
        "<<ComboboxSelected>>",
        update_stock_label
    )

    update_stock_label()

    tk.Label(
        window,
        text="Quantity to Add",
        bg=BG
    ).pack(
        pady=(15, 0)
    )

    quantity_entry = tk.Entry(
        window,
        width=30,
        font=("Arial", 12)
    )

    quantity_entry.pack(
        pady=10
    )

    def restock():

        name = product_box.get()

        try:

            quantity = int(
                quantity_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid quantity."
            )

            return

        if quantity <= 0:

            messagebox.showerror(
                "Error",
                "Quantity must be greater than zero."
            )

            return

        products[name]["quantity"] += quantity

        save_data(
            PRODUCT_FILE,
            products
        )

        messagebox.showinfo(
            "Success",
            f"{name} restocked by {quantity} units."
        )

        window.destroy()

        show_dashboard()

    tk.Button(
        window,
        text="RESTOCK",
        command=restock,
        width=22,
        height=2
    ).pack(
        pady=20
    )


# =========================================================
# DELETE PRODUCT
# =========================================================

def delete_product_gui():

    if not products:

        messagebox.showwarning(
            "No Products",
            "There are no products to delete."
        )

        return

    window = tk.Toplevel(root)

    window.title(
        "Delete Product"
    )

    window.geometry(
        "430x300"
    )

    window.configure(
        bg=BG
    )

    tk.Label(
        window,
        text="Delete Product",
        font=("Arial", 20, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        pady=25
    )

    tk.Label(
        window,
        text="Select Product",
        bg=BG
    ).pack()

    product_box = ttk.Combobox(
        window,
        values=list(products.keys()),
        state="readonly",
        width=30
    )

    product_box.pack(
        pady=15
    )

    product_box.current(0)

    def delete():

        name = product_box.get()

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{name}'?"
        )

        if not confirm:
            return

        del products[name]

        save_data(
            PRODUCT_FILE,
            products
        )

        messagebox.showinfo(
            "Deleted",
            f"{name} deleted successfully."
        )

        window.destroy()

        show_dashboard()

    tk.Button(
        window,
        text="DELETE PRODUCT",
        command=delete,
        width=22,
        height=2
    ).pack(
        pady=20
    )


# =========================================================
# PRODUCTS
# =========================================================

def show_products():

    clear_content()

    tk.Label(
        content,
        text="Products",
        font=("Arial", 26, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=35,
        pady=25
    )

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
        width=350
    )

    table.column(
        "price",
        width=200
    )

    table.column(
        "stock",
        width=200
    )

    table.pack(
        fill="both",
        expand=True,
        padx=35,
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

    button_frame = tk.Frame(
        content,
        bg=BG
    )

    button_frame.pack(
        pady=15
    )

    tk.Button(
        button_frame,
        text="EDIT",
        command=edit_product_gui,
        width=15,
        height=2
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        button_frame,
        text="RESTOCK",
        command=restock_product_gui,
        width=15,
        height=2
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        button_frame,
        text="DELETE",
        command=delete_product_gui,
        width=15,
        height=2
    ).pack(
        side="left",
        padx=5
    )


# =========================================================
# RECORD SALE + RECEIPT
# =========================================================

def record_sale_gui():

    if not products:

        messagebox.showwarning(
            "No Products",
            "Add a product first."
        )

        return

    window = tk.Toplevel(root)

    window.title(
        "Record Sale"
    )

    window.geometry(
        "500x550"
    )

    window.configure(
        bg=BG
    )

    tk.Label(
        window,
        text="Record Sale",
        font=("Arial", 22, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        pady=20
    )

    tk.Label(
        window,
        text="Customer Name",
        bg=BG
    ).pack()

    customer_entry = tk.Entry(
        window,
        width=32,
        font=("Arial", 12)
    )

    customer_entry.pack(
        pady=7
    )

    tk.Label(
        window,
        text="Customer Phone",
        bg=BG
    ).pack()

    phone_entry = tk.Entry(
        window,
        width=32,
        font=("Arial", 12)
    )

    phone_entry.pack(
        pady=7
    )

    tk.Label(
        window,
        text="Product",
        bg=BG
    ).pack(
        pady=(10, 0)
    )

    product_box = ttk.Combobox(
        window,
        values=list(products.keys()),
        state="readonly",
        width=30
    )

    product_box.pack(
        pady=7
    )

    product_box.current(0)

    tk.Label(
        window,
        text="Quantity",
        bg=BG
    ).pack()

    quantity_entry = tk.Entry(
        window,
        width=32,
        font=("Arial", 12)
    )

    quantity_entry.pack(
        pady=7
    )

    def record():

        customer = customer_entry.get().strip()

        phone = phone_entry.get().strip()

        product_name = product_box.get()

        if not customer:

            messagebox.showerror(
                "Error",
                "Enter customer name."
            )

            return

        if not phone:

            messagebox.showerror(
                "Error",
                "Enter customer phone."
            )

            return

        try:

            quantity = int(
                quantity_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid quantity."
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
                "Stock Error",
                f"Only {available} units available."
            )

            return

        price = products[
            product_name
        ]["price"]

        total = price * quantity

        receipt_number = len(sales) + 1

        date_time = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        products[
            product_name
        ]["quantity"] -= quantity

        sale = {

            "receipt": receipt_number,

            "customer": customer,

            "phone": phone,

            "product": product_name,

            "quantity": quantity,

            "price": price,

            "total": total,

            "date": date_time
        }

        sales.append(sale)

        save_data(
            PRODUCT_FILE,
            products
        )

        save_data(
            SALES_FILE,
            sales
        )

        receipt_window = tk.Toplevel(
            root
        )

        receipt_window.title(
            f"Receipt #{receipt_number}"
        )

        receipt_window.geometry(
            "450x500"
        )

        receipt_window.configure(
            bg="white"
        )

        receipt_text = f"""
================================
       SMART SHOP MANAGER
================================

Receipt No: {receipt_number:04d}
Date: {date_time}

Customer: {customer}
Phone: {phone}

--------------------------------
Product : {product_name}
Quantity: {quantity}
Price   : ₹{price:.2f}
--------------------------------

TOTAL: ₹{total:.2f}

================================
          THANK YOU!
================================
"""

        tk.Label(
            receipt_window,
            text=receipt_text,
            font=("Courier New", 11),
            bg="white",
            justify="left"
        ).pack(
            padx=20,
            pady=20
        )

        tk.Button(
            receipt_window,
            text="CLOSE RECEIPT",
            command=receipt_window.destroy,
            width=20,
            height=2
        ).pack(
            pady=10
        )

        window.destroy()

        show_dashboard()

    tk.Button(
        window,
        text="GENERATE RECEIPT",
        command=record,
        width=25,
        height=2
    ).pack(
        pady=25
    )


# =========================================================
# SALES HISTORY
# =========================================================

def show_sales():

    clear_content()

    tk.Label(
        content,
        text="Sales History",
        font=("Arial", 26, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=35,
        pady=25
    )

    table = ttk.Treeview(
        content,
        columns=(
            "receipt",
            "customer",
            "product",
            "quantity",
            "total",
            "date"
        ),
        show="headings"
    )

    table.heading(
        "receipt",
        text="Receipt"
    )

    table.heading(
        "customer",
        text="Customer"
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

    table.heading(
        "date",
        text="Date"
    )

    table.column(
        "receipt",
        width=80
    )

    table.column(
        "customer",
        width=150
    )

    table.column(
        "product",
        width=150
    )

    table.column(
        "quantity",
        width=80
    )

    table.column(
        "total",
        width=100
    )

    table.column(
        "date",
        width=160
    )

    table.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )

    for sale in sales:

        table.insert(
            "",
            "end",
            values=(
                sale.get(
                    "receipt",
                    "-"
                ),

                sale.get(
                    "customer",
                    "Old Customer"
                ),

                sale.get(
                    "product",
                    "-"
                ),

                sale.get(
                    "quantity",
                    0
                ),

                f"₹{sale.get('total', 0):.2f}",

                sale.get(
                    "date",
                    "-"
                )
            )
        )


# =========================================================
# ADD EXPENSE
# =========================================================

def add_expense_gui():

    window = tk.Toplevel(root)

    window.title(
        "Add Expense"
    )

    window.geometry(
        "420x330"
    )

    window.configure(
        bg=BG
    )

    tk.Label(
        window,
        text="Add Expense",
        font=("Arial", 20, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        pady=25
    )

    tk.Label(
        window,
        text="Expense Name",
        bg=BG
    ).pack()

    name_entry = tk.Entry(
        window,
        width=30,
        font=("Arial", 12)
    )

    name_entry.pack(
        pady=8
    )

    tk.Label(
        window,
        text="Amount",
        bg=BG
    ).pack()

    amount_entry = tk.Entry(
        window,
        width=30,
        font=("Arial", 12)
    )

    amount_entry.pack(
        pady=8
    )

    def add():

        name = name_entry.get().strip()

        if not name:

            messagebox.showerror(
                "Error",
                "Enter expense name."
            )

            return

        try:

            amount = float(
                amount_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid amount."
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

            "amount": amount,

            "date": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

        })

        save_data(
            EXPENSE_FILE,
            expenses
        )

        messagebox.showinfo(
            "Success",
            "Expense added successfully!"
        )

        window.destroy()

        show_dashboard()

    tk.Button(
        window,
        text="ADD EXPENSE",
        command=add,
        width=22,
        height=2
    ).pack(
        pady=25
    )


# =========================================================
# EXPENSE HISTORY
# =========================================================

def show_expenses():

    clear_content()

    tk.Label(
        content,
        text="Expense History",
        font=("Arial", 26, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=35,
        pady=25
    )

    table = ttk.Treeview(
        content,
        columns=(
            "name",
            "amount",
            "date"
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

    table.heading(
        "date",
        text="Date"
    )

    table.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=10
    )

    for expense in expenses:

        table.insert(
            "",
            "end",
            values=(

                expense.get(
                    "name",
                    "-"
                ),

                f"₹{expense.get('amount', 0):.2f}",

                expense.get(
                    "date",
                    "-"
                )
            )
        )


# =========================================================
# PROFIT
# =========================================================

def show_profit():

    clear_content()

    total_sales = sum(
        item.get("total", 0)
        for item in sales
    )

    total_expenses = sum(
        item.get("amount", 0)
        for item in expenses
    )

    profit = total_sales - total_expenses

    tk.Label(
        content,
        text="Profit Report",
        font=("Arial", 26, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        pady=35
    )

    tk.Label(
        content,
        text=f"Total Sales\n₹{total_sales:.2f}",
        font=("Arial", 20),
        bg=BG,
        fg=TEXT
    ).pack(
        pady=15
    )

    tk.Label(
        content,
        text=f"Total Expenses\n₹{total_expenses:.2f}",
        font=("Arial", 20),
        bg=BG,
        fg=TEXT
    ).pack(
        pady=15
    )

    tk.Label(
        content,
        text=f"NET PROFIT\n₹{profit:.2f}",
        font=("Arial", 25, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        pady=25
    )

# =========================================================
# SALES ANALYTICS
# =========================================================

def show_analytics():

    clear_content()

    total_revenue = sum(
        sale.get("total", 0)
        for sale in sales
    )

    total_transactions = len(sales)

    total_units = sum(
        sale.get("quantity", 0)
        for sale in sales
    )

    total_expenses = sum(
        expense.get("amount", 0)
        for expense in expenses
    )

    profit = total_revenue - total_expenses

    if total_transactions > 0:
        average_sale = (
            total_revenue / total_transactions
        )
    else:
        average_sale = 0

    # Best-selling product
    product_sales = {}

    for sale in sales:

        product = sale.get(
            "product",
            "Unknown"
        )

        quantity = sale.get(
            "quantity",
            0
        )

        product_sales[product] = (
            product_sales.get(product, 0)
            + quantity
        )

    if product_sales:

        best_product = max(
            product_sales,
            key=product_sales.get
        )

        best_quantity = product_sales[
            best_product
        ]

    else:

        best_product = "No sales yet"
        best_quantity = 0

    # Today's sales
    today = datetime.now().strftime(
        "%d-%m-%Y"
    )

    today_sales = 0

    for sale in sales:

        sale_date = sale.get(
            "date",
            ""
        )

        if sale_date.startswith(today):

            today_sales += sale.get(
                "total",
                0
            )

    # Header

    tk.Label(
        content,
        text="Sales Analytics",
        font=("Arial", 28, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=35,
        pady=(30, 5)
    )

    tk.Label(
        content,
        text="Business performance overview",
        font=("Arial", 12),
        bg=BG,
        fg=MUTED
    ).pack(
        anchor="w",
        padx=35
    )

    # Cards

    cards = tk.Frame(
        content,
        bg=BG
    )

    cards.pack(
        pady=30
    )

    create_card(
        cards,
        "Total Revenue",
        f"₹{total_revenue:.2f}"
    )

    create_card(
        cards,
        "Transactions",
        str(total_transactions)
    )

    create_card(
        cards,
        "Units Sold",
        str(total_units)
    )

    row2 = tk.Frame(
        content,
        bg=BG
    )

    row2.pack(
        pady=10
    )

    create_card(
        row2,
        "Today's Sales",
        f"₹{today_sales:.2f}"
    )

    create_card(
        row2,
        "Average Sale",
        f"₹{average_sale:.2f}"
    )

    create_card(
        row2,
        "Profit",
        f"₹{profit:.2f}"
    )

    # Best seller section

    best_frame = tk.Frame(
        content,
        bg=CARD,
        highlightbackground="#d9dde3",
        highlightthickness=1
    )

    best_frame.pack(
        fill="x",
        padx=35,
        pady=25
    )

    tk.Label(
        best_frame,
        text="🏆 Best-Selling Product",
        font=("Arial", 16, "bold"),
        bg=CARD,
        fg=TEXT
    ).pack(
        pady=(20, 8)
    )

    tk.Label(
        best_frame,
        text=(
            f"{best_product}  —  "
            f"{best_quantity} units sold"
        ),
        font=("Arial", 18),
        bg=CARD,
        fg=TEXT
    ).pack(
        pady=(0, 20)
    )
# =========================================================
# SEARCH
# =========================================================

def search_product():

    window = tk.Toplevel(root)

    window.title(
        "Search Product"
    )

    window.geometry(
        "450x300"
    )

    tk.Label(
        window,
        text="Search Product",
        font=("Arial", 20, "bold")
    ).pack(
        pady=25
    )

    entry = tk.Entry(
        window,
        width=30,
        font=("Arial", 12)
    )

    entry.pack(
        pady=10
    )

    result = tk.Label(
        window,
        text="",
        font=("Arial", 12)
    )

    result.pack(
        pady=20
    )

    def search():

        query = entry.get().lower().strip()

        found = []

        for name, data in products.items():

            if query in name.lower():

                found.append(
                    f"{name} | "
                    f"₹{data['price']:.2f} | "
                    f"Stock: {data['quantity']}"
                )

        if found:

            result.config(
                text="\n".join(found)
            )

        else:

            result.config(
                text="Product not found."
            )

    tk.Button(
        window,
        text="SEARCH",
        command=search,
        width=18
    ).pack()


# =========================================================
# LOW STOCK
# =========================================================

def show_low_stock():

    clear_content()

    tk.Label(
        content,
        text="Low Stock Alerts",
        font=("Arial", 26, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=35,
        pady=25
    )

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
                font=("Arial", 16),
                bg=BG,
                fg=TEXT
            ).pack(
                anchor="w",
                padx=50,
                pady=8
            )

    if not found:

        tk.Label(
            content,
            text="✓ No low-stock products.",
            font=("Arial", 16),
            bg=BG,
            fg=TEXT
        ).pack(
            pady=30
        )


# =========================================================
# SIDEBAR
# =========================================================

sidebar = tk.Frame(
    root,
    bg=SIDEBAR,
    width=220
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="SMART SHOP",
    font=("Arial", 20, "bold"),
    bg=SIDEBAR,
    fg="white"
).pack(
    pady=(35, 5)
)

tk.Label(
    sidebar,
    text="MANAGER",
    font=("Arial", 10),
    bg=SIDEBAR,
    fg="#aeb8c7"
).pack(
    pady=(0, 30)
)


def make_button(text, command):

    tk.Button(
        sidebar,
        text=text,
        command=command,
        width=22,
        height=2,
        bg=SIDEBAR,
        fg="white",
        activebackground="#344054",
        activeforeground="white",
        relief="flat",
        font=("Arial", 10, "bold")
    ).pack(
        pady=3
    )


make_button(
    "Dashboard",
    show_dashboard
)

make_button(
    "Add Product",
    add_product_gui
)

make_button(
    "Products",
    show_products
)

make_button(
    "Record Sale",
    record_sale_gui
)

make_button(
    "Sales History",
    show_sales
)

make_button(
    "Add Expense",
    add_expense_gui
)

make_button(
    "Expenses",
    show_expenses
)

make_button(
    "Profit",
    show_profit
)
make_button(
    "Sales Analytics",
    show_analytics
)
make_button(
    "Search",
    search_product
)

make_button(
    "Low Stock",
    show_low_stock
)


# =========================================================
# START APPLICATION
# =========================================================

show_dashboard()

root.mainloop()