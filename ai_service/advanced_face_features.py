"""Advanced face feature extraction for enhanced recognition accuracy."""
import cv2
import numpy as np
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class AdvancedFaceFeatureExtractor:
    """Extract detailed facial features for high-accuracy recognition."""
    
    def __init__(self):
        """Initialize feature extractors."""
        # Load cascade classifiers
        cascade_path = cv2.data.haarcascades
        
        self.face_cascade = cv2.CascadeClassifier(cascade_path + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cascade_path + 'haarcascade_eye.xml')
        
        logger.info("Advanced face feature extractor initialized")
    
    def extract_all_features(self, image) -> Optional[Dict]:
        """
        Extract comprehensive facial features.
        
        Args:
            image: Grayscale face image (normalized)
        
        Returns:
            Dictionary of features or None if extraction fails
        """
        try:
            features = {}
            
            # 1. Face structure features
            features['face_structure'] = self._extract_face_structure(image)
            
            # 2. Eye features (color, shape, position)
            features['eyes'] = self._extract_eye_features(image)
            
            # 3. Eyebrow features
            features['eyebrows'] = self._extract_eyebrow_features(image)
            
            # 4. Hair features (color, texture)
            features['hair'] = self._extract_hair_features(image)
            
            # 5. Skin tone features
            features['skin_tone'] = self._extract_skin_tone(image)
            
            # 6. Facial proportions
            features['proportions'] = self._extract_facial_proportions(image)
            
            # 7. Texture patterns
            features['texture'] = self._extract_texture_patterns(image)
            
            return features
        
        except Exception as e:
            logger.error(f"Error extracting advanced features: {str(e)}")
            return None
    
    def _extract_face_structure(self, image) -> np.ndarray:
        """
        Extract face structure features.
        
        Captures:
        - Face shape (oval, round, square)
        - Jawline characteristics
        - Cheekbone prominence
        - Face width-to-height ratio
        """
        h, w = image.shape
        features = []
        
        # 1. Aspect ratio (face shape indicator)
        aspect_ratio = w / h
        features.append(aspect_ratio)
        
        # 2. Face contour analysis using edge detection
        edges = cv2.Canny(image, 50, 150)
        
        # Analyze edges in different regions
        # Upper face (forehead)
        upper_edges = edges[:h//3, :]
        features.append(np.mean(upper_edges))
        features.append(np.std(upper_edges))
        
        # Middle face (cheeks, nose)
        middle_edges = edges[h//3:2*h//3, :]
        features.append(np.mean(middle_edges))
        features.append(np.std(middle_edges))
        
        # Lower face (jaw, chin)
        lower_edges = edges[2*h//3:, :]
        features.append(np.mean(lower_edges))
        features.append(np.std(lower_edges))
        
        # 3. Jawline sharpness (bottom 20% of face)
        jaw_region = image[int(0.8*h):, :]
        jaw_gradient_x = cv2.Sobel(jaw_region, cv2.CV_64F, 1, 0, ksize=3)
        jaw_gradient_y = cv2.Sobel(jaw_region, cv2.CV_64F, 0, 1, ksize=3)
        jaw_magnitude = np.sqrt(jaw_gradient_x**2 + jaw_gradient_y**2)
        features.append(np.mean(jaw_magnitude))
        features.append(np.std(jaw_magnitude))
        
        # 4. Cheekbone analysis (middle-upper face)
        cheek_region = image[int(0.3*h):int(0.6*h), :]
        features.append(np.mean(cheek_region))
        features.append(np.std(cheek_region))
        
        # 5. Face symmetry (compare left and right halves)
        left_half = image[:, :w//2]
        right_half = cv2.flip(image[:, w//2:], 1)
        
        # Resize to same size if needed
        if left_half.shape != right_half.shape:
            min_w = min(left_half.shape[1], right_half.shape[1])
            left_half = left_half[:, :min_w]
            right_half = right_half[:, :min_w]
        
        symmetry_diff = np.mean(np.abs(left_half.astype(float) - right_half.astype(float)))
        features.append(symmetry_diff)
        
        return np.array(features)
    
    def _extract_eye_features(self, image) -> np.ndarray:
        """
        Extract eye features.
        
        Captures:
        - Eye color (brightness in eye region)
        - Eye shape (width-to-height ratio)
        - Eye size relative to face
        - Inter-eye distance
        - Eye position
        """
        h, w = image.shape
        features = []
        
        # Detect eyes
        eyes = self.eye_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
        
        if len(eyes) >= 2:
            # Sort eyes by x-coordinate (left to right)
            eyes = sorted(eyes, key=lambda e: e[0])
            
            # Take first two eyes
            left_eye = eyes[0]
            right_eye = eyes[1]
            
            # Extract features for each eye
            for eye in [left_eye, right_eye]:
                ex, ey, ew, eh = eye
                eye_region = image[ey:ey+eh, ex:ex+ew]
                
                if eye_region.size > 0:
                    # Eye color (average brightness)
                    eye_brightness = np.mean(eye_region)
                    features.append(eye_brightness)
                    
                    # Eye shape (aspect ratio)
                    eye_aspect_ratio = ew / eh
                    features.append(eye_aspect_ratio)
                    
                    # Eye size relative to face
                    eye_size_ratio = (ew * eh) / (w * h)
                    features.append(eye_size_ratio)
                    
                    # Eye texture (standard deviation)
                    features.append(np.std(eye_region))
                    
                    # Iris region (center of eye)
                    iris_y1 = ey + eh//4
                    iris_y2 = ey + 3*eh//4
                    iris_x1 = ex + ew//4
                    iris_x2 = ex + 3*ew//4
                    iris_region = image[iris_y1:iris_y2, iris_x1:iris_x2]
                    
                    if iris_region.size > 0:
                        # Iris brightness (eye color indicator)
                        iris_brightness = np.mean(iris_region)
                        features.append(iris_brightness)
                        
                        # Iris contrast
                        iris_contrast = np.std(iris_region)
                        features.append(iris_contrast)
            
            # Inter-eye distance
            left_center_x = left_eye[0] + left_eye[2]//2
            right_center_x = right_eye[0] + right_eye[2]//2
            inter_eye_distance = (right_center_x - left_center_x) / w
            features.append(inter_eye_distance)
            
            # Eye vertical position
            avg_eye_y = (left_eye[1] + right_eye[1]) / 2
            eye_vertical_position = avg_eye_y / h
            features.append(eye_vertical_position)
        
        else:
            # If eyes not detected, use approximate regions
            # Left eye region (approximate)
            left_eye_region = image[int(0.25*h):int(0.4*h), int(0.2*w):int(0.4*w)]
            if left_eye_region.size > 0:
                features.append(np.mean(left_eye_region))
                features.append(np.std(left_eye_region))
            
            # Right eye region (approximate)
            right_eye_region = image[int(0.25*h):int(0.4*h), int(0.6*w):int(0.8*w)]
            if right_eye_region.size > 0:
                features.append(np.mean(right_eye_region))
                features.append(np.std(right_eye_region))
            
            # Pad with zeros if needed
            while len(features) < 16:
                features.append(0.0)
        
        # Ensure consistent size
        features = features[:16]
        while len(features) < 16:
            features.append(0.0)
        
        return np.array(features)
    
    def _extract_eyebrow_features(self, image) -> np.ndarray:
        """
        Extract eyebrow features.
        
        Captures:
        - Eyebrow thickness
        - Eyebrow shape (arch)
        - Eyebrow color (darkness)
        - Eyebrow position relative to eyes
        """
        h, w = image.shape
        features = []
        
        # Eyebrow regions (approximate - above eyes)
        # Left eyebrow
        left_brow_region = image[int(0.15*h):int(0.25*h), int(0.2*w):int(0.4*w)]
        if left_brow_region.size > 0:
            # Eyebrow darkness (darker = more prominent)
            brow_darkness = 255 - np.mean(left_brow_region)
            features.append(brow_darkness)
            
            # Eyebrow thickness (vertical gradient)
            brow_grad_y = cv2.Sobel(left_brow_region, cv2.CV_64F, 0, 1, ksize=3)
            brow_thickness = np.mean(np.abs(brow_grad_y))
            features.append(brow_thickness)
            
            # Eyebrow texture
            features.append(np.std(left_brow_region))
            
            # Eyebrow shape (horizontal gradient for arch detection)
            brow_grad_x = cv2.Sobel(left_brow_region, cv2.CV_64F, 1, 0, ksize=3)
            brow_arch = np.std(brow_grad_x)
            features.append(brow_arch)
        
        # Right eyebrow
        right_brow_region = image[int(0.15*h):int(0.25*h), int(0.6*w):int(0.8*w)]
        if right_brow_region.size > 0:
            brow_darkness = 255 - np.mean(right_brow_region)
            features.append(brow_darkness)
            
            brow_grad_y = cv2.Sobel(right_brow_region, cv2.CV_64F, 0, 1, ksize=3)
            brow_thickness = np.mean(np.abs(brow_grad_y))
            features.append(brow_thickness)
            
            features.append(np.std(right_brow_region))
            
            brow_grad_x = cv2.Sobel(right_brow_region, cv2.CV_64F, 1, 0, ksize=3)
            brow_arch = np.std(brow_grad_x)
            features.append(brow_arch)
        
        # Ensure consistent size
        while len(features) < 8:
            features.append(0.0)
        
        return np.array(features[:8])
    
    def _extract_hair_features(self, image) -> np.ndarray:
        """
        Extract hair features.
        
        Captures:
        - Hair color (brightness in hair region)
        - Hair texture
        - Hairline position
        """
        h, w = image.shape
        features = []
        
        # Hair region (top 15% of image)
        hair_region = image[:int(0.15*h), :]
        
        if hair_region.size > 0:
            # Hair color (average brightness)
            hair_brightness = np.mean(hair_region)
            features.append(hair_brightness)
            
            # Hair darkness (inverse)
            hair_darkness = 255 - hair_brightness
            features.append(hair_darkness)
            
            # Hair texture (standard deviation)
            hair_texture = np.std(hair_region)
            features.append(hair_texture)
            
            # Hair gradient (texture complexity)
            hair_grad_x = cv2.Sobel(hair_region, cv2.CV_64F, 1, 0, ksize=3)
            hair_grad_y = cv2.Sobel(hair_region, cv2.CV_64F, 0, 1, ksize=3)
            hair_gradient = np.mean(np.sqrt(hair_grad_x**2 + hair_grad_y**2))
            features.append(hair_gradient)
            
            # Hairline detection (edge at boundary)
            hairline_region = image[int(0.1*h):int(0.2*h), :]
            hairline_edges = cv2.Canny(hairline_region, 50, 150)
            hairline_prominence = np.mean(hairline_edges)
            features.append(hairline_prominence)
        
        # Ensure consistent size
        while len(features) < 5:
            features.append(0.0)
        
        return np.array(features[:5])
    
    def _extract_skin_tone(self, image) -> np.ndarray:
        """
        Extract skin tone features.
        
        Captures:
        - Overall skin brightness
        - Skin tone uniformity
        - Regional skin tone variations
        """
        h, w = image.shape
        features = []
        
        # Face region (excluding hair and background)
        face_region = image[int(0.2*h):int(0.8*h), int(0.2*w):int(0.8*w)]
        
        if face_region.size > 0:
            # Overall skin tone (brightness)
            skin_brightness = np.mean(face_region)
            features.append(skin_brightness)
            
            # Skin tone uniformity
            skin_uniformity = np.std(face_region)
            features.append(skin_uniformity)
            
            # Forehead skin tone
            forehead = image[int(0.2*h):int(0.3*h), int(0.3*w):int(0.7*w)]
            if forehead.size > 0:
                features.append(np.mean(forehead))
            
            # Cheek skin tone
            cheeks = image[int(0.4*h):int(0.6*h), int(0.2*w):int(0.8*w)]
            if cheeks.size > 0:
                features.append(np.mean(cheeks))
            
            # Chin skin tone
            chin = image[int(0.7*h):int(0.85*h), int(0.35*w):int(0.65*w)]
            if chin.size > 0:
                features.append(np.mean(chin))
        
        # Ensure consistent size
        while len(features) < 5:
            features.append(0.0)
        
        return np.array(features[:5])
    
    def _extract_facial_proportions(self, image) -> np.ndarray:
        """
        Extract facial proportion features.
        
        Captures:
        - Face width-to-height ratio
        - Upper face to lower face ratio
        - Eye spacing ratio
        - Nose width ratio
        """
        h, w = image.shape
        features = []
        
        # Face aspect ratio
        features.append(w / h)
        
        # Upper to lower face ratio
        upper_face = image[:h//2, :]
        lower_face = image[h//2:, :]
        upper_intensity = np.mean(upper_face)
        lower_intensity = np.mean(lower_face)
        features.append(upper_intensity / (lower_intensity + 1e-7))
        
        # Nose region width (approximate)
        nose_region = image[int(0.4*h):int(0.65*h), int(0.4*w):int(0.6*w)]
        if nose_region.size > 0:
            nose_width_ratio = nose_region.shape[1] / w
            features.append(nose_width_ratio)
            
            # Nose prominence (gradient)
            nose_grad = cv2.Sobel(nose_region, cv2.CV_64F, 1, 0, ksize=3)
            nose_prominence = np.mean(np.abs(nose_grad))
            features.append(nose_prominence)
        
        # Mouth region width
        mouth_region = image[int(0.65*h):int(0.8*h), int(0.3*w):int(0.7*w)]
        if mouth_region.size > 0:
            mouth_width_ratio = mouth_region.shape[1] / w
            features.append(mouth_width_ratio)
        
        # Ensure consistent size
        while len(features) < 5:
            features.append(0.0)
        
        return np.array(features[:5])
    
    def _extract_texture_patterns(self, image) -> np.ndarray:
        """
        Extract detailed texture patterns.
        
        Captures:
        - Skin texture (smoothness vs roughness)
        - Wrinkle patterns
        - Pore visibility
        """
        features = []
        
        # Apply Laplacian for texture detection
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        texture_variance = np.var(laplacian)
        features.append(texture_variance)
        
        # High-frequency texture (fine details)
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        high_freq = image.astype(float) - blurred.astype(float)
        features.append(np.mean(np.abs(high_freq)))
        features.append(np.std(high_freq))
        
        # Texture in different regions
        h, w = image.shape
        
        # Forehead texture
        forehead = image[int(0.15*h):int(0.3*h), int(0.3*w):int(0.7*w)]
        if forehead.size > 0:
            forehead_lap = cv2.Laplacian(forehead, cv2.CV_64F)
            features.append(np.var(forehead_lap))
        
        # Cheek texture
        cheek = image[int(0.4*h):int(0.6*h), int(0.2*w):int(0.4*w)]
        if cheek.size > 0:
            cheek_lap = cv2.Laplacian(cheek, cv2.CV_64F)
            features.append(np.var(cheek_lap))
        
        # Ensure consistent size
        while len(features) < 5:
            features.append(0.0)
        
        return np.array(features[:5])
    
    def features_to_vector(self, features_dict: Dict) -> np.ndarray:
        """
        Convert feature dictionary to single vector.
        
        Returns:
            256-dimensional feature vector
        """
        vector = []
        
        # Concatenate all features
        vector.extend(features_dict.get('face_structure', np.zeros(13)))
        vector.extend(features_dict.get('eyes', np.zeros(16)))
        vector.extend(features_dict.get('eyebrows', np.zeros(8)))
        vector.extend(features_dict.get('hair', np.zeros(5)))
        vector.extend(features_dict.get('skin_tone', np.zeros(5)))
        vector.extend(features_dict.get('proportions', np.zeros(5)))
        vector.extend(features_dict.get('texture', np.zeros(5)))
        
        # Convert to numpy array
        vector = np.array(vector)
        
        # Pad or truncate to 256 dimensions
        if len(vector) < 256:
            vector = np.pad(vector, (0, 256 - len(vector)), 'constant')
        else:
            vector = vector[:256]
        
        # L2 normalization
        vector = vector / (np.linalg.norm(vector) + 1e-7)
        
        return vector
