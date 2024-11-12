from pathlib import Path
import csv
import os
from typing import Dict, Tuple, Optional, Union

class LabelManager:
    """Manages the storage and retrieval of image labels."""
    
    def __init__(self, csv_path: Union[str, Path]):
        """
        Initialize the LabelManager with a path to the CSV file.
        
        Args:
            csv_path: Path to the CSV file for storing labels
        """
        self.csv_path = Path(csv_path)
        self.labels: Dict[str, str] = {}  # Dictionary to cache labels
        self.load_labels()  # Load existing labels on initialization
        
    def load_labels(self) -> None:
        """
        Load existing labels from CSV file.
        Creates the CSV file if it doesn't exist.
        """
        self.labels.clear()
        
        # Create file if it doesn't exist
        if not self.csv_path.exists():
            self.csv_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['image_path', 'parent_directory', 'label'])
            return
            
        try:
            with open(self.csv_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Use image_path as key for quick lookup
                    if 'image_path' in row and 'label' in row:
                        self.labels[row['image_path']] = row['label']
        except (IOError, csv.Error) as e:
            raise RuntimeError(f"Error loading labels: {str(e)}")
            
    def save_label(self, image_path: Union[str, Path], parent_directory: Union[str, Path], 
                   label: Union[str, int]) -> None:
        """
        Save a new label or update existing label.
        
        Args:
            image_path: Path to the image file
            parent_directory: Parent directory of the image
            label: Label value (0 for Fake, 1 for Live)
            
        Raises:
            RuntimeError: If there's an error saving to the CSV file
        """
        image_path_str = str(Path(image_path))
        parent_dir_str = str(Path(parent_directory))
        label_str = str(label)
        
        # Update cache
        self.labels[image_path_str] = label_str
        
        # Read existing data
        existing_data = []
        try:
            with open(self.csv_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                existing_data = list(reader)
        except FileNotFoundError:
            pass  # File will be created
            
        # Update or add new entry
        updated = False
        for row in existing_data:
            if row['image_path'] == image_path_str:
                row.update({
                    'parent_directory': parent_dir_str,
                    'label': label_str
                })
                updated = True
                break
                
        if not updated:
            existing_data.append({
                'image_path': image_path_str,
                'parent_directory': parent_dir_str,
                'label': label_str
            })
            
        # Write back to CSV
        try:
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['image_path', 'parent_directory', 'label'])
                writer.writeheader()
                writer.writerows(existing_data)
        except (IOError, csv.Error) as e:
            raise RuntimeError(f"Error saving label: {str(e)}")
            
    def get_label(self, image_path: Union[str, Path]) -> Optional[str]:
        """
        Retrieve the label for a given image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Label string if found, None otherwise
        """
        return self.labels.get(str(Path(image_path)))
        
    def get_progress(self) -> Tuple[int, int]:
        """
        Return the current labeling progress.
        
        Returns:
            Tuple of (number of labeled images, total unique images)
        """
        labeled_count = len(self.labels)
        return labeled_count, labeled_count  # Total is same as labeled since we only track labeled images
        
    def get_all_labels(self) -> Dict[str, str]:
        """
        Get all labels currently stored.
        
        Returns:
            Dictionary mapping image paths to their labels
        """
        return self.labels.copy()