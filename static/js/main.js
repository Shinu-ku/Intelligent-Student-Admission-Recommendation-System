/* Main Interactivity & DigiLocker Prototype Script */

document.addEventListener('DOMContentLoaded', function() {
    // 1. Toast / Alert Auto-dismiss after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // 2. Multi-Step Form Navigation in Application Page
    const wizardForm = document.getElementById('applicationWizardForm');
    if (wizardForm) {
        let currentStep = 1;
        const totalSteps = 5;

        const btnNext = document.getElementById('btnWizardNext');
        const btnPrev = document.getElementById('btnWizardPrev');
        const btnSubmit = document.getElementById('btnWizardSubmit');

        function updateWizardUI() {
            for (let i = 1; i <= totalSteps; i++) {
                const stepElement = document.getElementById(`wizardStep${i}`);
                const stepIndicator = document.getElementById(`indicatorStep${i}`);
                
                if (stepElement) {
                    stepElement.style.display = (i === currentStep) ? 'block' : 'none';
                }
                
                if (stepIndicator) {
                    if (i < currentStep) {
                        stepIndicator.className = 'tracker-step completed';
                        stepIndicator.innerHTML = '<i class="fas fa-check"></i>';
                    } else if (i === currentStep) {
                        stepIndicator.className = 'tracker-step active';
                        stepIndicator.innerHTML = i;
                    } else {
                        stepIndicator.className = 'tracker-step';
                        stepIndicator.innerHTML = i;
                    }
                }
            }

            if (btnPrev) btnPrev.style.display = (currentStep === 1) ? 'none' : 'inline-block';
            if (btnNext) btnNext.style.display = (currentStep === totalSteps) ? 'none' : 'inline-block';
            if (btnSubmit) btnSubmit.style.display = (currentStep === totalSteps) ? 'inline-block' : 'none';
        }

        if (btnNext) {
            btnNext.addEventListener('click', function() {
                if (validateCurrentStep(currentStep)) {
                    currentStep++;
                    updateWizardUI();
                }
            });
        }

        if (btnPrev) {
            btnPrev.addEventListener('click', function() {
                currentStep--;
                updateWizardUI();
            });
        }

        function validateCurrentStep(step) {
            const currentStepDiv = document.getElementById(`wizardStep${step}`);
            if (!currentStepDiv) return true;
            const requiredInputs = currentStepDiv.querySelectorAll('[required]');
            let isValid = true;

            requiredInputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('is-invalid');
                    isValid = false;
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                alert('Please fill in all mandatory fields before proceeding to the next step.');
            }
            return isValid;
        }

        updateWizardUI();
    }

    // 3. DigiLocker Prototype Verification AJAX handler
    window.triggerDigiLockerSim = function(docType) {
        const statusContainer = document.getElementById(`digiStatus_${docType.replace(/\s+/g, '_')}`);
        if (statusContainer) {
            statusContainer.innerHTML = '<span class="text-warning"><i class="fas fa-spinner fa-spin me-1"></i> Connecting to DigiLocker API...</span>';
        }

        fetch('/documents/digilocker-verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ document_type: docType })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                setTimeout(() => {
                    location.reload();
                }, 1200);
            } else {
                alert(data.message || 'DigiLocker verification failed.');
            }
        })
        .catch(err => {
            console.error('DigiLocker Error:', err);
            alert('Unable to connect to DigiLocker prototype service.');
        });
    };
});
