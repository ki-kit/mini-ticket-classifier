import streamlit as st
import requests
import json
from src.config import OLLAMA_URL, MODEL_NAME
from src.tickets import SAMPLE_TICKETS
from src.prompt import SYSTEM_PROMPT, get_user_prompt
from src.validator import validate_and_parse_response

st.set_page_config(page_title="AI Ticket Classifier", page_icon="🎫", layout="wide")

st.title("🎫 Mini AI Ticket Classifier")
st.caption(f"Powered by Ollama Local LLM Engine ({MODEL_NAME})")

def analyze_ticket(text: str):
    """Hits the Ollama API to run the analysis."""
    try:
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": get_user_prompt(text)}
            ],
            "options": {
                "temperature": 0.0  # Keep responses deterministic
            },
            "stream": False
        }
        response = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=30)
        
        if response.status_code == 200:
            raw_content = response.json().get("message", {}).get("content", "")
            return validate_and_parse_response(raw_content)
        else:
            return None, f"Ollama API Error: HTTP Status {response.status_code}"
    except Exception as e:
        return None, f"Connection Error: Could not reach Ollama instance. {str(e)}"

# Setup Sidebar layout for processing pre-made mock tickets
st.sidebar.header("📋 Preloaded Mock Tickets")
st.sidebar.write("Select and process individual tickets or process them all at once.")

# Individual Single Run Option
selected_ticket = st.sidebar.selectbox(
    "Choose a sample ticket to analyze:", 
    options=SAMPLE_TICKETS, 
    format_func=lambda x: f"Ticket #{x['id']}: {x['text'][:40]}..."
)

if st.sidebar.button("Run Analysis on Selected"):
    st.subheader(f"Analyzing Ticket #{selected_ticket['id']}")
    st.info(f"**Raw Text:** {selected_ticket['text']}")
    
    with st.spinner("Processing with local LLM..."):
        result, error = analyze_ticket(selected_ticket['text'])
        
    if error:
        st.error(error)
    else:
        st.success("Analysis Successful & Validated!")
        st.json(result)

st.sidebar.markdown("---")

# Batch Process All Option
if st.sidebar.button("⚡ Run All 5 Batch Tickets"):
    st.subheader("Batch Process Results")
    
    for ticket in SAMPLE_TICKETS:
        with st.expander(f"Ticket #{ticket['id']} - Details", expanded=True):
            st.write(f"**Text:** {ticket['text']}")
            with st.spinner("Classifying..."):
                result, error = analyze_ticket(ticket['text'])
            
            if error:
                st.error(f"❌ Failed Validation: {error}")
            else:
                st.success("✅ Valid Output Recieved")
                st.json(result)

# Custom Text Input Field Option
st.markdown("---")
st.subheader("📝 Test with custom inputs")
custom_input = st.text_area("Type or paste an incident description below:", placeholder="Example: The server crashed after I clicked export...")

if st.button("Classify Custom Incident"):
    if not custom_input.strip():
        st.warning("Please type something first.")
    else:
        with st.spinner("Thinking..."):
            result, error = analyze_ticket(custom_input)
        if error:
            st.error(error)
        else:
            st.json(result)