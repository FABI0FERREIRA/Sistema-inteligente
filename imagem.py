import pymongo
import tkinter as tk
from tkinter import messagebox

class CadastreLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de usuario")

        # Variables for registration
        self.id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.number_var = tk.StringVar()
        self.objeto_var = tk.StringVar()



        # Variables for login
        self.login_email_var = tk.StringVar()
        self.login_password_var = tk.StringVar()

        # Registration frame
        registration_frame = tk.Frame(root)
        registration_frame.pack(padx=10, pady=10)


        tk.Label(registration_frame, text="Name:").grid(row=0, column=0, sticky="w")
        tk.Entry(registration_frame, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(registration_frame, text="E-mail:").grid(row=1, column=0, sticky="w")
        tk.Entry(registration_frame, textvariable=self.email_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(registration_frame, text="Password:").grid(row=2, column=0, sticky="w")
        tk.Entry(registration_frame, textvariable=self.password_var, show="*").grid(row=2, column=1, padx=10, pady=5)

        tk.Label(registration_frame, text="Number:").grid(row=3, column=0, sticky="w")
        tk.Entry(registration_frame, textvariable=self.number_var).grid(row=3, column=1, padx=10, pady=5)

        tk.Label(registration_frame, text="Objeto:").grid(row=4, column=0, sticky="w")
        tk.Entry(registration_frame, textvariable=self.objeto_var).grid(row=4, column=1, padx=10, pady=5)

        tk.Button(registration_frame, text="Register", command=self.register_user).grid(row=5, column=0, columnspan=2, pady=10)

        # Login frame
        login_frame = tk.Frame(root)
        login_frame.pack(padx=10, pady=10)

        tk.Label(login_frame, text="E-mail:").grid(row=0, column=0, sticky="w")
        tk.Entry(login_frame, textvariable=self.login_email_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky="w")
        tk.Entry(login_frame, textvariable=self.login_password_var, show="*").grid(row=1, column=1, padx=10, pady=5)

        tk.Button(login_frame, text="Login", command=self.login_user).grid(row=2, column=0, columnspan=2, pady=10)

    def register_user(self):
        name = self.name_var.get()
        email = self.email_var.get()
        password = self.password_var.get()
        number = self.number_var.get()
        objeto = self.objeto_var.get()
        #print(objeto)
        try:
            cluster = pymongo.MongoClient("mongodb+srv://tempotemporesto:uSkg5lY0Z1L442EY@test.ty5rffy.mongodb.net/test?retryWrites=true&w=majority&appName=test")
            db = cluster["python"]
            collection = db["test"]

            # Check if the email is already registered
            if collection.find_one({"email": email}):
                messagebox.showerror("Registration Error", "Email already registered!")
            else:
                # Insert user information into the database
                user_data = {"name": name, "email": email, "password": password, "number": number ,"objeto": objeto }
                collection.insert_one(user_data)
                messagebox.showinfo("Registration", "User registered successfully!")

        except pymongo.errors.ConnectionFailure:
            messagebox.showerror("Database Error", "Failed to connect to the database!")

    def login_user(self):
        login_email = self.login_email_var.get()
        login_password = self.login_password_var.get()

        # Here you can implement code to check login credentials against the stored user information

        messagebox.showinfo("Login", "Login successful!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CadastreLoginApp(root)
    root.mainloop()

