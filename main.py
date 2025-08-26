"""
Content Idea Generator — Streamlit + OpenAI

How to run:
1. Install dependencies:
   pip install streamlit openai
2. Set your OpenAI API key as an environment variable:
   export OPENAI_API_KEY="sk-..."   (macOS / Linux)
   setx OPENAI_API_KEY "sk-..."     (Windows PowerShell)
   OR paste it in the sidebar of the app (not recommended for long-term use).
3. Run the app:
   streamlit run app.py

This single-file app provides a fast, polished MVP that returns a JSON array of content ideas
from the OpenAI Chat API, parses them, and shows tools to copy/download.
"""

import os
import json
import time
from io import StringIO
from typing import List

import streamlit as st
import openai

# ----------------------------
# Configuration / Defaults
# ----------------------------
DEFAULT_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 600
DEFAULT_NUM_IDEAS = 5

# ----------------------------
# Helpers
# ----------------------------

def set_api_key_from_env_or_input():
    """Prefer environment variable but allow a one-off key in the sidebar."""
    env_key = os.getenv("OPENAI_API_KEY")
    input_key = st.sidebar.text_input("OpenAI API key (optional)", type="password")
    if input_key:
        openai.api_key = input_key
        st.sidebar.success("Using API key from sidebar (not persisted).")
    elif env_key:
        openai.api_key = env_key
        st.sidebar.write("Using OPENAI_API_KEY from environment.")
    else:
        st.sidebar.warning("No OpenAI API key found. Set OPENAI_API_KEY env variable or paste it above.")


def extract_json_array(text: str) -> List[str]:
    """Tries to extract a JSON array of strings from text returned by the model.
    Falls back to line-splitting if JSON parse fails.
    """
    text = text.strip()
    # Common case: model returns a JSON array
    try:
        # Try to find the first '[' and last ']' to grab the JSON array
        start = text.index("[")
        end = text.rindex("]") + 1
        candidate = text[start:end]
        arr = json.loads(candidate)
        if isinstance(arr, list) and all(isinstance(i, str) for i in arr):
            return [i.strip() for i in arr if i and i.strip()]
    except Exception:
        pass

    # Fallback: split on newlines and remove numbering/dashes
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    cleaned = []
    for ln in lines:
        # Remove leading numbering like "1.", "-", "•"
        ln = ln.lstrip("-• ")
        # Remove numeric prefixes (e.g., "1. ")
        if ln and ln[0].isdigit():
            # drop leading digits and punctuation
            i = 0
            while i < len(ln) and (ln[i].isdigit() or ln[i] in ".) "):
                i += 1
            ln = ln[i:].strip()
        if ln:
            cleaned.append(ln)
    return cleaned


def call_openai_chat(prompt: str, temperature: float, model: str = DEFAULT_MODEL, max_tokens: int = MAX_TOKENS):
    if not getattr(openai, "api_key", None):
        raise RuntimeError("OpenAI API key is not set.")

    messages = [
        {"role": "system", "content": (
            "You are a helpful assistant that returns a strictly parseable JSON array "
            "of short, actionable content-creation ideas (strings)."
        )},
        {"role": "user", "content": prompt},
    ]

    resp = openai.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    text = resp.choices[0].message.content
    return text


def generate_ideas(topic: str, n: int = 5, style: str = "General", tone: str = "Practical", temperature: float = 0.7) -> List[str]:
    """Generate `n` content ideas for `topic` and return them as a list of strings."""
    prompt = (
        f"Topic: {topic}\n"
        f"Number of ideas: {n}\n"
        f"Style: {style}\n"
        f"Tone: {tone}\n"
        "Instructions: Return ONLY a JSON array of strings. Example: [\"Idea 1\", \"Idea 2\"]\n"
        "Each idea should be concise (preferably < 140 characters), actionable, and unique."
    )

    raw = call_openai_chat(prompt=prompt, temperature=temperature)
    ideas = extract_json_array(raw)

    # Defensive: if model gave more/less, trim/pad
    if len(ideas) >= n:
        return ideas[:n]

    # If fewer returned, attempt one more time with a stronger instruction
    if len(ideas) < n:
        fallback_prompt = (
            f"Topic: {topic}\nNumber of ideas: {n}\nStyle: {style}\nTone: {tone}\n"
            "Return ONLY a JSON array of exactly the requested number of ideas (strings)."
        )
        raw2 = call_openai_chat(prompt=fallback_prompt, temperature=temperature)
        ideas2 = extract_json_array(raw2)
        if len(ideas2) >= n:
            return ideas2[:n]

    # Final fallback: return whatever we have, possibly duplicated to reach n
    result = ideas[:]
    while len(result) < n:
        result.append(result[-1] + "") if result else result.append(f"{topic} - idea {len(result)+1}")
    return result


# ----------------------------
# Streamlit UI
# ----------------------------

def main():
    st.set_page_config(page_title="Content Idea Generator", layout="centered")
    st.title("⚡ Content Idea Generator — 1-hour MVP")

    # Sidebar controls
    st.sidebar.header("Settings")
    set_api_key_from_env_or_input()

    model = st.sidebar.selectbox("Model", options=["gpt-3.5-turbo"], index=0, help="Choose model (default: gpt-3.5-turbo).")
    num_ideas = st.sidebar.slider("Ideas per generation", min_value=1, max_value=20, value=DEFAULT_NUM_IDEAS)
    temp = st.sidebar.slider("Creativity (temperature)", min_value=0.0, max_value=1.0, value=0.7)
    style = st.sidebar.selectbox("Style/template", options=["General", "Listicle", "How-to", "Twitter thread", "Video hook", "Newsletter subject"], index=0)
    tone = st.sidebar.selectbox("Tone", options=["Practical", "Persuasive", "Funny", "Curious", "Controversial"], index=0)

    st.markdown(
        "Use this tool to generate quick, actionable content ideas. Keep scope narrow for better results (e.g., 'vegan breakfast recipes' rather than 'food')."
    )

    # Inputs
    topic = st.text_input("Enter your topic / niche / keyword(s)")
    col1, col2 = st.columns([1, 1])
    with col1:
        gen_btn = st.button("Generate Ideas")
    with col2:
        gen_more_btn = st.button("Generate More (append)")

    if "ideas" not in st.session_state:
        st.session_state.ideas = []
        st.session_state.topic = ""

    if gen_btn:
        if not topic:
            st.error("Please enter a topic before generating ideas.")
        else:
            with st.spinner("Generating ideas…"):
                try:
                    start = time.time()
                    ideas = generate_ideas(topic=topic, n=num_ideas, style=style, tone=tone, temperature=temp)
                    took = time.time() - start
                    st.session_state.ideas = ideas
                    st.session_state.topic = topic
                    st.success(f"Generated {len(ideas)} ideas (took {took:.1f}s)")
                except Exception as e:
                    st.exception(e)

    if gen_more_btn:
        if not st.session_state.topic:
            st.error("No previous topic — press 'Generate Ideas' first or enter a topic.")
        else:
            with st.spinner("Generating additional ideas…"):
                try:
                    more = generate_ideas(topic=st.session_state.topic, n=num_ideas, style=style, tone=tone, temperature=temp)
                    st.session_state.ideas += more
                    st.success(f"Appended {len(more)} more ideas — now {len(st.session_state.ideas)} total")
                except Exception as e:
                    st.exception(e)

    # Display results
    if st.session_state.ideas:
        st.subheader("Ideas")
        # numbered display + small action buttons
        for i, idea in enumerate(st.session_state.ideas, start=1):
            st.markdown(f"**{i}.** {idea}")

        st.divider()
        st.subheader("Bulk tools")
        joined = "\n".join([f"{i+1}. {it}" for i, it in enumerate(st.session_state.ideas)])
        st.text_area("Copy all ideas", value=joined, height=150)

        # CSV download
        csv_io = StringIO()
        csv_io.write("index,idea\n")
        for idx, it in enumerate(st.session_state.ideas, start=1):
            # escape double quotes
            safe = it.replace('"', '""')
            csv_io.write(f"{idx},\"{safe}\"\n")
        csv_bytes = csv_io.getvalue().encode("utf-8")
        st.download_button("Download CSV", data=csv_bytes, file_name="content_ideas.csv", mime="text/csv")

        # TXT download
        st.download_button("Download TXT", data=joined, file_name="content_ideas.txt", mime="text/plain")

        # Clear
        if st.button("Clear ideas"):
            st.session_state.ideas = []
            st.session_state.topic = ""
            st.experimental_rerun()

    # Footer / tips
    st.markdown("---")
    st.caption("Tip: narrow topics + specific style produce higher-quality ideas. Use the sidebar to tweak creativity and format.")


if __name__ == '__main__':
    main()
