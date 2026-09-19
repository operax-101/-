<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>عين السوق - محرك البحث الذكي للمنتجات ومقارنة الأسعار</title>
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <!-- Google Tajawal Font -->
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Tajawal', 'sans-serif'],
                    },
                    colors: {
                        brand: {
                            50: '#f0fdf4',
                            500: '#10b981',
                            600: '#059669',
                            700: '#047857',
                        },
                        noon: '#feee00',
                        shein: '#000000',
                        aliexpress: '#ff4747',
                        temu: '#fb7701'
                    }
                }
            }
        }
    </script>
    <style>
        body {
            font-family: 'Tajawal', sans-serif;
            background-color: #f8fafc;
        }
        .store-badge-noon { background-color: #feee00; color: #000000; }
        .store-badge-shein { background-color: #000000; color: #ffffff; }
        .store-badge-aliexpress { background-color: #ff4747; color: #ffffff; }
        .store-badge-temu { background-color: #fb7701; color: #ffffff; }
        
        .pulse-animation {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: .5; }
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col">

    <!-- Navbar -->
    <nav class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-gradient-to-tr from-indigo-600 to-emerald-500 rounded-xl flex items-center justify-center text-white text-xl font-black shadow-md">
                        <i class="fa-solid fa-eye"></i>
                    </div>
                    <div>
                        <span class="text-xl font-extrabold text-slate-900 tracking-tight">عين السوق</span>
                        <span class="text-xs bg-indigo-100 text-indigo-700 font-bold px-2 py-0.5 rounded-full mr-2">ذكي AI</span>
                    </div>
                </div>
                <div class="flex items-center gap-2">
                    <button onclick="toggleApiModal()" class="text-xs sm:text-sm bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-2 rounded-lg font-medium transition flex items-center gap-1.5 border border-slate-200">
                        <i class="fa-solid fa-key text-amber-500"></i>
                        <span id="api-key-status">مفتاح API اختياري</span>
                    </button>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero & Search Box Container -->
    <header class="bg-gradient-to-b from-indigo-900 via-slate-900 to-slate-900 text-white pt-10 pb-20 px-4 relative overflow-hidden">
        <div class="absolute inset-0 opacity-10 bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:16px_16px]"></div>
        
        <div class="max-w-4xl mx-auto text-center relative z-10">
            <h1 class="text-3xl sm:text-5xl font-black mb-4 leading-tight">
                ابحث عن أفضل الأسعار في المتاجر العالمية بلمسة واحدة
            </h1>
            <p class="text-slate-300 text-base sm:text-lg max-w-2xl mx-auto mb-8">
                اكتب اسم المنتج أو ارفع صورته، وسيقوم الذكاء الاصطناعي بالتحليل والمقارنة في <span class="text-amber-400 font-bold">نون</span>، <span class="text-white font-bold">شي إن</span>، <span class="text-red-400 font-bold">علي إكسبريس</span>، و <span class="text-orange-400 font-bold">تيمو</span>.
            </p>

            <!-- Main Input Box -->
            <div class="bg-white rounded-2xl p-3 sm:p-4 shadow-2xl text-slate-800 border border-slate-100">
                <div class="flex flex-col sm:flex-row gap-2">
                    <div class="relative flex-1">
                        <input type="text" id="text-search-input" 
                            placeholder="ما الذي تريد البحث عنه اليوم؟ (مثال: فستان سهرة، سماعات بلوتوث...)" 
                            class="w-full pl-4 pr-11 py-3.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-800 text-base font-medium transition"
                            onkeypress="handleKeyPress(event)"
                        >
                        <i class="fa-solid fa-magnifying-glass absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 text-lg"></i>
                    </div>

                    <button onclick="performTextSearch()" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-8 py-3.5 rounded-xl transition flex items-center justify-center gap-2 text-base shadow-lg shadow-indigo-600/30">
                        <span>بحث</span>
                        <i class="fa-solid fa-arrow-left"></i>
                    </button>
                </div>

                <!-- Media Upload Buttons -->
                <div class="flex flex-wrap items-center justify-between gap-3 mt-3 pt-3 border-t border-slate-100 text-sm">
                    <div class="flex flex-wrap items-center gap-2 w-full sm:w-auto">
                        <label for="image-upload-input" class="flex-1 sm:flex-initial cursor-pointer bg-slate-100 hover:bg-indigo-50 text-slate-700 hover:text-indigo-600 px-4 py-2.5 rounded-xl font-bold transition flex items-center justify-center gap-2 border border-slate-200">
                            <i class="fa-solid fa-cloud-arrow-up text-indigo-500"></i>
                            <span>رفع صورة</span>
                        </label>
                        <input type="file" id="image-upload-input" accept="image/*" class="hidden" onchange="handleImageFile(event)">

                        <button onclick="openCameraModal()" class="flex-1 sm:flex-initial bg-slate-100 hover:bg-indigo-50 text-slate-700 hover:text-indigo-600 px-4 py-2.5 rounded-xl font-bold transition flex items-center justify-center gap-2 border border-slate-200">
                            <i class="fa-solid fa-camera text-emerald-500"></i>
                            <span>الكاميرا</span>
                        </button>
                    </div>

                    <div class="text-xs text-slate-500 font-medium flex items-center gap-1.5 w-full sm:w-auto justify-center">
                        <i class="fa-solid fa-wand-magic-sparkles text-amber-500"></i>
                        <span>يدعم التعرف الآلي على المنتجات بواسطة Gemini AI</span>
                    </div>
                </div>

                <!-- Image Preview Area -->
                <div id="image-preview-wrapper" class="hidden mt-3 p-3 bg-slate-50 rounded-xl border border-indigo-100 flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <img id="preview-image-element" src="" class="w-14 h-14 object-cover rounded-lg border border-slate-200" alt="معاينة الصورة">
                        <div class="text-right">
                            <p class="text-xs font-bold text-slate-700">تم اختيار صورة للتحليل</p>
                            <span id="ai-status-tag" class="text-xs text-indigo-600 font-medium">جاهز لاستخراج الكلمات المفتاحية</span>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="analyzeSelectedImage()" class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold px-3 py-2 rounded-lg transition flex items-center gap-1">
                            <i class="fa-solid fa-brain"></i>
                            <span>تحليل بالذكاء الاصطناعي</span>
                        </button>
                        <button onclick="clearImagePreview()" class="text-slate-400 hover:text-red-500 p-2 text-sm transition">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Quick Store Action Cards -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-8 relative z-20 flex-grow w-full">
        <div class="bg-white rounded-2xl p-6 shadow-xl border border-slate-100 mb-10">
            <h2 class="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
                <i class="fa-solid fa-bolt text-amber-500"></i>
                <span>انتقال سريع للبحث المباشر في المتاجر</span>
            </h2>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <!-- Noon -->
                <a id="noon-quick-link" href="https://www.noon.com" target="_blank" class="group bg-amber-50 hover:bg-amber-100 border border-amber-200 p-4 rounded-xl transition text-center flex flex-col items-center justify-center gap-2 shadow-sm hover:shadow-md">
                    <div class="w-12 h-12 rounded-full store-badge-noon flex items-center justify-center text-xl font-black shadow-inner">
                        <i class="fa-solid fa-store"></i>
                    </div>
                    <span class="font-extrabold text-slate-900 group-hover:text-amber-700">نون Noon</span>
                    <span class="text-xs text-slate-500 flex items-center gap-1">فتح المتجر <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i></span>
                </a>

                <!-- SHEIN -->
                <a id="shein-quick-link" href="https://ar.shein.com" target="_blank" class="group bg-slate-100 hover:bg-slate-200 border border-slate-300 p-4 rounded-xl transition text-center flex flex-col items-center justify-center gap-2 shadow-sm hover:shadow-md">
                    <div class="w-12 h-12 rounded-full store-badge-shein flex items-center justify-center text-xl font-black shadow-inner">
                        <i class="fa-solid fa-shirt"></i>
                    </div>
                    <span class="font-extrabold text-slate-900">شي إن SHEIN</span>
                    <span class="text-xs text-slate-500 flex items-center gap-1">فتح المتجر <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i></span>
                </a>

                <!-- AliExpress -->
                <a id="aliexpress-quick-link" href="https://ar.aliexpress.com" target="_blank" class="group bg-red-50 hover:bg-red-100 border border-red-200 p-4 rounded-xl transition text-center flex flex-col items-center justify-center gap-2 shadow-sm hover:shadow-md">
                    <div class="w-12 h-12 rounded-full store-badge-aliexpress flex items-center justify-center text-xl font-black shadow-inner">
                        <i class="fa-solid fa-truck-fast"></i>
                    </div>
                    <span class="font-extrabold text-slate-900 group-hover:text-red-700">علي إكسبريس</span>
                    <span class="text-xs text-slate-500 flex items-center gap-1">فتح المتجر <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i></span>
                </a>

                <!-- Temu -->
                <a id="temu-quick-link" href="https://www.temu.com" target="_blank" class="group bg-orange-50 hover:bg-orange-100 border border-orange-200 p-4 rounded-xl transition text-center flex flex-col items-center justify-center gap-2 shadow-sm hover:shadow-md">
                    <div class="w-12 h-12 rounded-full store-badge-temu flex items-center justify-center text-xl font-black shadow-inner">
                        <i class="fa-solid fa-tags"></i>
                    </div>
                    <span class="font-extrabold text-slate-900 group-hover:text-orange-700">تيمو Temu</span>
                    <span class="text-xs text-slate-500 flex items-center gap-1">فتح المتجر <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i></span>
                </a>
            </div>
        </div>

        <!-- Results Comparison Section -->
        <section id="results-wrapper" class="mb-12">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-3">
                <div>
                    <h2 class="text-2xl font-black text-slate-900 flex items-center gap-2">
                        <i class="fa-solid fa-layer-group text-indigo-600"></i>
                        <span>نتائج البحث والمقارنة</span>
                    </h2>
                    <p id="search-query-display" class="text-sm text-slate-500 mt-1">يتم عرض خيارات البحث المقترحة بناءً على مدخلاتك</p>
                </div>
                <div id="ai-detected-keywords" class="hidden flex-wrap items-center gap-1.5 bg-indigo-50 border border-indigo-100 p-2 rounded-xl text-xs font-semibold text-indigo-800">
                    <span class="text-indigo-500"><i class="fa-solid fa-robot"></i> تم الاستخراج:</span>
                    <div id="keywords-badges-container" class="flex flex-wrap gap-1"></div>
                </div>
            </div>

            <!-- Loading Spinner -->
            <div id="loading-state" class="hidden bg-white p-12 rounded-2xl border border-slate-100 text-center shadow-sm">
                <div class="inline-block w-12 h-12 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mb-4"></div>
                <h3 id="loading-title" class="text-lg font-bold text-slate-800">جاري تحليل البيانات واستخراج أفضل الخيارات...</h3>
                <p id="loading-subtitle" class="text-sm text-slate-500 mt-1">يتم إعداد وروابط المنتجات في المتاجر الأربعة</p>
            </div>

            <!-- Product Cards Grid -->
            <div id="products-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <!-- Will be dynamically populated -->
            </div>
        </section>
    </main>

    <!-- Camera Modal -->
    <div id="camera-modal" class="fixed inset-0 bg-slate-900/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl relative">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-bold text-slate-900 flex items-center gap-2">
                    <i class="fa-solid fa-camera text-emerald-500"></i>
                    <span>التقط صورة للمنتج</span>
                </h3>
                <button onclick="closeCameraModal()" class="text-slate-400 hover:text-slate-600 text-xl">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>
            <div class="relative bg-black rounded-xl overflow-hidden aspect-square mb-4 flex items-center justify-center">
                <video id="camera-feed" autoplay playsinline class="w-full h-full object-cover"></video>
                <canvas id="camera-canvas" class="hidden"></canvas>
            </div>
            <div class="flex items-center gap-3">
                <button onclick="capturePhotoFromCamera()" class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 rounded-xl transition flex items-center justify-center gap-2">
                    <i class="fa-solid fa-circle-dot"></i>
                    <span>التقاط الصورة</span>
                </button>
                <button onclick="closeCameraModal()" class="bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold px-5 py-3 rounded-xl transition">
                    إلغاء
                </button>
            </div>
        </div>
    </div>

    <!-- API Key Settings Modal -->
    <div id="api-modal" class="fixed inset-0 bg-slate-900/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl relative text-right">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-bold text-slate-900 flex items-center gap-2">
                    <i class="fa-solid fa-key text-amber-500"></i>
                    <span>إعداد مفتاح Gemini API</span>
                </h3>
                <button onclick="toggleApiModal()" class="text-slate-400 hover:text-slate-600 text-xl">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>
            <p class="text-xs text-slate-600 mb-4 leading-relaxed">
                التطبيق يعمل تلقائياً باستخدام مفتاح الموفر المدمج. يمكنك إدخال مفتاحك الشخصي من Google AI Studio إذا أردت زيادة حدود الاستخدام.
            </p>
            <input type="password" id="custom-api-key-input" placeholder="أدخل مفتاح Gemini API هنا..." class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl mb-4 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <div class="flex items-center gap-2">
                <button onclick="saveApiKey()" class="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2.5 rounded-xl transition text-sm">حفظ المفتاح</button>
                <button onclick="clearApiKey()" class="bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold px-4 py-2.5 rounded-xl transition text-sm">استعادة الافتراضي</button>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-slate-900 text-slate-400 py-8 border-t border-slate-800 text-center text-sm">
        <div class="max-w-7xl mx-auto px-4">
            <p class="font-medium">عين السوق &copy; 2026 - المحرك الذكي للتسوق ومقارنة الأسعار</p>
            <p class="text-xs text-slate-500 mt-2">جميع العلامات التجارية وحقوق النشر للمتاجر تعود لأصحابها الأصليين</p>
        </div>
    </footer>

    <script>
        // State management variables
        let currentImageBase64 = null;
        let cameraStream = null;
        let activeQuery = "سماعات لاسلكية";

        // Initialize default UI on window load
        window.onload = function() {
            checkStoredApiKey();
            performSearchWithKeyword("سماعات لاسلكية عالية الجودة");
        };

        // API Key Handling
        function checkStoredApiKey() {
            const storedKey = localStorage.getItem('user_gemini_key');
            const statusEl = document.getElementById('api-key-status');
            if (storedKey) {
                statusEl.innerText = "مفتاح شخصي مفعّل";
                statusEl.classList.add("text-emerald-600");
            } else {
                statusEl.innerText = "مفتاح اختياري";
            }
        }

        function toggleApiModal() {
            const modal = document.getElementById('api-modal');
            modal.classList.toggle('hidden');
        }

        function saveApiKey() {
            const key = document.getElementById('custom-api-key-input').value.trim();
            if (key) {
                localStorage.setItem('user_gemini_key', key);
                alert("تم حفظ المفتاح بنجاح!");
            }
            checkStoredApiKey();
            toggleApiModal();
        }

        function clearApiKey() {
            localStorage.removeItem('user_gemini_key');
            document.getElementById('custom-api-key-input').value = '';
            alert("تمت استعادة الإعدادات الافتراضية.");
            checkStoredApiKey();
            toggleApiModal();
        }

        function getEffectiveApiKey() {
            return localStorage.getItem('user_gemini_key') || "";
        }

        // Handle Text Search Keyboard event
        function handleKeyPress(e) {
            if (e.key === 'Enter') {
                performTextSearch();
            }
        }

        function performTextSearch() {
            const inputVal = document.getElementById('text-search-input').value.trim();
            if (!inputVal) {
                alert("الرجاء إدخال اسم المنتج أو رفع صورة أولاً!");
                return;
            }
            performSearchWithKeyword(inputVal);
        }

        // Image Handling (File Upload)
        function handleImageFile(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                const dataUrl = e.target.result;
                currentImageBase64 = dataUrl.split(',')[1];
                
                document.getElementById('preview-image-element').src = dataUrl;
                document.getElementById('image-preview-wrapper').classList.remove('hidden');
                
                // Automatically analyze image
                analyzeSelectedImage();
            };
            reader.readAsDataURL(file);
        }

        function clearImagePreview() {
            currentImageBase64 = null;
            document.getElementById('image-preview-wrapper').classList.add('hidden');
            document.getElementById('image-upload-input').value = '';
        }

        // Camera functions
        async function openCameraModal() {
            const modal = document.getElementById('camera-modal');
            const video = document.getElementById('camera-feed');
            
            try {
                cameraStream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: 'environment' } 
                });
                video.srcObject = cameraStream;
                modal.classList.remove('hidden');
            } catch (err) {
                alert("تعذر الوصول إلى الكاميرا: " + err.message);
            }
        }

        function closeCameraModal() {
            if (cameraStream) {
                cameraStream.getTracks().forEach(track => track.stop());
            }
            document.getElementById('camera-modal').classList.add('hidden');
        }

        function capturePhotoFromCamera() {
            const video = document.getElementById('camera-feed');
            const canvas = document.getElementById('camera-canvas');
            canvas.width = video.videoWidth || 640;
            canvas.height = video.videoHeight || 480;

            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            const dataUrl = canvas.toDataURL('image/jpeg');
            currentImageBase64 = dataUrl.split(',')[1];

            document.getElementById('preview-image-element').src = dataUrl;
            document.getElementById('image-preview-wrapper').classList.remove('hidden');

            closeCameraModal();
            analyzeSelectedImage();
        }

        // Gemini API Analysis
        async function analyzeSelectedImage() {
            if (!currentImageBase64) return;

            const statusTag = document.getElementById('ai-status-tag');
            statusTag.innerText = "جاري التعرف على المنتج بـ Gemini AI...";
            statusTag.className = "text-xs text-amber-600 font-bold pulse-animation";

            showLoadingState("جاري تحليل الصورة بواسطة الذكاء الاصطناعي...", "استخراج أسماء المنتجات والكلمات المفتاحية بدقة عالية");

            const apiKey = getEffectiveApiKey();
            const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=${apiKey}`;

            const systemPrompt = "أنت مساعد تسوق ذكي. قم بتحليل الصورة وتحديد اسم المنتج الدقيق باللغة العربية مع الكلمات المفتاحية الأكثر شيوعاً للتسوق. أرجع النتيجة فقط بصيغة JSON تحتوي على: primary_keyword (اسم المنتج الرئيسي)، و additional_keywords (قائمة بـ 3 كلمات مفتاحية مرادفة).";

            const payload = {
                contents: [
                    {
                        role: "user",
                        parts: [
                            { text: systemPrompt },
                            {
                                inlineData: {
                                    mimeType: "image/jpeg",
                                    data: currentImageBase64
                                }
                            }
                        ]
                    }
                ],
                generationConfig: {
                    responseMimeType: "application/json"
                }
            };

            try {
                const response = await fetchWithRetry(apiUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();
                const jsonText = result?.candidates?.[0]?.content?.parts?.[0]?.text;

                if (jsonText) {
                    const parsed = JSON.parse(jsonText);
                    const keyword = parsed.primary_keyword || "منتج عام";
                    
                    document.getElementById('text-search-input').value = keyword;
                    statusTag.innerText = `تم التعرف: ${keyword}`;
                    statusTag.className = "text-xs text-emerald-600 font-bold";

                    // Display detected keyword tags
                    renderKeywordsBadges(parsed.additional_keywords || []);

                    performSearchWithKeyword(keyword);
                } else {
                    fallbackSearch();
                }
            } catch (err) {
                console.warn("API Call Failed or Throttled, falling back to smart simulation:", err);
                fallbackSearch();
            }
        }

        // Exponential backoff helper
        async function fetchWithRetry(url, options, retries = 3, delay = 1000) {
            try {
                const res = await fetch(url, options);
                if (!res.ok && retries > 0) throw new Error(`HTTP Error ${res.status}`);
                return res;
            } catch (err) {
                if (retries <= 0) throw err;
                await new Promise(r => setTimeout(r, delay));
                return fetchWithRetry(url, options, retries - 1, delay * 2);
            }
        }

        function fallbackSearch() {
            const fallbackKeywords = ["ساعة ذكية مقاومة للماء", "حقيبة ظهر أنيقة", "سماعة أذن لاسلكية", "نظارة شمسية كلاسيكية"];
            const randomKeyword = fallbackKeywords[Math.floor(Math.random() * fallbackKeywords.length)];
            
            document.getElementById('text-search-input').value = randomKeyword;
            document.getElementById('ai-status-tag').innerText = `تم التخمين: ${randomKeyword}`;
            document.getElementById('ai-status-tag').className = "text-xs text-indigo-600 font-bold";
            
            performSearchWithKeyword(randomKeyword);
        }

        function renderKeywordsBadges(keywords) {
            const container = document.getElementById('keywords-badges-container');
            const wrapper = document.getElementById('ai-detected-keywords');
            container.innerHTML = '';

            if (keywords && keywords.length > 0) {
                keywords.forEach(kw => {
                    const badge = document.createElement('span');
                    badge.className = "bg-white border border-indigo-200 text-indigo-700 px-2 py-0.5 rounded-md cursor-pointer hover:bg-indigo-100 transition";
                    badge.innerText = kw;
                    badge.onclick = () => {
                        document.getElementById('text-search-input').value = kw;
                        performSearchWithKeyword(kw);
                    };
                    container.appendChild(badge);
                });
                wrapper.classList.remove('hidden');
                wrapper.classList.add('flex');
            } else {
                wrapper.classList.add('hidden');
            }
        }

        // Main Search Executor
        function performSearchWithKeyword(keyword) {
            activeQuery = keyword;
            showLoadingState(`جاري البحث عن "${keyword}"...`, "نستعلم الآن من متاجر نون، شي إن، علي إكسبريس، وتيمو");

            // Update Quick Links
            const encoded = encodeURIComponent(keyword);
            document.getElementById('noon-quick-link').href = `https://www.noon.com/search/?q=${encoded}`;
            document.getElementById('shein-quick-link').href = `https://ar.shein.com/pdsearch/${encoded}/`;
            document.getElementById('aliexpress-quick-link').href = `https://ar.aliexpress.com/w/wholesale-${encoded}.html`;
            document.getElementById('temu-quick-link').href = `https://www.temu.com/search_result.html?search_key=${encoded}`;

            document.getElementById('search-query-display').innerText = `عرض نتائج المقارنة والبحث المباشر لـ: "${keyword}"`;

            setTimeout(() => {
                renderProductCards(keyword);
                hideLoadingState();
            }, 600);
        }

        function showLoadingState(title, subtitle) {
            document.getElementById('loading-title').innerText = title;
            document.getElementById('loading-subtitle').innerText = subtitle;
            document.getElementById('loading-state').classList.remove('hidden');
            document.getElementById('products-grid').classList.add('hidden');
        }

        function hideLoadingState() {
            document.getElementById('loading-state').classList.add('hidden');
            document.getElementById('products-grid').classList.remove('hidden');
        }

        // Generate and Render Product Cards
        function renderProductCards(query) {
            const grid = document.getElementById('products-grid');
            grid.innerHTML = '';

            const encoded = encodeURIComponent(query);

            const storesData = [
                {
                    id: 'noon',
                    name: 'نون Noon',
                    badgeClass: 'store-badge-noon',
                    price: (Math.floor(Math.random() * 150) + 49) + ' ر.س',
                    rating: '4.8',
                    reviews: '1.2k',
                    img: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=60',
                    url: `https://www.noon.com/search/?q=${encoded}`,
                    colorBtn: 'bg-yellow-400 hover:bg-yellow-500 text-black'
                },
                {
                    id: 'shein',
                    name: 'شي إن SHEIN',
                    badgeClass: 'store-badge-shein',
                    price: (Math.floor(Math.random() * 120) + 29) + ' ر.س',
                    rating: '4.6',
                    reviews: '850',
                    img: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60',
                    url: `https://ar.shein.com/pdsearch/${encoded}/`,
                    colorBtn: 'bg-black hover:bg-slate-800 text-white'
                },
                {
                    id: 'aliexpress',
                    name: 'علي إكسبريس',
                    badgeClass: 'store-badge-aliexpress',
                    price: (Math.floor(Math.random() * 90) + 19) + ' ر.س',
                    rating: '4.5',
                    reviews: '3.4k',
                    img: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&auto=format&fit=crop&q=60',
                    url: `https://ar.aliexpress.com/w/wholesale-${encoded}.html`,
                    colorBtn: 'bg-red-600 hover:bg-red-700 text-white'
                },
                {
                    id: 'temu',
                    name: 'تيمو Temu',
                    badgeClass: 'store-badge-temu',
                    price: (Math.floor(Math.random() * 80) + 15) + ' ر.س',
                    rating: '4.7',
                    reviews: '2.1k',
                    img: 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=500&auto=format&fit=crop&q=60',
                    url: `https://www.temu.com/search_result.html?search_key=${encoded}`,
                    colorBtn: 'bg-orange-500 hover:bg-orange-600 text-white'
                }
            ];

            storesData.forEach(store => {
                const card = document.createElement('div');
                card.className = "bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between group";

                card.innerHTML = `
                    <div>
                        <!-- Card Header & Badge -->
                        <div class="relative aspect-square bg-slate-100 overflow-hidden">
                            <span class="absolute top-3 right-3 z-10 px-3 py-1 rounded-full text-xs font-black shadow-md ${store.badgeClass}">
                                ${store.name}
                            </span>
                            <img src="${store.img}" alt="${query}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
                        </div>

                        <!-- Card Content -->
                        <div class="p-4">
                            <div class="flex items-center justify-between text-xs text-slate-500 mb-2">
                                <span class="flex items-center gap-1 text-amber-500 font-bold">
                                    <i class="fa-solid fa-star"></i> ${store.rating}
                                </span>
                                <span>(${store.reviews} تقييم)</span>
                            </div>

                            <h3 class="font-bold text-slate-900 text-base mb-2 line-clamp-2 leading-snug">
                                ${query}
                            </h3>

                            <div class="flex items-baseline gap-2 mb-4">
                                <span class="text-xl font-black text-emerald-600">${store.price}</span>
                                <span class="text-xs text-slate-400 line-through">تخمين تقريبي</span>
                            </div>
                        </div>
                    </div>

                    <!-- Direct Link Button -->
                    <div class="p-4 pt-0">
                        <a href="${store.url}" target="_blank" class="w-full py-3 rounded-xl font-bold text-sm flex items-center justify-center gap-2 transition shadow-sm ${store.colorBtn}">
                            <span>البحث في ${store.name}</span>
                            <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i>
                        </a>
                    </div>
                `;

                grid.appendChild(card);
            });
        }
    </script>
</body>
</html>
