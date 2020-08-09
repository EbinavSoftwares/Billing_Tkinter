import tkinter as tk
from collections import defaultdict
from datetime import date
from datetime import datetime
from tkinter import TclError
from tkinter import messagebox
from tkinter import ttk

import pandas as pd
from PIL import Image, ImageTk
from babel.numbers import format_currency
from tkcalendar import DateEntry
from ttkwidgets.autocomplete import AutocompleteEntry

from Models.Billing import Billing
from Models.Product import Product
from Models.Sales import Sales
from Models.Stock import Stock
from Models.User import User
from Utilities.Clock import Clock
from Utilities.windows import set_dpi_awareness


# Main class
class MainForm:
    # class variables
    is_admin_user = None
    logged_user = None
    user_profile = None

    def __init__(self):
        # set dpi to make clear objects
        set_dpi_awareness()

        # creating main window
        self.window = tk.Tk()
        self.window.option_add("*Font", "Calibri 14 bold")
        self.window['background'] = '#62b6e2'  # '#7794d8'
        self.window.columnconfigure(0, weight=1)
        self.window.title("Main Menu")

        # display settings
        self.window.fullScreenState = False
        self.window.attributes("-fullscreen", self.window.fullScreenState)
        self.w, self.h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (self.w, self.h))
        # self.window.geometry("%dx%d" % (1366, 768))
        self.window.columnconfigure(0, weight=1)
        self.window.state("zoomed")

        # form widgets
        self.menubar = None
        self.user_menu = None

        self.header_container = None
        self.content_container = None
        self.footer_container = None
        self.info_container_left = None
        self.banner_container = None
        self.info_container_right = None

        # form variables
        self.var_username = tk.StringVar()
        self.var_user_profile = tk.StringVar()

        # launch form
        self.main_form()

    # set username and user_profile
    def update_username(self):
        """
        set username and user_profile
        :return: None
        """
        self.var_username.set(MainForm.logged_user)
        self.var_user_profile.set(MainForm.user_profile)

    # set class variables
    @classmethod
    def set(cls, is_admin_user, logged_user):
        """
        Set class variables
        :param is_admin_user:
        :param logged_user:
        :return: None
        """
        cls.is_admin_user = is_admin_user
        cls.logged_user = logged_user

        if is_admin_user:
            cls.user_profile = "Admin"
        else:
            cls.user_profile = "Cashier"

    # main form
    def main_form(self):
        """
        Launch the main form
        :return: None
        """
        # menubar
        self.menubar = tk.Menu(self.window)

        # Sales and Billing
        sales_menu = tk.Menu(self.menubar, tearoff=0)
        sales_menu.add_command(label="Sales", command=lambda: self.load_content('Sales'))
        sales_menu.add_separator()
        sales_menu.add_command(label="Bills", command=lambda: self.load_content('Bills'))
        self.menubar.add_cascade(label="Sales & Bills", menu=sales_menu)

        # Product
        product_menu = tk.Menu(self.menubar, tearoff=0)
        product_menu.add_command(label="View Product", command=lambda: self.load_content('View Product'))
        self.menubar.add_cascade(label="Products", menu=product_menu)

        # Stock
        stock_menu = tk.Menu(self.menubar, tearoff=0)
        stock_menu.add_command(label="View Stock", command=lambda: self.load_content('View Stock'))
        self.menubar.add_cascade(label="Stock", menu=stock_menu)

        # Cash
        cash_menu = tk.Menu(self.menubar, tearoff=0)
        cash_menu.add_command(label="<in progress>", command=self.window.destroy)
        self.menubar.add_cascade(label="Cash Management", menu=cash_menu)

        # User
        self.user_menu = tk.Menu(self.menubar, tearoff=0)
        self.user_menu.add_command(label="Add New User", command=lambda: self.load_content('Add New User'))
        self.user_menu.add_command(label="View Users", command=lambda: self.load_content('View Users'))
        self.user_menu.add_separator()
        self.user_menu.add_command(label="Change Password", command=lambda: self.load_content('Change Password'))
        self.menubar.add_cascade(label="User Management", menu=self.user_menu)

        # Report
        report_menu = tk.Menu(self.menubar, tearoff=0)
        report_menu.add_command(label="Product List Report", command=lambda: self.load_content('Product List Report'))
        report_menu.add_command(label="Stock Report", command=lambda: self.load_content('Stock Report'))
        report_menu.add_command(label="Sales Report", command=lambda: self.load_content('Sales Report'))
        self.menubar.add_cascade(label="Report", menu=report_menu)

        # Admin
        admin_menu = tk.Menu(self.menubar, tearoff=0)
        admin_menu.add_command(label="<in progress>", command=self.window.destroy)
        self.menubar.add_cascade(label="Admin", menu=admin_menu)

        help_menu = tk.Menu(self.menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.window.destroy)
        self.menubar.add_cascade(label="Help", menu=help_menu)

        # Main Containers
        self.header_container = tk.Frame(self.window, relief=tk.RIDGE, bg='#62b6e2')
        self.header_container.pack(fill='x', expand=False, side=tk.TOP, anchor="nw")

        self.content_container = tk.Frame(self.window, relief=tk.RIDGE, bg='#62b6e2')
        self.content_container.pack(fill='both', expand=True, side=tk.TOP, anchor="n")

        self.footer_container = tk.Frame(self.window, bd=5, pady=3, relief=tk.RIDGE, bg='#62b6e2')
        self.footer_container.pack(fill='x', expand=True, side=tk.TOP, anchor="s")

        # header_container elements
        self.info_container_left = tk.Frame(self.header_container, bd=5, padx=5, relief=tk.RIDGE, bg='#fac150')
        self.info_container_left.pack(fill='both', expand=True, side=tk.LEFT, anchor="ne")

        self.banner_container = tk.Frame(self.header_container, bd=5, padx=5, relief=tk.RIDGE, bg='#fac150')
        self.banner_container.pack(fill='both', expand=False, side=tk.LEFT, anchor="nw")

        self.info_container_right = tk.Frame(self.header_container, bd=5, padx=5, relief=tk.RIDGE, bg='#fac150')
        self.info_container_right.pack(fill='both', expand=True, side=tk.RIGHT, anchor="ne")

        # info_container_left elements
        lbl_user = tk.Label(self.info_container_left, font=('Calibri', 14), text='User: ', bg='#fac150')
        lbl_user.grid(row=0, column=0, sticky='nw', padx=2)
        lbl_username = tk.Label(self.info_container_left, font=('Calibri bold', 14), text=self.logged_user,
                                textvariable=self.var_username, bg='#fac150', fg='green')
        lbl_username.grid(row=0, column=1, sticky='nw', padx=2)

        lbl_profile = tk.Label(self.info_container_left, font=('Calibri', 14), text='Profile: ', bg='#fac150')
        lbl_profile.grid(row=1, column=0, sticky='nw', padx=2)
        lbl_user_profile = tk.Label(self.info_container_left, font=('Calibri bold', 14), text=self.user_profile,
                                    textvariable=self.var_user_profile, bg='#fac150', fg='green')
        lbl_user_profile.grid(row=1, column=1, sticky='nw', padx=2)

        # info_container_right elements
        lbl_title = tk.Label(self.info_container_right, font=('Calibri', 14), text='Date: ', bg='#fac150')
        lbl_title.grid(row=0, column=0, sticky='nw', padx=2)
        lbl_time = Clock(self.info_container_right, seconds=False)
        lbl_time.configure(bg="#fac150", fg='green')
        lbl_time.grid(row=0, column=1, sticky="nw", padx=2)

        lbl_title = tk.Label(self.info_container_right, font=('Calibri', 14), text='Day: ', bg='#fac150')
        lbl_title.grid(row=1, column=0, sticky='nw', padx=2, pady=2)
        lbl_title = tk.Label(self.info_container_right, font=('Calibri bold', 14),
                             text=datetime.strftime(datetime.today(), '%A'), bg='#fac150', fg='green')
        lbl_title.grid(row=1, column=1, sticky='nw', padx=2)

        # banner
        self.banner_container.columnconfigure(0, weight=1)
        self.banner_container.rowconfigure(0, weight=1)
        self.banner_container.original = Image.open('Images/Header.png')
        resized = self.banner_container.original.resize((750, 50), Image.ANTIALIAS)
        self.banner_container.image = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        self.banner_container.display = tk.Label(self.banner_container, image=self.banner_container.image)
        self.banner_container.display.grid(row=0)

        # display menu
        self.window.config(menu=self.menubar)

    # show menu based on user_profile
    def show_menu(self, admin_user):
        """
        show menu based on user_profile
        :param admin_user:
        :return: None
        """
        if admin_user:
            for index in range(1, 9):
                self.menubar.entryconfig(index, state=tk.NORMAL)
        else:
            self.menubar.entryconfig('Sales & Bills', state=tk.NORMAL)
            self.menubar.entryconfig('User Management', state=tk.NORMAL)
            self.user_menu.entryconfig('Add New User', state=tk.DISABLED)
            self.user_menu.entryconfig('View Users', state=tk.DISABLED)
            self.menubar.entryconfig('Help', state=tk.NORMAL)

    # load appropriate form based on menu selection
    def load_content(self, form_name):
        """
        load appropriate form based on menu selection
        :param form_name: form name to be launched
        :return:
        """
        self.window.destroy()

        if form_name == 'Sales':
            AddSales()
        elif form_name == 'Bills':
            ViewBills()
        elif form_name == 'View Product':
            ViewProduct()
        elif form_name == 'View Stock':
            ViewStock()
        elif form_name == 'Sales Report':
            SalesReport()
        elif form_name == 'Change Password':
            pass


# Login Class
class Login(MainForm):
    def __init__(self):
        super().__init__()

        # login form variables and widgets
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.user_validated = None

        self.login_container = None
        self.ety_username = None
        self.btn_verify = None
        self.ety_secret_answer = None
        self.ety_new_password = None
        self.ety_confirm_password = None
        self.btn_submit = None

        # local variables
        self.new_password = tk.StringVar()
        self.confirm_password = tk.StringVar()
        self.secret_question = tk.StringVar()
        self.secret_answer = tk.StringVar()

        self.login_form()

    # launch login_form
    def login_form(self):
        """
        launch login form
        :return:
        """
        for widget in self.content_container.winfo_children():
            widget.destroy()

        for index in range(1, 9):
            self.menubar.entryconfig(index, state=tk.DISABLED)

        self.login_container = tk.Frame(self.content_container, bd=20, padx=10, pady=10, relief=tk.RIDGE, bg='#62b6e2')
        self.login_container.pack(fill=None, expand=True, side=tk.TOP, anchor="center")

        # content_container elements
        self.username.set("")
        lbl_username = tk.Label(self.login_container, text="Username: ", bg='#62b6e2')
        lbl_username.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        username = tk.Entry(self.login_container, textvariable=self.username)
        username.grid(row=0, column=1, columnspan=2, sticky="se", padx=5, pady=5)

        lbl_password = tk.Label(self.login_container, text="Password: ", bg='#62b6e2')
        lbl_password.grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        password = tk.Entry(self.login_container, textvariable=self.password, show='*')
        password.grid(row=1, column=1, columnspan=2, sticky="se", padx=5, pady=5)

        btn_cancel = tk.Button(self.login_container, text="Cancel", command=self.window.destroy)
        btn_cancel.grid(row=2, column=1, rowspan=2, sticky="news", padx=5, pady=5)

        btn_login = tk.Button(self.login_container, text="Login", command=self.validate_user)
        btn_login.grid(row=2, column=2, rowspan=2, sticky="news", padx=5, pady=5)

        lbl_forgot_password = tk.Label(self.login_container, text="Forgot Password?", bg='#62b6e2', fg="blue",
                                       cursor="hand2")
        lbl_forgot_password.grid(row=4, column=1, columnspan=2, sticky="nw", padx=5, pady=5)
        lbl_forgot_password.bind("<Button-1>", lambda x: self.forgot_password())

        # display window
        self.window.mainloop()
    
    def forgot_password_form(self):
        """
        launch forgot_password form  
        :return: None 
        """
        self.new_password.set("")
        self.confirm_password.set("")
        self.secret_question.set("")
        self.secret_answer.set("")

        fpassword_container = tk.Frame(self.content_container, bd=20, padx=10, pady=10, relief=tk.RIDGE, bg='#62b6e2')
        fpassword_container.pack(expand=True, side=tk.TOP, anchor="center")

        # content_container elements
        lbl_username = tk.Label(fpassword_container, text="Username: ", bg='#62b6e2')
        lbl_username.grid(row=0, column=0, sticky="news", padx=5, pady=5)
        self.ety_username = tk.Entry(fpassword_container, textvariable=self.username)
        self.ety_username.grid(row=0, column=1, sticky="news", padx=5, pady=5)

        self.btn_verify = tk.Button(fpassword_container, text="Verify", width=10, command=self.verify_username)
        self.btn_verify.grid(row=0, column=2, sticky="news", padx=5, pady=5)

        lbl_secret_question = tk.Label(fpassword_container, text="Secret Question: ", bg='#62b6e2')
        lbl_secret_question.grid(row=1, column=0, sticky="news", padx=5, pady=5)
        ety_secret_question = tk.Entry(fpassword_container, textvariable=self.secret_question, state='disabled')
        ety_secret_question.grid(row=1, column=1, columnspan=2, sticky="news", padx=5, pady=5)

        lbl_secret_answer = tk.Label(fpassword_container, text="Answer: ", bg='#62b6e2')
        lbl_secret_answer.grid(row=2, column=0, sticky="news", padx=5, pady=5)
        self.ety_secret_answer = tk.Entry(fpassword_container, show='*', textvariable=self.secret_answer,
                                          state='disabled')
        self.ety_secret_answer.grid(row=2, column=1, sticky="news", padx=5, pady=5)

        lbl_new_password = tk.Label(fpassword_container, text="New Passowrd: ", bg='#62b6e2')
        lbl_new_password.grid(row=3, column=0, sticky="news", padx=5, pady=5)
        self.ety_new_password = tk.Entry(fpassword_container, width=10, textvariable=self.new_password,
                                         show='*', state='disabled')
        self.ety_new_password.grid(row=3, column=1, sticky="news", padx=5, pady=5)

        lbl_confirm_password = tk.Label(fpassword_container, text="Confirm New Passowrd: ", bg='#62b6e2')
        lbl_confirm_password.grid(row=4, column=0, sticky="news", padx=5, pady=5)
        self.ety_confirm_password = tk.Entry(fpassword_container, width=10, textvariable=self.confirm_password,
                                             show='*', state='disabled')
        self.ety_confirm_password.grid(row=4, column=1, sticky="news", padx=5, pady=5)

        btn_cancel = tk.Button(fpassword_container, text="Cancel", width=10, command=self.login_form)
        btn_cancel.grid(row=5, column=1, rowspan=2, sticky="nw", padx=5, pady=5)

        self.btn_submit = tk.Button(fpassword_container, text="Submit", width=10, command=self.set_password,
                                    state='disabled')
        self.btn_submit.grid(row=5, column=1, rowspan=2, columnspan=2, sticky="ne", padx=5, pady=5)

    def forgot_password(self):
        """
        display forgot_password form
        :return: 
        """
        for widget in self.content_container.winfo_children():
            widget.destroy()

        self.forgot_password_form()

    def verify_username(self):
        """
        validate user
        :return: 
        """
        username = self.username.get().strip().lower()

        user = User.get_user(username)
        if user:
            self.ety_username.configure(state=tk.DISABLED)
            self.secret_question.set(user.secret_question)
            self.ety_secret_answer.configure(state=tk.NORMAL)
            self.ety_new_password.configure(state=tk.NORMAL)
            self.ety_confirm_password.configure(state=tk.NORMAL)
            self.btn_submit.configure(state=tk.NORMAL)
        else:
            messagebox.showerror("SS Fashion Tuty", f"username: '{username}' not found!")
            print(f"username: '{username}' not found!")

    def set_password(self):
        username = self.username.get().strip().lower()
        new_password = self.new_password.get()
        confirm_password = self.confirm_password.get()
        secret_answer = self.secret_answer.get().strip().lower()

        if len(new_password) <= 0:
            messagebox.showerror("SS Fashion Tuty", f"password must be 4 to 15 characters!")
            print(f"password must be 4 to 15 characters!")
            return

        if new_password != confirm_password:
            messagebox.showerror("SS Fashion Tuty", f"password and confirm_password are not same!")
            print(f"password and confirm_password are not same!")
            return

        if len(secret_answer) <= 0:
            messagebox.showerror("SS Fashion Tuty", f"secret_answer cannot be empty!")
            print(f"secret_answer cannot be empty!")
            return

        user = User.get_user(username)
        if user:
            if user.secret_answer == secret_answer:
                User.set_password(username, new_password)
                messagebox.showinfo("SS Fashion Tuty", f"user: {username} password changed!")
                print(f"user: {username} password changed!")

                self.login_form()
            else:
                messagebox.showerror("SS Fashion Tuty", f"secret_answer is incorrect!")
                print(f"secret_answer is incorrect!")
        else:
            messagebox.showerror("SS Fashion Tuty", f"username: '{username}' not found!")
            print(f"username: '{username}' not found!")

    def validate_user(self):
        username = self.username.get().strip().lower()
        password = self.password.get()

        user = User.get_user(username)
        if user:
            if user.password == password:
                self.user_validated = True
                MainForm.set(user.is_admin, username)
                self.update_username()

                print(f"username: '{username}' validated! and user_profile: {MainForm.is_admin_user}")

                for widget in self.content_container.winfo_children():
                    widget.destroy()

                self.show_menu(MainForm.is_admin_user)  # self.admin_user
            else:
                messagebox.showerror("SS Fashion Tuty", f"Invalid password!")
                print(f"Invalid password!")
        else:
            messagebox.showerror("SS Fashion Tuty", f"username: '{username}' is not registered!")
            print(f"username: '{username}' is not registered!")


class AddSales(MainForm):
    def __init__(self):
        super().__init__()

        # Set text variables
        self.product_id = tk.StringVar()
        self.product_name = tk.StringVar()
        self.product_type = tk.StringVar()
        self.product_size = tk.StringVar()
        self.selling_price = tk.DoubleVar()
        self.actual_price = tk.DoubleVar()

        self.quantity = tk.IntVar(value=1)
        self.total_amount = tk.StringVar()
        self.discount = tk.DoubleVar()
        self.bill_amount = tk.StringVar()

        self.search_product_id = tk.StringVar()

        self.filter_ety_product_name = None
        self.filter_ety_product_type = None

        # local variables
        self.tree = None
        self.sales_tree = None
        self.qty_window = None
        self.ety_search_product_id = None
        self.tree_container = None
        self.lbl_total_amount = None
        self.txt_receipt = None
        self.bill_date = None
        self.bill_no = None
        self.btn_save_bill = None

        self.selected = list()
        self.product_name_list = list()
        self.product_type_list = list()
        self.sales_counter = 0

        self.load_add_sales_form()

    def load_add_sales_form(self):
        for index in range(1, 9):
            self.menubar.entryconfig(index, state=tk.DISABLED)

        self.show_menu(MainForm.is_admin_user)
        self.update_username()

        products = Product.get_product_name_list()
        for product in products:
            self.product_name_list.append(product.product_name)

        products = Product.get_product_type_list()
        for product in products:
            self.product_type_list.append(product.product_type)

        # ********** Sub Containers *********
        left_container = tk.Frame(self.content_container, bd=5, padx=5, pady=2, relief=tk.RIDGE, bg='#62b6e2')
        left_container.pack(fill='both', expand=True, side=tk.LEFT)

        bill_container = tk.Frame(self.content_container, bd=5, padx=5, pady=5, relief=tk.RIDGE, bg='#62b6e2')
        bill_container.pack(fill='both', expand=True, side=tk.RIGHT)

        # left_container elements
        top_button_container = tk.Frame(left_container, relief=tk.RIDGE, bg='#62b6e2')
        top_button_container.pack(fill='both', expand=True, side=tk.TOP)

        search_container = tk.Frame(top_button_container, relief=tk.RIDGE, bg='#62b6e2')
        search_container.pack(fill='x', expand=True, side=tk.LEFT)

        filter_container = tk.Frame(top_button_container, relief=tk.RIDGE, bg='#62b6e2')
        filter_container.pack(fill='x', expand=True, side=tk.RIGHT)

        bottom_button_container = tk.Frame(left_container, relief=tk.RIDGE, bg='#62b6e2')
        bottom_button_container.pack(fill='both', expand=True, side=tk.BOTTOM)

        left_button_container = tk.Frame(bottom_button_container, relief=tk.RIDGE, bg='#62b6e2')
        left_button_container.pack(fill='x', expand=True, anchor='center', side=tk.LEFT)

        right_button_container = tk.Frame(bottom_button_container, relief=tk.RIDGE, bg='#62b6e2')
        right_button_container.pack(fill='x', expand=True, anchor='center', side=tk.RIGHT)

        # ********** left_search_container elements *********
        search_lbl_product_id = tk.Label(search_container, text="ID: ", bg='#62b6e2')
        search_lbl_product_id.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        self.ety_search_product_id = tk.Entry(search_container, width=10, textvariable=self.search_product_id)
        self.ety_search_product_id.grid(row=1, column=0, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_search_product_id.bind('<Return>', lambda event: self.search_product(event))

        btn_search = tk.Button(search_container, text="Search", command=self.search_product)
        btn_search.grid(row=1, column=1, sticky="sw", padx=2, pady=1)

        filter_lbl_product_name = tk.Label(filter_container, text="Name: ", bg='#62b6e2')
        filter_lbl_product_name.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        self.filter_ety_product_name = AutocompleteEntry(filter_container, completevalues=self.product_name_list)
        self.filter_ety_product_name.grid(row=1, column=0, sticky="nw", padx=2, pady=1, ipady=6)
        self.filter_ety_product_name.bind("<Return>", lambda event: self.filter_product(event))

        # self.filter_lbl_product_name = AutoCompleteEntry(self.product_list, filter_container)
        # self.filter_lbl_product_name.grid(row=1, column=0, sticky="nw", padx=2, pady=1, ipady=6)
        # self.filter_lbl_product_name.bind("<Return>", lambda event: self.filter_product(event))

        # filter_lbl_product_name = tk.Label(filter_container, text="Name: ", bg='#62b6e2')
        # filter_lbl_product_name.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        # filter_product_name = tk.Entry(filter_container, width=20, textvariable=self.filter_product_name)
        # filter_product_name.grid(row=1, column=0, sticky="nw", padx=2, pady=1, ipady=6)

        filter_lbl_product_type = tk.Label(filter_container, text="Type: ", bg='#62b6e2')
        filter_lbl_product_type.grid(row=0, column=1, sticky="nw", padx=1, pady=1)
        self.filter_ety_product_type = AutocompleteEntry(filter_container, completevalues=self.product_type_list)
        self.filter_ety_product_type.grid(row=1, column=1, sticky="nw", padx=2, pady=1, ipady=6)
        self.filter_ety_product_type.bind("<Return>", lambda event: self.filter_product(event))

        # filter_lbl_product_type = tk.Label(filter_container, text="Type: ", bg='#62b6e2')
        # filter_lbl_product_type.grid(row=0, column=1, sticky="nw", padx=1, pady=1)
        # filter_product_type = tk.Entry(filter_container, width=25, textvariable=self.filter_product_type)
        # filter_product_type.grid(row=1, column=1, sticky="nw", padx=2, pady=1, ipady=6)

        btn_filter = tk.Button(filter_container, text="Apply Filter", command=self.filter_product)
        btn_filter.grid(row=1, column=2, sticky="sw", padx=2, pady=1)

        btn_clear_filter = tk.Button(filter_container, text="Clear Filter", command=self.reload_products)
        btn_clear_filter.grid(row=1, column=3, sticky="news", padx=2, pady=1)

        lbl_bill_date = tk.Label(filter_container, text='Bill Date: ', bg='#62b6e2')
        lbl_bill_date.grid(row=0, column=2, sticky="nw", padx=1, pady=1)
        self.bill_date = DateEntry(filter_container, date_pattern='yyyy-mm-dd', background='yellow',
                                          foreground='black', borderwidth=2)
        self.bill_date.grid(row=0, column=3, sticky="sw", padx=2, pady=1, ipady=3)

        # ********** tree_containers elements *********
        self.tree_container = tk.Frame(left_container, pady=3, bg='#62b6e2', relief=tk.RIDGE)
        self.tree_container.pack(fill='both', expand=True, side=tk.TOP)

        header = ('product_id', 'product_name', 'product_type', 'product_size', 'selling_price', 'dummy')
        self.tree = ttk.Treeview(self.tree_container, columns=header, height=8, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(self.tree_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.tree_container, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Calibri', 12))
        style.configure("Treeview", font=('Calibri', 12), rowheight=25)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.tree_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=self.tree_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=self.tree_container)

        self.tree_container.grid_columnconfigure(0, weight=1)
        self.tree_container.grid_rowconfigure(0, weight=1)

        self.tree.heading("0", text="P_ID")
        self.tree.heading("1", text="PRODUCT_NAME")
        self.tree.heading("2", text="PRODUCT_TYPE")
        self.tree.heading("3", text="SIZE")
        self.tree.heading("4", text="PRICE")

        self.tree.column(0, anchor='center', width="80")
        self.tree.column(1, anchor=tk.W, width="150")
        self.tree.column(2, anchor=tk.W, width="200")
        self.tree.column(3, anchor='center', width="100")
        self.tree.column(4, anchor=tk.E, width="100")
        self.tree.column(5, anchor='center', width="5")

        self.reload_products()

        # ********** Product Details *********
        product_details_container = tk.Frame(left_container, bd=5, pady=3, relief=tk.RIDGE, bg='#62b6e2')
        product_details_container.pack(fill='both', expand=True, side=tk.LEFT)

        # lbl_product_details = tk.Label(product_details_container, text="Product Details", bg='#62b6e2')
        # lbl_product_details.grid(row=0, column=0, columnspan=2, sticky="news", padx=3, pady=3)
        # lbl_product_details.config(font=("Calibri bold", 14))

        lbl_product_id = tk.Label(product_details_container, text="ID: ", bg='#62b6e2')
        lbl_product_id.grid(row=1, column=0, sticky="nw", padx=3, pady=1)
        product_id = tk.Entry(product_details_container, width=10, textvariable=self.product_id, state='disabled')
        product_id.grid(row=1, column=1, sticky="nw", padx=3, pady=1)

        lbl_product_name = tk.Label(product_details_container, text="Product Name: ", bg='#62b6e2')
        lbl_product_name.grid(row=2, column=0, sticky="nw", padx=3, pady=1)
        product_name = tk.Entry(product_details_container, textvariable=self.product_name, state='disabled')
        product_name.grid(row=2, column=1, columnspan=2, sticky="nw", padx=3, pady=1)

        lbl_product_type = tk.Label(product_details_container, text="Product Type: ", bg='#62b6e2')
        lbl_product_type.grid(row=3, column=0, sticky="nw", padx=3, pady=1)
        product_type = tk.Entry(product_details_container, textvariable=self.product_type, state='disabled')
        product_type.grid(row=3, column=1, columnspan=2, sticky="nw", padx=3, pady=1)

        lbl_product_size = tk.Label(product_details_container, text="Size: ", bg='#62b6e2')
        lbl_product_size.grid(row=4, column=0, sticky="nw", padx=3, pady=1)
        product_size = tk.Entry(product_details_container, textvariable=self.product_size, state='disabled')
        product_size.grid(row=4, column=1, columnspan=2, sticky="nw", padx=3, pady=1)

        lbl_selling_price = tk.Label(product_details_container, text="Price: ", bg='#62b6e2')
        lbl_selling_price.grid(row=5, column=0, sticky="nw", padx=3, pady=1)
        selling_price = tk.Entry(product_details_container, width=10, textvariable=self.selling_price, state='disabled')
        selling_price.grid(row=5, column=1, sticky="nw", padx=3, pady=1)

        btn_add = tk.Button(product_details_container, text="Add", command=self.add_sales_by_button)
        btn_add.grid(row=7, column=1, sticky="news", columnspan=2, padx=1, pady=2)

        # ********** Sales Tree Details *********
        sales_tree_container = tk.Frame(left_container, bd=5, pady=3, relief=tk.RIDGE, bg='#62b6e2')
        sales_tree_container.pack(fill='both', expand=True, side=tk.RIGHT)

        header = ('#', 'product_id', 'product_name', 'selling_price', 'quantity', 'amount', 'dummy')
        self.sales_tree = ttk.Treeview(sales_tree_container, columns=header, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(sales_tree_container, orient="vertical", command=self.sales_tree.yview)
        hsb = ttk.Scrollbar(sales_tree_container, orient="horizontal", command=self.sales_tree.xview)

        self.sales_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.sales_tree.grid(column=0, row=0, sticky='nsew')

        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        sales_tree_container.grid_columnconfigure(0, weight=1)
        sales_tree_container.grid_rowconfigure(0, weight=1)

        self.sales_tree.heading("0", text="#")
        self.sales_tree.heading("1", text="PRODUCT_ID")
        self.sales_tree.heading("2", text="PRODUCT")
        self.sales_tree.heading("3", text="PRICE")
        self.sales_tree.heading("4", text="QTY")
        self.sales_tree.heading("5", text="Amount")

        self.sales_tree.column(0, anchor='center', minwidth=50, width=50)
        self.sales_tree.column(3, anchor='center', minwidth=100, width=100)
        self.sales_tree.column(4, anchor='center', minwidth=100, width=100)
        self.sales_tree.column(5, anchor=tk.E, minwidth=100, width=100)
        self.sales_tree.column(6, anchor='center', width=5)
        self.sales_tree["displaycolumns"] = (0, 2, 3, 4, 5, 6)

        self.tree.tag_configure("evenrow", background='#fbefcc')
        self.tree.tag_configure("oddrow", background='white', foreground='black')
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.tree.bind('<Double-1>', lambda event: self.get_quantity(event))
        self.tree.bind('<Return>', lambda event: self.get_quantity(event))

        # ********** bottom_button_container elements *********
        btn_new_bill = tk.Button(left_button_container, text="New Bill", command=self.clear_all)
        btn_new_bill.pack(side=tk.LEFT, expand=True, fill='both', padx=5, pady=1)
        btn_new_bill.config(font=("calibri", 20))

        btn_close = tk.Button(left_button_container, text="Close", command=self.window.destroy)
        btn_close.pack(side=tk.LEFT, expand=True, fill='both', padx=5, pady=1)
        btn_close.config(font=("calibri", 20))

        self.lbl_total_amount = tk.Label(right_button_container, fg='Red', relief=tk.RAISED,
                                         textvariable=self.total_amount, width=10)
        self.lbl_total_amount.pack(side=tk.RIGHT, expand=True, fill='both', padx=1, pady=1)
        self.lbl_total_amount.config(font=("calibri bold", 34))
        self.total_amount.set(format_currency(0, 'INR', locale='en_IN'))

        btn_calculate = tk.Button(right_button_container, text="Calculate",
                                  command=self.calculate_bill_amount)
        btn_calculate.pack(side=tk.RIGHT, fill='both', expand=True, padx=5, pady=1)
        btn_calculate.config(font=("calibri", 20))

        lbl_discount = tk.Label(right_button_container, text='Discount: ', bg='#62b6e2')
        lbl_discount.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=1)

        ety_discount = tk.Entry(right_button_container, width=5, textvariable=self.discount)
        ety_discount.pack(side=tk.LEFT, fill='x', expand=True, padx=5, pady=1)
        ety_discount.config(font=("calibri", 14))

        # ********** bill_container elements *********
        self.txt_receipt = tk.Text(bill_container, height=25, bg='white', bd=4, font=('Courier', 11))
        self.txt_receipt.pack(side=tk.TOP, expand=True, fill='x', padx=1, pady=1)

        lbl_bill_amount = tk.Label(bill_container, fg='Blue', relief=tk.RAISED,
                                   textvariable=self.bill_amount)
        lbl_bill_amount.pack(side=tk.TOP, expand=True, fill='x', padx=1, pady=1)
        lbl_bill_amount.config(font=("calibri bold", 46))
        self.bill_amount.set(format_currency(0, 'INR', locale='en_IN'))

        self.btn_save_bill = tk.Button(bill_container, text="Save Bill", bg='Green', fg='Yellow', command=self.save_bill)
        # btn_bill  .grid(row=1, column=1, rowspan=2, sticky="news", padx=1, pady=1)
        self.btn_save_bill.pack(side=tk.LEFT, expand=True, fill='x', padx=1, pady=1)
        self.btn_save_bill.config(font=("calibri bold", 22))

        btn_print_bill = tk.Button(bill_container, text="Print Bill", fg='Black', command=self.print_bill)
        btn_print_bill.pack(side=tk.RIGHT, expand=True, fill='x', padx=1, pady=1)
        btn_print_bill.config(font=("calibri bold", 22))

    def filter_product(self, event=None):
        product_name = self.filter_ety_product_name.get().strip()
        product_type = self.filter_ety_product_type.get().strip()

        products = Product.search_products(product_name=product_name, product_type=product_type)
        self.tree.delete(*self.tree.get_children())
        if products:
            row_num = 0
            for product in products:
                row_num += 1
                row = (product.product_id, product.product_name, product.product_type, product.product_size,
                       round(product.selling_price, 2))

                if row_num % 2 == 0:
                    self.tree.insert("", tk.END, values=row, tags=('evenrow', product.product_id))
                else:
                    self.tree.insert("", tk.END, values=row, tags=('oddrow', product.product_id))
        else:
            pass

    def search_product(self, event=None):
        product_id = self.search_product_id.get().strip()

        products = Product.search_products(product_id=product_id)
        if products is None:
            messagebox.showerror("SS Fashion Tuty", f"Product_id: {product_id} not found!")
            print(f"Product_id: {product_id} not found!")
        if isinstance(products, Product):
            self.tree.selection_set(self.tree.tag_has(str(product_id)))
            self.tree.focus_set()
            self.tree.focus(self.selected)
        else:
            pass

    def generate_bill_header(self, bill_no):
        self.txt_receipt.delete("1.0", tk.END)
        # self.txt_receipt.tag_configure('align_center', justify='center')
        # self.txt_receipt.tag_configure('align_left', justify='left')
        # self.txt_receipt.tag_configure('align_right', justify='right')

        self.txt_receipt.insert(tk.END, "\n")
        self.txt_receipt.insert(tk.END, f"{'SS Fashion Tuty':^41}\n")
        self.txt_receipt.insert(tk.END, f"{'Thalamuthu Nagar Main Road':^41}\n")
        self.txt_receipt.insert(tk.END, f"{'Koilpillaivilai, Tuticorin - 628002':^41}\n")
        self.txt_receipt.insert(tk.END, f"{'Contact: +91 9942380164':^41}\n")
        self.txt_receipt.insert(tk.END, "\n")

        form_bill_date = datetime.strftime(datetime.strptime(
            self.bill_date.get(), '%Y-%m-%d'), '%d-%b-%Y')
        bill_date = datetime.strftime(datetime.now(), '%d-%b-%Y')  # %d-%b-%Y')
        bill_time = datetime.strftime(datetime.now(), '%I:%M:%S %p')
        if form_bill_date != bill_date:
            bill_date = form_bill_date
            bill_time = "00:00:01 AM"

        self.txt_receipt.insert(tk.END, f"{' Cashier: ' + self.logged_user.upper():<21}")
        self.txt_receipt.insert(tk.END, f"{' Date: ' + bill_date + ' ':>20}\n")

        self.txt_receipt.insert(tk.END, f"{' Bill No: ' + str(bill_no):<21}")
        self.txt_receipt.insert(tk.END, f"{' Time: ' + bill_time+ ' ':>20}\n")

        self.txt_receipt.insert(tk.END, f"\n{'-' * 41}\n")
        self.txt_receipt.insert(tk.END, f"{'#':^4}")
        self.txt_receipt.insert(tk.END, f"{'Item':^15}")
        self.txt_receipt.insert(tk.END, f"{'Qty':^4}")
        self.txt_receipt.insert(tk.END, f"{'Price':^8}")
        self.txt_receipt.insert(tk.END, f"{'Amount':^8}\n")

        self.txt_receipt.insert(tk.END, f"{'-' * 41}\n")

    def generate_bill_footer(self, quantity_sum, discount, bill_amount):
        sub_total = float(bill_amount) + float(discount)
        self.txt_receipt.insert(tk.END, "\n")
        self.txt_receipt.insert(tk.END, f"{'-' * 41}\n")
        self.txt_receipt.insert(tk.END, f"    {'SubTotal':<15}{quantity_sum:^4}{sub_total:>17}\n")
        self.txt_receipt.insert(tk.END, f"{'-' * 41}\n")
        self.txt_receipt.insert(tk.END, f"    {'Discount':<15}{discount:>21}\n")

        self.txt_receipt.insert(tk.END, "\n")
        self.txt_receipt.insert(tk.END, f"{'-' * 41}\n")
        self.txt_receipt.insert(tk.END, f"    {'Total':<15}{bill_amount:>21}\n")
        self.txt_receipt.insert(tk.END, f"{'-' * 41}\n")

        self.txt_receipt.insert(tk.END, "\n\n")
        self.txt_receipt.insert(tk.END, f"{'Thank You & Visit again':^41}")
        self.txt_receipt.insert(tk.END, "\n")

    def print_bill(self):
        bill = self.txt_receipt.get("1.0", tk.END)

        file = open(f"bills/{str(self.bill_no)}.txt", 'w')
        file.write(bill)
        file.close()

    def clear_all(self):
        self.sales_counter = 0
        self.total_amount.set(format_currency(0, 'INR', locale='en_IN'))
        self.sales_tree.delete(*self.sales_tree.get_children())
        self.discount.set(0)
        self.bill_amount.set(format_currency(0, 'INR', locale='en_IN'))
        self.btn_save_bill.config(state="normal")

    def save_bill(self):
        self.calculate_bill_amount()
        amount = self.total_amount.get()[1:].replace(',', '')
        discount = self.discount.get()
        bill_amount = self.total_amount.get()[1:].replace(',', '')

        if float(bill_amount) > 0:
            sales_date = datetime.now()
            bill = (sales_date, amount, discount, bill_amount)
            bill_no = Billing.create_bill(bill)
            self.bill_no = bill_no
            self.generate_bill_header(bill_no=bill_no)
            sl_no = 0
            quantity_sum = 0
            for child in self.sales_tree.get_children():
                product_id = self.sales_tree.item(child)["values"][1]
                product_name = self.sales_tree.item(child)["values"][2]
                price = self.sales_tree.item(child)["values"][3]
                quantity = self.sales_tree.item(child)["values"][4]
                sub_amount = self.sales_tree.item(child)["values"][5]

                sales = (sales_date, bill_no, product_id, quantity, sub_amount)
                Sales.add_sales(sales)

                stock = (product_id, quantity)
                Stock.compute_stock(stock)

                sl_no += 1
                quantity_sum = quantity_sum + quantity
                self.txt_receipt.insert(tk.END, f"{sl_no:^4}")
                self.txt_receipt.insert(tk.END, f"{product_name[:15]:<15}")
                self.txt_receipt.insert(tk.END, f"{quantity:^4}")
                self.txt_receipt.insert(tk.END, f"{price:>7}")
                self.txt_receipt.insert(tk.END, f"{sub_amount:>10}\n")

            self.generate_bill_footer(quantity_sum=quantity_sum, discount=discount, bill_amount=bill_amount)
            self.btn_save_bill.config(state="disabled")
            messagebox.showinfo("SS Fashion Tuty", f"Bill No: {bill_no} Saved!")

            # self.clear_all()

    def calculate_total_amount(self):
        total_amount = 0
        for child in self.sales_tree.get_children():
            total_amount += float(self.sales_tree.item(child)["values"][5])

        self.total_amount.set(format_currency(total_amount, 'INR', locale='en_IN'))

    def calculate_bill_amount(self):
        self.calculate_total_amount()

        total_amount = self.total_amount.get()[1:].replace(',', '')

        try:
            discount = self.discount.get()
        except TclError:
            discount = 0

        self.total_amount.set(format_currency(float(total_amount) - float(discount), 'INR', locale='en_IN'))
        self.bill_amount.set(format_currency(float(total_amount) - float(discount), 'INR', locale='en_IN'))

    def get_quantity(self, event):
        self.window.wm_attributes("-disabled", True)

        self.qty_window = tk.Toplevel(self.window)
        self.qty_window.overrideredirect(True)

        # Gets the requested values of the height and width.
        window_width = self.qty_window.winfo_reqwidth()
        window_height = self.qty_window.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        position_right = int(self.qty_window.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.qty_window.winfo_screenheight() / 2 - window_height / 2)

        # Positions the window in the center of the page.
        self.qty_window.geometry("+{}+{}".format(position_right, position_down))

        qty_container = tk.Frame(self.qty_window, bd=20, padx=10, pady=5, relief=tk.RIDGE, bg='orange')
        qty_container.pack(expand=True, side=tk.TOP, anchor="n")

        lbl_quantity = tk.Label(qty_container, text="Quantity: ", bg='orange')
        lbl_quantity.grid(row=0, column=0, padx=5, pady=2)

        ety_quantity = tk.Entry(qty_container, width=5, textvariable=self.quantity)
        ety_quantity.grid(row=1, column=0, padx=5, pady=2)

        ety_quantity.delete(0, tk.END)
        ety_quantity.insert(tk.END, 1)
        self.quantity.set(1)
        ety_quantity.focus()
        ety_quantity.selection_range(0, tk.END)

        btn_ok = tk.Button(qty_container, text='OK', width=10, command=lambda: self.cleanup(event))
        btn_ok.grid(row=2, column=0, padx=5, pady=5)
        self.qty_window.bind('<Return>', lambda evnt: self.cleanup(event))
        self.qty_window.bind('<Escape>', lambda evnt: self.cleanup(event, add_quantity=False))

    def cleanup(self, event, add_quantity=True):
        quantity = int(self.quantity.get())
        self.window.wm_attributes("-disabled", False)
        self.qty_window.destroy()

        if add_quantity:
            self.quantity.set(quantity)
            self.add_sales(event)

    def add_sales_by_button(self):
        self.tree.event_generate('<Return>')

    def add_sales(self, event):
        quantity = self.quantity.get()

        self.selected = event.widget.selection()
        product = self.tree.item(self.selected)['values']

        for child in self.sales_tree.get_children():
            if self.sales_tree.item(child)["values"][1] == product[0]:
                prev_quantity = self.sales_tree.item(child)["values"][4]
                price = self.sales_tree.item(child)["values"][3]

                quantity += prev_quantity
                self.sales_tree.set(child, "#4", quantity)
                self.sales_tree.set(child, "#5", float(price) * quantity)

                break
        else:
            product_short = f"{product[1]} {product[2]} {product[3]}"
            self.sales_counter = self.sales_counter + 1
            row = (self.sales_counter, product[0], product_short, round(float(product[4]), 2), quantity,
                   round(float(product[4]), 2) * quantity)

            self.sales_tree.insert("", tk.END, values=row)

        self.calculate_total_amount()

        if len(self.tree.selection()) > 0:
            self.tree.selection_remove(self.tree.selection()[0])

        self.ety_search_product_id.focus()
        self.ety_search_product_id.selection_range(0, tk.END)

    def reload_products(self):
        self.filter_ety_product_name.delete(0, tk.END)
        self.filter_ety_product_type.delete(0, tk.END)

        self.tree.delete(*self.tree.get_children())

        rows = Product.get_all_products()
        row_num = 0
        for row in rows:
            row_num += 1
            rw = (row.product_id, row.product_name, row.product_type, row.product_size,
                  round(row.selling_price, 2))

            if row_num % 2 == 0:
                self.tree.insert("", tk.END, values=rw, tags=('evenrow', row.product_id))
            else:
                self.tree.insert("", tk.END, values=rw, tags=('oddrow', row.product_id))

    def on_tree_select(self, event):
        self.selected = event.widget.selection()

        # for multi-select
        # for idx in self.selected:
        #     product = self.tree.item(idx)['values']

        product = self.tree.item(self.selected)['values']

        if product:
            self.product_id.set(product[0])
            self.product_name.set(product[1])
            self.product_type.set(product[2])
            self.product_size.set(product[3])
            self.selling_price.set(product[4])


class ViewProduct(MainForm):
    def __init__(self):
        super().__init__()

        # Set text variables
        self.product_id = tk.StringVar()
        self.product_name = tk.StringVar()
        self.product_name = tk.StringVar()
        self.product_type = tk.StringVar()
        self.product_size = tk.StringVar()
        self.selling_price = tk.DoubleVar()
        self.actual_price = tk.DoubleVar()

        self.search_product_id = tk.StringVar()

        self.filter_ety_product_name = None
        self.filter_ety_product_type = None

        self.ety_search_product_id = None

        # local variables
        self.tree = None
        self.selected = list()
        self.product_name_list = list()
        self.product_type_list = list()

        self.load_view_product_form()

    def load_view_product_form(self):
        self.update_username()

        products = Product.get_product_name_list()
        for product in products:
            self.product_name_list.append(product.product_name)

        products = Product.get_product_type_list()
        for product in products:
            self.product_type_list.append(product.product_type)

        # ********** Sub Containers *********
        left_container = tk.Frame(self.content_container, bd=5, padx=5, pady=5, relief=tk.RIDGE, bg='#62b6e2')
        left_container.pack(fill='both', expand=True, side=tk.LEFT)

        bill_container = tk.Frame(self.content_container, bd=5, padx=10, pady=10, relief=tk.RIDGE,
                                  bg='#62b6e2')
        bill_container.pack(fill='both', expand=True, side=tk.RIGHT)

        left_button_container = tk.Frame(left_container, padx=5, pady=5, relief=tk.RIDGE, bg='#62b6e2')
        left_button_container.pack(fill='both', expand=True, side=tk.TOP)

        search_container = tk.Frame(left_button_container, padx=5, pady=5, relief=tk.RIDGE, bg='#62b6e2')
        search_container.pack(fill='x', expand=True, side=tk.LEFT)

        filter_container = tk.Frame(left_button_container, padx=5, pady=5, relief=tk.RIDGE, bg='#62b6e2')
        filter_container.pack(fill='x', expand=True, side=tk.LEFT)

        # ********** left_search_container elements *********
        search_lbl_product_id = tk.Label(search_container, text="ID: ", bg='#62b6e2')
        search_lbl_product_id.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        self.ety_search_product_id = tk.Entry(search_container, width=10, textvariable=self.search_product_id)
        self.ety_search_product_id.grid(row=1, column=0, sticky="nw", padx=5, pady=5, ipady=6)
        self.ety_search_product_id.bind('<Return>', lambda event: self.search_product(event))

        btn_search = tk.Button(search_container, text="Search", command=self.search_product)
        btn_search.grid(row=1, column=1, sticky="sw", padx=5, pady=1)

        filter_lbl_product_name = tk.Label(filter_container, text="Name: ", bg='#62b6e2')
        filter_lbl_product_name.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        self.filter_ety_product_name = AutocompleteEntry(filter_container, width=20,
                                                         completevalues=self.product_name_list)
        self.filter_ety_product_name.grid(row=1, column=0, sticky="nw", padx=5, pady=5, ipady=6)
        self.filter_ety_product_name.bind("<Return>", lambda event: self.filter_product(event))

        # filter_product_name = tk.Entry(filter_container, width=20, textvariable=self.filter_product_name)
        # filter_product_name.grid(row=1, column=0, sticky="nw", padx=5, pady=5, ipady=6)

        filter_lbl_product_type = tk.Label(filter_container, text="Type: ", bg='#62b6e2')
        filter_lbl_product_type.grid(row=0, column=1, sticky="nw", padx=5, pady=5)
        self.filter_ety_product_type = AutocompleteEntry(filter_container, width=25,
                                                         completevalues=self.product_type_list)
        self.filter_ety_product_type.grid(row=1, column=1, sticky="nw", padx=5, pady=5, ipady=6)
        self.filter_ety_product_type.bind("<Return>", lambda event: self.filter_product(event))

        # filter_product_type = tk.Entry(filter_container, width=25, textvariable=self.filter_product_type)
        # filter_product_type.grid(row=1, column=1, sticky="nw", padx=5, pady=5, ipady=6)

        btn_filter = tk.Button(filter_container, text="Apply Filter", command=self.filter_product)
        btn_filter.grid(row=1, column=2, sticky="sw", padx=5, pady=1)

        btn_clear_filter = tk.Button(filter_container, text="Clear Filter", command=self.reload_products)
        btn_clear_filter.grid(row=1, column=3, sticky="sw", padx=5, pady=1)

        # left_container
        tree_container = tk.Frame(left_container, pady=3, bg='#62b6e2', relief=tk.RIDGE)
        tree_container.pack(fill='both', expand=True, side=tk.TOP)

        header = ('product_id', 'product_name', 'product_type', 'product_size', 'selling_price', 'actual_price',
                  'dummy')
        self.tree = ttk.Treeview(tree_container, columns=header, height=15, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Calibri', 12))
        style.configure("Treeview", font=('Calibri', 12),  rowheight=25)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=tree_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=tree_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=tree_container)

        tree_container.grid_columnconfigure(0, weight=1)
        tree_container.grid_rowconfigure(0, weight=1)

        self.tree.heading("0", text="P_ID")
        self.tree.heading("1", text="PRODUCT_NAME")
        self.tree.heading("2", text="PRODUCT_TYPE")
        self.tree.heading("3", text="SIZE")
        self.tree.heading("4", text="SELL_PRICE")
        self.tree.heading("5", text="ACTUAL_PRICE")

        self.tree.column(0, anchor='center', width="80")
        self.tree.column(1, anchor=tk.W, width="150")
        self.tree.column(2, anchor=tk.W, width="200")
        self.tree.column(3, anchor='center', width="100")
        self.tree.column(4, anchor=tk.E, width="100")
        self.tree.column(5, anchor=tk.E, width="100")
        self.tree.column(6, anchor='center', width="5")

        self.reload_products()

        lbl_product_details = tk.Label(bill_container, text="Product Details", bg='#62b6e2')
        lbl_product_details.grid(row=0, column=0, columnspan=3, sticky="news", padx=3, pady=3)
        lbl_product_details.config(font=("Calibri bold", 24))

        lbl_dummy = tk.Label(bill_container, text="", bg='#62b6e2')
        lbl_dummy.grid(row=1, column=0, columnspan=3, sticky="news", padx=3, pady=3)
        lbl_dummy.config(font=("Calibri bold", 10))

        lbl_product_id = tk.Label(bill_container, text="ID: ", bg='#62b6e2')
        lbl_product_id.grid(row=2, column=0, sticky="nw", padx=3, pady=8)
        product_id = tk.Entry(bill_container, width=10, textvariable=self.product_id, state='disabled')
        product_id.grid(row=2, column=1, sticky="nw", padx=3, pady=8)

        lbl_product_name = tk.Label(bill_container, text="Product Name: ", bg='#62b6e2')
        lbl_product_name.grid(row=3, column=0, sticky="nw", padx=3, pady=8)
        product_name = tk.Entry(bill_container, textvariable=self.product_name)
        product_name.grid(row=3, column=1, columnspan=2, sticky="nw", padx=3, pady=8)

        lbl_product_type = tk.Label(bill_container, text="Product Type: ", bg='#62b6e2')
        lbl_product_type.grid(row=4, column=0, sticky="nw", padx=3, pady=8)
        product_type = tk.Entry(bill_container, textvariable=self.product_type)
        product_type.grid(row=4, column=1, columnspan=2, sticky="nw", padx=3, pady=8)

        lbl_product_size = tk.Label(bill_container, text="Size: ", bg='#62b6e2')
        lbl_product_size.grid(row=5, column=0, sticky="nw", padx=3, pady=8)
        product_size = tk.Entry(bill_container, textvariable=self.product_size)
        product_size.grid(row=5, column=1, columnspan=2, sticky="nw", padx=3, pady=8)

        lbl_selling_price = tk.Label(bill_container, text="Selling Price: ", bg='#62b6e2')
        lbl_selling_price.grid(row=6, column=0, sticky="nw", padx=3, pady=8)
        selling_price = tk.Entry(bill_container, width=10, textvariable=self.selling_price)
        selling_price.grid(row=6, column=1, sticky="nw", padx=3, pady=8)

        lbl_actual_price = tk.Label(bill_container, text="Actual Price: ", bg='#62b6e2')
        lbl_actual_price.grid(row=7, column=0, sticky="nw", padx=3, pady=8)
        actual_price = tk.Entry(bill_container, width=10, textvariable=self.actual_price)
        actual_price.grid(row=7, column=1, sticky="nw", padx=3, pady=8)

        btn_update_product = tk.Button(bill_container, text="Save Changes", command=self.update_product)
        btn_update_product.grid(row=9, column=1, rowspan=2, sticky="news", padx=3, pady=8)

        btn_delete_product = tk.Button(bill_container, text="Delete", command=self.delete_product)
        btn_delete_product.grid(row=9, column=2, rowspan=2, sticky="news", padx=3, pady=8)

        btn_add = tk.Button(bill_container, text="Add Product", command=self.add_product)
        btn_add.grid(row=11, column=1, columnspan=2, rowspan=2, sticky="news", padx=3, pady=3)

        btn_close = tk.Button(self.footer_container, text="Close", width='20', command=self.window.destroy)
        btn_close.pack(padx=5, pady=5)

        self.tree.tag_configure("evenrow", background='#fbefcc')
        self.tree.tag_configure("oddrow", background='white', foreground='black')
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

    def filter_product(self, event=None):
        product_name = self.filter_ety_product_name.get().strip()
        product_type = self.filter_ety_product_type.get().strip()

        products = Product.search_products(product_name=product_name, product_type=product_type)
        self.tree.delete(*self.tree.get_children())

        if products:
            row_num = 0
            for product in products:
                row_num += 1
                row = (product.product_id, product.product_name, product.product_type, product.product_size,
                       round(product.selling_price, 2), round(product.actual_price, 2))

                if row_num % 2 == 0:
                    self.tree.insert("", tk.END, values=row, tags=('evenrow', product.product_id))
                else:
                    self.tree.insert("", tk.END, values=row, tags=('oddrow', product.product_id))
        else:
            pass

    def clear_all(self):
        self.product_id.set("")
        self.product_name.set("")
        self.product_type.set("")
        self.product_size.set("")
        self.selling_price.set(0.0)
        self.actual_price.set(0.0)

    def search_product(self, event=None):
        product_id = self.search_product_id.get().strip()

        products = Product.search_products(product_id=product_id)
        if products is None:
            messagebox.showerror("SS Fashion Tuty", f"Product_id: {product_id} not found!")
            print(f"Product_id: {product_id} not found!")
        if isinstance(products, Product):
            self.tree.selection_set(self.tree.tag_has(str(product_id)))
            self.tree.focus_set()
            self.tree.focus(self.selected)
        else:
            pass

    def add_product(self):
        product_name = self.product_name.get().strip()  # .lower()
        product_type = self.product_type.get().strip()  # .lower()
        product_size = self.product_size.get().strip()  # .lower()

        try:
            selling_price = round(self.selling_price.get(), 2)
        except TclError:
            selling_price = 0.0

        try:
            actual_price = round(self.actual_price.get(), 2)
        except TclError:
            actual_price = 0.0

        if len(product_name) == 0:
            messagebox.showerror("SS Fashion Tuty", f"Product_Name is missing!")
            print(f"Product_Name is missing!")
            return

        if selling_price == "" or selling_price <= 0:
            messagebox.showerror("SS Fashion Tuty", f"Selling Price is missing!")
            print(f"selling price is missing!")
            return

        if len(product_type) == 0:
            product_type = "-"

        if len(product_size) == 0:
            product_size = "-"

        product = (product_name, product_type, product_size, selling_price, actual_price)
        Product.add_product(product)

        self.reload_products()

        print(f"Product: '{product_name}' is added!")
        msg_box = tk.messagebox.askquestion("SS Fashion Tuty", 'Product added! Do you want to add same product again?',
                                            icon='info')
        if msg_box == 'yes':
            pass
        else:
            self.clear_all()

    def reload_products(self):
        self.filter_ety_product_name.delete(0, tk.END)
        self.filter_ety_product_type.delete(0, tk.END)

        self.tree.delete(*self.tree.get_children())

        products = Product.get_all_products()

        row_num = 0
        for product in products:
            row_num += 1
            row = (product.product_id, product.product_name, product.product_type, product.product_size,
                   round(product.selling_price, 2), round(product.actual_price, 2))

            if row_num % 2 == 0:
                self.tree.insert("", tk.END, values=row, tags=('evenrow', product.product_id))
            else:
                self.tree.insert("", tk.END, values=row, tags=('oddrow', product.product_id))

    def on_tree_select(self, event):
        self.selected = event.widget.selection()

        # for multi-select
        # for idx in self.selected:
        #     product = self.tree.item(idx)['values']

        product = self.tree.item(self.selected)['values']

        if product:
            self.product_id.set(product[0])
            self.product_name.set(product[1])
            self.product_type.set(product[2])
            self.product_size.set(product[3])
            self.selling_price.set(product[4])
            self.actual_price.set(product[5])

    def update_product(self):
        product_id = self.product_id.get()
        product_name = self.product_name.get().strip()  # .lower()
        product_type = self.product_type.get().strip()  # .lower()
        product_size = self.product_size.get().strip()  # .lower()

        try:
            selling_price = round(self.selling_price.get(), 2)
        except TclError:
            selling_price = 0.0

        try:
            actual_price = round(self.actual_price.get(), 2)
        except TclError:
            actual_price = 0.0

        if len(product_name) == 0:
            messagebox.showerror("SS Fashion Tuty", f"Product_Name is missing!")
            print(f"Product_Name is missing!")
            return

        if selling_price == "" or selling_price <= 0:
            messagebox.showerror("SS Fashion Tuty", f"Selling Price is missing!")
            print(f"Selling Price is missing!")
            return

        if len(product_type) == 0:
            product_type = "-"

        if len(product_size) == 0:
            product_size = "-"

        product = (product_id, product_name, product_type, product_size, selling_price, actual_price)
        Product.update_product(product)
        self.reload_products()
        print(f"Product: '{product_name}' is updated!")
        messagebox.showinfo("SS Fashion Tuty", f"Product: '{product_name}' is updated!")

    def delete_product(self):
        product_id = self.product_id.get()

        product = Product.get_product(product_id)
        if product:
            msg_box = tk.messagebox.askquestion("SS Fashion Tuty", 'Are you sure to delete?', icon='info')
            if msg_box == 'yes':
                Product.delete_product(product.product_id)

                messagebox.showinfo("SS Fashion Tuty", f"Product_Id: {product_id} deleted!")
                print(f"Product_Id: {product_id} deleted!")

                self.product_id.set("")
                self.product_name.set("")
                self.product_type.set("")
                self.product_size.set("")
                self.selling_price.set(0.0)
                self.actual_price.set(0.0)

                self.reload_products()
            else:
                pass
        else:
            messagebox.showerror("SS Fashion Tuty", f"Product_Id: {product_id} not found!")
            print(f"Product_Id: {product_id} not found!")


class ViewStock(MainForm):
    def __init__(self):
        super().__init__()

        # Set text variables
        self.product_id = tk.StringVar()
        self.product_name = tk.StringVar()
        self.product_name = tk.StringVar()
        self.product_type = tk.StringVar()
        self.product_size = tk.StringVar()
        self.selling_price = tk.DoubleVar()
        self.actual_price = tk.DoubleVar()
        self.quantity = tk.IntVar()

        self.search_product_id = tk.StringVar()

        self.filter_ety_product_name = None
        self.filter_ety_product_type = None

        self.ety_search_product_id = None

        # local variables
        self.tree = None
        self.selected = list()
        self.product_name_list = list()
        self.product_type_list = list()

        self.load_view_stock_form()

    def load_view_stock_form(self):
        self.update_username()

        products = Product.get_product_name_list()
        for product in products:
            self.product_name_list.append(product.product_name)

        products = Product.get_product_type_list()
        for product in products:
            self.product_type_list.append(product.product_type)

        # ********** Sub Containers *********
        left_container = tk.Frame(self.content_container, bd=5, padx=5, pady=5, relief=tk.RIDGE, bg='#62b6e2')
        left_container.pack(fill='both', expand=True, side=tk.LEFT)

        bill_container = tk.Frame(self.content_container, bd=5, padx=10, pady=10, relief=tk.RIDGE,
                                  bg='#62b6e2')
        bill_container.pack(fill='both', expand=True, side=tk.RIGHT)

        left_button_container = tk.Frame(left_container, padx=5, pady=5, relief=tk.RIDGE, bg='#62b6e2')
        left_button_container.pack(fill='both', expand=True, side=tk.TOP)

        search_container = tk.Frame(left_button_container, padx=5, pady=5, relief=tk.RIDGE, bg='#62b6e2')
        search_container.pack(fill='x', expand=True, side=tk.LEFT)

        filter_container = tk.Frame(left_button_container, padx=5, pady=5, relief=tk.RIDGE, bg='#62b6e2')
        filter_container.pack(fill='x', expand=True, side=tk.LEFT)

        # ********** left_search_container elements *********
        search_lbl_product_id = tk.Label(search_container, text="ID: ", bg='#62b6e2')
        search_lbl_product_id.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        self.ety_search_product_id = tk.Entry(search_container, width=10, textvariable=self.search_product_id)
        self.ety_search_product_id.grid(row=1, column=0, sticky="nw", padx=5, pady=5, ipady=6)
        self.ety_search_product_id.bind('<Return>', lambda event: self.search_stock(event))

        btn_search = tk.Button(search_container, text="Search", command=self.search_stock)
        btn_search.grid(row=1, column=1, sticky="sw", padx=5, pady=1)

        filter_lbl_product_name = tk.Label(filter_container, text="Name: ", bg='#62b6e2')
        filter_lbl_product_name.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        self.filter_ety_product_name = AutocompleteEntry(filter_container, completevalues=self.product_name_list)
        self.filter_ety_product_name.grid(row=1, column=0, sticky="nw", padx=5, pady=5, ipady=6)
        self.filter_ety_product_name.bind("<Return>", lambda event: self.filter_stock(event))

        # filter_product_name = tk.Entry(filter_container, width=20, textvariable=self.filter_product_name)
        # filter_product_name.grid(row=1, column=0, sticky="nw", padx=5, pady=5, ipady=6)

        filter_lbl_product_type = tk.Label(filter_container, text="Type: ", bg='#62b6e2')
        filter_lbl_product_type.grid(row=0, column=1, sticky="nw", padx=5, pady=5)
        self.filter_ety_product_type = AutocompleteEntry(filter_container, completevalues=self.product_type_list)
        self.filter_ety_product_type.grid(row=1, column=1, sticky="nw", padx=5, pady=5, ipady=6)
        self.filter_ety_product_type.bind("<Return>", lambda event: self.filter_stock(event))

        # filter_product_type = tk.Entry(filter_container, width=25, textvariable=self.filter_product_type)
        # filter_product_type.grid(row=1, column=1, sticky="nw", padx=5, pady=5, ipady=6)

        btn_filter = tk.Button(filter_container, text="Apply Filter", command=self.filter_stock)
        btn_filter.grid(row=1, column=2, sticky="sw", padx=5, pady=1)

        btn_clear_filter = tk.Button(filter_container, text="Clear Filter", command=self.reload_stock)
        btn_clear_filter.grid(row=1, column=3, sticky="sw", padx=5, pady=1)

        # ********** left_container *********
        tree_container = tk.Frame(left_container, pady=3, bg='#62b6e2')
        tree_container.pack(fill='both', expand=True, side=tk.TOP)

        header = ('#', 'product_id', 'product_name', 'product_type', 'product_size', 'selling_price', 'actual_price',
                  'quantity', 'dummy')
        self.tree = ttk.Treeview(tree_container, columns=header, show="headings", height=15, selectmode="browse")
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Calibri', 12))
        style.configure("Treeview", font=('Calibri', 12), rowheight=25)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=tree_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=tree_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=tree_container)

        tree_container.grid_columnconfigure(0, weight=1)
        tree_container.grid_rowconfigure(0, weight=1)

        self.tree.heading("0", text="#")
        self.tree.heading("1", text="ID")
        self.tree.heading("2", text="PRODUCT_NAME")
        self.tree.heading("3", text="PRODUCT_TYPE")
        self.tree.heading("4", text="SIZE")
        self.tree.heading("5", text="SELL_PRICE")
        self.tree.heading("6", text="ACTUAL_PRICE")
        self.tree.heading("7", text="QTY")

        self.tree.column(0, anchor='center', width="50")
        self.tree.column(1, anchor='center', width="50")
        self.tree.column(2, anchor=tk.W, width="150")
        self.tree.column(3, anchor=tk.W, width="200")
        self.tree.column(4, anchor='center', width="100")
        self.tree.column(5, anchor=tk.E, width="100")
        self.tree.column(6, anchor=tk.E, width="120")
        self.tree.column(7, anchor='center', width="80")
        self.tree.column(8, anchor='center', width="5")

        self.reload_stock()

        lbl_product_details = tk.Label(bill_container, text="Product Details", bg='#62b6e2')
        lbl_product_details.grid(row=0, column=0, columnspan=3, sticky="news", padx=3, pady=3)
        lbl_product_details.config(font=("Calibri bold", 24))

        lbl_dummy = tk.Label(bill_container, text="", bg='#62b6e2')
        lbl_dummy.grid(row=1, column=0, columnspan=3, sticky="news", padx=3, pady=3)
        lbl_dummy.config(font=("Calibri bold", 10))

        lbl_product_id = tk.Label(bill_container, text="ID: ", bg='#62b6e2')
        lbl_product_id.grid(row=2, column=0, sticky="nw", padx=3, pady=8)
        product_id = tk.Entry(bill_container, width=10, textvariable=self.product_id, state='disabled')
        product_id.grid(row=2, column=1, sticky="nw", padx=3, pady=8)

        lbl_product_name = tk.Label(bill_container, text="Product Name: ", bg='#62b6e2')
        lbl_product_name.grid(row=3, column=0, sticky="nw", padx=3, pady=8)
        product_name = tk.Entry(bill_container, textvariable=self.product_name, state='disabled')
        product_name.grid(row=3, column=1, columnspan=2, sticky="nw", padx=3, pady=8)

        lbl_product_type = tk.Label(bill_container, text="Product Type: ", bg='#62b6e2')
        lbl_product_type.grid(row=4, column=0, sticky="nw", padx=3, pady=8)
        product_type = tk.Entry(bill_container, textvariable=self.product_type, state='disabled')
        product_type.grid(row=4, column=1, columnspan=2, sticky="nw", padx=3, pady=8)

        lbl_product_size = tk.Label(bill_container, text="Size: ", bg='#62b6e2')
        lbl_product_size.grid(row=5, column=0, sticky="nw", padx=3, pady=8)
        product_size = tk.Entry(bill_container, textvariable=self.product_size, state='disabled')
        product_size.grid(row=5, column=1, columnspan=2, sticky="nw", padx=3, pady=8)

        lbl_selling_price = tk.Label(bill_container, text="Selling Price: ", bg='#62b6e2')
        lbl_selling_price.grid(row=6, column=0, sticky="nw", padx=3, pady=8)
        selling_price = tk.Entry(bill_container, width=10, textvariable=self.selling_price, state='disabled')
        selling_price.grid(row=6, column=1, sticky="nw", padx=3, pady=8)

        lbl_actual_price = tk.Label(bill_container, text="Actual Price: ", bg='#62b6e2')
        lbl_actual_price.grid(row=7, column=0, sticky="nw", padx=3, pady=8)
        actual_price = tk.Entry(bill_container, width=10, textvariable=self.actual_price, state='disabled')
        actual_price.grid(row=7, column=1, sticky="nw", padx=3, pady=8)

        lbl_quantity = tk.Label(bill_container, text="Quantity: ", bg='#62b6e2')
        lbl_quantity.grid(row=8, column=0, sticky="nw", padx=3, pady=3)
        quantity = tk.Entry(bill_container, width=10, textvariable=self.quantity)
        quantity.grid(row=8, column=1, sticky="nw", padx=3, pady=3)

        btn_update_stock = tk.Button(bill_container, text="Save Changes", command=self.update_stock)
        btn_update_stock.grid(row=9, column=1, rowspan=2, sticky="news", padx=3, pady=3)

        btn_clear_stock = tk.Button(bill_container, text="Clear Stock", command=self.clear_stock)
        btn_clear_stock.grid(row=9, column=2, rowspan=2, sticky="news", padx=3, pady=3)

        btn_close = tk.Button(self.footer_container, text="Close", width='20', command=self.window.destroy)
        btn_close.pack(padx=5, pady=5)

        self.tree.tag_configure("evenrow", background='#fbefcc')
        self.tree.tag_configure("oddrow", background='white', foreground='black')
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

    def filter_stock(self, event=None):
        product_name = self.filter_ety_product_name.get().strip()
        product_type = self.filter_ety_product_type.get().strip()

        rows = Stock.search_stock(product_name=product_name, product_type=product_type)
        self.tree.delete(*self.tree.get_children())

        if len(rows):
            sl_no = 0
            for row in rows:
                product = row.Product
                stock = row.Stock

                sl_no = sl_no + 1
                quantity = "-"
                if stock:
                    quantity = stock.quantity

                rw = (sl_no, product.product_id, product.product_name, product.product_type, product.product_size,
                      round(product.selling_price, 2), round(product.actual_price, 2), quantity)

                if sl_no % 2 == 0:
                    self.tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_id))
                else:
                    self.tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_id))
        else:
            pass

    def reload_stock(self):
        self.filter_ety_product_name.delete(0, tk.END)
        self.filter_ety_product_type.delete(0, tk.END)

        self.tree.delete(*self.tree.get_children())

        rows = Stock.get_all_stocks()
        sl_no = 0
        for row in rows:
            product = row.Product
            stock = row.Stock

            sl_no = sl_no + 1
            quantity = "-"
            if stock:
                quantity = stock.quantity

            rw = (sl_no, product.product_id, product.product_name, product.product_type, product.product_size,
                  round(product.selling_price, 2), round(product.actual_price, 2), quantity)

            if sl_no % 2 == 0:
                self.tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_id))
            else:
                self.tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_id))

    def search_stock(self, event=None):
        product_id = self.search_product_id.get().strip()

        row = Stock.search_stock(product_id=product_id)
        if len(row):
            self.tree.selection_set(self.tree.tag_has(str(product_id)))
            self.tree.focus_set()
            self.tree.focus(self.selected)
        else:
            messagebox.showerror("SS Fashion Tuty", f"Product_id: {product_id} not found!")
            print(f"Product_id: {product_id} not found!")

    def on_tree_select(self, event):
        self.selected = event.widget.selection()

        # for multi-select
        # for idx in self.selected:
        #     product = self.tree.item(idx)['values']

        product = self.tree.item(self.selected)['values']

        self.product_id.set(product[1])
        self.product_name.set(product[2])
        self.product_type.set(product[3])
        self.product_size.set(product[4])
        self.selling_price.set(product[5])
        self.actual_price.set(product[6])
        self.quantity.set(product[7])

    def update_stock(self):
        product_id = self.product_id.get().strip().lower()

        try:
            quantity = round(self.quantity.get(), 0)
        except TclError:
            quantity = 0

        if quantity == "" or quantity < 0:
            messagebox.showerror("SS Fashion Tuty", f"quantity is missing!")
            print(f"quantity is missing!")
            return

        stock = (product_id, quantity)
        Stock.update_stock(stock)

        self.reload_stock()

        messagebox.showinfo("SS Fashion Tuty", f"Product: '{product_id}' is updated!")
        print(f"product: '{product_id}' is updated!")

    def clear_stock(self):
        product_id = self.product_id.get()

        stock = Stock.get_stock(product_id)
        if stock:
            msg_box = tk.messagebox.askquestion("SS Fashion Tuty", 'Are you sure to clear stock?', icon='info')
            if msg_box == 'yes':
                Stock.clear_stock(stock.product_id)
                self.quantity.set(0)
                self.reload_stock()

                print(f"Stock cleared for product_id: '{product_id}' !")
                messagebox.showinfo("SS Fashion Tuty", f"Stock cleared for product_id: '{product_id}' !")
            else:
                pass
        else:
            print(f"Product_id: {product_id} not found!")
            messagebox.showerror("SS Fashion Tuty", f"Product_id: {product_id} not found!")


class ViewBills(MainForm):
    def __init__(self):
        super().__init__()

        # Set text variables
        self.bill_no = tk.StringVar()
        self.bill_date = tk.StringVar()
        self.total_amount = tk.DoubleVar()
        self.discount = tk.DoubleVar()
        self.bill_amount = tk.DoubleVar()

        self.search_bill_no = tk.StringVar()

        # local variables
        self.tree = None
        self.sales_tree = None
        self.ety_search_bill_no = None
        self.tree_container = None
        self.lbl_total_amount = None
        self.filter_bill_date = None
        self.txt_receipt = None

        self.selected = []
        self.sales_counter = 0

        self.load_view_bills_form()

    def load_view_bills_form(self):
        for index in range(1, 9):
            self.menubar.entryconfig(index, state=tk.DISABLED)

        self.show_menu(MainForm.is_admin_user)
        self.update_username()

        # ********** Sub Containers *********
        left_container = tk.Frame(self.content_container, bd=5, padx=5, pady=2, relief=tk.RIDGE, bg='#62b6e2')
        left_container.pack(fill='both', expand=True, side=tk.LEFT)

        bill_container = tk.Frame(self.content_container, bd=5, padx=5, pady=5, relief=tk.RIDGE, bg='#62b6e2')
        bill_container.pack(fill='both', expand=True, side=tk.RIGHT)

        # left_container elements
        top_button_container = tk.Frame(left_container, relief=tk.RIDGE, bg='#62b6e2')
        top_button_container.pack(fill='both', expand=True, side=tk.TOP)

        search_container = tk.Frame(top_button_container, relief=tk.RIDGE, bg='#62b6e2')
        search_container.pack(fill='x', expand=True, side=tk.LEFT)

        filter_container = tk.Frame(top_button_container, relief=tk.RIDGE, bg='#62b6e2')
        filter_container.pack(fill='x', expand=True, side=tk.RIGHT)

        bottom_button_container = tk.Frame(left_container, relief=tk.RIDGE, bg='#62b6e2')
        bottom_button_container.pack(fill='both', expand=True, side=tk.BOTTOM)

        left_button_container = tk.Frame(bottom_button_container, relief=tk.RIDGE, bg='#62b6e2')
        left_button_container.pack(fill='both', expand=True, anchor='center', side=tk.LEFT)

        right_button_container = tk.Frame(bottom_button_container, relief=tk.RIDGE, bg='#62b6e2')
        right_button_container.pack(fill='both', expand=True, anchor='center', side=tk.RIGHT)

        # ********** left_search_container elements *********
        search_lbl_bill_no = tk.Label(search_container, text="Bill #: ", bg='#62b6e2')
        search_lbl_bill_no.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        self.ety_search_bill_no = tk.Entry(search_container, width=10, textvariable=self.search_bill_no)
        self.ety_search_bill_no.grid(row=1, column=0, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_search_bill_no.bind('<Return>', lambda event: self.search_bill(event))

        btn_search = tk.Button(search_container, text="Search", command=self.search_bill)
        btn_search.grid(row=1, column=1, sticky="sw", padx=2, pady=1)

        filter_lbl_bill_date = tk.Label(filter_container, text='Bill Date: ', bg='#62b6e2')
        filter_lbl_bill_date.grid(row=0, column=1, sticky="nw", padx=1, pady=1)
        self.filter_bill_date = DateEntry(filter_container, date_pattern='yyyy-mm-dd', background='yellow',
                                          foreground='black', borderwidth=2)
        self.filter_bill_date.grid(row=1, column=1, sticky="nw", padx=2, pady=1, ipady=6)

        btn_filter = tk.Button(filter_container, text="Apply Filter", command=self.filter_bill)
        btn_filter.grid(row=1, column=2, sticky="sw", padx=2, pady=1)

        btn_clear_filter = tk.Button(filter_container, text="Clear Filter", command=self.reload_bills)
        btn_clear_filter.grid(row=1, column=3, sticky="sw", padx=2, pady=1)

        # ********** tree_containers elements *********
        self.tree_container = tk.Frame(left_container, pady=3, bg='#62b6e2', relief=tk.RIDGE)
        self.tree_container.pack(fill='both', expand=True, side=tk.TOP)

        header = ('bill #', 'bill_date', 'total_amount', 'discount', 'bill_amount', 'dummy')
        self.tree = ttk.Treeview(self.tree_container, columns=header, height=8, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(self.tree_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.tree_container, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Calibri', 12))
        style.configure("Treeview", font=('Calibri', 12), rowheight=25)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.tree_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=self.tree_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=self.tree_container)

        self.tree_container.grid_columnconfigure(0, weight=1)
        self.tree_container.grid_rowconfigure(0, weight=1)

        self.tree.heading("0", text="BILL #")
        self.tree.heading("1", text="BILL_DATE")
        self.tree.heading("2", text="TOTAL_AMOUNT")
        self.tree.heading("3", text="DISCOUNT")
        self.tree.heading("4", text="BILL_AMOUNT")

        self.tree.column(0, anchor='center', width="80")
        self.tree.column(1, anchor=tk.W, width="150")
        self.tree.column(2, anchor=tk.E, width="100")
        self.tree.column(3, anchor=tk.E, width="80")
        self.tree.column(4, anchor=tk.E, width="100")
        self.tree.column(5, anchor='center', width="5")

        self.reload_bills()

        # ********** Product Details *********
        bill_details_container = tk.Frame(left_container, bd=5, pady=3, relief=tk.RIDGE, bg='#62b6e2')
        bill_details_container.pack(fill='both', expand=True, side=tk.LEFT)

        lbl_bill_details = tk.Label(bill_details_container, text="Bill Details", bg='#62b6e2')
        lbl_bill_details.grid(row=0, column=0, columnspan=2, sticky="news", padx=3, pady=1)
        lbl_bill_details.config(font=("Calibri bold", 14))

        lbl_bill_no = tk.Label(bill_details_container, text="BILL #: ", bg='#62b6e2')
        lbl_bill_no.grid(row=1, column=0, sticky="nw", padx=3, pady=1)
        bill_id = tk.Entry(bill_details_container, width=10, textvariable=self.bill_no, state='disabled')
        bill_id.grid(row=1, column=1, sticky="nw", padx=3, pady=1)

        lbl_date = tk.Label(bill_details_container, text="Bill Date: ", bg='#62b6e2')
        lbl_date.grid(row=2, column=0, sticky="nw", padx=3, pady=1)
        bill_date = tk.Entry(bill_details_container, textvariable=self.bill_date, width=22, state='disabled')
        bill_date.grid(row=2, column=1, columnspan=2, sticky="nw", padx=3, pady=1)

        lbl_total_amount = tk.Label(bill_details_container, text="Total Amount: ", bg='#62b6e2')
        lbl_total_amount.grid(row=3, column=0, sticky="nw", padx=3, pady=1)
        total_amount = tk.Entry(bill_details_container, width=12, textvariable=self.total_amount, state='disabled')
        total_amount.grid(row=3, column=1, columnspan=2, sticky="nw", padx=3, pady=1)

        lbl_discount = tk.Label(bill_details_container, text="Discount: ", bg='#62b6e2')
        lbl_discount.grid(row=4, column=0, sticky="nw", padx=3, pady=3)
        discount = tk.Entry(bill_details_container, width=12, textvariable=self.discount, state='disabled')
        discount.grid(row=4, column=1, columnspan=2, sticky="nw", padx=3, pady=1)

        lbl_bill_amount = tk.Label(bill_details_container, text="Bill Amount: ", bg='#62b6e2')
        lbl_bill_amount.grid(row=5, column=0, sticky="nw", padx=3, pady=1)
        bill_amount = tk.Entry(bill_details_container, width=12, textvariable=self.bill_amount, state='disabled')
        bill_amount.grid(row=5, column=1, sticky="nw", padx=3, pady=1)

        # ********** Sales Tree Details *********
        sales_tree_container = tk.Frame(left_container, bd=5, pady=3, relief=tk.RIDGE, bg='#62b6e2')
        sales_tree_container.pack(fill='both', expand=True, side=tk.RIGHT)

        header = ('#', 'product_id', 'product_name', 'selling_price', 'quantity', 'amount', 'dummy')
        self.sales_tree = ttk.Treeview(sales_tree_container, columns=header, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(sales_tree_container, orient="vertical", command=self.sales_tree.yview)
        hsb = ttk.Scrollbar(sales_tree_container, orient="horizontal", command=self.sales_tree.xview)

        self.sales_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.sales_tree.grid(column=0, row=0, sticky='nsew')

        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        sales_tree_container.grid_columnconfigure(0, weight=1)
        sales_tree_container.grid_rowconfigure(0, weight=1)

        self.sales_tree.heading("0", text="#")
        self.sales_tree.heading("1", text="PRODUCT_ID")
        self.sales_tree.heading("2", text="PRODUCT")
        self.sales_tree.heading("3", text="PRICE")
        self.sales_tree.heading("4", text="QTY")
        self.sales_tree.heading("5", text="Amount")

        self.sales_tree.column(0, anchor='center', minwidth=50, width=50)
        self.sales_tree.column(3, anchor=tk.E, minwidth=100, width=100)
        self.sales_tree.column(4, anchor='center', minwidth=100, width=100)
        self.sales_tree.column(5, anchor=tk.E, minwidth=100, width=100)
        self.sales_tree.column(6, anchor='center', width=5)
        self.sales_tree["displaycolumns"] = (0, 2, 3, 4, 5, 6)

        self.tree.tag_configure("evenrow", background='#fbefcc')
        self.tree.tag_configure("oddrow", background='white', foreground='black')
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        # ********** bottom_button_container elements *********
        btn_close = tk.Button(left_button_container, text="Close", command=self.window.destroy)
        btn_close.pack(side=tk.LEFT, expand=True, fill='both', padx=5, pady=1)
        btn_close.config(font=("calibri", 22))

        self.lbl_total_amount = tk.Label(right_button_container, fg='Red', relief=tk.RAISED,
                                         textvariable=self.total_amount, width=10)
        self.lbl_total_amount.pack(side=tk.RIGHT, expand=True, fill='both', padx=1, pady=1)
        self.lbl_total_amount.config(font=("calibri bold", 34))
        self.total_amount.set(format_currency(0, 'INR', locale='en_IN'))

        lbl_discount = tk.Label(right_button_container, text='Discount: ', bg='#62b6e2')
        lbl_discount.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=1)

        ety_discount = tk.Entry(right_button_container, width=5, textvariable=self.discount, state='disabled')
        ety_discount.pack(side=tk.LEFT, fill='x', expand=True, padx=5, pady=1)
        ety_discount.config(font=("calibri", 14))

        # ********** bill_container elements *********
        self.txt_receipt = tk.Text(bill_container, height=22, bg='white', bd=4, font=('Calibri', 12))
        self.txt_receipt.pack(side=tk.TOP, expand=True, fill='x', padx=1, pady=1)

        lbl_bill_amount = tk.Label(bill_container, fg='Blue', relief=tk.RAISED,
                                   textvariable=self.bill_amount)
        lbl_bill_amount.pack(side=tk.TOP, expand=True, fill='x', padx=1, pady=1)
        lbl_bill_amount.config(font=("calibri bold", 46))
        self.bill_amount.set(format_currency(0, 'INR', locale='en_IN'))

        btn_print_bill = tk.Button(bill_container, text="Print Bill", fg='Black', command=self.print_bill)
        btn_print_bill.pack(side=tk.LEFT, expand=True, fill='x', padx=1, pady=1)
        btn_print_bill.config(font=("calibri bold", 22))

    def clear_all(self):
        self.bill_no.set("")
        self.bill_date.set("")
        self.total_amount.set(format_currency(0, 'INR', locale='en_IN'))
        self.discount.set(0)
        self.bill_amount.set(format_currency(0, 'INR', locale='en_IN'))

        self.sales_tree.delete(*self.sales_tree.get_children())

    def filter_bill(self):
        self.clear_all()

        bill_date = self.filter_bill_date.get().strip()

        bills = Billing.search_bills(bill_date=bill_date)
        self.tree.delete(*self.tree.get_children())
        if bills:
            row_num = 0
            for bill in bills:
                row_num += 1
                row = (bill.bill_number, datetime.strftime(bill.bill_date, '%d-%b-%Y %I:%M:%S %p'),
                       round(bill.amount, 2), round(bill.discount, 2),
                       round(bill.bill_amount, 2))

                if row_num % 2 == 0:
                    self.tree.insert("", tk.END, values=row, tags=('evenrow', bill.bill_number))
                else:
                    self.tree.insert("", tk.END, values=row, tags=('oddrow', bill.bill_number))
        else:
            pass

    def search_bill(self, event=None):
        bill_number = self.search_bill_no.get().strip()

        bills = Billing.search_bills(bill_number=bill_number)
        if bills is None:
            messagebox.showerror("SS Fashion Tuty", f"Bill_No: {bill_number} not found!")
            print(f"Bill_No: {bill_number} not found!")
        if isinstance(bills, Billing):
            self.tree.selection_set(self.tree.tag_has(str(bill_number)))
            self.tree.focus_set()
            self.tree.focus(self.selected)
        else:
            pass

    def print_bill(self):
        # Receipt
        self.txt_receipt.delete("1.0", tk.END)
        self.txt_receipt.tag_configure('align_center', justify='center')
        self.txt_receipt.tag_configure('align_left', justify='left')
        self.txt_receipt.tag_configure('align_right', justify='right')

        self.txt_receipt.insert(tk.END, "SS Fashion Tuty\n", 'align_center')
        self.txt_receipt.insert(tk.END, "Thalamuthu Nagar Main Road,\n", 'align_center')
        self.txt_receipt.insert(tk.END, "Koilpillaivilai, Tuticorin - 628002\n", 'align_center')
        self.txt_receipt.insert(tk.END, "9942380164\n", 'align_center')
        self.txt_receipt.insert(tk.END, "\n", 'align_center')

        bill_number = '0123456'
        space_length = 31
        self.txt_receipt.insert(tk.END, f" Bill No: {bill_number}" + " " * space_length + f"Date: {date.today()}",
                                'align_left')
        # self.txt_Receipt.insert(tk.END, f"Date: {date.today()}\n", 'align_right')

        self.txt_receipt.insert(tk.END, f"\n{'- ' * 39}\n", 'align_left')
        self.txt_receipt.insert(tk.END, f" {'Item':<40}{'Qty':>5}{'Price':>10}{'Amount  ':>12}\n", 'align_right')
        self.txt_receipt.insert(tk.END, f"{'- ' * 39}\n", 'align_left')
        self.txt_receipt.insert(tk.END, f" {'Item No 1':<40}{'   10'}{'     10.00'}{'100.00  ':>12}\n", 'align_left')
        self.txt_receipt.insert(tk.END, f" {'Item No 2 Type 2       '}{'    1'}{'    100.00'}{'15000.00  ':>12}\n",
                                'align_left')

        self.txt_receipt.insert(tk.END, "\n", 'align_center')
        self.txt_receipt.insert(tk.END, f"{'- ' * 39}\n", 'align_left')
        self.txt_receipt.insert(tk.END, f" {'SubTotal':<35}{'10':>8}{'15000.00':>24}\n")
        self.txt_receipt.insert(tk.END, f"{'- ' * 39}\n", 'align_left')
        self.txt_receipt.insert(tk.END, f" {'Discount':<35}{'15000.00':>24}\n", 'align_right')

        self.txt_receipt.insert(tk.END, "\n", 'align_center')
        self.txt_receipt.insert(tk.END, f"{'- ' * 39}\n", 'align_left')
        self.txt_receipt.insert(tk.END, f" {'Total':<35}{'15000.00':>24}\n")
        self.txt_receipt.insert(tk.END, f"{'- ' * 39}\n", 'align_left')

        self.txt_receipt.insert(tk.END, "\n", 'align_center')
        self.txt_receipt.insert(tk.END, "\n", 'align_center')
        self.txt_receipt.insert(tk.END, "Thank You", 'align_center')

    def calculate_total_amount(self):
        total_amount = 0
        for child in self.sales_tree.get_children():
            total_amount += float(self.sales_tree.item(child)["values"][5])

        self.total_amount.set(format_currency(total_amount, 'INR', locale='en_IN'))

    def calculate_bill_amount(self):
        self.calculate_total_amount()

        total_amount = self.total_amount.get()[1:].replace(',', '')

        try:
            discount = self.discount.get()
        except TclError:
            discount = 0

        self.total_amount.set(format_currency(float(total_amount) - float(discount), 'INR', locale='en_IN'))
        self.bill_amount.set(format_currency(float(total_amount) - float(discount), 'INR', locale='en_IN'))

    def reload_bills(self):
        self.tree.delete(*self.tree.get_children())

        rows = Billing.get_all_bills()
        row_num = 0
        for row in rows:
            row_num += 1
            rw = (row.bill_number, datetime.strftime(row.bill_date, '%d-%b-%Y %I:%M:%S %p'),
                  round(row.amount, 2), round(row.discount, 2),
                  round(row.bill_amount, 2))

            if row_num % 2 == 0:
                self.tree.insert("", tk.END, values=rw, tags=('evenrow', row.bill_number))
            else:
                self.tree.insert("", tk.END, values=rw, tags=('oddrow', row.bill_number))

    def on_tree_select(self, event):
        self.selected = event.widget.selection()

        # for multi-select
        # for idx in self.selected:
        #     product = self.tree.item(idx)['values']

        bill = self.tree.item(self.selected)['values']

        if bill:
            self.bill_no.set(bill[0])
            self.bill_date.set(bill[1])
            self.total_amount.set(format_currency(float(bill[2]), 'INR', locale='en_IN'))
            self.discount.set(bill[3])
            self.bill_amount.set(format_currency(float(bill[4]), 'INR', locale='en_IN'))

            self.sales_tree.delete(*self.sales_tree.get_children())
            sales_counter = 0
            sales = Sales.get_sales(bill_number=self.bill_no.get())
            for sale in sales:
                product = Product.get_product(sale.product_id)

                sales_counter += 1
                if product:
                    product_short = f"{product.product_name} {product.product_type} {product.product_size}"

                    row = (sales_counter, sale.product_id, product_short, round(product.selling_price, 2),
                           sale.quantity, round(float(sale.amount), 2))
                else:
                    row = (sales_counter, '-', '-', '-', sale.quantity, round(float(sale.amount), 2))

                self.sales_tree.insert("", tk.END, values=row)


class SalesReport(MainForm):
    def __init__(self):
        super().__init__()

        # Set text variables
        # self.product_id = tk.StringVar()
        # self.product_name = tk.StringVar()
        # self.product_name = tk.StringVar()
        # self.product_type = tk.StringVar()
        # self.product_size = tk.StringVar()
        # self.selling_price = tk.DoubleVar()
        # self.actual_price = tk.DoubleVar()
        # self.quantity = tk.IntVar()

        self.search_product_id = tk.StringVar()

        self.filter_ety_product_name = None
        self.filter_ety_product_type = None

        self.ety_search_product_id = None

        # local variables
        self.tree = None
        self.selected = list()
        self.product_name_list = list()
        self.product_type_list = list()

        self.load_view_report_form()

    def load_view_report_form(self):
        self.update_username()

        products = Product.get_product_name_list()
        for product in products:
            self.product_name_list.append(product.product_name)

        products = Product.get_product_type_list()
        for product in products:
            self.product_type_list.append(product.product_type)

        # ********** Sub Containers *********
        left_container = tk.Frame(self.content_container, bd=5, padx=5, pady=5, relief=tk.RIDGE, bg='#62b6e2')
        left_container.pack(fill='both', expand=True, side=tk.LEFT)

        # bill_container = tk.Frame(self.content_container, bd=5, padx=10, pady=10, relief=tk.RIDGE,
        #                           bg='#62b6e2')
        # bill_container.pack(fill='both', expand=True, side=tk.RIGHT)

        left_button_container = tk.Frame(left_container, relief=tk.RIDGE, bg='#62b6e2')
        left_button_container.pack(fill='both', expand=True, side=tk.TOP)

        search_container = tk.Frame(left_button_container, relief=tk.RIDGE, bg='#62b6e2')
        search_container.pack(fill='x', expand=True, side=tk.LEFT)

        filter_container = tk.Frame(left_button_container, relief=tk.RIDGE, bg='#62b6e2')
        filter_container.pack(fill='x', expand=True, side=tk.LEFT)

        # ********** left_search_container elements *********
        search_lbl_product_id = tk.Label(search_container, text="ID: ", bg='#62b6e2')
        search_lbl_product_id.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        self.ety_search_product_id = tk.Entry(search_container, width=10, textvariable=self.search_product_id)
        self.ety_search_product_id.grid(row=1, column=0, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_search_product_id.bind('<Return>', lambda event: self.search_report(event))

        btn_search = tk.Button(search_container, text="Search", command=self.search_report)
        btn_search.grid(row=1, column=1, sticky="sw", padx=2, pady=1)

        filter_lbl_product_name = tk.Label(filter_container, text="Name: ", bg='#62b6e2')
        filter_lbl_product_name.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        self.filter_ety_product_name = AutocompleteEntry(filter_container, completevalues=self.product_name_list,
                                                         state='disabled')
        self.filter_ety_product_name.grid(row=1, column=0, sticky="nw", padx=5, pady=5, ipady=6)
        self.filter_ety_product_name.bind("<Return>", lambda event: self.filter_report(event))

        # filter_product_name = tk.Entry(filter_container, width=20, textvariable=self.filter_product_name)
        # filter_product_name.grid(row=1, column=0, sticky="nw", padx=5, pady=5, ipady=6)

        filter_lbl_product_type = tk.Label(filter_container, text="Type: ", bg='#62b6e2')
        filter_lbl_product_type.grid(row=0, column=1, sticky="nw", padx=5, pady=5)
        self.filter_ety_product_type = AutocompleteEntry(filter_container, completevalues=self.product_type_list,
                                                         state='disabled')
        self.filter_ety_product_type.grid(row=1, column=1, sticky="nw", padx=5, pady=5, ipady=6)
        self.filter_ety_product_type.grid(row=1, column=1, sticky="nw", padx=5, pady=5, ipady=6)
        self.filter_ety_product_type.bind("<Return>", lambda event: self.filter_report(event))

        # filter_product_type = tk.Entry(filter_container, width=25, textvariable=self.filter_product_type)
        # filter_product_type.grid(row=1, column=1, sticky="nw", padx=5, pady=5, ipady=6)

        btn_filter = tk.Button(filter_container, text="Apply Filter", command=self.filter_report, state='disabled')
        btn_filter.grid(row=1, column=2, sticky="sw", padx=2, pady=1)

        btn_clear_filter = tk.Button(filter_container, text="Clear Filter", command=self.reload_report)
        btn_clear_filter.grid(row=1, column=3, sticky="sw", padx=2, pady=1)

        btn_export = tk.Button(filter_container, text="Export to Excel", command=self.export_data)
        btn_export.grid(row=1, column=4, sticky="se", padx=15, pady=1)

        # ********** left_container *********
        tree_container = tk.Frame(left_container, pady=3, bg='#62b6e2')
        tree_container.pack(fill='both', expand=True, side=tk.TOP)

        header = ('#', 'date', 'product_id', 'product_name', 'product_type', 'product_size',
                  'selling_price', 'actual_price', 'quantity', 'total_amount', 'dummy')
        self.tree = ttk.Treeview(tree_container, columns=header, show="headings", height=15, selectmode="browse")
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Calibri', 12))
        style.configure("Treeview", font=('Calibri', 12), rowheight=25)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=tree_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=tree_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=tree_container)

        tree_container.grid_columnconfigure(0, weight=1)
        tree_container.grid_rowconfigure(0, weight=1)

        self.tree.heading("0", text="#")
        self.tree.heading("1", text="DATE")
        self.tree.heading("2", text="ID")
        self.tree.heading("3", text="PRODUCT_NAME")
        self.tree.heading("4", text="PRODUCT_TYPE")
        self.tree.heading("5", text="SIZE")
        self.tree.heading("6", text="SELL_PRICE")
        self.tree.heading("7", text="ACTUAL_PRICE")
        self.tree.heading("8", text="QTY")
        self.tree.heading("9", text="TOTAL_AMOUNT")

        self.tree.column(0, anchor='center', width="50")
        self.tree.column(1, anchor=tk.W, width="100")
        self.tree.column(2, anchor='center', width="50")
        self.tree.column(3, anchor=tk.W, width="150")
        self.tree.column(4, anchor=tk.W, width="200")
        self.tree.column(5, anchor='center', width="100")
        self.tree.column(6, anchor=tk.E, width="120")
        self.tree.column(7, anchor=tk.E, width="120")
        self.tree.column(8, anchor='center', width="80")
        self.tree.column(9, anchor=tk.E, width="120")
        self.tree.column(10, anchor='center', width="5")

        self.reload_report()

        btn_close = tk.Button(self.footer_container, text="Close", width='20', command=self.window.destroy)
        btn_close.pack(padx=5, pady=5)

        self.tree.tag_configure("evenrow", background='#fbefcc')
        self.tree.tag_configure("oddrow", background='white', foreground='black')
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

    def filter_report(self, event=None):
        product_name = self.filter_ety_product_name.get().strip()
        product_type = self.filter_ety_product_type.get().strip()

        rows = Stock.search_stock(product_name=product_name, product_type=product_type)
        self.tree.delete(*self.tree.get_children())

        if len(rows):
            sl_no = 0
            for row in rows:
                product = row.Product
                stock = row.Stock

                sl_no = sl_no + 1
                quantity = "-"
                if stock:
                    quantity = stock.quantity

                rw = (sl_no, product.product_id, product.product_name, product.product_type, product.product_size,
                      round(product.selling_price, 2), round(product.actual_price, 2), quantity)

                if sl_no % 2 == 0:
                    self.tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_id))
                else:
                    self.tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_id))
        else:
            pass

    def export_data(self):
        rows = self.tree.get_children()
        my_dict = defaultdict(list)
        for row in rows:
            my_dict["SL_NO"].append(self.tree.item(row)["values"][0])
            my_dict["DATE"].append(self.tree.item(row)["values"][1])
            my_dict["P_ID"].append(self.tree.item(row)["values"][2])
            my_dict["PRODUCT_NAME"].append(self.tree.item(row)["values"][3])
            my_dict["PRODUCT_TYPE"].append(self.tree.item(row)["values"][4])
            my_dict["SIZE"].append(self.tree.item(row)["values"][5])
            my_dict["SELL_PRICE"].append(self.tree.item(row)["values"][6])
            my_dict["ACTUAL_PRICE"].append(self.tree.item(row)["values"][7])
            my_dict["QUANTITY"].append(self.tree.item(row)["values"][8])
            my_dict["TOTAL_AMOUNT"].append(self.tree.item(row)["values"][9])

        my_dict = pd.DataFrame.from_dict(my_dict)
        try:
            my_dict.to_excel('SalesReport.xlsx', engine='xlsxwriter', index=False)
        except:
            print("Close the file than retry")

    def reload_report(self):
        self.filter_ety_product_name.delete(0, tk.END)
        self.filter_ety_product_type.delete(0, tk.END)

        self.tree.delete(*self.tree.get_children())

        sales = Sales.sales_report_daily()
        sl_no = 0
        for sale in sales:
            sl_no += 1
            product = Product.get_product(sale.product_id)
            rw = (sl_no, sale.sales_date, product.product_id, product.product_name,
                  product.product_type, product.product_size,
                  round(product.selling_price, 2), round(product.actual_price, 2),
                  sale.quantity, round(product.selling_price * sale.quantity, 2))

            if sl_no % 2 == 0:
                self.tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_id))
            else:
                self.tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_id))

    def search_report(self, event=None):
        product_id = self.search_product_id.get().strip()

        row = Stock.search_stock(product_id=product_id)
        if len(row):
            self.tree.selection_set(self.tree.tag_has(str(product_id)))
            self.tree.focus_set()
            self.tree.focus(self.selected)
        else:
            print('No items matched!')

    def on_tree_select(self, event):
        self.selected = event.widget.selection()
