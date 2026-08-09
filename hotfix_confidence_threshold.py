#!/usr/bin/env python3
"""
Hot-fix script to update confidence threshold in running container.
This script directly modifies the face_service.py file to use 60% threshold.
"""
import os
import re

def hotfix_confidence_threshold():
    """Update the confidence threshold to 60% in the face service."""
    
    service_file = "/app/backend/services/face_service.py"
    
    if not os.path.exists(service_file):
        print(f"❌ File not found: {service_file}")
        return False
    
    print("🔧 Hot-fixing confidence threshold...")
    
    # Read the current file
    with open(service_file, 'r') as f:
        content = f.read()
    
    # Show current configuration
    print("\n📊 Current Configuration:")
    for line in content.split('\n'):
        if 'MIN_CONFIDENCE' in line and '=' in line:
            print(f"  {line.strip()}")
        elif 'MAX_TOLERANCE' in line and '=' in line:
            print(f"  {line.strip()}")
    
    # Update MIN_CONFIDENCE to 0.60
    updated_content = re.sub(
        r'MIN_CONFIDENCE\s*=\s*0\.\d+.*',
        'MIN_CONFIDENCE   = 0.60   # 60% minimum confidence (user requested fix for 75-85% range)',
        content
    )
    
    # Add multi-frame constants if not present
    if 'MULTI_FRAME_COUNT' not in updated_content:
        # Find the line after MAX_TOLERANCE and add the new constants
        lines = updated_content.split('\n')
        new_lines = []
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            if 'MAX_TOLERANCE' in line and '=' in line:
                new_lines.append('MULTI_FRAME_COUNT = 5     # Number of frames to capture for averaging')
                new_lines.append('STABILIZATION_FRAMES = 3  # Minimum consecutive frames that must pass')
        
        updated_content = '\n'.join(new_lines)
    
    # Write the updated file
    with open(service_file, 'w') as f:
        f.write(updated_content)
    
    print("\n✅ Hot-fix Applied!")
    print("\n📊 New Configuration:")
    
    # Show updated configuration
    with open(service_file, 'r') as f:
        content = f.read()
    
    for line in content.split('\n'):
        if 'MIN_CONFIDENCE' in line and '=' in line:
            print(f"  {line.strip()}")
        elif 'MAX_TOLERANCE' in line and '=' in line:
            print(f"  {line.strip()}")
        elif 'MULTI_FRAME_COUNT' in line and '=' in line:
            print(f"  {line.strip()}")
        elif 'STABILIZATION_FRAMES' in line and '=' in line:
            print(f"  {line.strip()}")
    
    print("\n🔄 Please restart the application to apply changes:")
    print("   docker-compose restart")
    
    return True

if __name__ == "__main__":
    print("🔧 Confidence Threshold Hot-Fix Tool")
    print("=" * 50)
    hotfix_confidence_threshold()