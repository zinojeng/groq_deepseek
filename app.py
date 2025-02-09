import streamlit as st
import groq
import os

# 頁面配置
st.set_page_config(page_title="研究助手", layout="wide")

# 標題
st.title("🤖 AI 研究助手")

# 作者資訊
st.caption("""
Code by Dr. Tseng, Endocrinologist at Tungs' Taichung Metroharbor Hospital.
此程式使用 Groq DeepSeek 進行深度研究分析。
""")

# 程式說明
st.info("""
這是一個強大的研究助手工具，能夠幫助您深入探索任何主題。
使用 Groq DeepSeek 模型：
- 生成關鍵研究問題
- 進行深度研究分析
""")

# Sidebar for API keys and help information
with st.sidebar:
    st.title("⚙️ 設定與資訊")
    
    # API 設置移到最上方
    st.header("🔑 API 設置")
    
    groq_help = """
    如何獲取 Groq API Key:
    1. 訪問 Groq Console (https://console.groq.com/keys)
    2. 點擊右上角的 "Log In" 按鈕登入
    3. 如果是新用戶，需要先完成註冊
    4. 在左側選單中選擇 "API Keys"
    5. 點擊 "Create API Key" 按鈕
    6. 在表格中可以看到：
       - Name（金鑰名稱）
       - Secret Key（密鑰）
       - Created（創建時間）
       - Last Used（最後使用時間）
       - Usage（24小時內使用量）
    7. 複製並安全保存你的 Secret Key
    
    注意：請妥善保管你的 API key，避免未經授權的存取。
    """
    
    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        help=groq_help
    )
    
    # API key 驗證
    api_keys_valid = True
    if not groq_api_key:
        st.warning("請輸入必要的 API Key")
        api_keys_valid = False
    
    if api_keys_valid:
        # Set API key
        os.environ["GROQ_API_KEY"] = groq_api_key
    
    st.markdown("---")  # 分隔線
    
    # 模型資訊
    st.header("🤖 使用的 AI 模型")
    
    # 所有 expander 預設收合
    with st.expander("🚀 關於 DeepSeek-R1-Distill-Llama-70B"):
        st.markdown("""
        本應用使用的是 DeepSeek 的 R1 模型蒸餾版本，基於 Llama-3.3-70B-Instruct 
        模型進行微調。通過知識蒸餾保持了強大的推理能力，同時提高了效率。
        
        #### 主要特點：
        - 70B 參數規模
        - 128k 上下文窗口
        - 275 tps 生成速度
        - 支援鏈式思考 (Chain-of-Thought) 推理
        - 透過純強化學習 (RL) 提升推理能力
        
        #### 性能表現：
        - AIME 2024: Pass@1 分數 86.7%
        - MATH-500: Pass@1 分數 94.5% (所有蒸餾模型中最佳)
        - GPQA Diamond: 65.2%
        - LiveCode Bench: 57.5%
        
        #### 安全性與隱私：
        - 透過 Groq 的美國基礎設施部署
        - 查詢資料僅暫存於記憶體中
        - 會話結束後立即清除所有資料
        - 不會將資料傳送到 DeepSeek 的中國伺服器
        - 詳細隱私政策可參考 trust.groq.com
        
        #### 最佳使用建議：
        - 溫度設定 (Temperature): 0.5-0.7
          * 較低值 (0.5): 適合數學證明，結果更穩定
          * 較高值 (0.7): 適合創意解題，結果更多樣
        - 建議使用零樣本提示 (Zero-shot prompting)
        - 所有指令建議直接包含在用戶訊息中
        
        #### 應用場景：
        - 數學問題解決
        - 邏輯推理
        - 研究分析
        - 複雜問題的步驟分解
        - 結構化思考任務
        """)

@st.cache_resource
def initialize_groq():
    return groq.Groq(api_key=os.environ["GROQ_API_KEY"])


# 主要應用邏輯
def main():
    try:
        # 檢查 API key 是否有效
        if not groq_api_key:
            return
            
        # 初始化
        groq_client = initialize_groq()
        
        # 程式說明
        with st.expander("程式運作原理"):
            st.markdown("""
            1. **第一階段 - 問題生成**
               - 使用 DeepSeek 模型生成 5 個關鍵研究問題
               - 確保問題涵蓋主題的重要面向
            
            2. **第二階段 - 深入研究**
               - 使用 DeepSeek 模型進行詳細研究
               - 針對每個問題提供全面的答案和分析
            """)
        
        # 用戶輸入
        query = st.text_input(
            "🔍 請輸入您想研究的主題：",
            help="輸入任何您感興趣的主題，系統會自動生成研究問題並進行深入分析"
        )
        
        if st.button("開始研究"):
            if query:
                with st.spinner("正在生成研究問題..."):
                    completion = groq_client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": (
                                    "Suggest a list of 5 most important "
                                    f"questions to research on the topic: {query}"
                                )
                            }
                        ],
                        model="deepseek-r1-distill-llama-70b",
                    )
                    questions = completion.choices[0].message.content
                    st.write("### 研究問題：")
                    st.write(questions)
                
                with st.spinner("正在進行深入研究..."):
                    research_prompt = (
                        f"Based on these questions about {query}:\n{questions}\n\n"
                        f"Please provide a comprehensive research analysis following these steps:\n\n"
                        f"1. For each question:\n"
                        f"   - Use chain-of-thought reasoning to break down the problem\n"
                        f"   - Consider multiple perspectives and approaches\n"
                        f"   - Provide evidence and logical arguments\n"
                        f"   - Draw connections between related concepts\n\n"
                        f"2. After analyzing each question:\n"
                        f"   - Identify common themes and patterns\n"
                        f"   - Discuss potential implications\n"
                        f"   - Suggest areas for further investigation\n\n"
                        f"3. Conclude with:\n"
                        f"   - A synthesis of key findings\n"
                        f"   - Practical applications or recommendations\n"
                        f"   - Critical evaluation of the analysis\n\n"
                        f"Please structure your response clearly and use logical reasoning throughout."
                    )
                    
                    completion = groq_client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": research_prompt
                            }
                        ],
                        model="deepseek-r1-distill-llama-70b",
                        temperature=0.6,  # 設定適中的溫度值以平衡創意和準確性
                    )
                    st.write("### 研究結果：")
                    st.write(completion.choices[0].message.content)
            else:
                st.warning("請輸入研究主題")
    except Exception as e:
        st.error(f"發生錯誤：{str(e)}")


if __name__ == "__main__":
    main() 