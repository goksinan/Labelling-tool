import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from image_handler import ImageHandler
from ui_components import LabelingInterface
from label_manager import LabelManager

class ImageLabelingApp:
    """Main application class for the Image Labeling Tool."""
    
    def __init__(self):
        """Initialize the application and set up the main window."""
        self.root = tk.Tk()
        self.root.title("Image Labeling Tool")
        
        # Initialize components as None
        self.label_manager = None
        self.image_handler = None
        self.ui = None
        
        # Set CSV path one level up from src directory
        self.default_csv_path = Path(__file__).parent.parent / "image_labels.csv"
        self.default_csv_path_info = Path(__file__).parent.parent / "image_info.csv"
        
    def setup(self):
        """Initialize all components and setup the main application."""
        try:
            # Check if CSV file exists
            if not self.default_csv_path.exists():
                messagebox.showerror(
                    "Error",
                    f"No existing labels file found at {self.default_csv_path}"
                )
                self.root.destroy()
                return False

            # Initialize core components
            self.label_manager = LabelManager(self.default_csv_path)
            self.image_handler = ImageHandler(self.default_csv_path_info)
            
            # Initialize UI after core components
            self.ui = LabelingInterface(self.root, self.image_handler, self.label_manager)
            
            # Create menu bar
            self.create_menu()
            
            # Configure window behavior
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.geometry("1024x768")
            
            # Show mode selection dialog
            self.prompt_mode_selection()
            
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize application: {str(e)}")
            self.root.destroy()
            raise
            
    def create_menu(self):
        """Create the application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Directory...", command=self.open_directory)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def prompt_mode_selection(self):
        """Show dialog to choose between directory mode and review mode."""
        answer = messagebox.askquestion(
            "Select Mode",
            "Would you like to open a new directory for labeling?\n\n"
            "Select 'Yes' to choose a directory.\n"
            "Select 'No' to review existing labeled images."
        )
        
        if answer == 'yes':
            self.open_directory()
        else:
            self.review_labeled_images()

    def review_labeled_images(self):
        """Show dialog to select label for review and load matching images."""
        # Create dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Label to Review")
        dialog.geometry("300x300")
        dialog.transient(self.root)
        dialog.grab_set()

        # Create label selection
        tk.Label(dialog, text="Select label to review:").pack(pady=10)
        
        label_var = tk.StringVar(value="0")
        labels = [
            ("Live", "0"),
            ("Fake", "1"),
            ("Soft", "2"),
            ("Hard", "3"),
            ("Uncertain", "4"),
            ("Other", "5")
        ]
        
        for text, value in labels:
            tk.Radiobutton(
                dialog,
                text=text,
                value=value,
                variable=label_var
            ).pack()

        def on_confirm():
            target_label = label_var.get()
            dialog.destroy()
            
            # Get all labeled images and filter for target label
            labeled_paths = self.label_manager.get_all_labels()
            image_count = self.image_handler.scan_labeled_images(labeled_paths, target_label)
            
            if image_count == 0:
                messagebox.showwarning(
                    "No Images Found",
                    f"No images found with label '{target_label}'"
                )
                self.prompt_mode_selection()
                return
                
            # Load first image
            image, error = self.image_handler.next_image()
            if error:
                messagebox.showerror("Error", error)
            elif image:
                self.ui.update_display(image)

        tk.Button(
            dialog,
            text="Confirm",
            command=on_confirm
        ).pack(pady=20)
        
    def open_directory(self):
        """Open directory selection dialog and load images from selected directory."""
        directory = filedialog.askdirectory(
            title="Select Image Directory",
            mustexist=True
        )
        
        if directory:
            try:
                # Scan directory for images
                labeled_paths = self.label_manager.get_labeled_paths()
                image_count = self.image_handler.scan_directory(directory, labeled_paths)
                
                if image_count == 0:
                    messagebox.showwarning(
                        "No Images Found",
                        "No supported image files found in the selected directory."
                    )
                    return
                    
                # Load first image
                image, error = self.image_handler.next_image()
                if error:
                    messagebox.showerror("Error", error)
                elif image:
                    self.ui.update_display(image)
                    
            except Exception as e:
                messagebox.showerror(
                    "Directory Error",
                    f"Error loading directory: {str(e)}"
                )
                
    def show_about(self):
        """Show about dialog with application information."""
        messagebox.showinfo(
            "About Image Labeling Tool",
            "Image Labeling Tool\n\n"
            "A tool for efficiently labeling images as Live or Fake.\n\n"
            "Keyboard Shortcuts:\n"
            "← Previous Image\n"
            "→ Next Image\n"
            "0 Label as Live\n"
            "1 Label as Fake\n"
            "2 Label as Soft\n"
            "3 Label as Hard\n"
            "4 Label as Uncertain\n"
            "5 Label as Other\n"
            "O Show Original Image\n"
            "E Show Enhanced Image"
        )
        
    def on_closing(self):
        """Handle application closing."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            
    def run(self):
        """Start the application main loop."""
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageLabelingApp()
    try:
        app.setup()
        app.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}")