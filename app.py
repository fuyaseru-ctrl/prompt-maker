import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(
    page_title="投資分析プロンプト生成ツール",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 関数定義 ---

def copy_button_component(text_to_copy):
    """
    JavaScriptを使用してクリップボードにテキストをコピーするボタンを表示する関数
    """
    # テキスト内の改行やクォートをJS用にエスケープ処理
    escaped_text = text_to_copy.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    
    js_code = f"""
    <script>
    function copyText() {{
        const textToCopy = `{escaped_text}`;
        navigator.clipboard.writeText(textToCopy).then(function() {{
            const btn = document.getElementById("copyBtn");
            btn.innerText = "✅ コピーしました！";
            btn.style.backgroundColor = "#e0ffe0";
            setTimeout(() => {{
                btn.innerText = "📋 コピーする";
                btn.style.backgroundColor = "#ffffff";
            }}, 2000);
        }}, function(err) {{
            console.error('Async: Could not copy text: ', err);
        }});
    }}
    </script>
    <div style="text-align: right; margin-top: 5px;">
        <button id="copyBtn" onclick="copyText()" style="
            background-color: #ffffff; 
            border: 1px solid #d6d6d8; 
            border-radius: 4px; 
            padding: 8px 16px; 
            font-size: 14px;
            cursor: pointer; 
            color: #31333F;
            font-weight: 600;
            font-family: 'Source Sans Pro', sans-serif;">
            📋 コピーする
        </button>
    </div>
    """
    components.html(js_code, height=60)

# --- メイン画面 ---

st.title("🤖 株式分析AIプロンプト生成ツール")
st.markdown("銘柄コードを入力して、分析用のプロンプトを作成しますにゃ。")

# サイドバー設定
st.sidebar.header("設定メニュー")

# 以前「株ドラゴン」だった部分をリネーム！
st.sidebar.subheader("📡 フヤセルジワジワレーダー")
target_tickers = st.sidebar.text_area(
    "銘柄コード (カンマ区切り)", 
    value="7203, 9984, 8306",
    height=100
)

analysis_focus = st.sidebar.selectbox(
    "分析の視点",
    ["総合分析", "業績推移", "チャート形状", "将来性・材料"]
)

# 生成ボタン
if st.button("プロンプトを生成する", type="primary"):
    # ここでプロンプトの中身を作ります
    prompt_text = f"""
# 以下の銘柄について{analysis_focus}を行ってください。

## 対象銘柄
{target_tickers}

## 分析指示
あなたはプロの証券アナリストです。
上記銘柄について、投資家が注目すべき{analysis_focus}のポイントを
わかりやすく解説してください。

## 出力形式
- マークダウン形式
- 重要な数字は太字
- 最後に「フヤセルジワジワレーダー」による総評を入れてください。
"""
    st.session_state.generated_prompt = prompt_text
    st.success("プロンプトを生成しましたにゃ！")

# --- 結果表示エリア ---

st.markdown("---")

if 'generated_prompt' in st.session_state and st.session_state.generated_prompt:
    st.subheader("📝 生成されたプロンプト")
    
    # 【1つ目のコピー】標準のコードブロック（右上にアイコンあり）
    st.code(st.session_state.generated_prompt, language="markdown")
    
    # 【2つ目のコピー】追加したカスタムボタン
    # プロンプトの下に配置
    copy_button_component(st.session_state.generated_prompt)
    
    st.caption("※右上のアイコンか、下の「コピーする」ボタン、どちらでもコピーできますにゃ！")

else:
    st.info("サイドバーで銘柄を入力して「プロンプトを生成する」を押してください。")
