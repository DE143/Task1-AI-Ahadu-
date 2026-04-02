"""
Simple Chat Application - Telegram Style GUI
Users list on left, chat conversations on right
"""

import tkinter as tk
from tkinter import messagebox
from chat_manager import ChatManager
from user_auth import UserAuth
from datetime import datetime


class TelegramChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat App - Login")
        self.root.geometry("400x500")
        self.root.minsize(400, 500)
        
        self.chat_manager = ChatManager()
        self.user_auth = UserAuth()
        self.current_user = None
        self.selected_user = None
        self.replying_to = None
        self.is_logged_in = False
        
        # Telegram color scheme
        self.bg_main = "#17212b"
        self.bg_chat = "#0e1621"
        self.bg_input = "#17212b"
        self.msg_out_bg = "#2b5278"
        self.msg_in_bg = "#182533"
        self.text_primary = "#ffffff"
        self.text_secondary = "#aaaaaa"
        self.accent_color = "#5288c1"
        self.reply_line = "#5288c1"
        self.selected_bg = "#2b5278"
        
        self.show_login_page()
    
    def show_login_page(self):
        """Show login/register page"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.configure(bg=self.bg_main)
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_main)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo/Title
        tk.Label(
            main_frame,
            text="💬",
            font=("Segoe UI", 80),
            bg=self.bg_main,
            fg=self.accent_color
        ).pack(pady=(60, 10))
        
        tk.Label(
            main_frame,
            text="Chat App",
            font=("Segoe UI", 28, "bold"),
            bg=self.bg_main,
            fg=self.text_primary
        ).pack(pady=(0, 10))
        
        tk.Label(
            main_frame,
            text="Connect with friends and family",
            font=("Segoe UI", 11),
            bg=self.bg_main,
            fg=self.text_secondary
        ).pack(pady=(0, 40))
        
        # Login form
        form_frame = tk.Frame(main_frame, bg=self.bg_main)
        form_frame.pack(padx=50, pady=20)
        
        # Username
        tk.Label(
            form_frame,
            text="Username",
            font=("Segoe UI", 10),
            bg=self.bg_main,
            fg=self.text_secondary,
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
        self.login_username_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 12),
            bg="#0d1117",
            fg=self.text_primary,
            relief=tk.FLAT,
            insertbackground=self.text_primary,
            width=30
        )
        self.login_username_entry.pack(ipady=10, pady=(0, 15))
        self.login_username_entry.focus()
        
        # Password
        tk.Label(
            form_frame,
            text="Password",
            font=("Segoe UI", 10),
            bg=self.bg_main,
            fg=self.text_secondary,
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
        self.login_password_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 12),
            bg="#0d1117",
            fg=self.text_primary,
            relief=tk.FLAT,
            insertbackground=self.text_primary,
            show="●",
            width=30
        )
        self.login_password_entry.pack(ipady=10, pady=(0, 25))
        self.login_password_entry.bind("<Return>", lambda e: self.handle_login())
        
        # Login button
        login_btn = tk.Button(
            form_frame,
            text="Log In",
            font=("Segoe UI", 12, "bold"),
            bg=self.accent_color,
            fg=self.text_primary,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.handle_login,
            width=28,
            pady=10
        )
        login_btn.pack(pady=(0, 15))
        
        # Divider
        tk.Label(
            form_frame,
            text="or",
            font=("Segoe UI", 10),
            bg=self.bg_main,
            fg=self.text_secondary
        ).pack(pady=10)
        
        # Register button
        register_btn = tk.Button(
            form_frame,
            text="Create New Account",
            font=("Segoe UI", 11),
            bg="#1a2633",
            fg=self.text_primary,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.show_register_page,
            width=28,
            pady=10
        )
        register_btn.pack(pady=(10, 0))
    
    def show_register_page(self):
        """Show registration page"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.configure(bg=self.bg_main)
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_main)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Back button
        back_btn = tk.Label(
            main_frame,
            text="← Back",
            font=("Segoe UI", 11),
            bg=self.bg_main,
            fg=self.accent_color,
            cursor="hand2"
        )
        back_btn.pack(anchor="w", padx=20, pady=20)
        back_btn.bind("<Button-1>", lambda e: self.show_login_page())
        
        # Title
        tk.Label(
            main_frame,
            text="Create Account",
            font=("Segoe UI", 24, "bold"),
            bg=self.bg_main,
            fg=self.text_primary
        ).pack(pady=(20, 10))
        
        tk.Label(
            main_frame,
            text="Sign up to start chatting",
            font=("Segoe UI", 11),
            bg=self.bg_main,
            fg=self.text_secondary
        ).pack(pady=(0, 30))
        
        # Register form
        form_frame = tk.Frame(main_frame, bg=self.bg_main)
        form_frame.pack(padx=50, pady=20)
        
        # Username
        tk.Label(
            form_frame,
            text="Choose a Username",
            font=("Segoe UI", 10),
            bg=self.bg_main,
            fg=self.text_secondary,
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
        self.register_username_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 12),
            bg="#0d1117",
            fg=self.text_primary,
            relief=tk.FLAT,
            insertbackground=self.text_primary,
            width=30
        )
        self.register_username_entry.pack(ipady=10, pady=(0, 15))
        self.register_username_entry.focus()
        
        # Password
        tk.Label(
            form_frame,
            text="Create a Password",
            font=("Segoe UI", 10),
            bg=self.bg_main,
            fg=self.text_secondary,
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
        self.register_password_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 12),
            bg="#0d1117",
            fg=self.text_primary,
            relief=tk.FLAT,
            insertbackground=self.text_primary,
            show="●",
            width=30
        )
        self.register_password_entry.pack(ipady=10, pady=(0, 15))
        
        # Confirm Password
        tk.Label(
            form_frame,
            text="Confirm Password",
            font=("Segoe UI", 10),
            bg=self.bg_main,
            fg=self.text_secondary,
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
        self.register_confirm_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 12),
            bg="#0d1117",
            fg=self.text_primary,
            relief=tk.FLAT,
            insertbackground=self.text_primary,
            show="●",
            width=30
        )
        self.register_confirm_entry.pack(ipady=10, pady=(0, 25))
        self.register_confirm_entry.bind("<Return>", lambda e: self.handle_register())
        
        # Register button
        register_btn = tk.Button(
            form_frame,
            text="Sign Up",
            font=("Segoe UI", 12, "bold"),
            bg=self.accent_color,
            fg=self.text_primary,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.handle_register,
            width=28,
            pady=10
        )
        register_btn.pack()
    
    def handle_login(self):
        """Handle login attempt"""
        username = self.login_username_entry.get().strip()
        password = self.login_password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Login Failed", "Please enter both username and password")
            return
        
        if self.user_auth.login_user(username, password):
            self.current_user = username
            self.is_logged_in = True
            self.start_chat_app()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            self.login_password_entry.delete(0, tk.END)
    
    def handle_register(self):
        """Handle registration attempt"""
        username = self.register_username_entry.get().strip()
        password = self.register_password_entry.get().strip()
        confirm = self.register_confirm_entry.get().strip()
        
        if not username or not password or not confirm:
            messagebox.showwarning("Registration Failed", "Please fill in all fields")
            return
        
        if len(username) < 3:
            messagebox.showwarning("Registration Failed", "Username must be at least 3 characters")
            return
        
        if len(password) < 4:
            messagebox.showwarning("Registration Failed", "Password must be at least 4 characters")
            return
        
        if password != confirm:
            messagebox.showwarning("Registration Failed", "Passwords do not match")
            return
        
        if self.user_auth.user_exists(username):
            messagebox.showwarning("Registration Failed", "Username already exists")
            return
        
        if self.user_auth.register_user(username, password):
            messagebox.showinfo("Success", "Account created successfully!\nYou can now log in.")
            self.show_login_page()
        else:
            messagebox.showerror("Registration Failed", "Failed to create account")
    
    def start_chat_app(self):
        """Start the main chat application"""
        self.root.title("Chat App")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Clear login page
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.setup_ui()
        self.auto_refresh()
    
    def setup_ui(self):
        """Setup Telegram-style UI"""
        self.root.configure(bg=self.bg_main)
        
        # Left sidebar - User list
        sidebar = tk.Frame(self.root, bg=self.bg_main, width=320)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Sidebar header
        sidebar_header = tk.Frame(sidebar, bg=self.bg_main, height=60)
        sidebar_header.pack(fill=tk.X)
        sidebar_header.pack_propagate(False)
        
        menu_btn = tk.Label(
            sidebar_header,
            text="☰",
            font=("Segoe UI", 20),
            bg=self.bg_main,
            fg=self.text_primary,
            cursor="hand2"
        )
        menu_btn.pack(side=tk.LEFT, padx=15, pady=15)
        menu_btn.bind("<Button-1>", lambda e: self.show_menu())
        
        # New chat button
        new_chat_btn = tk.Label(
            sidebar_header,
            text="✏️",
            font=("Segoe UI", 18),
            bg=self.bg_main,
            fg=self.text_primary,
            cursor="hand2"
        )
        new_chat_btn.pack(side=tk.RIGHT, padx=15, pady=15)
        new_chat_btn.bind("<Button-1>", lambda e: self.show_new_chat_dialog())
        
        search_frame = tk.Frame(sidebar_header, bg="#0d1117", height=36)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15), pady=12)
        
        tk.Label(
            search_frame,
            text="🔍 Search",
            font=("Segoe UI", 10),
            bg="#0d1117",
            fg=self.text_secondary
        ).pack(side=tk.LEFT, padx=10)
        
        # Scrollable user list
        list_container = tk.Frame(sidebar, bg=self.bg_main)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        list_scrollbar = tk.Scrollbar(list_container, bg=self.bg_main)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.user_list_canvas = tk.Canvas(
            list_container,
            bg=self.bg_main,
            highlightthickness=0,
            yscrollcommand=list_scrollbar.set
        )
        self.user_list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scrollbar.config(command=self.user_list_canvas.yview)
        
        self.user_list_frame = tk.Frame(self.user_list_canvas, bg=self.bg_main)
        self.user_list_window = self.user_list_canvas.create_window(
            (0, 0),
            window=self.user_list_frame,
            anchor="nw"
        )
        
        self.user_list_canvas.bind("<Configure>", lambda e: self.user_list_canvas.itemconfig(
            self.user_list_window, width=e.width
        ))
        self.user_list_frame.bind("<Configure>", lambda e: self.user_list_canvas.configure(
            scrollregion=self.user_list_canvas.bbox("all")
        ))
        
        # Right side - Main chat area
        self.main_area = tk.Frame(self.root, bg=self.bg_chat)
        self.main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Show welcome screen initially
        self.show_welcome_screen()
    
    def show_welcome_screen(self):
        """Show welcome screen when no user is selected"""
        for widget in self.main_area.winfo_children():
            widget.destroy()
        
        welcome = tk.Frame(self.main_area, bg=self.bg_chat)
        welcome.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            welcome,
            text="💬",
            font=("Segoe UI", 80),
            bg=self.bg_chat,
            fg=self.text_secondary
        ).pack(expand=True, pady=(0, 20))
        
        tk.Label(
            welcome,
            text="Select a user to start chatting",
            font=("Segoe UI", 16),
            bg=self.bg_chat,
            fg=self.text_secondary
        ).pack(expand=True)
        
        tk.Label(
            welcome,
            text="Click ✏️ in the top right to start a new chat",
            font=("Segoe UI", 11),
            bg=self.bg_chat,
            fg=self.text_secondary
        ).pack(expand=True, pady=(10, 0))
    
    def setup_chat_area(self, username):
        """Setup chat area for selected user"""
        for widget in self.main_area.winfo_children():
            widget.destroy()
        
        # Chat header
        chat_header = tk.Frame(self.main_area, bg=self.bg_main, height=60)
        chat_header.pack(fill=tk.X)
        chat_header.pack_propagate(False)
        
        header_content = tk.Frame(chat_header, bg=self.bg_main)
        header_content.pack(side=tk.LEFT, padx=20, pady=10)
        
        # User avatar
        avatar = tk.Label(
            header_content,
            text=username[0].upper(),
            font=("Segoe UI", 16, "bold"),
            bg=self.accent_color,
            fg=self.text_primary,
            width=2,
            height=1
        )
        avatar.pack(side=tk.LEFT, padx=(0, 12))
        
        user_info = tk.Frame(header_content, bg=self.bg_main)
        user_info.pack(side=tk.LEFT)
        
        tk.Label(
            user_info,
            text=username,
            font=("Segoe UI", 13, "bold"),
            bg=self.bg_main,
            fg=self.text_primary,
            anchor="w"
        ).pack(anchor="w")
        
        tk.Label(
            user_info,
            text="online",
            font=("Segoe UI", 9),
            bg=self.bg_main,
            fg=self.text_secondary,
            anchor="w"
        ).pack(anchor="w")
        
        # Header buttons
        header_btns = tk.Frame(chat_header, bg=self.bg_main)
        header_btns.pack(side=tk.RIGHT, padx=20)
        
        for icon in ["🔍", "⋮"]:
            btn = tk.Label(
                header_btns,
                text=icon,
                font=("Segoe UI", 16),
                bg=self.bg_main,
                fg=self.text_secondary,
                cursor="hand2",
                padx=10
            )
            btn.pack(side=tk.LEFT)
        
        # Messages area
        messages_container = tk.Frame(self.main_area, bg=self.bg_chat)
        messages_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(messages_container, bg=self.bg_chat)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.messages_canvas = tk.Canvas(
            messages_container,
            bg=self.bg_chat,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.messages_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.messages_canvas.yview)
        
        self.messages_frame = tk.Frame(self.messages_canvas, bg=self.bg_chat)
        self.messages_window = self.messages_canvas.create_window(
            (0, 0),
            window=self.messages_frame,
            anchor="nw"
        )
        
        self.messages_canvas.bind("<Configure>", self.on_canvas_configure)
        self.messages_frame.bind("<Configure>", self.on_frame_configure)
        self.messages_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # Reply bar
        self.reply_bar = tk.Frame(self.main_area, bg="#1a2633", height=50)
        
        # Bottom input area
        bottom_area = tk.Frame(self.main_area, bg=self.bg_input)
        bottom_area.pack(fill=tk.X, side=tk.BOTTOM)
        
        input_container = tk.Frame(bottom_area, bg=self.bg_input)
        input_container.pack(fill=tk.X, padx=15, pady=12)
        
        attach_btn = tk.Label(
            input_container,
            text="📎",
            font=("Segoe UI", 18),
            bg=self.bg_input,
            fg=self.text_secondary,
            cursor="hand2"
        )
        attach_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        input_frame = tk.Frame(input_container, bg="#0d1117")
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.message_entry = tk.Text(
            input_frame,
            font=("Segoe UI", 11),
            bg="#0d1117",
            fg=self.text_primary,
            relief=tk.FLAT,
            height=1,
            wrap=tk.WORD,
            insertbackground=self.text_primary,
            padx=12,
            pady=10
        )
        self.message_entry.pack(fill=tk.BOTH, expand=True)
        self.message_entry.bind("<Return>", self.on_enter_press)
        self.message_entry.bind("<KeyRelease>", self.update_send_button)
        
        self.send_btn = tk.Label(
            input_container,
            text="🎤",
            font=("Segoe UI", 20),
            bg=self.bg_input,
            fg=self.text_secondary,
            cursor="hand2"
        )
        self.send_btn.pack(side=tk.LEFT, padx=(10, 0))
        self.send_btn.bind("<Button-1>", lambda e: self.send_message())
        
        # Load messages for this user
        self.load_messages()
        self.scroll_to_bottom()
    
    def create_user_item(self, username, is_selected=False):
        """Create a user list item"""
        bg_color = self.selected_bg if is_selected else self.bg_main
        
        user_frame = tk.Frame(self.user_list_frame, bg=bg_color, cursor="hand2")
        user_frame.pack(fill=tk.X)
        
        content = tk.Frame(user_frame, bg=bg_color)
        content.pack(fill=tk.X, padx=15, pady=12)
        
        # Avatar
        avatar = tk.Label(
            content,
            text=username[0].upper(),
            font=("Segoe UI", 14, "bold"),
            bg=self.accent_color,
            fg=self.text_primary,
            width=3,
            height=1
        )
        avatar.pack(side=tk.LEFT, padx=(0, 12))
        
        # User info
        info_frame = tk.Frame(content, bg=bg_color)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Username
        name_label = tk.Label(
            info_frame,
            text=username,
            font=("Segoe UI", 11, "bold"),
            bg=bg_color,
            fg=self.text_primary,
            anchor="w"
        )
        name_label.pack(anchor="w", fill=tk.X)
        
        # Last message preview
        last_msg = self.chat_manager.get_conversation_last_message(self.current_user, username)
        if last_msg:
            sender_prefix = "You: " if last_msg["user"] == self.current_user else ""
            preview_text = sender_prefix + last_msg["message"][:30] + ("..." if len(last_msg["message"]) > 30 else "")
            msg_label = tk.Label(
                info_frame,
                text=preview_text,
                font=("Segoe UI", 9),
                bg=bg_color,
                fg=self.text_secondary,
                anchor="w"
            )
            msg_label.pack(anchor="w", fill=tk.X, pady=(2, 0))
        
        # Bind click event
        for widget in [user_frame, content, avatar, info_frame, name_label]:
            widget.bind("<Button-1>", lambda e, u=username: self.select_user(u))
        
        if last_msg:
            msg_label.bind("<Button-1>", lambda e, u=username: self.select_user(u))
    
    def select_user(self, username):
        """Select a user and show their chat"""
        self.selected_user = username
        self.load_user_list()
        self.setup_chat_area(username)
    
    def load_user_list(self):
        """Load and display user list"""
        for widget in self.user_list_frame.winfo_children():
            widget.destroy()
        
        # Get all users except current user
        users = self.chat_manager.get_all_users(exclude_user=self.current_user)
        
        # Get all users who have had conversations with current user
        conversation_users = set()
        all_messages = self.chat_manager.get_recent_messages(limit=1000)
        for msg in all_messages:
            if msg["user"] != self.current_user:
                conversation_users.add(msg["user"])
        
        # Combine and deduplicate
        all_chat_users = list(conversation_users)
        
        if not all_chat_users:
            tk.Label(
                self.user_list_frame,
                text="No conversations yet\n\nClick ✏️ to start\na new chat!",
                font=("Segoe UI", 10),
                bg=self.bg_main,
                fg=self.text_secondary,
                justify=tk.CENTER
            ).pack(pady=50)
        else:
            for user in all_chat_users:
                self.create_user_item(user, user == self.selected_user)
        
        self.user_list_frame.update_idletasks()
    
    def show_menu(self):
        """Show menu with logout option"""
        menu = tk.Menu(self.root, tearoff=0, bg=self.bg_main, fg=self.text_primary, 
                      activebackground=self.accent_color, activeforeground=self.text_primary,
                      font=("Segoe UI", 10))
        
        menu.add_command(label=f"👤 Logged in as: {self.current_user}", state="disabled")
        menu.add_separator()
        menu.add_command(label="⚙️ Settings", command=self.show_settings)
        menu.add_command(label="🗑️ Clear All Chats", command=self.clear_all_chats)
        menu.add_separator()
        menu.add_command(label="🚪 Logout", command=self.logout)
        
        # Get the position of the menu button
        try:
            x = self.root.winfo_x() + 20
            y = self.root.winfo_y() + 80
            menu.post(x, y)
        except:
            menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
    
    def show_settings(self):
        """Show settings dialog"""
        messagebox.showinfo("Settings", f"Logged in as: {self.current_user}\n\nMore settings coming soon!")
    
    def clear_all_chats(self):
        """Clear all chat messages"""
        result = messagebox.askyesno(
            "Clear All Chats",
            "Are you sure you want to delete all your messages?\n\nThis action cannot be undone."
        )
        
        if result:
            if self.chat_manager.clear_chat():
                self.selected_user = None
                self.load_user_list()
                self.show_welcome_screen()
                messagebox.showinfo("Success", "All chats have been cleared!")
    
    def logout(self):
        """Logout current user"""
        result = messagebox.askyesno(
            "Logout",
            f"Are you sure you want to logout?\n\nYou are currently logged in as: {self.current_user}"
        )
        
        if result:
            # Reset user state
            self.current_user = None
            self.selected_user = None
            self.replying_to = None
            self.is_logged_in = False
            
            # Stop auto-refresh
            if hasattr(self, 'refresh_job'):
                self.root.after_cancel(self.refresh_job)
            
            # Reset window size
            self.root.geometry("400x500")
            self.root.minsize(400, 500)
            self.root.title("Chat App - Login")
            
            # Show login page
            self.show_login_page()
    
    def show_new_chat_dialog(self):
        """Show dialog to start a new chat with someone"""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Chat")
        dialog.geometry("350x150")
        dialog.configure(bg=self.bg_main)
        dialog.transient(self.root)
        dialog.grab_set()
        
        x = (dialog.winfo_screenwidth() // 2) - (175)
        y = (dialog.winfo_screenheight() // 2) - (75)
        dialog.geometry(f"350x150+{x}+{y}")
        
        tk.Label(
            dialog,
            text="Who do you want to chat with?",
            font=("Segoe UI", 13, "bold"),
            bg=self.bg_main,
            fg=self.text_primary
        ).pack(pady=(20, 10))
        
        name_entry = tk.Entry(
            dialog,
            font=("Segoe UI", 12),
            bg="#0d1117",
            fg=self.text_primary,
            relief=tk.FLAT,
            insertbackground=self.text_primary
        )
        name_entry.pack(padx=30, pady=10, ipady=8, fill=tk.X)
        name_entry.focus()
        
        def start_chat():
            username = name_entry.get().strip()
            if username:
                if username == self.current_user:
                    messagebox.showwarning("Invalid", "You cannot chat with yourself!")
                    return
                dialog.destroy()
                self.select_user(username)
        
        btn = tk.Button(
            dialog,
            text="Start Chat",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_color,
            fg=self.text_primary,
            relief=tk.FLAT,
            cursor="hand2",
            command=start_chat,
            padx=20,
            pady=8
        )
        btn.pack(pady=10)
        
        name_entry.bind("<Return>", lambda e: start_chat())
    
    def update_send_button(self, event=None):
        """Update send button icon"""
        if hasattr(self, 'message_entry'):
            text = self.message_entry.get("1.0", "end-1c").strip()
            if text:
                self.send_btn.config(text="➤", fg=self.accent_color)
            else:
                self.send_btn.config(text="🎤", fg=self.text_secondary)
    
    def on_enter_press(self, event):
        """Handle Enter key"""
        if event.state & 0x1:
            return
        else:
            self.send_message()
            return "break"
    
    def on_canvas_configure(self, event):
        """Handle canvas resize"""
        self.messages_canvas.itemconfig(self.messages_window, width=event.width)
    
    def on_frame_configure(self, event):
        """Update scroll region"""
        self.messages_canvas.configure(scrollregion=self.messages_canvas.bbox("all"))
    
    def on_mousewheel(self, event):
        """Handle mouse wheel"""
        self.messages_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_message_bubble(self, parent, msg_data, is_own):
        """Create message bubble"""
        container = tk.Frame(parent, bg=self.bg_chat)
        container.pack(fill=tk.X, padx=10, pady=3)
        
        bubble_bg = self.msg_out_bg if is_own else self.msg_in_bg
        bubble = tk.Frame(container, bg=bubble_bg)
        
        if is_own:
            bubble.pack(side=tk.RIGHT, anchor="e", padx=(100, 5))
        else:
            bubble.pack(side=tk.LEFT, anchor="w", padx=(5, 100))
        
        # Reply indicator
        if "reply_to" in msg_data:
            reply_container = tk.Frame(bubble, bg=bubble_bg)
            reply_container.pack(fill=tk.X, padx=10, pady=(8, 0))
            
            reply_line = tk.Frame(reply_container, bg=self.reply_line, width=3)
            reply_line.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
            
            reply_content = tk.Frame(reply_container, bg=bubble_bg)
            reply_content.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            tk.Label(
                reply_content,
                text=msg_data['reply_to']['user'],
                font=("Segoe UI", 9, "bold"),
                bg=bubble_bg,
                fg=self.reply_line,
                anchor="w"
            ).pack(anchor="w")
            
            tk.Label(
                reply_content,
                text=msg_data['reply_to']['message'][:50] + ("..." if len(msg_data['reply_to']['message']) > 50 else ""),
                font=("Segoe UI", 9),
                bg=bubble_bg,
                fg=self.text_secondary,
                anchor="w",
                wraplength=350
            ).pack(anchor="w")
        
        # Message text
        msg_label = tk.Label(
            bubble,
            text=msg_data["message"],
            font=("Segoe UI", 11),
            bg=bubble_bg,
            fg=self.text_primary,
            anchor="w",
            justify=tk.LEFT,
            wraplength=400
        )
        msg_label.pack(anchor="w", padx=10, pady=(8 if "reply_to" not in msg_data else 3, 2))
        
        # Bottom info
        bottom = tk.Frame(bubble, bg=bubble_bg)
        bottom.pack(fill=tk.X, padx=10, pady=(0, 8))
        
        time_text = msg_data["timestamp"].split()[1][:5]
        
        time_label = tk.Label(
            bottom,
            text=time_text,
            font=("Segoe UI", 8),
            bg=bubble_bg,
            fg=self.text_secondary
        )
        time_label.pack(side=tk.LEFT)
        
        reply_btn = tk.Label(
            bottom,
            text="Reply",
            font=("Segoe UI", 8),
            bg=bubble_bg,
            fg=self.accent_color,
            cursor="hand2"
        )
        reply_btn.pack(side=tk.RIGHT, padx=(10, 0))
        reply_btn.bind("<Button-1>", lambda e: self.show_reply_bar(msg_data))
    
    def show_reply_bar(self, msg_data):
        """Show reply bar"""
        self.replying_to = msg_data
        
        for widget in self.reply_bar.winfo_children():
            widget.destroy()
        
        self.reply_bar.pack(fill=tk.X, before=self.main_area.winfo_children()[-1])
        
        container = tk.Frame(self.reply_bar, bg="#1a2633")
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)
        
        line = tk.Frame(container, bg=self.reply_line, width=3)
        line.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        content = tk.Frame(container, bg="#1a2633")
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            content,
            text=f"Reply to {msg_data['user']}",
            font=("Segoe UI", 9, "bold"),
            bg="#1a2633",
            fg=self.reply_line
        ).pack(anchor="w")
        
        tk.Label(
            content,
            text=msg_data['message'][:60] + ("..." if len(msg_data['message']) > 60 else ""),
            font=("Segoe UI", 9),
            bg="#1a2633",
            fg=self.text_secondary
        ).pack(anchor="w")
        
        close_btn = tk.Label(
            container,
            text="✕",
            font=("Segoe UI", 14),
            bg="#1a2633",
            fg=self.text_secondary,
            cursor="hand2"
        )
        close_btn.pack(side=tk.RIGHT, padx=(10, 0))
        close_btn.bind("<Button-1>", lambda e: self.cancel_reply())
        
        self.message_entry.focus()
    
    def cancel_reply(self):
        """Cancel reply"""
        self.replying_to = None
        self.reply_bar.pack_forget()
    
    def send_message(self):
        """Send message"""
        if not self.selected_user:
            return
        
        if not hasattr(self, 'message_entry'):
            return
        
        message = self.message_entry.get("1.0", "end-1c").strip()
        
        if not message:
            return
        
        reply_data = None
        if self.replying_to:
            reply_data = {
                "user": self.replying_to["user"],
                "message": self.replying_to["message"]
            }
        
        if self.chat_manager.add_message(self.current_user, message, reply_data):
            self.message_entry.delete("1.0", tk.END)
            self.cancel_reply()
            self.load_messages()
            self.load_user_list()
            self.scroll_to_bottom()
            self.update_send_button()
    
    def load_messages(self):
        """Load messages for selected user"""
        if not self.selected_user or not hasattr(self, 'messages_frame'):
            return
        
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        
        # Get conversation between current user and selected user
        messages = self.chat_manager.get_recent_messages(
            user_filter=self.selected_user,
            current_user=self.current_user
        )
        
        if not messages:
            tk.Label(
                self.messages_frame,
                text=f"No messages with {self.selected_user} yet\nSend a message to start the conversation!",
                font=("Segoe UI", 11),
                bg=self.bg_chat,
                fg=self.text_secondary,
                justify=tk.CENTER
            ).pack(expand=True, pady=100)
        else:
            for msg in messages:
                is_own = msg["user"] == self.current_user
                self.create_message_bubble(self.messages_frame, msg, is_own)
        
        self.messages_frame.update_idletasks()
    
    def scroll_to_bottom(self):
        """Scroll to bottom"""
        if hasattr(self, 'messages_canvas'):
            self.root.update_idletasks()
            self.messages_canvas.yview_moveto(1.0)
    
    def auto_refresh(self):
        """Auto-refresh"""
        if self.is_logged_in:
            self.load_user_list()
            if self.selected_user:
                self.load_messages()
            self.refresh_job = self.root.after(3000, self.auto_refresh)


def main():
    root = tk.Tk()
    app = TelegramChatApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
