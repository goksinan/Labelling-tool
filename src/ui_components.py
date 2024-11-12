import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path
from typing import Optional, Callable

class LabelingInterface:
    """Main UI component for the image labeling interface."""
    
    def __init__(self, root: tk.Tk, image_handler, label_manager):
        self.root = root
        self.image_handler = image_handler
        self.label_manager = label_manager
        self.current_photo = None  # Keep reference to prevent garbage collection
        self.label_var = tk.StringVar(value="0")  # Default to Live (0)
        self.setup_ui()
        self.bind_shortcuts()
        
    def setup_ui(self):
        """Create and arrange all UI elements."""
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Main container with padding
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights for resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Create UI sections
        self.create_header(main_container)
        self.create_image_display(main_container)
        self.create_controls(main_container)
        self.create_progress_display(main_container)
        
    def create_header(self, parent):
        """Create the header section with path information."""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.path_label = ttk.Label(header_frame, text="No image loaded")
        self.path_label.grid(row=0, column=0, sticky="w")
        
    def create_image_display(self, parent):
        """Create the main image display area."""
        # Canvas for image display with scrollbars
        self.canvas_frame = ttk.Frame(parent)
        self.canvas_frame.grid(row=1, column=0, sticky="nsew")
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="gray90")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        
    def create_controls(self, parent):
        """Create navigation and labeling controls."""
        controls_frame = ttk.Frame(parent)
        controls_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        
        # Contrast control
        contrast_frame = ttk.Frame(controls_frame)
        contrast_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Label(contrast_frame, text="Contrast:").grid(row=0, column=0, padx=(0, 5))
        self.contrast_scale = ttk.Scale(
            contrast_frame,
            from_=0,
            to=200,
            orient="horizontal",
            value=100,
            command=self.on_contrast_change
        )
        self.contrast_scale.grid(row=0, column=1, sticky="ew")
        
        # Navigation and labeling frame
        nav_frame = ttk.Frame(controls_frame)
        nav_frame.grid(row=1, column=0, sticky="ew")
        
        # Previous/Next buttons
        self.prev_btn = ttk.Button(nav_frame, text="Previous", command=self.on_previous)
        self.prev_btn.grid(row=0, column=0, padx=5)
        
        # Label radio buttons
        label_frame = ttk.LabelFrame(nav_frame, text="Image Label")
        label_frame.grid(row=0, column=1, padx=20)
        
        ttk.Radiobutton(
            label_frame,
            text="Live",
            value="0",  # Changed to 0 for Live
            variable=self.label_var,
            command=self.on_label_change
        ).grid(row=0, column=0, padx=10)
        
        ttk.Radiobutton(
            label_frame,
            text="Fake",
            value="1",  # Changed to 1 for Fake
            variable=self.label_var,
            command=self.on_label_change
        ).grid(row=0, column=1, padx=10)
        
        self.next_btn = ttk.Button(nav_frame, text="Next", command=self.on_next)
        self.next_btn.grid(row=0, column=2, padx=5)
        
        # Configure grid weights
        controls_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=1)
        contrast_frame.grid_columnconfigure(1, weight=1)
        
    def create_progress_display(self, parent):
        """Create the progress tracking display."""
        progress_frame = ttk.Frame(parent)
        progress_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        
        self.progress_label = ttk.Label(progress_frame, text="0/0 images labeled")
        self.progress_label.grid(row=0, column=0, sticky="w")
        
    def bind_shortcuts(self):
        """Bind keyboard shortcuts."""
        self.root.bind('<Left>', lambda e: self.on_previous())
        self.root.bind('<Right>', lambda e: self.on_next())
        self.root.bind('0', lambda e: self.label_var.set("0"))  # Live
        self.root.bind('1', lambda e: self.label_var.set("1"))  # Fake
        
    def update_display(self, image: Optional[Image.Image] = None):
        """Update the UI with current image and label information."""
        if image:
            # Convert PIL image to PhotoImage and keep reference
            # Calculate scaling factor to fit in canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:  # Ensure canvas has valid size
                # Calculate scale factor to fit image in canvas
                width_scale = canvas_width / image.width
                height_scale = canvas_height / image.height
                scale_factor = min(width_scale, height_scale)
                
                # Scale image if necessary
                if scale_factor < 1:
                    new_width = int(image.width * scale_factor)
                    new_height = int(image.height * scale_factor)
                    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            self.current_photo = ImageTk.PhotoImage(image)
            
            # Update canvas
            self.canvas.delete("all")
            self.canvas.create_image(
                canvas_width // 2,
                canvas_height // 2,
                anchor="center",
                image=self.current_photo
            )
            
            # Update scrollregion
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            # Update path label and load existing label
            current_path, parent_dir = self.image_handler.get_current_image_info()
            if current_path:
                self.path_label.configure(
                    text=f"Directory: {parent_dir}\nImage: {current_path.name}"
                )
                # Load existing label if any, defaults to "0" (Live)
                self.label_var.set(self.label_manager.get_label(current_path))
                # Auto-save default Live label
                self.label_manager.save_label(
                    current_path,
                    parent_dir,
                    self.label_var.get(),
                    auto_save=True
                )
        else:
            # Clear display if no image
            self.canvas.delete("all")
            self.path_label.configure(text="No image loaded")
            self.label_var.set("0")  # Default to Live
            
        # Update progress display
        labeled_count, total_count = self.label_manager.get_progress()
        self.progress_label.configure(text=f"{labeled_count}/{total_count} images labeled")
        
    def on_contrast_change(self, value):
        """Handle contrast slider changes."""
        if self.image_handler.current_image:
            adjusted_image = self.image_handler.adjust_contrast(float(value))
            if adjusted_image:
                self.update_display(adjusted_image)
                
    def on_previous(self):
        """Handle previous button click."""
        image, error = self.image_handler.previous_image()
        if image:
            self.update_display(image)
        elif error:
            self.show_error(error)
            
    def on_next(self):
        """Handle next button click."""
        image, error = self.image_handler.next_image()
        if image:
            self.update_display(image)
        elif error:
            self.show_error(error)
            
    def on_label_change(self):
        """Handle label selection change."""
        current_path, parent_dir = self.image_handler.get_current_image_info()
        if current_path and self.label_var.get():
            try:
                self.label_manager.save_label(
                    current_path,
                    parent_dir,
                    self.label_var.get()
                )
                self.update_display(self.image_handler.current_image)
            except RuntimeError as e:
                self.show_error(str(e))
                
    def show_error(self, message: str):
        """Display error message to user."""
        tk.messagebox.showerror("Error", message)