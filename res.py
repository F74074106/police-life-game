import os
import google.generativeai as genai
from flask import Flask, render_template_string, request

# =================設定區=================
# 請將下方的 "你的_GOOGLE_API_KEY_貼在這裡" 換成你剛剛申請的那串鑰匙
API_KEY = "AIzaSyD4xQDUwH9iN67mHpdVBKbOhzeg4f_SUl0"

# 設定 AI 模型
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash')


app = Flask(__name__)

# =================人設 (Prompt) 設定區=================
# 這裡就是這個網站的靈魂，你可以隨意修改這些指令！
STYLES = {
    "comfort": "你現在是一位溫柔知性的心理諮商師。請用充滿同理心、溫暖的語氣安慰使用者。告訴他事情會好轉的，給予一些正向的鼓勵。不要說教，只要傾聽和安撫。",
    "roast": "你現在是一位超級毒舌的脫口秀演員。請用幽默、諷刺、稍微尖酸刻薄的語氣回應。針對使用者的煩惱進行吐槽，讓他意識到這根本沒什麼大不了。可以好笑，但不要使用髒話。",
    "ceo": "你現在是一位霸道總裁。語氣要狂妄、自信、充滿佔有慾。用一種'天塌下來有我頂著'的態度回應。常用詞：'女人/男人'、'記住'、'不允許你這樣'。",
    "joke": "你現在是一位喜劇演員。不管使用者說什麼悲慘的事，你都要想辦法把它轉成一個相關的笑話或幽默的段子，讓他破涕為笑。",
    "nonsense": "你是一位廢話大師。請用看似高深莫測但其實完全沒有內容的「廢話文學」來回應。例如：'聽君一席話，如聽一席話'。"
}

# =================前端網頁 (HTML + CSS)=================
# 為了方便，我直接把網頁寫在這裡。使用了 Tailwind CSS 讓介面變漂亮。
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 情緒樹洞</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #f3f4f6; font-family: 'Microsoft JhengHei', sans-serif; }
        .loader { border-top-color: #3498db; -webkit-animation: spinner 1.5s linear infinite; animation: spinner 1.5s linear infinite; }
        @keyframes spinner { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen px-4">

    <div class="bg-white p-8 rounded-2xl shadow-xl max-w-md w-full">
        <h1 class="text-3xl font-bold text-center text-gray-800 mb-2">🌳 情緒樹洞</h1>
        <p class="text-center text-gray-500 mb-6">把你的心情告訴 AI，選擇一種回應風格</p>

        <form method="POST" action="/" id="moodForm">
            <div class="mb-4">
                <label class="block text-gray-700 text-sm font-bold mb-2">你今天怎麼了？</label>
                <textarea name="user_input" rows="4" class="w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-blue-500" placeholder="例如：工作好累，老闆今天又罵我..." required>{{ user_input if user_input else '' }}</textarea>
            </div>

            <div class="mb-6">
                <label class="block text-gray-700 text-sm font-bold mb-2">選擇回應風格：</label>
                <div class="grid grid-cols-2 gap-2">
                    <label class="cursor-pointer border rounded-lg p-2 hover:bg-blue-50 flex items-center">
                        <input type="radio" name="style" value="comfort" class="mr-2" checked> 👼 溫柔安慰
                    </label>
                    <label class="cursor-pointer border rounded-lg p-2 hover:bg-red-50 flex items-center">
                        <input type="radio" name="style" value="roast" class="mr-2"> 😈 毒舌吐槽
                    </label>
                    <label class="cursor-pointer border rounded-lg p-2 hover:bg-purple-50 flex items-center">
                        <input type="radio" name="style" value="ceo" class="mr-2"> 😎 霸道總裁
                    </label>
                    <label class="cursor-pointer border rounded-lg p-2 hover:bg-yellow-50 flex items-center">
                        <input type="radio" name="style" value="joke" class="mr-2"> 🤡 講個笑話
                    </label>
                    <label class="cursor-pointer border rounded-lg p-2 hover:bg-gray-50 flex items-center col-span-2">
                        <input type="radio" name="style" value="nonsense" class="mr-2"> 🌀 廢話文學
                    </label>
                </div>
            </div>

            <button type="submit" class="w-full bg-blue-600 text-white font-bold py-3 rounded-lg hover:bg-blue-700 transition duration-300">
                生成回應 ✨
            </button>
        </form>

        {% if result %}
        <div class="mt-8 bg-gray-50 border-l-4 border-blue-500 p-4 rounded animate-fade-in">
            <p class="text-sm text-gray-500 mb-1">AI 的回應 ({{ style_name }})：</p>
            <p class="text-gray-800 text-lg leading-relaxed font-medium">{{ result }}</p>
        </div>
        {% endif %}
        
        {% if error %}
        <div class="mt-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
            <strong class="font-bold">發生錯誤：</strong>
            <span class="block sm:inline">{{ error }}</span>
        </div>
        {% endif %}
    </div>

</body>
</html>
"""

# =================後端路由處理=================
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    user_input = ""
    style_name = ""
    error = None

    if request.method == 'POST':
        user_input = request.form.get('user_input')
        style_key = request.form.get('style')
        
        # 取得對應的風格名稱供顯示用
        style_map = {"comfort": "溫柔安慰", "roast": "毒舌吐槽", "ceo": "霸道總裁", "joke": "講笑話", "nonsense": "廢話文學"}
        style_name = style_map.get(style_key, "AI")

        # 取得系統指令 (Prompt)
        system_prompt = STYLES.get(style_key, STYLES['comfort'])

        try:
            # 呼叫 Google Gemini API
            chat = model.start_chat(history=[])
            response = chat.send_message(f"System Instruction: {system_prompt}\n\nUser Input: {user_input}")
            result = response.text
        except Exception as e:
            error = f"連線失敗，請檢查 API Key 或網路。錯誤訊息: {str(e)}"

    return render_template_string(HTML_TEMPLATE, result=result, user_input=user_input, style_name=style_name, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5000)