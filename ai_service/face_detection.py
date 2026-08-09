"""Face detection module using OpenCV."""
import cv2
import os
import logging

logger = logging.getLogger(__name__)


class FaceDetector:
    """Face detection using Haar Cascade."""
    
    def __init__(self, cascade_path=None):
        """Initialize face detector."""
        if cascade_path is None:
            cascade_path = os.path.join(
                os.path.dirname(__file__), 
                '..', 
                'models', 
                'haarcascade_frontalface_default.xml'
            )
        
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            raise ValueError(f"Failed to load Haar Cascade from {cascade_path}")
        
        logger.info("Face detector initialized successfully")
    
    def detect_faces(self, image, scale_factor=1.3, min_neighbors=5):
        """
        Detect faces in an image.
        
        Args:
            image: Image array (BGR format)
            scale_factor: Parameter specifying how much the image size is reduced
            min_neighbors: Parameter specifying how many neighbors each candidate rectangle should have
        
        Returns:
            List of face rectangles [(x, y, w, h), ...]
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray, 
                scaleFactor=scale_factor, 
                minNeighbors=min_neighbors
            )
            
            logger.info(f"Detected {len(faces)} face(s)")
            return faces
        
        except Exception as e:
            logger.error(f"Error detecting faces: {str(e)}")
            return []
    
    def draw_faces(self, image, faces, color=(255, 0, 0), thickness=2):
        """
        Draw rectangles around detected faces.
        
        Args:
            image: Image array
            faces: List of face rectangles
            color: Rectangle color (BGR)
            thickness: Rectangle thickness
        
        Returns:
            Image with drawn rectangles
        """
        image_copy = image.copy()
        
        for (x, y, w, h) in faces:
            cv2.rectangle(image_copy, (x, y), (x + w, y + h), color, thickness)
        
        return image_copy
    
    def get_largest_face(self, faces):
        """
        Get the largest face from detected faces.
        
        Args:
            faces: List of face rectangles
        
        Returns:
            Largest face rectangle or None
        """
        if len(faces) == 0:
            return None
        
        # Calculate area for each face
        areas = [w * h for (x, y, w, h) in faces]
        
        # Get index of largest face
        largest_idx = areas.index(max(areas))
        
        return faces[largest_idx]
    
    def crop_face(self, image, face_rect, padding=20):
        """
        Crop face region from image with padding.
        
        Args:
            image: Image array
            face_rect: Face rectangle (x, y, w, h)
            padding: Padding around face
        
        Returns:
            Cropped face image
        """
        x, y, w, h = face_rect
        
        # Add padding
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(image.shape[1], x + w + padding)
        y2 = min(image.shape[0], y + h + padding)
        
        return image[y1:y2, x1:x2]
