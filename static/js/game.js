// Game JavaScript Functions
class TreasureHuntGame {
    constructor() {
        this.initializeEventListeners();
        this.setupAnimations();
    }

    initializeEventListeners() {
        // Form submission handling
        const decryptionForm = document.querySelector('.decryption-form');
        if (decryptionForm) {
            decryptionForm.addEventListener('submit', this.handleFormSubmission.bind(this));
        }

        // Input validation
        const inputField = document.getElementById('input');
        if (inputField) {
            inputField.addEventListener('input', this.validateInput.bind(this));
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyboardShortcuts.bind(this));
    }

    handleFormSubmission(event) {
        const submitButton = event.target.querySelector('button[type="submit"]');
        const inputField = event.target.querySelector('#input');
        
        if (submitButton && inputField) {
            // Add loading state
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Đang xử lý...';
            submitButton.disabled = true;
            
            // Validate input before submission
            if (!this.validateInputValue(inputField.value, inputField.dataset.algorithm)) {
                event.preventDefault();
                this.showError('Vui lòng nhập dữ liệu hợp lệ!');
                this.resetSubmitButton(submitButton);
                return false;
            }
        }
    }

    validateInput(event) {
        const input = event.target;
        const algorithm = input.form.querySelector('input[name="algorithm"]').value;
        const isValid = this.validateInputValue(input.value, algorithm);
        
        // Visual feedback
        if (input.value.length > 0) {
            if (isValid) {
                input.classList.remove('is-invalid');
                input.classList.add('is-valid');
            } else {
                input.classList.remove('is-valid');
                input.classList.add('is-invalid');
            }
        } else {
            input.classList.remove('is-valid', 'is-invalid');
        }
    }

    validateInputValue(value, algorithm) {
        if (!value || value.trim() === '') return false;

        switch (algorithm) {
            case 'caesar':
                const num = parseInt(value);
                return !isNaN(num) && num >= 0 && num <= 25;
            
            case 'vigenere':
                return /^[a-zA-Z]+$/.test(value.trim());
            
            case 'rsa':
                // Check if it matches pattern (n, d)
                return /^\(\s*\d+\s*,\s*\d+\s*\)$/.test(value.trim());
            
            case 'aes':
                return value.trim().length > 0;
            
            default:
                return true;
        }
    }

    resetSubmitButton(button) {
        setTimeout(() => {
            button.innerHTML = '<i class="fas fa-key me-2"></i>Giải Mã';
            button.disabled = false;
        }, 1000);
    }

    handleKeyboardShortcuts(event) {
        // Alt + H for hint
        if (event.altKey && event.key === 'h') {
            event.preventDefault();
            const hintButton = document.querySelector('button[onclick*="getHint"]');
            if (hintButton) {
                hintButton.click();
            }
        }

        // Alt + I for algorithm info
        if (event.altKey && event.key === 'i') {
            event.preventDefault();
            const infoButton = document.querySelector('button[onclick*="showAlgorithmInfo"]');
            if (infoButton) {
                infoButton.click();
            }
        }

        // Enter to submit form when input is focused
        if (event.key === 'Enter' && event.target.id === 'input') {
            event.target.form.submit();
        }
    }

    setupAnimations() {
        // Animate cards on scroll
        this.setupScrollAnimations();
        
        // Add hover effects
        this.setupHoverEffects();
        
        // Initialize tooltips
        this.initializeTooltips();
    }

    setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                }
            });
        }, observerOptions);

        // Observe algorithm cards and other elements
        document.querySelectorAll('.algorithm-card, .game-card, .info-card').forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            observer.observe(card);
        });
    }

    setupHoverEffects() {
        // Add sparkle effect on hover for special elements
        document.querySelectorAll('.achievement-badge.special').forEach(badge => {
            badge.addEventListener('mouseenter', this.addSparkleEffect.bind(this));
        });

        // Add glow effect for buttons
        document.querySelectorAll('.btn-primary').forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.boxShadow = '0 0 20px rgba(255, 215, 0, 0.6)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.boxShadow = '';
            });
        });
    }

    addSparkleEffect(event) {
        const element = event.target;
        const rect = element.getBoundingClientRect();
        
        for (let i = 0; i < 5; i++) {
            setTimeout(() => {
                const sparkle = document.createElement('div');
                sparkle.innerHTML = '✨';
                sparkle.style.position = 'absolute';
                sparkle.style.left = (rect.left + Math.random() * rect.width) + 'px';
                sparkle.style.top = (rect.top + Math.random() * rect.height) + 'px';
                sparkle.style.pointerEvents = 'none';
                sparkle.style.zIndex = '1000';
                sparkle.style.animation = 'sparkle 1s linear forwards';
                
                document.body.appendChild(sparkle);
                
                setTimeout(() => {
                    if (sparkle.parentNode) {
                        sparkle.parentNode.removeChild(sparkle);
                    }
                }, 1000);
            }, i * 100);
        }
    }

    initializeTooltips() {
        // Add helpful tooltips
        const tooltipElements = [
            { selector: '.level-indicator.locked', text: 'Hoàn thành cấp độ trước để mở khóa' },
            { selector: '.level-indicator.current', text: 'Cấp độ hiện tại' },
            { selector: '.level-indicator.completed', text: 'Đã hoàn thành' }
        ];

        tooltipElements.forEach(item => {
            document.querySelectorAll(item.selector).forEach(element => {
                element.title = item.text;
            });
        });
    }

    showError(message) {
        // Create and show error toast
        const toast = document.createElement('div');
        toast.className = 'alert alert-danger alert-dismissible fade show position-fixed';
        toast.style.left = '50%';
        toast.style.bottom = '40px';
        toast.style.top = '';
        toast.style.transform = 'translateX(-50%)';
        toast.style.zIndex = '99999';
        toast.style.minWidth = '300px';
        toast.style.animation = 'slideUpBottom 0.5s ease-out';
        
        toast.innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 5000);
    }

    showSuccess(message) {
        // Create and show success toast
        const toast = document.createElement('div');
        toast.className = 'alert alert-success alert-dismissible fade show position-fixed';
        toast.style.left = '50%';
        toast.style.bottom = '40px';
        toast.style.top = '';
        toast.style.transform = 'translateX(-50%)';
        toast.style.zIndex = '99999';
        toast.style.minWidth = '300px';
        toast.style.animation = 'slideUpBottom 0.5s ease-out';
        
        toast.innerHTML = `
            <i class="fas fa-check-circle me-2"></i>
            ${message}
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 5000);
    }
}

// Enhanced hint function
function getHint(levelNum) {
    const hintContent = document.getElementById('hint-content');
    
    // Show loading state
    hintContent.innerHTML = `
        <div class="text-center">
            <i class="fas fa-spinner fa-spin me-2"></i>
            Đang tải gợi ý...
        </div>
    `;
    
    fetch(`/hint/${levelNum}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            hintContent.innerHTML = `
                <div class="alert alert-warning">
                    <i class="fas fa-lightbulb me-2"></i>
                    <strong>Gợi ý:</strong><br>
                    ${data.hint}
                </div>
            `;
            
            // Add animation
            hintContent.style.animation = 'fadeInUp 0.5s ease';
        })
        .catch(error => {
            console.error('Error:', error);
            hintContent.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Không thể tải gợi ý. Vui lòng thử lại!
                    <button onclick="getHint(${levelNum})" class="btn btn-sm btn-outline-danger ms-2">
                        <i class="fas fa-redo me-1"></i>Thử lại
                    </button>
                </div>
            `;
        });
}

// Enhanced algorithm explanation function
function showAlgorithmInfo(algorithm) {
    const modalContent = document.getElementById('modal-algorithm-content');
    const sidebarContent = document.getElementById('algorithm-explanation');
    
    // Show loading state
    const loadingHtml = `
        <div class="text-center">
            <i class="fas fa-spinner fa-spin me-2"></i>
            Đang tải thông tin thuật toán...
        </div>
    `;
    
    modalContent.innerHTML = loadingHtml;
    if (sidebarContent) {
        sidebarContent.innerHTML = loadingHtml;
    }
    
    fetch(`/explain/${algorithm}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const content = `
                <div class="algorithm-explanation">
                    ${data.explanation}
                    <div class="mt-3 p-3 bg-light rounded">
                        <h6><i class="fas fa-keyboard me-2"></i>Phím tắt:</h6>
                        <small class="text-muted">
                            Alt + H: Xem gợi ý | Alt + I: Thông tin thuật toán | Enter: Gửi kết quả
                        </small>
                    </div>
                </div>
            `;
            
            modalContent.innerHTML = content;
            if (sidebarContent) {
                sidebarContent.innerHTML = content;
            }
            
            // Show modal
            const modal = new bootstrap.Modal(document.getElementById('algorithmModal'));
            modal.show();
        })
        .catch(error => {
            console.error('Error:', error);
            const errorHtml = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Không thể tải thông tin thuật toán. Vui lòng thử lại!
                    <button onclick="showAlgorithmInfo('${algorithm}')" class="btn btn-sm btn-outline-danger ms-2">
                        <i class="fas fa-redo me-1"></i>Thử lại
                    </button>
                </div>
            `;
            
            modalContent.innerHTML = errorHtml;
            if (sidebarContent) {
                sidebarContent.innerHTML = errorHtml;
            }
        });
}

// CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideUpBottom {
        from {
            opacity: 0;
            transform: translateX(-50%) translateY(100px);
        }
        to {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
    }
    
    @keyframes sparkle {
        0% {
            opacity: 0;
            transform: scale(0) rotate(0deg);
        }
        50% {
            opacity: 1;
            transform: scale(1) rotate(180deg);
        }
        100% {
            opacity: 0;
            transform: scale(0) rotate(360deg);
        }
    }
`;
document.head.appendChild(style);

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const game = new TreasureHuntGame();
    
    // Add welcome message for first-time visitors
    if (!sessionStorage.getItem('welcomed')) {
        setTimeout(() => {
            const welcomeToast = document.createElement('div');
            welcomeToast.className = 'alert alert-info alert-dismissible fade show position-fixed';
            welcomeToast.style.left = '50%';
            welcomeToast.style.bottom = '40px';
            welcomeToast.style.top = '';
            welcomeToast.style.transform = 'translateX(-50%)';
            welcomeToast.style.zIndex = '99999';
            welcomeToast.style.minWidth = '350px';
            welcomeToast.style.animation = 'slideUpBottom 0.5s ease-out';
            
            welcomeToast.innerHTML = `
                <i class="fas fa-treasure-chest me-2"></i>
                <strong>Chào mừng đến với Kho Báu Mật Mã!</strong><br>
                Sử dụng phím tắt: Alt+H (gợi ý), Alt+I (thông tin thuật toán)
                <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
            `;
            
            document.body.appendChild(welcomeToast);
            sessionStorage.setItem('welcomed', 'true');
            
            setTimeout(() => {
                if (welcomeToast.parentNode) {
                    welcomeToast.remove();
                }
            }, 8000);
        }, 2000);
    }
});

// Export for potential module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TreasureHuntGame;
}
