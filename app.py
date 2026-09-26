<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>موقع الذكاء الاصطناعي</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: #0f172a;
            color: #f8fafc;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }

        header {
            background-color: #1e293b;
            padding: 1rem 2rem;
            text-align: center;
            border-bottom: 1px solid #334155;
        }

        #chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .message {
            max-width: 75%;
            padding: 1rem;
            border-radius: 12px;
            line-height: 1.6;
            white-space: pre-wrap;
        }

        .user-message {
            align-self: flex-start;
            background-color: #2563eb;
            color: #ffffff;
            border-bottom-right-radius: 2px;
        }

        .ai-message {
            align-self: flex-end;
            background-color: #334155;
            color: #f8fafc;
            border-bottom-left-radius: 2px;
        }

        #input-container {
            padding: 1rem;
            background-color: #1e293b;
            display: flex;
            gap: 0.5rem;
            border-top: 1px solid #334155;
        }

        input {
            flex: 1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            border: 1px solid #475569;
            background-color: #0f172a;
            color: #fff;
            outline: none;
        }

        button {
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            border: none;
            background-color: #2563eb;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        button:hover {
            background-color: #1d4ed8;
        }
    </style>
</head>
<body>

    <header>
        <h2>مساعد الذكاء الاصطناعي</h2>
    </header>

    <div id="chat-container"></div>

    <div id="input-container">
        <input type="text" id="user-input" placeholder="اكتب سؤالك هنا..." onkeydown="if(event.key==='Enter') sendMessage()">
        <button onclick="sendMessage()">إرسال</button>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const chatContainer = document.getElementById('chat-container');
            const text = input.value.trim();

            if (!text) return;

            // إضافة رسالة المستخدم
            appendMessage(text, 'user-message');
            input.value = '';

            // إضافة مؤشر الانتظار
            const loadingDiv = appendMessage('جاري التفكير...', 'ai-message');

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });

                const data = await response.json();
                loadingDiv.textContent = data.reply || data.error;
            } catch (err) {
                loadingDiv.textContent = 'حدث خطأ في الاتصال بالسيرفر.';
            }

            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function appendMessage(text, className) {
            const chatContainer = document.getElementById('chat-container');
            const div = document.createElement('div');
            div.className = `message ${className}`;
            div.textContent = text;
            chatContainer.appendChild(div);
            chatContainer.scrollTop = chatContainer.scrollHeight;
            return div;
        }
    </script>
</body>
</html>
