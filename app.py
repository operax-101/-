import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة في Streamlit
st.set_page_config(
    page_title="PriceFinder AI 2.0 Pro",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# كود HTML و JavaScript المكتمل مع صور متعددة لكل منتج ومتجر
html_code = """
<!DOCTYPE html>
<html lang="ar" dir="rtl" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>PriceFinder AI 2.0 Pro</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: { 50: '#eef2ff', 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca' }
          }
        }
      }
    }
  </script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');
    body { font-family: 'Tajawal', sans-serif; }
  </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen pb-16">

  <!-- Header -->
  <header class="sticky top-0 z-50 bg-slate-800/90 backdrop-blur-md border-b border-slate-700">
    <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
      <div class="flex items-center gap-2 text-indigo-400 font-extrabold text-xl">
        <span>🔍 PriceFinder AI</span>
      </div>
      <div class="flex items-center gap-3">
        <select id="currencySelect" onchange="updateCurrency()" class="bg-slate-700 text-white text-sm font-bold rounded-lg px-3 py-1.5 border border-slate-600 outline-none cursor-pointer">
          <option value="OMR">OMR (ر.ع.)</option>
          <option value="AED">AED (د.إ)</option>
          <option value="SAR">SAR (ر.س)</option>
          <option value="USD">USD ($)</option>
          <option value="EUR">EUR (€)</option>
        </select>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <main class="max-w-7xl mx-auto px-4 pt-10">
    <section class="text-center space-y-4 max-w-3xl mx-auto mb-10">
      <h1 class="text-3xl sm:text-5xl font-black text-white leading-tight">
        قارن أسعار المتاجر فوراً بالذكاء الاصطناعي
      </h1>
      <p class="text-slate-400 text-sm sm:text-base">
        يبحث في Noon, AliExpress, Temu, و SHEIN ويعطيك خيارات الشراء بذكاء.
      </p>

      <form onsubmit="runSearch(event)" class="flex gap-2 bg-slate-800 p-2 rounded-2xl border border-slate-700 shadow-2xl">
        <input
          type="text"
          id="searchInput"
          placeholder="اكتب اسم أي منتج (مثال: حذاء رياضي، iPhone 15، ساعة ذكية، عطر)..."
          class="w-full bg-transparent text-white px-4 py-2 outline-none text-base"
        />
        <button
          type="submit"
          class="bg-indigo-600 hover:bg-indigo-700 font-bold text-white px-6 py-3 rounded-xl transition shrink-0 cursor-pointer"
        >
          بحث
        </button>
      </form>
    </section>

    <!-- Loading UI -->
    <div id="loadingUI" class="hidden text-center py-16 space-y-3">
      <div class="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
      <p id="loadingText" class="text-indigo-400 font-bold animate-pulse">جاري الاستعلام والمقارنة بين المتاجر...</p>
    </div>

    <!-- Results Container -->
    <div id="resultsUI" class="hidden space-y-6">
      <div class="border-b border-slate-800 pb-4 flex justify-between items-center flex-wrap gap-2">
        <h2 id="resultTitle" class="text-2xl font-bold"></h2>
        <span class="text-xs text-emerald-400 font-bold bg-emerald-950/60 px-3 py-1 rounded-full border border-emerald-800">
          تم العثور على 4 متاجر
        </span>
      </div>

      <div id="cardsGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"></div>
    </div>
  </main>

  <script>
    const RATES = { OMR: 0.385, AED: 3.67, SAR: 3.75, USD: 1.0, EUR: 0.92 };
    const SYMBOLS = { OMR: 'ر.ع.', AED: 'د.إ', SAR: 'ر.س', USD: '$', EUR: '€' };

    let lastQuery = '';

    // دالة توفر صور مختلفة لكل متجر حسب تصنيف البحث
    function getCategoryData(query) {
      const q = query.toLowerCase();
      
      if (q.includes('حذاء') || q.includes('شوز') || q.includes('shoe') || q.includes('sneaker') || q.includes('nike')) {
        return {
          baseUSD: 65,
          imgs: [
            'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&fit=crop',
            'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=600&fit=crop',
            'https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=600&fit=crop',
            'https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=600&fit=crop'
          ]
        };
      }
      if (q.includes('ساعة') || q.includes('watch') || q.includes('smartwatch')) {
        return {
          baseUSD: 85,
          imgs: [
            'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&fit=crop',
            'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=600&fit=crop',
            'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=600&fit=crop',
            'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=600&fit=crop'
          ]
        };
      }
      if (q.includes('آيفون') || q.includes('iphone') || q.includes('هاتف') || q.includes('phone') || q.includes('سامسونج')) {
        return {
          baseUSD: 780,
          imgs: [
            'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600&fit=crop',
            'https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=600&fit=crop',
            'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=600&fit=crop',
            'https://images.unsplash.com/photo-1580910051074-3eb694886505?w=600&fit=crop'
          ]
        };
      }
      if (q.includes('حقيبة') || q.includes('شنطة') || q.includes('bag')) {
        return {
          baseUSD: 42,
          imgs: [
            'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&fit=crop',
            'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=600&fit=crop',
            'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&fit=crop',
            'https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=600&fit=crop'
          ]
        };
      }
      if (q.includes('عطر') || q.includes('perfume')) {
        return {
          baseUSD: 95,
          imgs: [
            'https://images.unsplash.com/photo-1541643600914-78b084683601?w=600&fit=crop',
            'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=600&fit=crop',
            'https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=600&fit=crop',
            'https://images.unsplash.com/photo-1588405748880-12d1d2a59f75?w=600&fit=crop'
          ]
        };
      }

      // صور افتراضية لمختلف المنتجات العامة
      return {
        baseUSD: 40,
        imgs: [
          'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&fit=crop',
          'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&fit=crop',
          'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=600&fit=crop',
          'https://images.unsplash.com/photo-1560343090-f0409e92791a?w=600&fit=crop'
        ]
      };
    }

    function runSearch(e) {
      if (e) e.preventDefault();
      const query = document.getElementById('searchInput').value.trim();
      if (!query) return;

      lastQuery = query;
      document.getElementById('resultsUI').classList.add('hidden');
      document.getElementById('loadingUI').classList.remove('hidden');

      setTimeout(() => {
        displayResults();
        document.getElementById('loadingUI').classList.add('hidden');
        document.getElementById('resultsUI').classList.remove('hidden');
      }, 500);
    }

    function updateCurrency() {
      if (lastQuery) displayResults();
    }

    function displayResults() {
      const currency = document.getElementById('currencySelect').value;
      const meta = getCategoryData(lastQuery);
      const base = meta.baseUSD;
      const rate = RATES[currency] || 1;
      const sym = SYMBOLS[currency];

      document.getElementById('resultTitle').innerText = `نتائج البحث عن: "${lastQuery}"`;

      const stores = [
        { store: 'Noon', title: `${lastQuery} - الاصلي الضمان العالي`, price: (base * 1.1 * rate).toFixed(2), shipUSD: 0, score: 98, img: meta.imgs[0], url: 'https://www.noon.com' },
        { store: 'AliExpress', title: `منتج ${lastQuery} شحن سريع`, price: (base * 0.85 * rate).toFixed(2), shipUSD: 3.50, score: 94, img: meta.imgs[1], url: 'https://www.aliexpress.com' },
        { store: 'Temu', title: `عرض خاص: ${lastQuery} سعر اقتصادي`, price: (base * 0.65 * rate).toFixed(2), shipUSD: 0, score: 88, img: meta.imgs[2], url: 'https://www.temu.com' },
        { store: 'SHEIN', title: `${lastQuery} إكسسوارات الموضة`, price: (base * 0.72 * rate).toFixed(2), shipUSD: 2.00, score: 82, img: meta.imgs[3], url: 'https://www.shein.com' }
      ];

      const grid = document.getElementById('cardsGrid');
      grid.innerHTML = '';

      stores.forEach(item => {
        const shippingText = item.shipUSD === 0 ? 'مجاني' : `${(item.shipUSD * rate).toFixed(2)} ${sym}`;
        
        grid.innerHTML += `
          <div class="bg-slate-800 rounded-2xl border border-slate-700 p-4 flex flex-col justify-between shadow-lg hover:border-indigo-500 transition">
            <div>
              <div class="flex justify-between items-center mb-2">
                <span class="text-xs font-bold px-2.5 py-1 bg-indigo-950 text-indigo-300 rounded-md border border-indigo-800">${item.store}</span>
                <span class="text-xs text-emerald-400 font-bold">تطابق ${item.score}%</span>
              </div>
              <div class="aspect-square rounded-xl bg-slate-700 overflow-hidden mb-3">
                <img src="${item.img}" alt="${item.title}" class="w-full h-full object-cover hover:scale-105 transition duration-300" />
              </div>
              <h3 class="font-bold text-sm text-white line-clamp-2 mb-2">${item.title}</h3>
            </div>
            <div class="pt-3 border-t border-slate-700">
              <div class="text-2xl font-black text-white mb-1">${item.price} ${sym}</div>
              <div class="text-xs text-slate-400 mb-3">الشحن: ${shippingText}</div>
              <a href="${item.url}" target="_blank" rel="noopener noreferrer" class="block text-center w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl transition">
                رابط الشراء المباشر
              </a>
            </div>
          </div>
        `;
      });
    }
  </script>
</body>
</html>
"""

# عرض الواجهة كاملة داخل Streamlit
components.html(html_code, height=900, scrolling=True)
