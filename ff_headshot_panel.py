#!/usr/bin/env python3
"""
Free Fire Headshot Panel - Pydroid3
A simple panel to track headshots in Free Fire
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os

class FFHeadshotPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Free Fire Headshot Panel")
        self.root.geometry("400x600")
        self.root.configure(bg="#1a1a2e")
        
        # Data storage
        self.headshot_count = 0
        self.session_data = []
        self.data_file = "ff_headshots.json"
        self.load_data()
        
        # Configure colors
        self.bg_color = "#1a1a2e"
        self.fg_color = "#00ff00"
        self.accent_color = "#ff0000"
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(
            self.root,
            text="🎯 FREE FIRE HEADSHOT PANEL 🎯",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack(pady=20)
        
        # Headshot Counter Display
        self.counter_label = tk.Label(
            self.root,
            text=f"HEADSHOTS: {self.headshot_count}",
            font=("Arial", 48, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        self.counter_label.pack(pady=20)
        
        # Headshot buttons frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        # Add Headshot Button
        add_btn = tk.Button(
            button_frame,
            text="➕ ADD HEADSHOT",
            command=self.add_headshot,
            font=("Arial", 12, "bold"),
            bg=self.fg_color,
            fg="#000000",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        add_btn.pack(pady=10)
        
        # Undo Button
        undo_btn = tk.Button(
            button_frame,
            text="↶ UNDO",
            command=self.undo_headshot,
            font=("Arial", 12, "bold"),
            bg="#ffaa00",
            fg="#000000",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        undo_btn.pack(pady=10)
        
        # Reset Button
        reset_btn = tk.Button(
            button_frame,
            text="🔄 RESET",
            command=self.reset_counter,
            font=("Arial", 12, "bold"),
            bg=self.accent_color,
            fg="#ffffff",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        reset_btn.pack(pady=10)
        
        # Stats frame
        stats_frame = tk.Frame(self.root, bg="#2a2a3e", relief=tk.SUNKEN, bd=2)
        stats_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        stats_label = tk.Label(
            stats_frame,
            text="SESSION STATS",
            font=("Arial", 12, "bold"),
            bg="#2a2a3e",
            fg=self.fg_color
        )
        stats_label.pack(pady=10)
        
        # Stats display
        self.stats_text = tk.Text(
            stats_frame,
            height=8,
            width=40,
            bg="#0a0a1a",
            fg=self.fg_color,
            font=("Courier", 10),
            state=tk.DISABLED
        )
        self.stats_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Footer
        footer_label = tk.Label(
            self.root,
            text="GG! Keep grinding headshots 💪",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color
        )
        footer_label.pack(pady=10)
        
    def add_headshot(self):
        """Add a headshot to the counter"""
        self.headshot_count += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.session_data.append({
            "time": timestamp,
            "count": self.headshot_count
        })
        self.update_display()
        self.save_data()
        
    def undo_headshot(self):
        """Undo the last headshot"""
        if self.headshot_count > 0:
            self.headshot_count -= 1
            if self.session_data:
                self.session_data.pop()
            self.update_display()
            self.save_data()
        else:
            messagebox.showinfo("Info", "No headshots to undo!")
            
    def reset_counter(self):
        """Reset the counter"""
        if messagebox.askyesno("Reset", "Are you sure you want to reset the counter?"):
            self.headshot_count = 0
            self.session_data = []
            self.update_display()
            self.save_data()
            
    def update_display(self):
        """Update all display elements"""
        self.counter_label.config(text=f"HEADSHOTS: {self.headshot_count}")
        
        # Update stats
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        if self.session_data:
            stats_text = f"Total Headshots: {self.headshot_count}\n"
            stats_text += f"Session Time: {self.session_data[0]['time']} - {self.session_data[-1]['time']}\n"
            stats_text += f"\nLast 5 Headshots:\n"
            stats_text += "-" * 35 + "\n"
            
            for idx, data in enumerate(self.session_data[-5:], 1):
                stats_text += f"{idx}. Time: {data['time']} | Count: {data['count']}\n"
        else:
            stats_text = "No headshots yet. Start grinding! 🎮"
        
        self.stats_text.insert(1.0, stats_text)
        self.stats_text.config(state=tk.DISABLED)
        
    def save_data(self):
        """Save data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump({
                    "headshot_count": self.headshot_count,
                    "session_data": self.session_data,
                    "last_updated": datetime.now().isoformat()
                }, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")
            
    def load_data(self):
        """Load data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.headshot_count = data.get("headshot_count", 0)
                    self.session_data = data.get("session_data", [])
        except Exception as e:
            print(f"Error loading data: {e}")

def main():
    root = tk.Tk()
    app = FFHeadshotPanel(root)
    root.mainloop()

if __name__ == "__main__":
    main()
