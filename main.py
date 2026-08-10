import gradio as gr
import time

# ==========================================
# Main Backend Function
# ==========================================

def research_assistant(file, task, question, progress=gr.Progress()):

    if file is None:
        gr.Warning("Please upload a document before analyzing.")
        return (
            "⚠️ No document uploaded",
            "Upload a PDF to see extracted entities here.",
            "### 👋 Upload a PDF to begin.\n\nOnce you upload a document and hit **Analyze**, your AI-generated response will appear here.",
            gr.update(visible=False),
        )

    progress(0.05, desc="📄 Reading document...")
    document = extract_pdf_text(file.name)
    time.sleep(0.15)

    progress(0.35, desc="🏷️ Classifying document...")
    classification = classify_document(document)
    time.sleep(0.15)

    progress(0.6, desc="👥 Extracting named entities...")
    entities = get_entities(document)
    time.sleep(0.15)

    task_prompts = {
        "Ask Question": question,
        "Summarize": "Summarize this document in concise bullet points.",
        "Explain Like I'm 10": "Explain this document as if teaching a 10 year old.",
        "Generate Quiz": "Generate 10 quiz questions with answers.",
        "Generate Flashcards": "Generate flashcards from this document.",
        "Interview Questions": "Generate interview questions based on this document.",
        "Executive Summary": "Create an executive summary of this document."
    }

    prompt = task_prompts.get(task, question)

    progress(0.8, desc="🤖 Thinking...")
    answer = ask_document(document, prompt)

    progress(1.0, desc="✅ Done!")
    gr.Info("Analysis complete!")

    return (
        f"🏷️ {classification}",
        entities,
        answer,
        gr.update(visible=True),
    )


def toggle_question_box(task):
    """Show the question textbox only when the user picks 'Ask Question'."""
    return gr.update(visible=(task == "Ask Question"))


def clear_all():
    return (
        None,
        "Ask Question",
        "",
        "💤 Waiting for a document...",
        "Upload a PDF to see extracted entities here.",
        "### 👋 Upload a PDF to begin.",
        gr.update(visible=False),
    )


# ==========================================
# Custom CSS — Vibrant, animated, glassmorphic theme
# ==========================================

css = """
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800;900&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root{
    --bg-page:#0F1020;
    --bg-panel:rgba(255,255,255,0.06);
    --bg-panel-soft:rgba(255,255,255,0.04);
    --border-soft:rgba(255,255,255,0.10);
    --border-strong:rgba(168,124,255,0.55);
    --text-primary:#F5F3FF;
    --text-muted:#A9A6C4;
    --accent:#8B5CF6;
    --accent-2:#EC4899;
    --accent-3:#22D3EE;
    --accent-soft:rgba(139,92,246,0.15);
    --accent-glow:rgba(139,92,246,0.45);
    --cta:linear-gradient(135deg,#8B5CF6 0%,#EC4899 100%);
    --cta-hover:linear-gradient(135deg,#7C3AED 0%,#DB2777 100%);
    --radius-lg:20px;
    --radius-md:14px;
    --transition:220ms cubic-bezier(0.4,0,0.2,1);
}

body, .gradio-container{
    background:
        radial-gradient(circle at 15% 10%, rgba(139,92,246,0.20) 0%, transparent 45%),
        radial-gradient(circle at 85% 0%, rgba(236,72,153,0.16) 0%, transparent 45%),
        radial-gradient(circle at 50% 100%, rgba(34,211,238,0.12) 0%, transparent 50%),
        var(--bg-page) !important;
    font-family:'Inter', sans-serif;
    color:var(--text-primary);
    background-attachment:fixed;
}

.gradio-container{
    max-width:1500px !important;
    margin:auto;
    padding:28px 20px 60px 20px;
}

footer{ display:none !important; }

/* ---------- Animated aurora blobs ---------- */
.aurora{
    position:fixed;
    border-radius:50%;
    filter:blur(90px);
    z-index:-1;
    opacity:0.55;
    animation:float 14s ease-in-out infinite;
}
.aurora.a1{ width:420px; height:420px; background:#8B5CF6; top:-120px; left:-100px; }
.aurora.a2{ width:380px; height:380px; background:#EC4899; bottom:-140px; right:-80px; animation-delay:3s; }
.aurora.a3{ width:320px; height:320px; background:#22D3EE; top:40%; right:10%; animation-delay:6s; }

@keyframes float{
    0%,100%{ transform:translate(0,0) scale(1); }
    50%{ transform:translate(30px,-40px) scale(1.08); }
}

/* ---------- Header ---------- */
.header-wrap{
    text-align:center;
    padding:38px 20px 30px 20px;
    position:relative;
}

.header-wrap h1{
    font-family:'Sora', sans-serif !important;
    font-weight:900 !important;
    font-size:2.8rem !important;
    letter-spacing:-0.02em !important;
    margin:0 !important;
    display:inline-block !important;
    line-height:1.25 !important;
    background:linear-gradient(90deg,#8B5CF6,#EC4899 45%,#22D3EE);
    background-size:200% auto;
    -webkit-background-clip:text;
    background-clip:text;
    color:transparent !important;
    animation:shine 6s linear infinite;
}

@keyframes shine{
    to{ background-position:200% center; }
}

.header-wrap .subtitle{
    font-family:'Inter', sans-serif;
    font-weight:500;
    color:var(--text-muted);
    font-size:1.05rem;
    margin-top:8px;
    letter-spacing:0.01em;
}

.header-wrap .rule{
    width:72px;
    height:4px;
    margin:20px auto 0 auto;
    border-radius:99px;
    background:linear-gradient(90deg,#8B5CF6,#EC4899,#22D3EE);
    box-shadow:0 0 16px var(--accent-glow);
}

.header-wrap .powered-by{
    font-family:'JetBrains Mono', monospace;
    font-size:0.8rem;
    letter-spacing:0.05em;
    color:var(--text-muted);
    margin-top:18px;
    text-transform:uppercase;
}

.header-wrap .powered-by b{
    color:var(--accent-3);
    font-weight:500;
}

.badge-row{
    display:flex;
    gap:10px;
    justify-content:center;
    flex-wrap:wrap;
    margin-top:18px;
}

.pill{
    font-family:'JetBrains Mono', monospace;
    font-size:0.72rem;
    padding:6px 14px;
    border-radius:99px;
    background:var(--bg-panel);
    border:1px solid var(--border-soft);
    color:var(--text-muted);
    backdrop-filter:blur(6px);
}

/* ---------- Panels / Groups ---------- */
.gr-group, .form{
    background:var(--bg-panel) !important;
    border:1px solid var(--border-soft) !important;
    border-radius:var(--radius-lg) !important;
    backdrop-filter:blur(14px);
    box-shadow:0 4px 24px rgba(0,0,0,0.25);
    transition:border-color var(--transition), box-shadow var(--transition), transform var(--transition);
}

.gr-group:hover{
    border-color:var(--border-strong) !important;
    box-shadow:0 8px 32px rgba(139,92,246,0.18);
    transform:translateY(-2px);
}

/* Accordion */
button.label-wrap, .accordion > .label-wrap{
    font-family:'Sora', sans-serif !important;
    font-weight:700 !important;
    color:var(--text-primary) !important;
}

/* ---------- Labels ---------- */
label span, .block > label > span{
    font-family:'Inter', sans-serif !important;
    font-weight:600 !important;
    color:var(--text-muted) !important;
    font-size:0.86rem !important;
    letter-spacing:0.01em;
}

/* ---------- Inputs ---------- */
textarea,
input[type="text"],
input[type="search"],
.gr-box, select{
    background:var(--bg-panel-soft) !important;
    border:1px solid var(--border-soft) !important;
    border-radius:var(--radius-md) !important;
    color:var(--text-primary) !important;
    font-size:15px !important;
    transition:border-color var(--transition), box-shadow var(--transition), background var(--transition) !important;
}

textarea:focus,
input[type="text"]:focus,
select:focus{
    border-color:var(--accent) !important;
    box-shadow:0 0 0 3px var(--accent-soft) !important;
    outline:none !important;
}

textarea::placeholder, input::placeholder{
    color:#7A7793 !important;
}

/* Dropdown menu items */
ul.options{
    background:#1A1B33 !important;
    border:1px solid var(--border-soft) !important;
    border-radius:var(--radius-md) !important;
    box-shadow:0 10px 30px rgba(0,0,0,0.4);
}
ul.options li.item:hover{
    background:var(--accent-soft) !important;
    color:var(--accent-3) !important;
}

/* ---------- File Upload ---------- */
.file-preview, [data-testid="file-upload"], .upload-box{
    background:var(--bg-panel-soft) !important;
    border:2px dashed var(--border-soft) !important;
    border-radius:var(--radius-lg) !important;
    transition:border-color var(--transition), background var(--transition), transform var(--transition) !important;
}

.upload-box:hover, [data-testid="file-upload"]:hover{
    border-color:var(--accent-3) !important;
    background:var(--accent-soft) !important;
    transform:scale(1.01);
}

.upload-box:hover svg, [data-testid="file-upload"]:hover svg{
    color:var(--accent-3) !important;
    transform:translateY(-3px) scale(1.05);
}

/* ---------- Buttons ---------- */
button{
    border-radius:var(--radius-md) !important;
    font-family:'Sora', sans-serif !important;
    font-weight:700 !important;
    transition:transform var(--transition), box-shadow var(--transition), background var(--transition), border-color var(--transition) !important;
}

button.primary, .gr-button-primary{
    background:var(--cta) !important;
    background-size:150% 150% !important;
    border:none !important;
    color:#FFFFFF !important;
    box-shadow:0 4px 20px rgba(139,92,246,0.4);
    position:relative;
    overflow:hidden;
}

button.primary:hover, .gr-button-primary:hover{
    background:var(--cta-hover) !important;
    transform:translateY(-3px) scale(1.02);
    box-shadow:0 10px 28px rgba(236,72,153,0.45);
}

button.primary:active{
    transform:translateY(-1px) scale(0.99);
}

button.secondary{
    background:var(--bg-panel-soft) !important;
    border:1px solid var(--border-soft) !important;
    color:var(--text-primary) !important;
}

button.secondary:hover{
    border-color:var(--accent-3) !important;
    color:var(--accent-3) !important;
    transform:translateY(-2px);
}

/* Example chips */
.gr-samples-table button, .gr-sample-textbox, .gallery-item, .example{
    background:var(--bg-panel) !important;
    border:1px solid var(--border-soft) !important;
    border-radius:99px !important;
    color:var(--text-muted) !important;
    font-family:'Inter', sans-serif !important;
    font-weight:500 !important;
    font-size:0.85rem !important;
    transition:all var(--transition) !important;
}

.gr-samples-table button:hover, .example:hover{
    border-color:var(--accent-3) !important;
    color:var(--accent-3) !important;
    background:var(--accent-soft) !important;
    transform:translateY(-2px) scale(1.03);
}

/* ---------- Output panels ---------- */
textarea[disabled], .disabled textarea{
    color:var(--text-primary) !important;
    -webkit-text-fill-color:var(--text-primary) !important;
    opacity:1 !important;
}

/* Markdown answer panel */
.prose, .markdown-body{
    color:var(--text-primary) !important;
    font-family:'Inter', sans-serif !important;
    line-height:1.7;
}

.prose h1, .prose h2, .prose h3{
    font-family:'Sora', sans-serif !important;
    color:var(--text-primary) !important;
}

.prose code{
    background:var(--bg-panel-soft) !important;
    color:var(--accent-3) !important;
    border-radius:6px;
    padding:2px 6px;
    font-family:'JetBrains Mono', monospace !important;
}

/* ---------- Tabs ---------- */
.tabs > .tab-nav{
    border-bottom:1px solid var(--border-soft) !important;
    gap:6px;
}
.tabs > .tab-nav button{
    color:var(--text-muted) !important;
    font-family:'Sora', sans-serif !important;
    font-weight:600 !important;
    border-radius:10px 10px 0 0 !important;
}
.tabs > .tab-nav button.selected{
    color:var(--accent-3) !important;
    background:var(--accent-soft) !important;
}

/* Status strip */
.status-strip{
    font-family:'JetBrains Mono', monospace;
    font-size:0.82rem;
    color:var(--accent-3);
    text-align:center;
    padding:6px 0;
}

/* Scrollbar polish */
::-webkit-scrollbar{ width:8px; height:8px; }
::-webkit-scrollbar-track{ background:transparent; }
::-webkit-scrollbar-thumb{ background:rgba(255,255,255,0.15); border-radius:99px; }
::-webkit-scrollbar-thumb:hover{ background:var(--accent-glow); }

/* Focus visibility for accessibility */
button:focus-visible, input:focus-visible, textarea:focus-visible{
    outline:2px solid var(--accent-3) !important;
    outline-offset:2px;
}

@media (prefers-reduced-motion: reduce){
    *{ transition:none !important; animation:none !important; }
}
"""

# ==========================================
# UI
# ==========================================

with gr.Blocks(

    title="ResearchMind AI",

    theme=gr.themes.Base(
        primary_hue="purple",
        secondary_hue="pink",
        neutral_hue="slate",
        radius_size="lg",
        font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
    ).set(
        body_background_fill="#0F1020",
        body_background_fill_dark="#0F1020",

        block_background_fill="rgba(255,255,255,0.06)",
        block_background_fill_dark="rgba(255,255,255,0.06)",
        block_border_color="rgba(255,255,255,0.10)",
        block_border_color_dark="rgba(255,255,255,0.10)",
        block_label_background_fill="rgba(255,255,255,0.06)",
        block_label_background_fill_dark="rgba(255,255,255,0.06)",
        block_label_text_color="#A9A6C4",
        block_label_text_color_dark="#A9A6C4",
        block_title_text_color="#F5F3FF",
        block_title_text_color_dark="#F5F3FF",

        body_text_color="#F5F3FF",
        body_text_color_dark="#F5F3FF",
        body_text_color_subdued="#A9A6C4",
        body_text_color_subdued_dark="#A9A6C4",

        border_color_primary="rgba(255,255,255,0.10)",
        border_color_primary_dark="rgba(255,255,255,0.10)",
        border_color_accent="#8B5CF6",
        border_color_accent_dark="#8B5CF6",

        input_background_fill="rgba(255,255,255,0.04)",
        input_background_fill_dark="rgba(255,255,255,0.04)",
        input_border_color="rgba(255,255,255,0.10)",
        input_border_color_dark="rgba(255,255,255,0.10)",
        input_border_color_focus="#8B5CF6",
        input_border_color_focus_dark="#8B5CF6",
        input_placeholder_color="#7A7793",
        input_placeholder_color_dark="#7A7793",

        button_primary_background_fill="#8B5CF6",
        button_primary_background_fill_dark="#8B5CF6",
        button_primary_background_fill_hover="#7C3AED",
        button_primary_background_fill_hover_dark="#7C3AED",
        button_primary_text_color="#FFFFFF",
        button_primary_text_color_dark="#FFFFFF",
        button_primary_border_color="transparent",
        button_primary_border_color_dark="transparent",

        button_secondary_background_fill="rgba(255,255,255,0.04)",
        button_secondary_background_fill_dark="rgba(255,255,255,0.04)",
        button_secondary_background_fill_hover="rgba(255,255,255,0.10)",
        button_secondary_background_fill_hover_dark="rgba(255,255,255,0.10)",
        button_secondary_text_color="#F5F3FF",
        button_secondary_text_color_dark="#F5F3FF",
        button_secondary_border_color="rgba(255,255,255,0.10)",
        button_secondary_border_color_dark="rgba(255,255,255,0.10)",

        color_accent="#8B5CF6",

        panel_background_fill="rgba(255,255,255,0.06)",
        panel_background_fill_dark="rgba(255,255,255,0.06)",
        panel_border_color="rgba(255,255,255,0.10)",
        panel_border_color_dark="rgba(255,255,255,0.10)",

        shadow_drop="0 4px 24px rgba(0,0,0,0.25)",
        shadow_drop_lg="0 8px 32px rgba(139,92,246,0.18)",
    ),

    css=css,

    js="""
    () => {
        document.documentElement.classList.remove('dark');
        const url = new URL(window.location.href);
        if (url.searchParams.get('__theme') !== 'dark') {
            url.searchParams.set('__theme', 'dark');
            window.history.replaceState(null, '', url);
        }
    }
    """

) as demo:

    gr.HTML("""
    <div class="aurora a1"></div>
    <div class="aurora a2"></div>
    <div class="aurora a3"></div>

    <div class="header-wrap">
    <h1>🤖 ResearchMind AI</h1>
    <div class="subtitle">Your Intelligent Research Assistant — upload, ask, understand.</div>
    <div class="rule"></div>
    <div class="badge-row">
        <span class="pill">⚡ Fast Analysis</span>
        <span class="pill">🧠 AI Powered</span>
        <span class="pill">📚 7 Study Modes</span>
    </div>
    <p class="powered-by">Powered by <b>Gemini 2.5 Flash</b> · Hugging Face · Gradio</p>
    </div>
    """)

    with gr.Row():

        # ================= LEFT PANEL =================

        with gr.Column(scale=1):

            with gr.Group():

                pdf = gr.File(
                    label="📂 Upload Research Document",
                    file_types=[".pdf"],
                )

                task = gr.Dropdown(
                    choices=[
                        "Ask Question",
                        "Summarize",
                        "Explain Like I'm 10",
                        "Generate Quiz",
                        "Generate Flashcards",
                        "Interview Questions",
                        "Executive Summary",
                    ],
                    value="Ask Question",
                    label="🎯 AI Task",
                )

                question = gr.Textbox(
                    label="💬 Your Question",
                    lines=4,
                    placeholder="Ask anything about the uploaded document...",
                    visible=True,
                )

                with gr.Row():
                    analyze = gr.Button("🚀 Analyze Document", variant="primary", scale=3)
                    clear_btn = gr.Button("🗑️ Clear", variant="secondary", scale=1)

            gr.Markdown(
                "💡 **Tip:** switch the *AI Task* dropdown to instantly change what "
                "ResearchMind generates — no need to retype your question every time.",
            )

        # ================= RIGHT PANEL =================

        with gr.Column(scale=2):

            with gr.Tabs():

                with gr.Tab("🤖 AI Response"):
                    answer = gr.Markdown(
                        value="### 👋 Upload a PDF to begin.\n\nOnce you upload a document and hit **Analyze**, your AI-generated response will appear here.",
                    )
                    copy_hint = gr.Markdown(
                        "_Select the text above and copy it — or export it manually._",
                        visible=False,
                    )

                with gr.Tab("📊 Hugging Face Insights"):
                    classification = gr.Textbox(
                        label="📂 Document Classification",
                        value="💤 Waiting for a document...",
                        interactive=False,
                    )

                    entities = gr.Textbox(
                        label="👥 Named Entities",
                        value="Upload a PDF to see extracted entities here.",
                        lines=10,
                        interactive=False,
                    )

    gr.Markdown("### ✨ Quick Prompts")

    gr.Examples(
        examples=[
            ["Summarize this document"],
            ["Who are the authors?"],
            ["Explain the conclusion"],
            ["Generate interview questions"],
            ["Generate flashcards"],
            ["Generate MCQs"],
        ],
        inputs=question,
        label="",
    )

    # ---------------- Interactivity wiring ----------------

    task.change(
        fn=toggle_question_box,
        inputs=task,
        outputs=question,
    )

    analyze.click(
        fn=research_assistant,
        inputs=[pdf, task, question],
        outputs=[classification, entities, answer, copy_hint],
    )

    clear_btn.click(
        fn=clear_all,
        inputs=None,
        outputs=[pdf, task, question, classification, entities, answer, copy_hint],
    )

demo.launch(
    share=True,
    debug=True,
)