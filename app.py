<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>محرك بحث المنتجات الذكي | نون، شي إن، علي اكسبريس، تيمو</title>
    <!-- Google Fonts & FontAwesome Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --primary: #4f46e5;
            --primary-dark: #4338ca;
            --secondary: #06b6d4;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --border-color: #e2e8f0;
            
            /* Store Colors */
            --noon-color: #feee00;
            --noon-text: #000000;
            --shein-color: #000000;
            --shein-text: #ffffff;
            --aliexpress-color: #ff4747;
            --aliexpress-text: #ffffff;
            --temu-color: #fb7701;
            --temu-text: #ffffff;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Tajawal', sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.6;
            padding-bottom: 50px;
        }

        /* Header */
        header {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 40px 20px;
            text-align: center;
            border-radius: 0 0 25px 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }

        header h1 {
            font-size: 2.2rem;
            margin-bottom: 10px;
            font-weight: 800;
        }

        header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        /* Container */
        .container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Search Section */
        .search-box {
            background: var(--card-bg);
            padding: 25px;
            border-radius: 20px;
            margin-top: -30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .search-input-group {
            display: flex;
            gap: 10px;
            position: relative;
        }

        .search-input-group input[type="text"] {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid var(--border-color);
            border-radius: 12px;
            font-size: 1.1rem;
            outline: none;
            transition: all 0.3s;
        }

        .search-input-group input[type="text"]:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.15);
        }

        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .btn-primary {
            background-color: var(--primary);
            color: white;
        }

        .btn-primary:hover {
            background-color: var(--primary-dark);
            transform: translateY(-2px);
        }

        .btn-camera {
            background-color: #f1f5f9;
            color: var(--text-main);
            border: 2px dashed #cbd5e1;
        }

        .btn-camera:hover {
            background-color: #e2e8f0;
            border-color: var(--primary);
        }

        /* Image Preview Area */
        .image-preview-container {
            display: none;
            position: relative;
            width: 120px;
            height: 120px;
            margin-top: 10px;
            border-radius: 12px;
            overflow: hidden;
            border: 2px solid var(--primary);
        }

        .image-preview-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .remove-img-btn {
            position: absolute;
            top: 5px;
            right: 5px;
            background: rgba(0,0,0,0.6);
            color: white;
            border: none;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Camera Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .modal-content {
            background: white;
            padding: 20px;
            border-radius: 20px;
            max-width: 500px;
            width: 100%;
            text-align: center;
        }

        #video-feed {
            width: 100%;
            border-radius: 12px;
            background: #000;
            margin-bottom: 15px;
        }

        /* Quick Links to Stores */
        .store-quick-links {
            margin-top: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }

        .store-card {
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            transition: transform 0.3s, box-shadow 0.3s;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }

        .store-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        }

        .store-card i {
            font-size: 1.8rem;
        }

        .store-noon { background-color: var(--noon-color); color: var(--noon-text); }
        .store-shein { background-color: var(--shein-color); color: var(--shein-text); }
        .store-aliexpress { background-color: var(--aliexpress-color); color: var(--aliexpress-text); }
        .store-temu { background-color: var(--temu-color); color: var(--temu-text); }

        /* Results Section */
        .results-section {
            margin-top: 40px;
        }

        .section-title {
            font-size: 1.5rem;
            margin-bottom: 20px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .results-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 20px;
        }

        .product-card {
            background: var(--card-bg);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            transition: transform 0.3s;
            display: flex;
            flex-direction: column;
            border: 1px solid var(--border-color);
        }

        .product-card:hover {
            transform: translateY(-5px);
        }

        .product-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            z-index: 2;
        }

        .product-img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            background-color: #f1f5f9;
            position: relative;
        }

        .product-info {
            padding: 15px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }

        .product-title {
            font-size: 0.95rem;
            font-weight: 700;
            margin-bottom: 10px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            height: 2.8em;
        }

        .product-price {
            font-size: 1.2rem;
            font-weight: 800;
            color: var(--primary-dark);
            margin-bottom: 15px;
        }

        .product-btn {
            margin-top: auto;
            width: 100%;
            padding: 10px;
            text-align: center;
            text-decoration: none;
            border-radius: 10px;
            font-weight: bold;
            font-size: 0.9rem;
            display: block;
        }

        /* Loading Spinner */
        .loading {
            display: none;
            text-align: center;
            padding: 40px;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid var(--primary);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @media (max-width: 600px) {
            .search-input-group {
                flex-direction: column;
            }
            header h1 {
                font-size: 1.8rem;
            }
        }
    </style>
</head>
<body>

    <header>
        <div class="container">
            <h1><i class="fa-solid fa-bag-shopping"></i> محرك البحث المقارن للمنتجات</h1>
            <p>ابحث عن أي منتج بالنص أو بالصورة وقارن النتائج مباشرة في نون، شي إن، علي اكسبريس، وتيمو</p>
        </div>
    </header>

    <div class="container">
        <!-- Search Box -->
        <div class="search-box">
            <div class="search-input-group">
                <input type="text" id="search-input" placeholder="اكتب اسم المنتج (مثال: سماعات لاسلكية، فستان، ساعة...)" onkeypress="handleKeyPress(event)">
                <button class="btn btn-primary" onclick="executeSearch()"><i class="fa-solid fa-magnifying-glass"></i> بحث</button>
            </div>
            
            <div style="display: flex; gap: 10px; flex-wrap: wrap; align-items: center;">
                <label for="image-upload" class="btn btn-camera">
                    <i class="fa-solid fa-image"></i> رفع صورة من الجهاز
                </label>
                <input type="file" id="image-upload" accept="image/*" style="display: none;" onchange="handleImageUpload(event)">

                <button class="btn btn-camera" onclick="openCamera()">
                    <i class="fa-solid fa-camera"></i> التقاط صورة بالكاميرا
                </button>
            </div>

            <!-- Image Preview -->
            <div class="image-preview-container" id="preview-container">
                <button class="remove-img-btn" onclick="clearImage()">&times;</button>
                <img id="preview-img" src="" alt="معاينة الصورة">
            </div>
        </div>

        <!-- Quick Links / Direct Search Buttons -->
        <div class="results-section">
            <h2 class="section-title"><i class="fa-solid fa-bolt"></i> البحث المباشر في المتاجر الأربعة</h2>
            <div class="store-quick-links">
                <a id="link-noon" href="https://www.noon.com" target="_blank" class="store-card store-noon">
                    <i class="fa-solid fa-store"></i> نون (Noon)
                </a>
                <a id="link-shein" href="https://www.shein.com" target="_blank" class="store-card store-shein">
                    <i class="fa-solid fa-shirt"></i> شي إن (SHEIN)
                </a>
                <a id="link-aliexpress" href="https://www.aliexpress.com" target="_blank" class="store-card store-aliexpress">
                    <i class="fa-solid fa-truck-fast"></i> علي اكسبريس
                </a>
                <a id="link-temu" href="https://www.temu.com" target="_blank" class="store-card store-temu">
                    <i class="fa-solid fa-tags"></i> تيمو (Temu)
                </a>
            </div>
        </div>

        <!-- Loading Indicator -->
        <div class="loading" id="loading-spinner">
            <div class="spinner"></div>
            <p id="loading-text">جاري جلب النتائج والمقارنة...</p>
        </div>

        <!-- Search Results Grid -->
        <div class="results-section" id="results-container" style="display: none;">
            <h2 class="section-title"><i class="fa-solid fa-list-check"></i> النتائج المقترحة للمقارنة</h2>
            <div class="results-grid" id="results-grid"></div>
        </div>
    </div>

    <!-- Camera Modal -->
    <div class="modal" id="camera-modal">
        <div class="modal-content">
            <h3>التقط صورة للمنتج</h3>
            <video id="video-feed" autoplay playsinline></video>
            <div style="display: flex; gap: 10px; justify-content: center;">
                <button class="btn btn-primary" onclick="capturePhoto()"><i class="fa-solid fa-camera"></i> التقاط</button>
                <button class="btn btn-camera" onclick="closeCamera()">إلغاء</button>
            </div>
        </div>
    </div>

    <script>
        let currentStream = null;
        let selectedKeyword = "";

        // Auto Update Direct Search Links
        function updateStoreLinks(query) {
            const encodedQuery = encodeURIComponent(query);
            document.getElementById('link-noon').href = `https://www.noon.com/search/?q=${encodedQuery}`;
            document.getElementById('link-shein').href = `https://ar.shein.com/pdsearch/${encodedQuery}/`;
            document.getElementById('link-aliexpress').href = `https://ar.aliexpress.com/w/wholesale-${encodedQuery}.html`;
            document.getElementById('link-temu').href = `https://www.temu.com/search_result.html?search_key=${encodedQuery}`;
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                executeSearch();
            }
        }

        function executeSearch() {
            const query = document.getElementById('search-input').value.trim();
            if (!query && !selectedKeyword) {
                alert('الرجاء إدخال اسم المنتج أو اختيار صورة للبحث!');
                return;
            }

            const searchTerm = query || selectedKeyword;
            updateStoreLinks(searchTerm);
            renderResults(searchTerm);
        }

        // Image Handling
        function handleImageUpload(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    showPreview(e.target.result);
                    processImageSearch();
                }
                reader.readAsDataURL(file);
            }
        }

        function showPreview(imageSrc) {
            document.getElementById('preview-img').src = imageSrc;
            document.getElementById('preview-container').style.display = 'block';
        }

        function clearImage() {
            document.getElementById('preview-container').style.display = 'none';
            document.getElementById('preview-img').src = '';
            document.getElementById('image-upload').value = '';
            selectedKeyword = "";
        }

        // Camera Logic
        async function openCamera() {
            const modal = document.getElementById('camera-modal');
            const video = document.getElementById('video-feed');
            try {
                currentStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
                video.srcObject = currentStream;
                modal.style.display = 'flex';
            } catch (err) {
                alert('تعذر الوصول إلى الكاميرا: ' + err.message);
            }
        }

        function closeCamera() {
            if (currentStream) {
                currentStream.getTracks().forEach(track => track.stop());
            }
            document.getElementById('camera-modal').style.display = 'none';
        }

        function capturePhoto() {
            const video = document.getElementById('video-feed');
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            
            const imageData = canvas.toDataURL('image/jpeg');
            showPreview(imageData);
            closeCamera();
            processImageSearch();
        }

        // Simulate Image Recognition AI
        function processImageSearch() {
            document.getElementById('loading-spinner').style.display = 'block';
            document.getElementById('loading-text').innerText = 'جاري تحليل الصورة والتعرف على المنتج...';
            document.getElementById('results-container').style.display = 'none';

            // Simulation of AI detection tags
            const mockTags = ['ساعة ذكية', 'سماعات بلوتوث', 'حقيبة ظهر', 'نظارات شمسية', 'قميص رجالي'];
            const detectedTag = mockTags[Math.floor(Math.random() * mockTags.length)];

            setTimeout(() => {
                document.getElementById('search-input').value = detectedTag;
                selectedKeyword = detectedTag;
                executeSearch();
            }, 1500);
        }

        // Display Demo Comparison Data
        function renderResults(query) {
            const spinner = document.getElementById('loading-spinner');
            const container = document.getElementById('results-container');
            const grid = document.getElementById('results-grid');

            spinner.style.display = 'block';
            document.getElementById('loading-text').innerText = 'جاري البحث في المتغيرات والألوان بجميع المتاجر...';
            container.style.display = 'none';

            setTimeout(() => {
                spinner.style.display = 'none';
                container.style.display = 'block';

                const stores = [
                    { name: 'نون', class: 'store-noon', badgeBg: 'var(--noon-color)', badgeText: 'var(--noon-text)', link: `https://www.noon.com/search/?q=${encodeURIComponent(query)}` },
                    { name: 'شي إن', class: 'store-shein', badgeBg: 'var(--shein-color)', badgeText: 'var(--shein-text)', link: `https://ar.shein.com/pdsearch/${encodeURIComponent(query)}/` },
                    { name: 'علي اكسبريس', class: 'store-aliexpress', badgeBg: 'var(--aliexpress-color)', badgeText: 'var(--aliexpress-text)', link: `https://ar.aliexpress.com/w/wholesale-${encodeURIComponent(query)}.html` },
                    { name: 'تيمو', class: 'store-temu', badgeBg: 'var(--temu-color)', badgeText: 'var(--temu-text)', link: `https://www.temu.com/search_result.html?search_key=${encodeURIComponent(query)}` }
                ];

                const placeholderImages = [
                    'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400',
                    'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
                    'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400',
                    'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=400'
                ];

                grid.innerHTML = '';

                stores.forEach((store, index) => {
                    const price = (Math.random() * 80 + 20).toFixed(2);
                    const productCard = `
                        <div class="product-card">
                            <span class="product-badge" style="background:${store.badgeBg}; color:${store.badgeText};">${store.name}</span>
                            <img class="product-img" src="${placeholderImages[index]}" alt="${query}">
                            <div class="product-info">
                                <h3 class="product-title">${query} - أفضل الخيارات المتوفرة في ${store.name}</h3>
                                <div class="product-price">${price} $</div>
                                <a href="${store.link}" target="_blank" class="product-btn ${store.class}">
                                    عرض المنتج في ${store.name} <i class="fa-solid fa-arrow-left"></i>
                                </a>
                            </div>
                        </div>
                    `;
                    grid.innerHTML += productCard;
                });

            }, 1000);
        }
    </script>
</body>
</html>
