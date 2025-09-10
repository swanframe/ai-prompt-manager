/**
 * AI Prompt Manager - JavaScript Application
 */

// Global application object
const PromptManager = {
    // Initialize application
    init() {
        this.bindEvents();
        this.initTooltips();
        this.autoHideAlerts();
        this.initSearchFeatures();
    },

    // Bind global event listeners
    bindEvents() {
        // Confirm delete actions
        document.querySelectorAll('[data-confirm]').forEach(element => {
            element.addEventListener('click', this.handleConfirmAction);
        });

        // Auto-save form drafts
        document.querySelectorAll('form[data-autosave]').forEach(form => {
            this.initAutoSave(form);
        });

        // Handle AJAX forms
        document.querySelectorAll('form[data-ajax]').forEach(form => {
            form.addEventListener('submit', this.handleAjaxForm);
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyboardShortcuts);
    },

    // Initialize Bootstrap tooltips
    initTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    },

    // Auto-hide alert messages after 5 seconds
    autoHideAlerts() {
        document.querySelectorAll('.alert:not(.alert-permanent)').forEach(alert => {
            setTimeout(() => {
                if (alert && alert.parentNode) {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }
            }, 5000);
        });
    },

    // Initialize search features
    initSearchFeatures() {
        const searchInput = document.querySelector('input[name="q"]');
        if (searchInput) {
            // Add search suggestions (if needed)
            this.initSearchSuggestions(searchInput);
            
            // Clear search button
            this.addClearSearchButton(searchInput);
        }
    },

    // Handle confirmation dialogs
    handleConfirmAction(e) {
        const message = e.target.dataset.confirm || 'Are you sure?';
        if (!confirm(message)) {
            e.preventDefault();
        }
    },

    // Initialize auto-save for forms
    initAutoSave(form) {
        const formId = form.id || 'form_' + Date.now();
        const storageKey = 'autosave_' + formId;
        
        // Load saved data
        const savedData = this.loadFormData(storageKey);
        if (savedData) {
            this.populateForm(form, savedData);
        }

        // Save data on input
        form.addEventListener('input', () => {
            this.debounce(() => {
                const formData = this.serializeForm(form);
                this.saveFormData(storageKey, formData);
            }, 1000)();
        });

        // Clear saved data on successful submit
        form.addEventListener('submit', () => {
            setTimeout(() => {
                localStorage.removeItem(storageKey);
            }, 100);
        });
    },

    // Handle AJAX form submissions
    handleAjaxForm(e) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
        const button = form.querySelector('button[type="submit"]');
        
        // Show loading state
        const originalText = button.textContent;
        button.classList.add('loading');
        button.disabled = true;

        fetch(form.action, {
            method: form.method,
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.showNotification('Success!', 'success');
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
            } else {
                this.showNotification(data.error || 'An error occurred', 'error');
            }
        })
        .catch(error => {
            this.showNotification('Network error occurred', 'error');
            console.error('Error:', error);
        })
        .finally(() => {
            // Reset loading state
            button.classList.remove('loading');
            button.disabled = false;
            button.textContent = originalText;
        });
    },

    // Handle keyboard shortcuts
    handleKeyboardShortcuts(e) {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[name="q"]');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }

        // Escape to close modals
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modal = bootstrap.Modal.getInstance(openModal);
                if (modal) modal.hide();
            }
        }
    },

    // Add clear button to search input
    addClearSearchButton(searchInput) {
        if (searchInput.value) {
            const clearBtn = document.createElement('button');
            clearBtn.type = 'button';
            clearBtn.className = 'btn btn-link position-absolute end-0 top-50 translate-middle-y';
            clearBtn.style.zIndex = '10';
            clearBtn.innerHTML = '<i class="bi bi-x-circle"></i>';
            clearBtn.onclick = () => {
                searchInput.value = '';
                searchInput.focus();
                clearBtn.remove();
            };
            
            searchInput.parentNode.style.position = 'relative';
            searchInput.parentNode.appendChild(clearBtn);
        }
    },

    // Initialize search suggestions
    initSearchSuggestions(searchInput) {
        let timeout;
        searchInput.addEventListener('input', () => {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                const query = searchInput.value.trim();
                if (query.length >= 2) {
                    this.fetchSearchSuggestions(query);
                } else {
                    this.hideSuggestions();
                }
            }, 300);
        });
    },

    // Fetch search suggestions via API
    fetchSearchSuggestions(query) {
        fetch(`/prompts/api/search?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                if (data.results && data.results.length > 0) {
                    this.showSuggestions(data.results.slice(0, 5));
                } else {
                    this.hideSuggestions();
                }
            })
            .catch(() => this.hideSuggestions());
    },

    // Show search suggestions dropdown
    showSuggestions(suggestions) {
        // Implementation for showing search suggestions
        // This would create a dropdown with suggestions
    },

    // Hide search suggestions
    hideSuggestions() {
        const dropdown = document.getElementById('search-suggestions');
        if (dropdown) {
            dropdown.remove();
        }
    },

    // Show notification toast
    showNotification(message, type = 'info') {
        const toastContainer = document.querySelector('.toast-container') || this.createToastContainer();
        
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = `
            <div class="toast-header">
                <i class="bi bi-${this.getIconForType(type)} text-${type === 'error' ? 'danger' : type} me-2"></i>
                <strong class="me-auto">${this.capitalizeFirst(type)}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">${message}</div>
        `;
        
        toastContainer.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast after it's hidden
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    },

    // Create toast container if it doesn't exist
    createToastContainer() {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
        return container;
    },

    // Get icon for notification type
    getIconForType(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-triangle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    },

    // Utility: Capitalize first letter
    capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    },

    // Utility: Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Utility: Serialize form data
    serializeForm(form) {
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        return data;
    },

    // Utility: Populate form with data
    populateForm(form, data) {
        Object.keys(data).forEach(key => {
            const input = form.querySelector(`[name="${key}"]`);
            if (input) {
                input.value = data[key];
            }
        });
    },

    // Utility: Save form data to localStorage
    saveFormData(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
        } catch (e) {
            console.warn('Failed to save form data:', e);
        }
    },

    // Utility: Load form data from localStorage
    loadFormData(key) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : null;
        } catch (e) {
            console.warn('Failed to load form data:', e);
            return null;
        }
    }
};

// Character and word counter for textareas
function initTextareaCounters() {
    document.querySelectorAll('textarea[data-counter]').forEach(textarea => {
        const counter = document.getElementById(textarea.dataset.counter);
        if (counter) {
            const updateCounter = () => {
                const count = textarea.value.length;
                const max = textarea.maxLength || Infinity;
                counter.textContent = `${count}${max !== Infinity ? `/${max}` : ''} characters`;
                
                if (max !== Infinity && count > max * 0.9) {
                    counter.classList.add('text-warning');
                }
                if (count >= max) {
                    counter.classList.remove('text-warning');
                    counter.classList.add('text-danger');
                }
            };
            
            textarea.addEventListener('input', updateCounter);
            updateCounter(); // Initial count
        }
    });
}

// New Conversation Functions
async function copyConversation() {
    const items = document.querySelectorAll('#conversationList .conversation-item');
    let content = "";

    items.forEach((el, idx) => {
        const role = el.getAttribute('data-role') || 'unknown';
        const text = el.innerText.trim();
        content += `[${role.toUpperCase()}] ${text}`;
        if (idx < items.length - 1) content += '\n\n---\n\n';
    });

    try {
        await navigator.clipboard.writeText(content);
        new bootstrap.Toast(document.getElementById('copyToast')).show();
    } catch (e) {
        const ta = document.createElement('textarea');
        ta.value = content;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        new bootstrap.Toast(document.getElementById('copyToast')).show();
    }
}

function submitResponse(projectId, promptId) {
    const role = document.getElementById('respRole').value;
    const content = document.getElementById('respContent').value.trim();

    if (!content) return;

    fetch(`/responses/project/${projectId}/prompt/${promptId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ role, content })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('respContent').value = "";
        loadConversation(projectId, promptId);
    });
}

function loadConversation(projectId, promptId) {
    fetch(`/responses/project/${projectId}/prompt/${promptId}`)
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('conversationList');
            list.innerHTML = "";
            data.forEach(resp => {
                const div = document.createElement('div');
                div.className = 'conversation-item mb-2 p-2 border rounded';
                div.setAttribute('data-role', resp.role);
                div.innerHTML = `<strong>[${resp.role}]</strong><br>${resp.content}`;
                list.appendChild(div);
            });
        });
}
// End of new functions

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    PromptManager.init();
    initTextareaCounters();
});