import streamlit as st
import time
import random
import numpy as np
from datetime import datetime
import json
import uuid

# Set page configuration
st.set_page_config(
    page_title="Quantum-Optimized AI Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #e6f3ff;
        border-left: 5px solid #2196F3;
    }
    .chat-message.assistant {
        background-color: white;
        border-left: 5px solid #4CAF50;
    }
    .chat-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    .chat-header img {
        margin-right: 0.5rem;
    }
    .thinking-indicator {
        display: flex;
        align-items: center;
        margin: 1rem 0;
        font-style: italic;
        color: #555;
    }
    .thinking-dot {
        height: 8px;
        width: 8px;
        background-color: #555;
        border-radius: 50%;
        margin: 0 2px;
        display: inline-block;
        animation: pulse 1.5s infinite;
    }
    .thinking-dot:nth-child(2) {
        animation-delay: 0.3s;
    }
    .thinking-dot:nth-child(3) {
        animation-delay: 0.6s;
    }
    @keyframes pulse {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }
    .prompt-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }
    .deep-thinking-button {
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 0.5rem;
        background-color: white;
        display: flex;
        align-items: center;
        cursor: pointer;
        transition: all 0.3s;
    }
    .deep-thinking-button:hover {
        background-color: #f0f0f0;
    }
    .deep-thinking-active {
        background-color: #e6f7ff;
        border-color: #1890ff;
    }
    .model-info {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    .clear-button {
        cursor: pointer;
        color: #666;
        font-size: 0.9rem;
        padding: 5px 10px;
        border-radius: 4px;
        transition: background-color 0.3s;
    }
    .clear-button:hover {
        background-color: #f0f0f0;
        text-decoration: underline;
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 24px;
        font-size: 16px;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .stButton > button:disabled {
        background-color: #cccccc;
        cursor: not-allowed;
    }
    .quantum-badge {
        background-color: rgba(76, 175, 80, 0.1);
        color: #4CAF50;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        margin-left: 8px;
    }
    .stTextArea > div > div > textarea {
        border-radius: 4px;
        border-color: #ddd;
    }
    .thinking-progress {
        margin-top: 5px;
    }
    .footnote {
        font-size: 0.7rem;
        color: #999;
        text-align: center;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'thinking_mode' not in st.session_state:
    st.session_state.thinking_mode = False
if 'is_thinking' not in st.session_state:
    st.session_state.is_thinking = False
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'waiting_for_response' not in st.session_state:
    st.session_state.waiting_for_response = False
if 'progress_value' not in st.session_state:
    st.session_state.progress_value = 0

# Function to generate responses
def generate_response(prompt, thinking_mode=False, model="quantum", temperature=0.7):
    # For demo purposes, we're using canned responses
    # In a real app, this would call an AI API
    
    basic_responses = [
        "Based on quantum-optimized analysis, the solution to your problem involves a multi-faceted approach. First, we need to consider the underlying patterns in the data structure. The optimization technique I would recommend leverages parallel processing with reduced memory overhead.",
        "I've analyzed your request using our quantum-enhanced algorithms. The key insight is that traditional approaches overlook the potential for dimensional reduction before processing. By applying our optimized framework, we can achieve significantly faster results with lower computational requirements.",
        "Your question touches on several complex domains. Using quantum-inspired optimization techniques, I can provide a more comprehensive answer than conventional methods would allow. The critical factor here is understanding how different variables interact across computational frameworks."
    ]
    
    technical_responses = [
        "Looking at this problem through the lens of computational complexity theory, we can identify multiple optimization opportunities. The time complexity can be reduced from O(n²) to O(n log n) by implementing a quantum-inspired sorting algorithm that leverages entanglement properties within the data structure.",
        "The approach I recommend is based on tensor decomposition methods adapted from quantum mechanics. By representing your problem as a multi-dimensional tensor, we can apply singular value decomposition to isolate the most influential factors with minimal information loss.",
        "After analyzing your query, I've identified that we can leverage quantum parallelism concepts to expedite this computation. By restructuring the algorithm to exploit inherent symmetries in the problem space, we can achieve polynomial speedup over classical methods."
    ]
    
    # Pick response pool based on the query complexity
    word_count = len(prompt.split())
    if "code" in prompt.lower() or "algorithm" in prompt.lower() or word_count > 15:
        responses = technical_responses
    else:
        responses = basic_responses
    
    # Pick a random response
    response = random.choice(responses)
    
    # If deep thinking mode is enabled, add more detailed analysis
    if thinking_mode:
        deep_analysis = [
            "\n\nDoing deeper analysis through quantum optimization pathways reveals additional insights:\n\n1. The conventional approach would miss critical edge cases in approximately 17% of scenarios\n2. By restructuring the computational graph, we can achieve 2.8x more efficient resource utilization\n3. There's a previously unidentified opportunity for pipelined execution that reduces latency by 32%",
            "\n\nExtended quantum-optimized reasoning suggests:\n\n1. Traditional methods would encounter diminishing returns beyond certain threshold\n2. Through graph restructuring and tensor decomposition, we can maintain linear scaling across much larger datasets\n3. The optimal solution incorporates adaptive resource allocation based on workload characteristics",
            "\n\nUsing quantum-enhanced thinking patterns, I've identified these critical factors:\n\n1. The problem space contains non-obvious symmetries that can be exploited for 43% faster computation\n2. Dynamic reallocation of computational resources yields significantly better results than static allocation\n3. By interleaving operations in a specific sequence, we can minimize memory transfers and achieve near-theoretical maximum throughput"
        ]
        response += random.choice(deep_analysis)
    
    return response

# Handle deep thinking toggle from JavaScript
if st.session_state.get('toggle_deep_thinking'):
    st.session_state.thinking_mode = not st.session_state.thinking_mode
    st.session_state.toggle_deep_thinking = False

# Handle clear chat from JavaScript
if st.session_state.get('clear_chat'):
    st.session_state.chat_history = []
    st.session_state.clear_chat = False

# Sidebar - Model Selection
st.sidebar.title("Model Settings")
model_option = st.sidebar.selectbox(
    "Choose Model",
    ["Quantum GPU-Optimized LLM", "Standard LLM"],
    index=0
)

temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
max_tokens = st.sidebar.slider("Max Output Tokens", min_value=256, max_value=4096, value=2048, step=256)

# Add conversation export option to sidebar
st.sidebar.markdown("---")
if st.sidebar.button("Export Conversation"):
    # Prepare conversation data
    conversation_data = {
        "session_id": st.session_state.session_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model": model_option,
        "messages": st.session_state.chat_history
    }
    
    # Convert to JSON string
    conversation_json = json.dumps(conversation_data, indent=2)
    
    # Display download link
    st.sidebar.download_button(
        label="Download JSON",
        data=conversation_json,
        file_name=f"conversation_{st.session_state.session_id[:8]}_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )

# Add About section to sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("## About")
st.sidebar.markdown("""
This application demonstrates a quantum-optimized AI assistant interface. The quantum optimization technology significantly enhances processing speed and efficiency.

**Key Features:**
- Deep thinking mode for complex reasoning
- Quantum-optimized response generation
- Advanced context understanding
- Conversation export functionality
""")

# For GitHub Pages compatibility
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="footnote">
    Version 1.0.0 • Deployed on GitHub Pages<br>
    © 2025 Quantum AI Technologies
</div>
""", unsafe_allow_html=True)

# Main content
st.markdown("<div class='header-container'><h1>Quantum-Optimized AI Assistant</h1><span class='clear-button' id='clear-chat'>Clear chat</span></div>", unsafe_allow_html=True)

# JavaScript for handling button clicks
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Handle deep thinking toggle
    const deepThinkingButton = document.getElementById('deep-thinking-toggle');
    if (deepThinkingButton) {
        deepThinkingButton.addEventListener('click', function() {
            const isActive = this.classList.contains('deep-thinking-active');
            if (isActive) {
                this.classList.remove('deep-thinking-active');
            } else {
                this.classList.add('deep-thinking-active');
            }
            // Send message to Streamlit
            window.parent.Streamlit.setComponentValue({type: 'toggle_deep_thinking', value: true});
        });
    }

    // Handle clear chat
    const clearChatButton = document.getElementById('clear-chat');
    if (clearChatButton) {
        clearChatButton.addEventListener('click', function() {
            if (confirm('Are you sure you want to clear the chat history?')) {
                window.parent.Streamlit.setComponentValue({type: 'clear_chat', value: true});
            }
        });
    }
});
</script>
""", unsafe_allow_html=True)

# Display welcome message if chat is empty
if not st.session_state.chat_history:
    st.markdown("""
    <div class="chat-message assistant">
        <div class="chat-header">
            <span>Assistant</span>
            <span class="quantum-badge">Quantum AI</span>
            <span style="margin-left: auto; font-weight: normal; font-size: 0.8rem; color: #666;">Now</span>
        </div>
        <p>Welcome to the Quantum-Optimized AI Assistant. I'm designed to provide enhanced responses using quantum-inspired algorithms and deep thinking capabilities.</p>
        <p>How can I assist you today?</p>
    </div>
    """, unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat_history:
    role = message["role"]
    content = message["content"]
    timestamp = message.get("timestamp", "")
    
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user">
            <div class="chat-header">
                <span>You</span>
                <span style="margin-left: auto; font-weight: normal; font-size: 0.8rem; color: #666;">{timestamp}</span>
            </div>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        badge = '<span class="quantum-badge">Quantum AI</span>' if model_option == "Quantum GPU-Optimized LLM" else ''
        st.markdown(f"""
        <div class="chat-message assistant">
            <div class="chat-header">
                <span>Assistant</span>
                {badge}
                <span style="margin-left: auto; font-weight: normal; font-size: 0.8rem; color: #666;">{timestamp}</span>
            </div>
            {content}
        </div>
        """, unsafe_allow_html=True)

# Thinking indicator
if st.session_state.is_thinking:
    thinking_container = st.empty()
    progress_bar = st.empty()
    
    # Animated thinking indicator with dots
    thinking_html = """
    <div class="thinking-indicator">
        <div>Thinking<span class="thinking-dot"></span><span class="thinking-dot"></span><span class="thinking-dot"></span></div>
    </div>
    """
    thinking_container.markdown(thinking_html, unsafe_allow_html=True)
    
    # Show progress bar for deep thinking mode
    if st.session_state.thinking_mode:
        progress = progress_bar.progress(st.session_state.progress_value)

# Input area
st.markdown("<div class='prompt-container'>", unsafe_allow_html=True)

# Two-column layout for deep thinking button and prompt
col1, col2 = st.columns([1, 6])

with col1:
    deep_thinking_class = "deep-thinking-button deep-thinking-active" if st.session_state.thinking_mode else "deep-thinking-button"
    deep_thinking_html = f"""
    <div class="{deep_thinking_class}" id="deep-thinking-toggle">
        <span>🧠 Deep Thinking</span>
    </div>
    """
    st.markdown(deep_thinking_html, unsafe_allow_html=True)

with col2:
    # Disable input while waiting for response
    prompt = st.text_area("Send a message", height=80, key="prompt_input", disabled=st.session_state.waiting_for_response)
    
    # Display model info beneath the text area
    if model_option == "Quantum GPU-Optimized LLM":
        model_info = "Using Quantum GPU-Optimized LLM with 70-120% performance improvement"
    else:
        model_info = "Using Standard LLM"
    
    st.markdown(f"<div class='model-info'>{model_info}</div>", unsafe_allow_html=True)

# Submit button row
submit_col1, submit_col2 = st.columns([6, 1])
with submit_col2:
    submit_button = st.button("Submit", disabled=st.session_state.waiting_for_response or not prompt.strip())

st.markdown("</div>", unsafe_allow_html=True)

# Handle message submission
if submit_button and prompt:
    # Add user message to chat history
    current_time = datetime.now().strftime("%H:%M")
    st.session_state.chat_history.append({
        "role": "user",
        "content": prompt,
        "timestamp": current_time
    })
    
    # Set flags for thinking state
    st.session_state.is_thinking = True
    st.session_state.waiting_for_response = True
    st.session_state.progress_value = 0
    
    # Rerun to show thinking indicator
    st.experimental_rerun()

# Process thinking and response generation
if st.session_state.is_thinking:
    # Determine thinking time based on mode and model
    base_thinking_time = 2 if model_option == "Quantum GPU-Optimized LLM" else 4
    thinking_time = base_thinking_time if not st.session_state.thinking_mode else base_thinking_time * 3
    
    # For deep thinking mode, update progress bar
    if st.session_state.thinking_mode:
        steps = 10
        for i in range(steps):
            # Simulate computation with random progress increases
            time.sleep(thinking_time / steps)
            st.session_state.progress_value = min((i + 1) / steps, 1.0)
            st.experimental_rerun()
    else:
        # Simple delay for regular mode
        time.sleep(thinking_time)
    
    # Generate response
    user_prompt = st.session_state.chat_history[-1]["content"]
    response = generate_response(
        prompt=user_prompt,
        thinking_mode=st.session_state.thinking_mode,
        model="quantum" if model_option == "Quantum GPU-Optimized LLM" else "standard",
        temperature=temperature
    )
    
    # Add assistant response to chat history
    current_time = datetime.now().strftime("%H:%M")
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response,
        "timestamp": current_time
    })
    
    # Reset states
    st.session_state.is_thinking = False
    st.session_state.waiting_for_response = False
    st.session_state.progress_value = 0
    
    # Update the interface
    st.experimental_rerun()

# Add compatibility script for GitHub Pages
footer_html = """
<script>
// GitHub Pages compatibility script
// This ensures the app can handle page reloads and deep linking
document.addEventListener('DOMContentLoaded', function() {
    // Store chat state in local storage on changes
    function persistChatState() {
        const chatHistory = window.streamlitState?.chat_history || [];
        localStorage.setItem('quantum_ai_chat_history', JSON.stringify(chatHistory));
    }
    
    // Check for local storage on page load
    function restoreChatState() {
        const savedChat = localStorage.getItem('quantum_ai_chat_history');
        if (savedChat && window.streamlitState) {
            window.streamlitState.chat_history = JSON.parse(savedChat);
            // Trigger Streamlit update
            window.parent.Streamlit.setComponentValue({type: 'restore_chat', value: true});
        }
    }
    
    // Observe for changes to chat state
    const observer = new MutationObserver(function(mutations) {
        persistChatState();
    });
    
    // Start observing once Streamlit is fully loaded
    const checkStreamlit = setInterval(function() {
        if (window.streamlitState) {
            clearInterval(checkStreamlit);
            restoreChatState();
            
            // Set up observer
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }
    }, 100);
});
</script>
"""

st.markdown(footer_html, unsafe_allow_html=True)
