# Image Labeling Tool - Master Plan

## Overview
A Python-based GUI application for efficiently labeling images as "Live" or "Fake". The tool allows users to navigate through images in a directory structure, apply labels, and save them to a CSV file while maintaining the ability to review and modify previous labels.

## Core Features and Functionality

### Image Management
- Recursive directory scanning for all supported image formats
- Automatic tracking of labeled images
- Support for common image formats (jpg, jpeg, png, bmp, gif)
- Skip previously labeled images during normal navigation
- Progress tracking (e.g., "45/200 total images labeled")

### User Interface
- Main image display area with contrast adjustment slider
- Live/Fake checkbox selection
- Previous/Next navigation buttons
- Keyboard shortcuts (Left/Right arrow keys)
- Display of current image path and parent directory
- Progress indicator showing labeled/total images
- Warning display for corrupt/unsupported images

### Label Management
- CSV-based label storage with format: image_path,parent_directory,label
- Ability to view and modify existing labels
- Auto-selection of existing label when reviewing labeled images
- Real-time label saving when navigating between images

### Error Handling
- Display warnings for corrupt or unsupported images
- Allow skipping problematic files
- Clear error messages in the UI

## Technical Stack Recommendations

### GUI Framework
**Recommended: tkinter**
- Pros:
  - Built into Python standard library
  - Lightweight and suitable for simple interfaces
  - Cross-platform compatibility
- Cons:
  - Basic styling capabilities
  - Limited modern UI components

### Image Processing
**Recommended: Pillow (PIL)**
- Pros:
  - Extensive image format support
  - Built-in image manipulation capabilities
  - Efficient memory handling
- Cons:
  - Some advanced formats might require additional libraries

## Data Model

### File Structure
```
project_directory/
├── image_labels.csv
├── src/
│   ├── main.py
│   ├── image_handler.py
│   ├── ui_components.py
│   └── label_manager.py
```

### Label Storage Schema
```csv
parent_directory, image_name, label (0 or 1)
parent_dir, image.jpg, 0
```
