import streamlit as st
from openai import OpenAI
import io
import requests
from PIL import Image
import random

# Set page config
st.set_page_config(
    page_title="Mandala Art Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, cool aesthetic
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #ffffff;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        color: #e94560;
    }
    
    /* Custom Container */
    .custom-container {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #e94560, #0f3460);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    /* Success/Info Messages */
    .stSuccess, .stInfo {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")
    st.markdown("---")
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key to generate art."
    )
    
    st.markdown("---")
    st.subheader("🎨 Creative Studio")
    
    # Creative Controls
    style_options = ["Classic Geometric", "Floral & Organic", "Cyberpunk / Neon", "Gothic / Dark", "Zen / Minimalist", "Cosmic / Celestial"]
    mood_options = ["Peaceful & Calm", "Energetic & Vibrant", "Mysterious & Deep", "Joyful & Bright", "Spiritual & Sacred"]
    material_options = ["Ink on Paper", "Digital Line Art", "Chalk on Blackboard", "Gold Foil on Black", "Watercolor Outline"]
    
    selected_style = st.selectbox("Art Style", style_options)
    selected_mood = st.selectbox("Mood / Vibe", mood_options)
    selected_material = st.radio("Material Style", material_options)
    complexity = st.slider("Complexity Level", 1, 10, 7, help="1 = Simple, 10 = Extremely Intricate")

    st.markdown("---")
    if st.button("🎲 Surprise Me!"):
        selected_style = random.choice(style_options)
        selected_mood = random.choice(mood_options)
        selected_material = random.choice(material_options)
        complexity = random.randint(3, 10)
        st.success(f"Randomized! Style: {selected_style}")

    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #rgba(255,255,255,0.6); font-size: 0.8rem;'>
            Powered by DALL·E 3
        </div>
    """, unsafe_allow_html=True)

# Main Content
st.title("🎨 Mandala Art Generator")
st.markdown("<p style='font-size: 1.2rem; opacity: 0.8;'>Transform words into intricate, symmetrical masterpieces.</p>", unsafe_allow_html=True)

# Main Logic
if not api_key:
    st.info("👋 Welcome! Please enter your OpenAI API Key in the sidebar to begin.")
else:
    try:
        client = OpenAI(api_key=api_key)
        
        # Input Section
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                user_word = st.text_input(
                    "Enter your inspiration",
                    placeholder="e.g., Serenity, Chaos, Bloom...",
                    label_visibility="collapsed"
                )
            with col2:
                generate_btn = st.button("✨ Generate", use_container_width=True)

        if generate_btn and user_word:
            with st.spinner("🎨 Weaving your mandala..."):
                try:
                    # Construct Dynamic Prompt
                    complexity_desc = "simple and clean" if complexity < 4 else "highly intricate and detailed" if complexity > 7 else "balanced detail"
                    
                    prompt = f"""
                    A {complexity_desc} mandala art piece based on the concept of '{user_word}'.
                    Style: {selected_style}.
                    Mood: {selected_mood}.
                    Medium: {selected_material}.
                    
                    The design must be perfectly symmetrical and centered.
                    High contrast, sharp lines.
                    If 'Ink on Paper' or 'Digital Line Art', use black lines on white background.
                    If 'Chalk on Blackboard' or 'Gold Foil on Black', use light lines on dark background.
                    No shading, no gradients, just pure line art unless the style dictates otherwise.
                    """
                    
                    response = client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                    )

                    image_url = response.data[0].url
                    
                    # Display Result
                    st.markdown("---")
                    st.subheader(f"Your '{user_word}' Mandala")
                    st.caption(f"Style: {selected_style} | Mood: {selected_mood} | Complexity: {complexity}/10")
                    
                    # Layout for image and download
                    img_col, action_col = st.columns([2, 1])
                    
                    with img_col:
                        st.image(image_url, use_container_width=True)
                    
                    with action_col:
                        st.success("✨ Generation Complete!")
                        
                        # Fetch image for download
                        img_response = requests.get(image_url)
                        img_bytes = img_response.content
                        
                        st.download_button(
                            label="📥 Download High-Res PNG",
                            data=img_bytes,
                            file_name=f"mandala_{user_word}_{selected_style}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                        
                        st.markdown("### Tips")
                        st.info("Try different styles and moods to see how the interpretation changes!")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        
        elif generate_btn and not user_word:
            st.warning("Please enter a word to inspire your mandala.")

    except Exception as e:
        st.error(f"Error initializing OpenAI client: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; opacity: 0.5; font-size: 0.8rem;'>
        Generated art is unique and yours to keep.
    </div>
""", unsafe_allow_html=True)