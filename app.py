# --- 5. THE APP INTERFACE ---
def main():
    st.set_page_config(page_title="Starlight Oracle", page_icon="🌙", layout="wide")

    # --- COSMIC STYLING (CSS) ---
    st.markdown("""
    <style>
    /* Main Background Image */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1534796636912-3b95b3ab5980?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=3600");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Content Box Styling */
    .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem !important; /* Reduced padding slightly */
        margin-top: 2rem;
    }

    /* Header Text Styling */
    h1, h2, h3 { color: #2E004F !important; }
    
    .main-header {
        font-size: 3.5em; 
        color: #4B0082; 
        text-align: center; 
        font-weight: bold;
        text-shadow: 2px 2px 4px #ccc;
    }
    
    .sub-header {
        font-size: 1.4em; 
        color: #555; 
        text-align: center; 
        margin-bottom: 2em;
        font-style: italic;
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: #4B0082;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #6A0DAD;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- APP CONTENT ---
    st.markdown('<p class="main-header">✨ Starlight Oracle</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Discover your cosmic blueprint and future path.</p>', unsafe_allow_html=True)

    # --- UPDATED SIDEBAR ---
    with st.sidebar:
        # SPACER: This pushes everything down!
        st.markdown("<br><br>", unsafe_allow_html=True) 
        
        st.image("https://cdn-icons-png.flaticon.com/512/2647/2647306.png", width=100) # Optional: A nice moon icon at the top
        st.header("Enter Your Details")
        st.write("The stars are ready to speak...")
        
        name = st.text_input("First Name")
        
        # Added a spacer here too, just in case
        st.write("") 
        dob = st.date_input("Date of Birth", min_value=datetime.date(1940, 1, 1))
        
        st.write("")
        generate_btn = st.button("Generate Detailed Report ✨")

    if generate_btn and name:
        sign = get_zodiac_sign(dob.day, dob.month)
        
        # Safety check: if sign is unknown (invalid date)
        if sign == "Unknown":
            st.error("The stars are confused. Please check your birth date.")
            return

        symbol = ZODIAC_SYMBOLS.get(sign, "")
        
        # Progress Bar
        progress_text = "Consulting the stars..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        my_bar.empty()

        report = ASTRO_DATA.get(sign, {})

        # --- DISPLAY RESULTS ---
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown(f"<h2 style='text-align: center; color: #4B0082;'>Hello, {name}</h2>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{symbol}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center;'>Your Sun Sign is {sign}</h3>", unsafe_allow_html=True)
        
        st.write("---")

        tab1, tab2, tab3, tab4 = st.tabs(["🦁 Personality", "💼 Career", "💚 Health", "🔮 Future (1 Year)"])

        with tab1:
            st.markdown(f"### The Nature of a {sign}")
            st.write(report.get("Personality", "Data not available."))
            st.info("💡 **Tip:** This describes your core essence.")

        with tab2:
            st.markdown(f"### {sign} at Work")
            st.write(report.get("Career", "Data not available."))

        with tab3:
            st.markdown(f"### Vitality & Wellness")
            st.write(report.get("Health", "Data not available."))

        with tab4:
            st.markdown(f"### Predictive Outlook: 2026")
            st.markdown(f"_{report.get('Future', 'Data not available.')}_")

        # --- PDF DOWNLOAD ---
        st.write("---")
        st.subheader("📥 Keep Your Reading")
        
        pdf_bytes = create_pdf(name, sign, report)
        
        st.download_button(
            label="Download Report as PDF",
            data=pdf_bytes,
            file_name=f"{name}_Astrology_Report.pdf",
            mime="application/pdf"
        )

    elif generate_btn and not name:
        st.error("Please enter your name to begin the reading.")
    
    else:
        st.info("👈 Please use the sidebar to enter your birth details.")

if __name__ == "__main__":
    main()
