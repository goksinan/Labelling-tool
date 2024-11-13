import os
from pathlib import Path
from PIL import Image, ImageEnhance
from typing import List, Optional, Tuple, Set
import cv2
import numpy as np

class ImageHandler:
    """Handles image loading, processing, and navigation through the image directory."""
    
    SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.jp2', '.png', '.bmp', '.gif')
    
    def __init__(self):
        self.current_image: Optional[Image.Image] = None
        self.original_image: Optional[Image.Image] = None  # Store original for contrast adjustments
        self.image_paths: List[Path] = []
        self.current_index: int = -1
        self.labeled_images: Set[str] = set()  # Track labeled images
        
    def scan_directory(self, directory_path: str, labeled_paths: Set[str]) -> int:
        """
        Scan directory recursively for supported image files.
        
        Args:
            directory_path: Path to the directory to scan
            labeled_paths: Set of paths that have already been labeled
            
        Returns:
            Number of image files found
            
        Raises:
            FileNotFoundError: If directory doesn't exist
            PermissionError: If directory is not accessible
        """
        self.image_paths = []
        self.current_index = -1
        self.labeled_images = labeled_paths
        
        try:
            for root, _, files in os.walk(directory_path):
                for file in files:
                    if file.lower().endswith(self.SUPPORTED_FORMATS):
                        self.image_paths.append(Path(root) / file)
        except (FileNotFoundError, PermissionError) as e:
            raise e
            
        # Sort paths for consistent ordering
        self.image_paths.sort()
        
        # Find the first unlabeled image
        for i, path in enumerate(self.image_paths):
            if str(path) not in self.labeled_images:
                self.current_index = i - 1  # Set to one before so next_image() will land on it
                break
        else:
            # If all images are labeled, start from the beginning
            self.current_index = -1
            
        return len(self.image_paths)
        
    def load_image(self, image_path: Optional[Path] = None) -> Tuple[Optional[Image.Image], str]:
        """
        Load an image file and prepare it for display.
        
        Args:
            image_path: Optional specific path to load, otherwise uses current_index
            
        Returns:
            Tuple of (PIL Image object or None, error message or empty string)
            
        Note:
            Returns None, error_message if image loading fails
        """
        if image_path:
            path_to_load = image_path
        elif 0 <= self.current_index < len(self.image_paths):
            path_to_load = self.image_paths[self.current_index]
        else:
            return None, "No valid image path specified"
            
        try:
            # Load and convert to RGB to ensure consistency
            self.original_image = Image.open(path_to_load).convert('RGB')
            self.current_image = self.original_image.copy()
            return self.current_image, ""
        except (IOError, OSError) as e:
            return None, f"Error loading image: {str(e)}"
            
    def adjust_contrast(self, value: float) -> Optional[Image.Image]:
        """
        Adjust the contrast of the current image.
        
        Args:
            value: Contrast value (0-200, where 100 is normal)
            
        Returns:
            Adjusted PIL Image object or None if no image is loaded
        """
        if self.original_image is None:
            return None
            
        # Convert slider value to contrast factor (0-2)
        contrast_factor = max(0, value) / 100
        
        # Apply contrast adjustment to original image
        enhancer = ImageEnhance.Contrast(self.original_image)
        self.current_image = enhancer.enhance(contrast_factor)
        return self.current_image
        
    def next_image(self) -> Tuple[Optional[Image.Image], str]:
        """
        Navigate to the next image in the sequence.
        
        Returns:
            Tuple of (PIL Image object or None, error message or empty string)
        """
        if not self.image_paths:
            return None, "No images in directory"
            
        self.current_index = (self.current_index + 1) % len(self.image_paths)
        return self.load_image()
        
    def previous_image(self) -> Tuple[Optional[Image.Image], str]:
        """
        Navigate to the previous image in the sequence.
        
        Returns:
            Tuple of (PIL Image object or None, error message or empty string)
        """
        if not self.image_paths:
            return None, "No images in directory"
            
        self.current_index = (self.current_index - 1) % len(self.image_paths)
        return self.load_image()
    
    def get_current_image_info(self) -> Tuple[Optional[Path], Optional[Path]]:
        """
        Get the current image path and its parent directory.
        
        Returns:
            Tuple of (current image path or None, parent directory path or None)
        """
        if 0 <= self.current_index < len(self.image_paths):
            current_path = self.image_paths[self.current_index]
            return current_path, current_path.parent
        return None, None
    
    def get_progress(self) -> Tuple[int, int]:
        """
        Get the current progress through the image set.
        
        Returns:
            Tuple of (current index + 1, total number of images)
        """
        return self.current_index + 1, len(self.image_paths)
    
    def enhance_image(self) -> Optional[Image.Image]:
        """
        Enhance image using CLAHE and unsharp masking.
        """
        if self.original_image is None:
            return None
            
        # Convert PIL to CV2 format
        img_cv = cv2.cvtColor(np.array(self.original_image), cv2.COLOR_RGB2LAB)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img_cv[:,:,0] = clahe.apply(img_cv[:,:,0])
        
        # Convert back to RGB
        enhanced = cv2.cvtColor(img_cv, cv2.COLOR_LAB2RGB)
        
        # Apply unsharp masking
        gaussian = cv2.GaussianBlur(enhanced, (0,0), 2.0)
        unsharp_mask = cv2.addWeighted(enhanced, 1.5, gaussian, -0.5, 0)
        
        # Convert back to PIL
        return Image.fromarray(unsharp_mask)