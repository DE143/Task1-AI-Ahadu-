"""
User Authentication Manager
Handles user registration and login
"""

import json
import hashlib
from typing import Dict, Optional


class UserAuth:
    def __init__(self, filename: str = "users.json"):
        self.filename = filename
        self.users: Dict[str, str] = {}
        self.load_users()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, password: str) -> bool:
        """Register a new user"""
        if not username.strip() or not password.strip():
            return False
        
        if username in self.users:
            return False
        
        self.users[username] = self.hash_password(password)
        return self.save_users()
    
    def login_user(self, username: str, password: str) -> bool:
        """Verify user credentials"""
        if username not in self.users:
            return False
        
        return self.users[username] == self.hash_password(password)
    
    def user_exists(self, username: str) -> bool:
        """Check if username exists"""
        return username in self.users
    
    def save_users(self) -> bool:
        """Save users to file"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False
    
    def load_users(self) -> bool:
        """Load users from file"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
            return True
        except FileNotFoundError:
            self.users = {}
            return True
        except Exception as e:
            print(f"Error loading users: {e}")
            self.users = {}
            return False
