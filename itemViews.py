import json
from tkinter import Tk, Frame, Label, ttk

GEOMETRY = "1024x768+0+0"


class ItemViewer:
    def __init__(self, item_viewer_page, filename) -> None:
        self.item_viewer_page = item_viewer_page
        self.item_viewer_page.title("Inventory - Shop Management System")
        self.item_viewer_page.geometry(GEOMETRY)
        self.item_viewer_page.configure(bg="light blue")

        self.item_frame = Frame(self.item_viewer_page, bg="light blue")
        self.item_frame.pack(pady=50)

        self.title = Label(
            self.item_frame,
            text="Inventory",
            font=("Unispace", 30),
            bg="light blue",
            justify="center",
        )
        self.title.grid(row=0, columnspan=3, padx=10, pady=10)

        self.tree = ttk.Treeview(
            self.item_frame, columns=("Item", "Price (Rs.)", "Stock"), show="headings"
        )
        self.tree.grid(row=1, column=0, columnspan=3, padx=10)

        self.tree.heading("Item", text="Item")
        self.tree.heading("Price (Rs.)", text="Price (Rs.)")
        self.tree.heading("Stock", text="Stock")

        self.filename = filename
        self.load_items_from_file()
        self.display_items()

    def load_items_from_file(self):
        try:
            with open(self.filename, "r") as file:
                items_data = json.load(file)

            self.items = []
            for item_data in items_data:
                item = {
                    "name": item_data["NAME"],
                    "price": item_data["PRICE"],
                    "stock": item_data["STOCK"],
                }
                self.items.append(item)
        except FileNotFoundError:
            print("Error: File not found.")
            self.items = []
        except json.JSONDecodeError:
            print("Error: Unable to decode JSON data.")
            self.items = []

    def display_items(self):
        for item in self.items:
            self.tree.insert(
                "", "end", values=(item["name"], item["price"], item["stock"])
            )


def main_inventory():

    root = Tk()
    filename = "./DB/shop_items.json"
    item_viewer = ItemViewer(root, filename)
    root.wm_state("zoomed")
    root.mainloop(item_viewer)
