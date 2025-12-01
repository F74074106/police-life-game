import google.generativeai as genai

# ==========================================
# 請在這裡貼上你的 API Key
API_KEY = "AIzaSyD4xQDUwH9iN67mHpdVBKbOhzeg4f_SUl0"
# ==========================================

genai.configure(api_key=API_KEY)

print("正在查詢你的帳號可用模型...\n")

try:
    found_any = False
    # 列出所有模型
    for m in genai.list_models():
        # 我們只找可以「生成內容 (generateContent)」的模型
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ 發現可用模型: {m.name}")
            found_any = True
    
    if not found_any:
        print("❌ 連線成功，但沒有找到任何可用的生成模型。")
    else:
        print("\n請複製上面其中一個模型的名字（例如 models/gemini-pro），填入你的程式碼中！")

except Exception as e:
    print(f"❌ 發生錯誤: {e}")