from tkinter import *
from tkinter import messagebox
from admin_functions import FILE_PATH, AdminFunctions
from itemViews import ItemViewer
from gui import ShopUI
import json


class About:
    @staticmethod
    def show_about():
        about_text = """
        Shop Management System
        
        Version: 1.0
        
        About:
        The Shop Management System is a desktop application designed to streamline 
        the management of retail operations. It provides functionalities for 
        inventory management, sales tracking, and reporting.
        
        Features:
        - Add, edit, and delete products from inventory
        - Conduct sales transactions and generate receipts
        - Generate reports on sales, inventory levels, and revenue
        
        Developed by: Mirza Ali Raza (2023-CE-42)
        """

        about_window = Toplevel(root)
        about_window.title("About Shop Management System")

        text = Text(about_window, wrap=WORD)
        text.pack(fill=BOTH, expand=True)

        text.insert(END, about_text)
        text.config(state=DISABLED)


class Login:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Login - Shop Management System")
        self.parent.geometry("1024x768+0+0")
        self.parent.configure(bg="light blue")

        self.login_frame = Frame(self.parent, bg="light blue")
        self.login_frame.pack(pady=50)  # Login Background

        # Title
        self.title = Label(
            self.login_frame,
            text="Login to Shop Management System",
            font=("Unispace", 30),
            bg="light blue",
        )
        self.title.grid(row=0, columnspan=2, padx=10, pady=10)

        # Username and Password Labels and Entries.
        self.usr_label = Label(
            self.login_frame,
            text="Username:",
            font=("Unispace", 20),
            bg="light blue",
        )
        self.usr_label.grid(row=1, column=0, padx=10, pady=10, sticky=E)
        self.usr_entry = Entry(self.login_frame, width=20)
        self.usr_entry.grid(row=1, column=1, padx=10, pady=10)

        self.pw_label = Label(
            self.login_frame,
            text="Password:",
            font=("Unispace", 20),
            bg="light blue",
        )
        self.pw_label.grid(row=2, column=0, padx=10, pady=10, sticky=E)
        self.pw_entry = Entry(self.login_frame, width=20, show="*")
        self.pw_entry.grid(row=2, column=1, padx=10, pady=10)

        # Login and restart buttons.
        self.login_button = Button(
            self.login_frame,
            text="Login",
            command=self.authenticate,
            font=("Unispace", 20),
            bg="light blue",
        )
        self.login_button.grid(row=3, columnspan=2, padx=10, pady=10)

        self.restart_button = Button(
            self.parent,
            text="Restart",
            command=self.restart,
            font=("Unispace", 16),
            bg="red",
            fg="white",
            padx=10,
            pady=5,
        )
        self.restart_button.place(x=1410, y=0)

        self.signup_button = Button(
            self.login_frame,
            text="Sign Up",
            command=self.signup,
            font=("Unispace", 20),
            bg="light blue",
        )
        self.signup_button.grid(row=4, columnspan=2, padx=10, pady=10)

        # Credentials file path.
        self.credentials_file = "./usr/users.json"

    def restart(self):
        """Restart application"""
        self.parent.destroy()
        root = Tk()
        login_window = Login(root)
        root.wm_state("zoomed")
        root.mainloop()

    def authenticate(self):
        username = self.usr_entry.get()
        password = self.pw_entry.get()

        user_credentials = self.read_credentials()

        for user_data in user_credentials:
            if user_data["username"] == username and user_data["password"] == password:
                # Successful authentication
                self.login_successful(user_data["role"])
                return
        # If authentication fails...
        messagebox.showerror("Login Failed", "Invalid username or password.")

    def read_credentials(self):
        """Read the credentials from a JSON file."""
        try:
            with open(self.credentials_file, "r") as file:
                user_credentials = json.load(file)
                return user_credentials
        except FileNotFoundError:
            with open("./usr/users.json", "x") as f_json:
                f_json.close()
            print("Error: User credentials file not found.")
            return []
        except Exception as e:
            print(f"Error reading user credentials: {e}")
            return []

    def save_credentials(self, user_credentials) -> None:
        try:
            with open(self.credentials_file, "w") as file:
                json.dump(user_credentials, file, indent=4)
        except Exception as e:
            print(f"Error saving user credentials: {e}")

    def login_successful(self, role) -> None:
        self.parent.destroy()
        root = Tk()
        # Depending on the role, open the appropriate window
        if role == "stock":
            admin_window = AdminFunctions(root)
            root.wm_state("zoomed")
        elif role == "items":
            item_viewer = ItemViewer(root, FILE_PATH)
            root.wm_state("zoomed")
        elif role == "shop":
            shop = ShopUI(root)
            root.wm_state("zoomed")
        root.mainloop()

    def signup(self) -> None:
        username = self.usr_entry.get()
        password = self.pw_entry.get()

        # Read credentials
        user_credentials = self.read_credentials()

        # Check if username already exists
        for user_data in user_credentials:
            if user_data["username"] == username:
                messagebox.showerror("Sign Up Failed", "Username already exists.")
                return

        role = self.choose_role()

        user_credentials.append(
            {"username": username, "password": password, "role": role}
        )

        # Save updated credentials...
        self.save_credentials(user_credentials)

        messagebox.showinfo(
            "Sign Up Successful", f"User '{username}' signed up with role: {role}."
        )

    def choose_role(self) -> str:
        """Choose role for new user."""
        role_dialog = Toplevel(self.parent)
        role_dialog.title("Choose Role")
        role_dialog.geometry("300x200")

        label = Label(role_dialog, text="Select Role:", font=("Unispace", 16))
        label.pack(pady=10)

        role = StringVar()
        role.set("shop")  # Default role is shop manager

        admin_radio = Radiobutton(
            role_dialog, text="Stock Manager", variable=role, value="stock"
        )
        admin_radio.pack(anchor=W)
        viewer_radio = Radiobutton(
            role_dialog, text="Inventory Manager", variable=role, value="items"
        )
        viewer_radio.pack(anchor=W)
        items_radio = Radiobutton(
            role_dialog, text="Shop Manager", variable=role, value="shop"
        )
        items_radio.pack(anchor=W)

        confirm_button = Button(
            role_dialog,
            text="Confirm",
            command=role_dialog.destroy,
            font=("Unispace", 14),
        )
        confirm_button.pack(pady=10)

        role_dialog.grab_set()  # Ensure focus on the dialog
        role_dialog.wait_window()  # Wait for user input

        return role.get()


# Entry point of the application
root = Tk()
login_window = Login(root)
root.wm_state("zoomed")

# Create a button to show the about information
about_button = Button(
    root,
    text="About",
    command=About.show_about,
    font=("Unispace", 20),
    bg="light blue",
)
about_button.pack(pady=10)

root.mainloop()
