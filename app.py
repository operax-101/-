<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>عين السوق | محرك بحث المنتجات الذكي</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts (Tajawal) -->
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            font-family: 'Tajawal', sans-serif;
        }
        .store-noon { background-color: #feee00; color: #000000; }
        .store-shein { background-color: #000000; color: #ffffff; }
        .store-aliexpress { background-color: #ff4747; color: #ffffff; }
        .store-temu { background-color: #fb7701; color: #ffffff; }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col">

    <!-- Header -->
    <header class="bg-gradient-to-r from-indigo-600 to-cyan-600 text-white py-10 px-4 shadow-lg rounded-b-3xl text-center">
        <div class="max-w-4xl mx-auto">
            <h1 class="text-3xl md:text-4xl font-extrabold mb-3 flex items-center justify-center gap-3">
                <i class="fa-solid fa-cart-shopping"></i> عين السوق
            </h1>
            <p class="text-indigo-100 text-base md:text-lg">
                ابحث عن أي منتج بالنص أو بالصورة وقارن النتائج فوراً بين نون، شي إن، علي إكسبريس، وتيمو
            </p>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-4xl mx-auto px-4 flex-1 w-full -mt-6">
        
        <!-- Search & Upload Section -->
        <div class="bg-white rounded-2xl shadow-xl p-6 mb-8 border border-slate-100">
            <div class="flex flex-col sm:flex-row gap-3 mb-4">
                <input type="text" id="searchInput" placeholder="اكتب اسم المنتج (مثال: ساعة ذكية، فستان، سماعة...)" 
                       class="flex-1 px-4 py-3 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-lg"
                       onkeypress="if(event.key === 'Enter') startSearch()">
                <button onclick="startSearch()" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-6 py-3 rounded-xl transition flex items-center justify-center gap-2">
                    <i class="fa-solid fa-magnifying-glass"></i> بحث
                </button>
            </div>

            <!-- Upload / Camera Buttons -->
            <div class="flex flex-wrap gap-3 items-center justify-center sm:justify-start">
                <label for="fileInput" class="cursor-pointer bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium px-4 py-2.5 rounded-xl border border-dashed border-slate-300 flex items-center gap-2 transition text-sm">
                    <i class="fa-solid fa-image text-indigo-600"></i> رفع صورة من الجهاز
                </label>
                <input type="file" id="fileInput" accept="image/*" class="hidden" onchange="handleFileUpload(event)">

                <button onclick="openCamera()" class="bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium px-4 py-2.5 rounded-xl border border-dashed border-slate-300 flex items-center gap-2 transition text-sm">
                    <i class="fa-solid fa-camera text-indigo-600"></i> التقاط صورة بالكاميرا
                </button>
            </div>

            <!-- Image Preview Box -->
            <div id="imagePreviewContainer" class="hidden mt-4 relative w-28 h-28 border-2 border-indigo-500 rounded-xl overflow-hidden">
                <img id="imagePreview" src="" alt="معاينة" class="w-full h-full object-cover">
                <button onclick="clearImage()" class="absolute top-1 right-1 bg-black/60 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs hover:bg-black">
                    &times;
                </button>
            </div>
        </div>

        <!-- Quick Links to Stores -->
        <div class="mb-8">
            <h2 class="text-xl font-bold mb-4 flex items-center gap-2 text-slate-700">
                <i class="fa-solid fa-bolt text-yellow-500"></i> البحث المباشر في المتاجر الأربعة
            </h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <a id="btnNoon" href="https://www.noon.com" target="_blank" class="store-noon p-4 rounded-xl font-bold text-center shadow hover:opacity-90 transition flex flex-col items-center gap-2">
                    <i class="fa-solid fa-store text-2xl"></i> نون (Noon)
                </a>
                <a id="btnShein" href="https://www.shein.com" target="_blank" class="store-shein p-4 rounded-xl font-bold text-center shadow hover:opacity-90 transition flex flex-col items-center gap-2">
                    <i class="fa-solid fa-shirt text-2xl"></i> شي إن (SHEIN)
                </a>
                <a id="btnAliexpress" href="https://www.aliexpress.com" target="_blank" class="store-aliexpress p-4 rounded-xl font-bold text-center shadow hover:opacity-90 transition flex flex-col items-center gap-2">
                    <i class="fa-solid fa-truck-fast text-2xl"></i> علي إكسبريس
                </a>
                <a id="btnTemu" href="https://www.temu.com" target="_blank" class="store-temu p-4 rounded-xl font-bold text-center shadow hover:opacity-90 transition flex flex-col items-center gap-2">
                    <i class="fa-solid fa-tags text-2xl"></i> تيمو (Temu)
                </a>
            </div>
        </div>

        <!-- Loading Indicator -->
        <div id="loading" class="hidden text-center py-10">
            <div class="inline-block w-10 h-10 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mb-3"></div>
            <p id="loadingText" class="text-slate-600 font-medium">جاري البحث ومقارنة الأسعار...</p>
        </div>

        <!-- Results Grid -->
        <div id="resultsContainer" class="hidden mb-12">
            <h2 class="text-xl font-bold mb-4 flex items-center gap-2 text-slate-700">
                <i class="fa-solid fa-list-check text-indigo-600"></i> بطاقات البحث في المتاجر
            </h2>
            <div id="resultsGrid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4"></div>
        </div>

    </main>

    <!-- Camera Modal -->
    <div id="cameraModal" class="hidden fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4">
        <div class="bg-white p-5 rounded-2xl max-w-md w-full text-center">
            <h3 class="font-bold text-lg mb-3">التقط صورة للمنتج</h3>
            <video id="webcam" autoplay playsinline class="w-full rounded-xl bg-black mb-4 h-64 object-cover"></video>
            <div class="flex gap-2 justify-center">
                <button onclick="takePhoto()" class="bg-indigo-600 text-white font-bold px-5 py-2.5 rounded-xl hover:bg-indigo-700">
                    <i class="fa-solid fa-camera"></i> التقاط
                </button>
                <button onclick="closeCamera()" class="bg-slate-200 text-slate-700 font-bold px-5 py-2.5 rounded-xl hover:bg-slate-300">
                    إلغاء
                </button>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-slate-800 text-slate-400 py-6 text-center text-sm">
        <p>موقع عين السوق لمقارنة الأسعار &copy; جميع الحقوق محفوظة</p>
    </footer>

    <!-- JavaScript Logic -->
    <script>
        let videoStream = null;
        let imageSearchKeyword = "";

        // تحديث روابط البحث المباشرة
        function updateStoreLinks(term) {
            const encoded = encodeURIComponent(term);
            document.getElementById('btnNoon').href = `https://www.noon.com/search/?q=${encoded}`;
            document.getElementById('btnShein').href = `https://ar.shein.com/pdsearch/${encoded}/`;
            document.getElementById('btnAliexpress').href = `https://ar.aliexpress.com/w/wholesale-${encoded}.html`;
            document.getElementById('btnTemu').href = `https://www.temu.com/search_result.html?search_key=${encoded}`;
        }

        // بدء تنفيذ البحث
        function startSearch() {
            const inputVal = document.getElementById('searchInput').value.trim();
            const term = inputVal || imageSearchKeyword;

            if (!term) {
                alert("الرجاء كتابة اسم المنتج أو رفع/التقاط صورة للبحث!");
                return;
            }

            updateStoreLinks(term);
            showResults(term);
        }

        // معالجة رفع الملفات
        function handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    displayImagePreview(e.target.result);
                    analyzeImageMock();
                }
                reader.readAsDataURL(file);
            }
        }

        function displayImagePreview(src) {
            document.getElementById('imagePreview').src = src;
            document.getElementById('imagePreviewContainer').classList.remove('hidden');
        }

        function clearImage() {
            document.getElementById('imagePreviewContainer').classList.add('hidden');
            document.getElementById('imagePreview').src = '';
            document.getElementById('fileInput').value = '';
            imageSearchKeyword = "";
        }

        // فتح الكاميرا
        async function openCamera() {
            try {
                videoStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
                const videoEl = document.getElementById('webcam');
                videoEl.srcObject = videoStream;
                document.getElementById('cameraModal').classList.remove('hidden');
            } catch (err) {
                alert("تعذر فتح الكاميرا: " + err.message);
            }
        }

        function closeCamera() {
            if (videoStream) {
                videoStream.getTracks().forEach(track => track.stop());
            }
            document.getElementById('cameraModal').classList.add('hidden');
        }

        function takePhoto() {
            const video = document.getElementById('webcam');
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);

            const dataUrl = canvas.toDataURL('image/jpeg');
            displayImagePreview(dataUrl);
            closeCamera();
            analyzeImageMock();
        }

        // محاكاة التعرف على الصورة
        function analyzeImageMock() {
            const loader = document.getElementById('loading');
            const loadText = document.getElementById('loadingText');
            loader.classList.remove('hidden');
            loadText.innerText = "جاري التعرف على الصورة واكتشاف المنتج...";

            const detectedProducts = ['ساعة ذكية', 'سماعات بلوتوث', 'حقيبة ظهر', 'نظارات شمسية', 'فستان نسائي'];
            const randomTag = detectedProducts[Math.floor(Math.random() * detectedProducts.length)];

            setTimeout(() => {
                document.getElementById('searchInput').value = randomTag;
                imageSearchKeyword = randomTag;
                loader.classList.add('hidden');
                startSearch();
            }, 1200);
        }

        // عرض بطاقات النتائج
        function showResults(term) {
            const loader = document.getElementById('loading');
            const resultsContainer = document.getElementById('resultsContainer');
            const resultsGrid = document.getElementById('resultsGrid');

            loader.classList.remove('hidden');
            document.getElementById('loadingText').innerText = "جاري البحث والمقارنة بين المتاجر...";
            resultsContainer.classList.add('hidden');

            setTimeout(() => {
                loader.classList.add('hidden');
                resultsContainer.classList.remove('hidden');

                const stores = [
                    { name: 'نون', style: 'store-noon', url: `https://www.noon.com/search/?q=${encodeURIComponent(term)}` },
                    { name: 'شي إن', style: 'store-shein', url: `https://ar.shein.com/pdsearch/${encodeURIComponent(term)}/` },
                    { name: 'علي إكسبريس', style: 'store-aliexpress', url: `https://ar.aliexpress.com/w/wholesale-${encodeURIComponent(term)}.html` },
                    { name: 'تيمو', style: 'store-temu', url: `https://www.temu.com/search_result.html?search_key=${encodeURIComponent(term)}` }
                ];

                const images = [
                    'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400',
                    'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
                    'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400',
                    'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=400'
                ];

                resultsGrid.innerHTML = '';

                stores.forEach((store, index) => {
                    const cardHtml = `
                        <div class="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition flex flex-col">
                            <div class="relative">
                                <span class="absolute top-2 right-2 px-3 py-1 rounded-full text-xs font-bold ${store.style}">
                                    ${store.name}
                                </span>
                                <img src="${images[index]}" alt="${term}" class="w-full h-44 object-cover bg-slate-100">
                            </div>
                            <div class="p-4 flex flex-col flex-1">
                                <h3 class="font-bold text-slate-800 text-sm mb-3 line-clamp-2">
                                    ${term} - نتائج البحث في ${store.name}
                                </h3>
                                <a href="${store.url}" target="_blank" class="mt-auto w-full py-2.5 text-center font-bold rounded-xl text-sm transition ${store.style}">
                                    عرض المنتجات في ${store.name}
                                </a>
                            </div>
                        </div>
                    `;
                    resultsGrid.innerHTML += cardHtml;
                });
            }, 800);
        }
    </script>
</body>
</html>
