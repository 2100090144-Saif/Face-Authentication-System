""" NewFace recognition service with comprehensive audit logging."""
import uuid 
import logging 
import datetime
from backend.app import db
from backend.models import User, FaceEncoding
from ai_service import FaceRecognizer
from ai_service.utils import load_image_from_bytes, bgr_to_rgb, validate_image

logger = logging.getLogger(__name__) 

# Dedicated audit logger - every attempt gets a full trace
audit_logger = logging.getLogger('face_auth.audit')
    
# Security constants - single source of truth
# CRITICAL: These values control authentication strictness
# - Lower tolerance = stricter matching (rejects more faces)
# - Higher confidence = requires better match quality 
MIN_CONFIDENCE   = 0.60   # 60% minimum confidence in 0-1 scale (FIXED: was 60.0 causing unit mismatch)
MAX_TOLERANCE    = 0.45   # maximum distance allowed (user requested 0.45)
MULTI_FRAME_COUNT = 5     # Number of frames to capture for averaging
STABILIZATION_FRAMES = 3  # Minimum consecutive frames that must pass

# Global singleton instance
_face_service_instance = None


def get_face_service():
    """
    Get or create the singleton FaceService instance.
    This ensures the face recognizer is initialized ONLY ONCE.
    """
    global _face_service_instance
    if _face_service_instance is None:
        _face_service_instance = FaceService(tolerance=MAX_TOLERANCE, model='large')
        logger.info("🔒 FaceService singleton created (FIRST AND ONLY initialization)")
    return _face_service_instance


def _audit(attempt_id: str, step: str, decision: str, detail: str, **kwargs):
    """Write a structured audit log line."""
    extras = " | ".join(f"{k}={v}" for k, v in kwargs.items())
    audit_logger.info(
        f"[{attempt_id}] STEP={step:<25} DECISION={decision:<7} {detail}"
        + (f" | {extras}" if extras else "")
    )


class FaceService:
    """Service for face recognition operations."""

    def __init__(self, tolerance=0.35, model='large'):
        """Initialize face service."""
        # Always enforce the hard cap regardless of config value
        safe_tolerance = min(tolerance, MAX_TOLERANCE)
        self.recognizer = FaceRecognizer(tolerance=safe_tolerance, model=model)
        logger.info(f"FaceService initialized (tolerance={safe_tolerance}, model={model})")

    # ------------------------------------------------------------------ #
    #  REGISTER                                                            #
    # ------------------------------------------------------------------ #
    def register_face(self, user, image_bytes):
        """Register user's face. Returns (face_encoding_obj, error_message)."""
        try:
            image = load_image_from_bytes(image_bytes)
            if image is None:
                return None, "Failed to load image"

            if not validate_image(image):
                return None, "Invalid image format"

            image_rgb = bgr_to_rgb(image)
            encoding = self.recognizer.generate_encoding(image_rgb)

            if encoding is None:
                return None, "No face detected in image"

            face_encoding = FaceEncoding(user_id=user.id, encoding=encoding)
            db.session.add(face_encoding)
            user.face_recognition_enabled = True
            db.session.commit()

            logger.info(f"✅ Face registered for user {user.username} (user_id={user.id})")
            return face_encoding, None

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error registering face: {str(e)}", exc_info=True)
            return None, "Failed to register face"

    # ------------------------------------------------------------------ #
    #  AUTHENTICATE  (NO retry decorator — every attempt is independent)  #
    # ------------------------------------------------------------------ #
    def authenticate_face(self, image_bytes):
        """
        Authenticate user by face with MULTI-FRAME verification and stabilization.

        Returns:
            Tuple of (user | None, confidence: float, error_message | None)
            Authentication is ONLY successful when:
              - user   is not None
              - error  is None
              - confidence >= MIN_CONFIDENCE (60%)
              - distance <= MAX_TOLERANCE (0.45)
              - EXACTLY one face detected
              - User has face recognition enabled
              - Multi-frame verification passes
        """
        attempt_id = uuid.uuid4().hex[:8].upper()   # unique ID per attempt
        timestamp  = datetime.datetime.utcnow().isoformat()

        _audit(attempt_id, "START", "INFO",
               f"New face authentication attempt with multi-frame verification", 
               timestamp=timestamp,
               min_confidence=MIN_CONFIDENCE,
               max_tolerance=MAX_TOLERANCE,
               multi_frame_count=MULTI_FRAME_COUNT)

        # ── Step 1: Multi-frame processing ──────────────────────────────────
        frame_results = []
        
        for frame_idx in range(MULTI_FRAME_COUNT):
            _audit(attempt_id, f"FRAME_{frame_idx+1}_START", "INFO",
                   f"Processing frame {frame_idx+1}/{MULTI_FRAME_COUNT}")
            
            # Process single frame
            frame_user, frame_confidence, frame_error = self._authenticate_single_frame(
                image_bytes, attempt_id, frame_idx + 1
            )
            
            frame_results.append({
                'user': frame_user,
                'confidence': frame_confidence,
                'error': frame_error,
                'distance': 1.0 - frame_confidence if frame_confidence > 0 else float('inf')
            })
            
            # Calculate distance and confidence percentage for logging
            frame_distance = 1.0 - frame_confidence if frame_confidence > 0 else float('inf')
            frame_confidence_pct = (1 - frame_distance) * 100 if frame_distance != float('inf') else 0.0
            
            _audit(attempt_id, f"FRAME_{frame_idx+1}_RESULT", "INFO",
                   f"Frame result",
                   confidence_raw=f"{frame_confidence:.4f}",
                   confidence_pct=f"{frame_confidence_pct:.1f}%",
                   distance=f"{frame_distance:.4f}",
                   error=frame_error or "None")

        # ── Step 2: Multi-frame analysis ────────────────────────────────────
        valid_frames = [r for r in frame_results if r['error'] is None and r['user'] is not None]
        
        if len(valid_frames) == 0:
            _audit(attempt_id, "MULTI_FRAME_ANALYSIS", "REJECT",
                   f"No valid frames out of {MULTI_FRAME_COUNT}")
            return None, 0.0, "No valid face detected in any frame"
        
        # Calculate average confidence and distance
        avg_confidence_raw = sum(r['confidence'] for r in valid_frames) / len(valid_frames)
        avg_distance = sum(r['distance'] for r in valid_frames) / len(valid_frames)
        
        # Keep confidence in 0-1 scale for threshold comparisons
        # avg_confidence is used for threshold checks (must be 0-1 scale)
        avg_confidence = avg_confidence_raw  # 0-1 scale
        
        # Calculate percentage for logging only
        avg_confidence_pct = avg_confidence * 100
        
        # Check for consistent user across frames
        user_ids = [r['user'].id for r in valid_frames if r['user']]
        if len(set(user_ids)) > 1:
            _audit(attempt_id, "MULTI_FRAME_ANALYSIS", "REJECT",
                   f"Inconsistent users across frames", user_ids=str(user_ids))
            return None, 0.0, "Inconsistent face recognition across frames"
        
        # Get the consistent user
        consistent_user = valid_frames[0]['user']
        
        _audit(attempt_id, "MULTI_FRAME_ANALYSIS", "PASS",
               f"Multi-frame analysis complete",
               valid_frames=len(valid_frames),
               total_frames=MULTI_FRAME_COUNT,
               avg_confidence_raw=f"{avg_confidence_raw:.4f}",
               avg_confidence_pct=f"{avg_confidence_pct:.1f}%",
               avg_distance=f"{avg_distance:.4f}",
               user_id=consistent_user.id)

        # ── Step 3: Stabilization check ─────────────────────────────────────
        consecutive_passes = 0
        max_consecutive = 0
        
        for result in frame_results:
            # FIXED: Use raw confidence (0-1 scale) for comparison
            result_confidence = result['confidence'] if result['confidence'] > 0 else 0.0
            
            if (result['error'] is None and 
                result['user'] is not None and 
                result_confidence >= MIN_CONFIDENCE):
                consecutive_passes += 1
                max_consecutive = max(max_consecutive, consecutive_passes)
            else:
                consecutive_passes = 0
        
        if max_consecutive < STABILIZATION_FRAMES:
            _audit(attempt_id, "STABILIZATION_CHECK", "REJECT",
                   f"Insufficient consecutive passes",
                   max_consecutive=max_consecutive,
                   required=STABILIZATION_FRAMES,
                   avg_confidence_pct=f"{avg_confidence_pct:.1f}%")
            return None, avg_confidence_pct, f"Face recognition not stable enough ({max_consecutive}/{STABILIZATION_FRAMES} consecutive passes)"

        _audit(attempt_id, "STABILIZATION_CHECK", "PASS",
               f"Stabilization check passed",
               consecutive_passes=max_consecutive,
               required=STABILIZATION_FRAMES)

        # ── Step 4: Final confidence gate ───────────────────────────────────
        # CRITICAL: avg_confidence is in 0-1 scale, MIN_CONFIDENCE is also 0-1 scale
        if avg_confidence < MIN_CONFIDENCE:
            min_confidence_pct = MIN_CONFIDENCE * 100
            _audit(attempt_id, "FINAL_CONFIDENCE_GATE", "REJECT",
                   f"Average confidence {avg_confidence_pct:.1f}% < required {min_confidence_pct:.0f}%",
                   avg_confidence_pct=f"{avg_confidence_pct:.1f}%",
                   avg_distance=f"{avg_distance:.4f}",
                   required=f"{min_confidence_pct:.0f}%")
            return None, avg_confidence_pct, f"Average face match confidence too low ({avg_confidence_pct:.1f}% < {min_confidence_pct:.0f}%)"

        # ── Step 5: FINAL ALLOW ─────────────────────────────────────────────
        _audit(attempt_id, "FINAL_DECISION", "ALLOW",
               f"✅ Multi-frame authentication successful",
               username=consistent_user.username,
               user_id=consistent_user.id,
               avg_confidence_raw=f"{avg_confidence_raw:.4f}",
               avg_confidence_pct=f"{avg_confidence_pct:.1f}%",
               avg_distance=f"{avg_distance:.4f}",
               valid_frames=len(valid_frames),
               stabilization_passes=max_consecutive)

        return consistent_user, avg_confidence_pct, None

    def _authenticate_single_frame(self, image_bytes, attempt_id, frame_num):
        """
        Authenticate a single frame (internal method for multi-frame processing).
        
        Returns:
            Tuple of (user | None, confidence: float, error_message | None)
        """
        frame_prefix = f"F{frame_num}"
        
        # ── Step 1: load image ──────────────────────────────────────────
        try:
            image = load_image_from_bytes(image_bytes)
        except Exception as e:
            _audit(attempt_id, f"{frame_prefix}_LOAD_IMAGE", "REJECT", f"Exception: {e}")
            return None, 0.0, "Failed to load image"

        if image is None:
            _audit(attempt_id, f"{frame_prefix}_LOAD_IMAGE", "REJECT", "load_image_from_bytes returned None")
            return None, 0.0, "Failed to load image"

        # ── Step 2: validate image ──────────────────────────────────────
        if not validate_image(image):
            _audit(attempt_id, f"{frame_prefix}_VALIDATE_IMAGE", "REJECT", "Image failed validation")
            return None, 0.0, "Invalid image format"

        # ── Step 3: convert colour space ────────────────────────────────
        image_rgb = bgr_to_rgb(image)

        # ── Step 4: generate encoding ───────────────────────────────────
        try:
            unknown_encoding = self.recognizer.generate_encoding(image_rgb)
        except Exception as e:
            _audit(attempt_id, f"{frame_prefix}_GENERATE_ENCODING", "REJECT", f"Exception: {e}")
            return None, 0.0, "Encoding generation failed"

        if unknown_encoding is None:
            _audit(attempt_id, f"{frame_prefix}_GENERATE_ENCODING", "REJECT", "No face detected in image")
            return None, 0.0, "No face detected in image"

        # ── Step 5: load registered encodings ───────────────────────────
        try:
            active_encodings = FaceEncoding.query.filter_by(is_active=True).all()
        except Exception as e:
            _audit(attempt_id, f"{frame_prefix}_LOAD_DB_ENCODINGS", "REJECT", f"DB query error: {e}")
            return None, 0.0, "Database error"

        if not active_encodings:
            _audit(attempt_id, f"{frame_prefix}_LOAD_DB_ENCODINGS", "REJECT",
                   "No registered faces in system")
            return None, 0.0, "No registered faces in system"

        # ── Step 6: deserialize encodings with error handling ────────────
        known_encodings = []
        user_ids = []
        failed_count = 0
        
        for enc in active_encodings:
            try:
                encoding_array = enc.encoding  # Uses property getter with safe deserialization
                if encoding_array is not None:
                    known_encodings.append(encoding_array)
                    user_ids.append(enc.user_id)
                else:
                    failed_count += 1
                    logger.warning(f"Failed to deserialize encoding {enc.id} for user {enc.user_id}")
            except Exception as e:
                failed_count += 1
                logger.error(f"Error loading encoding {enc.id}: {e}", exc_info=True)
        
        # Log deserialization results
        if failed_count > 0:
            _audit(attempt_id, f"{frame_prefix}_LOAD_DB_ENCODINGS", "WARNING",
                   f"Loaded {len(known_encodings)} encodings, {failed_count} failed deserialization")
        
        # Check if we have any valid encodings
        if len(known_encodings) == 0:
            _audit(attempt_id, f"{frame_prefix}_LOAD_DB_ENCODINGS", "REJECT",
                   f"No valid encodings available (total={len(active_encodings)}, failed={failed_count})")
            return None, 0.0, "No valid face encodings in system"
        
        _audit(attempt_id, f"{frame_prefix}_LOAD_DB_ENCODINGS", "PASS",
               f"Loaded {len(known_encodings)} valid encodings")

        # ── Step 7: find best match ──────────────────────────────────────

        # ── Step 7: find best match ──────────────────────────────────────
        try:
            match_idx, confidence = self.recognizer.find_best_match(
                known_encodings, unknown_encoding
            )
        except Exception as e:
            _audit(attempt_id, f"{frame_prefix}_FIND_BEST_MATCH", "REJECT", f"Exception: {e}")
            return None, 0.0, "Matching failed"

        # Calculate distance for logging (distance = 1 - confidence)
        distance = 1.0 - confidence if confidence > 0 else float('inf')

        # ── Step 8: tolerance gate ───────────────────────────────────────
        if match_idx is None:
            return None, 0.0, "Face not recognized"

        # ── Step 9: confidence gate ──────────────────────────────────────
        # FIXED: confidence is in 0-1 scale, MIN_CONFIDENCE is also 0-1 scale
        if confidence < MIN_CONFIDENCE:
            confidence_pct = confidence * 100
            min_confidence_pct = MIN_CONFIDENCE * 100
            return None, confidence, f"Face match confidence too low ({confidence_pct:.1f}% < {min_confidence_pct:.0f}%)"

        # ── Step 10: resolve user ─────────────────────────────────────────
        user_id = user_ids[match_idx]
        try:
            user = User.query.get(user_id)
        except Exception as e:
            return None, 0.0, "Database error"

        if user is None:
            return None, 0.0, "User not found"

        # ── Step 11: check face recognition enabled ──────────────────────
        if not user.face_recognition_enabled:
            return None, 0.0, "Face recognition disabled for this user"

        return user, confidence, None

    # ------------------------------------------------------------------ #
    #  HELPERS                                                             #
    # ------------------------------------------------------------------ #
    def get_user_encodings(self, user):
        """Get all active face encodings for user."""
        try:
            return FaceEncoding.query.filter_by(user_id=user.id, is_active=True).all()
        except Exception as e:
            logger.error(f"Error getting user encodings: {str(e)}")
            return []

    def delete_user_encodings(self, user):
        """Delete all face encodings for user. Returns (count, error)."""
        try:
            encodings = FaceEncoding.query.filter_by(user_id=user.id).all()
            count = len(encodings)
            for enc in encodings:
                db.session.delete(enc)
            user.face_recognition_enabled = False
            db.session.commit()
            logger.info(f"Deleted {count} face encodings for user {user.username}")
            return count, None
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting face encodings: {str(e)}", exc_info=True)
            return 0, "Failed to delete face encodings"
