import streamlit as st

# 1. 画面のタイトル
st.title("🚀 AIプロンプト製造機")
st.write("必要な情報を入力すると、AIへの指示書（プロンプト）を自動で作ります。")

# 2. 入力フォームを作る
with st.form("prompt_form"):
    # 左側と右側に列を分ける
    col1, col2 = st.columns(2)
    
    with col1:
        role = st.selectbox("AIの役割", ["プロのライター", "優秀なマーケター", "Pythonエンジニア", "親しみやすい相談相手"])
        target = st.text_input("ターゲット（誰向け？）", placeholder="例：30代の初心者")
    
    with col2:
        tone = st.selectbox("トーン（雰囲気）", ["論理的・冷静", "情熱的・エモーショナル", "親しみやすい・フランク", "丁寧・ビジネス"])
        output_format = st.text_input("出力形式", placeholder="例：箇条書き、マークダウン、表形式")

    # メインのやりたいこと
    goal = st.text_area("やりたいこと・テーマ（必須）", height=150, placeholder="例：ダイエットに挫折しないためのコツを5つ教えてほしい")

    # 生成ボタン
    submitted = st.form_submit_button("プロンプトを生成する")

# 3. ボタンが押されたらプロンプトを作る
if submitted:
    if not goal:
        st.error("「やりたいこと」を入力してください！")
    else:
        # プロンプトの組み立て（ここが製造機の心臓部）
        generated_prompt = f"""
# 命令書
あなたは「{role}」として振る舞ってください。
以下の制約条件と入力文をもとに、最高の回答を出力してください。

## 制約条件
- **ターゲット読者**: {target}
- **文体・トーン**: {tone}
- **出力形式**: {output_format}

## 入力文（やりたいこと）
{goal}

## 出力
"""
        st.markdown("### ✨ 完成したプロンプト")
        st.code(generated_prompt, language="markdown")
        st.success("右上のコピーボタンでコピーして、ChatGPTやClaudeに貼り付けて使ってください！")
