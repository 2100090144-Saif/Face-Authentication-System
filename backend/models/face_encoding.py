"""Face encoding model with safe JSON serialization."""
import json
import logging
import numpy as np
from datetime import datetime
from backend.app import db

logger = logging.getLogger(__name__)


class FaceEncoding(db.Model):
    """Face encoding model for storing face recognition data."""
    
    __tablename__ = 'face_encodings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    encoding_json = db.Column(db.Text, nullable=False)  # Stores encoding as JSON list
    image_path = db.Column(db.String(255), nullable=True)  # Optional reference
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    
    def __repr__(self):
        return f'<FaceEncoding user_id={self.user_id} id={self.id}>'
    
    @property
    def encoding(self):
        """
        Get encoding as numpy array with safe deserialization.
        
        Returns:
            numpy.ndarray or None if deserialization fails
        """
        try:
            if not self.encoding_json:
                logger.error(f"FaceEncoding {self.id}: encoding_json is empty")
                return None
            
            # Parse JSON to list
            encoding_list = json.loads(self.encoding_json)
            
            # Convert to numpy array
            encoding_array = np.array(encoding_list, dtype=np.float64)
            
            # Validate dimensions (should be 128)
            if encoding_array.shape[0] != 128:
                logger.error(
                    f"FaceEncoding {self.id}: Invalid dimensions {encoding_array.shape[0]}, expected 128"
                )
                return None
            
            return encoding_array
            
        except json.JSONDecodeError as e:
            logger.error(f"FaceEncoding {self.id}: JSON decode error: {e}")
            return None
        except Exception as e:
            logger.error(f"FaceEncoding {self.id}: Deserialization error: {e}", exc_info=True)
            return None
    
    @encoding.setter
    def encoding(self, value):
        """
        Set encoding from numpy array with safe serialization.
        
        Args:
            value: numpy.ndarray (128-dimensional)
        """
        try:
            if value is None:
                raise ValueError("Encoding cannot be None")
            
            # Convert numpy array to list
            if isinstance(value, np.ndarray):
                encoding_list = value.tolist()
            elif isinstance(value, list):
                encoding_list = value
            else:
                raise ValueError(f"Invalid encoding type: {type(value)}")
            
            # Validate dimensions
            if len(encoding_list) != 128:
                raise ValueError(f"Invalid encoding dimensions: {len(encoding_list)}, expected 128")
            
            # Store as JSON
            self.encoding_json = json.dumps(encoding_list)
            
            logger.debug(f"FaceEncoding {self.id}: Encoding serialized successfully (128 dimensions)")
            
        except Exception as e:
            logger.error(f"FaceEncoding serialization error: {e}", exc_info=True)
            raise
    
    def to_dict(self):
        """Convert face encoding to dictionary (exclude encoding data)."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }
