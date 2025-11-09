# Import the necessary libraries
import streamlit as st  # For creating the web app interface
from langchain_google_genai import ChatGoogleGenerativeAI  # For interacting with Google Gemini via LangChain
from langgraph.prebuilt import create_react_agent  # For creating a ReAct agent
from langchain_core.messages import HumanMessage, AIMessage  # For message formatting
import base64  # For encoding images
from PIL import Image  # For image processing
import io  # For handling file streams

# --- Custom CSS for Attractive UI ---
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .sidebar .sidebar-content {
        background: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%);
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 10px;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #FF8E53;
    }
    .stSelectbox>div>div>select {
        border-radius: 10px;
        border: 2px solid #FE6B8B;
    }
    .stFileUploader>div>div>button {
        background: #4CAF50;
        color: white;
        border-radius: 10px;
    }
    .chat-message {
        border-radius: 15px;
        padding: 10px;
        margin: 10px 0;
    }
    .user-message {
        background: #e3f2fd;
        color: #0d47a1;
    }
    .assistant-message {
        background: #f3e5f5;
        color: #4a148c;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.markdown("""
    <div style="text-align: center; padding: 20px; background: rgba(255, 255, 255, 0.1); border-radius: 15px; margin-bottom: 20px;">
        <h1 style="color: white;">📚 BrainBoost Education Chatbot</h1>
        <p style="color: #ffeb3b; font-size: 18px;">Your friendly AI tutor for learning, university advice, and more! 🚀</p>
    </div>
    """, unsafe_allow_html=True)

# --- Main Layout with Columns ---
col1, col2 = st.columns([1, 3])  # Sidebar on left, chat on right

with col1:
    # --- Sidebar for Settings ---
    with st.expander("⚙️ Settings & Upload", expanded=True):
        # Create a text input field for the Google AI API Key.
        google_api_key = st.text_input("🔑 Google AI API Key", type="password", placeholder="Enter your API key here...")
        
        # Add a select box for subject focus
        subject_focus = st.selectbox(
            "🎯 Subject Focus",
            ["General", "Math", "Science", "History", "Literature", "Programming", "University Info", "Scholarships", "Majors", "Student Consultation"],
            help="Choose a focus to get tailored advice!"
        )
        
        # Add file uploader
        uploaded_file = st.file_uploader(
            "📁 Upload File (Image, PDF, Text)",
            type=["png", "jpg", "jpeg", "gif", "pdf", "txt"],
            help="Upload and discuss files with me!"
        )
        
        # Reset button
        reset_button = st.button("🔄 Reset Conversation")

with col2:
    # --- Chat Area ---
    st.subheader("💬 Chat with BrainBoost")
    
    # Initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display past messages with custom styling
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message"><strong>BrainBoost:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    prompt = st.text_input("💭 Ask me anything...", placeholder="Type your question or discuss the uploaded file...")
    
    # Submit button for better UX
    if st.button("🚀 Send Message"):
        if not prompt and not uploaded_file:
            st.warning("Please enter a message or upload a file!")
        else:
            # Process file upload
            full_content = prompt or ""
            file_content = None
            if uploaded_file:
                file_type = uploaded_file.type
                if file_type.startswith("image/"):
                    # Display image preview in chat
                    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
                    image = Image.open(uploaded_file)
                    buffer = io.BytesIO()
                    image.save(buffer, format="PNG")
                    file_content = base64.b64encode(buffer.getvalue()).decode("utf-8")
                    full_content += f"\n\n[Uploaded Image: {file_content}]"
                    st.success("Image uploaded and ready to analyze! 🎉")
                elif file_type == "text/plain":
                    file_content = uploaded_file.read().decode("utf-8")
                    full_content += f"\n\n[Uploaded File Content: {file_content}]"
                    # Display text preview
                    st.text_area("Uploaded Text Preview", file_content[:500] + "..." if len(file_content) > 500 else file_content, height=100, disabled=True)
                    st.success("Text file uploaded! 📄")
                elif file_type == "application/pdf":
                    st.warning("PDF handling is basic. Full support coming soon! 📑")
                    file_content = "PDF content: [Placeholder - Content not fully extracted]"
                    full_content += f"\n\n{file_content}"
                    # Placeholder for PDF preview
                    st.info("PDF uploaded. Discuss it in your message!")
            
            # Add to history
            st.session_state.messages.append({"role": "user", "content": full_content})
            
            # Display user message
            st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {prompt}</div>', unsafe_allow_html=True)
            
            # Agent response
            if google_api_key:
                try:
                    # Initialize agent if needed
                    if ("agent" not in st.session_state) or (getattr(st.session_state, "_last_key", None) != google_api_key) or (getattr(st.session_state, "_last_subject", None) != subject_focus):
                        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key, temperature=0.7)
                        base_prompt = "You are BrainBoost, a fun educational assistant. Help with learning, explain concepts, and discuss uploaded files/images."
                        if subject_focus == "University Info":
                            base_prompt += " Focus on universities, admissions, and campus life."
                        elif subject_focus == "Scholarships":
                            base_prompt += " Focus on scholarships and funding."
                        elif subject_focus == "Majors":
                            base_prompt += " Focus on majors and career paths."
                        elif subject_focus == "Student Consultation":
                            base_prompt += " Provide advice on student life and transitions."
                        elif subject_focus != "General":
                            base_prompt += f" Focus on {subject_focus}."
                        st.session_state.agent = create_react_agent(model=llm, tools=[], prompt=base_prompt)
                        st.session_state._last_key = google_api_key
                        st.session_state._last_subject = subject_focus
                        st.session_state.pop("messages", None)
                    
                    # Process messages for agent
                    messages = []
                    for msg in st.session_state.messages:
                        if msg["role"] == "user":
                            if "[Uploaded Image:" in msg["content"]:
                                text_part = msg["content"].split("\n\n[Uploaded Image:")[0]
                                image_part = msg["content"].split("[Uploaded Image: ")[1].rstrip("]")
                                messages.append(HumanMessage(content=[{"type": "text", "text": text_part}, {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_part}"}}]))
                            else:
                                messages.append(HumanMessage(content=msg["content"]))
                        else:
                            messages.append(AIMessage(content=msg["content"]))
                    
                    response = st.session_state.agent.invoke({"messages": messages})
                    answer = response["messages"][-1].content if "messages" in response and response["messages"] else "Sorry, couldn't generate a response!"
                    
                    # Display assistant message
                    st.markdown(f'<div class="chat-message assistant-message"><strong>BrainBoost:</strong> {answer}</div>', unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.balloons()  # Fun animation
                    
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Please enter your API key!")

# --- Footer ---
st.markdown("""
    <div style="text-align: center; padding: 10px; background: rgba(255, 255, 255, 0.1); border-radius: 10px; margin-top: 20px;">
        <p style="color: white;">Made with ❤️ by BrainBoost Team | Powered by Streamlit & Google Gemini</p>
    </div>
    """, unsafe_allow_html=True)

# Handle reset
if reset_button:
    st.session_state.pop("agent", None)
    st.session_state.pop("messages", None)
    st.success("Conversation reset! 🔄")
    st.rerun()
