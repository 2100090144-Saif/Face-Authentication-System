// Settings JavaScript

// Load settings on page load
document.addEventListener('DOMContentLoaded', loadSettings);

async function loadSettings() {
    try {
        const response = await fetch('/api/v1/settings');
        const data = await response.json();
        
        if (data.success) {
            const settings = data.data;
            
            // Update toggle
            const toggle = document.getElementById('face-toggle');
            toggle.checked = settings.face_recognition_enabled;
            
            // Update status text
            const statusText = document.getElementById('face-status-text');
            if (settings.face_recognition_enabled) {
                statusText.textContent = `Enabled (${settings.encoding_count} face encoding(s) registered)`;
                statusText.style.color = '#28a745';
                document.getElementById('face-actions').style.display = 'block';
                document.getElementById('face-register-prompt').style.display = 'none';
            } else {
                statusText.textContent = 'Disabled';
                statusText.style.color = '#dc3545';
                document.getElementById('face-actions').style.display = 'none';
                document.getElementById('face-register-prompt').style.display = 'block';
            }
        } else {
            showMessage(data.error || 'Failed to load settings', 'error');
        }
    } catch (error) {
        console.error('Error loading settings:', error);
        showMessage('An error occurred while loading settings', 'error');
    }
}

async function toggleFaceRecognition() {
    const toggle = document.getElementById('face-toggle');
    const enabled = toggle.checked;
    
    try {
        const response = await fetch('/api/v1/settings/face-recognition', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ enabled })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(`Face recognition ${enabled ? 'enabled' : 'disabled'}`, 'success');
            
            // Reload settings
            setTimeout(() => {
                loadSettings();
            }, 1000);
        } else {
            showMessage(data.error || 'Failed to update settings', 'error');
            // Revert toggle
            toggle.checked = !enabled;
        }
    } catch (error) {
        console.error('Error updating settings:', error);
        showMessage('An error occurred while updating settings', 'error');
        // Revert toggle
        toggle.checked = !enabled;
    }
}

async function deleteFaceData() {
    if (!confirm('Are you sure you want to delete all your face data? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch('/api/v1/face/encodings', {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(`Deleted ${data.data.deleted_count} face encoding(s)`, 'success');
            
            // Reload settings
            setTimeout(() => {
                loadSettings();
            }, 1500);
        } else {
            showMessage(data.error || 'Failed to delete face data', 'error');
        }
    } catch (error) {
        console.error('Error deleting face data:', error);
        showMessage('An error occurred while deleting face data', 'error');
    }
}
