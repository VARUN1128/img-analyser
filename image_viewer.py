
import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
                             QGraphicsPixmapItem, QVBoxLayout, QHBoxLayout, QWidget,
                             QPushButton, QFileDialog, QLabel, QStatusBar, QToolBar,
                             QMessageBox)
from PyQt6.QtCore import Qt, QRectF, QPointF, QSize
from PyQt6.QtGui import QPixmap, QTransform, QPainter, QDragEnterEvent, QDropEvent, QAction
from PyQt6.QtWidgets import QGraphicsView


class ImageGraphicsView(QGraphicsView):
    """
    Custom QGraphicsView that handles mouse wheel zooming and panning.
    Inherits from QGraphicsView to add custom zoom and pan functionality.
    """
    
    def __init__(self, parent=None):
        """Initialize the custom graphics view with zoom and pan capabilities."""
        super().__init__(parent)
        
        # Set up the view properties
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        
        # Initialize zoom level
        self.zoom_factor = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 10.0
        
        # Enable mouse tracking for better interaction
        self.setMouseTracking(True)
    
    def wheelEvent(self, event):
        """
        Handle mouse wheel events for zooming in and out.
        
        Args:
            event: The mouse wheel event containing delta and position information
        """
        # Get the zoom factor from the wheel delta
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor
        
        # Determine zoom direction based on wheel delta
        if event.angleDelta().y() > 0:
            # Zoom in
            factor = zoom_in_factor
        else:
            # Zoom out
            factor = zoom_out_factor
        
        # Calculate new zoom level
        new_zoom = self.zoom_factor * factor
        
        # Clamp zoom level to min/max bounds
        if self.min_zoom <= new_zoom <= self.max_zoom:
            self.zoom_factor = new_zoom
            
            # Apply zoom transformation
            transform = QTransform()
            transform.scale(self.zoom_factor, self.zoom_factor)
            self.setTransform(transform)
            
            # Emit zoom changed signal if parent has the method
            if hasattr(self.parent(), 'update_zoom_label'):
                self.parent().update_zoom_label()
    
    def fitInView(self, rect, mode=Qt.AspectRatioMode.KeepAspectRatio):
        """
        Fit the entire scene in the view while maintaining aspect ratio.
        
        Args:
            rect: The rectangle to fit in the view
            mode: The aspect ratio mode to use
        """
        # Reset zoom factor
        self.zoom_factor = 1.0
        
        # Get the viewport size
        viewport_size = self.viewport().size()
        
        # Calculate the scale factors
        scale_x = viewport_size.width() / rect.width()
        scale_y = viewport_size.height() / rect.height()
        
        # Use the smaller scale to fit the entire image
        scale = min(scale_x, scale_y)
        
        # Apply the transformation
        transform = QTransform()
        transform.scale(scale, scale)
        self.setTransform(transform)
        
        # Update zoom factor
        self.zoom_factor = scale
        
        # Center the image in the view
        self.centerOn(rect.center())
        
        # Emit zoom changed signal if parent has the method
        if hasattr(self.parent(), 'update_zoom_label'):
            self.parent().update_zoom_label()


class ImageViewerApp(QMainWindow):
    """
    Main application window for the Image Viewer.
    Contains the menu bar, toolbar, image display area, and status bar.
    """
    
    def __init__(self):
        """Initialize the main application window and set up the UI."""
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Image Viewer - PyQt6")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(400, 300)
        
        # Initialize variables
        self.current_image_path = None
        self.original_pixmap = None
        self.graphics_item = None
        
        # Set up the UI components
        self.setup_ui()
        self.setup_actions()
        self.setup_toolbar()
        self.setup_status_bar()
        
        # Set up the central widget
        self.setup_central_widget()
        
        # Enable drag and drop for images
        self.setAcceptDrops(True)
    
    def setup_ui(self):
        """Set up the main UI components and layout."""
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
    
    def setup_actions(self):
        """Create and set up the application actions."""
        # Open Image action
        self.open_action = QAction("Open Image", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.setStatusTip("Open an image file")
        self.open_action.triggered.connect(self.open_image)
        
        # Zoom In action
        self.zoom_in_action = QAction("Zoom In", self)
        self.zoom_in_action.setShortcut("Ctrl++")
        self.zoom_in_action.setStatusTip("Zoom in on the image")
        self.zoom_in_action.triggered.connect(self.zoom_in)
        
        # Zoom Out action
        self.zoom_out_action = QAction("Zoom Out", self)
        self.zoom_out_action.setShortcut("Ctrl+-")
        self.zoom_out_action.setStatusTip("Zoom out from the image")
        self.zoom_out_action.triggered.connect(self.zoom_out)
        
        # Fit to View action
        self.fit_action = QAction("Fit to View", self)
        self.fit_action.setShortcut("Ctrl+F")
        self.fit_action.setStatusTip("Fit the image to the current view")
        self.fit_action.triggered.connect(self.fit_to_view)
        
        # Reset Zoom action
        self.reset_zoom_action = QAction("Reset Zoom", self)
        self.reset_zoom_action.setShortcut("Ctrl+0")
        self.reset_zoom_action.setStatusTip("Reset zoom to 100%")
        self.reset_zoom_action.triggered.connect(self.reset_zoom)
    
    def setup_toolbar(self):
        """Create and set up the toolbar with action buttons."""
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        
        # Add actions to toolbar
        self.toolbar.addAction(self.open_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.zoom_in_action)
        self.toolbar.addAction(self.zoom_out_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.fit_action)
        self.toolbar.addAction(self.reset_zoom_action)
    
    def setup_status_bar(self):
        """Set up the status bar to display image information and zoom level."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Create status labels
        self.image_info_label = QLabel("No image loaded")
        self.zoom_label = QLabel("Zoom: 100%")
        
        # Add labels to status bar
        self.status_bar.addWidget(self.image_info_label)
        self.status_bar.addPermanentWidget(self.zoom_label)
    
    def setup_central_widget(self):
        """Set up the central widget containing the image display area."""
        # Create graphics scene and view
        self.scene = QGraphicsScene()
        self.view = ImageGraphicsView(self)
        self.view.setScene(self.scene)
        
        # Add the view to the main layout
        self.main_layout.addWidget(self.view)
    
    def open_image(self):
        """
        Open a file dialog to select and load an image.
        Supports common image formats like PNG, JPG, BMP, etc.
        """
        # Open file dialog for image selection
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp);;All Files (*)"
        )
        
        if file_path:
            self.load_image(file_path)
    
    def load_image(self, file_path):
        """
        Load an image from the specified file path and display it.
        
        Args:
            file_path (str): Path to the image file to load
        """
        try:
            # Load the pixmap from file
            pixmap = QPixmap(file_path)
            
            if pixmap.isNull():
                QMessageBox.critical(self, "Error", f"Failed to load image: {file_path}")
                return
            
            # Store the original pixmap and file path
            self.original_pixmap = pixmap
            self.current_image_path = file_path
            
            # Clear the current scene
            self.scene.clear()
            
            # Create a graphics item for the image
            self.graphics_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.graphics_item)
            
            # Set the scene rectangle to match the image
            self.scene.setSceneRect(QRectF(pixmap.rect()))
            
            # Reset zoom and fit image to view
            self.reset_zoom()
            self.fit_to_view()
            
            # Update status bar with image information
            self.update_image_info()
            
            # Update window title
            filename = os.path.basename(file_path)
            self.setWindowTitle(f"Image Viewer - {filename}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading image: {str(e)}")
    
    def update_image_info(self):
        """Update the status bar with current image information."""
        if self.original_pixmap:
            width = self.original_pixmap.width()
            height = self.original_pixmap.height()
            size_mb = os.path.getsize(self.current_image_path) / (1024 * 1024)
            
            info_text = f"Image: {width}x{height} pixels, {size_mb:.1f} MB"
            self.image_info_label.setText(info_text)
        else:
            self.image_info_label.setText("No image loaded")
    
    def update_zoom_label(self):
        """Update the zoom label in the status bar."""
        zoom_percentage = int(self.view.zoom_factor * 100)
        self.zoom_label.setText(f"Zoom: {zoom_percentage}%")
    
    def zoom_in(self):
        """Zoom in on the image by increasing the zoom factor."""
        current_zoom = self.view.zoom_factor
        new_zoom = min(current_zoom * 1.25, self.view.max_zoom)
        
        if new_zoom != current_zoom:
            self.view.zoom_factor = new_zoom
            transform = QTransform()
            transform.scale(new_zoom, new_zoom)
            self.view.setTransform(transform)
            self.update_zoom_label()
    
    def zoom_out(self):
        """Zoom out from the image by decreasing the zoom factor."""
        current_zoom = self.view.zoom_factor
        new_zoom = max(current_zoom / 1.25, self.view.min_zoom)
        
        if new_zoom != current_zoom:
            self.view.zoom_factor = new_zoom
            transform = QTransform()
            transform.scale(new_zoom, new_zoom)
            self.view.setTransform(transform)
            self.update_zoom_label()
    
    def fit_to_view(self):
        """Fit the entire image in the current view while maintaining aspect ratio."""
        if self.original_pixmap:
            self.view.fitInView(self.scene.sceneRect())
    
    def reset_zoom(self):
        """Reset the zoom level to 100% (original size)."""
        if self.original_pixmap:
            self.view.zoom_factor = 1.0
            transform = QTransform()
            transform.scale(1.0, 1.0)
            self.view.setTransform(transform)
            self.update_zoom_label()
    
    def resizeEvent(self, event):
        """
        Handle window resize events to automatically fit the image to the new view size.
        
        Args:
            event: The resize event containing the new size information
        """
        super().resizeEvent(event)
        
        # If there's an image loaded, fit it to the new view size
        if self.original_pixmap and self.graphics_item:
            # Use a timer to delay the fit operation until the resize is complete
            QApplication.processEvents()
            self.fit_to_view()
    
    def dragEnterEvent(self, event):
        """
        Handle drag enter events to accept image files.
        
        Args:
            event: The drag enter event
        """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        """
        Handle drop events to load dropped image files.
        
        Args:
            event: The drop event containing the dropped file information
        """
        urls = event.mimeData().urls()
        if urls:
            # Get the first dropped file
            file_path = urls[0].toLocalFile()
            
            # Check if it's an image file
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
                self.load_image(file_path)
            else:
                QMessageBox.warning(self, "Invalid File", "Please drop an image file.")


def main():
    """
    Main entry point of the application.
    Creates and runs the Image Viewer application.
    """
    # Create the Qt application
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Image Viewer")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("PyQt6 Image Viewer")
    
    # Create and show the main window
    viewer = ImageViewerApp()
    viewer.show()
    
    # Start the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
