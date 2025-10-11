// Custom Symbol Picker Component for uploaded images
class CustomSymbolPicker {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error('Custom symbol picker container not found:', containerId);
            return;
        }

        this.selectedSymbol = options.defaultSymbol || null;
        this.onSymbolChange = options.onSymbolChange || (() => {});
        this.showLabel = options.showLabel !== false;
        this.isOpen = false;
        this.symbols = [];

        this.init();
    }

    async init() {
        await this.loadSymbols();
        this.createSymbolPicker();
        this.bindEvents();
    }

    async loadSymbols() {
        try {
            const response = await fetch('/api/custom-symbols/');
            const data = await response.json();
            if (data.status === 'success') {
                this.symbols = data.symbols;
            }
        } catch (error) {
            console.error('Error loading custom symbols:', error);
            this.symbols = [];
        }
    }

    createSymbolPicker() {
        const selectedSymbolData = this.symbols.find(s => s.id === this.selectedSymbol);

        const html = `
            <div class="custom-symbol-picker">
                ${this.showLabel ? '<label class="custom-symbol-picker-label">Choose Custom Symbol</label>' : ''}

                <div class="custom-symbol-picker-header">
                    <div class="selected-custom-symbol-display">
                        <div class="selected-custom-symbol-icon">
                            ${selectedSymbolData ?
                                `<img src="${selectedSymbolData.image_url}" alt="${selectedSymbolData.name}" style="width: 24px; height: 24px; object-fit: contain;" />` :
                                '<div style="width: 24px; height: 24px; background: #f0f0f0; border: 1px solid #ccc; display: flex; align-items: center; justify-content: center; font-size: 12px;">📷</div>'
                            }
                        </div>
                        <span class="selected-custom-symbol-name">${selectedSymbolData ? selectedSymbolData.name : 'No symbol selected'}</span>
                        <div class="dropdown-arrow">▼</div>
                    </div>
                </div>

                <div class="custom-symbol-picker-dropdown" style="display: none;">
                    <div class="custom-symbol-search">
                        <input type="text" placeholder="Search symbols..." class="custom-symbol-search-input">
                    </div>

                    <div class="custom-symbol-grid">
                        ${this.symbols.map(symbol => `
                            <div class="custom-symbol-option ${symbol.id === this.selectedSymbol ? 'selected' : ''}"
                                 data-symbol-id="${symbol.id}"
                                 title="${symbol.name}">
                                <div class="custom-symbol-icon">
                                    <img src="${symbol.image_url}" alt="${symbol.name}" style="width: 40px; height: 40px; object-fit: contain; border-radius: 4px;" />
                                </div>
                                <span class="custom-symbol-name">${symbol.name}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;

        this.container.innerHTML = html;
    }

    bindEvents() {
        const header = this.container.querySelector('.custom-symbol-picker-header');
        const dropdown = this.container.querySelector('.custom-symbol-picker-dropdown');
        const searchInput = this.container.querySelector('.custom-symbol-search-input');

        // Toggle dropdown
        header.addEventListener('click', (e) => {
            if (!e.target.closest('.custom-symbol-option')) {
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

        // Symbol selection
        dropdown.addEventListener('click', (e) => {
            const symbolOption = e.target.closest('.custom-symbol-option');
            if (symbolOption && symbolOption.dataset.symbolId) {
                e.preventDefault();
                e.stopPropagation();
                const symbolId = parseInt(symbolOption.dataset.symbolId);
                this.selectSymbol(symbolId);
                return false;
            }
        });

        // Search functionality
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.filterSymbols(e.target.value);
            });

            searchInput.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        }

        // Prevent dropdown close when clicking inside
        dropdown.addEventListener('click', (e) => {
            e.stopPropagation();
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
        const dropdown = this.container.querySelector('.custom-symbol-picker-dropdown');
        const arrow = this.container.querySelector('.dropdown-arrow');

        dropdown.style.display = 'block';
        arrow.style.transform = 'rotate(180deg)';
        this.isOpen = true;

        // Focus search input
        const searchInput = this.container.querySelector('.custom-symbol-search-input');
        if (searchInput) {
            setTimeout(() => searchInput.focus(), 100);
        }
    }

    closeDropdown() {
        const dropdown = this.container.querySelector('.custom-symbol-picker-dropdown');
        const arrow = this.container.querySelector('.dropdown-arrow');

        dropdown.style.display = 'none';
        arrow.style.transform = 'rotate(0deg)';
        this.isOpen = false;

        // Clear search
        const searchInput = this.container.querySelector('.custom-symbol-search-input');
        if (searchInput) {
            searchInput.value = '';
            this.filterSymbols('');
        }
    }

    selectSymbol(symbolId) {
        const symbolData = this.symbols.find(s => s.id === symbolId);
        if (symbolData) {
            this.selectedSymbol = symbolId;
            this.updateSelectedDisplay();
            this.updateSelectionUI();
            this.onSymbolChange(symbolId, symbolData);
            this.closeDropdown();
        }
    }

    updateSelectedDisplay() {
        const iconDiv = this.container.querySelector('.selected-custom-symbol-icon');
        const name = this.container.querySelector('.selected-custom-symbol-name');
        const selectedSymbolData = this.symbols.find(s => s.id === this.selectedSymbol);

        if (iconDiv) {
            if (selectedSymbolData) {
                iconDiv.innerHTML = `<img src="${selectedSymbolData.image_url}" alt="${selectedSymbolData.name}" style="width: 24px; height: 24px; object-fit: contain;" />`;
            } else {
                iconDiv.innerHTML = '<div style="width: 24px; height: 24px; background: #f0f0f0; border: 1px solid #ccc; display: flex; align-items: center; justify-content: center; font-size: 12px;">📷</div>';
            }
        }

        if (name) {
            name.textContent = selectedSymbolData ? selectedSymbolData.name : 'No symbol selected';
        }
    }

    updateSelectionUI() {
        // Remove all selected classes
        this.container.querySelectorAll('.custom-symbol-option').forEach(option => {
            option.classList.remove('selected');
        });

        // Add selected class to current selection
        if (this.selectedSymbol) {
            const selectedOption = this.container.querySelector(`[data-symbol-id="${this.selectedSymbol}"]`);
            if (selectedOption) {
                selectedOption.classList.add('selected');
            }
        }
    }

    filterSymbols(searchTerm) {
        const term = searchTerm.toLowerCase().trim();
        const options = this.container.querySelectorAll('.custom-symbol-option');

        options.forEach(option => {
            const symbolName = option.querySelector('.custom-symbol-name').textContent.toLowerCase();
            const matches = !term || symbolName.includes(term);
            option.style.display = matches ? 'flex' : 'none';
        });
    }

    getSelectedSymbol() {
        return this.symbols.find(s => s.id === this.selectedSymbol) || null;
    }

    setSymbol(symbolId) {
        if (symbolId && this.symbols.find(s => s.id === symbolId)) {
            this.selectedSymbol = symbolId;
            this.updateSelectedDisplay();
            this.updateSelectionUI();
        } else {
            this.selectedSymbol = null;
            this.updateSelectedDisplay();
            this.updateSelectionUI();
        }
    }
}

// Initialize custom symbol picker
function initCustomSymbolPicker(containerId, options = {}) {
    return new CustomSymbolPicker(containerId, options);
}