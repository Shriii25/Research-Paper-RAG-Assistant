import os
import shutil
import streamlit as st
import rag

# --------------------------------------------------
# RAG FUNCTIONS
# --------------------------------------------------

build_vectorstore = rag.build_vectorstore
ask_question = rag.ask_question
generate_literature_review = rag.generate_literature_review
get_summaries = rag.get_summaries
generate_all_summaries = rag.generate_all_summaries
generate_collection_summary = rag.generate_collection_summary

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Research Paper RAG Assistant",
    layout="wide"
)

# --------------------------------------------------
# UTILITY FUNCTIONS
# --------------------------------------------------

def clear_papers():

    if os.path.exists("papers"):
        shutil.rmtree("papers")

    os.makedirs(
        "papers",
        exist_ok=True
    )


def clear_summaries():

    if os.path.exists("summaries"):
        shutil.rmtree("summaries")

    os.makedirs(
        "summaries",
        exist_ok=True
    )


def clear_vectorstore():

    if os.path.exists("vectorstore"):
        shutil.rmtree("vectorstore")

    os.makedirs(
        "vectorstore",
        exist_ok=True
    )

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📚 Research Paper RAG Assistant")

st.write("""
Upload research papers, build a knowledge base,
generate summaries, create literature reviews,
and ask questions across all uploaded papers.
""")

# --------------------------------------------------
# HOW TO USE
# --------------------------------------------------

with st.expander("📖 How To Use"):

    st.markdown("""
### Step 1
Upload PDF research papers.

### Step 2
Build Knowledge Base.

### Step 3
Generate Paper Summaries.

### Step 4
Generate Collection Summary.

### Step 5
Generate Literature Review.

### Step 6
Ask Questions.

---

### Example Questions

- Summarize all papers
- Compare methodologies across papers
- What datasets were used?
- What future work is suggested?
- What are common limitations?
- Compare research themes
""")

# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

st.header("📤 Upload Research Papers")

uploaded_files = st.file_uploader(
    "Upload PDF Research Papers",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    os.makedirs(
        "papers",
        exist_ok=True
    )

    uploaded_count = 0

    for file in uploaded_files:

        save_path = os.path.join(
            "papers",
            file.name
        )

        if not os.path.exists(save_path):

            with open(
                save_path,
                "wb"
            ) as f:

                f.write(
                    file.getbuffer()
                )

            uploaded_count += 1

    if uploaded_count > 0:

        st.success(
            f"{uploaded_count} paper(s) uploaded."
        )

# --------------------------------------------------
# PROJECT MANAGEMENT
# --------------------------------------------------

st.header("⚙️ Project Management")

col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        "Delete All Papers"
    ):

        clear_papers()

        st.success(
            "All papers deleted."
        )

        st.rerun()

with col2:

    if st.button(
        "Delete Summaries"
    ):

        clear_summaries()

        st.success(
            "Summaries deleted."
        )

        st.rerun()

with col3:

    if st.button(
        "Clear Knowledge Base"
    ):

        clear_vectorstore()
        clear_summaries()

        st.success(
            "Knowledge base cleared."
        )

        st.rerun()

# --------------------------------------------------
# UPLOADED PAPERS
# --------------------------------------------------

st.header("📄 Uploaded Papers")

pdf_files = []

if os.path.exists("papers"):

    pdf_files = [

        file

        for file in os.listdir("papers")

        if file.endswith(".pdf")
    ]

if pdf_files:

    for pdf in pdf_files:

        st.write(f"• {pdf}")

else:

    st.info(
        "No papers uploaded yet."
    )

# --------------------------------------------------
# STATS
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Research Papers",
        len(pdf_files)
    )

with col2:

    summary_count = 0

    if os.path.exists("summaries"):

        summary_count = len(
            [
                file

                for file in os.listdir(
                    "summaries"
                )

                if file.endswith(".json")
            ]
        )

    st.metric(
        "Summaries Generated",
        summary_count
    )

# --------------------------------------------------
# BUILD KNOWLEDGE BASE
# --------------------------------------------------

st.header("🧠 Knowledge Base")

if st.button(
    "Build Knowledge Base"
):

    if not pdf_files:

        st.warning(
            "Please upload papers first."
        )

    else:

        with st.spinner(
            "Building vector database..."
        ):

            chunks = build_vectorstore()

        st.success(
            f"Database created with {chunks} chunks."
        )

# --------------------------------------------------
# GENERATE SUMMARIES
# --------------------------------------------------

st.header("📝 Paper Summaries")

if st.button(
    "Generate Paper Summaries"
):

    if not pdf_files:

        st.warning(
            "Please upload papers first."
        )

    else:

        with st.spinner(
            "Generating summaries..."
        ):

            count = generate_all_summaries()

        st.success(
            f"{count} new summaries generated."
        )

# --------------------------------------------------
# SIDEBAR SUMMARIES
# --------------------------------------------------

st.sidebar.title(
    "📚 Paper Summaries"
)

summaries = get_summaries()

if summaries:

    selected = st.sidebar.selectbox(
        "Choose Paper",
        list(
            summaries.keys()
        )
    )

    st.sidebar.markdown(
        summaries[selected]
    )

# --------------------------------------------------
# COLLECTION SUMMARY
# --------------------------------------------------

st.header("📊 Collection Summary")

if st.button(
    "Generate Collection Summary"
):

    with st.spinner(
        "Analyzing papers..."
    ):

        summary = (
            generate_collection_summary()
        )

    st.markdown(summary)

# --------------------------------------------------
# LITERATURE REVIEW
# --------------------------------------------------

st.header("📖 Literature Review")

if st.button(
    "Generate Literature Review"
):

    with st.spinner(
        "Generating literature review..."
    ):

        review = (
            generate_literature_review()
        )

    st.markdown(review)

    if os.path.exists(
        "literature_review.txt"
    ):

        with open(
            "literature_review.txt",
            "r",
            encoding="utf-8"
        ) as f:

            st.download_button(
                label="Download Literature Review",
                data=f.read(),
                file_name="literature_review.txt",
                mime="text/plain"
            )

# --------------------------------------------------
# ASK QUESTIONS
# --------------------------------------------------

st.header("❓ Ask Questions")

query = st.text_input(
    "Ask anything about your uploaded papers"
)

if st.button(
    "Search Papers"
):

    if not query:

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching..."
        ):

            answer, citations = (
                ask_question(query)
            )

        st.subheader(
            "Answer"
        )

        st.write(answer)

        st.subheader(
            "Sources"
        )

        for source in citations:

            st.write(
                f"• {source}"
            )

# --------------------------------------------------
# EXAMPLE QUESTIONS
# --------------------------------------------------

st.header("💡 Example Questions")

examples = [

    "Summarize all uploaded papers",

    "What are the main research themes?",

    "Compare methodologies across papers",

    "What datasets are commonly used?",

    "What limitations are discussed?",

    "What future work is suggested?",

    "What are the key findings across papers?",

    "Compare approaches used in the uploaded papers",

    "Generate a literature review of this collection"
]

for example in examples:

    st.write(
        f"• {example}"
    )