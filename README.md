# PyQt6 Image Viewer

A modern, cross-platform desktop application for viewing and manipulating images with advanced zoom and pan capabilities.

## Features

- **Image Loading**: Open images in common formats (PNG, JPG, JPEG, BMP, GIF, TIFF, WebP)
- **Zoom Controls**: Zoom in/out with buttons, mouse wheel, or keyboard shortcuts
- **Pan & Navigation**: Click and drag to pan around zoomed images
- **Responsive UI**: Automatically adjusts to window resizing
- **Drag & Drop**: Simply drag image files onto the application window
- **Cross-Platform**: Works on Windows, macOS, and Linux without code changes
- **Modern Interface**: Clean, intuitive toolbar and status bar

## Screenshots

The application features a clean interface with:
- Toolbar with Open, Zoom, and Fit controls
- Central image display area
- Status bar showing image information and zoom level
- Resizable window that adapts to content

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Install Dependencies
```bash
pip install -r requirements.txt
```

Or install PyQt6 directly:
```bash
pip install PyQt6
```

## Usage

### Running the Application
```bash
python image_viewer.py
```

### Opening Images
1. Click the "Open Image" button in the toolbar
2. Use the file dialog to select an image file
3. Or drag and drop an image file onto the application window

### Zoom Controls
- **Zoom In**: Click the zoom in button, use Ctrl++, or scroll up with mouse wheel
- **Zoom Out**: Click the zoom out button, use Ctrl+-, or scroll down with mouse wheel
- **Fit to View**: Click the fit button or use Ctrl+F to fit the entire image
- **Reset Zoom**: Click the reset button or use Ctrl+0 to return to 100% zoom

### Navigation
- **Pan**: Click and drag to move around when zoomed in
- **Scroll**: Use scroll bars when image is larger than the view

### Keyboard Shortcuts
- `Ctrl+O`: Open Image
- `Ctrl++`: Zoom In
- `Ctrl+-`: Zoom Out
- `Ctrl+F`: Fit to View
- `Ctrl+0`: Reset Zoom

## Supported Image Formats

- PNG (Portable Network Graphics)
- JPG/JPEG (Joint Photographic Experts Group)
- BMP (Bitmap)
- GIF (Graphics Interchange Format)
- TIFF (Tagged Image File Format)
- WebP (Web Picture format)

## Technical Details

### Architecture
- **Main Window**: `ImageViewerApp` class inheriting from `QMainWindow`
- **Graphics View**: Custom `ImageGraphicsView` class for zoom/pan functionality
- **Scene Management**: `QGraphicsScene` with `QGraphicsPixmapItem` for image display
- **Transform Handling**: `QTransform` for smooth scaling and zooming

### Key Components
- **Toolbar**: Quick access to common functions
- **Status Bar**: Real-time image information and zoom level display
- **Graphics View**: High-performance image rendering with smooth zooming
- **Event Handling**: Mouse wheel zoom, drag & drop, window resize events

### Performance Features
- Smooth pixmap transformation with `SmoothPixmapTransform`
- Efficient viewport updates
- Optimized zoom calculations
- Memory-efficient image handling

## Development

### Project Structure
```
image_viewer/
├── image_viewer.py      # Main application file
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Code Quality
- Comprehensive docstrings for all classes and methods
- Clear separation of concerns between UI and logic
- Error handling for file operations
- Cross-platform compatibility considerations

### Extending the Application
The modular design makes it easy to add new features:
- Add new image processing tools
- Implement image filters or effects
- Add support for additional file formats
- Create custom zoom behaviors

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'PyQt6'"**
- Solution: Install PyQt6 with `pip install PyQt6`

**Images not loading properly**
- Check file format support
- Ensure file permissions allow reading
- Verify image file integrity

**Performance issues with large images**
- The application automatically optimizes rendering
- Very large images (>100MP) may require more memory

**Zoom not working as expected**
- Ensure mouse wheel is functional
- Check that the image is properly loaded
- Try using the toolbar buttons instead

### Platform-Specific Notes

**Windows**
- Tested on Windows 10/11
- Works with both mouse and touch input

**macOS**
- Native macOS appearance and behavior
- Supports trackpad gestures

**Linux**
- Compatible with major desktop environments
- GTK and KDE themes are respected

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## Version History

- **v1.0**: Initial release with core image viewing, zoom, and pan functionality
