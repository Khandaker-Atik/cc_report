// Professional Interactive Features for Community Clinic App

// Subtle UI Enhancement Functions
document.addEventListener('DOMContentLoaded', function() {
    // Add subtle fade-in to cards with intersection observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1, rootMargin: '20px' });

    const cards = document.querySelectorAll('.pro-card, .result-card, .chart-container');
    cards.forEach((card, index) => {
        card.classList.add('fade-in');
        observer.observe(card);
    });

    // Add subtle hover effects to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-1px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Form validation enhancement
    const formControls = document.querySelectorAll('.form-control');
    formControls.forEach(control => {
        control.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        control.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
            if (this.value.trim() !== '') {
                this.parentElement.classList.add('has-value');
            } else {
                this.parentElement.classList.remove('has-value');
            }
        });
    });

    // Add loading spinner to form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn && !submitBtn.classList.contains('loading')) {
                submitBtn.classList.add('loading');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner"></span>Processing...';
                
                // Restore button after 5 seconds if form doesn't redirect
                setTimeout(() => {
                    if (submitBtn.classList.contains('loading')) {
                        submitBtn.classList.remove('loading');
                        submitBtn.innerHTML = originalText;
                    }
                }, 5000);
            }
        });
    });
});

// Name Generator specific functions
function refreshNames() {
    const refreshBtn = document.querySelector('[onclick="refreshNames()"]');
    if (refreshBtn) {
        const originalText = refreshBtn.innerHTML;
        refreshBtn.innerHTML = '<span class="spinner"></span>Refreshing...';
        refreshBtn.disabled = true;
        
        fetch('/refresh-names')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update the status indicator
                    const statusIndicator = document.querySelector('.status-indicator');
                    if (statusIndicator) {
                        statusIndicator.innerHTML = `
                            <div class="status-dot bg-green-500"></div>
                            Connected to Google Sheets: ${data.male_count} male names, ${data.female_count} female names
                        `;
                        statusIndicator.className = 'status-indicator status-success';
                    }
                    
                    // Show success message
                    showNotification('Names refreshed successfully!', 'success');
                } else {
                    showNotification('Failed to refresh names: ' + data.message, 'error');
                }
            })
            .catch(error => {
                showNotification('Error refreshing names', 'error');
                console.error('Error:', error);
            })
            .finally(() => {
                refreshBtn.innerHTML = originalText;
                refreshBtn.disabled = false;
            });
    }
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notif => notif.remove());
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm`;
    
    const bgColor = {
        'success': 'bg-green-500',
        'error': 'bg-red-500',
        'warning': 'bg-yellow-500',
        'info': 'bg-blue-500'
    }[type] || 'bg-blue-500';
    
    notification.classList.add(bgColor, 'text-white');
    notification.innerHTML = `
        <div class="flex items-center">
            <span class="flex-1">${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-white opacity-70 hover:opacity-100">×</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Chart subtle enhancements
function animateChart(chartElement) {
    if (chartElement && typeof Chart !== 'undefined') {
        const ctx = chartElement.getContext('2d');
        // Add subtle animation configuration for Chart.js if used
        const originalOptions = chartElement.chart?.options || {};
        if (chartElement.chart) {
            chartElement.chart.options.animation = {
                duration: 800,
                easing: 'easeOutQuart'
            };
            chartElement.chart.update();
        }
    }
}

// Enhanced table interactions
function enhanceTable(table) {
    if (!table) return;
    
    // Add sorting capability to headers
    const headers = table.querySelectorAll('th');
    headers.forEach((header, index) => {
        header.style.cursor = 'pointer';
        header.style.userSelect = 'none';
        header.addEventListener('click', () => sortTable(table, index));
    });
    
    // Add row highlighting
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8fafc';
            this.style.transform = 'scale(1.01)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
            this.style.transform = 'scale(1)';
        });
    });
}

// Simple table sorting function
function sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    if (!tbody) return;
    
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const isNumeric = !isNaN(parseFloat(rows[0]?.cells[columnIndex]?.textContent));
    
    rows.sort((a, b) => {
        const aVal = a.cells[columnIndex]?.textContent.trim();
        const bVal = b.cells[columnIndex]?.textContent.trim();
        
        if (isNumeric) {
            return parseFloat(aVal) - parseFloat(bVal);
        } else {
            return aVal.localeCompare(bVal);
        }
    });
    
    // Clear tbody and append sorted rows
    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));
}

// Form auto-save functionality (optional)
function enableAutoSave(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('change', function() {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            localStorage.setItem(`autosave_${formId}`, JSON.stringify(data));
        });
    });
    
    // Restore saved data on page load
    const savedData = localStorage.getItem(`autosave_${formId}`);
    if (savedData) {
        try {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(key => {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) {
                    input.value = data[key];
                }
            });
        } catch (e) {
            console.error('Error restoring form data:', e);
        }
    }
}

// Progressive Enhancement
function progressivelyEnhance() {
    // Enhance all tables
    document.querySelectorAll('.pro-table').forEach(enhanceTable);
    
    // Animate charts if present
    document.querySelectorAll('canvas').forEach(animateChart);
    
    // Add subtle intersection observer for scroll effects
    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.2 });
    
    document.querySelectorAll('.slide-up').forEach(el => {
        scrollObserver.observe(el);
    });
}

// Initialize progressive enhancements when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', progressivelyEnhance);
} else {
    progressivelyEnhance();
}

// Export functions for global use
window.refreshNames = refreshNames;
window.showNotification = showNotification;
window.enhanceTable = enhanceTable;
window.enableAutoSave = enableAutoSave;