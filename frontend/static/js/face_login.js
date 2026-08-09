// Face Login JavaScript

let stream = null;
let video = null;
let canvas = null;

document.addEventListener('DOMContentLoaded', () => {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
});

async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        });
        
        video.srcObject = stream;
        
        // Show authenticate button, hide start button
        document.getElementById('start-camera').style.display = 'none';
        document.getElementById('authenticate-btn').style.display = 'inline-block';
        
        showStatus('Camera started. Position your face in the frame.', 'success');
    } catch (error) {
        console.error('Camera error:', error);
        showStatus('Failed to access camera. Please check permissions.', 'error');
        showMessage('Camera access denied. Please enable camera permissions in your browser.', 'error');
    }
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
}

async function authenticateWithFace() {
    if (!stream) {
        showMessage('Camera not started', 'error');
        return;
    }
    
    // Set canvas size to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw video frame to canvas
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert canvas to blob
    canvas.toBlob(async (blob) => {
        if (!blob) {
            showMessage('Failed to capture image', 'error');
            return;
        }
        
        // Show loading state
        document.getElementById('authenticate-btn').disabled = true;
        document.getElementById('authenticate-btn').textContent = 'Authenticating...';
        showStatus('Authenticating...', 'info');
        
        // Create form data
        const formData = new FormData();
        formData.append('image', blob, 'face.jpg');
        
        try {
            const response = await fetch('/api/v1/face/login', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                const confidence = (data.data.confidence * 100).toFixed(1);
                showMessage(`Authentication successful! (${confidence}% confidence)`, 'success');
                showStatus(`Welcome, ${data.data.user.username}! Redirecting...`, 'success');
                
                // Stop camera
                stopCamera();
                
                // Redirect to dashboard
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 2000);
            } else {
                showMessage(data.error || 'Face authentication failed', 'error');
                showStatus(data.error || 'Authentication failed. Please try again.', 'error');
                
                // Show retry button
                document.getElementById('authenticate-btn').style.display = 'none';
                document.getElementById('retry-btn').style.display = 'inline-block';
            }
        } catch (error) {
            console.error('Authentication error:', error);
            showMessage('An error occurred during face authentication', 'error');
            showStatus('Error occurred. Please try again.', 'error');
            
            // Show retry button
            document.getElementById('authenticate-btn').style.display = 'none';
            document.getElementById('retry-btn').style.display = 'inline-block';
        } finally {
            document.getElementById('authenticate-btn').disabled = false;
            document.getElementById('authenticate-btn').textContent = 'Authenticate';
        }
    }, 'image/jpeg', 0.95);
}

function retryCapture() {
    // Reset buttons
    document.getElementById('retry-btn').style.display = 'none';
    document.getElementById('authenticate-btn').style.display = 'inline-block';
    
    // Clear status
    showStatus('Position your face in the frame and try again.', 'info');
}

function showStatus(message, type) {
    const statusEl = document.getElementById('status');
    statusEl.textContent = message;
    statusEl.className = `status-message ${type}`;
}

// Clean up on page unload
window.addEventListener('beforeunload', stopCamera);
