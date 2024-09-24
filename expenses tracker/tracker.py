import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json
import matplotlib.colors as mcolors
import numpy as np

class ExpenseTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Tracker")
        self.master.configure(bg='#1E1E1E')
        self.master.geometry("1400x900")

        self.df = self.load_data()
        self.savings = self.calculate_savings()
        self.cash_savings = self.df[self.df['Type'] == 'Cash Savings']['Amount'].sum()
        self.crypto = self.df[self.df['Type'] == 'Crypto']['Amount'].sum()
        self.other = self.df[self.df['Type'] == 'Other']['Amount'].sum()

        self.create_widgets()
        self.update_charts()
        self.update_entry_list()

    def create_widgets(self):
        left_frame = tk.Frame(self.master, bg='#1E1E1E')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground='#2E2E2E', background='#2E2E2E', foreground='white')
        style.configure('Treeview', background='#2E2E2E', fieldbackground='#2E2E2E', foreground='white')
        style.configure('Treeview.Heading', background='#3E3E3E', foreground='white')

        tk.Label(left_frame, text="Type:", bg='#1E1E1E', fg='white', font=('Arial', 12)).grid(row=0, column=0, sticky='w', pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(left_frame, textvariable=self.type_var, values=["Expense", "Income", "Cash Savings", "Crypto", "Other"], font=('Arial', 12), width=30)
        self.type_combo.grid(row=0, column=1, sticky='ew', pady=5)

        tk.Label(left_frame, text="Category:", bg='#1E1E1E', fg='white', font=('Arial', 12)).grid(row=1, column=0, sticky='w', pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(left_frame, textvariable=self.category_var, font=('Arial', 12), width=30)
        self.category_combo.grid(row=1, column=1, sticky='ew', pady=5)

        tk.Label(left_frame, text="Subcategory:", bg='#1E1E1E', fg='white', font=('Arial', 12)).grid(row=2, column=0, sticky='w', pady=5)
        self.subcategory_var = tk.StringVar()
        self.subcategory_combo = ttk.Combobox(left_frame, textvariable=self.subcategory_var, font=('Arial', 12), width=30)
        self.subcategory_combo.grid(row=2, column=1, sticky='ew', pady=5)

        self.type_combo.bind("<<ComboboxSelected>>", self.update_categories)
        self.category_combo.bind("<<ComboboxSelected>>", self.update_subcategories)

        tk.Label(left_frame, text="Amount:", bg='#1E1E1E', fg='white', font=('Arial', 12)).grid(row=3, column=0, sticky='w', pady=5)
        self.amount_entry = tk.Entry(left_frame, bg='#2E2E2E', fg='white', font=('Arial', 12))
        self.amount_entry.grid(row=3, column=1, sticky='ew', pady=5)

        tk.Button(left_frame, text="➕ Add Entry", command=self.add_entry, font=('Arial', 14), bg='#3E3E3E', fg='white', height=2).grid(row=4, column=0, columnspan=2, sticky='ew', pady=10)

        self.entry_list = ttk.Treeview(left_frame, columns=('DateTime', 'Type', 'Category', 'Subcategory', 'Amount'), show='headings', height=30)
        self.entry_list.heading('DateTime', text='Date & Time')
        self.entry_list.heading('Type', text='Type')
        self.entry_list.heading('Category', text='Category')
        self.entry_list.heading('Subcategory', text='Subcategory')
        self.entry_list.heading('Amount', text='Amount')
        self.entry_list.grid(row=5, column=0, columnspan=2, sticky='nsew', pady=10)

        left_frame.grid_columnconfigure(1, weight=1)
        left_frame.grid_rowconfigure(5, weight=1)

        tk.Button(left_frame, text="🗑️ Remove Selected Entry", command=self.remove_entry, font=('Arial', 14), bg='#3E3E3E', fg='white', height=2).grid(row=6, column=0, columnspan=2, sticky='ew', pady=10)

        right_frame = tk.Frame(self.master, bg='#1E1E1E')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.fig, axes = plt.subplots(2, 2, figsize=(12, 12))
        self.ax1, self.ax2, self.ax3, self.ax4 = axes.flatten()
        self.fig.patch.set_facecolor('#1E1E1E')
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.canvas.mpl_connect('motion_notify_event', self.hover)

    def update_categories(self, event):
        entry_type = self.type_var.get()
        if entry_type == "Expense":
            categories = ["Food", "Transportation", "Housing", "Entertainment", "Other"]
        elif entry_type == "Income":
            categories = ["Salary", "Investment", "Gift", "Other"]
        else:
            categories = ["N/A"]
        self.category_combo['values'] = categories
        self.category_var.set('')
        self.subcategory_combo['values'] = []
        self.subcategory_var.set('')

    def update_subcategories(self, event):
        category = self.category_var.get()
        if self.type_var.get() == "Expense":
            subcategories = {
                "Food": ["Groceries", "Dining Out", "Snacks"],
                "Transportation": ["Public Transit", "Fuel", "Car Maintenance"],
                "Housing": ["Rent", "Utilities", "Maintenance"],
                "Entertainment": ["Movies", "Games", "Hobbies"],
                "Other": ["Clothing", "Healthcare", "Miscellaneous"]
            }
        elif self.type_var.get() == "Income":
            subcategories = {
                "Salary": ["Regular", "Bonus", "Overtime"],
                "Investment": ["Stocks", "Bonds", "Real Estate"],
                "Gift": ["Birthday", "Holiday", "Other"],
                "Other": ["Refund", "Miscellaneous"]
            }
        else:
            subcategories = {"N/A": ["N/A"]}
        self.subcategory_combo['values'] = subcategories.get(category, [])
        self.subcategory_var.set('')

    def add_entry(self):
        entry_type = self.type_var.get()
        category = self.category_var.get()
        subcategory = self.subcategory_var.get()
        amount = float(self.amount_entry.get())
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_entry = pd.DataFrame({'DateTime': [date_time], 'Type': [entry_type], 'Category': [category], 'Subcategory': [subcategory], 'Amount': [amount]})
        self.df = pd.concat([self.df, new_entry], ignore_index=True)

        if entry_type == "Income":
            self.savings += amount
        elif entry_type == "Expense":
            self.savings -= amount
        elif entry_type == "Cash Savings":
            self.cash_savings += amount
        elif entry_type == "Crypto":
            self.crypto += amount
        elif entry_type == "Other":
            self.other += amount

        self.update_entry_list()
        self.update_charts()
        self.save_data()

    def remove_entry(self):
        selected_item = self.entry_list.selection()[0]
        index = self.entry_list.index(selected_item)
        
        removed_entry = self.df.iloc[index]
        if removed_entry['Type'] == "Income":
            self.savings -= removed_entry['Amount']
        elif removed_entry['Type'] == "Expense":
            self.savings += removed_entry['Amount']
        elif removed_entry['Type'] == "Cash Savings":
            self.cash_savings -= removed_entry['Amount']
        elif removed_entry['Type'] == "Crypto":
            self.crypto -= removed_entry['Amount']
        elif removed_entry['Type'] == "Other":
            self.other -= removed_entry['Amount']

        self.df = self.df.drop(self.df.index[index])
        self.update_entry_list()
        self.update_charts()
        self.save_data()

    def update_entry_list(self):
        self.entry_list.delete(*self.entry_list.get_children())
        for index, row in self.df.iterrows():
            self.entry_list.insert('', 'end', values=(row['DateTime'], row['Type'], row['Category'], row['Subcategory'], row['Amount']))

    def update_charts(self):
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.clear()
            ax.set_facecolor('#1E1E1E')

        expenses = self.df[self.df['Type'] == 'Expense']
        income = self.df[self.df['Type'] == 'Income']

        def create_color_map(data):
            categories = data['Category'].unique()
            color_map = {}
            for i, category in enumerate(categories):
                base_color = plt.cm.Set3(i / len(categories))
                subcategories = data[data['Category'] == category]['Subcategory'].unique()
                for j, subcategory in enumerate(subcategories):
                    shade = mcolors.rgb_to_hsv(base_color[:3])
                    shade[2] = 0.5 + (j / len(subcategories)) * 0.5
                    color_map[(category, subcategory)] = mcolors.hsv_to_rgb(shade)
            return color_map

        if not expenses.empty:
            expense_color_map = create_color_map(expenses)
            expense_colors = [expense_color_map[(row['Category'], row['Subcategory'])] for _, row in expenses.iterrows()]
            self.expense_pie = self.ax1.pie(expenses['Amount'], labels=expenses['Subcategory'], colors=expense_colors, autopct='%1.1f%%', startangle=90)
            self.ax1.set_title('Expenses by Subcategory', color='white')

        if not income.empty:
            income_color_map = create_color_map(income)
            income_colors = [income_color_map[(row['Category'], row['Subcategory'])] for _, row in income.iterrows()]
            self.income_pie = self.ax2.pie(income['Amount'], labels=income['Subcategory'], colors=income_colors, autopct='%1.1f%%', startangle=90)
            self.ax2.set_title('Income by Subcategory', color='white')

        savings_data = pd.DataFrame({
            'Category': ['Savings', 'Cash Savings', 'Crypto', 'Other'],
            'Amount': [self.savings, self.cash_savings, self.crypto, self.other]
        })
        colors = plt.cm.Set3(np.linspace(0, 1, len(savings_data)))

        if savings_data['Amount'].sum() > 0:
            self.ax3.pie(savings_data['Amount'], labels=savings_data['Category'], colors=colors, 
                         autopct=lambda pct: f'{pct:.1f}%\n(${savings_data["Amount"][savings_data.index[int(pct/100.*len(savings_data))]]:,.2f})')
        else:
            self.ax3.text(0.5, 0.5, 'No savings data', ha='center', va='center', color='white')

        self.ax3.set_title('Savings Distribution', color='white')

        if not self.df.empty:
            self.df['Date'] = pd.to_datetime(self.df['DateTime']).dt.date
            cashflow = self.df.groupby('Date').apply(lambda x: x[x['Type'] == 'Income']['Amount'].sum() - x[x['Type'] == 'Expense']['Amount'].sum()).cumsum().reset_index()
            cashflow.columns = ['Date', 'Cumulative']
            self.ax4.plot(cashflow['Date'], cashflow['Cumulative'], color='white')
            self.ax4.set_title('Cashflow', color='white')
            self.ax4.tick_params(axis='x', rotation=45, colors='white')
            self.ax4.tick_params(axis='y', colors='white')

        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            for text in ax.texts:
                text.set_color('white')

        self.fig.tight_layout()
        self.canvas.draw()

    def hover(self, event):
        for ax in [self.ax1, self.ax2, self.ax3]:
            if ax.contains(event)[0]:
                for wedge in ax.patches:
                    wedge.set_edgecolor('white')
                    wedge.set_linewidth(1)

                clicked_wedge = None
                for wedge in ax.patches:
                    cont, _ = wedge.contains(event)
                    if cont:
                        clicked_wedge = wedge
                        break

                if clicked_wedge:
                    clicked_wedge.set_edgecolor('yellow')
                    clicked_wedge.set_linewidth(3)
                    self.highlight_transactions(clicked_wedge)

                self.canvas.draw_idle()

    def highlight_transactions(self, wedge):
        category = wedge.get_label()
        for item in self.entry_list.get_children():
            values = self.entry_list.item(item)['values']
            if values[2] == category or values[3] == category:
                self.entry_list.item(item, tags=('highlight',))
            else:
                self.entry_list.item(item, tags=())
        self.entry_list.tag_configure('highlight', background='yellow', foreground='black')

    def load_data(self):
        try:
            with open('expense_data.json', 'r') as f:
                data = json.load(f)
            return pd.DataFrame(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return pd.DataFrame(columns=['DateTime', 'Type', 'Category', 'Subcategory', 'Amount'])

    def save_data(self):
        data = self.df.to_dict('records')
        with open('expense_data.json', 'w') as f:
            json.dump(data, f, indent=2)

    def calculate_savings(self):
        income = self.df[self.df['Type'] == 'Income']['Amount'].sum()
        expenses = self.df[self.df['Type'] == 'Expense']['Amount'].sum()
        return income - expenses

    def on_closing(self):
        self.save_data()
        self.master.destroy()

root = tk.Tk()
app = ExpenseTracker(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()
