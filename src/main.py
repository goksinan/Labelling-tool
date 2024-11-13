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
        
    def setup(self):
        """Initialize minimal components and prompt for directory."""
        try:            
            # Show initial directory selection dialog
            self.prompt_directory_selection()
            
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize application: {str(e)}")
            self.root.destroy()
            raise

    def initialize_components(self, directory: str):
        """Initialize components after directory selection."""
        try:
            # Set CSV path in the selected directory
            csv_path = Path(directory) / "image_labels.csv"
            
            # Check if CSV exists and prompt user
            if csv_path.exists():
                proceed = messagebox.askquestion(
                    "Warning",
                    "image_labels.csv already exists in this directory. It will be modified. Do you want to proceed?",
                    icon='warning'
                )
                if proceed == 'no':
                    self.root.destroy()
                    return False
            
            # Initialize core components
            self.label_manager = LabelManager(csv_path)
            self.image_handler = ImageHandler()
            
            # Initialize UI after core components
            self.ui = LabelingInterface(self.root, self.image_handler, self.label_manager)

            # Create menu bar
            self.create_menu()

            # Configure window behavior
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.geometry("1024x768")
        
        except Exception as e:
            messagebox.showerror(
                "Initialization Error",
                f"Failed to initialize components: {str(e)}"
            )
            return False
            
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
        
    def prompt_directory_selection(self):
        """Show directory selection dialog and load images."""
        answer = messagebox.askquestion(
            "Select Directory",
            "Would you like to select a directory containing images to label?"
        )
        
        if answer == 'yes':
            self.open_directory()
        
    def open_directory(self):
        """Open directory selection dialog and load images from selected directory."""
        directory = filedialog.askdirectory(
            title="Select Image Directory",
            mustexist=True
        )
        
        # Initialize components
        self.initialize_components(directory)

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
            "2 Label as Uncertain\n"
            "3 Label as Other\n"
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