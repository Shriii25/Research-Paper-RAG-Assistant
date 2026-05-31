import os
import json

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

import google.generativeai as genai


load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

embeddings = None

def get_embeddings():
    global embeddings

    if embeddings is None:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    return embeddings

VECTOR_DB = "vectorstore"


def generate_summary(docs, filename):

    text = ""

    for doc in docs[:10]:
        text += doc.page_content + "\n"

    prompt = f"""
You are a research analyst.

Read this research paper and provide:

Title

Problem Statement

Methodology

Dataset

Results

Limitations

Future Work

Paper Content:

{text[:15000]}
"""

    response = model.generate_content(prompt)

    return {
        "paper": filename,
        "summary": response.text
    }


def save_summary(summary):

    os.makedirs(
        "summaries",
        exist_ok=True
    )

    filepath = os.path.join(
        "summaries",
        summary["paper"] + ".json"
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            summary,
            f,
            indent=4
        )


def build_vectorstore():

    all_docs = []

    for file in os.listdir("papers"):

        if not file.endswith(".pdf"):
            continue

        path = os.path.join(
            "papers",
            file
        )

        loader = PyPDFLoader(path)

        docs = loader.load()

        all_docs.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(
        all_docs
    )

    db = FAISS.from_documents(
        chunks,
        get_embeddings()
    )

    db.save_local(
        VECTOR_DB
    )

    return len(chunks)

def generate_all_summaries():

    os.makedirs(
        "summaries",
        exist_ok=True
    )

    generated = 0

    for file in os.listdir("papers"):

        if not file.endswith(".pdf"):
            continue

        summary_file = os.path.join(
            "summaries",
            file + ".json"
        )

        if os.path.exists(summary_file):
            continue

        path = os.path.join(
            "papers",
            file
        )

        loader = PyPDFLoader(path)

        docs = loader.load()

        summary = generate_summary(
            docs,
            file
        )

        save_summary(summary)

        generated += 1

    return generated


def load_db():

    return FAISS.load_local(
        VECTOR_DB,
        get_embeddings(),
        allow_dangerous_deserialization=True
    )


def ask_question(query):

    db = load_db()

    docs = db.similarity_search(
        query,
        k=5
    )

    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )

    prompt = f"""
Answer only from the context.

If information is missing,
say so.

Context:

{context}

Question:

{query}
"""

    response = model.generate_content(
        prompt
    )

    citations = []

    for doc in docs:

        source = os.path.basename(
            doc.metadata.get(
                "source",
                "Unknown"
            )
        )

        page = doc.metadata.get(
            "page",
            0
        )

        citations.append(
            f"{source} | Page {page+1}"
        )

    return (
        response.text,
        list(set(citations))
    )


def generate_literature_review():

    summaries = []

    for file in os.listdir(
        "summaries"
    ):

        path = os.path.join(
            "summaries",
            file
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            summaries.append(
                data["summary"]
            )

    combined = "\n\n".join(
        summaries
    )

    prompt = f"""
You are a senior AI researcher.

Analyze these research paper summaries.

Create a detailed literature review.

Include:

1. Overview

2. Main Themes

3. Common Methodologies

4. Key Findings

5. Research Gaps

6. Future Research Directions

Summaries:

{combined}
"""

    response = model.generate_content(
        prompt
    )

    review = response.text

    with open(
        "literature_review.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(review)

    return review


def get_summaries():

    papers = {}

    if not os.path.exists(
        "summaries"
    ):
        return papers

    for file in os.listdir(
        "summaries"
    ):

        path = os.path.join(
            "summaries",
            file
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            papers[data["paper"]] = (
                data["summary"]
            )

    return papers
def generate_collection_summary():

    summaries = get_summaries()

    if not summaries:

        return "No summaries found."

    combined = "\n\n".join(
        summaries.values()
    )

    prompt = f"""
You are an AI research analyst.

Analyze all paper summaries and provide:

1. Research Areas
2. Main Contributions
3. Common Themes
4. Key Findings
5. Future Directions

Paper Summaries:

{combined}
"""

    response = model.generate_content(
        prompt
    )

    return response.text

print("=" * 50)
print("RAG LOADED SUCCESSFULLY")
print("generate_all_summaries:", "generate_all_summaries" in globals())
print("generate_collection_summary:", "generate_collection_summary" in globals())
print("=" * 50)