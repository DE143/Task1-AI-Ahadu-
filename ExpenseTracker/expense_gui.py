import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from expense_manager import ExpenseManager

class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker Pro")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        self.manager = ExpenseManager()
        
        # Color scheme
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'light': '#ecf0f1',
            'dark': '#34495e'
        }
        
        self.setup_ui()
        self.refresh_display()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="💰 Expense Tracker Pro", 
            font=('Arial', 20, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        )
        title_label.pack(pady=15)
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Input and Summary
        left_panel = tk.Frame(main_container, bg='white', relief='raised', bd=1)
        left_panel.pack(side='left', fill='both', padx=(0, 5), pady=0, expand=False)
        left_panel.config(width=350)
        
        # Summary Cards
        self.create_summary_cards(left_panel)
        
        # Input Form
        self.create_input_form(left_panel)
        
        # Right panel - Transactions and Chart
        right_panel = tk.Frame(main_container, bg='#f0f0f0')
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Chart
        self.create_chart_section(right_panel)
        
        # Transactions List
        self.create_transactions_list(right_panel)
    
    def create_summary_cards(self, parent):
        """Create summary cards for balance, income, and expenses"""
        summary_frame = tk.Frame(parent, bg='white')
        summary_frame.pack(fill='x', padx=15, pady=15)
        
        tk.Label(
            summary_frame,
            text="Financial Summary",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg=self.colors['dark']
        ).pack(anchor='w', pady=(0, 10))
        
        # Balance Card
        self.balance_card = self.create_card(
            summary_frame, "Total Balance", "$0.00", self.colors['secondary']
        )
        
        # Income Card
        self.income_card = self.create_card(
            summary_frame, "Total Income", "$0.00", self.colors['success']
        )
        
        # Expenses Card
        self.expense_card = self.create_card(
            summary_frame, "Total Expenses", "$0.00", self.colors['danger']
        )
    
    def create_card(self, parent, title, value, color):
        """Create a summary card"""
        card = tk.Frame(parent, bg=color, relief='flat', bd=0)
        card.pack(fill='x', pady=5)
        
        tk.Label(
            card,
            text=title,
            font=('Arial', 9),
            bg=color,
            fg='white'
        ).pack(anchor='w', padx=15, pady=(10, 0))
        
        value_label = tk.Label(
            card,
            text=value,
            font=('Arial', 18, 'bold'),
            bg=color,
            fg='white'
        )
        value_label.pack(anchor='w', padx=15, pady=(0, 10))
        
        return value_label
    
    def create_input_form(self, parent):
        """Create input form for adding transactions"""
        form_frame = tk.Frame(parent, bg='white')
        form_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            form_frame,
            text="Add Transaction",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg=self.colors['dark']
        ).pack(anchor='w', pady=(0, 15))
        
        # Transaction Type
        tk.Label(form_frame, text="Type:", font=('Arial', 9), bg='white').pack(anchor='w')
        self.type_var = tk.StringVar(value='expense')
        type_frame = tk.Frame(form_frame, bg='white')
        type_frame.pack(fill='x', pady=(5, 10))
        
        tk.Radiobutton(
            type_frame,
            text="Income",
            variable=self.type_var,
            value='income',
            font=('Arial', 9),
            bg='white',
            activebackground='white',
            selectcolor=self.colors['success']
        ).pack(side='left', padx=(0, 20))
        
        tk.Radiobutton(
            type_frame,
            text="Expense",
            variable=self.type_var,
            value='expense',
            font=('Arial', 9),
            bg='white',
            activebackground='white',
            selectcolor=self.colors['danger']
        ).pack(side='left')
        
        # Amount
        tk.Label(form_frame, text="Amount ($):", font=('Arial', 9), bg='white').pack(anchor='w', pady=(5, 0))
        self.amount_entry = tk.Entry(form_frame, font=('Arial', 11), relief='solid', bd=1)
        self.amount_entry.pack(fill='x', pady=5, ipady=5)
        
        # Category
        tk.Label(form_frame, text="Category:", font=('Arial', 9), bg='white').pack(anchor='w', pady=(5, 0))
        self.category_var = tk.StringVar()
        categories = ['Food', 'Transport', 'Shopping', 'Bills', 'Entertainment', 'Healthcare', 'Salary', 'Other']
        self.category_combo = ttk.Combobox(
            form_frame,
            textvariable=self.category_var,
            values=categories,
            font=('Arial', 10),
            state='readonly'
        )
        self.category_combo.pack(fill='x', pady=5, ipady=3)
        self.category_combo.set('Food')
        
        # Date
        tk.Label(form_frame, text="Date:", font=('Arial', 9), bg='white').pack(anchor='w', pady=(5, 0))
        self.date_entry = tk.Entry(form_frame, font=('Arial', 11), relief='solid', bd=1)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.pack(fill='x', pady=5, ipady=5)
        
        # Add Button
        add_btn = tk.Button(
            form_frame,
            text="Add Transaction",
            font=('Arial', 10, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.add_transaction
        )
        add_btn.pack(fill='x', pady=(15, 0), ipady=8)
    
    def create_chart_section(self, parent):
        """Create chart section for spending trends"""
        chart_frame = tk.Frame(parent, bg='white', relief='raised', bd=1)
        chart_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        tk.Label(
            chart_frame,
            text="Spending by Category",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg=self.colors['dark']
        ).pack(anchor='w', padx=15, pady=10)
        
        # Chart canvas
        self.chart_container = tk.Frame(chart_frame, bg='white')
        self.chart_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))
    
    def create_transactions_list(self, parent):
        """Create transactions list section"""
        list_frame = tk.Frame(parent, bg='white', relief='raised', bd=1)
        list_frame.pack(fill='both', expand=True)
        
        header_frame = tk.Frame(list_frame, bg='white')
        header_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            header_frame,
            text="Recent Transactions",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg=self.colors['dark']
        ).pack(side='left')
        
        # Clear button
        clear_btn = tk.Button(
            header_frame,
            text="Clear All",
            font=('Arial', 9),
            bg=self.colors['danger'],
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.clear_all_transactions
        )
        clear_btn.pack(side='right', padx=5)
        
        # Treeview
        tree_frame = tk.Frame(list_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Create treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=('Date', 'Type', 'Category', 'Amount'),
            show='headings',
            yscrollcommand=scrollbar.set,
            height=8
        )
        
        self.tree.heading('Date', text='Date')
        self.tree.heading('Type', text='Type')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Amount', text='Amount')
        
        self.tree.column('Date', width=100)
        self.tree.column('Type', width=80)
        self.tree.column('Category', width=100)
        self.tree.column('Amount', width=100)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Style for treeview
        style = ttk.Style()
        style.configure('Treeview', rowheight=30, font=('Arial', 9))
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
    
    def add_transaction(self):
        """Add a new transaction"""
        try:
            amount = float(self.amount_entry.get())
            category = self.category_var.get()
            transaction_type = self.type_var.get()
            date = self.date_entry.get()
            
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return
            
            if not category:
                messagebox.showerror("Error", "Please select a category")
                return
            
            self.manager.add_transaction(amount, category, transaction_type, date)
            
            # Clear inputs
            self.amount_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
            
            self.refresh_display()
            messagebox.showinfo("Success", "Transaction added successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    def refresh_display(self):
        """Refresh all display elements"""
        self.update_summary_cards()
        self.update_transactions_list()
        self.update_chart()
    
    def update_summary_cards(self):
        """Update summary card values"""
        balance = self.manager.calculate_balance()
        income = self.manager.get_total_income()
        expenses = self.manager.get_total_expenses()
        
        self.balance_card.config(text=f"${balance:,.2f}")
        self.income_card.config(text=f"${income:,.2f}")
        self.expense_card.config(text=f"${expenses:,.2f}")
    
    def update_transactions_list(self):
        """Update transactions list"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add transactions
        for transaction in self.manager.get_all_transactions():
            amount_str = f"${transaction['amount']:,.2f}"
            if transaction['type'] == 'expense':
                amount_str = f"-{amount_str}"
            else:
                amount_str = f"+{amount_str}"
            
            self.tree.insert('', 'end', values=(
                transaction['date'],
                transaction['type'].capitalize(),
                transaction['category'],
                amount_str
            ))
    
    def update_chart(self):
        """Update spending chart"""
        # Clear previous chart
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        
        category_totals = self.manager.get_category_totals()
        
        if not category_totals:
            tk.Label(
                self.chart_container,
                text="No expense data to display",
                font=('Arial', 10),
                bg='white',
                fg='gray'
            ).pack(expand=True)
            return
        
        # Create bar chart
        fig = Figure(figsize=(6, 3), dpi=100)
        ax = fig.add_subplot(111)
        
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())
        
        colors = ['#3498db', '#e74c3c', '#f39c12', '#27ae60', '#9b59b6', '#1abc9c', '#34495e', '#e67e22']
        bar_colors = colors[:len(categories)]
        
        ax.bar(categories, amounts, color=bar_colors, alpha=0.8)
        ax.set_ylabel('Amount ($)', fontsize=9)
        ax.set_title('Expenses by Category', fontsize=10, fontweight='bold')
        ax.tick_params(axis='both', labelsize=8)
        
        # Rotate x labels if needed
        if len(categories) > 4:
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        fig.tight_layout()
        
        # Embed chart
        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def clear_all_transactions(self):
        """Clear all transactions"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all transactions?"):
            self.manager.transactions = []
            self.manager.save_data()
            self.refresh_display()
            messagebox.showinfo("Success", "All transactions cleared!")

def main():
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
