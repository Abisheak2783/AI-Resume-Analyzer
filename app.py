import streamlit as st
from utils import extract_text_from_pdf , analyze_resume , compare_resume_job , generate_interview_questions , evaluate_answer , career_advisor , improve_resume , rewrite_resume, semantic_resume_match, generate_professional_resume,generate_resume_docx,generate_resume_pdf,keyword_optimizer, calculate_ats_score
from pdf_generator import generate_pdf_report
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Global Font & Smooth Antialiasing */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    -webkit-font-smoothing: antialiased;
}

/* Main App Container */
.stApp {
    background: #F8FAFC;
    color: #1E293B;
}

/* Sidebar Gradient Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
    border-right: 1px solid #334155;
}

/* Sidebar Text & Branding */
[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

/* Sidebar Radio Options Styling */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    font-size: 0.95rem;
    font-weight: 500;
}

/* Buttons Styling */
.stButton > button {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    color: #FFFFFF !important;
    border-radius: 10px;
    border: none;
    padding: 10px 22px;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.2px;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
    transform: translateY(-1px);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Input Fields & Text Areas */
.stTextInput input, .stTextArea textarea {
    border-radius: 10px !important;
    border: 1px solid #CBD5E1 !important;
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    font-size: 0.95rem !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
}

/* File Uploader Styling */
[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border: 2px dashed #CBD5E1;
    border-radius: 12px;
    padding: 15px;
    transition: border-color 0.2s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #2563EB;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 18px 20px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.07);
}

[data-testid="stMetricValue"] {
    font-weight: 800 !important;
    color: #0F172A !important;
}

[data-testid="stMetricLabel"] {
    font-weight: 600 !important;
    color: #64748B !important;
}

/* Headers */
h1 {
    font-weight: 800 !important;
    color: #0F172A !important;
    letter-spacing: -0.5px;
}

h2, h3 {
    font-weight: 700 !important;
    color: #1E293B !important;
    letter-spacing: -0.3px;
}

/* Divider Styling */
hr {
    border-color: #E2E8F0 !important;
    margin: 1.5rem 0 !important;
}

/* Section Wise ATS Score Cards */
.ats-section-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 16px;
    margin-top: 15px;
    margin-bottom: 20px;
}
.ats-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    border: 1px solid #E2E8F0;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.ats-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}
.ats-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}
.ats-card-title {
    font-weight: 600;
    font-size: 0.95rem;
    color: #1E293B;
    display: flex;
    align-items: center;
    gap: 8px;
}
.ats-score-pill {
    font-weight: 700;
    font-size: 0.85rem;
    padding: 4px 10px;
    border-radius: 20px;
}
.pill-high { background-color: #DEF7EC; color: #03543F; }
.pill-medium { background-color: #FEF08A; color: #713F12; }
.pill-low { background-color: #FDE8E8; color: #9B1C1C; }

.ats-progress-track {
    background-color: #F1F5F9;
    border-radius: 8px;
    height: 10px;
    width: 100%;
    overflow: hidden;
}
.ats-progress-bar {
    height: 100%;
    border-radius: 8px;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
.bar-high { background: linear-gradient(90deg, #10B981, #059669); }
.bar-medium { background: linear-gradient(90deg, #F59E0B, #D97706); }
.bar-low { background: linear-gradient(90deg, #EF4444, #DC2626); }

/* ATS Improvement Suggestions */
.ats-suggestion-card {
    background-color: #FEFCE8;
    border-left: 4px solid #EAB308;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}
.ats-suggestion-text {
    color: #854D0E;
    font-weight: 500;
    font-size: 0.95rem;
}
.ats-success-card {
    background-color: #F0FDF4;
    border-left: 4px solid #22C55E;
    border-radius: 8px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    color: #166534;
    font-weight: 600;
    font-size: 1rem;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

/* Skill Chips */
.skill-chips-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
    margin-bottom: 20px;
}
.chip-matched {
    background-color: #DEF7EC;
    color: #03543F;
    border: 1px solid #84E1BC;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.88rem;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.chip-missing {
    background-color: #FDE8E8;
    color: #9B1C1C;
    border: 1px solid #F8B4B4;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.88rem;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

/* Resume Rewriter Split View */
.diff-header-orig {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
    margin-bottom: 12px;
    border-bottom: 2px solid #94A3B8;
}
.diff-header-ai {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
    margin-bottom: 12px;
    border-bottom: 2px solid #10B981;
}
.diff-title {
    font-weight: 700;
    font-size: 1.05rem;
    color: #1E293B;
}
.badge-orig {
    background: #F1F5F9;
    color: #475569;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 12px;
}
.badge-ai {
    background: #DEF7EC;
    color: #03543F;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 12px;
}

/* Resume Builder Templates & Preview */
.template-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin-bottom: 25px;
}
.template-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}
.template-icon {
    font-size: 2rem;
    margin-bottom: 8px;
}
.template-title {
    font-weight: 700;
    color: #1E293B;
    font-size: 1rem;
    margin-bottom: 4px;
}
.template-desc {
    font-size: 0.82rem;
    color: #64748B;
}
.resume-paper-container {
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: 30px 35px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
    border: 1px solid #E2E8F0;
    margin-top: 20px;
    margin-bottom: 30px;
    color: #1E293B;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)
#sidebar
with st.sidebar:

    st.title("🤖 AI Resume Analyzer")

    st.markdown("---")

    st.subheader("Navigation")

    menu = st.radio(

        "",

        [

            "🏠 Dashboard",

            "📄 Resume Analysis",

            "📊 ATS Score",

            "🎯 Resume Matching",

            "🧠 Interview Coach",

            "💼 Career Advisor",

            "✍ Resume Rewriter",

            "🏆 Resume Builder",

            "📥 Reports",

            "⚙ Settings"

        ]

    )

    st.markdown("---")

    st.info("Version 2.0")

if menu == "🏠 Dashboard":

    st.title("🏠 Dashboard")

    st.success("Welcome to AI Resume Analyzer")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        ats_score = st.session_state.get("ats_score", 0)

        st.metric(
            "ATS Score",
            f"{ats_score}%"
        )

    with col2:
        match_score = st.session_state.get("match_score", 0)
        st.metric(
            "Resume Match",
            f"{match_score}%"
        )
     
    with col3:
        missing_skills = st.session_state.get("missing_skills", [])

        st.metric(
            "Missing Skills",
            len(missing_skills)
        )

    with col4:
        ats_score = st.session_state.get("ats_score", 0)

        if ats_score >= 90:
            status = "Excellent"
        elif ats_score >= 75:
            status = "Good"
        elif ats_score >= 60:
            status = "Average"
        else:
            status = "Needs Improvement"

        st.metric("Status", status)
    st.markdown("---")

    # ---------------- Dashboard Overview ---------------- #
    st.subheader("📊 Dashboard Overview")
    st.info("""
This dashboard gives a quick overview of your resume performance.

You can use the sidebar to access:

• 📄 Resume Analysis

• 💡 ATS Score

• 🎯 Resume Matching

• 🧠 Interview Coach

• 💼 Career Advisor

• 📥 Reports
""")

elif menu == "📄 Resume Analysis":
 st.title("📄 AI RESUME ANALYZER")
 st.subheader("Analyze Your Resume Using AI")
 uf=st.file_uploader("Upload Your Resume(pdf only)",type=["pdf"])
 st.markdown("""Resume Summary ,Technical skills , soft skills ,ATS score""")
 if uf is not None:
    resume_text = extract_text_from_pdf(uf)
    #save in session
    st.session_state["resume_text"]= resume_text
    st.session_state["uploaded_filename"] = uf.name
    st.session_state["uploaded_filetype"] = uf.type
 if "resume_text" in st.session_state:
    resume_text = st.session_state["resume_text"]
    st.success("Resume Uploaded Successfully")

    st.write("uploaded file details")
    st.write(f"File Name: {st.session_state['uploaded_filename']}")
    st.write(f"File Type: {st.session_state['uploaded_filetype']}")

    st.subheader("📄 Extracted Resume Text")

    st.text_area(
    "Resume Content",
    resume_text,
    height=350
    )   

    #Job Description
    st.subheader("📄 Job Description")
    job_description = st.text_area(
    "Paste Job Description Here",
       height=250
    )

    #Analyze Resume Button
    if st.button("🚀 Analyze Resume"):
        with st.spinner("Analyzing Resume... Please Wait..."):
            analysis=analyze_resume(resume_text)
            st.session_state["analysis"] = analysis
        st.success("Resume Analysis Completed")
    if "analysis" in st.session_state:
        st.subheader("AI Resume Analysis")
        st.markdown(
            st.session_state["analysis"]
        )

        #ats score calculation
# ATS Score Dashboard
elif menu == "📊 ATS Score":

    st.title("📊 ATS Score Dashboard")

    if "resume_text" not in st.session_state:

        st.warning("⚠ Please upload your resume first from Resume Analysis.")

    else:

        resume_text = st.session_state["resume_text"]

        total_score, section_scores, suggestions = calculate_ats_score(
            resume_text
        )

        st.session_state["ats_score"]= total_score

        st.metric(
            "Overall ATS Score",
            f"{total_score}%"
        )

        st.progress(total_score / 100)

        if total_score >= 90:

            st.success("🌟 Excellent Resume")

        elif total_score >= 75:

            st.info("👍 Good Resume")

        elif total_score >= 60:

            st.warning("⚠ Needs Improvement")

        else:

            st.error("❌ Poor ATS Score")

        st.markdown("---")

        st.subheader("📋 Section Wise ATS Score")

        # Section Wise ATS Score cards

        icons = {
            "Contact Information": "📇",
            "Skills": "⚡",
            "Projects": "🚀",
            "Education": "🎓",
            "Experience": "💼",
            "Formatting": "🎨"
        }

        cards_html = ['<div class="ats-section-grid">']
        for section, value in section_scores.items():
            max_val = 10 if section in ["Education", "Formatting", "Contact Information"] else 20
            pct = int((value / max_val) * 100)
            icon = icons.get(section, "📌")

            if pct >= 80:
                pill_cls, bar_cls = "pill-high", "bar-high"
            elif pct >= 60:
                pill_cls, bar_cls = "pill-medium", "bar-medium"
            else:
                pill_cls, bar_cls = "pill-low", "bar-low"

            card = f'<div class="ats-card"><div class="ats-card-header"><span class="ats-card-title">{icon} {section}</span><span class="ats-score-pill {pill_cls}">{value}/{max_val} ({pct}%)</span></div><div class="ats-progress-track"><div class="ats-progress-bar {bar_cls}" style="width: {pct}%;"></div></div></div>'
            cards_html.append(card)

        cards_html.append('</div>')
        st.markdown("".join(cards_html), unsafe_allow_html=True)

        st.markdown("---")

        st.subheader("💡 ATS Improvement Suggestions")

        # ATS Improvement Suggestions

        if suggestions:
            sug_html = []
            for item in suggestions:
                sug_html.append(f'<div class="ats-suggestion-card"><span>💡</span><span class="ats-suggestion-text">{item}</span></div>')
            st.markdown("".join(sug_html), unsafe_allow_html=True)
        else:
            st.markdown("""<div class="ats-success-card"><span>🎉</span><span>Your Resume is fully ATS friendly! No additional changes needed.</span></div>""", unsafe_allow_html=True)
#Compare Resume with Job Description
elif menu == "🎯 Resume Matching":
    st.title("🎯 Resume Matching & Alignment")
    st.write("Compare your resume against a job description to identify skill alignment and semantic match.")

    if "resume_text" not in st.session_state:
        st.warning("⚠ Please upload your resume first from Resume Analysis.")

    else:
        resume_text = st.session_state["resume_text"]

        # Resume Matching & Skill Chips

        job_description = st.text_area(
            "📄 Paste Job Description Here",
            height=220
        )

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            run_keyword_match = st.button("📊 Compare Skill Match", use_container_width=True)

        with col_btn2:
            run_semantic_match = st.button("🧠 Calculate Semantic AI Match", use_container_width=True)

        if run_keyword_match:
            if not job_description.strip():
                st.warning("Please enter a Job Description.")
            else:
                score, matched, missing = compare_resume_job(
                    resume_text,
                    job_description
                )
                st.session_state["match_score"] = score
                st.session_state["matched_skills"] = matched
                st.session_state["missing_skills"] = missing

        if run_semantic_match:
            if not job_description.strip():
                st.warning("Please enter a Job Description.")
            else:
                with st.spinner("Calculating Semantic Match..."):
                    semantic_score = semantic_resume_match(
                        resume_text,
                        job_description
                    )
                    st.session_state["semantic_score"] = float(semantic_score)

        # ---------------- Display Results ---------------- #
        if "match_score" in st.session_state or "semantic_score" in st.session_state:
            st.markdown("---")

            col_m1, col_m2 = st.columns(2)

            with col_m1:
                if "match_score" in st.session_state:
                    score = st.session_state["match_score"]
                    st.metric("Skill Match Score", f"{score}%")
                    st.progress(score / 100)

            with col_m2:
                if "semantic_score" in st.session_state:
                    sem_score = st.session_state["semantic_score"]
                    st.metric("Semantic AI Match", f"{sem_score}%")
                    st.progress(sem_score / 100)

            if "matched_skills" in st.session_state:
                matched = st.session_state.get("matched_skills", [])
                missing = st.session_state.get("missing_skills", [])

                st.subheader("✅ Matched Skills")
                if matched:
                    chips_matched = ['<div class="skill-chips-container">']
                    for skill in matched:
                        chips_matched.append(f'<span class="chip-matched">✓ {skill.title()}</span>')
                    chips_matched.append('</div>')
                    st.markdown("".join(chips_matched), unsafe_allow_html=True)
                else:
                    st.info("No direct skill matches detected.")

                st.subheader("❌ Missing Skills")
                if missing:
                    chips_missing = ['<div class="skill-chips-container">']
                    for skill in missing:
                        chips_missing.append(f'<span class="chip-missing">✗ {skill.title()}</span>')
                    chips_missing.append('</div>')
                    st.markdown("".join(chips_missing), unsafe_allow_html=True)
                else:
                    st.success("🎉 Outstanding! No missing required skills found.")

#AI interview coach
elif menu == "🧠 Interview Coach":
 st.markdown("---")
 st.title("AI Interview Coach")
 if "resume_text" not in st.session_state:
     st.warning("⚠ Please upload your resume first from Resume Analysis.")
 else:
    resume_text = st.session_state["resume_text"]
    st.subheader("🎤 AI Interview Questions")
    if st.button("Generate Interview question"):
        with st.spinner("Generating Interview Questions..."):
          questions = generate_interview_questions(
                    resume_text,
                )
          st.session_state["questions"]=questions
    if "questions" in st.session_state:
          st.markdown(st.session_state["questions"])

    st.markdown("---")
    st.subheader("📝 Practice Your Answer")      
    question = st.text_area(
    "Interview Question",
    height=120
    )
    answer = st.text_area(
      "Your Answer",
       height=250
    )
    if st.button("✅ Evaluate My Answer"):

      if question.strip() == "" or answer.strip() == "":
        st.warning("Please enter both the question and your answer.")

      else:

        with st.spinner("Evaluating your answer..."):

            feedback = evaluate_answer(
                question,
                answer
            )

        st.subheader("🤖 AI Feedback")

        st.markdown(feedback)


# ai career advisor
elif menu == "💼 Career Advisor":
 st.title("🎯 AI Career Advisor")
 st.write("Get personalized AI career guidance based on your resume.")

 if "resume_text" not in st.session_state:
    st.warning("⚠ Please upload your resume first from Resume Analysis.")

 else:
    resume_text = st.session_state["resume_text"]

    if st.button("🚀 Generate Career Advice"):

     with st.spinner("Generating Career Guidance..."):

        advice = career_advisor(resume_text)
        st.session_state["career_advice"] = advice

    if "career_advice" in st.session_state:
        st.success("✅ Career Advice Generated Successfully!")
        st.subheader("🤖 AI Career Report")
        st.markdown(
            st.session_state["career_advice"]
        )
#Resume Improvement Section
elif menu == "📝 Resume Improvement":

    st.title("📝 AI Resume Improvement System")

    if "resume_text" not in st.session_state:
        st.warning("⚠ Please upload your resume first from Resume Analysis.")

    else:

        resume_text = st.session_state["resume_text"]

        if st.button("🚀 Improve My Resume"):

            with st.spinner("Analyzing Resume Improvements..."):

                report = improve_resume(resume_text)

                st.session_state["resume_improvement"] = report

            st.success("✅ Resume Improvement Completed!")

        if "resume_improvement" in st.session_state:

            st.subheader("🤖 AI Resume Improvement Report")

            st.markdown(st.session_state["resume_improvement"])

#Resume Rewriter
elif menu == "✍ Resume Rewriter":

    st.title("✍ AI Resume Rewriter & Split View")
    st.write("Transform your resume into a high-impact, ATS-optimized version with side-by-side comparison.")

    if "resume_text" not in st.session_state:

        st.warning("⚠ Please upload your resume first from Resume Analysis.")

    else:

        resume_text = st.session_state["resume_text"]

        # Split-Screen Diff View

        if st.button("🚀 Rewrite & Enhance Resume", use_container_width=True):

            with st.spinner("Analyzing and Rewriting Resume using AI..."):

                rewritten_resume = rewrite_resume(resume_text)

                st.session_state["rewritten_resume"] = rewritten_resume

            st.success("✅ Resume Rewritten & Enhanced Successfully!")

        if "rewritten_resume" in st.session_state:

            st.markdown("---")
            st.subheader("⚡ Split-Screen Comparison")

            orig_words = len(resume_text.split())
            new_words = len(st.session_state["rewritten_resume"].split())

            m_col1, m_col2, m_col3 = st.columns(3)

            with m_col1:
                st.metric("Original Word Count", orig_words)
            with m_col2:
                st.metric("AI Enhanced Word Count", new_words, delta=f"{new_words - orig_words} words")
            with m_col3:
                st.metric("ATS Optimization Level", "High (ATS-Ready)", delta="Enhanced")

            col_orig, col_ai = st.columns(2)

            with col_orig:
                st.markdown("""<div class="diff-header-orig"><span class="diff-title">📄 Original Resume</span><span class="badge-orig">RAW TEXT</span></div>""", unsafe_allow_html=True)
                st.text_area(
                    "Original Resume Content",
                    resume_text,
                    height=500,
                    key="orig_resume_view"
                )

            with col_ai:
                st.markdown("""<div class="diff-header-ai"><span class="diff-title">✨ AI Enhanced Resume</span><span class="badge-ai">ATS OPTIMIZED</span></div>""", unsafe_allow_html=True)
                st.text_area(
                    "Rewritten Resume Content",
                    st.session_state["rewritten_resume"],
                    height=500,
                    key="ai_resume_view"
                )
# Download Report
elif menu == "📥 Reports":

    st.markdown("---")
    st.title("📥 Reports")
    st.write("Download your AI-generated reports and professional resume.")

    # ---------------- PDF Report ---------------- #
    st.subheader("📄 AI Resume Report")

    if st.button("Generate PDF Report"):

        generate_pdf_report(

            filename="Resume_Report.pdf",

            resume_analysis=st.session_state.get(
                "analysis",
                "Not Available"
            ),

            career_advice=st.session_state.get(
                "career_advice",
                "Not Available"
            ),

            resume_improvement=st.session_state.get(
                "resume_improvement",
                "Not Available"
            ),

            rewritten_resume=st.session_state.get(
                "rewritten_resume",
                "Not Available"
            )

        )

        st.success("✅ PDF Report Generated Successfully!")

    try:

        with open("Resume_Report.pdf", "rb") as pdf_file:

            st.download_button(

                label="📄 Download PDF Report",

                data=pdf_file,

                file_name="AI_Resume_Report.pdf",

                mime="application/pdf"

            )

    except FileNotFoundError:

        pass

    # ---------------- Professional Resume ---------------- #

    if "professional_resume" in st.session_state:

        st.subheader("🏆 Professional Resume Downloads")

        docx_file = generate_resume_docx(
            st.session_state["professional_resume"]
        )

        with open(docx_file, "rb") as file:

            st.download_button(

                "📄 Download DOCX Resume",

                file,

                file_name="Professional_Resume.docx",

                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"

            )

        pdf_file = generate_resume_pdf(
            st.session_state["professional_resume"]
        )

        with open(pdf_file, "rb") as file:

            st.download_button(

                "📑 Download PDF Resume",

                file,

                file_name="Professional_Resume.pdf",

                mime="application/pdf"

            )

    else:

        st.info("Generate a Professional Resume first.")

# Professional Resume Builder
elif menu == "🏆 Resume Builder":

    st.title("🏆 Professional Resume Builder")
    st.write("Craft an executive, ATS-optimized professional resume in seconds.")

    if "resume_text" not in st.session_state:

        st.warning("⚠ Please upload your resume first from Resume Analysis.")

    else:

        resume_text = st.session_state["resume_text"]

        # Resume Builder Templates & Preview

        # ---------------- Template Overview Cards ---------------- #
        st.markdown("""<div class="template-grid">
<div class="template-card">
    <div class="template-icon">📄</div>
    <div class="template-title">ATS Friendly</div>
    <div class="template-desc">Simple, 100% scanner readable linear layout.</div>
</div>
<div class="template-card">
    <div class="template-icon">🎨</div>
    <div class="template-title">Modern</div>
    <div class="template-desc">Attractive formatting with clear section highlights.</div>
</div>
<div class="template-card">
    <div class="template-icon">💼</div>
    <div class="template-title">Corporate</div>
    <div class="template-desc">Formal executive business layout for senior roles.</div>
</div>
<div class="template-card">
    <div class="template-icon">⚡</div>
    <div class="template-title">Minimal</div>
    <div class="template-desc">Ultra-clean, concise focus on key impact points.</div>
</div>
</div>""", unsafe_allow_html=True)

        col_tmpl, col_color = st.columns([2, 1])

        with col_tmpl:
            template = st.selectbox(
                "Choose Resume Template",
                [
                    "ATS Friendly",
                    "Modern",
                    "Corporate",
                    "Minimal"
                ]
            )

        with col_color:
            color_accent = st.selectbox(
                "Header Accent Color",
                [
                    "Executive Blue",
                    "Emerald Green",
                    "Classic Charcoal",
                    "Royal Purple"
                ]
            )

        # ---------------- Generate Resume ---------------- #
        if st.button("🚀 Generate Professional Resume"):

            with st.spinner("Generating Professional Resume..."):

                professional_resume = generate_professional_resume(
                    resume_text,
                    template
                )

                st.session_state["professional_resume"] = professional_resume
                st.session_state["resume_accent"] = color_accent

            st.success("✅ Professional Resume Generated Successfully!")

        # ---------------- Display & Export Resume ---------------- #
        if "professional_resume" in st.session_state:

            st.markdown("---")
            st.subheader("📄 Generated Professional Resume")

            accent_colors = {
                "Classic Charcoal": "#1E293B",
                "Executive Blue": "#2563EB",
                "Emerald Green": "#059669",
                "Royal Purple": "#7C3AED"
            }
            border_color = accent_colors.get(st.session_state.get("resume_accent", "Executive Blue"), "#2563EB")

            # Paper-like preview container
            st.markdown(f"""<div class="resume-paper-container" style="border-top: 6px solid {border_color};">
<div>{st.session_state['professional_resume'].replace('\n', '<br>')}</div>
</div>""", unsafe_allow_html=True)

            st.subheader("📥 Download Resume Formats")

            col_docx, col_pdf = st.columns(2)

            with col_docx:
                docx_file = generate_resume_docx(
                    st.session_state["professional_resume"]
                )

                with open(docx_file, "rb") as file:
                    st.download_button(
                        label="📄 Download Resume (.docx)",
                        data=file,
                        file_name=f"Professional_Resume_{template.replace(' ', '_')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )

            with col_pdf:
                pdf_file = generate_resume_pdf(
                    st.session_state["professional_resume"]
                )

                with open(pdf_file, "rb") as file:
                    st.download_button(
                        label="📑 Download Resume (.pdf)",
                        data=file,
                        file_name=f"Professional_Resume_{template.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
     

# Resume Keyword Optimizer
elif menu == "🎯 Keyword Optimizer":

    st.title("🎯 Resume Keyword Optimizer")

    if "resume_text" not in st.session_state:

        st.warning("⚠ Please upload your resume first from Resume Analysis.")

    else:

        resume_text = st.session_state["resume_text"]

        st.subheader("📄 Job Description")

        job_description = st.text_area(
            "Paste Job Description Here",
            height=250
        )

        if st.button("🚀 Optimize Resume Keywords"):

            if not job_description.strip():

                st.warning("Please enter a Job Description.")

            else:

                with st.spinner("Optimizing Resume..."):

                    keyword_result = keyword_optimizer(
                        resume_text,
                        job_description
                    )

                    st.session_state["keyword_result"] = keyword_result

                st.success("✅ Keyword Analysis Completed!")

        if "keyword_result" in st.session_state:

            st.subheader("📋 Keyword Optimization Report")

            st.markdown(
                st.session_state["keyword_result"]
            )
#settings
elif menu == "⚙ Settings":

    st.title("⚙ Settings")

    st.write("Customize your AI Resume Analyzer.")

    st.markdown("---")

    st.subheader("Theme")

    theme = st.selectbox(
        "Select Theme",
        [
            "Light",
            "Dark"
        ]
    )

    st.subheader("AI Model")

    model = st.selectbox(
        "Choose AI Model",
        [
            "Gemini 2.5 Flash",
            "Gemini 2.5 Pro"
        ]
    )

    st.subheader("Report Format")

    report = st.multiselect(
        "Include in Report",
        [
            "Resume Analysis",
            "ATS Score",
            "Resume Matching",
            "Career Advice",
            "Interview Questions"
        ],
        default=[
            "Resume Analysis",
            "ATS Score"
        ]
    )

    st.markdown("---")

    if st.button("💾 Save Settings"):

        st.success("Settings Saved Successfully.")