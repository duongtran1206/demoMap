// OSM Symbol Picker Component
class OSMSymbolPicker {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error('Symbol picker container not found:', containerId);
            return;
        }
        
        this.selectedSymbol = options.defaultSymbol || 'marker';
        this.onSymbolChange = options.onSymbolChange || (() => {});
        this.showLabel = options.showLabel !== false;
        this.isOpen = false;
        
        this.init();
    }
    
    init() {
        this.createSymbolPicker();
        this.bindEvents();
        // Add symbol handlers after HTML is created
        setTimeout(() => this.addSymbolClickHandlers(), 100);
    }
    
    createSymbolPicker() {
        const selectedSymbolData = OSM_SYMBOLS[this.selectedSymbol] || OSM_SYMBOLS['marker'];
        
        const html = `
            <div class="symbol-picker">
                ${this.showLabel ? '<label class="symbol-picker-label">Choose Map Symbol</label>' : ''}
                
                <div class="symbol-picker-header">
                    <div class="selected-symbol-display">
                        <div class="selected-symbol-icon">
                            ${createSymbolIcon(this.selectedSymbol, 24)}
                        </div>
                        <span class="selected-symbol-name">${selectedSymbolData.name}</span>
                        <div class="dropdown-arrow">▼</div>
                    </div>
                </div>
                
                <div class="symbol-picker-dropdown" style="display: none;">
                    <div class="symbol-search">
                        <input type="text" placeholder="Search symbols..." class="symbol-search-input">
                    </div>
                    
                    <div class="symbol-categories">
                        ${this.renderCategories()}
                    </div>
                </div>
            </div>
        `;
        
        this.container.innerHTML = html;
    }
    
    renderCategories() {
        return Object.keys(SYMBOL_CATEGORIES).map(category => `
            <div class="symbol-category">
                <h4 class="symbol-category-title">${category}</h4>
                <div class="symbol-grid">
                    ${SYMBOL_CATEGORIES[category].map(symbol => `
                        <div class="symbol-option ${symbol.key === this.selectedSymbol ? 'selected' : ''}" 
                             data-symbol="${symbol.key}"
                             title="${symbol.name}">
                            <div class="symbol-icon">
                                ${createSymbolIcon(symbol.key, 32)}
                            </div>
                            <span class="symbol-name">${symbol.name}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `).join('');
    }
    
    bindEvents() {
        const header = this.container.querySelector('.symbol-picker-header');
        const dropdown = this.container.querySelector('.symbol-picker-dropdown');
        const searchInput = this.container.querySelector('.symbol-search-input');
        const arrow = this.container.querySelector('.dropdown-arrow');
        
        // Toggle dropdown
        header.addEventListener('click', (e) => {
            // Only toggle if not clicking on a symbol option
            if (!e.target.closest('.symbol-option')) {
                e.preventDefault();
                e.stopPropagation();
                this.toggleDropdown();
            }
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.container.contains(e.target)) {
                this.closeDropdown();
            }
        });
        
        // Symbol selection - use delegation on dropdown only
        dropdown.addEventListener('click', (e) => {
            const symbolOption = e.target.closest('.symbol-option');
            if (symbolOption && symbolOption.dataset.symbol) {
                e.preventDefault();
                e.stopPropagation();
                console.log('Symbol clicked:', symbolOption.dataset.symbol);
                this.selectSymbol(symbolOption.dataset.symbol);
                return false;
            }
        });
        
        // Search functionality
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.filterSymbols(e.target.value);
            });
            
            // Prevent closing dropdown when clicking in search
            searchInput.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        }
        
        // Prevent dropdown close when clicking inside
        dropdown.addEventListener('click', (e) => {
            e.stopPropagation();
        });
        
        // Alternative: Add direct click handlers to all symbol options
        this.addSymbolClickHandlers();
    }
    
    addSymbolClickHandlers() {
        const symbolOptions = this.container.querySelectorAll('.symbol-option');
        symbolOptions.forEach(option => {
            option.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const symbolKey = option.dataset.symbol;
                console.log('Direct click handler - symbol:', symbolKey);
                if (symbolKey) {
                    this.selectSymbol(symbolKey);
                }
            });
        });
    }
    
    toggleDropdown() {
        if (this.isOpen) {
            this.closeDropdown();
        } else {
            this.openDropdown();
        }
    }
    
    openDropdown() {
        const dropdown = this.container.querySelector('.symbol-picker-dropdown');
        const arrow = this.container.querySelector('.dropdown-arrow');
        
        dropdown.style.display = 'block';
        arrow.style.transform = 'rotate(180deg)';
        this.isOpen = true;
        
        // Focus search input
        const searchInput = this.container.querySelector('.symbol-search-input');
        if (searchInput) {
            setTimeout(() => searchInput.focus(), 100);
        }
    }
    
    closeDropdown() {
        const dropdown = this.container.querySelector('.symbol-picker-dropdown');
        const arrow = this.container.querySelector('.dropdown-arrow');
        
        dropdown.style.display = 'none';
        arrow.style.transform = 'rotate(0deg)';
        this.isOpen = false;
        
        // Clear search
        const searchInput = this.container.querySelector('.symbol-search-input');
        if (searchInput) {
            searchInput.value = '';
            this.filterSymbols('');
        }
    }
    
    selectSymbol(symbolKey) {
        console.log('selectSymbol called with:', symbolKey);
        console.log('OSM_SYMBOLS[symbolKey]:', OSM_SYMBOLS[symbolKey]);
        
        if (OSM_SYMBOLS[symbolKey]) {
            console.log('Symbol found, updating selection...');
            this.selectedSymbol = symbolKey;
            this.updateSelectedDisplay();
            this.updateSelectionUI();
            this.onSymbolChange(symbolKey, OSM_SYMBOLS[symbolKey]);
            this.closeDropdown();
            console.log('Selection updated to:', symbolKey);
        } else {
            console.error('Symbol not found:', symbolKey);
        }
    }
    
    updateSelectedDisplay() {
        const iconDiv = this.container.querySelector('.selected-symbol-icon');
        const name = this.container.querySelector('.selected-symbol-name');
        const selectedSymbolData = OSM_SYMBOLS[this.selectedSymbol];
        
        if (iconDiv) {
            iconDiv.innerHTML = createSymbolIcon(this.selectedSymbol, 24);
        }
        
        if (name) {
            name.textContent = selectedSymbolData.name;
        }
    }
    
    updateSelectionUI() {
        // Remove all selected classes
        this.container.querySelectorAll('.symbol-option').forEach(option => {
            option.classList.remove('selected');
        });
        
        // Add selected class to current selection
        const selectedOption = this.container.querySelector(`[data-symbol="${this.selectedSymbol}"]`);
        if (selectedOption) {
            selectedOption.classList.add('selected');
        }
    }
    
    filterSymbols(searchTerm) {
        const categories = this.container.querySelectorAll('.symbol-category');
        const term = searchTerm.toLowerCase().trim();
        
        categories.forEach(category => {
            const options = category.querySelectorAll('.symbol-option');
            let hasVisibleOptions = false;
            
            options.forEach(option => {
                const symbolName = option.querySelector('.symbol-name').textContent.toLowerCase();
                const matches = !term || symbolName.includes(term);
                
                option.style.display = matches ? 'flex' : 'none';
                if (matches) hasVisibleOptions = true;
            });
            
            category.style.display = hasVisibleOptions ? 'block' : 'none';
        });
    }
    
    getSelectedSymbol() {
        return {
            key: this.selectedSymbol,
            ...OSM_SYMBOLS[this.selectedSymbol]
        };
    }
    
    setSymbol(symbolKey) {
        if (OSM_SYMBOLS[symbolKey]) {
            this.selectedSymbol = symbolKey;
            this.updateSelectedDisplay();
            this.updateSelectionUI();
        }
    }
}

// Initialize symbol picker
function initSymbolPicker(containerId, options = {}) {
    return new OSMSymbolPicker(containerId, options);
}

// Debug: Check if OSM_SYMBOLS is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('OSM_SYMBOLS loaded:', typeof OSM_SYMBOLS !== 'undefined');
    console.log('Total symbols:', Object.keys(OSM_SYMBOLS || {}).length);
});