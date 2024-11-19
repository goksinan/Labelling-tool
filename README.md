# Image Labeling Tool

A Python-based GUI application for efficiently labeling images. The tool provides an intuitive interface for navigating through images in a directory structure, applying labels, and saving them to a CSV file.

## Features

- Simple and efficient interface for image labeling
- Support for multiple label categories:
  - Live (0)
  - Fake (1)
  - Soft (2)
  - Hard (3)
  - Uncertain (4)
  - Other (5)
- Support for common image formats (jpg, jpeg, jp2, png, bmp, gif)
- Image enhancement features:
  - Contrast adjustment
  - CLAHE enhancement
  - Unsharp masking
  - FFT visualization
- Two operational modes:
  - Directory scanning for new labeling
  - Review mode for existing labels
- Image metrics display (Lens Score, Focus, Visibility)
- Keyboard shortcuts for quick navigation and labeling
- Automatic progress tracking and label persistence
- CSV-based storage of image labels and metrics

## Requirements

- Python 3.8 or higher
- Poetry for dependency management
- Required packages:
  - Pillow (PIL)
  - OpenCV (cv2)
  - tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/image-labeling-tool.git
cd image-labeling-tool
```

2. Install dependencies using Poetry:
```bash
poetry install
```

## Usage

1. Start the application:
```bash
poetry shell
python src/main.py
```

2. Select a directory containing images when prompted
3. Use the interface to navigate and label images:
   - Use navigation buttons or keyboard shortcuts
   - Select label using radio buttons or keyboard shortcuts
   - Adjust contrast using the slider
   - Toggle between original and enhanced views

Labels are automatically saved to `image_labels.csv` in the project directory.

### Keyboard Shortcuts

- `←` Previous image
- `→` Next image
- `0` Label as Live
- `1` Label as Fake
- `2` Label as Soft
- `3` Label as Hard
- `4` Label as Uncertain
- `5` Label as Other
- `O` Show Original image
- `E` Show Enhanced image
- `F` Show FFT visualization

## Output Format

The tool uses two CSV files:
- `image_labels.csv`: Stores image labels with columns:
  - `image_path`: Full path to the image file
  - `label`: Label value (0: Live, 1: Fake, 2: Soft, 3: Hard, 4: Uncertain, 5: Other)
- `image_info.csv`: Stores image metrics with columns:
  - `file_name`: Name of the image file
  - `lens_score`: Numerical score for lens quality
  - `focus`: Focus quality metric
  - `visibility`: Visibility metric

## Project Structure

```
image-labeling-tool/
├── src/
│   ├── main.py           # Application entry point
│   ├── image_handler.py  # Image processing and navigation
│   ├── ui_components.py  # UI implementation
│   └── label_manager.py  # Label storage and management
├── image_labels.csv      # Label storage
├── image_info.csv        # Image metrics storage
├── pyproject.toml        # Project dependencies
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.