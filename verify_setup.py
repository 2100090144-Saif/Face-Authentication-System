"""
Verify Python version and face recognition setup inside Docker container.
Run this after the container starts:
    docker exec face_auth_app python verify_setup.py
"""
import sys
import platform

PASS = "✅"
FAIL = "❌"
WARN = "⚠️ "

results = []

def check(label, fn):
    try:
        ok, detail = fn()
        status = PASS if ok else FAIL
        results.append((ok, label, detail))
        print(f"  {status}  {label:<40} {detail}")
        return ok
    except Exception as e:
        results.append((False, label, str(e)))
        print(f"  {FAIL}  {label:<40} ERROR: {e}")
        return False


print()
print("=" * 65)
print("  Face Authentication System - Environment Verification")
print("=" * 65)

# ── 1. Python version ────────────────────────────────────────────────
print("\n[1] Python Environment")

def check_python():
    v = sys.version_info
    version_str = f"{v.major}.{v.minor}.{v.micro}"
    ok = v.major == 3 and v.minor in (10, 11)
    note = "✓ compatible" if ok else f"⚠ need 3.10 or 3.11, got {version_str}"
    return ok, f"Python {version_str}  ({note})"

check("Python version (need 3.10 or 3.11)", check_python)

def check_platform():
    return True, platform.platform()

check("Platform", check_platform)

# ── 2. Core libraries ────────────────────────────────────────────────
print("\n[2] Core Libraries")

def check_numpy():
    import numpy as np
    return True, f"numpy {np.__version__}"
check("numpy", check_numpy)

def check_cv2():
    import cv2
    return True, f"opencv {cv2.__version__}"
check("opencv-python", check_cv2)

def check_pillow():
    from PIL import Image
    import PIL
    return True, f"Pillow {PIL.__version__}"
check("Pillow", check_pillow)

# ── 3. dlib ──────────────────────────────────────────────────────────
print("\n[3] dlib (critical for face_recognition)")

def check_dlib():
    import dlib
    return True, f"dlib {dlib.__version__}"
check("dlib", check_dlib)

def check_dlib_cuda():
    import dlib
    cuda = dlib.DLIB_USE_CUDA
    return True, f"CUDA support = {cuda}"
check("dlib CUDA support", check_dlib_cuda)

# ── 4. face_recognition ──────────────────────────────────────────────
print("\n[4] face_recognition library")

def check_face_recognition():
    import face_recognition
    return True, "face_recognition imported OK"
check("face_recognition import", check_face_recognition)

def check_face_recognition_models():
    import face_recognition_models
    return True, "face_recognition_models imported OK"
check("face_recognition_models", check_face_recognition_models)

def check_face_recognition_functional():
    import face_recognition
    import numpy as np
    # Create a tiny blank image and try to run face_locations
    blank = np.zeros((100, 100, 3), dtype=np.uint8)
    locs = face_recognition.face_locations(blank)
    return True, f"face_locations() ran OK (found {len(locs)} faces in blank image)"
check("face_recognition functional test", check_face_recognition_functional)

# ── 5. Flask stack ───────────────────────────────────────────────────
print("\n[5] Flask Stack")

def check_flask():
    import flask
    return True, f"Flask {flask.__version__}"
check("Flask", check_flask)

def check_sqlalchemy():
    import sqlalchemy
    return True, f"SQLAlchemy {sqlalchemy.__version__}"
check("SQLAlchemy", check_sqlalchemy)

def check_flask_login():
    import flask_login
    return True, "flask_login imported OK"
check("Flask-Login", check_flask_login)

def check_bcrypt():
    import flask_bcrypt
    return True, "flask_bcrypt imported OK"
check("Flask-Bcrypt", check_bcrypt)

# ── 6. Project modules ───────────────────────────────────────────────
print("\n[6] Project Modules")

def check_ai_service():
    from ai_service import FaceRecognizer, FaceDetector
    r = FaceRecognizer()
    return True, f"FaceRecognizer initialized, fallback={r._use_fallback}"
check("ai_service (FaceRecognizer)", check_ai_service)

def check_face_recognition_active():
    from ai_service.face_recognition import FACE_RECOGNITION_AVAILABLE
    if FACE_RECOGNITION_AVAILABLE:
        return True, "Using dlib face_recognition library ✓"
    else:
        return False, "Using OpenCV fallback (dlib not available)"
check("face_recognition library active", check_face_recognition_active)

# ── Summary ──────────────────────────────────────────────────────────
print()
print("=" * 65)
passed = sum(1 for ok, _, _ in results if ok)
failed = sum(1 for ok, _, _ in results if not ok)
total  = len(results)

print(f"  Results: {passed}/{total} passed  |  {failed} failed")

if failed == 0:
    print(f"\n  {PASS} ALL CHECKS PASSED - System is fully operational!")
    print(f"  face_recognition library is active with dlib backend.")
    print(f"  Face authentication will use high-accuracy dlib encodings.")
else:
    print(f"\n  {FAIL} {failed} check(s) failed.")
    for ok, label, detail in results:
        if not ok:
            print(f"     - {label}: {detail}")

print("=" * 65)
print()

sys.exit(0 if failed == 0 else 1)
