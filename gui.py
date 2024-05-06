from collections import defaultdict
from tkinter import (
    ttk,
    messagebox,
    Frame,
    Label,
    Button,
    Tk,
    BOTH,
)
import json
import random
import time
import re

GEOMETRY = "1024x768+0+0"


class ShopUI:
    def __init__(self, parent):
        self.cart: list = []
        self.parent = parent
        self.parent.title("Shop Management System")
        self.parent.geometry(GEOMETRY)

        # Set light blue background
        self.shop_frame = Frame(self.parent, bg="light blue")
        self.shop_frame.pack(fill=BOTH, expand=True)

        self.removed_product_name = None

        self.shop_heading = Label(
            self.shop_frame,
            text="Shop Management System",
            font=("Unispace", 30, "bold"),
            bg="light blue",
            fg="#333",
        )
        self.shop_heading.pack(pady=(20, 40), anchor="w")  # Anchor to the left

        # Frame to hold product selection widgets
        self.product_frame = Frame(self.shop_frame, bg="light blue")
        self.product_frame.pack(pady=(0, 20), anchor="w")  # Anchor to the left

        self.new_customer_button = Button(
            self.parent,
            text="New Customer",
            command=self.restart_program,
            bg="#4CAF50",
            fg="#FFF",
            font=("Unispace", 14),
        )
        self.new_customer_button.place(x=860, y=0)

        self.fetch_button = Button(
            self.product_frame,
            text="Fetch Product",
            font=("Unispace", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.fetch_product,
        )
        self.fetch_button.grid(
            row=0, column=0, padx=(20, 10), sticky="w"
        )  # Shift to the left

        self.product_drop_down_box = ttk.Combobox(
            self.product_frame,
            width=50,
            font=("Unispace", 14),
            state="readonly",
        )
        self.product_drop_down_box.grid(
            row=1, column=0, columnspan=3, padx=(20, 20), pady=10, sticky="ew"
        )

        # Bind the function to update product details when an item is selected
        self.product_drop_down_box.bind(
            "<<ComboboxSelected>>", self.update_product_details
        )

        # Frame to display product details
        self.details_frame = Frame(self.shop_frame, bg="light blue")
        self.details_frame.pack(pady=20, anchor="w")  # Anchor to the left

        self.product_name_label = Label(
            self.details_frame,
            text="Product Name:",
            font=("Unispace", 14),
            bg="light blue",
        )
        self.product_name_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.product_name_value = Label(
            self.details_frame,
            text="",
            font=("Unispace", 14),
            bg="light blue",
        )
        self.product_name_value.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.price_label = Label(
            self.details_frame,
            text="Price:",
            font=("Unispace", 14),
            bg="light blue",
        )
        self.price_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.price_value = Label(
            self.details_frame,
            text="",
            font=("Unispace", 14),
            bg="light blue",
        )
        self.price_value.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.quantity_label = Label(
            self.details_frame,
            text="",
            font=("Unispace", 14),
            bg="light blue",
        )
        self.quantity_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        # Button to buy product
        self.buy_button = Button(
            self.shop_frame,
            text="Add to Cart",
            font=("Unispace", 16, "bold"),
            bg="#FF5722",
            fg="white",
            command=self.buy_product,
        )
        self.buy_button.pack(pady=10, anchor="w")  # Anchor to the left

        # Button to remove product
        self.remove_button = Button(
            self.shop_frame,
            text="Remove from Cart",
            font=("Unispace", 16, "bold"),
            bg="#FF5722",
            fg="white",
            command=self.remove_product,
        )
        self.remove_button.pack(pady=10, anchor="w")  # Anchor to the left

        self.remove_button = Button(
            self.shop_frame,
            text="",
            font=("Unispace", 16, "bold"),
            bg="#FF5722",
            fg="white",
            command=self.cart.clear,
        )
        # Cart Counter
        self.cart_counter_label = Label(
            self.shop_frame,
            text="",
            font=("Unispace", 14),
            bg="light blue",
        )
        self.cart_counter_label.pack(pady=5, anchor="w")  # Anchor to the left

        self.cart_counter_value = Label(
            self.shop_frame,
            text="",
            font=("Unispace", 14),
            bg="light blue",
        )
        self.cart_counter_value.pack(pady=5, anchor="w")  # Anchor to the left

        # Generate Receipt Button
        self.generate_receipt_button = Button(
            self.shop_frame,
            text="Generate Receipt",
            font=("Unispace", 16, "bold"),
            bg="#2196F3",
            fg="white",
            command=lambda: (
                self.generate_receipt(),
                self.product_counter.clear(),
                self.cart.clear(),
            ),
        )
        self.generate_receipt_button.pack(pady=10, anchor="w")  # Anchor to the left

        self.product_counter = defaultdict(int)

        self.preview_frame = Frame(self.shop_frame, bg="light blue")
        self.preview_frame.place(x=700, y=250)

        # Create the treeview widget for the preview table
        self.preview_tree = ttk.Treeview(
            self.preview_frame, columns=("Name", "Quantity", "Price", "Total")
        )
        self.preview_tree.heading("#0", text="ID")
        self.preview_tree.heading("Name", text="Name")
        self.preview_tree.heading("Quantity", text="Quantity")
        self.preview_tree.heading("Price", text="Price")
        self.preview_tree.heading("Total", text="Total")
        self.preview_tree.column("#0", width=50)
        self.preview_tree.column("Name", width=200)
        self.preview_tree.column("Quantity", width=100)
        self.preview_tree.column("Price", width=100)
        self.preview_tree.column("Total", width=100)
        self.preview_tree.pack(fill=BOTH, expand=True)

        # Button to clear the preview table
        self.clear_preview_button = Button(
            self.preview_frame,
            text="Clear Cart",
            font=("Unispace", 14, "bold"),
            bg="#FF5722",
            fg="white",
            command=lambda: (
                self.clear_preview(),
                self.cart.clear(),
                self.product_counter.clear(),
            ),
        )
        self.clear_preview_button.pack(pady=10)
        self.generate_report_button = Button(
            self.shop_frame,
            text="",
            font=("Unispace", 16, "bold"),
            bg="#2196F3",
            fg="white",
            command=(
                lambda: (
                    self.generate_sales_report_content(),
                    self.product_counter.clear(),
                    self.cart.clear(),
                ),
            ),  # Bind the method here
        )

    def update_preview_table(self):
        # Clear the existing items in the preview table
        self.preview_tree.delete(*self.preview_tree.get_children())

        # Dictionary to store the total quantity for each item
        total_quantity_dict = defaultdict(int)

        # Calculate total quantity for each item in the cart
        for item in self.cart:
            name = item["NAME"]
            total_quantity_dict[name] += 1

        # Populate the preview table with unique items and their total quantities
        for name, total_quantity in total_quantity_dict.items():
            item = self.get_product_details(name)
            if item:
                TAX = float(item["TAX"]) / 100.0
                price = round(float(item["PRICE"]), 2)
                total = total_quantity * price
                total += total * TAX
                total = round(total, 2)
                item_id = item["ID"]

                # Insert or update the entry in the preview table
                self.preview_tree.insert(
                    "",
                    "end",
                    text=str(item_id),
                    values=(name, total_quantity, price, total),
                )

                # Check if the product's quantity has reached zero
                if total_quantity == 0:
                    # Remove the entry from the preview table
                    self.remove_entry_from_preview(name)
            else:
                # If the product details are not found, remove it from the cart
                self.remove_product_from_cart(name)

        # Reset the removed_product_name attribute
        self.removed_product_name = None

    def remove_entry_from_preview(self, product_name):
        # Find and delete the entry from the preview table
        for child in self.preview_tree.get_children():
            values = self.preview_tree.item(child)["values"]
            if values[0] == product_name:
                self.preview_tree.delete(child)
                break

    def remove_product_from_cart(self, product_name):
        # Remove the product from the cart
        self.cart = [item for item in self.cart if item["NAME"] != product_name]

    def clear_preview(self):
        # Clear the preview table
        self.preview_tree.delete(*self.preview_tree.get_children())
        self.preview_tree.update()

    def fetch_product(self):
        # Fetch product names and IDs from data source
        product_names_and_ids = self.get_product_names_and_ids()

        # Clear the existing items in the dropdown
        self.product_drop_down_box["values"] = ()

        # Populate the dropdown with fetched product names and IDs
        if product_names_and_ids:
            self.product_drop_down_box["values"] = product_names_and_ids
            self.product_drop_down_box.current(0)  # Select the first item by default

    def update_quantity_label(self, selected_product_name):
        quantity = self.product_counter[selected_product_name]
        self.quantity_label.config(text=f"")

    def get_product_names_and_ids(self):
        try:
            with open("./DB/shop_items.json", "r") as file:
                items = json.load(file)
                product_names_and_ids = [item["NAME"] for item in items]
                return product_names_and_ids
        except FileNotFoundError:
            print("Error: Products file not found.")
            return []
        except json.JSONDecodeError:
            print("Error: Unable to decode JSON data.")
            return []

    def buy_product(self):
        selected_product_name = self.product_drop_down_box.get()
        if selected_product_name:
            product_details = self.get_product_details(selected_product_name)
            if product_details:
                if product_details["STOCK"] > 0:
                    self.cart.append(product_details)
                    self.product_counter[selected_product_name] += 1
                    self.update_cart_counter()
                    self.update_quantity_label(selected_product_name)
                else:
                    messagebox.showwarning("Warning", "Product is out of stock.")
            else:
                messagebox.showerror("Error", "Product details not found.")
        else:
            messagebox.showerror("Error", "Please select a product to add.")
        self.update_preview_table()

    def remove_product(self):
        selected_product_name = self.product_drop_down_box.get()
        if selected_product_name:
            if selected_product_name in self.product_counter:
                if self.product_counter[selected_product_name] > 0:
                    # Decrement the quantity of the selected product in the cart
                    self.product_counter[selected_product_name] -= 1

                    # Update the preview table

                    # Reset the removed_product_name attribute
                    self.removed_product_name = selected_product_name

                    self.update_preview_table()
                    # Update the cart counter
                    self.update_cart_counter()

                    # Update the quantity label for the selected product
                    self.update_quantity_label(selected_product_name)
                else:
                    messagebox.showwarning(
                        "Warning", "Product quantity is already zero."
                    )
            else:
                messagebox.showerror("Error", "Product not found in cart.")
        else:
            messagebox.showerror("Error", "Please select a product to remove.")

    def update_cart_counter(self):
        self.cart_counter_value.config(text="")

    def generate_receipt(self) -> str:
        receipt_file_path = f"./Receipts/Bill--{int(time.time())}.txt"
        self.bill(receipt_file_path)
        self.clear_preview()
        return receipt_file_path

    def get_product_price(self, product_name):
        try:
            with open("./DB/shop_items.json", "r") as file:
                items = json.load(file)
                for item in items:
                    if item["NAME"] == product_name:
                        return float(item["PRICE"])
        except FileNotFoundError:
            print("Error: Products file not found.")
            return None
        except json.JSONDecodeError:
            print("Error: Unable to decode JSON data.")
            return None

    def get_product_tax(self, product_name):
        try:
            with open("./DB/shop_items.json", "r") as f:
                items = json.load(f)
                for item in items:
                    if item["NAME"] == product_name:
                        return item["TAX"]
        except FileNotFoundError:
            print("Error: Products file not found.")
            return None
        except json.JSONDecodeError:
            print("Error: Unable to decode JSON data.")
            return None

    def bill(self, file_path) -> dict:
        if not bool(self.product_counter):
            print("Cart is empty!")
            messagebox.showerror(title="Error", message="Cart is empty!")
            return "Cart is empty!"
        new_cart = self.product_counter
        with open("./DB/receipt_no.json", "r") as F:
            data_F = json.load(F)
        receipt_no = data_F[0]["receipt_no"]
        try:
            with open(file_path, "w") as bill_file:
                bill_file.write("\t\t\t\t\t\t\t\t\tShop Management System\n")
                bill_file.write("\t\t\t\t\t\t\t\t\tLahore, PK\n")
                bill_file.write(
                    f"\t\t\t\t\t\t\t\t\t+92 {random.randint(100, 999)} {random.randint(1000000, 9999999)}\n"
                )
                bill_file.write(f"\t\t\t\t\t\t\t\t\tRECEIPT No. {int(receipt_no)}\n\n")
                bill_file.write(
                    "\t\t\t\t\t----------------------------------------------------------------------\n"
                )
                bill_file.write(
                    f"\t\t\t\t\t#\t\tName\t\t\t\t\t\tQuantity\t\tTax(%)\t\tAmount (Rs.)\n"
                )
                total_price = 0

                for i, (name, quantity) in enumerate(
                    self.product_counter.items(), start=1
                ):
                    price = int(self.get_product_price(name) * quantity)
                    TAX = self.get_product_tax(name)
                    total_price += price
                    price_init: list = []
                    with open("./DB/shop_items.json", "r") as f:
                        items = json.load(f)
                        for item in items:
                            if item["NAME"] == name:
                                price_init.append(item["RETAIL_PRICE"])
                    net_total = float(sum(price_init)) * quantity
                    grand_total = int(total_price)
                    data = f"\t\t\t\t\t{i}\t\t{name}\t\t\t\t\t\t{quantity}\t\t\t\t\t\t{TAX}\t\t\t\t\t\t{price}\n"
                    bill_file.write(data)

                final = f"\n\n\t\t\t\t\n\n\n\t\t\t\t\tGrand Total: Rs.{round(grand_total, 2)}\n\n\t\t\t\tTax: 17%"
                fbr_invoice_num = f"\n\t\t\t\t\tFBR Invoice Number: {random.randint(1000000000000, 10000000000000)}"
                bill_file.write(
                    "\n\t\t\t\t\t----------------------------------------------------------------------\n"
                )
                bill_file.write(final)
                bill_file.write(fbr_invoice_num)
                messagebox.showinfo("Receipt", "Bill generated!")
                receipt_no += 1
                data_F[0]["receipt_no"] = receipt_no
                with open("./DB/receipt_no.json", "w") as file_json:
                    json.dump(data_F, file_json)
            return new_cart

        except Exception as e:
            messagebox.showerror(title="Error", message=str(e))
            return "Error creating bill."

    def update_product_details(self, event=None):
        selected_product = self.product_drop_down_box.get()
        if selected_product:
            product_details = self.get_product_details(selected_product)
            if product_details:
                self.product_name_value.config(text=product_details["NAME"])
                self.price_value.config(text=f"Rs.{product_details['PRICE']:.2f}")
                self.update_quantity_label(selected_product)  # Update quantity label
            else:
                messagebox.showerror("Error", "Product details not found.")
        else:
            self.product_name_value.config(text="")
            self.price_value.config(text="")

    def restart_program(self):
        self.parent.destroy()

        root = Tk()
        admin_app = ShopUI(root)

        # Configure the UI to always launch maximized
        root.wm_state("zoomed")

        root.mainloop()

    def get_product_details(self, product_name):
        try:
            with open("./DB/shop_items.json", "r") as file:
                items = json.load(file)
                for item in items:
                    if item["NAME"] == product_name:
                        return item
            return None
        except FileNotFoundError:
            print("Error: Products file not found.")
            return None
        except json.JSONDecodeError:
            print("Error: Unable to decode JSON data.")
            return None

    def append_to_sales_report(self, cart):
        sales_report_file = "./Reports/SalesReport.txt"
        if not cart:
            print("No cart information to append.")
            return

        try:
            with open(sales_report_file, "a") as report_file:
                for item in cart:
                    product_name = item["NAME"]
                    quantity = self.product_counter[product_name]
                    price = float(item["PRICE"])
                    tax = float(item["TAX"])
                    total_price = round((price * quantity) * (1 + tax / 100), 2)
                    line = f"{product_name},{quantity},{total_price}\n"
                    report_file.write(line)
        except Exception as e:
            messagebox.showerror(
                f"Error:",
                f"Failed to append cart information to sales report file '{sales_report_file}': {e}",
            )

    def generate_sales_report_content(self):
        # Initialize variables to store sales data
        total_sales = 0
        product_sales: defaultdict = (
            self.bill()
        )  # Dictionary to store sales for each product

        # Iterate over all files in the Receipts directory
        receipts_dir = f"./Receipts/{self.generate_receipt()}"
        with open(receipts_dir, "r") as bill_file:
            bill_content = bill_file.read()

        # Extract product-wise sales information using regular expressions
        matches = re.findall(r"- (.+?): Rs\.(\d+\.\d+)", bill_content)
        if matches:
            for product_name, sales_amount in matches:
                sales = float(sales_amount)
                quantity = int(
                    re.search(r"(\d+)", product_name).group(1)
                )  # Extract quantity from product name
                total_sales += sales
                product_sales[product_name] += quantity * sales

        # Generate the sales report content
        sales_report_content = "Sales Report\n\n"
        sales_report_content += f"Date: {time.strftime('%Y-%m-%d')}\n\n"
        sales_report_content += f"Total Sales: ${total_sales:.2f}\n\n"
        sales_report_content += "Product-wise Sales:\n"

        # Add product-wise sales to the report content
        for product_name, sales in product_sales.items():
            sales_report_content += f"- {product_name}: ${sales:.2f}\n"

        # Save the sales report to the Reports directory
        current_time = int(time.time())
        report_filename = f"./Reports/Report--{current_time}.txt"
        with open(report_filename, "w") as report_file:
            report_file.write(sales_report_content)

        return report_filename


if __name__ == "__main__":
    root = Tk()
    admin_app = ShopUI(root)

    # Configure the UI to always launch maximized
    root.wm_state("zoomed")

    root.mainloop()
