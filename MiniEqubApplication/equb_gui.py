import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from equb_manager import EqubManager
import random

class EqubGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ahadu Equb System - Multi-Group Manager")
        self.root.geometry("1300x800")
        self.root.configure(bg="#f0f0f0")
        
        self.manager = EqubManager()
        self.current_group_id = None
        
        # Color scheme - Ahadu flag inspired
        self.primary_color = "#1a5f3f"  # Green
        self.secondary_color = "#ffd700"  # Gold/Yellow
        self.accent_color = "#c8102e"  # Red
        self.info_color = "#2980b9"
        self.bg_color = "#ecf0f1"
        
        self.setup_ui()
        self.refresh_groups()
    
    def setup_ui(self):
        """Setup the main UI"""
        # Title
        title_frame = tk.Frame(self.root, bg=self.primary_color, height=90)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="Ahadu Equb System ",
            font=("Arial", 22, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Manage Multiple ROSCA Groups | Members can join multiple groups",
            font=("Arial", 10),
            bg=self.primary_color,
            fg=self.secondary_color
        )
        subtitle_label.pack()
        
        # Group selector bar
        self.setup_group_selector()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Group & Member Management
        left_panel = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.setup_left_panel(left_panel)
        
        # Middle panel - Round Management
        middle_panel = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        middle_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.setup_round_panel(middle_panel)
        
        # Right panel - History
        right_panel = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        self.setup_history_panel(right_panel)

    def setup_group_selector(self):
        """Setup group selector bar"""
        selector_frame = tk.Frame(self.root, bg=self.secondary_color, height=60)
        selector_frame.pack(fill=tk.X)
        selector_frame.pack_propagate(False)
        
        left_frame = tk.Frame(selector_frame, bg=self.secondary_color)
        left_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(left_frame, text="Select Group:", font=("Arial", 11, "bold"), bg=self.secondary_color, fg=self.primary_color).pack(side=tk.LEFT, padx=5)
        
        self.group_var = tk.StringVar()
        self.group_combo = ttk.Combobox(left_frame, textvariable=self.group_var, state="readonly", font=("Arial", 10), width=30)
        self.group_combo.pack(side=tk.LEFT, padx=5)
        self.group_combo.bind("<<ComboboxSelected>>", self.on_group_select)
        
        tk.Button(
            selector_frame,
            text="➕ New Group",
            command=self.create_new_group,
            bg=self.primary_color,
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=5
        ).pack(side=tk.RIGHT, padx=10)
    
    def setup_left_panel(self, parent):
        """Setup left panel for group and member management"""
        header = tk.Label(
            parent,
            text="👥 Group Members",
            font=("Arial", 14, "bold"),
            bg=self.primary_color,
            fg="white",
            pady=8
        )
        header.pack(fill=tk.X)
        
        # Add member section
        add_frame = tk.Frame(parent, bg="white", pady=10)
        add_frame.pack(fill=tk.X, padx=10)
        
        tk.Label(add_frame, text="Add Member to Group", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", pady=5)
        
        form_frame = tk.Frame(add_frame, bg="white")
        form_frame.pack(fill=tk.X)
        
        tk.Label(form_frame, text="Name:", font=("Arial", 9), bg="white").grid(row=0, column=0, sticky="w", pady=3)
        self.member_name_entry = tk.Entry(form_frame, font=("Arial", 9), width=20)
        self.member_name_entry.grid(row=0, column=1, pady=3, padx=5)
        
        tk.Label(form_frame, text="Phone:", font=("Arial", 9), bg="white").grid(row=1, column=0, sticky="w", pady=3)
        self.member_phone_entry = tk.Entry(form_frame, font=("Arial", 9), width=20)
        self.member_phone_entry.grid(row=1, column=1, pady=3, padx=5)
        
        btn_frame = tk.Frame(add_frame, bg="white")
        btn_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(
            btn_frame,
            text="➕ Add to Group",
            command=self.add_member_to_group,
            bg=self.primary_color,
            fg="white",
            font=("Arial", 9, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=8,
            pady=4
        ).pack(side=tk.LEFT, padx=3)
        
        tk.Button(
            btn_frame,
            text="🗑️ Remove",
            command=self.remove_member_from_group,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 9, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=8,
            pady=4
        ).pack(side=tk.LEFT, padx=3)
        
        # Member list
        tk.Label(parent, text="Members in Selected Group", font=("Arial", 10, "bold"), bg="white").pack(pady=(10, 5))
        
        tree_frame = tk.Frame(parent, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.member_tree = ttk.Treeview(
            tree_frame,
            columns=("Name", "Phone", "Status", "Contributed"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15
        )
        self.member_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.member_tree.yview)
        
        self.member_tree.heading("Name", text="Name")
        self.member_tree.heading("Phone", text="Phone")
        self.member_tree.heading("Status", text="Status")
        self.member_tree.heading("Contributed", text="Total Paid")
        
        self.member_tree.column("Name", width=100)
        self.member_tree.column("Phone", width=90)
        self.member_tree.column("Status", width=80)
        self.member_tree.column("Contributed", width=90)

    def setup_round_panel(self, parent):
        """Setup round management panel"""
        header = tk.Label(
            parent,
            text="🎲 Round Management (Lottery)",
            font=("Arial", 14, "bold"),
            bg=self.accent_color,
            fg="white",
            pady=8
        )
        header.pack(fill=tk.X)
        
        # Current cycle info
        info_frame = tk.Frame(parent, bg="#fff9e6", relief=tk.RIDGE, bd=2)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.cycle_info_label = tk.Label(
            info_frame,
            text="Select a group to view details",
            font=("Arial", 10),
            bg="#fff9e6",
            justify=tk.LEFT
        )
        self.cycle_info_label.pack(pady=10, padx=10)
        
        # Lottery section
        lottery_frame = tk.Frame(parent, bg="white", pady=10)
        lottery_frame.pack(fill=tk.X, padx=10)
        
        tk.Label(lottery_frame, text="🎰 Lottery Distribution", font=("Arial", 11, "bold"), bg="white", fg=self.accent_color).pack(pady=5)
        
        tk.Button(
            lottery_frame,
            text="🎲 Run Lottery & Distribute",
            command=self.run_lottery,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10
        ).pack(pady=10)
        
        self.lottery_result_label = tk.Label(
            lottery_frame,
            text="",
            font=("Arial", 10, "bold"),
            bg="white",
            fg=self.primary_color
        )
        self.lottery_result_label.pack(pady=5)
        
        # Manual selection (optional)
        manual_frame = tk.Frame(parent, bg="#f0f0f0", relief=tk.RIDGE, bd=1)
        manual_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(manual_frame, text="Manual Selection (Optional)", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=5)
        
        self.manual_recipient_var = tk.StringVar()
        self.manual_recipient_combo = ttk.Combobox(manual_frame, textvariable=self.manual_recipient_var, state="readonly", font=("Arial", 9), width=25)
        self.manual_recipient_combo.pack(pady=5)
        
        tk.Button(
            manual_frame,
            text="Distribute to Selected",
            command=self.manual_distribute,
            bg=self.info_color,
            fg="white",
            font=("Arial", 9, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(pady=5)
        
        # Recent rounds
        tk.Label(parent, text="Recent Rounds", font=("Arial", 10, "bold"), bg="white").pack(pady=(10, 5))
        
        rounds_frame = tk.Frame(parent, bg="white")
        rounds_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(rounds_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.rounds_tree = ttk.Treeview(
            rounds_frame,
            columns=("Round", "Recipient", "Amount", "Date"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=8
        )
        self.rounds_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.rounds_tree.yview)
        
        self.rounds_tree.heading("Round", text="Round")
        self.rounds_tree.heading("Recipient", text="Winner")
        self.rounds_tree.heading("Amount", text="Payout")
        self.rounds_tree.heading("Date", text="Date")
        
        self.rounds_tree.column("Round", width=60)
        self.rounds_tree.column("Recipient", width=100)
        self.rounds_tree.column("Amount", width=90)
        self.rounds_tree.column("Date", width=100)

    def setup_history_panel(self, parent):
        """Setup history panel"""
        header = tk.Label(
            parent,
            text="📊 Group History",
            font=("Arial", 14, "bold"),
            bg=self.info_color,
            fg="white",
            pady=8
        )
        header.pack(fill=tk.X)
        
        # Group selector for history
        history_selector_frame = tk.Frame(parent, bg="white", pady=10)
        history_selector_frame.pack(fill=tk.X, padx=10)
        
        tk.Label(history_selector_frame, text="View History for:", font=("Arial", 9, "bold"), bg="white").pack(anchor="w")
        
        self.history_group_var = tk.StringVar()
        self.history_group_combo = ttk.Combobox(history_selector_frame, textvariable=self.history_group_var, state="readonly", font=("Arial", 9), width=30)
        self.history_group_combo.pack(pady=5, fill=tk.X)
        self.history_group_combo.bind("<<ComboboxSelected>>", self.on_history_group_select)
        
        # Statistics
        stats_frame = tk.Frame(parent, bg="white")
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 9),
            bg="white",
            justify=tk.LEFT
        )
        self.stats_label.pack(anchor="w")
        
        # History text
        self.history_text = scrolledtext.ScrolledText(
            parent,
            font=("Courier", 8),
            height=20,
            wrap=tk.WORD,
            bg="#f9f9f9"
        )
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(parent, bg="white")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(
            btn_frame,
            text="🔄 New Cycle",
            command=self.force_new_cycle,
            bg=self.info_color,
            fg="white",
            font=("Arial", 9, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=8,
            pady=4
        ).pack(side=tk.LEFT, padx=3)
        
        tk.Button(
            btn_frame,
            text="🗑️ Delete Group",
            command=self.delete_group,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 9, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=8,
            pady=4
        ).pack(side=tk.LEFT, padx=3)

    def create_new_group(self):
        """Create a new Equb group"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Equb Group")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="🏦 Create New Equb Group", font=("Arial", 16, "bold")).pack(pady=20)
        
        frame = tk.Frame(dialog)
        frame.pack(pady=10, padx=20)
        
        tk.Label(frame, text="Group Name:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        group_name_entry = tk.Entry(frame, font=("Arial", 10), width=25)
        group_name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(frame, text="Fixed Amount (ETB):", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        amount_entry = tk.Entry(frame, font=("Arial", 10), width=25)
        amount_entry.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(frame, text="Frequency:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        frequency_var = tk.StringVar(value="Monthly")
        frequency_combo = ttk.Combobox(frame, textvariable=frequency_var, values=["Daily", "Weekly", "Monthly"], state="readonly", width=23)
        frequency_combo.grid(row=2, column=1, pady=5, padx=5)
        
        def save_group():
            try:
                name = group_name_entry.get().strip()
                amount = float(amount_entry.get())
                if not name or amount <= 0:
                    raise ValueError()
                
                group_id = self.manager.create_group(name, amount, frequency_var.get())
                messagebox.showinfo("Success", f"Group '{name}' created successfully!")
                dialog.destroy()
                self.refresh_groups()
                self.current_group_id = group_id
                self.select_group(group_id)
            except:
                messagebox.showerror("Error", "Please enter valid group details!")
        
        tk.Button(dialog, text="Create Group", command=save_group, bg=self.primary_color, fg="white", font=("Arial", 11, "bold"), padx=20, pady=5).pack(pady=20)
    
    def add_member_to_group(self):
        """Add member to current group"""
        if not self.current_group_id:
            messagebox.showwarning("No Group", "Please select a group first!")
            return
        
        name = self.member_name_entry.get().strip()
        phone = self.member_phone_entry.get().strip()
        
        if not name:
            messagebox.showwarning("Input Error", "Please enter member name!")
            return
        
        # Add member to system (or get existing)
        member_id = self.manager.add_member_to_system(name, phone)
        
        # Add to current group
        if self.manager.add_member_to_group(self.current_group_id, member_id):
            messagebox.showinfo("Success", f"Member '{name}' added to group!")
            self.member_name_entry.delete(0, tk.END)
            self.member_phone_entry.delete(0, tk.END)
            self.refresh_current_group()
        else:
            messagebox.showinfo("Info", f"Member '{name}' is already in this group!")
    
    def remove_member_from_group(self):
        """Remove member from current group"""
        if not self.current_group_id:
            messagebox.showwarning("No Group", "Please select a group first!")
            return
        
        selection = self.member_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a member to remove!")
            return
        
        item = self.member_tree.item(selection[0])
        name = item['values'][0]
        
        # Find member ID
        members = self.manager.get_group_members(self.current_group_id)
        member_id = None
        for m in members:
            if m['name'] == name:
                member_id = m['id']
                break
        
        if member_id and messagebox.askyesno("Confirm Remove", f"Remove '{name}' from this group?\n\nNote: Can only remove if they haven't received yet."):
            if self.manager.remove_member_from_group(self.current_group_id, member_id):
                messagebox.showinfo("Success", f"Member '{name}' removed from group!")
                self.refresh_current_group()
            else:
                messagebox.showerror("Error", "Cannot remove member who has already received in this cycle!")

    def run_lottery(self):
        """Run lottery to select random recipient"""
        if not self.current_group_id:
            messagebox.showwarning("No Group", "Please select a group first!")
            return
        
        available = self.manager.get_available_recipients(self.current_group_id)
        if not available:
            messagebox.showinfo("Cycle Complete", "All members have received! Starting new cycle...")
            self.manager.start_new_cycle(self.current_group_id)
            self.refresh_current_group()
            return
        
        cycle_info = self.manager.get_group_cycle_info(self.current_group_id)
        
        # Show lottery animation
        lottery_dialog = tk.Toplevel(self.root)
        lottery_dialog.title("🎲 Running Lottery...")
        lottery_dialog.geometry("400x300")
        lottery_dialog.transient(self.root)
        lottery_dialog.grab_set()
        
        tk.Label(lottery_dialog, text="🎰 LOTTERY IN PROGRESS", font=("Arial", 18, "bold"), fg=self.accent_color).pack(pady=20)
        
        name_label = tk.Label(lottery_dialog, text="", font=("Arial", 24, "bold"), fg=self.primary_color)
        name_label.pack(pady=30)
        
        # Animate names
        animation_count = [0]
        
        def animate():
            if animation_count[0] < 20:
                random_member = random.choice(available)
                name_label.config(text=random_member['name'])
                animation_count[0] += 1
                lottery_dialog.after(100, animate)
            else:
                # Select winner
                winner = random.choice(available)
                name_label.config(text=f"🎉 {winner['name']} 🎉", fg=self.accent_color)
                
                def confirm_winner():
                    lottery_dialog.destroy()
                    self.distribute_to_member(winner['id'], winner['name'], is_lottery=True)
                
                tk.Button(
                    lottery_dialog,
                    text="✅ Confirm & Distribute",
                    command=confirm_winner,
                    bg=self.accent_color,
                    fg="white",
                    font=("Arial", 12, "bold"),
                    padx=20,
                    pady=10
                ).pack(pady=20)
        
        animate()
    
    def manual_distribute(self):
        """Manually distribute to selected member"""
        if not self.current_group_id:
            messagebox.showwarning("No Group", "Please select a group first!")
            return
        
        recipient_name = self.manual_recipient_var.get()
        if not recipient_name:
            messagebox.showwarning("Selection Error", "Please select a recipient!")
            return
        
        # Find member ID
        members = self.manager.get_group_members(self.current_group_id)
        member_id = None
        for m in members:
            if m['name'] == recipient_name:
                member_id = m['id']
                break
        
        if member_id:
            self.distribute_to_member(member_id, recipient_name, is_lottery=False)
    
    def distribute_to_member(self, member_id, member_name, is_lottery=False):
        """Distribute funds to a specific member"""
        cycle_info = self.manager.get_group_cycle_info(self.current_group_id)
        total_payout = cycle_info['fixed_amount'] * cycle_info['total_members']
        
        method = "🎲 Lottery" if is_lottery else "Manual"
        confirm_msg = f"Distribute Round {cycle_info['current_round'] + 1}?\n\n"
        confirm_msg += f"Method: {method}\n"
        confirm_msg += f"Recipient: {member_name}\n"
        confirm_msg += f"Each member contributes: ETB {cycle_info['fixed_amount']:,.2f}\n"
        confirm_msg += f"Total payout: ETB {total_payout:,.2f}\n\n"
        confirm_msg += f"All {cycle_info['total_members']} members will be charged."
        
        if messagebox.askyesno("Confirm Distribution", confirm_msg):
            round_data = self.manager.start_new_round(self.current_group_id, member_id)
            if round_data:
                messagebox.showinfo(
                    "Distribution Complete!",
                    f"Round {round_data['round_number']} completed!\n\n"
                    f"Winner: {member_name}\n"
                    f"Payout: ETB {round_data['total_payout']:,.2f}\n"
                    f"Per member: ETB {round_data['amount_per_member']:,.2f}"
                )
                self.lottery_result_label.config(text=f"Last Winner: {member_name} - ETB {round_data['total_payout']:,.2f}")
                self.refresh_current_group()
            else:
                messagebox.showerror("Error", "Failed to distribute. Member may have already received.")
    
    def force_new_cycle(self):
        """Force start a new cycle"""
        if not self.current_group_id:
            messagebox.showwarning("No Group", "Please select a group first!")
            return
        
        if messagebox.askyesno("New Cycle", "Start a new cycle? This will reset all members' received status."):
            self.manager.start_new_cycle(self.current_group_id)
            messagebox.showinfo("Success", "New cycle started!")
            self.refresh_current_group()
    
    def delete_group(self):
        """Delete current group"""
        if not self.current_group_id:
            messagebox.showwarning("No Group", "Please select a group first!")
            return
        
        group = self.manager.get_group(self.current_group_id)
        if messagebox.askyesno("Confirm Delete", f"Delete group '{group['name']}'?\n\nThis action cannot be undone!"):
            self.manager.delete_group(self.current_group_id)
            messagebox.showinfo("Success", "Group deleted!")
            self.current_group_id = None
            self.refresh_groups()

    def on_group_select(self, event=None):
        """Handle group selection"""
        selected = self.group_var.get()
        if selected:
            # Extract group ID from selection
            for group in self.manager.get_all_groups():
                if f"{group['name']} (ETB {group['fixed_amount']:,.2f})" == selected:
                    self.current_group_id = group['id']
                    self.select_group(group['id'])
                    break
    
    def on_history_group_select(self, event=None):
        """Handle history group selection"""
        selected = self.history_group_var.get()
        if selected:
            for group in self.manager.get_all_groups():
                if f"{group['name']} (ETB {group['fixed_amount']:,.2f})" == selected:
                    self.refresh_history(group['id'])
                    break
    
    def select_group(self, group_id):
        """Select and display a specific group"""
        self.current_group_id = group_id
        self.refresh_current_group()
    
    def refresh_groups(self):
        """Refresh group list"""
        groups = self.manager.get_all_groups()
        group_names = [f"{g['name']} (ETB {g['fixed_amount']:,.2f})" for g in groups]
        
        self.group_combo['values'] = group_names
        self.history_group_combo['values'] = group_names
        
        if groups and not self.current_group_id:
            self.current_group_id = groups[0]['id']
            self.group_combo.current(0)
            self.history_group_combo.current(0)
            self.select_group(self.current_group_id)
        elif self.current_group_id:
            # Keep current selection
            group = self.manager.get_group(self.current_group_id)
            if group:
                display_name = f"{group['name']} (ETB {group['fixed_amount']:,.2f})"
                if display_name in group_names:
                    self.group_combo.set(display_name)
                    self.history_group_combo.set(display_name)
    
    def refresh_current_group(self):
        """Refresh all displays for current group"""
        if not self.current_group_id:
            return
        
        self.refresh_members()
        self.refresh_rounds()
        self.refresh_cycle_info()
        self.update_recipient_lists()
        self.refresh_history(self.current_group_id)
    
    def refresh_members(self):
        """Refresh member list"""
        for item in self.member_tree.get_children():
            self.member_tree.delete(item)
        
        if not self.current_group_id:
            return
        
        members = self.manager.get_group_members(self.current_group_id)
        for member in members:
            status = "✅ Received" if member['has_received'] else "⏳ Waiting"
            self.member_tree.insert(
                "",
                tk.END,
                values=(
                    member['name'],
                    member['phone'],
                    status,
                    f"ETB {member['total_contributed']:,.2f}"
                )
            )
    
    def refresh_rounds(self):
        """Refresh rounds list"""
        for item in self.rounds_tree.get_children():
            self.rounds_tree.delete(item)
        
        if not self.current_group_id:
            return
        
        rounds = self.manager.get_group_rounds(self.current_group_id)
        for round_data in reversed(rounds[-10:]):
            self.rounds_tree.insert(
                "",
                tk.END,
                values=(
                    f"R{round_data['round_number']}",
                    round_data['recipient_name'],
                    f"ETB {round_data['total_payout']:,.2f}",
                    round_data['date'].split()[0]
                )
            )
    
    def refresh_cycle_info(self):
        """Refresh cycle information"""
        if not self.current_group_id:
            self.cycle_info_label.config(text="Select a group to view details")
            return
        
        cycle_info = self.manager.get_group_cycle_info(self.current_group_id)
        
        info_text = f"Group: {cycle_info['group_name']}\n"
        info_text += f"Cycle: {cycle_info['cycle_number']} | Round: {cycle_info['current_round']}/{cycle_info['total_members']}\n"
        info_text += f"Received: {cycle_info['received_count']} | Remaining: {cycle_info['remaining']}\n"
        info_text += f"Fixed Amount: ETB {cycle_info['fixed_amount']:,.2f} ({cycle_info['frequency']})"
        
        self.cycle_info_label.config(text=info_text)
    
    def update_recipient_lists(self):
        """Update available recipients in dropdowns"""
        if not self.current_group_id:
            return
        
        available = self.manager.get_available_recipients(self.current_group_id)
        names = [m['name'] for m in available]
        
        self.manual_recipient_combo['values'] = names
        if names:
            self.manual_recipient_combo.current(0)
    
    def refresh_history(self, group_id):
        """Refresh history for a specific group"""
        self.history_text.delete(1.0, tk.END)
        
        group = self.manager.get_group(group_id)
        if not group:
            return
        
        cycle_info = self.manager.get_group_cycle_info(group_id)
        rounds = self.manager.get_group_rounds(group_id)
        members = self.manager.get_group_members(group_id)
        
        self.history_text.insert(tk.END, f"{'='*70}\n")
        self.history_text.insert(tk.END, f"  {group['name']}\n")
        self.history_text.insert(tk.END, f"{'='*70}\n\n")
        
        # Statistics
        self.history_text.insert(tk.END, f"  Total Members: {len(members)}\n")
        self.history_text.insert(tk.END, f"  Total Rounds Completed: {len(rounds)}\n")
        self.history_text.insert(tk.END, f"  Current Cycle: {cycle_info['cycle_number']}\n")
        self.history_text.insert(tk.END, f"  Fixed Contribution: ETB {cycle_info['fixed_amount']:,.2f}\n")
        self.history_text.insert(tk.END, f"  Frequency: {cycle_info['frequency']}\n")
        self.history_text.insert(tk.END, f"  Created: {group['created_date']}\n\n")
        
        # Member summary
        self.history_text.insert(tk.END, f"  Member Summary:\n")
        self.history_text.insert(tk.END, f"  {'-'*70}\n")
        for member in members:
            status = "✅" if member['has_received'] else "⏳"
            self.history_text.insert(tk.END, f"  {status} {member['name']:<20} Paid: ETB {member['total_contributed']:>10,.2f}  Received: ETB {member['total_received']:>10,.2f}\n")
        
        if rounds:
            self.history_text.insert(tk.END, f"\n  Round History:\n")
            self.history_text.insert(tk.END, f"  {'-'*70}\n")
            
            for round_data in reversed(rounds[-20:]):
                self.history_text.insert(tk.END, f"\n  Round {round_data['round_number']} (Cycle {round_data['cycle_number']})\n")
                self.history_text.insert(tk.END, f"  Date: {round_data['date']}\n")
                self.history_text.insert(tk.END, f"  Winner: {round_data['recipient_name']}\n")
                self.history_text.insert(tk.END, f"  Payout: ETB {round_data['total_payout']:,.2f}\n")
                self.history_text.insert(tk.END, f"  {'-'*70}\n")

def main():
    root = tk.Tk()
    app = EqubGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
