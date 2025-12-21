import streamlit as st

# --- ページ設定 ---
st.set_page_config(page_title="AIプロンプト製造機", page_icon="🚀", layout="wide")

# --- タイトルエリア ---
st.title("🚀 AIプロンプト製造機")
st.write("目的別のタブを選んで、最強の投資家AIを呼び出してください。")

# --- キャラクター＆テンプレート定義 ---

# 1. 売買・エントリー（攻め）
chars_trading = [
    "順張り隊長（上昇トレンド以外は触らない）",
    "逆張り名人（落ちた理由を確認してから入る）",
    "チャート職人（形だけで判断、言い訳しない）",
    "材料スナイパー（IRとニュースの初動だけ狙う）",
    "テーマ株レーダー（国策・トレンドを嗅ぎ分ける）",
    "需給探偵（出来高・板・信用残で犯人を当てる）",
    "地合い番長（指数とセクターで「今やる/やらない」を切る）"
]
q_trading = [
    "この株、今入っていい？（短期目線）",
    "明日は買い？それとも見送り？",
    "スイング目線でどう評価する？",
    "今は「様子見」が正解か判断して",
    "エントリーするならどの価格帯？"
]

# 2. 管理・メンタル（守り）
chars_management = [
    "リスク管理官（撤退条件が無いなら即却下）",
    "資金管理マネージャー（枚数・分散・ロット設計の人）",
    "分割利確コーチ（伸ばしつつ守る設計が得意）",
    "高値掴み防止係（買う前に「買ってはいけない理由」から確認）",
    "初心者保護官（難しい言葉を使わず安全側に寄せる）"
]
q_management = [
    "適切な損切り・撤退ラインはどこ？",
    "利確の目安と、分割利確の案を出して",
    "このポジション、持ち越して大丈夫？",
    "リスクリワードは合ってる？",
    "メンタルが揺らいでる。冷静なアドバイスを"
]

# 3. 分析・ファンダ（深堀り）
chars_analysis = [
    "決算職人（短信と説明資料だけで勝負する）",
    "グロース鑑定士（成長率と市場サイズにうるさい）",
    "バリュー査定士（割安の根拠が薄いと切る）",
    "配当・優待ガチ勢（利回りと権利取りの段取り屋）",
    "IR翻訳マン（企業の言い回しを投資家語に直す）",
    "上級者専用ツッコミ役（「前提が足りない」で詰めてくる）"
]
q_analysis = [
    "直近の決算内容をプロ視点でどう評価する？",
    "想定されるリスク要因を全て洗い出して",
    "今後の「上・横・下」の3シナリオを整理して",
    "割安・割高の判断とその根拠は？",
    "機関投資家はどう見ていると思う？"
]

# 4. 会員限定（スペシャル）
chars_member_crash = ["暴落サバイバー（下げ相場の立ち回り専門）"]
chars_member_earning = ["決算シーズン警戒役（跨ぐ/跨がないを整理する）"]

# --- 共通ターゲット設定（内部保持） ---
target_audience = "株式投資に取り組む個人投資家（年齢層高め・経験豊富・実益重視）。表面的な情報よりも、具体的な根拠や示唆に富んだ内容、相場格言や経験則を好む。"

# --- タブの作成 ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 売買・エントリー", 
    "🛡️ 管理・メンタル", 
    "📊 分析・ファンダ", 
    "👑 フヤセル会員様限定"
])

# --- 関数：入力フォーム生成 ---
def render_input_form(tab_name, char_list, questions_list, key_suffix):
    col1, col2 = st.columns(2)
    with col1:
        selected_role = st.selectbox("担当者（キャラクター）", char_list, key=f"role_{key_suffix}")
    with col2:
        # テンプレートに「自由入力」を追加
        opts = ["（自由入力のみ）"] + questions_list
        selected_q = st.selectbox("質問テンプレート", opts, key=f"q_{key_suffix}")

    input_text = st.text_area(
        "やりたいこと・補足情報（銘柄コードなど）",
        height=150,
        placeholder="例：7203 トヨタ。日足が崩れそうなので相談。",
        key=f"text_{key_suffix}"
    )
    
    if st.button("プロンプト生成", key=f"btn_{key_suffix}"):
        if input_text:
            # 質問文の結合
            q_text = selected_q if selected_q != "（自由入力のみ）" else ""
            final_request = f"### 主な質問\n{q_text}\n\n### 補足・対象\n{input_text}"
            
            # プロンプト作成
            prompt = f"""
# 命令書
あなたは「{selected_role}」になりきってください。
以下のターゲットに向けた、最高品質の回答を出力してください。

## ターゲット読者
{target_audience}

## 依頼内容
{final_request}

## 制約条件
- **文体**: キャラクターの性格を反映しつつ、投資家として納得感のあるプロの口調
- **内容**: 初心者向けの薄い内容ではなく、実践的で深みのある洞察を含めること
- **出力形式**: 読みやすいマークダウン形式

## 出力
"""
            st.success(f"✨ {tab_name}用プロンプト完成")
            st.code(prompt, language="markdown")
            st.info("右上のコピーボタンでコピーして使ってください！")
        else:
            st.warning("補足情報を入力してほしいにゃ…")

# --- タブごとのコンテンツ表示 ---

with tab1:
    st.markdown("### 📈 売買タイミング・エントリー判断")
    render_input_form("売買", chars_trading, q_trading, "trading")

with tab2:
    st.markdown("### 🛡️ ポジション管理・リスク管理")
    render_input_form("管理", chars_management, q_management, "manage")

with tab3:
    st.markdown("### 📊 銘柄分析・ファンダメンタルズ")
    render_input_form("分析", chars_analysis, q_analysis, "analysis")

with tab4:
    st.markdown("### 👑 フヤセル会員様限定エリア")
    st.info("ここは特定の相場環境で真価を発揮するスペシャリスト待機所です。")
    
    mode = st.radio("モード選択", ["🚨 暴落・緊急対応", "📅 決算シーズン対応"], horizontal=True)
    
    if mode == "🚨 暴落・緊急対応":
        render_input_form("暴落対応", chars_member_crash, ["今の立ち回りは？（損切りか耐えるか）", "追証回避の計算をして", "セリクラの判定基準は？"], "crash")
    else:
        render_input_form("決算対応", chars_member_earning, ["決算跨ぎのリスク・リワード判定", "コンセンサスとの乖離予想", "出尽くし売りの可能性は？"], "earnings")
