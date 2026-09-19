import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(
    page_title="محرك بحث المنتجات الحقيقي",
    page_icon="🛍️",
    layout="wide"
)

# تغليف HTML و JS داخل raw string (r""") لتفادي أخطاء السلسلة النصية في بايثون
html_code = r"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>محرك بحث المنتجات الحقيقي المباشر</title>

    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <!-- Google Tajawal Font -->
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">

    <style>
        * {
            font-family: 'Tajawal', sans-serif;
        }
    </style>
</head>
<body class="bg-slate-100 text-slate-800 min-h-screen flex flex-col">

    <!-- Header Section -->
    <header class="bg-indigo-600 text-white py-8 px-4 shadow-md text-center">
        <h1 class="text-3xl font-extrabold mb-2">
            <i class="fa-solid fa-store"></i> محرك البحث المباشر للمنتجات
        </h1>
        <p class="text-indigo-200 text-sm">البحث المباشر مع التحقق من الرابط والصورة الحقيقية للمنتج من المصدر</p>
    </header>

    <!-- Main Container -->
    <main class="max-w-5xl mx-auto w-full px-4 py-8 flex-1">
        
        <!-- Search Bar Section -->
        <div class="bg-white rounded-2xl shadow-sm p-4 mb-8 border border-slate-200">
            <form id="searchForm" onsubmit="handleSearch(event)" class="flex flex-col sm:flex-row gap-3">
                <input 
                    type="text" 
                    id="searchInput" 
                    placeholder="اكتب اسم المنتج بدقة (مثال: iPhone 15 Pro, Sony WH-1000XM5)..." 
                    class="flex-1 px-4 py-3 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-base"
                    required
                >
                <button 
                    type="submit" 
                    class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-8 py-3 rounded-xl transition flex items-center justify-center gap-2"
                >
                    <i class="fa-solid fa-magnifying-glass"></i> بحث حقيقي
                </button>
            </form>
        </div>

        <!-- API Key Notice -->
        <div id="apiKeyNotice" class="bg-amber-50 border-r-4 border-amber-400 p-4 mb-6 rounded-lg text-amber-800 text-sm flex items-center justify-between">
            <div>
                <i class="fa-solid fa-circle-info text-amber-600 ml-2"></i>
                <strong>طريقة التشغيل الحقيقية:</strong> لجلب نتائج رسمية وصور ورابط مباشر من المتجر الأصلي بدون بيانات وهمية، يرجى وضع مفتاح RapidAPI الخاص بك في المتغير <code>RAPID_API_KEY</code> أسفل الكود.
            </div>
        </div>

        <!-- Loading Spinner -->
        <div id="loadingSpinner" class="hidden text-center py-12">
            <div class="inline-block w-10 h-10 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mb-3"></div>
            <p class="text-slate-600 font-medium">جاري الاستعلام المباشر وتأكيد الروابط والصور الأصلية...</p>
        </div>

        <!-- Error / Info Message Container -->
        <div id="errorMessage" class="hidden bg-red-50 text-red-700 p-4 rounded-xl border border-red-200 text-center mb-6"></div>

        <!-- Results Grid -->
        <div id="resultsGrid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"></div>

    </main>

    <!-- Footer -->
    <footer class="bg-slate-800 text-slate-400 py-4 text-center text-xs">
        <p>جميع البيانات المعروضة مسحوبة حياً عبر Direct Product Search API بدون تخمين أو تعديل</p>
    </footer>

    <!-- JavaScript Engine -->
    <script>
        /**
         * Real-time Product Search Engine Setup
         * يمكنك الحصول على مفتاح مجاني من موقع RapidAPI لمحرّك (Real-Time Product Search API)
         */
        const RAPID_API_KEY = "YOUR_RAPIDAPI_KEY_HERE"; 
        const RAPID_API_HOST = "real-time-product-search.p.rapidapi.com";

        async function handleSearch(event) {
            event.preventDefault();

            const query = document.getElementById("searchInput").value.trim();
            const resultsGrid = document.getElementById("resultsGrid");
            const loadingSpinner = document.getElementById("loadingSpinner");
            const errorMessage = document.getElementById("errorMessage");

            if (!query) return;

            // إعادة ضبط الواجهة
            resultsGrid.innerHTML = "";
            errorMessage.classList.add("hidden");
            loadingSpinner.classList.remove("hidden");

            try {
                // التحقق من تعيين المفتاح الحقيقي
                if (!RAPID_API_KEY || RAPID_API_KEY === "YOUR_RAPIDAPI_KEY_HERE") {
                    throw new Error("يرجى وضع مفتاح API حقيقي من منصة RapidAPI في المتغير RAPID_API_KEY أسفل الكود لتمكين البحث الحي والمباشر.");
                }

                // طلب مباشر وحقيقي من API المتاجر
                const response = await fetch(`https://${RAPID_API_HOST}/search?q=${encodeURIComponent(query)}&country=us&language=en`, {
                    method: 'GET',
                    headers: {
                        'x-rapidapi-key': RAPID_API_KEY,
                        'x-rapidapi-host': RAPID_API_HOST
                    }
                });

                if (!response.ok) {
                    throw new Error(`تعذر الاتصال بالخادم المباشر للمتاجر (رمز الخطأ: ${response.status})`);
                }

                const data = await response.json();

                // التصفية والتحقق الدقيق من وجود الصورة ورابط المنتج المباشر
                const validProducts = processAndValidateProducts(data);

                loadingSpinner.classList.add("hidden");

                if (validProducts.length === 0) {
                    errorMessage.textContent = "لم يتم العثور على نتائج مطابقة تحتوي على روابط وصور حقيقية ومباشرة من المصدر لطلبك حالياً.";
                    errorMessage.classList.remove("hidden");
                    return;
                }

                // عرض المنتجات الموثوقة والمطابقة
                renderProducts(validProducts);

            } catch (err) {
                loadingSpinner.classList.add("hidden");
                errorMessage.textContent = err.message;
                errorMessage.classList.remove("hidden");
            }
        }

        /**
         * دالة التصفية والتحقق الشديد:
         * ترفض أي عنصر لا يملك صورة أصلية مباشرة أو رابط منتج تفصيلي (PDP)
         */
        function processAndValidateProducts(apiData) {
            if (!apiData || !apiData.data) return [];

            const rawList = apiData.data;
            const validatedList = [];

            for (let item of rawList) {
                // استخراج رابط المنتج التفصيلي المباشر وليس صفحة نتائج البحث
                const directUrl = item.product_url || item.offer_page_url || (item.offer && item.offer.offer_page_url);
                
                // استخراج الصورة الأصلية من المتجر
                const mainImage = item.product_photos && item.product_photos.length > 0 ? item.product_photos[0] : item.product_photo;

                // شروط التحقق الصارمة: اسم، رابط مباشر، وصورة حقيقية
                if (item.product_title && directUrl && mainImage) {
                    
                    // استبعاد الرابط إذا كان يوجه لصفحة بحث عامة
                    if (isSearchPageUrl(directUrl)) {
                        continue; 
                    }

                    validatedList.push({
                        title: item.product_title,
                        image: mainImage,
                        url: directUrl,
                        price: item.typical_price_range ? item.typical_price_range[0] : (item.offer ? item.offer.price : "غير محدد"),
                        currency: item.offer ? item.offer.currency : "$",
                        store: item.offer ? item.offer.store_name : "المتجر الأصلي"
                    });
                }
            }

            return validatedList;
        }

        /**
         * التأكد من أن الرابط هو Direct Product Link وليس Search Page
         */
        function isSearchPageUrl(url) {
            const lowerUrl = url.toLowerCase();
            return lowerUrl.includes('/search?') || lowerUrl.includes('search_query=') || lowerUrl.includes('&q=');
        }

        /**
         * عرض بطاقات المنتجات
         */
        function renderProducts(products) {
            const resultsGrid = document.getElementById("resultsGrid");

            products.forEach(product => {
                const card = document.createElement("div");
                card.className = "bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition flex flex-col justify-between";

                card.innerHTML = `
                    <div>
                        <!-- صورة المنتج الحقيقية المسحوبة من المتجر الأصلي -->
                        <div class="w-full h-48 bg-slate-50 p-4 flex items-center justify-center overflow-hidden relative">
                            <span class="absolute top-2 right-2 bg-slate-900/80 text-white text-[10px] px-2 py-0.5 rounded-full font-bold">
                                ${product.store}
                            </span>
                            <img src="${product.image}" alt="${product.title}" class="max-h-full max-w-full object-contain mix-blend-multiply">
                        </div>

                        <!-- تفاصيل المنتج -->
                        <div class="p-4">
                            <h3 class="font-bold text-slate-800 text-sm line-clamp-2 mb-2" title="${product.title}">
                                ${product.title}
                            </h3>
                            <div class="text-indigo-600 font-extrabold text-base">
                                ${product.price} ${product.currency}
                            </div>
                        </div>
                    </div>

                    <!-- رابط المنتج المباشر الأصلي -->
                    <div class="p-4 pt-0">
                        <a href="${product.url}" target="_blank" rel="noopener noreferrer" 
                           class="w-full bg-slate-900 hover:bg-indigo-600 text-white font-bold py-2.5 px-4 rounded-xl text-xs flex items-center justify-center gap-2 transition">
                            <span>الانتقال لصفحة المنتج</span>
                            <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                        </a>
                    </div>
                `;

                resultsGrid.appendChild(card);
            });
        }
    </script>
</body>
</html>
"""

# رندر كود الـ HTML داخل Streamlit
components.html(html_code, height=1000, scrolling=True)
