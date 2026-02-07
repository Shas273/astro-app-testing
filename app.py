import streamlit as st
import datetime
import time
from fpdf import FPDF

# --- 1. CONFIGURATION & ASSETS ---
# Dictionary for Zodiac Symbols (Glyphs)
ZODIAC_SYMBOLS = {
    "Aries": "♈", "Taurus": "♉", "Gemini": "♊", "Cancer": "♋",
    "Leo": "♌", "Virgo": "♍", "Libra": "♎", "Scorpio": "♏",
    "Sagittarius": "♐", "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓"
}

# --- 2. ASTROLOGY DATA ENGINE ---
ASTRO_DATA = {
    "Aries": {
        "Personality": "You are a pioneer and a trailblazer. Your energy is infectious, and you rarely back down from a challenge. You value honesty and directness above all else.",
        "Career": "You thrive in leadership roles or entrepreneurship. You dislike being micromanaged. Best fields: Sports, Management, Military, or Startups.",
        "Health": "You are prone to headaches and stress-related tension. Remember to slow down and hydrate. High-intensity cardio works best for you.",
        "Future": "The coming year brings a focus on partnerships. While you usually go it alone, 2026 will teach you the power of collaboration. Watch for a major career pivot in October."
    },
    "Taurus": {
        "Personality": "Grounded, reliable, and a lover of luxury. You are the anchor for your friends and family. You have immense patience but can be stubborn when pushed.",
        "Career": "You excel in roles that require consistency and an eye for aesthetics. Best fields: Finance, Art, Real Estate, or Culinary Arts.",
        "Health": "Throat and neck issues can be common. Watch your sugar intake, as you love indulgence. Yoga or pilates will help maintain flexibility.",
        "Future": "Financial stability is the theme for your next year. Investments made now will pay off. A long-dormant creative talent will re-emerge around spring."
    },
    "Gemini": {
        "Personality": "Curious, adaptable, and a master communicator. You can talk to anyone about anything. You have a dual nature that allows you to see both sides of every argument.",
        "Career": "You need variety and mental stimulation. Routine is your enemy. Best fields: Journalism, Sales, Marketing, or Teaching.",
        "Health": "Your nervous system is sensitive. Anxiety can manifest physically. Prioritize sleep and try meditation to quiet your active mind.",
        "Future": "Your social circle will expand rapidly this year. Networking will bring a golden opportunity. Be careful not to scatter your energy on too many projects at once."
    },
    "Cancer": {
        "Personality": "Intuitive, nurturing, and deeply emotional. You protect your loved ones fiercely. You are guided by the moon and your moods can shift like the tides.",
        "Career": "You do well in roles where you can care for others or manage resources. Best fields: Healthcare, Human Resources, Social Work, or Hospitality.",
        "Health": "Stomach and digestive issues are your weak spot, often linked to emotional stress. Comfort food is okay, but balance it with greens.",
        "Future": "This is a year of home and foundation. You might move house or renovate. An old family issue will finally be resolved, bringing you peace."
    },
    "Leo": {
        "Personality": "Charismatic, bold, and warm-hearted. You were born to shine. You are generous to a fault and expect loyalty in return.",
        "Career": "You need to be seen and appreciated. You are a natural leader or performer. Best fields: Entertainment, Politics, CEO, or Public Relations.",
        "Health": "Heart health and upper back strength are key for you. Keep your spine strong. Avoid burnout from trying to do too much.",
        "Future": "Your creative spark is igniting. A hobby could turn into a lucrative side hustle this year. Romance is also highlighted—expect passion."
    },
    "Virgo": {
        "Personality": "Analytical, practical, and detail-oriented. You see the flaws that others miss and you strive for perfection. You are the helper of the zodiac.",
        "Career": "You excel where precision is required. You organize the chaos. Best fields: Data Analysis, Editing, Medicine, or Accounting.",
        "Health": "Digestive health and nervous tension are issues. You tend to worry yourself sick. Herbal teas and routine are your best medicine.",
        "Future": "A year of skill-building. You may go back to school or take a major certification. Your disciplined approach will attract a mentor who opens doors."
    },
    "Libra": {
        "Personality": "Diplomatic, charming, and fair-minded. You seek balance and harmony in all things. You hate conflict and will go to great lengths to keep the peace.",
        "Career": "You make an excellent mediator or designer. You have a great eye for beauty. Best fields: Law, Fashion, Design, or Diplomacy.",
        "Health": "Kidneys and lower back need attention. Drink plenty of water. Balance your social life with alone time to recharge.",
        "Future": "Relationships take center stage. If single, a significant partner may appear. If attached, the relationship will deepen. A legal matter will resolve in your favor."
    },
    "Scorpio": {
        "Personality": "Intense, passionate, and secretive. You feel things deeply and have a powerful presence. You are excellent at uncovering the truth.",
        "Career": "You love solving mysteries or dealing with crisis. Best fields: Psychology, Investigation, Research, or Surgery.",
        "Health": "Reproductive health and emotional detoxing are important. Physical activity is crucial to release your intense pent-up energy.",
        "Future": "A year of transformation. You will shed an old identity or habit that no longer serves you. Financially, look out for shared resources or inheritances."
    },
    "Sagittarius": {
        "Personality": "Optimistic, adventurous, and philosophical. You are a seeker of truth and freedom. You are blunt but usually hilarious.",
        "Career": "You need freedom and travel. You are a lifelong learner. Best fields: Travel, Higher Education, Publishing, or Law.",
        "Health": "Hips and thighs are your area. You are generally robust but can be accident-prone due to rushing. Outdoor sports are essential for you.",
        "Future": "Your horizons are broadening. International travel or working with foreign cultures is likely. Your optimism will help you overcome a minor hurdle in mid-year."
    },
    "Capricorn": {
        "Personality": "Disciplined, ambitious, and practical. You play the long game. You are often the most mature person in the room and value tradition.",
        "Career": "You are the boss. You build structures and manage large responsibilities. Best fields: Government, Banking, Architecture, or Administration.",
        "Health": "Knees, bones, and teeth need care. Ensure you get enough Calcium. Don't let work stress stiffen your joints—stretch daily.",
        "Future": "Career culmination. All your hard work is about to be recognized. A promotion or award is likely. Just remember to balance this success with family time."
    },
    "Aquarius": {
        "Personality": "Innovative, independent, and humanitarian. You march to the beat of your own drum. You care about the collective more than the individual.",
        "Career": "You need to work on the future. You love technology and social causes. Best fields: Tech, Science, Aviation, or Non-profit work.",
        "Health": "Circulation and ankles are your weak points. Keep moving to keep the blood flowing. You need mental breaks to disconnect from the world's problems.",
        "Future": "A year of community. You will find your 'tribe' this year—a group of people who share your weirdest interests. A tech idea you have could gain traction."
    },
    "Pisces": {
        "Personality": "Dreamy, empathetic, and artistic. You are a spiritual soul who absorbs the emotions of others. You have a vivid imagination.",
        "Career": "You need creative flow and emotional connection. The corporate grind drains you. Best fields: Music, Photography, Healing, or Charity.",
        "Health": "Feet and immune system. You are sensitive to substances, so be careful with alcohol or caffeine. Swimming is your best exercise.",
        "Future": "Spiritual growth is massive this year. Your intuition will be sharper than ever. Trust your gut over logic in a major decision coming up in the summer."
    }
}

# --- 3. LOGIC FUNCTIONS ---
def get_zodiac_sign(day, month):
    if (month == 12 and day >= 22) or (month == 1 and day <= 19): return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18): return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20): return "Pisces"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19): return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20): return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20): return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22): return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22): return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22): return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22): return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21): return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21): return "Sagittarius"
    return "Unknown"

# --- 4. PDF GENERATION FUNCTION ---
def create_pdf(name, sign, data):
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'Starlight Oracle Report', 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title Info
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Prepared for: {name}", 0, 1)
    pdf.cell(0, 10, f"Sun Sign: {sign}", 0, 1)
    pdf.ln(5)
    
    # Body Content
    categories = ["Personality", "Career", "Health", "Future"]
    
    for category in categories:
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(100, 100, 255) # Light Blue Header
        pdf.cell(0, 10, category.upper(), 0, 1)
        
        pdf.set_font("Arial", size=11)
        pdf.set_text_color(0, 0, 0) # Black text
        # MultiCell allows text to wrap to the next line automatically
        text_content = data.get(category, "N/A")
        pdf.multi_cell(0, 7, text_content)
        pdf.ln(5)
        
    return pdf.output(dest='S').encode('latin-1')

# --- 5. THE APP INTERFACE ---
def main():
    st.set_page_config(page_title="Starlight Oracle", page_icon="🌙", layout="wide")

    # --- COSMIC STYLING (CSS) ---
    # This block injects CSS to create the starry background and style the text
    st.markdown("""
    <style>
    /* Main Background Image */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1534796636912-3b95b3ab5980?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=3600");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Content Box Styling - Semi-transparent white */
    .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 3rem !important;
        margin-top: 2rem;
    }

    /* Header Text Styling */
    h1, h2, h3 {
        color: #2E004F !important; /* Deep Purple */
    }
    
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

    with st.sidebar:
        st.header("Enter Your Details")
        st.write("The stars are ready to speak...")
        name = st.text_input("First Name")
        dob = st.date_input("Date of Birth", min_value=datetime.date(1940, 1, 1))
        generate_btn = st.button("Generate Detailed Report ✨")

    if generate_btn and name:
        sign = get_zodiac_sign(dob.day, dob.month)
        symbol = ZODIAC_SYMBOLS.get(sign, "")
        
        # Progress Bar Animation
        progress_text = "Consulting the stars..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        my_bar.empty()

        report = ASTRO_DATA.get(sign, {})

        # --- DISPLAY RESULTS WITH SYMBOLS ---
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

        # --- PDF DOWNLOAD BUTTON ---
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
