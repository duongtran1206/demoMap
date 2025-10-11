// Admin Dashboard JavaScript with CRUD Operations
class GeoJSONManager {
    constructor() {
        this.currentEditId = null;
        this.init();
    }

    init() {
        this.loadStatistics();
        this.loadGeoJSONFiles();
        this.loadLayerControl();
        this.bindEvents();
    }

    bindEvents() {
        // File upload event
        const fileUpload = document.getElementById('file-upload');
        if (fileUpload) {
            fileUpload.addEventListener('change', (e) => this.handleFileUpload(e));
        }

        // CRUD Form event
        const crudForm = document.getElementById('crud-form');
        if (crudForm) {
            crudForm.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        // Modal close events
        window.addEventListener('click', (e) => {
            const modal = document.getElementById('crudModal');
            if (e.target === modal) {
                this.closeCrudModal();
            }
        });
    }

    async loadStatistics() {
        try {
            const response = await fetch('/api/geojson-files/');
            if (response.status === 403) {
                this.showMessage('Access denied - Admin authentication required', 'error');
                return;
            }

            const files = await response.json();
            
            const activeFiles = files.filter(f => f.is_active).length;
            const totalPoints = files.reduce((sum, f) => sum + f.feature_count, 0);
            
            document.getElementById('total-files').textContent = files.length;
            document.getElementById('active-files').textContent = activeFiles;
            document.getElementById('total-points').textContent = totalPoints.toLocaleString();
        } catch (error) {
            console.error('Error loading statistics:', error);
            this.showMessage('Error loading statistics', 'error');
        }
    }

    async loadGeoJSONFiles() {
        try {
            const response = await fetch('/api/geojson-files/');
            
            if (response.status === 403) {
                this.showMessage('Access denied - Admin authentication required', 'error');
                return;
            }
            
            const files = await response.json();
            
            const tbody = document.getElementById('geojson-list');
            tbody.innerHTML = '';
            
            if (files.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="7" style="text-align: center; padding: 40px; color: #666;">
                            No GeoJSON files uploaded yet.
                        </td>
                    </tr>
                `;
                return;
            }
            
            files.forEach(file => {
                const row = this.createFileTableRow(file);
                tbody.appendChild(row);
            });
            
        } catch (error) {
            console.error('Error loading files:', error);
            this.showMessage('Error loading files', 'error');
        }
    }

    createFileTableRow(file) {
        const row = document.createElement('tr');
        
        const createdDate = new Date(file.created_at).toLocaleDateString();
        const fileName = file.file ? file.file.split('/').pop() : 'N/A';
        
        row.innerHTML = `
            <td>${file.id}</td>
            <td class="file-name-cell" title="${file.name}">${file.name}</td>
            <td>${file.map_type === 'embed' ? 'Embed Map' : 'Embed VN Map'}</td>
            <td class="file-path-cell" title="${fileName}">${fileName}</td>
            <td>${file.feature_count || 0}</td>
            <td>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 20px; height: 20px; border-radius: 3px; border: 1px solid #ddd; background-color: ${file.color || '#FF0000'};"></div>
                    <span style="font-size: 0.8em; color: #666;">${file.color || '#FF0000'}</span>
                </div>
            </td>
            <td>
                <span class="status-${file.is_active ? 'active' : 'inactive'}">
                    ${file.is_active ? 'Active' : 'Inactive'}
                </span>
            </td>
            <td>${createdDate}</td>
            <td>
                <button class="action-btn btn-view" onclick="geoManager.viewFile(${file.id})" title="View">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="action-btn btn-edit" onclick="geoManager.editFile(${file.id})" title="Edit">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="action-btn btn-delete" onclick="geoManager.deleteFile(${file.id})" title="Delete">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        
        return row;
    }

    async loadLayerControl() {
        try {
            const response = await fetch('/api/map-layers/');
            
            if (response.status === 403) {
                this.showMessage('Access denied - Admin authentication required', 'error');
                return;
            }
            
            const layers = await response.json();
            
            const container = document.getElementById('layer-control-list');
            container.innerHTML = '';
            
            if (layers.length === 0) {
                container.innerHTML = '<p class="text-muted">No layers available.</p>';
                return;
            }
            
            layers.forEach(layer => {
                const item = this.createLayerItem(layer);
                container.appendChild(item);
            });
            
        } catch (error) {
            console.error('Error loading layers:', error);
            this.showMessage('Error loading layers', 'error');
        }
    }

    createLayerItem(layer) {
        const div = document.createElement('div');
        div.className = 'layer-item';
        div.innerHTML = `
            <div class="layer-info">
                <span class="layer-name">${layer.name}</span>
                <span class="layer-count">${layer.feature_count || 0} features</span>
            </div>
            <label class="switch">
                <input type="checkbox" ${layer.is_visible ? 'checked' : ''} 
                       onchange="geoManager.toggleLayer(${layer.id}, this.checked)">
                <span class="slider"></span>
            </label>
        `;
        return div;
    }

    // CRUD Operations
    showCreateModal() {
        // Show modal first
        const modal = document.getElementById('crudModal');
        if (!modal) {
            console.error('Modal element not found!');
            return;
        }
        modal.style.display = 'block';

        // Wait for modal to be displayed and elements to be available
        const setupModal = () => {
            console.log('Setting up create modal elements...');
            this.currentEditId = null;

            const elements = {
                modalTitle: document.getElementById('modal-title'),
                fileId: document.getElementById('file-id'),
                fileName: document.getElementById('file-name'),
                fileDesc: document.getElementById('file-description'),
                fileMapType: document.getElementById('file-map-type'),
                customSymbolInput: document.getElementById('file-custom-symbol'),
                geojsonFileInput: document.getElementById('geojson-file'),
                fileActive: document.getElementById('file-active'),
                uploadGroup: document.getElementById('file-upload-group'),
                submitBtn: document.getElementById('submit-btn')
            };

            // Check if all required elements exist
            const missingElements = Object.entries(elements).filter(([key, el]) => !el && key !== 'customSymbolInput');
            if (missingElements.length > 0) {
                console.error('Missing elements:', missingElements.map(([key]) => key));
                // Retry after a short delay
                setTimeout(setupModal, 50);
                return;
            }

            // Set up elements
            if (elements.modalTitle) elements.modalTitle.textContent = 'Add New GeoJSON File';
            if (elements.fileId) elements.fileId.value = '';
            if (elements.fileName) elements.fileName.value = '';
            if (elements.fileDesc) elements.fileDesc.value = '';
            if (elements.fileMapType) elements.fileMapType.value = 'embed';

            console.log('Custom symbol input element:', elements.customSymbolInput);
            if (elements.customSymbolInput) {
                elements.customSymbolInput.value = '';
                console.log('Set custom symbol input to empty');
            } else {
                console.warn('Custom symbol input not found - this may be expected if modal is still loading');
            }

            if (elements.geojsonFileInput) elements.geojsonFileInput.value = '';
            if (elements.fileActive) elements.fileActive.checked = true;
            if (elements.uploadGroup) elements.uploadGroup.style.display = 'block';
            if (elements.submitBtn) elements.submitBtn.textContent = 'Create';

            // Initialize custom symbol picker
            setTimeout(() => {
                if (typeof initializeCustomSymbolPicker === 'function') {
                    initializeCustomSymbolPicker(9); // Default to Caritas Symbol (ID 9)
                }
            }, 100);

            console.log('Create modal setup complete');
        };

        // Use multiple attempts to ensure elements are available
        requestAnimationFrame(() => {
            setTimeout(setupModal, 10);
        });
    }

    async editFile(id) {
        try {
            const response = await fetch(`/api/geojson-files/${id}/`);
            if (response.status === 403) {
                this.showMessage('Access denied - Admin authentication required', 'error');
                return;
            }
            
            const file = await response.json();
            
            // Show modal first
            document.getElementById('crudModal').style.display = 'block';

            // Small delay to ensure modal is rendered
            setTimeout(() => {
                this.currentEditId = id;
                document.getElementById('modal-title').textContent = 'Edit GeoJSON File';
                document.getElementById('file-id').value = file.id;
                document.getElementById('file-name').value = file.name || '';
                document.getElementById('file-description').value = file.description || '';
                document.getElementById('file-map-type').value = file.map_type || 'embed';
                
                const customSymbolInput = document.getElementById('file-custom-symbol');
                if (customSymbolInput) customSymbolInput.value = file.custom_symbol ? file.custom_symbol.id : '';

                document.getElementById('file-active').checked = file.is_active;

                // Update custom symbol picker if available
                if (window.customSymbolPicker) {
                    window.customSymbolPicker.setSymbol(file.custom_symbol ? file.custom_symbol.id : 9); // Default to Caritas Symbol (ID 9)
                } else {
                    // Initialize picker with current symbol
                    setTimeout(() => {
                        if (typeof initializeCustomSymbolPicker === 'function') {
                            initializeCustomSymbolPicker(file.custom_symbol ? file.custom_symbol.id : 9); // Default to Caritas Symbol (ID 9)
                        }
                    }, 100);
                }
                if (customSymbolInput) customSymbolInput.value = file.custom_symbol ? file.custom_symbol.id : '';

                document.getElementById('file-active').checked = file.is_active;
                document.getElementById('file-upload-group').style.display = 'none';
                document.getElementById('submit-btn').textContent = 'Update';
            }, 10);
        } catch (error) {
            console.error('Error loading file for edit:', error);
            this.showMessage('Error loading file details', 'error');
        }
    }

    async viewFile(id) {
        try {
            const response = await fetch(`/api/geojson-files/${id}/`);
            if (response.status === 403) {
                this.showMessage('Access denied - Admin authentication required', 'error');
                return;
            }
            
            const file = await response.json();
            
            const info = `File ID: ${file.id}
Name: ${file.name}
Description: ${file.description || 'No description'}
Features: ${file.feature_count || 0}
Color: ${file.color || '#FF0000'}
Active: ${file.is_active ? 'Yes' : 'No'}
Created: ${new Date(file.created_at).toLocaleString()}
Updated: ${new Date(file.updated_at).toLocaleString()}`;
            
            alert(info);
        } catch (error) {
            console.error('Error viewing file:', error);
            this.showMessage('Error loading file details', 'error');
        }
    }

    async deleteFile(id) {
        if (!confirm('Are you sure you want to delete this GeoJSON file? This action cannot be undone.')) {
            return;
        }

        try {
            const response = await fetch(`/api/geojson-files/${id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                    'Content-Type': 'application/json',
                },
            });

            if (response.status === 403) {
                this.showMessage('Access denied - Admin authentication required', 'error');
                return;
            }

            if (response.ok) {
                this.showMessage('File deleted successfully!', 'success');
                this.refreshData();
            } else {
                throw new Error('Failed to delete file');
            }
        } catch (error) {
            console.error('Error deleting file:', error);
            this.showMessage('Error deleting file', 'error');
        }
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append('name', document.getElementById('file-name').value);
        formData.append('description', document.getElementById('file-description').value);
        formData.append('map_type', document.getElementById('file-map-type').value);
        
        // Always use custom symbol
        formData.append('custom_symbol', document.getElementById('file-custom-symbol').value);
        formData.append('symbol', 'marker'); // Default emoji symbol (not used)
        
        formData.append('is_active', document.getElementById('file-active').checked);

        console.log('Form data before submit:', {
            name: document.getElementById('file-name').value,
            description: document.getElementById('file-description').value,
            map_type: document.getElementById('file-map-type').value,
            custom_symbol: document.getElementById('file-custom-symbol').value,
            is_active: document.getElementById('file-active').checked
        });

        const fileInput = document.getElementById('geojson-file');
        if (fileInput.files.length > 0) {
            formData.append('file', fileInput.files[0]);
        }

        try {
            let url, method;
            if (this.currentEditId) {
                url = `/api/geojson-files/${this.currentEditId}/`;
                method = 'PUT';
            } else {
                url = '/api/geojson-files/';
                method = 'POST';
            }

            const response = await fetch(url, {
                method: method,
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: formData
            });

            if (response.status === 403) {
                this.showMessage('Access denied - Admin authentication required', 'error');
                return;
            }

            if (response.ok) {
                this.showMessage(`File ${this.currentEditId ? 'updated' : 'created'} successfully!`, 'success');
                this.closeCrudModal();
                this.refreshData();
            } else {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Operation failed');
            }
        } catch (error) {
            console.error('Error saving file:', error);
            this.showMessage(`Error ${this.currentEditId ? 'updating' : 'creating'} file: ${error.message}`, 'error');
        }
    }

    async handleFileUpload(e) {
        const files = e.target.files;
        if (files.length === 0) return;

        for (let i = 0; i < files.length; i++) {
            await this.uploadSingleFile(files[i]);
        }

        e.target.value = ''; // Reset input
        this.refreshData();
    }

    async uploadSingleFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('name', file.name.replace(/\.[^/.]+$/, "")); // Remove extension
        formData.append('color', '#FF0000'); // Default color for drag&drop uploads
        formData.append('is_active', 'true');

        try {
            const response = await fetch('/api/geojson-files/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: formData
            });

            if (response.status === 403) {
                this.showMessage('Access denied - Admin authentication required', 'error');
                return;
            }

            if (response.ok) {
                this.showMessage(`File "${file.name}" uploaded successfully!`, 'success');
            } else {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Upload failed');
            }
        } catch (error) {
            console.error('Upload error:', error);
            this.showMessage(`Error uploading "${file.name}": ${error.message}`, 'error');
        }
    }

    // Layer Control Functions
    async toggleLayer(layerId, visible) {
        try {
            const response = await fetch(`/api/map-layers/${layerId}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({ is_visible: visible })
            });

            if (response.status === 403) {
                this.showMessage('Access denied - Admin authentication required', 'error');
                return;
            }

            if (!response.ok) {
                throw new Error('Failed to update layer visibility');
            }
        } catch (error) {
            console.error('Error toggling layer:', error);
            this.showMessage('Error updating layer visibility', 'error');
        }
    }

    async selectAllLayers() {
        try {
            const response = await fetch('/api/select-all-layers/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                }
            });

            if (response.status === 403) {
                this.showMessage('Access denied - Admin authentication required', 'error');
                return;
            }

            const result = await response.json();
            if (result.status === 'success') {
                this.showMessage('All layers selected!', 'success');
                this.loadLayerControl();
            }
        } catch (error) {
            console.error('Error selecting all layers:', error);
            this.showMessage('Error selecting all layers', 'error');
        }
    }

    async deselectAllLayers() {
        try {
            const response = await fetch('/api/deselect-all-layers/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                }
            });

            if (response.status === 403) {
                this.showMessage('Access denied - Admin authentication required', 'error');
                return;
            }

            const result = await response.json();
            if (result.status === 'success') {
                this.showMessage('All layers deselected!', 'success');
                this.loadLayerControl();
            }
        } catch (error) {
            console.error('Error deselecting all layers:', error);
            this.showMessage('Error deselecting all layers', 'error');
        }
    }

    // Utility Functions
    closeCrudModal() {
        document.getElementById('crudModal').style.display = 'none';
        this.currentEditId = null;
    }

    refreshData() {
        this.loadStatistics();
        this.loadGeoJSONFiles();
        this.loadLayerControl();
        this.notifyEmbeddedMaps();
    }

    notifyEmbeddedMaps() {
        // Create a custom event to notify any embedded maps on the same domain
        try {
            // Use localStorage to communicate with embedded maps
            const updateEvent = {
                type: 'map_data_updated',
                timestamp: new Date().getTime(),
                source: 'admin_dashboard'
            };
            
            localStorage.setItem('map_update_event', JSON.stringify(updateEvent));
            
            // Remove the event after a short time to avoid storage buildup
            setTimeout(() => {
                localStorage.removeItem('map_update_event');
            }, 1000);
        } catch (error) {
            console.log('Could not notify embedded maps:', error);
        }
    }

    refreshFileList() {
        this.loadGeoJSONFiles();
        this.showMessage('File list refreshed!', 'success');
    }

    getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : '';
    }

    showMessage(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            animation: slideInRight 0.3s ease;
        `;

        switch(type) {
            case 'success':
                alertDiv.style.background = '#28a745';
                break;
            case 'error':
                alertDiv.style.background = '#dc3545';
                break;
            case 'warning':
                alertDiv.style.background = '#ffc107';
                alertDiv.style.color = '#333';
                break;
            default:
                alertDiv.style.background = '#17a2b8';
        }

        alertDiv.textContent = message;
        document.body.appendChild(alertDiv);

        setTimeout(() => {
            alertDiv.style.animation = 'slideOutRight 0.3s ease forwards';
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.parentNode.removeChild(alertDiv);
                }
            }, 300);
        }, 3000);
    }
}

// Global Functions (for onclick handlers)
function showCreateModal() {
    geoManager.showCreateModal();
}

function closeCrudModal() {
    geoManager.closeCrudModal();
}

function selectAllLayers() {
    geoManager.selectAllLayers();
}

function deselectAllLayers() {
    geoManager.deselectAllLayers();
}

function refreshFileList() {
    geoManager.refreshFileList();
}

// Initialize the manager
let geoManager;
document.addEventListener('DOMContentLoaded', function() {
    geoManager = new GeoJSONManager();
    
    // Add symbol type toggle functionality
    document.addEventListener('change', function(e) {
        if (e.target.name === 'symbol_type') {
            const customGroup = document.getElementById('custom-symbol-group');
            const emojiGroup = document.getElementById('emoji-symbol-group');
            
            if (e.target.value === 'custom') {
                if (customGroup) customGroup.style.display = 'block';
                if (emojiGroup) emojiGroup.style.display = 'none';
                // Initialize custom symbol picker if not already done
                setTimeout(() => {
                    if (typeof initializeCustomSymbolPicker === 'function' && !window.customSymbolPicker) {
                        initializeCustomSymbolPicker(null);
                    }
                }, 100);
            } else if (e.target.value === 'emoji') {
                if (customGroup) customGroup.style.display = 'none';
                if (emojiGroup) emojiGroup.style.display = 'block';
                // Clear custom symbol value
                const customSymbolInput = document.getElementById('file-custom-symbol');
                if (customSymbolInput) customSymbolInput.value = '';
            }
        }
    });
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);