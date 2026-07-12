"""
LearnMate – Personalized Course Pathway Generator
Powered by IBM Watsonx.ai (Granite) + Streamlit
"""

import os
import streamlit as st
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# ── Environment ──────────────────────────────────────────────────────────────
load_dotenv()

IBM_API_KEY    = os.getenv("IBM_API_KEY")
IBM_PROJECT_ID = os.getenv("IBM_PROJECT_ID")
IBM_URL        = os.getenv("IBM_URL", "https://au-syd.ml.cloud.ibm.com")

# ── Agent System Prompt ───────────────────────────────────────────────────────
AGENT_INSTRUCTIONS = """
You are LearnMate, a highly elite technical academic coach and curriculum architect
with deep expertise across software engineering, data science, AI/ML, cloud infrastructure,
cybersecurity, UX design, and product management.

Your mission is to produce a hyper-personalised, actionable learning roadmap for the student.

CROSS-REFERENCE RULES:
- Carefully analyse the student's existing skills against the target career requirements.
- Identify skill gaps and prioritise bridging them in the earliest months.
- Never recommend topics the student already masters; instead build on them.
- Calibrate depth and pacing strictly to the stated skill level (Beginner / Intermediate / Advanced).
- Respect the weekly learning hours — do not over-load or under-load the student.

OUTPUT FORMAT — strictly follow this Markdown structure, no deviations:

## 🎯 Career Target: <career>
## 📊 Skill Gap Analysis
<bullet list of gaps identified vs existing skills>

## 🗓️ Month-by-Month Learning Roadmap
### Month 1 – <theme>
- **Core Topics:** <list>
- **Resources:** <specific books / free courses / docs>
- **Project Milestone:** <concrete mini-project>
- **Evaluation Metric:** <how to measure completion>

### Month 2 – <theme>
... (continue for 4–6 months based on skill level)

## 🔑 Recommended Core Technologies & Tools
<categorised bullet list>

## 🏗️ Capstone Project Ideas
<2–3 substantial project ideas with brief descriptions>

## 📈 Progress Evaluation Framework
- **Weekly Check-in:** <self-assessment method>
- **Monthly Milestone Gate:** <criteria to advance>
- **Final Competency Benchmark:** <industry-standard measure>

## 💡 Pro Tips from Your Coach
<3–5 motivational and tactical tips specific to this career path>

Be thorough, specific, and actionable. Avoid generic advice. Every recommendation must be
directly tied to the student's stated background, target career, and available weekly hours.
"""

# ── Watsonx Client ────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_model() -> ModelInference:
    credentials = Credentials(url=IBM_URL, api_key=IBM_API_KEY)
    client = APIClient(credentials=credentials, project_id=IBM_PROJECT_ID)
    model = ModelInference(
        model_id="ibm/granite-8b-code-instruct",
        api_client=client,
        params={
            GenParams.MAX_NEW_TOKENS: 3000,
            GenParams.TEMPERATURE:    0.7,
            GenParams.TOP_P:          0.95,
            GenParams.REPETITION_PENALTY: 1.1,
        },
    )
    return model


def build_user_prompt(career: str, level: str, skills: str, hours: int) -> str:
    return (
        f"Student Profile:\n"
        f"- Target Career: {career}\n"
        f"- Current Skill Level: {level}\n"
        f"- Existing Technical Skills: {skills if skills.strip() else 'None provided'}\n"
        f"- Weekly Learning Availability: {hours} hours/week\n\n"
        f"Generate my complete personalised learning roadmap following your structured format exactly."
    )


def generate_roadmap(career, level, skills, hours):
    model = get_model()
    messages = [
        {"role": "system", "content": AGENT_INSTRUCTIONS},
        {"role": "user",   "content": build_user_prompt(career, level, skills, hours)},
    ]
    response = model.chat(messages=messages)
    return response["choices"][0]["message"]["content"]


# ── Streamlit UI ──────────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="LearnMate – Course Pathway Generator",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # ── Custom CSS (minimal, inline) ─────────────────────────────────────────
    st.markdown(
        """
        <style>
            /* Sidebar label weight */
            [data-testid="stSidebar"] label { font-weight: 600; }

            /* Hero banner */
            .hero-banner {
                background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
                border-radius: 12px;
                padding: 2rem 2.5rem;
                color: white;
                margin-bottom: 1.5rem;
            }
            .hero-banner h1 { margin: 0; font-size: 2.2rem; font-weight: 800; }
            .hero-banner p  { margin: 0.4rem 0 0; font-size: 1.05rem; opacity: 0.88; }

            /* Roadmap card */
            .roadmap-card {
                background: #f8faff;
                border: 1px solid #d1deff;
                border-left: 5px solid #2563eb;
                border-radius: 10px;
                padding: 1.8rem 2rem;
                margin-top: 1rem;
            }

            /* Footer */
            .footer {
                text-align: center;
                font-size: 0.78rem;
                color: #6b7280;
                margin-top: 3rem;
                padding-top: 0.8rem;
                border-top: 1px solid #e5e7eb;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ── Hero Banner ──────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="hero-banner">
            <h1>🎓 LearnMate</h1>
            <p>Your AI-powered Personalized Course Pathway Generator &mdash; built on IBM Watsonx.ai &amp; Granite</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Sidebar Inputs ───────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(
        "![IBM Watsonx](https://img.shields.io/badge/Powered%20by-IBM%20Watsonx.ai-0F62FE?style=for-the-badge)", 
        unsafe_allow_html=True)
        st.title("🛠️ Configure Your Path")
        st.markdown("---")

        career = st.selectbox(
            "🎯 Target Career",
            options=[
                "AI Engineer / LLM Developer",
                "Data Scientist & Analyst",
                "Computer Vision Engineer",
                "Frontend Web Developer",
                "Backend Systems Engineer",
                "Full-Stack Developer",
                "UI/UX Product Designer",
                "Product Manager (Tech)",
                "Data Visualization Expert",
                "Cybersecurity Analyst",
                "Cloud & DevOps Engineer",
                "IoT & Smart Systems Engineer",
            ],
            help="Select the career role you are aiming for.",
        )

        level = st.selectbox(
            "📶 Current Skill Level",
            options=["Beginner", "Intermediate", "Advanced"],
            help="Honest self-assessment gives the best roadmap.",
        )

        skills = st.text_input(
            "🧰 Existing Technical Skills",
            placeholder="e.g. Python, SQL, React, Docker",
            help="Comma-separate the tools, languages, or frameworks you already know.",
        )

        hours = st.slider(
            "⏱️ Weekly Learning Goal (hours)",
            min_value=2,
            max_value=20,
            value=8,
            step=1,
            help="How many hours per week can you dedicate to learning?",
        )

        st.markdown("---")
        generate_btn = st.button(
            "🚀 Generate My Roadmap",
            use_container_width=True,
            type="primary",
        )

        st.markdown(
            """
            <div style='font-size:0.78rem;color:#6b7280;margin-top:1rem;'>
            Powered by <strong>IBM Watsonx.ai</strong><br>
            Model: <code>granite-8b-code-instruct</code>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Main Panel ───────────────────────────────────────────────────────────
    if not generate_btn:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("**Step 1** – Select your target career from the sidebar dropdown.")
        with col2:
            st.info("**Step 2** – Fill in your skill level, existing skills, and weekly hours.")
        with col3:
            st.info("**Step 3** – Click **Generate My Roadmap** to get your personalised plan.")

        st.markdown("---")
        st.markdown(
            """
            ### What LearnMate provides:
            | Section | Description |
            |---|---|
            | 📊 Skill Gap Analysis | Identifies what you need to learn vs. what you know |
            | 🗓️ Month-by-Month Roadmap | Phased curriculum with topics, resources & projects |
            | 🔑 Core Technologies | Categorised tools & frameworks for your target role |
            | 🏗️ Capstone Project Ideas | Real-world portfolio-worthy project suggestions |
            | 📈 Evaluation Framework | Milestones and benchmarks to track your progress |
            | 💡 Pro Coach Tips | Tactical advice tailored to your specific career path |
            """
        )
    else:
        # Validate env vars before calling API
        if not IBM_API_KEY or not IBM_PROJECT_ID:
            st.error(
                "⚠️ **Configuration Error** — `IBM_API_KEY` or `IBM_PROJECT_ID` is missing. "
                "Please check your `.env` file and restart the app."
            )
            st.stop()

        with st.spinner("🤖 LearnMate is crafting your personalised roadmap via IBM Watsonx.ai…"):
            try:
                roadmap_md = generate_roadmap(career, level, skills, hours)
            except Exception as exc:
                st.error(f"❌ Watsonx.ai API error: {exc}")
                st.stop()

        # ── Summary ribbon ───────────────────────────────────────────────────
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🎯 Career Target", career.split("/")[0].strip())
        c2.metric("📶 Skill Level", level)
        c3.metric("⏱️ Weekly Hours", f"{hours} hrs")
        c4.metric("🧰 Skills Entered", str(len([s for s in skills.split(",") if s.strip()])) if skills.strip() else "0")

        st.markdown("---")

        # ── Roadmap output ───────────────────────────────────────────────────
        st.markdown(roadmap_md)

        # ── Download button ──────────────────────────────────────────────────
        st.download_button(
            label="⬇️  Download Roadmap as Markdown",
            data=roadmap_md,
            file_name=f"learnmate_roadmap_{career.replace(' ', '_').replace('/', '-')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    # ── Footer ───────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="footer">LearnMate &nbsp;|&nbsp; Built with IBM Watsonx.ai &amp; Granite &nbsp;|&nbsp; Streamlit</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
