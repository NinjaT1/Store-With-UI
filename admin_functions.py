from tkinter import END, Tk, Frame, Button, Label, Entry, Checkbutton, BooleanVar
import json
import random
from pathlib import Path

FILE_PATH = Path("./DB/shop_items.json")
TAX = 1.17


class AdminFunctions:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Admin Functions")
        self.parent.geometry("1024x768+0+0")
        self.parent.configure(bg="light blue")

        self.admin_frame = Frame(self.parent, bg="light blue")
        self.admin_frame.pack(fill="both", expand=True)

        self.heading = Label(
            self.admin_frame,
            text="Manage Shop Database",
            font=("Unispace", 30),
            bg="light blue",
        )
        self.heading.pack(pady=50)

        self.items = self.load_items_from_file(FILE_PATH)

        self.success_label = Label(
            self.admin_frame,
            text="",
            bg="light blue",
            fg="green",
            font=("Unispace", 14),
        )
        self.success_label.pack(pady=10)

        entry_frame = Frame(self.admin_frame, bg="light blue")
        entry_frame.pack(pady=20)

        name_label = Label(
            entry_frame, text="Product Name:", bg="light blue", font=("Unispace", 14)
        )
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.name_entry = Entry(entry_frame, font=("Unispace", 14), width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        price_label = Label(
            entry_frame, text="Price:", bg="light blue", font=("Unispace", 14)
        )
        price_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.price_entry = Entry(entry_frame, font=("Unispace", 14), width=30)
        self.price_entry.grid(row=1, column=1, padx=10, pady=10)

        stock_label = Label(
            entry_frame, text="Stock:", bg="light blue", font=("Unispace", 14)
        )
        stock_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.stock_entry = Entry(entry_frame, font=("Unispace", 14), width=30)
        self.stock_entry.grid(row=2, column=1, padx=10, pady=10)

        self.check_var: bool = BooleanVar()
        self.tax_label_entry = Checkbutton(
            entry_frame,
            text="Add Tax",
            variable=self.check_var,
            padx=10,
            pady=10,
            font=("Unispace", 15),
            bg="light blue",
        )
        self.tax_label_entry.grid(row=3, column=1, padx=10, pady=10)

        add_button = Button(
            entry_frame,
            text="Add Item",
            font=("Unispace", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            command=lambda: (
                self.add_item(),
                self.name_entry.delete(0, END),
                self.price_entry.delete(0, END),
                self.stock_entry.delete(0, END),
                self.check_var.set(False),
            ),
        )
        add_button.grid(row=4, columnspan=2, pady=20)

        remove_label = Label(
            entry_frame,
            text="Enter Product Name to Remove:",
            bg="light blue",
            font=("Unispace", 14),
        )

        remove_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.remove_entry = Entry(entry_frame, font=("Unispace", 14), width=30)
        self.remove_entry.grid(row=5, column=1, padx=10, pady=10)

        remove_stock_label = Label(
            entry_frame,
            text="Enter Units to Remove:",
            bg="light blue",
            font=("Unispace", 14),
        )

        remove_stock_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.remove_stock_entry = Entry(entry_frame, font=("Unispace", 14), width=30)
        self.remove_stock_entry.grid(row=6, column=1, padx=10, pady=10)

        self.remove_reason_label = Label(
            entry_frame,
            text="Enter reason for removal:",
            bg="light blue",
            font=("Unispace", 14),
        )

        self.remove_reason_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.remove_reason_entry = Entry(entry_frame, font=("Unispace", 14), width=30)
        self.remove_reason_entry.grid(row=7, column=1, padx=10, pady=10)

        remove_button = Button(
            entry_frame,
            text="Remove Item",
            font=("Unispace", 14, "bold"),
            bg="red",
            fg="white",
            command=lambda: (
                self.remove_item(),
                self.remove_stock_entry.delete(0, END),
                self.remove_entry.delete(0, END),
            ),
        )
        remove_button.grid(row=8, columnspan=2, pady=20)

    def load_items_from_file(self, file_path):
        try:
            with open(file_path, "r") as json_file:
                items = json.load(json_file)
                return items
        except FileNotFoundError:
            with open(file_path, "x") as f:
                f.close()
            print("No file found! Created new empty file!")
            return []
        except json.JSONDecodeError:
            print("Error: The file contains invalid JSON data.")
            return []

    def save_items_to_file(self, items, file_path):
        try:
            with open(file_path, "w") as json_file:
                json.dump(items, json_file, indent=4)
        except Exception as e:
            print(f"Error saving items to file: {e}")

    def shop_entry(self):
        pass

    def add_item(self):
        name: str = str(self.name_entry.get())
        sales_price: float = float(self.price_entry.get())
        stock: int = int(self.stock_entry.get())
        if self.check_var.get():
            retail_price = float(sales_price / TAX)
            sales_price += 0.0
        else:
            retail_price: float = 0
            sales_price = retail_price

        if name and sales_price and stock:
            try:
                sales_price = float(sales_price)
                stock = int(stock)
            except ValueError:
                self.show_message("Error: Price and Stock must be numbers.", "red")
                return

            # Check if the item already exists in the list
            existing_item = next(
                (item for item in self.items if item["NAME"] == name), None
            )
            if existing_item:
                existing_item["STOCK"] += stock
                self.save_items_to_file(self.items, FILE_PATH)
                self.show_message(
                    f"{stock} units of {name} added to inventory.", "green"
                )
            else:
                new_item = {
                    "ID": random.randint(100, 999),
                    "NAME": name,
                    "STOCK": stock,
                    "PRICE": round(sales_price, 2),
                    "RETAIL_PRICE": round(retail_price, 2),
                    "TAX": round(((TAX - 1.00) * 100.0), 2),
                }
                self.items.append(new_item)
                self.save_items_to_file(self.items, FILE_PATH)
                self.show_message(f"{name} added successfully.", "green")
        else:
            self.show_message("Error: Please fill in all fields.", "red")

    def remove_item(self):
        name_to_remove = self.remove_entry.get()
        stock_to_remove = int(self.remove_stock_entry.get())
        if name_to_remove:
            found = False
            for item in self.items:
                if item["NAME"] == name_to_remove:
                    if stock_to_remove >= item["STOCK"]:
                        self.items.remove(item)
                    else:
                        item["STOCK"] -= stock_to_remove
                    self.save_items_to_file(self.items, FILE_PATH)
                    self.show_message(
                        f"{stock_to_remove} units of {name_to_remove} removed from inventory.",
                        "green",
                    )
                    found = True
                    break
            if not found:
                self.show_message(f"Error: {name_to_remove} not found.", "red")
        else:
            self.show_message("Error: Please enter a product name to remove.", "red")

    def show_message(self, message, color):
        self.success_label.config(text=message, fg=color)
        self.success_label.after(1000, lambda: self.success_label.config(text=""))

    def removal_reason(self):
        item = self.remove_entry.get()
        reason = self.remove_reason.get()


if __name__ == "__main__":
    root = Tk()
    admin = AdminFunctions(root)
    root.wm_state("zoomed")
    root.mainloop()
