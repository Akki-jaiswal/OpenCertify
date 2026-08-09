const form = document.getElementById('certForm');
const templateInput = document.getElementById('templateFile');
const sigInput = document.getElementById('signatureFile');
const previewImage = document.getElementById('previewImage');
const previewName = document.getElementById('previewName');
const previewDate = document.getElementById('previewDate');
const previewSig = document.getElementById('previewSignature');
const sandboxContainer = document.getElementById('sandboxContainer');

let imgNaturalWidth = 2000;
let imgNaturalHeight = 1500;

// Update Preview Background
templateInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            previewImage.src = event.target.result;
            
            // Get natural dimensions to set slider max limits
            const tempImg = new Image();
            tempImg.onload = function() {
                imgNaturalWidth = tempImg.width;
                imgNaturalHeight = tempImg.height;
                
                // Set aspect ratio of the sandbox to match image exactly
                sandboxContainer.style.aspectRatio = `${imgNaturalWidth} / ${imgNaturalHeight}`;
                
                document.getElementById('nameX').max = imgNaturalWidth;
                document.getElementById('nameY').max = imgNaturalHeight;
                document.getElementById('dateX').max = imgNaturalWidth;
                document.getElementById('dateY').max = imgNaturalHeight;
                document.getElementById('sigX').max = imgNaturalWidth;
                document.getElementById('sigY').max = imgNaturalHeight;
                
                // Auto-center the name on template load
                document.getElementById('nameX').value = imgNaturalWidth / 2;
                document.getElementById('nameY').value = imgNaturalHeight / 2 - 50;
                
                // Make default font size larger so it's readable on big images
                document.getElementById('nameFontSize').value = Math.floor(imgNaturalWidth / 15);
                
                updatePreview();
            };
            tempImg.src = event.target.result;
        };
        reader.readAsDataURL(file);
    }
});

// Update Signature Preview
sigInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            previewSig.src = event.target.result;
            previewSig.classList.remove('hidden');
            updatePreview();
        };
        reader.readAsDataURL(file);
    } else {
        previewSig.classList.add('hidden');
    }
});

// Attach listeners to all inputs
const inputsToWatch = ['nameX', 'nameY', 'nameFontSize', 'nameColor', 'dateText', 'dateX', 'dateY', 'dateFontSize', 'dateColor', 'sigX', 'sigY', 'sigScale', 'sigText', 'sigFontSize', 'sigColor'];
inputsToWatch.forEach(id => {
    document.getElementById(id).addEventListener('input', updatePreview);
});

function updatePreview() {
    const scaleFactor = sandboxContainer.clientWidth / imgNaturalWidth;

    // Name Update
    const nx = document.getElementById('nameX').value;
    const ny = document.getElementById('nameY').value;
    const nfs = document.getElementById('nameFontSize').value;
    const nc = document.getElementById('nameColor').value;
    
    // PIL centers text. In CSS, we translate -50% to emulate centering based on X.
    previewName.style.left = `${(nx / imgNaturalWidth) * 100}%`;
    previewName.style.top = `${(ny / imgNaturalHeight) * 100}%`;
    previewName.style.transform = `translateX(-50%)`;
    previewName.style.fontSize = `${nfs * scaleFactor}px`;
    previewName.style.color = nc;

    // Date Update
    const dText = document.getElementById('dateText').value;
    const dx = document.getElementById('dateX').value;
    const dy = document.getElementById('dateY').value;
    const dfs = document.getElementById('dateFontSize').value;
    const dc = document.getElementById('dateColor').value;

    if (dText.trim() !== "") {
        previewDate.classList.remove('hidden');
        previewDate.textContent = dText;
        previewDate.style.left = `${(dx / imgNaturalWidth) * 100}%`;
        previewDate.style.top = `${(dy / imgNaturalHeight) * 100}%`;
        previewDate.style.fontSize = `${dfs * scaleFactor}px`;
        previewDate.style.color = dc;
    } else {
        previewDate.classList.add('hidden');
    }

    // Signature Update
    const sx = document.getElementById('sigX').value;
    const sy = document.getElementById('sigY').value;
    const sScale = document.getElementById('sigScale').value;
    const sText = document.getElementById('sigText').value;
    const sfs = document.getElementById('sigFontSize').value;
    const sc = document.getElementById('sigColor').value;
    
    const previewSigText = document.getElementById('previewSigText');

    if (sText.trim() !== "") {
        // Use text signature
        previewSig.classList.add('hidden');
        previewSigText.classList.remove('hidden');
        previewSigText.textContent = sText;
        previewSigText.style.left = `${(sx / imgNaturalWidth) * 100}%`;
        previewSigText.style.top = `${(sy / imgNaturalHeight) * 100}%`;
        previewSigText.style.fontSize = `${sfs * scaleFactor}px`;
        previewSigText.style.color = sc;
    } else {
        // Use image signature if available
        previewSigText.classList.add('hidden');
        if (!previewSig.classList.contains('hidden') && sigInput.files.length > 0) {
            previewSig.style.left = `${(sx / imgNaturalWidth) * 100}%`;
            previewSig.style.top = `${(sy / imgNaturalHeight) * 100}%`;
            const sigActualWidth = previewSig.naturalWidth || 200;
            previewSig.style.width = `${sigActualWidth * sScale * scaleFactor}px`;
        }
    }
}

// Window resize needs to recalculate font sizes
window.addEventListener('resize', updatePreview);

// Prevent accidental submission on 'Enter' key press in inputs
form.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
        e.preventDefault();
    }
});

// Form Submission Logic
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = form.querySelector('.submit-btn');
    const progressContainer = document.getElementById('progressContainer');
    const terminal = document.getElementById('terminal');

    terminal.innerHTML = '';
    progressContainer.classList.remove('hidden');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Processing... ⏳';

    const formData = new FormData(form);

    try {
        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        
        if (data.status === 'error') {
            appendLog(`❌ Error: ${data.message}`);
            submitBtn.disabled = false;
            submitBtn.textContent = 'Generate & Send Emails 🚀';
            return;
        }

        appendLog('🚀 Process started! Connecting to backend...');
        
        const eventSource = new EventSource('/progress');
        
        eventSource.onmessage = function(event) {
            if (event.data !== 'ping') {
                appendLog(event.data);
                
                if (event.data.includes('✅ Process complete!') || event.data.includes('❌ Error:')) {
                    eventSource.close();
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Generate & Send Emails 🚀';
                }
            }
        };

        eventSource.onerror = function() {
            appendLog('⚠️ Lost connection to progress stream.');
            eventSource.close();
            submitBtn.disabled = false;
            submitBtn.textContent = 'Generate & Send Emails 🚀';
        };

    } catch (error) {
        appendLog(`❌ Network Error: ${error.message}`);
        submitBtn.disabled = false;
        submitBtn.textContent = 'Generate & Send Emails 🚀';
    }
});

function appendLog(message) {
    const terminal = document.getElementById('terminal');
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    logEntry.textContent = `> ${message}`;
    terminal.appendChild(logEntry);
    terminal.scrollTop = terminal.scrollHeight;
}

// Init preview once to apply default values
updatePreview();
