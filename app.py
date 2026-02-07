import streamlit as st
import datetime

# --- 1. Helper Function: Determine Zodiac Sign ---
def get_zodiac_sign(day, month):
    # Simple logic to determine sign based on date
    if (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Pisces"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    else:
        return "Unknown"

# --- 2. Helper Function: Get a Reading ---
def get_reading(sign):
    # In a real app, this might pull from a database of your writings
    readings = {
        "Fire": "Energy is high today! Take action on your goals.",
        "Water": "Trust your intuition. Emotions may be strong.",
        "Air": "Communication is key. Reach out to an old friend.",
        "Earth": "Stay grounded. Focus on practical matters today."
    }
    
    # Assign elements to signs for simple readings
    fire_signs = ["Aries", "Leo", "Sagittarius"]
    water_signs = ["Cancer", "Scorpio", "Pisces"]
    air_signs = ["Gemini", "Libra", "Aquarius"]
    earth_signs = ["Taurus", "Virgo", "Capricorn"]

    if sign in fire_signs:
        return readings["Fire"]
    elif sign in water_signs:
        return readings["Water"]
    elif sign in air_signs:
        return readings["Air"]
    elif sign in earth_signs:
        return readings["Earth"]
    else:
        return " The stars are cloudy. Please check your date."

# --- 3. The App Layout ---
def main():
    # Set the page title and icon
    st.set_page_config(page_title="Celestial Insights", page_icon="✨")

    # Title and Introduction
    st.title("✨ Celestial Insights")
    st.write("Welcome to your personalized astrology portal.")
    st.write("---")

    # User Input Section
    st.sidebar.header("Enter Your Details")
    name = st.sidebar.text_input("What is your name?")
    dob = st.sidebar.date_input("Date of Birth", min_value=datetime.date(1920, 1, 1))

    # Button to Generate Reading
    if st.sidebar.button("Reveal My Destiny"):
        if name:
            # Calculate Data
            sign = get_zodiac_sign(dob.day, dob.month)
            reading = get_reading(sign)

            # Display Results
            st.header(f"Hello, {name}!")
            st.subheader(f"Your Sun Sign is: **{sign}**")
            
            # Show a decorative box with the reading
            st.info(f"🔮 **Today's Reading:** {reading}")
            
            st.success("Would you like a deeper reading? Contact us to book a full chart session!")
        else:
            st.warning("Please enter your name to begin.")

# Run the app
if __name__ == "__main__":
    main()