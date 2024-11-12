# Image Labeling Tool

A Python-based GUI application for efficiently labeling images as "Live" or "Fake". The tool provides an intuitive interface for navigating through images in a directory structure, applying labels, and saving them to a CSV file.

## Features

- Simple and efficient interface for image labeling
- Support for common image formats (jpg, jpeg, png, bmp, gif)
- Contrast adjustment for better image viewing
- Keyboard shortcuts for quick navigation and labeling
- Automatic progress tracking and label persistence
- CSV-based storage of image labels

## Requirements

- Python 3.8 or higher
- Poetry for dependency management
- Pillow (PIL) for image processing
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
poetry run label-images
```

2. Select a directory containing images when prompted
3. Use the interface to navigate and label images:
   - Click "Previous" or "Next" (or use ← → arrow keys)
   - Select "Live" or "Fake" (or use 1/0 keys)
   - Adjust contrast using the slider if needed

Labels are automatically saved to `image_labels.csv` in the project directory.

### Keyboard Shortcuts

- `←` Previous image
- `→` Next image
- `1` Label as Live
- `0` Label as Fake

## Output Format

The tool saves labels in a CSV file with the following columns:
- `image_path`: Full path to the image file
- `parent_directory`: Directory containing the image
- `label`: 1 for Live, 0 for Fake

## Project Structure

```
image-labeling-tool/
├── src/
│   ├── main.py           # Application entry point
│   ├── image_handler.py  # Image processing logic
│   ├── ui_components.py  # UI implementation
│   └── label_manager.py  # Label management
├── image_labels.csv      # Generated label storage
├── pyproject.toml        # Project dependencies
└── README.md            # This file
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.