"""Face recognition module with OpenCV fallback."""
import logging
import numpy as np
from typing import List, Tuple, Optional
import cv2

logger = logging.getLogger(__name__)

try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    logger.warning("face_recognition library not installed. Using OpenCV fallback. Run: pip install face-recognition")

# Import advanced feature extractor
try:
    from .advanced_face_features import AdvancedFaceFeatureExtractor
    ADVANCED_FEATURES_AVAILABLE = True
except ImportError:
    ADVANCED_FEATURES_AVAILABLE = False
    logger.warning("Advanced features not available")


class OpenCVFallbackRecognizer:
    """Fallback face recognizer using OpenCV when face_recognition is not available."""
    
    def __init__(self, tolerance=0.6, model='large'):
        """Initialize OpenCV-based recognizer with FIXED tolerance."""
        # FIXED: Use the global MAX_TOLERANCE (0.45) for consistency
        self.tolerance = min(tolerance, 0.45)  # Cap at 0.45 for maximum security
        self.model = model
        
        # Load face detector
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Initialize advanced feature extractor
        if ADVANCED_FEATURES_AVAILABLE:
            self.advanced_extractor = AdvancedFaceFeatureExtractor()
            self.use_advanced = True
            logger.info(f"OpenCV fallback with ADVANCED features initialized (tolerance={self.tolerance})")
        else:
            self.use_advanced = False
            logger.info(f"OpenCV fallback with basic features initialized (tolerance={self.tolerance})")
    
    def generate_encoding(self, image) -> Optional[np.ndarray]:
        """
        Generate face encoding using OpenCV with STANDARDIZED 128-dimensional output.
        
        Args:
            image: Image array (RGB format)
        
        Returns:
            Face encoding (128-dimensional array) or None if no face found
        """
        try:
            # Convert RGB to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            if len(faces) == 0:
                logger.warning("No face detected in image")
                return None
            
            if len(faces) > 1:
                logger.warning(f"Multiple faces detected ({len(faces)}), using largest one")
            
            # Get largest face
            largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
            x, y, w, h = largest_face
            
            # Extract face region with padding
            padding = int(0.2 * min(w, h))
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(gray.shape[1], x + w + padding)
            y2 = min(gray.shape[0], y + h + padding)
            
            face_roi = gray[y1:y2, x1:x2]
            
            # Resize to standard size
            face_resized = cv2.resize(face_roi, (128, 128))
            
            # Normalize lighting
            face_normalized = cv2.equalizeHist(face_resized)
            
            # ALWAYS use basic features for consistent 128-dimensional output
            # This ensures compatibility across all encodings in the database
            encoding = self._generate_basic_encoding(face_normalized)
            logger.info("Face encoding generated with STANDARDIZED 128-dimensional features")
            return encoding
        
        except Exception as e:
            logger.error(f"Error generating face encoding: {str(e)}")
            return None
    
    def _generate_basic_encoding(self, face_normalized) -> np.ndarray:
        """Generate basic encoding (fallback method)."""
        features = []
        
        # 1. Local Binary Pattern (LBP) features - 32 dimensions
        lbp_features = self._compute_lbp_features(face_normalized, grid_size=4, bins=8)
        features.extend(lbp_features[:32])
        
        # 2. Gradient magnitude features - 32 dimensions
        gradient_features = self._compute_gradient_features(face_normalized, grid_size=4)
        features.extend(gradient_features[:32])
        
        # 3. Multi-scale histogram features - 32 dimensions
        hist_features = self._compute_multiscale_histogram(face_normalized)
        features.extend(hist_features[:32])
        
        # 4. Facial landmark region features - 32 dimensions
        landmark_features = self._compute_landmark_region_features(face_normalized)
        features.extend(landmark_features[:32])
        
        # Ensure exactly 128 dimensions
        encoding = np.array(features[:128])
        if len(encoding) < 128:
            encoding = np.pad(encoding, (0, 128 - len(encoding)), 'constant')
        
        # L2 normalization
        encoding = encoding / (np.linalg.norm(encoding) + 1e-7)
        
        return encoding
    
    def _compute_lbp_features(self, image, grid_size=4, bins=8):
        """Compute Local Binary Pattern features."""
        features = []
        h, w = image.shape
        cell_h, cell_w = h // grid_size, w // grid_size
        
        for i in range(grid_size):
            for j in range(grid_size):
                cell = image[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]
                
                # Simple LBP: compare center pixel with neighbors
                lbp_hist = np.zeros(bins)
                if cell.shape[0] > 2 and cell.shape[1] > 2:
                    center = cell[1:-1, 1:-1]
                    
                    # Compare with 8 neighbors
                    neighbors = [
                        cell[:-2, 1:-1],  # top
                        cell[2:, 1:-1],   # bottom
                        cell[1:-1, :-2],  # left
                        cell[1:-1, 2:],   # right
                        cell[:-2, :-2],   # top-left
                        cell[:-2, 2:],    # top-right
                        cell[2:, :-2],    # bottom-left
                        cell[2:, 2:]      # bottom-right
                    ]
                    
                    for idx, neighbor in enumerate(neighbors):
                        if neighbor.shape == center.shape:
                            binary = (neighbor > center).astype(int)
                            lbp_hist[idx % bins] += np.sum(binary)
                
                # Normalize
                lbp_hist = lbp_hist / (np.sum(lbp_hist) + 1e-7)
                features.extend(lbp_hist)
        
        return np.array(features)
    
    def _compute_gradient_features(self, image, grid_size=4):
        """Compute gradient magnitude features."""
        # Compute gradients
        grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        features = []
        h, w = magnitude.shape
        cell_h, cell_w = h // grid_size, w // grid_size
        
        for i in range(grid_size):
            for j in range(grid_size):
                cell = magnitude[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]
                features.append(np.mean(cell))
                features.append(np.std(cell))
        
        return np.array(features)
    
    def _compute_multiscale_histogram(self, image):
        """Compute histogram features at multiple scales."""
        features = []
        
        # Full face histogram
        hist_full = cv2.calcHist([image], [0], None, [16], [0, 256]).flatten()
        hist_full = hist_full / (np.sum(hist_full) + 1e-7)
        features.extend(hist_full)
        
        # Upper half (eyes region)
        h = image.shape[0]
        upper = image[:h//2, :]
        hist_upper = cv2.calcHist([upper], [0], None, [8], [0, 256]).flatten()
        hist_upper = hist_upper / (np.sum(hist_upper) + 1e-7)
        features.extend(hist_upper)
        
        # Lower half (mouth region)
        lower = image[h//2:, :]
        hist_lower = cv2.calcHist([lower], [0], None, [8], [0, 256]).flatten()
        hist_lower = hist_lower / (np.sum(hist_lower) + 1e-7)
        features.extend(hist_lower)
        
        return np.array(features)
    
    def _compute_landmark_region_features(self, image):
        """Compute features from key facial regions."""
        h, w = image.shape
        features = []
        
        # Define approximate regions (without landmark detection)
        regions = {
            'left_eye': (int(0.25*h), int(0.35*h), int(0.2*w), int(0.4*w)),
            'right_eye': (int(0.25*h), int(0.35*h), int(0.6*w), int(0.8*w)),
            'nose': (int(0.4*h), int(0.6*h), int(0.4*w), int(0.6*w)),
            'mouth': (int(0.65*h), int(0.85*h), int(0.3*w), int(0.7*w))
        }
        
        for region_name, (y1, y2, x1, x2) in regions.items():
            region = image[y1:y2, x1:x2]
            if region.size > 0:
                features.append(np.mean(region))
                features.append(np.std(region))
                
                # Gradient in region
                grad_x = cv2.Sobel(region, cv2.CV_64F, 1, 0, ksize=3)
                grad_y = cv2.Sobel(region, cv2.CV_64F, 0, 1, ksize=3)
                magnitude = np.sqrt(grad_x**2 + grad_y**2)
                features.append(np.mean(magnitude))
        
        return np.array(features)
    
    def compare_faces(self, known_encoding: np.ndarray, unknown_encoding: np.ndarray) -> Tuple[bool, float]:
        """Compare two face encodings using cosine similarity with FIXED confidence calculation."""
        try:
            # Calculate cosine similarity
            dot_product = np.dot(known_encoding, unknown_encoding)
            norm_product = np.linalg.norm(known_encoding) * np.linalg.norm(unknown_encoding)
            similarity = dot_product / (norm_product + 1e-7)
            
            # Convert to distance (0 = identical, 1 = completely different)
            distance = 1 - similarity
            
            # FIXED: Confidence calculation - convert distance to percentage
            # confidence = (1 - distance) * 100 for percentage
            confidence_percentage = (1 - distance) * 100
            
            # Check if match (using distance tolerance)
            is_match = distance <= self.tolerance
            
            logger.debug(
                f"[MATCH DEBUG] distance={distance:.4f}, "
                f"confidence={confidence_percentage:.1f}%, "
                f"tolerance={self.tolerance}, "
                f"is_match={is_match}, "
                f"similarity={similarity:.4f}"
            )
            
            # Return raw confidence (0-1 scale) for internal calculations
            # The percentage conversion happens in face_service.py
            return is_match, 1 - distance
        
        except Exception as e:
            logger.error(f"compare_faces ERROR: {str(e)}", exc_info=True)
            return False, 0.0
    
    def find_best_match(self, known_encodings: List[np.ndarray], unknown_encoding: np.ndarray) -> Tuple[Optional[int], float]:
        """
        Find best matching face. Returns (index, confidence) or (None, 0.0).
        
        SECURITY: Only returns a match if:
        1. Distance is within tolerance threshold
        2. It's the best match among all candidates
        
        Returns:
            (match_index, confidence) if match found within tolerance
            (None, 0.0) if no match found or all matches exceed tolerance
        """
        try:
            if len(known_encodings) == 0:
                logger.warning("find_best_match: No known encodings provided")
                return None, 0.0

            best_match_idx = None   # stays None until tolerance is satisfied
            best_confidence = 0.0   # stays 0.0 until valid match found
            best_distance   = float('inf')

            logger.info(f"find_best_match: Comparing against {len(known_encodings)} known faces, tolerance={self.tolerance}")

            for idx, known_encoding in enumerate(known_encodings):
                # Compare faces
                is_match, confidence = self.compare_faces(known_encoding, unknown_encoding)
                distance = 1.0 - confidence

                logger.info(
                    f"  Candidate {idx}: distance={distance:.4f}, "
                    f"confidence={confidence:.4f}, "
                    f"within_tolerance={is_match}, "
                    f"tolerance_threshold={self.tolerance}"
                )

                # CRITICAL: Only consider candidates that pass the tolerance gate
                # This prevents false positives from being selected
                if is_match and distance < best_distance:
                    best_distance   = distance
                    best_confidence = confidence
                    best_match_idx  = idx
                    logger.info(f"  → New best match: idx={idx}, confidence={confidence:.4f}")

            # SECURITY CHECK: Verify we actually found a match within tolerance
            if best_match_idx is not None:
                logger.info(
                    f"find_best_match RESULT: MATCH FOUND - "
                    f"index={best_match_idx}, "
                    f"confidence={best_confidence:.4f}, "
                    f"distance={best_distance:.4f}, "
                    f"tolerance={self.tolerance}"
                )
                return best_match_idx, best_confidence
            else:
                # Calculate what the best distance was (even if it failed tolerance)
                all_distances = []
                for known_encoding in known_encodings:
                    _, conf = self.compare_faces(known_encoding, unknown_encoding)
                    all_distances.append(1.0 - conf)
                
                min_distance = min(all_distances) if all_distances else float('inf')
                
                logger.warning(
                    f"find_best_match RESULT: NO MATCH - "
                    f"All faces exceeded tolerance. "
                    f"Best distance={min_distance:.4f}, "
                    f"tolerance={self.tolerance}, "
                    f"exceeded_by={min_distance - self.tolerance:.4f}"
                )
                return None, 0.0

        except Exception as e:
            logger.error(f"find_best_match ERROR: {str(e)}", exc_info=True)
            return None, 0.0


class FaceRecognizer:
    """Face recognition with automatic fallback to OpenCV if face_recognition is not available."""
    
    def __init__(self, tolerance=0.6, model='large'):
        """
        Initialize face recognizer with FIXED tolerance.
        
        Args:
            tolerance: How much distance between faces to consider a match (lower is stricter)
            model: 'small' or 'large' - large is more accurate but slower
        """
        # FIXED: Use consistent tolerance (0.45) across all components
        self.tolerance = min(tolerance, 0.45)  # Cap at 0.45 for consistency
        self.model = model
        
        if FACE_RECOGNITION_AVAILABLE:
            self._use_fallback = False
            logger.info(f"Face recognizer initialized with face_recognition library (tolerance={self.tolerance}, model={model})")
        else:
            self._use_fallback = True
            self._fallback = OpenCVFallbackRecognizer(tolerance=self.tolerance, model=model)
            logger.info(f"Face recognizer initialized with OpenCV fallback (tolerance={self.tolerance})")
    
    def generate_encoding(self, image) -> Optional[np.ndarray]:
        """
        Generate face encoding from image.

        Args:
            image: Image array (RGB format)

        Returns:
            Face encoding (128-dimensional array) or None if no face found
        """
        if self._use_fallback:
            return self._fallback.generate_encoding(image)
        
        try:
            # Detect face locations
            face_locations = face_recognition.face_locations(image)
            
            if len(face_locations) == 0:
                logger.warning("No face detected in image")
                return None
            
            if len(face_locations) > 1:
                logger.warning(f"Multiple faces detected ({len(face_locations)}), using first one")
            
            # Generate encoding for first face
            encodings = face_recognition.face_encodings(
                image, 
                face_locations, 
                model=self.model
            )
            
            if len(encodings) == 0:
                logger.warning("Failed to generate face encoding")
                return None
            
            logger.info("Face encoding generated successfully")
            return encodings[0]
        
        except Exception as e:
            logger.error(f"Error generating face encoding: {str(e)}")
            return None
    
    def compare_faces(self, known_encoding: np.ndarray, unknown_encoding: np.ndarray) -> Tuple[bool, float]:
        """
        Compare two face encodings with FIXED confidence calculation.

        Args:
            known_encoding: Known face encoding
            unknown_encoding: Unknown face encoding to compare

        Returns:
            Tuple of (is_match, confidence)
        """
        if self._use_fallback:
            return self._fallback.compare_faces(known_encoding, unknown_encoding)
        
        try:
            # Calculate face distance
            distance = face_recognition.face_distance([known_encoding], unknown_encoding)[0]
            
            # Check if match
            is_match = distance <= self.tolerance
            
            # FIXED: Confidence calculation - convert distance to percentage for logging
            confidence_percentage = (1 - distance) * 100
            
            logger.debug(
                f"[MATCH DEBUG] distance={distance:.4f}, "
                f"confidence={confidence_percentage:.1f}%, "
                f"tolerance={self.tolerance}, "
                f"is_match={is_match}"
            )
            
            # Return raw confidence (0-1 scale) for internal calculations
            return is_match, 1 - distance
        
        except Exception as e:
            logger.error(f"compare_faces ERROR: {str(e)}", exc_info=True)
            return False, 0.0
    
    def find_best_match(self, known_encodings: List[np.ndarray], unknown_encoding: np.ndarray) -> Tuple[Optional[int], float]:
        """
        Find best matching face from list of known encodings.
        
        SECURITY: Only returns a match if distance is within tolerance threshold.

        Args:
            known_encodings: List of known face encodings
            unknown_encoding: Unknown face encoding to match

        Returns:
            Tuple of (best_match_index, confidence) or (None, 0.0) if no match
        """
        if self._use_fallback:
            return self._fallback.find_best_match(known_encodings, unknown_encoding)
        
        try:
            if len(known_encodings) == 0:
                logger.warning("find_best_match: No known encodings provided")
                return None, 0.0
            
            logger.info(f"find_best_match: Comparing against {len(known_encodings)} known faces, tolerance={self.tolerance}")
            
            # Calculate distances to all known faces
            distances = face_recognition.face_distance(known_encodings, unknown_encoding)
            
            # Log all distances for debugging
            for idx, dist in enumerate(distances):
                conf_pct = (1 - dist) * 100
                within_tol = dist <= self.tolerance
                logger.info(
                    f"  Candidate {idx}: distance={dist:.4f}, "
                    f"confidence={conf_pct:.1f}%, "
                    f"within_tolerance={within_tol}, "
                    f"tolerance_threshold={self.tolerance}"
                )
            #Saif
            # Find best match
            best_match_idx = np.argmin(distances)
            best_distance = distances[best_match_idx]
            #Test comment
            # CRITICAL: Check if best match is within tolerance
            if best_distance <= self.tolerance:
                confidence = 1 - best_distance
                confidence_pct = confidence * 100
                logger.info(
                    f"find_best_match RESULT: MATCH FOUND - "
                    f"index={best_match_idx}, "
                    f"confidence={confidence_pct:.1f}%, "
                    f"distance={best_distance:.4f}, "
                    f"tolerance={self.tolerance}"
                )
                return best_match_idx, confidence
            else:
                logger.warning(
                    f"find_best_match RESULT: NO MATCH - "
                    f"Best distance={best_distance:.4f} exceeds tolerance={self.tolerance}, "
                    f"exceeded_by={best_distance - self.tolerance:.4f}"
                )
                return None, 0.0
        
        except Exception as e:
            logger.error(f"find_best_match ERROR: {str(e)}", exc_info=True)
            return None, 0.0
    
    def batch_generate_encodings(self, images: List[np.ndarray]) -> List[Optional[np.ndarray]]:
        """
        Generate encodings for multiple images.
        
        Args:
            images: List of image arrays
        
        Returns:
            List of encodings (None for images with no face)
        """
        encodings = []
        
        for i, image in enumerate(images):
            logger.info(f"Processing image {i+1}/{len(images)}")
            encoding = self.generate_encoding(image)
            encodings.append(encoding)
        
        return encodings
