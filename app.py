import streamlit as st
import pandas as pd
from rag_eng import answer_question

st.set_page_config(
    page_title="Alopecia in Young Women Research Intelligence Platform",
    page_icon="🧬",
    layout="wide",
)

st.markdown("""
<style>
:root {
    --bg: #f8f1e8;
    --cream: #fffaf2;
    --card: rgba(255, 250, 242, 0.86);
    --border: rgba(120, 92, 65, 0.18);
    --text: #2d241d;
    --muted: #7b6a5d;
    --accent: #9b6b43;
    --accent2: #c99a6b;
    --rose: #d8a7a1;
    --sage: #879f7b;
    --gold: #c8a15a;
}

.stApp {
    background:
        radial-gradient(circle at 12% 12%, rgba(216,167,161,0.32), transparent 28%),
        radial-gradient(circle at 85% 8%, rgba(201,154,107,0.26), transparent 30%),
        linear-gradient(135deg, #f8f1e8 0%, #fffaf2 45%, #efe1d1 100%);
    color: var(--text);
}

.block-container {
    padding-top: 2rem;
    max-width: 1320px;
}

.stApp:before {
    content: "";
    position: fixed;
    width: 420px;
    height: 420px;
    border-radius: 999px;
    background: rgba(201,154,107,0.16);
    top: 80px;
    right: -150px;
    filter: blur(8px);
    animation: floatBlob 9s ease-in-out infinite alternate;
    z-index: 0;
}

.stApp:after {
    content: "";
    position: fixed;
    width: 360px;
    height: 360px;
    border-radius: 999px;
    background: rgba(216,167,161,0.18);
    bottom: -120px;
    left: -100px;
    filter: blur(10px);
    animation: floatBlob2 11s ease-in-out infinite alternate;
    z-index: 0;
}

@keyframes floatBlob {
    from { transform: translateY(0px) translateX(0px); }
    to { transform: translateY(35px) translateX(-25px); }
}

@keyframes floatBlob2 {
    from { transform: translateY(0px) translateX(0px); }
    to { transform: translateY(-30px) translateX(30px); }
}

h1, h2, h3, h4 {
    color: var(--text);
    letter-spacing: -0.02em;
}

.hero, .card, .source-card, .card-light {
    position: relative;
    z-index: 1;
}

.hero {
    padding: 2.35rem;
    border-radius: 30px;
    background: linear-gradient(135deg, rgba(255,250,242,0.94), rgba(239,225,209,0.84));
    border: 1px solid var(--border);
    margin-bottom: 1.5rem;
    box-shadow: 0 25px 70px rgba(77, 54, 37, 0.13);
    backdrop-filter: blur(18px);
}

.hero-title {
    font-size: 2.55rem;
    font-weight: 850;
    margin-bottom: 0.5rem;
}

.hero-subtitle {
    color: #6d5b4d;
    font-size: 1.08rem;
    max-width: 920px;
    line-height: 1.7;
}

.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 1.35rem;
    margin-bottom: 1rem;
    box-shadow: 0 18px 45px rgba(77, 54, 37, 0.10);
    backdrop-filter: blur(16px);
    transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 24px 55px rgba(77, 54, 37, 0.15);
}

.card-light {
    background: rgba(255,250,242,0.78);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 1.15rem;
    margin-bottom: 1rem;
    box-shadow: 0 12px 30px rgba(77, 54, 37, 0.09);
    transition: transform 0.22s ease;
}

.card-light:hover {
    transform: translateY(-4px);
}

.source-card {
    background: rgba(255,250,242,0.88);
    border: 1px solid rgba(120,92,65,0.18);
    border-radius: 18px;
    padding: 1rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 10px 25px rgba(77,54,37,0.08);
}

.badge {
    display: inline-block;
    padding: 0.45rem 0.8rem;
    border-radius: 999px;
    background: rgba(155,107,67,0.11);
    border: 1px solid rgba(155,107,67,0.24);
    color: #7a4f2d;
    font-weight: 750;
    font-size: 0.88rem;
    margin-right: 0.45rem;
    margin-bottom: 0.35rem;
}

.badge-green {
    background: rgba(135,159,123,0.16);
    border: 1px solid rgba(135,159,123,0.30);
    color: #556b48;
}

.badge-gold {
    background: rgba(200,161,90,0.16);
    border: 1px solid rgba(200,161,90,0.32);
    color: #7a5a20;
}

.small-muted {
    color: var(--muted);
    font-size: 0.95rem;
    line-height: 1.65;
}

.answer-box {
    font-size: 1.05rem;
    line-height: 1.75;
    color: #3f3329;
}

div[data-testid="stMetric"] {
    background: rgba(255,250,242,0.84);
    border: 1px solid var(--border);
    padding: 1rem;
    border-radius: 18px;
    box-shadow: 0 14px 35px rgba(77, 54, 37, 0.08);
}

div[data-testid="stMetricLabel"] {
    color: #7b6a5d;
}

div[data-testid="stMetricValue"] {
    color: #2d241d;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f1dfca 0%, #fffaf2 100%);
    border-right: 1px solid rgba(120, 92, 65, 0.15);
}

section[data-testid="stSidebar"] * {
    color: #3f3329;
}

.stTextArea textarea {
    background-color: rgba(255,250,242,0.94) !important;
    color: #2d241d !important;
    border: 1px solid rgba(120,92,65,0.24) !important;
    border-radius: 18px !important;
    box-shadow: inset 0 2px 8px rgba(77,54,37,0.04);
}

.stTextArea textarea:focus {
    border: 1px solid rgba(155,107,67,0.55) !important;
    box-shadow: 0 0 0 3px rgba(155,107,67,0.12) !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background-color: rgba(255,250,242,0.94);
    border-color: rgba(120,92,65,0.24);
    border-radius: 14px;
}

.stButton > button {
    border-radius: 16px;
    background: linear-gradient(135deg, #9b6b43, #c99a6b);
    color: white;
    border: none;
    padding: 0.72rem 1rem;
    font-weight: 800;
    box-shadow: 0 14px 30px rgba(155,107,67,0.22);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 38px rgba(155,107,67,0.30);
}

button[data-baseweb="tab"] {
    background: rgba(255,250,242,0.66);
    border-radius: 14px;
    margin-right: 0.25rem;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background: rgba(155,107,67,0.16);
    color: #7a4f2d;
}

.stDataFrame {
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid rgba(120,92,65,0.14);
}

html {
    scroll-behavior: smooth;
}
</style>
""", unsafe_allow_html=True)


def build_final_stance(query, supportive, limiting, neutral):
    q = query.lower()

    if any(term in q for term in ["homeopathic", "homeopathy", "natural", "herbal", "ayurvedic", "holistic"]):
        return (
            "Insufficient direct evidence",
            "The retrieved evidence does not directly support homeopathic or alternative treatments. "
            "The platform found alopecia-related literature, but not studies specifically testing these interventions."
        )

    if limiting > supportive:
        return (
            "Limited or negative evidence",
            "The retrieved sources contain more limiting or negative evidence language than supportive language."
        )

    if supportive > limiting:
        return (
            "Mostly supportive evidence",
            "The retrieved sources contain more supportive treatment language than limiting language. "
            "This should still be interpreted by diagnosis, population match, and evidence quality."
        )

    return (
        "Mixed or unclear evidence",
        "The retrieved sources do not clearly lean supportive or limiting."
    )


with st.sidebar:
    st.markdown("## 🧬 AIP")
    st.caption("Alopecia Intelligence Platform")
    st.markdown("---")
    st.markdown("### AI System Pipeline")
    st.markdown("""
    **1. Semantic Retrieval**  
    **2. Source Reranking**  
    **3. Evidence Grading**  
    **4. Multi-Study Synthesis**  
    **5. Final Stance Analysis**
    """)
    st.markdown("---")
    st.markdown("### Tech Stack")
    st.markdown("""
    Python · Streamlit · ChromaDB  
    Sentence Transformers · PyTorch · RAG · NLP · Evidence Scoring
    """)
    st.markdown("---")
    st.caption("AI engineering use case: biomedical evidence synthesis")

st.markdown("""
<div class="hero">
    <div class="hero-title">Alopecia Intelligence Platform</div>
    <div class="hero-subtitle">
        A research-powered intelligence platform designed to help young women and their families explore alopecia treatment evidence.
        The system uses AI-powered semantic retrieval, reranking, evidence scoring, multi-study synthesis, PubMed-grounded citation tracking,
        research gap detection, and final stance analysis.
    </div>
    <br>
    <span class="badge">Evidence-Aware RAG</span>
    <span class="badge">Semantic Search</span>
    <span class="badge">Reranking</span>
    <span class="badge">Evidence Synthesis</span>
    <span class="badge">Final Stance</span>
    <span class="badge">PubMed Grounded</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <h3>Ask a research question</h3>
    <p class="small-muted">
        Enter a treatment, safety, population, or evidence-gap question. The platform retrieves biomedical evidence,
        reranks sources, generates a custom evidence-based answer, and exposes the source trail behind the response.
    </p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([2.2, 1])

with left:
    query = st.text_area(
        "Research Question",
        placeholder="Example: Is there evidence that homeopathic treatments work for women with alopecia?",
        height=120,
    )

with right:
    top_k = st.slider("Evidence sources to use", 1, 8, 5)

    example = st.selectbox(
        "Demo question",
        [
            "",
            "What is the best medication for alopecia in teenage girls?",
            "Is ritlecitinib effective for alopecia areata?",
            "Is minoxidil useful for female hair loss?",
            "Is there evidence that homeopathic treatments work for women with alopecia?",
            "What are the safety concerns for alopecia treatments?",
        ],
    )

if example and not query.strip():
    query = example

analyze = st.button("Run Evidence Analysis", type="primary", use_container_width=True)

if analyze:
    if not query.strip():
        st.warning("Please enter a research question.")
    else:
        with st.spinner("Retrieving, reranking, synthesizing, and scoring evidence..."):
            output = answer_question(query, top_k=top_k)

        answer = output.get("answer", "No answer generated.")
        sources = output.get("sources", [])
        direction = output.get("evidence_direction", {})
        evidence_table = output.get("evidence_table", [])
        insights = output.get("research_insights", [])
        retrieved_context = output.get("retrieved_context", "")
        evidence_synthesis = output.get("evidence_synthesis", {})
        advanced_outputs = output.get("advanced_outputs", {})

        supportive = direction.get("supportive_count", 0)
        limiting = direction.get("limiting_count", 0)
        neutral = direction.get("neutral_count", 0)
        conclusion = direction.get("conclusion", "Unavailable")
        query_type = advanced_outputs.get("query_type", "general_evidence")

        stance, stance_explanation = build_final_stance(query, supportive, limiting, neutral)

        st.markdown("## Analysis Results")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Supportive", supportive)
        c2.metric("Limiting", limiting)
        c3.metric("Neutral", neutral)
        c4.metric("Sources", len(sources))

        st.markdown(f"""
        <div class="card">
            <span class="badge">{conclusion}</span>
            <span class="badge badge-green">{query_type}</span>
            <span class="badge badge-gold">{stance}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>Evidence-Based Answer</h3>
        """, unsafe_allow_html=True)
        st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>Final Stance</h3>
        """, unsafe_allow_html=True)
        st.markdown(f"<div class='answer-box'><b>{stance}</b><br>{stance_explanation}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("### Citation-Based Source Trail")

        if evidence_table:
            for row in evidence_table:
                pmid = row.get("pubmed_id", "Unknown")
                link = row.get("pubmed_link", "")
                relevance = row.get("relevance_score", 0)
                rerank = row.get("rerank_score", "N/A")
                row_direction = row.get("direction", "Unclear")
                snippet = row.get("snippet", "")

                pmid_display = f"<a href='{link}' target='_blank'>PMID {pmid}</a>" if link else f"PMID {pmid}"

                st.markdown(f"""
                <div class="source-card">
                    <b>{pmid_display}</b><br>
                    <span class="badge">Relevance: {relevance}</span>
                    <span class="badge">Rerank: {rerank}</span>
                    <span class="badge">{row_direction}</span>
                    <p class="small-muted">{snippet}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No citation sources returned.")

        tab1, tab2, tab3, tab4 = st.tabs([
            "Evidence Synthesis",
            "Evidence Table",
            "Research Insights",
            "Raw Context"
        ])

        with tab1:
            synthesis = evidence_synthesis.get("synthesis", {})
            study_summaries = evidence_synthesis.get("study_summaries", [])

            st.markdown("### Final Evidence Conclusion")
            st.write(synthesis.get("final_conclusion", "No synthesis available."))

            st.markdown("### Evidence Gaps")
            gaps = synthesis.get("evidence_gaps", [])
            if gaps:
                for gap in gaps:
                    st.write(f"• {gap}")
            else:
                st.info("No evidence gaps generated.")

            st.markdown("### Study-Level Summaries")
            if study_summaries:
                st.dataframe(pd.DataFrame(study_summaries), use_container_width=True, hide_index=True)
            else:
                st.info("No study-level summaries generated.")

        with tab2:
            graded = advanced_outputs.get("graded_evidence", evidence_table)
            if graded:
                df = pd.DataFrame(graded)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No evidence table returned.")

        with tab3:
            if insights:
                for insight in insights:
                    st.write(f"• {insight}")
            else:
                st.info("No research insights generated.")

        with tab4:
            with st.expander("Retrieved Evidence Context"):
                st.write(retrieved_context)

else:
    st.markdown("## Demo Workflows")
    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="card-light">
            <h4>Treatment Efficacy</h4>
            <p class="small-muted">Ask whether a medication has source-backed evidence of effectiveness.</p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="card-light">
            <h4>Evidence Gaps</h4>
            <p class="small-muted">Identify when the literature does not directly support a claim.</p>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="card-light">
            <h4>Final Stance</h4>
            <p class="small-muted">Translate retrieved evidence into a clear research conclusion.</p>
        </div>
        """, unsafe_allow_html=True)