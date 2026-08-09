#!/usr/bin/env python3
"""
Fix encoding dimension mismatches in the database.
This script standardizes all face encodings to 128 dimensions.
"""
import sys
import os
import numpy as np
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app, db
from backend.models import FaceEncoding, User

def fix_encoding_dimensions():
    """Fix encoding dimension mismatches in the database."""
    app = create_app()
    
    with app.app_context():
        print("🔍 Analyzing face encodings in database...")
        
        # Get all face encodings
        encodings = FaceEncoding.query.all()
        
        if not encodings:
            print("❌ No face encodings found in database")
            return
        
        print(f"📊 Found {len(encodings)} face encodings")
        
        # Analyze dimensions
        dimension_stats = {}
        problematic_encodings = []
        
        for enc in encodings:
            try:
                encoding_array = enc.encoding
                if encoding_array is not None:
                    dims = len(encoding_array)
                    dimension_stats[dims] = dimension_stats.get(dims, 0) + 1
                    
                    if dims != 128:
                        problematic_encodings.append({
                            'id': enc.id,
                            'user_id': enc.user_id,
                            'dimensions': dims,
                            'encoding': enc
                        })
                else:
                    print(f"⚠️  Encoding {enc.id} has None encoding")
            except Exception as e:
                print(f"❌ Error analyzing encoding {enc.id}: {e}")
        
        print("\n📈 Dimension Statistics:")
        for dims, count in sorted(dimension_stats.items()):
            status = "✅ CORRECT" if dims == 128 else "❌ INCORRECT"
            print(f"  {dims}D: {count} encodings {status}")
        
        if not problematic_encodings:
            print("\n✅ All encodings have correct dimensions (128D)")
            return
        
        print(f"\n🔧 Found {len(problematic_encodings)} encodings with incorrect dimensions")
        
        # Ask for confirmation
        response = input("\n❓ Do you want to fix these encodings? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Operation cancelled")
            return
        
        print("\n🔧 Fixing encoding dimensions...")
        
        fixed_count = 0
        deleted_count = 0
        
        for prob in problematic_encodings:
            try:
                encoding = prob['encoding']
                original_dims = prob['dimensions']
                
                if original_dims > 128:
                    # Truncate to 128 dimensions
                    new_encoding = encoding.encoding[:128]
                    # Normalize
                    new_encoding = new_encoding / (np.linalg.norm(new_encoding) + 1e-7)
                    
                    encoding.encoding = new_encoding
                    print(f"  ✂️  Truncated encoding {encoding.id} from {original_dims}D to 128D")
                    fixed_count += 1
                    
                elif original_dims < 128:
                    # Pad to 128 dimensions
                    new_encoding = np.pad(encoding.encoding, (0, 128 - original_dims), 'constant')
                    # Normalize
                    new_encoding = new_encoding / (np.linalg.norm(new_encoding) + 1e-7)
                    
                    encoding.encoding = new_encoding
                    print(f"  📏 Padded encoding {encoding.id} from {original_dims}D to 128D")
                    fixed_count += 1
                
            except Exception as e:
                print(f"❌ Error fixing encoding {prob['id']}: {e}")
                # Delete problematic encoding
                try:
                    db.session.delete(prob['encoding'])
                    print(f"  🗑️  Deleted problematic encoding {prob['id']}")
                    deleted_count += 1
                except Exception as del_e:
                    print(f"❌ Error deleting encoding {prob['id']}: {del_e}")
        
        # Commit changes
        try:
            db.session.commit()
            print(f"\n✅ Successfully fixed {fixed_count} encodings")
            if deleted_count > 0:
                print(f"🗑️  Deleted {deleted_count} problematic encodings")
            print("💾 Changes committed to database")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error committing changes: {e}")
            return
        
        # Verify fix
        print("\n🔍 Verifying fix...")
        encodings_after = FaceEncoding.query.all()
        dimension_stats_after = {}
        
        for enc in encodings_after:
            try:
                if enc.encoding is not None:
                    dims = len(enc.encoding)
                    dimension_stats_after[dims] = dimension_stats_after.get(dims, 0) + 1
            except Exception as e:
                print(f"❌ Error verifying encoding {enc.id}: {e}")
        
        print("\n📈 Final Dimension Statistics:")
        for dims, count in sorted(dimension_stats_after.items()):
            status = "✅ CORRECT" if dims == 128 else "❌ STILL INCORRECT"
            print(f"  {dims}D: {count} encodings {status}")
        
        if all(dims == 128 for dims in dimension_stats_after.keys()):
            print("\n🎉 All encodings now have correct dimensions (128D)!")
        else:
            print("\n⚠️  Some encodings still have incorrect dimensions")

if __name__ == "__main__":
    print("🔧 Face Encoding Dimension Fix Tool")
    print("=" * 50)
    fix_encoding_dimensions()