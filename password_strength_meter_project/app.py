import re
import streamlit as st
import secrets
import string

# -------------------------------
# Page styling and custom CSS
# -------------------------------
st.set_page_config(page_title="Password_Strength_Meter_By_Muqaddas", page_icon="🌘", layout="centered")

# Custom CSS for UI styling
st.markdown("""
<style>
    /* Center the main content area */
    .main {text-align: center;}
    
   /* Center the password input box horizontally */
    .stTextInput > div > div {margin: auto !important;}
    
    /* Center the label for the password input */
    label[for="password_input"] {
        display: flex;
        justify-content: center !important;
        width: 100%;
    }
    
    /* Center the text inside the password input box */
    .stTextInput input {text-align: center;}
    
    /* Style all Streamlit buttons: full width, background color, text color, and font size */
    .stButton button {
        width: 100%; /* Make buttons full width of their container */
        background-color: rgb(180, 238, 230); /* Button background */
        color: black; /* Button text color */
        font-size: 18px; /* Button text size */
    }
    
    /* Change button background on hover */
    .stButton button:hover {
        background-color: rgb(238, 243, 243);
    }
    
    /* Center items in password container and add spacing between them */
    .password-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px; /* Space between items */
    }
    
    /* Style the strength meter bar */
    .strength-meter {
        height: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    /* Style for each password requirement item (icon + text) */
    .requirement-item {
        display: flex;
        align-items: center;
        gap: 5px;
        margin: 5px 0;
    }
    
    /* Style for the copy password button */
    .copy-button {
        background-color: #2196F3;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        cursor: pointer;
    }
    
    /* Change copy button color on hover */
    .copy-button:hover {
        background-color: #1976D2;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Page title and description
# -------------------------------
st.title("🔐 Password Strength Meter")
st.write("Check and improve your password security level. 🔍")

# -------------------------------
# Function to generate a strong password
# -------------------------------
def generate_strong_password(length=10):
    """Generate a strong password with mixed characters"""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))

# -------------------------------
# Function to check password strength
# -------------------------------
def check_password_strength(password):
    score = 0
    feedback = []
    requirements = {
        "length": {"met": False, "message": "At least 8 characters"},
        "uppercase": {"met": False, "message": "At least one uppercase letter"},
        "lowercase": {"met": False, "message": "At least one lowercase letter"},
        "number": {"met": False, "message": "At least one number"},
        "special": {"met": False, "message": "At least one special character"}
    }
    
    # Length Check
    if len(password) >= 8:
        score += 1
        requirements["length"]["met"] = True
    else:
        feedback.append("❌ Password should be *at least 8 characters long*.")
    
    # Uppercase Check
    if re.search(r"[A-Z]", password):
        score += 1
        requirements["uppercase"]["met"] = True
    # Lowercase Check
    if re.search(r"[a-z]", password):
        score += 1
        requirements["lowercase"]["met"] = True
    # Digit Check
    if re.search(r"\d", password):
        score += 1
        requirements["number"]["met"] = True
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
        requirements["special"]["met"] = True
    
    return score, feedback, requirements

# -------------------------------
# Session State for Password
# -------------------------------
if 'password' not in st.session_state:
    st.session_state.password = ""
if 'generated_password' not in st.session_state:
    st.session_state.generated_password = ""

# -------------------------------
# Password Input Box
# -------------------------------
password = st.text_input(
    "Enter your password:",
    type="password",
    value=st.session_state.generated_password or st.session_state.password,
    key="password_input",
    help="Ensure your password is strong 🔐"
)
st.session_state.password = password

# -------------------------------
# Generate Password Button
# -------------------------------
if st.button("🎲 Generate Strong Password"):
    generated_password = generate_strong_password()
    st.session_state.generated_password = generated_password
    st.session_state.password = generated_password
    st.rerun()  # Refresh to show generated password in input

# -------------------------------
# Display Generated Password
# -------------------------------
if st.session_state.generated_password:
    st.info(f"Generated Password: {st.session_state.generated_password}")
    st.code(st.session_state.generated_password)

# -------------------------------
# Check Password Strength Button and Output
# -------------------------------
if st.button("Check Strength"):
    if password:
        score, feedback, requirements = check_password_strength(password)
        strength_colors = {
            0: "#ff0000",  # Red
            1: "#ff4d4d",  # Light Red
            2: "#ffa64d",  # Orange
            3: "#ffff4d",  # Yellow
            4: "#4dff4d",  # Light Green
            5: "#00ff00"   # Green
        }
        # Strength meter bar (color and width based on score)
        st.markdown(f"""
        <div style="background-color: {strength_colors[score]}; width: {max(score,1) * 20}%;"
        class="strength-meter"></div>
        """, unsafe_allow_html=True)
        # Strength rating message
        if score == 5:
            st.success("✅ Very Strong Password!")
        elif score == 4:
            st.success("✅ Strong Password!")
        elif score == 3:
            st.info("⚠ Moderate Password - Consider adding more security features.")
        else:
            st.error("❌ Weak Password - Improve it using the suggestions below.")
        # Password requirements checklist
        st.subheader("Password Requirements:")
        for req, status in requirements.items():
            icon = "✅" if status["met"] else "❌"
            st.markdown(f"- {icon} {status['message']}")
        # Feedback for improvement
        if feedback:
            with st.expander("🔍 Improve your password"):
                for item in feedback:
                    st.write(item)
    else:
        st.warning("⚠ Please enter a password first!")