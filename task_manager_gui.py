import tkinter as tk
from tkinter import ttk, messagebox
import json
import csv
from datetime import datetime

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager Pro")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")
        
        self.tasks = []
        self.load_tasks()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(fill=tk.X)
        
        title_label = tk.Label(header, text="📋 Task Manager Pro", 
                               font=("Arial", 24, "bold"), 
                               bg="#2c3e50", fg="white")
        title_label.pack(pady=20)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Input form
        left_panel = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=0)
        
        form_title = tk.Label(left_panel, text="Add New Task", 
                             font=("Arial", 16, "bold"), 
                             bg="white", fg="#2c3e50")
        form_title.pack(pady=15)
        
        # Task Title
        tk.Label(left_panel, text="Task Title:", font=("Arial", 11), 
                bg="white", fg="#34495e").pack(anchor=tk.W, padx=20, pady=(10, 5))
        self.title_entry = tk.Entry(left_panel, font=("Arial", 11), width=30)
        self.title_entry.pack(padx=20, pady=(0, 15))
        
        # Deadline
        tk.Label(left_panel, text="Deadline (YYYY-MM-DD):", font=("Arial", 11), 
                bg="white", fg="#34495e").pack(anchor=tk.W, padx=20, pady=(0, 5))
        self.deadline_entry = tk.Entry(left_panel, font=("Arial", 11), width=30)
        self.deadline_entry.pack(padx=20, pady=(0, 15))
        
        # Priority
        tk.Label(left_panel, text="Priority:", font=("Arial", 11), 
                bg="white", fg="#34495e").pack(anchor=tk.W, padx=20, pady=(0, 5))
        self.priority_var = tk.StringVar(value="Medium")
        priority_frame = tk.Frame(left_panel, bg="white")
        priority_frame.pack(padx=20, pady=(0, 20))
        
        for priority in ["High", "Medium", "Low"]:
            tk.Radiobutton(priority_frame, text=priority, variable=self.priority_var, 
                          value=priority, font=("Arial", 10), bg="white",
                          selectcolor="#3498db").pack(side=tk.LEFT, padx=5)
        
        # Add button
        add_btn = tk.Button(left_panel, text="➕ Add Task", 
                           command=self.add_task,
                           font=("Arial", 12, "bold"), 
                           bg="#27ae60", fg="white",
                           cursor="hand2", relief=tk.FLAT,
                           padx=20, pady=10)
        add_btn.pack(pady=10)
        
        # Export buttons
        export_frame = tk.Frame(left_panel, bg="white")
        export_frame.pack(pady=20)
        
        tk.Button(export_frame, text="📄 Export JSON", 
                 command=self.export_json,
                 font=("Arial", 10), bg="#3498db", fg="white",
                 cursor="hand2", relief=tk.FLAT, padx=10, pady=5).pack(pady=5, fill=tk.X)
        
        tk.Button(export_frame, text="📊 Export CSV", 
                 command=self.export_csv,
                 font=("Arial", 10), bg="#3498db", fg="white",
                 cursor="hand2", relief=tk.FLAT, padx=10, pady=5).pack(pady=5, fill=tk.X)
        
        # Right panel - Task list
        right_panel = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        list_title = tk.Label(right_panel, text="Task List", 
                             font=("Arial", 16, "bold"), 
                             bg="white", fg="#2c3e50")
        list_title.pack(pady=15)
        
        # Treeview for tasks
        tree_frame = tk.Frame(right_panel, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, columns=("Title", "Deadline", "Priority", "Status"),
                                show="headings", yscrollcommand=scrollbar.set, height=15)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Configure columns
        self.tree.heading("Title", text="Task Title")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("Title", width=250)
        self.tree.column("Deadline", width=100)
        self.tree.column("Priority", width=80)
        self.tree.column("Status", width=80)
        
        # Style for treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        
        # Action buttons
        btn_frame = tk.Frame(right_panel, bg="white")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="✓ Complete", 
                 command=self.complete_task,
                 font=("Arial", 10, "bold"), bg="#27ae60", fg="white",
                 cursor="hand2", relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑 Delete", 
                 command=self.delete_task,
                 font=("Arial", 10, "bold"), bg="#e74c3c", fg="white",
                 cursor="hand2", relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🔄 Refresh", 
                 command=self.refresh_tasks,
                 font=("Arial", 10, "bold"), bg="#95a5a6", fg="white",
                 cursor="hand2", relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        
        self.refresh_tasks()
    
    def add_task(self):
        title = self.title_entry.get().strip()
        deadline = self.deadline_entry.get().strip()
        priority = self.priority_var.get()
        
        if not title:
            messagebox.showwarning("Input Error", "Please enter a task title!")
            return
        
        if not deadline:
            messagebox.showwarning("Input Error", "Please enter a deadline!")
            return
        
        task = {
            "title": title,
            "deadline": deadline,
            "priority": priority,
            "completed": False
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.refresh_tasks()
        
        # Clear inputs
        self.title_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.priority_var.set("Medium")
        
        messagebox.showinfo("Success", "✅ Task added successfully!")
    
    def complete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to complete!")
            return
        
        index = self.tree.index(selected[0])
        self.tasks[index]["completed"] = True
        self.save_tasks()
        self.refresh_tasks()
        messagebox.showinfo("Success", "✅ Task marked as completed!")
    
    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to delete!")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            index = self.tree.index(selected[0])
            self.tasks.pop(index)
            self.save_tasks()
            self.refresh_tasks()
            messagebox.showinfo("Success", "🗑 Task deleted!")
    
    def refresh_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for task in self.tasks:
            status = "✔ Done" if task["completed"] else "❌ Pending"
            priority_color = {
                "High": "red",
                "Medium": "orange",
                "Low": "green"
            }.get(task["priority"], "black")
            
            item = self.tree.insert("", tk.END, values=(
                task["title"],
                task["deadline"],
                task["priority"],
                status
            ))
            
            # Color code by priority
            if task["priority"] == "High":
                self.tree.item(item, tags=("high",))
            elif task["priority"] == "Medium":
                self.tree.item(item, tags=("medium",))
            else:
                self.tree.item(item, tags=("low",))
        
        self.tree.tag_configure("high", background="#ffcccc")
        self.tree.tag_configure("medium", background="#fff4cc")
        self.tree.tag_configure("low", background="#ccffcc")
    
    def export_json(self):
        try:
            with open("tasks.json", "w") as f:
                json.dump(self.tasks, f, indent=4)
            messagebox.showinfo("Success", "📁 Exported to tasks.json")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def export_csv(self):
        try:
            with open("tasks.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Deadline", "Priority", "Completed"])
                for task in self.tasks:
                    writer.writerow([
                        task["title"],
                        task["deadline"],
                        task["priority"],
                        task["completed"]
                    ])
            messagebox.showinfo("Success", "📁 Exported to tasks.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []
    
    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
