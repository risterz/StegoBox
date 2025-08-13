#!/usr/bin/env python3
"""
StegoBox GUI - Modern Steganography Tool
Hide folders/ZIP files in images with a beautiful interface
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import customtkinter as ctk
import threading
import os
import sys
import struct
import zipfile
import io
import getpass
from pathlib import Path
import time

from PIL import Image, ImageTk

# Import steganography functions from the local module
from example import (
    zip_folder_to_bytes, load_payload, append_embed, append_extract,
    lsb_embed, lsb_extract, lsb_capacity, encrypt_payload, decrypt_payload,
    APPEND_MAGIC, LSB_MAGIC, VERSION
)

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class StegoBoxGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("🕵️ StegoBox - Advanced Steganography Tool | Created by @Risterz")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main interface
        self.create_interface()
    
    def create_interface(self):
        """Create the main GUI interface"""
        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # Sidebar title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="🕵️ StegoBox", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Method selection
        self.method_label = ctk.CTkLabel(self.sidebar_frame, text="Method:")
        self.method_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        
        self.method_var = ctk.StringVar(value="append")
        self.method_menu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["append", "lsb"],
            variable=self.method_var,
            command=self.method_changed
        )
        self.method_menu.grid(row=2, column=0, padx=20, pady=10)
        
        # Theme toggle
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Theme:")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=(10, 20))
        
        # Main content area
        self.create_main_content()
        
        # Status bar
        self.status_var = ctk.StringVar(value="Ready")
        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var)
        self.status_label.grid(row=3, column=1, padx=20, pady=(0, 20), sticky="ew")
    
    def create_main_content(self):
        """Create the main content area with tabs"""
        # Create tabview
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        # Add tabs
        self.tabview.add("Hide Data")
        self.tabview.add("Extract Data")
        
        # Configure tabs
        self.create_hide_tab()
        self.create_extract_tab()
    
    def create_hide_tab(self):
        """Create the hide data tab"""
        tab = self.tabview.tab("Hide Data")
        
        # Cover image selection
        self.cover_frame = ctk.CTkFrame(tab)
        self.cover_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        ctk.CTkLabel(tab, text="1. Select Cover Image:", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, padx=20, pady=(20, 5), sticky="w"
        )
        
        self.cover_path_var = ctk.StringVar()
        self.cover_entry = ctk.CTkEntry(tab, textvariable=self.cover_path_var, width=400)
        self.cover_entry.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        
        self.cover_button = ctk.CTkButton(tab, text="Browse", command=self.select_cover_image)
        self.cover_button.grid(row=1, column=1, padx=(0, 20), pady=5)
        
        # Data selection
        ctk.CTkLabel(tab, text="2. Select Data to Hide:", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=2, column=0, padx=20, pady=(20, 5), sticky="w"
        )
        
        self.data_path_var = ctk.StringVar()
        self.data_entry = ctk.CTkEntry(tab, textvariable=self.data_path_var, width=400)
        self.data_entry.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        self.data_button = ctk.CTkButton(tab, text="Browse", command=self.select_data)
        self.data_button.grid(row=3, column=1, padx=(0, 20), pady=5)
        
        # Encryption options
        self.encrypt_var = ctk.BooleanVar()
        self.encrypt_check = ctk.CTkCheckBox(
            tab, 
            text="Encrypt with password (LSB only)", 
            variable=self.encrypt_var,
            command=self.toggle_encryption
        )
        self.encrypt_check.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        
        self.password_var = ctk.StringVar()
        self.password_entry = ctk.CTkEntry(tab, textvariable=self.password_var, show="*", placeholder_text="Password")
        self.password_entry.grid(row=5, column=0, padx=20, pady=5, sticky="ew")
        self.password_entry.configure(state="disabled")
        
        # Output selection
        ctk.CTkLabel(tab, text="3. Output Location:", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=6, column=0, padx=20, pady=(20, 5), sticky="w"
        )
        
        self.output_path_var = ctk.StringVar()
        self.output_entry = ctk.CTkEntry(tab, textvariable=self.output_path_var, width=400)
        self.output_entry.grid(row=7, column=0, padx=20, pady=5, sticky="ew")
        
        self.output_button = ctk.CTkButton(tab, text="Browse", command=self.select_output)
        self.output_button.grid(row=7, column=1, padx=(0, 20), pady=5)
        
        # Hide button
        self.hide_button = ctk.CTkButton(
            tab, 
            text="🔒 Hide Data", 
            command=self.hide_data,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.hide_button.grid(row=8, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        
        # Progress bar
        self.hide_progress = ctk.CTkProgressBar(tab)
        self.hide_progress.grid(row=9, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        self.hide_progress.set(0)
        
        # Configure grid weights
        tab.grid_columnconfigure(0, weight=1)
    
    def create_extract_tab(self):
        """Create the extract data tab"""
        tab = self.tabview.tab("Extract Data")
        
        # Stego image selection
        ctk.CTkLabel(tab, text="1. Select Stego Image:", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, padx=20, pady=(20, 5), sticky="w"
        )
        
        self.stego_path_var = ctk.StringVar()
        self.stego_entry = ctk.CTkEntry(tab, textvariable=self.stego_path_var, width=400)
        self.stego_entry.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        
        self.stego_button = ctk.CTkButton(tab, text="Browse", command=self.select_stego_image)
        self.stego_button.grid(row=1, column=1, padx=(0, 20), pady=5)
        
        # Password entry
        ctk.CTkLabel(tab, text="2. Password (if encrypted):", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=2, column=0, padx=20, pady=(20, 5), sticky="w"
        )
        
        self.extract_password_var = ctk.StringVar()
        self.extract_password_entry = ctk.CTkEntry(
            tab, 
            textvariable=self.extract_password_var, 
            show="*", 
            placeholder_text="Leave empty if not encrypted"
        )
        self.extract_password_entry.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        # Extract output selection
        ctk.CTkLabel(tab, text="3. Extract to:", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=4, column=0, padx=20, pady=(20, 5), sticky="w"
        )
        
        self.extract_output_var = ctk.StringVar()
        self.extract_output_entry = ctk.CTkEntry(tab, textvariable=self.extract_output_var, width=400)
        self.extract_output_entry.grid(row=5, column=0, padx=20, pady=5, sticky="ew")
        
        self.extract_output_button = ctk.CTkButton(tab, text="Browse", command=self.select_extract_output)
        self.extract_output_button.grid(row=5, column=1, padx=(0, 20), pady=5)
        
        # Extract button
        self.extract_button = ctk.CTkButton(
            tab, 
            text="🔓 Extract Data", 
            command=self.extract_data,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.extract_button.grid(row=6, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        
        # Progress bar
        self.extract_progress = ctk.CTkProgressBar(tab)
        self.extract_progress.grid(row=7, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        self.extract_progress.set(0)
        
        # Configure grid weights
        tab.grid_columnconfigure(0, weight=1)
    
    def method_changed(self, value):
        """Handle method selection change"""
        if value == "lsb":
            self.encrypt_check.configure(state="normal")
            self.status_var.set("LSB mode selected - invisible hiding with optional encryption")
        else:
            self.encrypt_check.configure(state="disabled")
            self.encrypt_var.set(False)
            self.password_entry.configure(state="disabled")
            self.status_var.set("Append mode selected - fast hiding, larger file size")
    
    def toggle_encryption(self):
        """Toggle password field based on encryption checkbox"""
        if self.encrypt_var.get():
            self.password_entry.configure(state="normal")
        else:
            self.password_entry.configure(state="disabled")
    
    def change_appearance_mode(self, new_mode):
        """Change the appearance mode"""
        ctk.set_appearance_mode(new_mode.lower())
    
    def select_cover_image(self):
        """Select cover image file"""
        file_path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.cover_path_var.set(file_path)
    
    def select_data(self):
        """Select data to hide (folder or ZIP file)"""
        choice = messagebox.askyesno(
            "Select Data Type",
            "Do you want to select a folder? (No = select ZIP file)"
        )
        
        if choice:  # Folder
            folder_path = filedialog.askdirectory(title="Select Folder to Hide")
            if folder_path:
                self.data_path_var.set(folder_path)
        else:  # ZIP file
            file_path = filedialog.askopenfilename(
                title="Select ZIP File",
                filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
            )
            if file_path:
                self.data_path_var.set(file_path)
    
    def select_output(self):
        """Select output location for stego image"""
        file_path = filedialog.asksaveasfilename(
            title="Save Stego Image As",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("BMP files", "*.bmp"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.output_path_var.set(file_path)
    
    def select_stego_image(self):
        """Select stego image for extraction"""
        file_path = filedialog.askopenfilename(
            title="Select Stego Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.stego_path_var.set(file_path)
    
    def select_extract_output(self):
        """Select output location for extracted data"""
        file_path = filedialog.asksaveasfilename(
            title="Save Extracted Data As",
            defaultextension=".zip",
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
        )
        if file_path:
            self.extract_output_var.set(file_path)
    
    def hide_data(self):
        """Hide data in the selected image"""
        # Validate inputs
        if not self.cover_path_var.get():
            messagebox.showerror("Error", "Please select a cover image")
            return
        
        if not self.data_path_var.get():
            messagebox.showerror("Error", "Please select data to hide")
            return
        
        if not self.output_path_var.get():
            messagebox.showerror("Error", "Please select output location")
            return
        
        if self.method_var.get() == "lsb" and self.encrypt_var.get() and not self.password_var.get():
            messagebox.showerror("Error", "Please enter a password for encryption")
            return
        
        # Run hiding operation in a separate thread
        threading.Thread(target=self._hide_data_thread, daemon=True).start()
    
    def _hide_data_thread(self):
        """Thread function for hiding data"""
        try:
            self.hide_progress.set(0.1)
            self.status_var.set("Loading data...")
            
            # Load payload
            data_path = self.data_path_var.get()
            if os.path.isdir(data_path):
                payload = zip_folder_to_bytes(data_path)
            else:
                payload = load_payload(data_path)
            
            self.hide_progress.set(0.3)
            self.status_var.set("Processing image...")
            
            # Load cover image
            cover_path = self.cover_path_var.get()
            output_path = self.output_path_var.get()
            
            self.hide_progress.set(0.5)
            
            if self.method_var.get() == "append":
                self.status_var.set("Hiding data using append method...")
                append_embed(cover_path, payload, output_path)
            else:  # LSB method
                self.status_var.set("Hiding data using LSB method...")
                password = self.password_var.get() if self.encrypt_var.get() else None
                if password:
                    payload = encrypt_payload(payload, password)
                lsb_embed(cover_path, payload, output_path)
            
            self.hide_progress.set(1.0)
            self.status_var.set("Data hidden successfully!")
            
            messagebox.showinfo("Success", f"Data hidden successfully!\nStego image saved to: {output_path}")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to hide data: {str(e)}")
        finally:
            self.hide_progress.set(0)
    
    def extract_data(self):
        """Extract data from the selected stego image"""
        # Validate inputs
        if not self.stego_path_var.get():
            messagebox.showerror("Error", "Please select a stego image")
            return
        
        if not self.extract_output_var.get():
            messagebox.showerror("Error", "Please select output location")
            return
        
        # Run extraction operation in a separate thread
        threading.Thread(target=self._extract_data_thread, daemon=True).start()
    
    def _extract_data_thread(self):
        """Thread function for extracting data"""
        try:
            self.extract_progress.set(0.1)
            self.status_var.set("Loading stego image...")
            
            stego_path = self.stego_path_var.get()
            output_path = self.extract_output_var.get()
            password = self.extract_password_var.get() or None
            
            self.extract_progress.set(0.3)
            self.status_var.set("Detecting hidden data...")
            
            # Try both methods
            payload = None
            method_used = None
            
            try:
                payload = append_extract(stego_path)
                method_used = "append"
            except:
                try:
                    payload = lsb_extract(stego_path)
                    method_used = "lsb"
                except:
                    raise Exception("No hidden data found or corrupted data")
            
            self.extract_progress.set(0.6)
            self.status_var.set(f"Extracting data using {method_used} method...")
            
            # Decrypt if password provided
            if password and method_used == "lsb":
                try:
                    payload = decrypt_payload(payload, password)
                except:
                    raise Exception("Incorrect password or data not encrypted")
            
            self.extract_progress.set(0.8)
            self.status_var.set("Saving extracted data...")
            
            # Save extracted data
            with open(output_path, 'wb') as f:
                f.write(payload)
            
            self.extract_progress.set(1.0)
            self.status_var.set("Data extracted successfully!")
            
            messagebox.showinfo("Success", f"Data extracted successfully using {method_used} method!\nSaved to: {output_path}")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to extract data: {str(e)}")
        finally:
            self.extract_progress.set(0)

def main():
    """Main entry point for the GUI application"""
    app = StegoBoxGUI()
    app.mainloop()

if __name__ == "__main__":
    main()