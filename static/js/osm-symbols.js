// OpenStreetMap Carto Symbols Library
const OSM_SYMBOLS = {
    // Amenities - Food & Drink
    'restaurant': {
        name: 'Restaurant',
        category: 'Food & Drink',
        icon: 'restaurant-15',
        color: '#734a08'
    },
    'cafe': {
        name: 'Cafe',
        category: 'Food & Drink', 
        icon: 'cafe-15',
        color: '#734a08'
    },
    'bar': {
        name: 'Bar',
        category: 'Food & Drink',
        icon: 'bar-15',
        color: '#734a08'
    },
    'fast_food': {
        name: 'Fast Food',
        category: 'Food & Drink',
        icon: 'fast-food-15',
        color: '#734a08'
    },
    
    // Shopping
    'shop': {
        name: 'Shop',
        category: 'Shopping',
        icon: 'shop-15',
        color: '#ac39ac'
    },
    'grocery': {
        name: 'Supermarket',
        category: 'Shopping',
        icon: 'grocery-15',
        color: '#ac39ac'
    },
    'clothing_store': {
        name: 'Clothing Store',
        category: 'Shopping',
        icon: 'clothing-store-15',
        color: '#ac39ac'
    },
    'car': {
        name: 'Car Dealership',
        category: 'Shopping',
        icon: 'car-15',
        color: '#ac39ac'
    },
    
    // Transportation
    'bus': {
        name: 'Bus Stop',
        category: 'Transportation',
        icon: 'bus-15',
        color: '#0066ff'
    },
    'rail': {
        name: 'Railway',
        category: 'Transportation',
        icon: 'rail-15',
        color: '#0066ff'
    },
    'parking': {
        name: 'Parking',
        category: 'Transportation',
        icon: 'parking-15',
        color: '#0066ff'
    },
    'airport': {
        name: 'Airport',
        category: 'Transportation',
        icon: 'airport-15',
        color: '#0066ff'
    },
    
    // Healthcare
    'hospital': {
        name: 'Hospital',
        category: 'Healthcare',
        icon: 'hospital-15',
        color: '#da0092'
    },
    'pharmacy': {
        name: 'Pharmacy',
        category: 'Healthcare',
        icon: 'pharmacy-15',
        color: '#da0092'
    },
    'dentist': {
        name: 'Dentist',
        category: 'Healthcare',
        icon: 'dentist-15',
        color: '#da0092'
    },
    'veterinary': {
        name: 'Veterinary',
        category: 'Healthcare',
        icon: 'veterinary-15',
        color: '#da0092'
    },
    
    // Education
    'school': {
        name: 'School',
        category: 'Education',
        icon: 'school-15',
        color: '#f4f11a'
    },
    'college': {
        name: 'University',
        category: 'Education',
        icon: 'college-15',
        color: '#f4f11a'
    },
    'library': {
        name: 'Library',
        category: 'Education',
        icon: 'library-15',
        color: '#f4f11a'
    },
    
    // Finance
    'bank': {
        name: 'Bank',
        category: 'Finance',
        icon: 'bank-15',
        color: '#734a08'
    },
    'atm': {
        name: 'ATM',
        category: 'Finance',
        icon: 'atm-15',
        color: '#734a08'
    },
    
    // Tourism & Lodging
    'lodging': {
        name: 'Hotel',
        category: 'Tourism',
        icon: 'lodging-15',
        color: '#0066ff'
    },
    'museum': {
        name: 'Museum',
        category: 'Tourism',
        icon: 'museum-15',
        color: '#734a08'
    },
    'attraction': {
        name: 'Tourist Attraction',
        category: 'Tourism',
        icon: 'attraction-15',
        color: '#734a08'
    },
    'campsite': {
        name: 'Campsite',
        category: 'Tourism',
        icon: 'campsite-15',
        color: '#0066ff'
    },
    
    // Services
    'post': {
        name: 'Post Office',
        category: 'Services',
        icon: 'post-15',
        color: '#f4f11a'
    },
    'police': {
        name: 'Police',
        category: 'Services',
        icon: 'police-15',
        color: '#da0092'
    },
    'fire_station': {
        name: 'Fire Station',
        category: 'Services',
        icon: 'fire-station-15',
        color: '#da0092'
    },
    'town_hall': {
        name: 'Town Hall',
        category: 'Services',
        icon: 'town-hall-15',
        color: '#734a08'
    },
    
    // Sports & Recreation
    'soccer': {
        name: 'Soccer Field',
        category: 'Sports',
        icon: 'soccer-15',
        color: '#39ac39'
    },
    'tennis': {
        name: 'Tennis Court',
        category: 'Sports',
        icon: 'tennis-15',
        color: '#39ac39'
    },
    'swimming': {
        name: 'Swimming',
        category: 'Sports',
        icon: 'swimming-15',
        color: '#39ac39'
    },
    'golf': {
        name: 'Golf Course',
        category: 'Sports',
        icon: 'golf-15',
        color: '#39ac39'
    },
    
    // Business & Office
    'commercial': {
        name: 'Business',
        category: 'Business',
        icon: 'commercial-15',
        color: '#007cff'
    },
    'industry': {
        name: 'Industry',
        category: 'Business',
        icon: 'industry-15',
        color: '#666666'
    },
    
    // Default
    'marker': {
        name: 'Default Marker',
        category: 'General',
        icon: 'marker-15',
        color: '#007cff'
    }
};

// Group symbols by category
const SYMBOL_CATEGORIES = {};
Object.keys(OSM_SYMBOLS).forEach(key => {
    const symbol = OSM_SYMBOLS[key];
    if (!SYMBOL_CATEGORIES[symbol.category]) {
        SYMBOL_CATEGORIES[symbol.category] = [];
    }
    SYMBOL_CATEGORIES[symbol.category].push({
        key: key,
        ...symbol
    });
});

// Function to get Maki icon URL
function getMakiIconUrl(iconName, size = 15, color = '007cff') {
    // Remove color hex prefix if present
    color = color.replace('#', '');
    return `https://api.mapbox.com/styles/v1/mapbox/streets-v11/sprite/maki-${iconName}@2x.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw`;
}

// Alternative: Use simple colored circles with symbols
function createSymbolIcon(symbolKey, size = 20) {
    const symbol = OSM_SYMBOLS[symbolKey] || OSM_SYMBOLS['marker'];
    const iconHtml = `
        <div style="
            width: ${size}px;
            height: ${size}px;
            background-color: ${symbol.color};
            border: 2px solid white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
            font-size: ${size * 0.6}px;
            color: white;
            font-weight: bold;
        ">
            ${getSymbolEmoji(symbolKey)}
        </div>
    `;
    return iconHtml;
}

// Emoji mapping for symbols
function getSymbolEmoji(symbolKey) {
    const emojiMap = {
        'restaurant': '🍽️',
        'cafe': '☕',
        'bar': '🍺',
        'fast_food': '🍔',
        'shop': '🛍️',
        'grocery': '🛒',
        'clothing_store': '👕',
        'car': '🚗',
        'bus': '🚌',
        'rail': '🚂',
        'parking': '🅿️',
        'airport': '✈️',
        'hospital': '🏥',
        'pharmacy': '💊',
        'dentist': '🦷',
        'veterinary': '🐕',
        'school': '🏫',
        'college': '🎓',
        'library': '📚',
        'bank': '🏦',
        'atm': '💰',
        'lodging': '🏨',
        'museum': '🏛️',
        'attraction': '📍',
        'campsite': '🏕️',
        'post': '📮',
        'police': '👮',
        'fire_station': '🚒',
        'town_hall': '🏛️',
        'soccer': '⚽',
        'tennis': '🎾',
        'swimming': '🏊',
        'golf': '⛳',
        'commercial': '🏢',
        'industry': '🏭',
        'marker': '📌'
    };
    return emojiMap[symbolKey] || '📌';
}