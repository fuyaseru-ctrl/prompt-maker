import streamlit as st
import streamlit.components.v1 as components
import re
import unicodedata

# ページ設定
st.set_page_config(
    page_title="投資分析プロンプト生成ツール",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 関数定義 ---

def clean_tickers(text):
    """
    入力されたテキストを正規化し、リスト化する関数
    - 全角を半角に変換
    - スペース、改行、カンマで分割
    - 空白を除去し、大文字に変換
    """
    if not text:
        return []
    
    # 全角→半角変換 (NFKC正規化)
    normalized_text = unicodedata.normalize('NFKC', text)
    
    # 区切り文字（カンマ、スペース、改行）で分割
    tokens = re.split(r'[,\s\n]+', normalized_text)
    
    # 空文字を除去し、すべて大文字に変換
    clean_list = [t.upper() for t in tokens if t]
    
    return clean_list

def copy_button_component(text_to_copy):
    """
    JavaScriptを使用してクリップボードにテキストをコピーするボタンを表示する関数
    """
    escaped_text = text_to_copy.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    
    js_code = f"""
    <script>
    function copyText() {{
        const textToCopy = `{escaped_text}`;
        navigator.clipboard.writeText(textToCopy).then(function() {{
            const btn = document.getElementById("copyBtn");
            btn.innerText = "✅ コピー完了";
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

# --- サイドバー設定 ---

st.sidebar.header("設定メニュー")

# キャラクター選択（デフォルトはプロ）
character_role = st.sidebar.selectbox(
    "キャラクター設定",
    ["プロの証券アナリスト", "辛口ファンドマネージャー", "フヤにゃん（癒やし系）"],
    index=0
)

# 分析の視点 → 「聞きたいこと」に変更
analysis_focus = st.sidebar.selectbox(
    "聞きたいこと",
    [
        "今の株価での売買判断（買い/売り/様子見）",
        "直近の決算評価と業績推移",
        "チャート形状とテクニカル分析",
        "将来性と懸念材料のリスク分析",
        "機関投資家の動きと需給状況"
    ]
)

# --- メイン画面 ---

st.title("株式分析プロンプト生成")

# 銘柄入力（デフォルト空欄、説明書き調整）
raw_tickers = st.text_area(
    "銘柄コードを入力してください（スペース・改行・カンマ区切り対応 / 大文字小文字OK）", 
    value="",
    height=120,
    placeholder="例：\n7203\n9984\nMSFT"
)

# 生成ボタン
if st.button("プロンプトを生成する", type="primary"):
    
    # 入力データのクリーニング
    ticker_list = clean_tickers(raw_tickers)
    
    # --- エラー処理：ここだけフヤにゃん登場 ---
    if not ticker_list:
        st.error("フヤにゃん「にゃ、にゃんと！銘柄コードが空っぽだにゃ…。これじゃ分析できないよぉ〜。何か入力してほしいにゃ…（ふて寝）」")
    else:
        # 銘柄リストを文字列に変換（カンマ区切り）
        tickers_str = ", ".join(ticker_list)
        
        # プロンプト作成
        prompt_text = f"""
# 以下の銘柄について「{analysis_focus}」を中心に分析してください。

## 対象銘柄
{tickers_str}

## あなたの役割
{character_role}として振る舞ってください。

## 分析指示
上記銘柄について、投資家が最も知りたい情報を簡潔かつ論理的に解説してください。
特に「{analysis_focus}」については、具体的な根拠を示して結論を出してください。

## 出力形式
- マークダウン形式で見やすく
- 重要な数値や判定は太字
- 結論を先に述べる
"""
        st.session_state.generated_prompt = prompt_text
        
        # 成功メッセージ（標準語）
        st.success(f"{len(ticker_list)}件の銘柄でプロンプトを生成しました。")

# --- 結果表示エリア ---

if 'generated_prompt' in st.session_state and st.session_state.generated_prompt:
    st.markdown("---")
    st.subheader("生成結果")
    
    # 1つ目のコピー（標準）
    st.code(st.session_state.generated_prompt, language="markdown")
    
    # 2つ目のコピー（ボタン）
    copy_button_component(st.session_state.generated_prompt)
