"""
Simple Chat Application - Backend Manager
Handles message storage, retrieval, and file operations
"""

import json
from datetime import datetime
from typing import Dict, List


class ChatManager:
    def __init__(self, filename: str = "chat_data.json"):
        self.filename = filename
        self.messages: Dict[str, List[Dict]] = {}
        self.load_chat()
    
    def add_message(self, user: str, message: str, reply_to: Dict = None) -> bool:
        """Add a message to the chat"""
        if not user.strip() or not message.strip():
            return False
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if user not in self.messages:
            self.messages[user] = []
        
        msg_data = {
            "message": message,
            "timestamp": timestamp
        }
        
        if reply_to:
            msg_data["reply_to"] = reply_to
        
        self.messages[user].append(msg_data)
        
        self.save_chat()
        return True
    
    def get_recent_messages(self, limit: int = 50, user_filter: str = None, current_user: str = None) -> List[Dict]:
        """Get recent messages - if user_filter is set, get conversation between current_user and user_filter"""
        all_messages = []
        
        for user, user_messages in self.messages.items():
            for idx, msg_data in enumerate(user_messages):
                msg = {
                    "user": user,
                    "message": msg_data["message"],
                    "timestamp": msg_data["timestamp"],
                    "id": f"{user}_{idx}"
                }
                
                if "reply_to" in msg_data:
                    msg["reply_to"] = msg_data["reply_to"]
                
                all_messages.append(msg)
        
        # Sort by timestamp
        all_messages.sort(key=lambda x: x["timestamp"])
        
        # Filter for conversation between two users
        if user_filter and current_user:
            all_messages = [
                msg for msg in all_messages 
                if (msg["user"] == user_filter or msg["user"] == current_user)
            ]
        
        return all_messages[-limit:]
    
    def get_all_users(self, exclude_user: str = None) -> List[str]:
        """Get list of all users who have sent messages, excluding specified user"""
        users = list(self.messages.keys())
        if exclude_user and exclude_user in users:
            users.remove(exclude_user)
        return users
    
    def get_conversation_last_message(self, user1: str, user2: str) -> Dict:
        """Get the last message in a conversation between two users"""
        all_messages = []
        
        for user in [user1, user2]:
            if user in self.messages:
                for msg_data in self.messages[user]:
                    all_messages.append({
                        "user": user,
                        "message": msg_data["message"],
                        "timestamp": msg_data["timestamp"]
                    })
        
        if not all_messages:
            return None
        
        all_messages.sort(key=lambda x: x["timestamp"])
        return all_messages[-1]
    
    def save_chat(self) -> bool:
        """Save chat data to file"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving chat: {e}")
            return False
    
    def load_chat(self) -> bool:
        """Load chat data from file"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.messages = json.load(f)
            return True
        except FileNotFoundError:
            self.messages = {}
            return True
        except Exception as e:
            print(f"Error loading chat: {e}")
            self.messages = {}
            return False
    
    def clear_chat(self) -> bool:
        """Clear all messages"""
        self.messages = {}
        return self.save_chat()
