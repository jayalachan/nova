import streamlit as st
import datetime
import json
import os
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.markdown("""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-MN6GLP579Q"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-MN6GLP579Q');
</script>
""", unsafe_allow_html=True)


# -----------------------------
# EMAIL CONFIGURATION
# -----------------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = st.secrets["email"]["address"]
SMTP_PASSWORD = st.secrets["email"]["password"]

def send_confirmation_email(to_email, user_name, application_id, application_data):
    """Sends personalized confirmation email to user"""
    try:
        # Generate personalized message based on interests
        personalized_message = ""
        interests = application_data.get('interests', [])
        income = application_data.get('monthly_income', 0)
        hobbies = application_data.get('hobbies', '').lower()
        
        # Personalization by interests
        if "E-learning" in interests or "education" in hobbies or "learning" in hobbies:
            personalized_message += "<li>🎓 <strong>Education Benefit:</strong> As a learning enthusiast, you'll get 20% off on Coursera, Udemy, and Platzi with your NovaCard.</li>"
        
        if "Streaming" in interests or "movies" in hobbies or "series" in hobbies or "music" in hobbies:
            personalized_message += "<li>🎬 <strong>Premium Entertainment:</strong> Enjoy 3 months free of Netflix or Spotify Premium when you activate your card.</li>"
        
        if "Travel" in interests or "traveling" in hobbies or "tourism" in hobbies:
            personalized_message += "<li>✈️ <strong>Frequent Traveler:</strong> Accumulate miles on every purchase and access VIP lounges at selected airports.</li>"
        
        if "Technology" in interests or "Gaming" in interests or "tech" in hobbies or "gaming" in hobbies:
            personalized_message += "<li>💻 <strong>Tech Lover:</strong> Exclusive discounts at tech and gaming stores, plus 5% cashback on digital purchases.</li>"
        
        if "Food" in interests or "food" in hobbies or "cooking" in hobbies:
            personalized_message += "<li>🍕 <strong>Foodie Benefits:</strong> 2x1 at partner restaurants and 10% off on delivery apps.</li>"
        
        if "Sports" in interests or "gym" in hobbies or "sport" in hobbies or "fitness" in hobbies:
            personalized_message += "<li>💪 <strong>Active Life:</strong> Discounts at gyms, sports equipment, and premium fitness apps.</li>"
        
        # Personalization by income
        if income >= 1500:
            personalized_message += "<li>💎 <strong>Premium Profile:</strong> Based on your income level, you qualify for a high credit limit and exclusive VIP benefits.</li>"
        
        # If no specific interests
        if not personalized_message:
            personalized_message = "<li>🎁 <strong>General Benefits:</strong> Enjoy 3% cashback on all your purchases and access to exclusive promotions.</li>"
        
        msg = MIMEMultipart('alternative')
        msg['From'] = SMTP_EMAIL
        msg['To'] = to_email
        msg['Subject'] = f'✅ NovaCard - Application #{application_id} Received'
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #2E86C1; text-align: center;">💳 NovaCard</h2>
                    <h3>Hello {user_name}! 🎉</h3>
                    
                    <p>We have successfully received your NovaCard application.</p>
                    
                    <div style="background-color: #f0f8ff; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <p><strong>Application Number:</strong> #{application_id}</p>
                        <p><strong>Date:</strong> {datetime.datetime.now().strftime("%m/%d/%Y %H:%M")}</p>
                    </div>
                    
                    <h4>🎯 Personalized Benefits for You:</h4>
                    <ul style="background-color: #f9f9f9; padding: 20px; border-radius: 8px; border-left: 4px solid #2E86C1;">
                        {personalized_message}
                    </ul>
                    
                    <h4>📋 Next Steps:</h4>
                    <ol>
                        <li>We'll review your information within the next 24-48 hours</li>
                        <li>We'll contact you to verify some details</li>
                        <li>You'll receive the decision via email and SMS</li>
                    </ol>
                    
                    <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 0.9em; color: #666;">
                        <strong>Contact:</strong><br>
                        📧 info@novacard.com<br>
                        📱 +593 99 123 4567
                    </p>
                    
                    <p style="font-size: 0.8em; color: #999; text-align: center; margin-top: 20px;">
                        This is a demo project for educational purposes.
                    </p>
                </div>
            </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")
        return False

def send_admin_notification(application_data):
    """Sends notification to admin about new application"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = SMTP_EMAIL
        msg['To'] = SMTP_EMAIL
        msg['Subject'] = f'🔔 New NovaCard Application #{application_data["id"]}'
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #2E86C1;">🔔 New Application Received</h2>
                    
                    <h3>Applicant Information:</h3>
                    <ul>
                        <li><strong>Name:</strong> {application_data['full_name']}</li>
                        <li><strong>ID Number:</strong> {application_data['id_number']}</li>
                        <li><strong>Email:</strong> {application_data['email']}</li>
                        <li><strong>Phone:</strong> {application_data['phone']}</li>
                        <li><strong>Age:</strong> {application_data['age']} years</li>
                        <li><strong>Income:</strong> ${application_data['monthly_income']}</li>
                        <li><strong>Occupation:</strong> {application_data.get('occupation', 'N/A')}</li>
                    </ul>
                    
                    <h4>Interests:</h4>
                    <p>{', '.join(application_data.get('interests', [])) if application_data.get('interests') else 'Not specified'}</p>
                    
                    <p style="margin-top: 20px; padding: 10px; background-color: #f0f8ff; border-radius: 5px;">
                        <strong>Application date:</strong> {application_data['application_date']}
                    </p>
                </div>
            </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        st.error(f"Error sending admin notification: {str(e)}")
        return False

# -----------------------------
# DATA SAVING FUNCTIONS
# -----------------------------
def get_applications_file():
    """Gets the JSON file path"""
    return Path("applications.json")

def load_applications():
    """Loads existing applications from JSON file"""
    file_path = get_applications_file()
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_application(application_data):
    """Saves a new application to JSON file"""
    applications = load_applications()
    
    # Add timestamp and unique ID
    application_data['id'] = len(applications) + 1
    application_data['application_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    applications.append(application_data)
    
    file_path = get_applications_file()
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(applications, f, indent=4, ensure_ascii=False)
    
    return application_data['id']

# -----------------------------
# APP CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="NovaCard – Digital Card",
    page_icon="💳",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def initialize_session_state():
    """Initializes session variables"""
    if 'application_submitted' not in st.session_state:
        st.session_state.application_submitted = False
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    if 'application_id' not in st.session_state:
        st.session_state.application_id = None

# Initialize state
initialize_session_state()

# -----------------------------
# CUSTOM STYLING
# -----------------------------
st.markdown(
    """
    <style>
        .main-title { 
            font-size: 2.8rem; 
            font-weight: bold; 
            color: #2E86C1; 
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle { 
            font-size: 1.3rem; 
            color: #566573; 
            text-align: center; 
            margin-bottom: 40px;
        }
        .footer { 
            font-size: 0.85rem; 
            color: #7f8c8d; 
            text-align: center; 
            margin-top: 60px;
            padding: 20px;
            border-top: 1px solid #ecf0f1;
        }
        .stButton>button { 
            background-color: #2E86C1; 
            color: white; 
            border-radius: 8px;
            font-weight: 600;
            padding: 0.5rem 2rem;
            transition: all 0.3s;
        }
        .stButton>button:hover { 
            background-color: #1F618D;
            transform: translateY(-2px);
        }
        .benefit-card {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 4px solid #2E86C1;
        }
        .metric-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 10px 0;
        }
        .success-message {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .warning-box {
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
            color: #856404;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# ENHANCED SIDEBAR
# -----------------------------
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/2E86C1/FFFFFF?text=NovaCard", use_container_width=True)
    st.markdown("---")
    menu = st.radio(
        "🧭 Navigation",
        ["🏠 Home", "✨ Benefits", "📝 Apply", "📊 Applications", "❓ FAQ"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Show application counter
    total_applications = len(load_applications())
    st.metric("📋 Total Applications", total_applications)
    
    st.markdown("---")
    st.markdown("### 📞 Contact")
    st.markdown("📧 info@novacard.com")
    st.markdown("📱 +593 99 123 4567")
    
    if st.session_state.application_submitted:
        st.success(f"✅ Application #{st.session_state.application_id}")

# -----------------------------
# HOME
# -----------------------------
if menu == "🏠 Home":
    st.markdown("<div class='main-title'>💳 NovaCard</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>The digital card designed for your lifestyle</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            "<div class='metric-container'><h3>100%</h3><p>Digital</p></div>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            "<div class='metric-container'><h3>24/7</h3><p>Support</p></div>",
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            "<div class='metric-container'><h3>5min</h3><p>Approval</p></div>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    
    st.markdown("### 🎯 What is NovaCard?")
    st.write("""
    NovaCard is more than a credit card: it's your digital financial companion. 
    Specifically designed for young professionals between **25 and 35 years old**, 
    it offers:
    
    - 🚀 **100% online process** - No paperwork or branch visits
    - 🎁 **Smart rewards** - Earn points for responsible spending
    - 🔐 **Latest generation security** - Your money always protected
    - 🌟 **Exclusive benefits** - On the platforms you use most
    """)

    st.info("💡 **Ready to take the next step?** Visit the 'Apply' section and complete your application in less than 5 minutes.")

# -----------------------------
# BENEFITS
# -----------------------------
elif menu == "✨ Benefits x":
    st.header("✨ Exclusive Benefits")
    
    tab1, tab2, tab3 = st.tabs(["🎁 Rewards", "🛡️ Security", "📋 Requirements"])
    
    with tab1:
        st.markdown("### NovaPoints Rewards System")
        
        benefits = [
            ("💳", "Cashback", "Up to 3% on your daily purchases"),
            ("📚", "E-Learning", "20% discount on Coursera, Udemy and Platzi"),
            ("🎬", "Streaming", "3 months free of Netflix or Spotify Premium"),
            ("🚲", "Mobility", "15% off on Uber, Cabify and scooter apps"),
            ("✈️", "Travel", "Accumulate miles on every international purchase"),
            ("🍕", "Dining", "2x1 at selected restaurants")
        ]
        
        for icon, title, desc in benefits:
            st.markdown(
                f"""
                <div class='benefit-card'>
                    <h4>{icon} {title}</h4>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    with tab2:
        st.markdown("### 🛡️ Your Security is Our Priority")
        st.write("""
        - 🔐 **Bank-level encryption** - Your data protected with cutting-edge technology
        - 📱 **Real-time alerts** - Instant notifications for every transaction
        - 🚫 **Immediate blocking** - Freeze your card from the app in seconds
        - 💰 **Fraud protection** - 24/7 monitoring of suspicious activities
        - 🔄 **Secure online shopping** - Temporary virtual cards for internet purchases
        """)
        
        st.warning("🔔 If you detect any suspicious activity, you can block your card immediately from the app.")
    
    with tab3:
        st.markdown("### 📋 Application Requirements")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            #### ✅ Basic Requirements
            - Age: 25-70 years
            - Income: Minimum $800/month
            - Residence in Ecuador
            - Valid ID card
            """)
        
        with col2:
            st.markdown("""
            #### 📄 Documentation
            - ID card
            - Proof of income
            - Active email
            - Phone number
            """)
        
        st.success("💡 **Ideal Profile:** Young professionals with digital lifestyle, stable income and good credit history.")

# -----------------------------
# APPLICATION FORM
# -----------------------------
elif menu == "📝 Apply":
    st.header("📝 Apply for your NovaCard")
    
    if st.session_state.application_submitted:
        st.markdown(
            f"""
            <div class='success-message'>
                <h3>🎉 Application Received, {st.session_state.user_name}!</h3>
                <p><strong>Application Number: #{st.session_state.application_id}</strong></p>
                <p>We have successfully received your application. We'll contact you within the next 24-48 hours.</p>
                <p><strong>Next steps:</strong></p>
                <ul>
                    <li>✅ You'll receive a confirmation email</li>
                    <li>📋 We'll review your information</li>
                    <li>📧 You'll be notified of the decision via email and SMS</li>
                </ul>
                <p style='margin-top: 15px;'>📧 <strong>Check your inbox</strong> (including spam) for the confirmation email.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("📝 Submit another application"):
            st.session_state.application_submitted = False
            st.rerun()
    else:
        st.write("Complete the form to apply for your card. The process takes less than 5 minutes.")
        
        with st.form("application_form", clear_on_submit=True):
            st.subheader("📋 Personal Information")
            
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name *", placeholder="John Doe")
            with col2:
                id_number = st.text_input("ID Number *", placeholder="1234567890")
            
            col3, col4 = st.columns(2)
            with col3:
                email = st.text_input("Email *", placeholder="john@email.com")
            with col4:
                phone = st.text_input("Phone Number *", placeholder="0991234567")
            
            st.subheader("💼 Financial Information")
            
            col5, col6 = st.columns(2)
            with col5:
                age = st.number_input("Age *", min_value=18, max_value=70, value=25, step=1)
            with col6:
                income = st.number_input("Monthly Income (USD) *", min_value=0, value=800, step=100)
            
            occupation = st.text_input("Occupation", placeholder="e.g., Software Developer")
            
            st.subheader("🎯 Preferences")
            
            interests = st.multiselect(
                "Select your interests (optional)",
                ["E-learning", "Streaming", "Travel", "Food", "Sports", "Technology", "Music", "Gaming"]
            )
            
            hobbies = st.text_area("Tell us about your hobbies", placeholder="I love learning new technologies...")
            reason = st.text_area("Why do you want a NovaCard?", placeholder="I'm looking for a card that fits my digital lifestyle...")
            
            st.markdown("---")
            
            terms = st.checkbox("I accept the terms and conditions *")
            privacy = st.checkbox("I accept the privacy policy and data processing *")
            
            st.caption("* Required fields")
            
            submitted = st.form_submit_button("🚀 Submit Application", use_container_width=True)
            
            if submitted:
                # Basic validation
                if not full_name or not id_number or not email or not phone:
                    st.error("⚠️ Please complete all required fields.")
                elif not terms or not privacy:
                    st.error("⚠️ You must accept the terms and conditions and privacy policy.")
                else:
                    # Prepare data to save
                    application_data = {
                        "full_name": full_name,
                        "id_number": id_number,
                        "email": email,
                        "phone": phone,
                        "age": age,
                        "monthly_income": income,
                        "occupation": occupation,
                        "interests": interests,
                        "hobbies": hobbies,
                        "reason": reason,
                        "accept_terms": terms,
                        "accept_privacy": privacy
                    }
                    
                    # Save to JSON
                    application_id = save_application(application_data)
                    
                    # Update state
                    st.session_state.application_submitted = True
                    st.session_state.user_name = full_name
                    st.session_state.application_id = application_id
                    
                    # Processing simulation
                    with st.spinner("Processing your application..."):
                        import time
                        time.sleep(1)
                    
                    # Send emails
                    with st.spinner("📧 Sending confirmation email..."):
                        email_sent = send_confirmation_email(email, full_name, application_id, application_data)
                        if email_sent:
                            st.success("✅ Confirmation email sent!")
                        
                        # Notify admin
                        send_admin_notification(application_data)
                    
                    # Personalized messages based on interests
                    if "E-learning" in interests:
                        st.info("🎓 We detected your interest in education. NovaCard offers 20% discount on educational platforms.")
                    
                    if income >= 1500:
                        st.info("💎 Based on your income, you qualify for premium benefits. We'll contact you with a special offer.")
                    
                    st.rerun()


# -----------------------------
# FAQ
# -----------------------------
elif menu == "❓ FAQ":
    st.header("❓ Frequently Asked Questions")
    
    with st.expander("🕐 How long does approval take?"):
        st.write("The approval process is almost instant. In most cases, you'll receive a response in less than 24 hours.")
    
    with st.expander("💳 What is the credit limit?"):
        st.write("The credit limit is determined based on your financial profile. It generally ranges from $500 to $5,000 for new users.")
    
    with st.expander("💰 Are there maintenance fees?"):
        st.write("NovaCard does NOT charge maintenance fees for the first year. After that, you only pay if your monthly spending is less than $100.")
    
    with st.expander("🌍 Can I use it abroad?"):
        st.write("Yes! NovaCard works worldwide wherever Visa/Mastercard cards are accepted. No hidden fees.")
    
    with st.expander("📱 Do I need to install an app?"):
        st.write("Yes, the NovaCard app is available for iOS and Android. From there you control all aspects of your card.")
    
    with st.expander("🔒 What do I do if I lose my card?"):
        st.write("Block it immediately from the app or call us at +593 99 123 4567. Your money will always be protected.")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown(
    """
    <div class='footer'>
        <p>⚠️ <strong>Legal Notice:</strong> This site was created solely for demonstration and educational purposes.</p>
        <p>NovaCard does not represent a real financial institution nor does it conduct real financial operations.</p>
        <p style='margin-top: 15px;'>© 2025 NovaCard Demo. Built with Streamlit.</p>
    </div>
    """,
    unsafe_allow_html=True,
)