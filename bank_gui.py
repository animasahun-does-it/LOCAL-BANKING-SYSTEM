import database
from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter import ttk

class Bank:
    def __init__(self, window):
        self.window = window
        self.window.title("Python Bank")
        self.window.geometry("800x600")
        self.window.config(bg="white")
        self.icon = PhotoImage(file='logo.png')  # app icon
        self.window.iconphoto(True, self.icon)  # setting the app icon
        self.hide_bal_btn = None
        database.create_table()
        self.main()



    # logout function
    def logout(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.main()

    def hide_balance(self, balance):

        if self.hide_bal_btn:
            self.show_balance.config(text=f" ₦{balance:,.2f}")
            self.hide_bal_btn = False

        else:
           self.show_balance.config(text="₦ ****")
           self.hide_bal_btn = True



    def login(self):
        email = (self.login_email_entry.get()).lower()
        pin = self.pin_entry.get()
        response = database.user_login(email, pin)

        if response:
            firstname, lastname, balance, account_number = database.user_info(email)
            self.dashboard(firstname, lastname, balance, account_number)

        else:
            messagebox.showerror(title="Error", message="Invalid email or pin")

    def create_account(self):
        pin = self.create_pin_entry.get()
        lastname = (self.lastname_entry.get()).strip().title()
        firstname = (self.firstname_entry.get()).strip().title()
        email = (self.email_entry.get()).strip().lower()
        phone_num = self.phone_entry.get()
        account_number = phone_num[1:]

        if not firstname or not lastname:
            messagebox.showerror(title="Error", message="Kindly input your name")
            return

        if len(phone_num) != 11:
            messagebox.showerror(title="Error", message="Kindly use this format for your phone number\n07000000000")
            return

        if "@" not in email or ".com" not in email:
            messagebox.showerror(title="Error", message="Invalid email")
            return

        if not pin.isdigit() or len(pin) != 4:
            messagebox.showerror(title="Error", message="Pin must be four digit")
            return

        if pin != self.confirm_pin_entry.get():
            messagebox.showerror(title="Error", message="Make sure pin matches")
            return

        if self.agree_State.get() == 0:
            messagebox.showerror(title="Error", message="You have to agree to the terms and conditions to proceed")
            return

        if database.check_dup(email):
            messagebox.showerror(title="Error", message="There is an account with this email already")
            return

        if database.check_dup(None, phone_num):
            messagebox.showerror(title="Error", message="There is an account with this phone number already")
            return

        else:
            database.create_user(account_number, firstname, lastname, email, pin, phone_num)
            messagebox.showinfo(title="Success", message="Account created successfully", parent=self.window)
            self.main()



    def deposit(self, firstname, lastname, balance, account_number):
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit")
        correct_pin = database.get_user_pin(account_number)

        if amount >= 100:
            pin = simpledialog.askinteger("Verify", "Enter your pin", parent=self.window)

            if pin == int(correct_pin):
                database.deposit_user(account_number, amount)
                messagebox.showinfo(title="Successful", message=f"You have successfully deposit {amount}")
                updated_balance = balance + amount
                self.dashboard(firstname, lastname, updated_balance, account_number)

            else:
                messagebox.showerror(title="Error", message="Incorrect pin")
                return

        elif amount < 100:
            messagebox.showerror(title="Error", message="You cannot deposit less than ₦100")
            return

    def withdraw(self, firstname, lastname, balance, account_number):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw", parent=self.window)
        correct_pin = database.get_user_pin(account_number)

        if amount <= float(balance):
            pin = simpledialog.askinteger("Verify", "Enter your pin", parent=self.window)

            if pin == int(correct_pin):
                database.withdraw_user(account_number, amount)
                messagebox.showinfo(title="Successful", message=f"You have withdraw {amount}")
                updated_balance = balance - amount
                self.dashboard(firstname, lastname, updated_balance, account_number)

            else:
                messagebox.showerror(title="Error", message="Incorrect pin")
                return

        elif amount > balance:
            messagebox.showerror(title="Error", message=f"You cannot withdraw more than {balance}", parent=self.window)
            return

    def transfer(self, firstname, lastname, balance, account_number):
        receiver_account_number = simpledialog.askstring("Transfer", "Enter Receiver's Account Number")
        correct_pin = database.get_user_pin(account_number)
        receiver_info = database.user_info(None, receiver_account_number)

        if receiver_info:
            receiver_firstname, receiver_lastname = receiver_info
            response = messagebox.askyesno(title="", message=f"Confirm Receiver's name:\n {receiver_firstname} {receiver_lastname}")

            if response:
                amount = simpledialog.askfloat("Transfer", "Enter amount to transfer")

                if amount <= float(balance):
                    pin = simpledialog.askinteger("Verify", "Enter your pin", parent=self.window)

                    if pin == int(correct_pin):
                        database.transfer_amount(account_number, receiver_account_number, amount)
                        messagebox.showinfo(title="Successful", message=f"You have transferred {amount}")
                        updated_balance = float(balance) - amount
                        self.dashboard(firstname, lastname, updated_balance, account_number)

                    else:
                        messagebox.showerror(title="Error", message="Incorrect pin")
                        return

                elif amount > balance:
                    messagebox.showerror(title="Error", message=f"You cannot transfer less than {balance}")
                    return

            else:
                return
        else:
            messagebox.showerror(title="Error", message="Receiver not found")

    def main(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        Label(self.window, text=" Welcome to the Bank",
                image= self.icon,
                font=("Impact", 40),
                bg="#2E5C6E",
                fg="white",
                compound= "left").pack(pady=20, fill="x")

        login_frame = Frame(self.window, bg="#DCE3E7")
        login_frame.pack(pady=50)

        Label(login_frame, text="Login", font=("Arial", 30), fg="#2E2E2E", bg="#DCE3E7").pack(pady=30)

        input_frame = Frame(login_frame, bg="#DCE3E7")
        input_frame.pack()

        login_email_label = Label(input_frame, text="Email address:", font=("Arial", 15), bg="#DCE3E7", fg="#2E2E2E")
        login_email_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.login_email_entry = Entry(input_frame, font=("calibre", 15), width=25)
        self.login_email_entry.grid(row=1, column=1, padx=5, pady=5)


        pin_label = Label(input_frame, text="Pin:", font=("Arial", 15), bg="#DCE3E7", fg="#2E2E2E")
        pin_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        self.pin_entry = Entry(input_frame, show="*", font=("Calibre", 15), width=5)
        self.pin_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")


        submit_button = Button(login_frame, text="Login", bg="#F5A623", fg="black", activebackground="black",
                               activeforeground="#F5A623", command=self.login, font=("Arial", 15))
        submit_button.pack(pady=20)

        create_account_link = Button(login_frame, text="No account. Create one", command=self.create_account_window,
                                     fg="blue", bg="#DCE3E7", relief="solid")
        create_account_link.pack(pady=10)

    def create_account_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.agree_State = IntVar()

        Label(self.window, text=" Welcome to the Bank",
                image= self.icon,
                font=("Impact", 40),
                bg="#2E5C6E",
                fg="white",
                compound= "left").pack(pady=20,
                                                                                                           fill="x")

        create_frame = Frame(self.window, bg="#DCE3E7")
        create_frame.pack()

        create_label = Label(create_frame, text="Create Account", font=("Arial", 30), fg="#2E2E2E", bg="#DCE3E7",
                             width=20)
        create_label.pack(pady=10)

        input_frame = Frame(create_frame, bg="#DCE3E7")
        input_frame.pack(pady=20)

        firstname_label = Label(input_frame, text="First Name:", font=("Arial", 15), bg="#DCE3E7", fg="#2E2E2E")
        firstname_label.grid(row=0, column=0, pady=5, padx=5)

        self.firstname_entry = Entry(input_frame, font=("Calibre", 15))
        self.firstname_entry.grid(row=0, column=1, padx=5, pady=5)

        lastname_label = Label(input_frame, text="Last Name:", font=("Arial", 15), bg="#DCE3E7", fg="#2E2E2E")
        lastname_label.grid(row=1, column=0, padx=5, pady=5)

        self.lastname_entry = Entry(input_frame, font=("Calibre", 15))
        self.lastname_entry.grid(row=1, column=1, padx=5, pady=5)

        email_label = Label(input_frame, text="Email:", font=("Arial", 15), bg="#DCE3E7", fg="#2E2E2E")
        email_label.grid(row=2, column=0, pady=5, padx=5)

        self.email_entry = Entry(input_frame, font=("Calibre", 15))
        self.email_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        phone_label = Label(input_frame, text="Phone Number: ", font=("Arial", 15), bg="#DCE3E7", fg="#2E2E2E")
        phone_label.grid(row=3, column=0, padx=5, pady=5)

        self.phone_entry = Entry(input_frame, font=("Calibre", 15))
        self.phone_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
        # self.phone_entry.insert(0, "+234")

        pin_label = Label(input_frame, text="Pin:", font=("Arial", 15), bg="#DCE3E7", fg="#2E2E2E")
        pin_label.grid(row=4, column=0, padx=5, pady=5)

        self.create_pin_entry = Entry(input_frame, show="*", font=("Calibre", 15), width=5)
        self.create_pin_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        confirm_pin_label = Label(input_frame, text="Confirm Pin:", font=("Arial", 15), bg="#DCE3E7", fg="#2E2E2E")
        confirm_pin_label.grid(row=5, column=0, padx=5, pady=5)

        self.confirm_pin_entry = Entry(input_frame, show="*", font=("Calibre", 15), width=5)
        self.confirm_pin_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        agree_checkbox = Checkbutton(create_frame, text="I agree to the terms and condition of this app",
                                     variable=self.agree_State, onvalue=1, offvalue=0)
        agree_checkbox.pack()

        submit_button = Button(create_frame, text="Create Account", bg="#F5A623", fg="black",
                               activebackground="black", activeforeground="#F5A623", command=self.create_account)
        submit_button.pack(pady=15)

        main_window_link = Button(create_frame, text="Already have an account. Login", command=self.main,
                                  fg="blue", bg="#DCE3E7", relief="solid")
        main_window_link.pack(pady=10)

    def dashboard(self, firstname, lastname, balance, account_number):

        for widget in self.window.winfo_children():
            widget.destroy()

        top_frame = Frame(self.window, bg="#2E5C6E", height=60)
        top_frame.pack(fill="x")

        Label(top_frame, text="Python Bank",image= self.icon,  font=("Impact", 20), bg="#2E5C6E", fg="white",
              compound= "left").pack(
            padx=20,
                                                                                                        side="left")

        logout_btn = Button(top_frame, text="Logout", fg="white", bg="red", font=("Arial", 12, "bold"),
                            command=self.logout)
        logout_btn.pack(side="right", padx=20)

        welcome_label = Label(self.window, text=f"Welcome, {firstname} {lastname}!", font=("Arial", 20), bg="white",
                              fg="#2E5C6E")
        welcome_label.pack(pady=15)

        main_frame = Frame(self.window, bg="#DCE3E7")
        main_frame.pack(pady=20)

        account_number_entry = Entry(main_frame, bg="white", fg="black", bd=2, width=28)
        account_number_entry.insert(0, f"Account Number: {account_number}")
        account_number_entry.config(state="readonly")
        account_number_entry.pack(anchor="w", pady=10, padx=10)

        balance_frame = Frame(main_frame)
        balance_frame.pack()

        Label(balance_frame, text="Account Balance", font=("Arial", 15), bg="#DCE3E7").pack(side="top")

        balance_label_frame = Frame(main_frame, bg="#DCE3E7")
        balance_label_frame.pack()

        self.show_balance = Label(balance_label_frame, text=f" ₦{balance:,.2f}", font=("Arial", 20, "bold"),
                                bg="#DCE3E7", fg="green")
        self.show_balance.pack(side="left")

        hide_balance = Button(balance_label_frame, text="👁", command= lambda :self.hide_balance(balance))
        hide_balance.pack(side="left")

        transaction_frame = Frame(main_frame, bg="#DCE3E7")
        transaction_frame.pack(pady=10)

        deposit_frame = Frame(transaction_frame, bg="#DCE3E7")
        deposit_frame.pack(side="left", padx=20, pady=20)

        deposit_btn = Button(deposit_frame, text="➕", font=("Arial", 20), width=3,
                             command=lambda: self.deposit(firstname, lastname, balance, account_number))
        deposit_btn.pack()

        deposit_label = Label(deposit_frame, text="Deposit", bg="#DCE3E7", fg="#2E2E2E", font=("Arial", 15))
        deposit_label.pack()

        transfer_frame = Frame(transaction_frame, bg="#DCE3E7")
        transfer_frame.pack(side="left", padx=20)

        transfer_btn = Button(transfer_frame, text="↔", font=("Arial", 20), width=3,
                              command=lambda: self.transfer(firstname, lastname, balance, account_number))
        transfer_btn.pack()

        transfer_label = Label(transfer_frame, text="Transfer", bg="#DCE3E7", fg="#2E2E2E", font=("Arial", 15))
        transfer_label.pack()

        withdraw_frame = Frame(transaction_frame, bg="#DCE3E7")
        withdraw_frame.pack(side="left", padx=20)

        withdraw_btn = Button(withdraw_frame, text="➖", font=("Arial", 20), width=3,
                              command=lambda: self.withdraw(firstname, lastname, balance, account_number))
        withdraw_btn.pack()

        withdraw_label = Label(withdraw_frame, text="Withdraw", bg="#DCE3E7", fg="#2E2E2E", font=("Arial", 15))
        withdraw_label.pack()

        history_frame = LabelFrame(main_frame, text="Transaction History",
                                   font=("Arial", 14), bg="white", fg="#2E2E2E", padx=10, pady=10)
        history_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = ("Date", "Type", "Amount", "Balance")

        transaction_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=8)

        for column in columns:
            transaction_tree.column(column, anchor="w", width=150)
            transaction_tree.heading(column, text=column)

        transaction_tree.pack()

        scrollbar = Scrollbar(history_frame)
        scrollbar.pack(side="right", fill="y")

        transaction_tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=transaction_tree.yview)

        transactions = database.get_history(account_number)
        for transaction in transactions:
            transaction_tree.insert('', 'end', values=(transaction[0], transaction[1], f"₦{transaction[2]:,.2f}",
                                                       f"₦{transaction[3]:,.2f}"))

if __name__ == "__main__":
    window = Tk()
    app = Bank(window)
    window.mainloop()
