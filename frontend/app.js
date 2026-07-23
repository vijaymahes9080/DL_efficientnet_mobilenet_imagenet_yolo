/**
 * NEURAL SYNERGY - MULTI-MODEL EMOTION RECOGNITION ENGINE
 * Client-side Controller & Interactive Engine
 */

document.addEventListener('DOMContentLoaded', () => {
    // --- CONSTANTS & STATE ---
    const CLASS_NAMES = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise'];
    const EMOTION_COLORS = {
        'Angry': '#ef4444',
        'Disgust': '#10b981',
        'Fear': '#a855f7',
        'Happy': '#eab308',
        'Neutral': '#94a3b8',
        'Sad': '#3b82f6',
        'Surprise': '#f97316'
    };

    let currentTab = 'tab-hud';
    let isCameraRunning = false;
    let cameraStream = null;
    let cameraInterval = null;
    let lastFrameTime = Date.now();

    let loadedImageB64 = null;
    let lastPredictionResponse = null;
    let predictChartInstance = null;
    let analyticsAccChart = null;
    let analyticsLogLossChart = null;

    // --- DOM ELEMENTS ---
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    // HUD Elements
    const btnToggleCam = document.getElementById('btn-toggle-cam');
    const webcamVideo = document.getElementById('webcam-video');
    const hudCanvas = document.getElementById('hud-canvas');
    const camPlaceholder = document.getElementById('cam-placeholder');
    const hudModelSelect = document.getElementById('hud-model-select');
    const hudFpsCounter = document.getElementById('hud-fps-counter');
    const hudLatencyCounter = document.getElementById('hud-latency-counter');
    const hudDomLabel = document.getElementById('hud-dom-label');
    const hudDomConf = document.getElementById('hud-dom-conf');
    const hudBarsContainer = document.getElementById('hud-bars-container');

    // Predictor Elements
    const dropzone = document.getElementById('image-dropzone');
    const fileInput = document.getElementById('file-input');
    const btnBrowse = document.getElementById('btn-browse');
    const btnRunPredict = document.getElementById('btn-run-predict');
    const predictorModelSelect = document.getElementById('predictor-model-select');
    const imagePreview = document.getElementById('image-preview');
    const previewCanvas = document.getElementById('preview-canvas');
    const previewPlaceholder = document.getElementById('preview-placeholder');
    const predictTimeBadge = document.getElementById('predict-time-badge');
    const consensusEmotionText = document.getElementById('consensus-emotion-text');
    const consensusConfText = document.getElementById('consensus-conf-text');
    const presetBtns = document.querySelectorAll('.preset-btn');

    // Arena Elements
    const arenaGrid = document.getElementById('arena-grid');

    // XAI Elements
    const xaiOpacity = document.getElementById('xai-opacity');
    const xaiOpacityVal = document.getElementById('xai-opacity-val');
    const xaiBaseImg = document.getElementById('xai-base-img');
    const xaiOverlayImg = document.getElementById('xai-overlay-img');
    const xaiPlaceholder = document.getElementById('xai-placeholder');

    // --- INITIALIZATION ---
    initSidebarBars();
    initTabNavigation();
    initWebcam();
    initPredictor();
    initXAIControls();
    initAnalyticsCharts();

    // --------------------------------------------------------------------------
    // TAB NAVIGATION
    // --------------------------------------------------------------------------
    function initTabNavigation() {
        tabButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetTab = btn.getAttribute('data-tab');
                if (targetTab === currentTab) return;

                tabButtons.forEach(b => b.classList.remove('active'));
                tabContents.forEach(c => c.classList.remove('active'));

                btn.classList.add('active');
                document.getElementById(targetTab).classList.add('active');
                currentTab = targetTab;

                // Stop camera if switching away from HUD
                if (currentTab !== 'tab-hud' && isCameraRunning) {
                    stopCamera();
                }
            });
        });
    }

    // --------------------------------------------------------------------------
    // TAB 1: LIVE HUD WEBCAM INFERENCE
    // --------------------------------------------------------------------------
    function initSidebarBars() {
        hudBarsContainer.innerHTML = '';
        CLASS_NAMES.forEach(name => {
            const row = document.createElement('div');
            row.className = 'prob-row';
            row.innerHTML = `
                <div class="prob-meta">
                    <span class="name" style="color: ${EMOTION_COLORS[name]}">${name}</span>
                    <span class="val" id="hud-val-${name}">0.0%</span>
                </div>
                <div class="prob-track">
                    <div class="prob-fill" id="hud-fill-${name}" style="background-color: ${EMOTION_COLORS[name]}"></div>
                </div>
            `;
            hudBarsContainer.appendChild(row);
        });
    }

    function initWebcam() {
        btnToggleCam.addEventListener('click', () => {
            if (isCameraRunning) {
                stopCamera();
            } else {
                startCamera();
            }
        });
    }

    async function startCamera() {
        try {
            cameraStream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480, facingMode: 'user' }
            });
            webcamVideo.srcObject = cameraStream;
            await webcamVideo.play();

            isCameraRunning = true;
            camPlaceholder.style.display = 'none';
            btnToggleCam.innerHTML = '<i class="fa-solid fa-power-off"></i> Stop Camera';
            btnToggleCam.classList.replace('primary', 'secondary');

            // Set canvas dimensions to match video
            hudCanvas.width = webcamVideo.videoWidth || 640;
            hudCanvas.height = webcamVideo.videoHeight || 480;

            // Start frame capture loop
            cameraInterval = setInterval(processWebcamFrame, 120);
        } catch (err) {
            alert('Failed accessing webcam: ' + err.message);
        }
    }

    function stopCamera() {
        if (cameraInterval) clearInterval(cameraInterval);
        if (cameraStream) {
            cameraStream.getTracks().forEach(track => track.stop());
        }
        isCameraRunning = false;
        camPlaceholder.style.display = 'flex';
        btnToggleCam.innerHTML = '<i class="fa-solid fa-power-off"></i> Start Camera';
        btnToggleCam.classList.replace('secondary', 'primary');
        const ctx = hudCanvas.getContext('2d');
        ctx.clearRect(0, 0, hudCanvas.width, hudCanvas.height);
    }

    async function processWebcamFrame() {
        if (!isCameraRunning) return;

        const now = Date.now();
        const fps = Math.round(1000 / (now - lastFrameTime));
        lastFrameTime = now;
        hudFpsCounter.innerText = `FPS: ${fps}`;

        // Draw current video frame to offscreen canvas
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = hudCanvas.width;
        tempCanvas.height = hudCanvas.height;
        const tempCtx = tempCanvas.getContext('2d');
        tempCtx.drawImage(webcamVideo, 0, 0, tempCanvas.width, tempCanvas.height);

        const frameB64 = tempCanvas.toDataURL('image/jpeg', 0.8);
        const selectedModel = hudModelSelect.value;

        try {
            const res = await fetch('/api/predict_frame', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ frame: frameB64, model: selectedModel })
            });
            const data = await res.json();

            if (data.status === 'success') {
                hudLatencyCounter.innerText = `Latency: ${data.latency_ms} ms`;
                renderHUDOverlay(data);
            }
        } catch (err) {
            console.error('Frame prediction error:', err);
        }
    }

    function renderHUDOverlay(data) {
        const ctx = hudCanvas.getContext('2d');
        ctx.clearRect(0, 0, hudCanvas.width, hudCanvas.height);

        if (data.face_detected && data.bounding_box) {
            const [x, y, w, h] = data.bounding_box;
            const emotion = data.dominant_emotion;
            const conf = data.confidence;
            const color = EMOTION_COLORS[emotion] || '#00f2fe';

            // Draw bounding box
            ctx.strokeStyle = color;
            ctx.lineWidth = 3;
            ctx.strokeRect(x, y, w, h);

            // Draw label pill
            ctx.fillStyle = color;
            ctx.fillRect(x, y - 28, Math.max(140, w), 28);

            ctx.fillStyle = '#000000';
            ctx.font = 'bold 14px Outfit, sans-serif';
            ctx.fillText(`${emotion.toUpperCase()} (${conf}%)`, x + 8, y - 9);

            // Update sidebar dominant display
            hudDomLabel.innerText = emotion.toUpperCase();
            hudDomLabel.style.color = color;
            hudDomConf.innerText = `${conf}% Confidence (${data.latency_ms} ms)`;

            // Update sidebar bars
            CLASS_NAMES.forEach(name => {
                const probVal = data.probabilities[name] || 0;
                document.getElementById(`hud-val-${name}`).innerText = `${probVal}%`;
                document.getElementById(`hud-fill-${name}`).style.width = `${probVal}%`;
            });
        }
    }

    // --------------------------------------------------------------------------
    // TAB 2: IMAGE PREDICTOR LAB & ARENA
    // --------------------------------------------------------------------------
    function initPredictor() {
        btnBrowse.addEventListener('click', () => fileInput.click());

        fileInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files[0]) {
                handleFileSelect(e.target.files[0]);
            }
        });

        dropzone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropzone.style.borderColor = '#00f2fe';
        });

        dropzone.addEventListener('dragleave', () => {
            dropzone.style.borderColor = 'rgba(0, 242, 254, 0.3)';
        });

        dropzone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropzone.style.borderColor = 'rgba(0, 242, 254, 0.3)';
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                handleFileSelect(e.dataTransfer.files[0]);
            }
        });

        presetBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const preset = btn.getAttribute('data-preset');
                loadPresetSample(preset);
            });
        });

        btnRunPredict.addEventListener('click', runInference);
    }

    function handleFileSelect(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            loadedImageB64 = e.target.result;
            imagePreview.src = loadedImageB64;
            imagePreview.classList.remove('preview-hidden');
            previewPlaceholder.style.display = 'none';
            btnRunPredict.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    function loadPresetSample(preset) {
        // Generate high quality face canvas drawing as preset
        const canvas = document.createElement('canvas');
        canvas.width = 300;
        canvas.height = 300;
        const ctx = canvas.getContext('2d');

        // Background
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(0, 0, 300, 300);

        // Face outline
        ctx.beginPath();
        ctx.arc(150, 150, 90, 0, Math.PI * 2);
        ctx.fillStyle = '#fde047';
        ctx.fill();

        // Eyes
        ctx.fillStyle = '#000000';
        ctx.beginPath();
        ctx.arc(115, 130, 10, 0, Math.PI * 2);
        ctx.arc(185, 130, 10, 0, Math.PI * 2);
        ctx.fill();

        // Mouth based on preset emotion
        ctx.beginPath();
        ctx.lineWidth = 6;
        ctx.strokeStyle = '#000000';

        if (preset === 'happy') {
            ctx.arc(150, 160, 50, 0.1 * Math.PI, 0.9 * Math.PI, false);
        } else if (preset === 'angry') {
            ctx.arc(150, 200, 40, 1.1 * Math.PI, 1.9 * Math.PI, false);
            // Eyebrows
            ctx.lineWidth = 5;
            ctx.moveTo(100, 110); ctx.lineTo(130, 125);
            ctx.moveTo(200, 110); ctx.lineTo(170, 125);
            ctx.stroke();
        } else if (preset === 'surprise') {
            ctx.arc(150, 180, 20, 0, Math.PI * 2);
            ctx.fill();
        } else if (preset === 'sad') {
            ctx.arc(150, 200, 45, 1.1 * Math.PI, 1.9 * Math.PI, false);
        }
        ctx.stroke();

        loadedImageB64 = canvas.toDataURL('image/jpeg');
        imagePreview.src = loadedImageB64;
        imagePreview.classList.remove('preview-hidden');
        previewPlaceholder.style.display = 'none';
        btnRunPredict.disabled = false;

        runInference();
    }

    async function runInference() {
        if (!loadedImageB64) return;

        btnRunPredict.disabled = true;
        btnRunPredict.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing Neural Layers...';

        const selectedModel = predictorModelSelect.value;

        try {
            const res = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: loadedImageB64, model: selectedModel })
            });
            const data = await res.json();

            if (data.status === 'success') {
                lastPredictionResponse = data;
                renderPredictionResults(data);
                renderArenaResults(data);
                setupXAIDisplay(data);
            }
        } catch (err) {
            alert('Prediction request failed: ' + err.message);
        } finally {
            btnRunPredict.disabled = false;
            btnRunPredict.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Run Neural Inference';
        }
    }

    function renderPredictionResults(data) {
        predictTimeBadge.innerText = `${data.total_latency_ms} ms`;
        const consensus = data.consensus;
        const color = EMOTION_COLORS[consensus.emotion] || '#00f2fe';

        consensusEmotionText.innerText = consensus.emotion.toUpperCase();
        consensusEmotionText.style.color = color;
        consensusConfText.innerText = `${consensus.confidence}% Confidence`;
        consensusConfText.style.backgroundColor = color;

        // Render probability chart
        const ctx = document.getElementById('predict-chart').getContext('2d');
        if (predictChartInstance) predictChartInstance.destroy();

        const probsData = CLASS_NAMES.map(name => consensus.probabilities[name] || 0);

        predictChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: CLASS_NAMES,
                datasets: [{
                    label: 'Probability (%)',
                    data: probsData,
                    backgroundColor: CLASS_NAMES.map(name => EMOTION_COLORS[name]),
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
                    y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' }, max: 100 }
                }
            }
        });
    }

    // --------------------------------------------------------------------------
    // TAB 3: 4-MODEL HEAD-TO-HEAD ARENA
    // --------------------------------------------------------------------------
    function renderArenaResults(data) {
        arenaGrid.innerHTML = '';
        const results = data.model_results;

        Object.keys(results).forEach(key => {
            const m = results[key];
            const color = EMOTION_COLORS[m.dominant_emotion] || '#00f2fe';

            const card = document.createElement('div');
            card.className = 'arena-card';
            card.innerHTML = `
                <div class="arena-card-header">
                    <h4>${m.name}</h4>
                    <span style="font-size: 11px; color: #94a3b8">${m.latency_ms} ms</span>
                </div>
                <div class="arena-dom" style="color: ${color}">
                    ${m.dominant_emotion.toUpperCase()}
                </div>
                <div style="text-align: center; font-size: 12px; font-weight: 700; margin-bottom: 12px">
                    Confidence: ${m.confidence}%
                </div>
                <div class="bars-container">
                    ${CLASS_NAMES.map(name => `
                        <div class="prob-row">
                            <div class="prob-meta">
                                <span style="font-size: 10px">${name}</span>
                                <span style="font-size: 10px">${m.probabilities[name]}%</span>
                            </div>
                            <div class="prob-track" style="height: 4px">
                                <div class="prob-fill" style="width: ${m.probabilities[name]}%; background-color: ${EMOTION_COLORS[name]}"></div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
            arenaGrid.appendChild(card);
        });
    }

    // --------------------------------------------------------------------------
    // TAB 4: EXPLAINABLE AI (GRAD-CAM)
    // --------------------------------------------------------------------------
    function initXAIControls() {
        xaiOpacity.addEventListener('input', (e) => {
            const val = e.target.value;
            xaiOpacityVal.innerText = `${val}%`;
            xaiOverlayImg.style.opacity = val / 100;
        });
    }

    function setupXAIDisplay(data) {
        if (data.grad_cam_overlay) {
            xaiBaseImg.src = loadedImageB64;
            xaiOverlayImg.src = data.grad_cam_overlay;
            xaiOverlayImg.style.opacity = xaiOpacity.value / 100;
            xaiPlaceholder.style.display = 'none';
        }
    }

    // --------------------------------------------------------------------------
    // TAB 5: ECOSYSTEM ANALYTICS & BENCHMARKS
    // --------------------------------------------------------------------------
    function initAnalyticsCharts() {
        const ctxAcc = document.getElementById('chart-accuracy-latency').getContext('2d');
        analyticsAccChart = new Chart(ctxAcc, {
            type: 'bar',
            data: {
                labels: ['EfficientNet-B0', 'YOLOv8 Class', 'ResNet50', 'MobileNetV2'],
                datasets: [
                    {
                        label: 'Accuracy (%)',
                        data: [98.57, 95.52, 94.57, 93.52],
                        backgroundColor: '#00f2fe',
                        borderRadius: 6
                    },
                    {
                        label: 'Latency (ms)',
                        data: [14.2, 8.5, 22.1, 6.1],
                        backgroundColor: '#ff0844',
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: { legend: { labels: { color: '#f8fafc' } } },
                scales: {
                    x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
                    y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
                }
            }
        });

        const ctxLogLoss = document.getElementById('chart-log-loss').getContext('2d');
        analyticsLogLossChart = new Chart(ctxLogLoss, {
            type: 'line',
            data: {
                labels: ['EfficientNet-B0', 'YOLOv8 Class', 'ResNet50', 'MobileNetV2'],
                datasets: [{
                    label: 'Logarithmic Loss (Lower is better)',
                    data: [0.2186, 0.3063, 0.3570, 0.3533],
                    borderColor: '#7928ca',
                    backgroundColor: 'rgba(121, 40, 202, 0.2)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { labels: { color: '#f8fafc' } } },
                scales: {
                    x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
                    y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
                }
            }
        });
    }
});
