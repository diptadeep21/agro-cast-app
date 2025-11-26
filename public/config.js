// API Configuration for AgroCast
// This file is injected at build time by Amplify
// Set API_URL in Amplify Console > App settings > Environment variables

// For Amplify build-time injection, we'll use a script tag approach
window.AGROCAST_CONFIG = window.AGROCAST_CONFIG || {
    API_BASE: '' // Will be set from Amplify environment variable or default to empty
};

// Try to get API_URL from Amplify environment variable (set during build)
// Amplify injects environment variables as window._env or via build-time replacement
if (typeof window !== 'undefined') {
    // Check for Amplify-injected config
    if (window._env && window._env.API_URL) {
        window.AGROCAST_CONFIG.API_BASE = window._env.API_URL;
    }
    // Fallback: check for meta tag (we'll add this)
    const metaApiUrl = document.querySelector('meta[name="api-url"]');
    if (metaApiUrl && metaApiUrl.content) {
        window.AGROCAST_CONFIG.API_BASE = metaApiUrl.content;
    }
}

