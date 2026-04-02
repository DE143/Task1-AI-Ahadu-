import json
from datetime import datetime
from typing import List, Dict

class ExpenseManager:
    def __init__(self, data_file='expense_data.json'):
        self.data_file = data_file
        self.transactions = []
        self.load_data()
    
    def load_data(self):
        """Load transactions from file"""
        try:
            with open(self.data_file, 'r') as f:
                self.transactions = json.load(f)
        except FileNotFoundError:
            self.transactions = []
    
    def save_data(self):
        """Save transactions to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.transactions, f, indent=2)
    
    def add_transaction(self, amount: float, category: str, transaction_type: str, date: str = None):
        """Add income or expense transaction"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        transaction = {
            'amount': amount,
            'category': category,
            'type': transaction_type,
            'date': date
        }
        self.transactions.append(transaction)
        self.save_data()
        return transaction
    
    def calculate_balance(self) -> float:
        """Calculate total balance (income - expenses)"""
        balance = 0
        for transaction in self.transactions:
            if transaction['type'] == 'income':
                balance += transaction['amount']
            else:
                balance -= transaction['amount']
        return balance
    
    def get_total_income(self) -> float:
        """Calculate total income"""
        return sum(t['amount'] for t in self.transactions if t['type'] == 'income')
    
    def get_total_expenses(self) -> float:
        """Calculate total expenses"""
        return sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
    
    def get_category_totals(self) -> Dict[str, float]:
        """Get spending by category"""
        category_totals = {}
        for transaction in self.transactions:
            if transaction['type'] == 'expense':
                category = transaction['category']
                category_totals[category] = category_totals.get(category, 0) + transaction['amount']
        return category_totals
    
    def get_all_transactions(self) -> List[Dict]:
        """Get all transactions sorted by date (newest first)"""
        return sorted(self.transactions, key=lambda x: x['date'], reverse=True)
