import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import re

# Previous dictionaries remain the same
PURPOSE_OPTIONS = {
    'general': 'General',
    'stability': 'Stability',
    'growth': 'Growth',
    'educational': 'Educational',
    'financial': 'Financial',
    'business': 'Business',
    'concentration': 'Concentration',
    'gealth_wealth': 'Health & Wealth',
    'success_real_state': 'Success in Real Estate',
    'love_affection': 'Love & Affection',
    'creativity': 'Creativity',
    'wealth_prosperity': 'Wealth & Prosperity',
    'respect': 'Respect',
    'mental_health': 'Mental Health',
    'luxury': 'Luxury',
    'love_relationship': 'Love & Relationship',
    'pregnancy_delay': 'Pregnancy Delay',
    'decision_making': 'Decision Making',
    'legal_matters': 'Legal Matters',
    'overthinking': 'Overthinking'
}

SUGGESTION_TYPES = {
    'moon': 'Moon Based',
    'manifest': 'Manifest Based'
}

def is_valid_time(time_str):
    """Validate time string in 24-hour format (HH:MM)"""
    pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
    return bool(pattern.match(time_str))

def is_valid_email(email):
    """Validate email format"""
    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(pattern.match(email))

def is_valid_mobile(mobile):
    """Validate mobile number (10 digits)"""
    pattern = r"""
        ^[98765]                           # Starts with 9, 8, 7, 6, or 5
        (?!.*(\d)\1{4})                    # No digit repeated more than 4 times consecutively
        (?!.*012345)                       # Does not contain pattern 012345
        (?!.*543210)                       # Does not contain pattern 543210
        (?!.*653210)                       # Does not contain pattern 653210
        (?!.*0123456)                      # Does not contain pattern 0123456
        (?!.*9876543210)                   # Does not contain pattern 9876543210
        \d{9}$                             # Followed by 9 digits (10 digits total)
    """

    # Match the pattern with the phone number
    # if re.fullmatch(pattern, mobile, re.VERBOSE):
    # pattern = re.compile(r'^[6-9]\d{9}$')
    return bool(re.fullmatch(pattern, mobile, re.VERBOSE))

def format_date(date):
    """Convert date to required format YYYY/MM/DD"""
    return date.strftime('%Y/%m/%d')

def format_time(time_str):
    """Return the time string as is since it's already in HH:MM format"""
    return time_str

def create_card_html(name, image_url, info, product_url):
    # Previous card HTML creation function remains the same
    return f"""
        <div style="
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            margin: 10px;
            text-align: center;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <div>
                <h3 style="color: #1f77b4; margin-bottom: 10px;">{name}</h3>
                <img src="{image_url}" style="
                    max-width: 200px;
                    height: auto;
                    border-radius: 4px;
                    margin: 10px 0;
                ">
                <p style="color: #666;"></p>
            </div>
            <div style="margin-top: 10px;">
                <a href="{product_url}" target="_blank" style="
                    display: inline-block;
                    padding: 8px 16px;
                    background-color: #1f77b4;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    transition: background-color 0.3s;
                ">View Product</a>
            </div>
        </div>
    """

def call_rudraksha_api(date, time, name, purpose, suggestion_type, email, mobile):
    """Call the Rudraksha recommendation API"""
    base_url = "https://api.astroarunpandit.org/get-recommended-rudraksha"
    
    formatted_date = format_date(date)
    encoded_name = requests.utils.quote(name)
    
    # Build URL with all parameters
    url = f"{base_url}?date={formatted_date}&name={encoded_name}&chart_type={suggestion_type}&email={email}&mobile={mobile}"
    
    if time:
        formatted_time = format_time(time)
        url += f"&time={formatted_time}"
        
    if purpose != 'general':
        url += f"&purpose={purpose}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    

def fetch_country_data():
    """Fetch country data from GitHub"""
    url = "https://raw.githubusercontent.com/vivekjustthink/Country-Code-And-Details/master/country_code_and_details.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        countries = response.json()
        # print(countries)
        
        # Format country data for dropdown: "THREE_LETTER_CODE (+code)"
        formatted_countries = [
            {
                'label': f"{country['country_code']} (+{country['phone_code']})",
                'value': country['phone_code']
            }
            for country in countries
        ]
        
        # Sort by three letter country code
        formatted_countries.sort(key=lambda x: x['label'])
        
        # Find India's index for default selection (IND)
        default_index = next(
            (i for i, c in enumerate(formatted_countries) 
             if 'IND' in c['label']),
            0
        )
        
        return formatted_countries, default_index
    except Exception as e:
        st.error(f"Error fetching country data: {str(e)}")
        return [], 0

def main():
    st.title("Rudraksha Recommendation API Tester")

    # Fetch country data
    country_list, default_country_index = fetch_country_data()
    
    # Custom CSS
    st.markdown("""
        <style>
        .stSelectbox {
            margin-bottom: 1rem;
        }
        .stTable {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .invalid-feedback {
            color: red;
            font-size: 0.8em;
            margin-top: -15px;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Input fields in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        suggestion_type = st.selectbox(
            "Select Suggestion Type",
            options=list(SUGGESTION_TYPES.keys()),
            format_func=lambda x: SUGGESTION_TYPES[x],
            index=0
        )
        
        # Time input section with checkbox
        unknown_time = st.checkbox("I don't know the birth time")
        time_input = None
        if not unknown_time:
            time_input = st.text_input(
                "Enter Time (24-hour format HH:MM)", 
                "12:05",
                help="Enter time in 24-hour format (e.g., 13:30 for 1:30 PM)"
            )
        
        # Email input with validation
        email = st.text_input(
            "Enter Email",
            placeholder="example@email.com",
            help="Enter a valid email address"
        )
        if email and not is_valid_email(email):
            st.markdown('<p class="invalid-feedback">Please enter a valid email address</p>', unsafe_allow_html=True)

        # Purpose dropdown
        purpose_display_name = st.selectbox(
            "Select Purpose",
            options=list(PURPOSE_OPTIONS.keys()),
            format_func=lambda x: PURPOSE_OPTIONS[x],
            index=0
        )
        
    with col2:
        date = st.date_input("Select Date", datetime(1999, 8, 1))
        name = st.text_input("Enter Name", "Dev Gupta")
        
        # Mobile input with validation
        mobile_col1, mobile_col2 = st.columns([1, 2])
        with mobile_col1:
            country_code = st.selectbox(
                "Country Code",
                options=[c['label'] for c in country_list],
                index=default_country_index,
                key="country_code"
            )
        with mobile_col2:
            mobile = st.text_input(
                "Enter Mobile Number",
                placeholder="10-digit mobile number",
                help="Enter a valid 10-digit mobile number starting with 6-9"
            )

        # Get selected country code
        selected_code = next(
            (c['value'] for c in country_list 
             if c['label'] == country_code),
            '91'
        )
        if mobile and not is_valid_mobile(mobile):
            st.markdown('<p class="invalid-feedback">Please enter a valid 10-digit mobile number</p>', unsafe_allow_html=True)
    
    # Validate all inputs before enabling the submit button
    is_valid_inputs = (
        name and 
        (not time_input or is_valid_time(time_input)) and
        is_valid_email(email) if email else False and
        is_valid_mobile(mobile) if mobile else False
    )
    
    if not is_valid_inputs:
        st.warning("Please fill all required fields with valid information")
        
    if st.button("Get Recommendation", disabled=not is_valid_inputs):
        with st.spinner("Fetching recommendation..."):
            result = call_rudraksha_api(
                date, 
                None if unknown_time else time_input, 
                name, 
                purpose_display_name,
                suggestion_type,
                email,
                mobile
            )
            
            if 'error' not in result:
                # Display selected options
                if unknown_time:
                    st.info(f"Suggestion Type: {SUGGESTION_TYPES[suggestion_type]} | Purpose: {PURPOSE_OPTIONS[purpose_display_name]} | Time: Not Provided")
                else:
                    st.info(f"Suggestion Type: {SUGGESTION_TYPES[suggestion_type]} | Purpose: {PURPOSE_OPTIONS[purpose_display_name]} | Time: {time_input}")
                
                # Display Rudraksha Recommendations
                st.subheader("Recommended Rudrakshas")
                
                # Create 3-column layout for cards
                cols = st.columns(3)
                for i, rudraksha in enumerate(result['result']):
                    with cols[i % 3]:
                        st.markdown(create_card_html(
                            rudraksha['name'],
                            rudraksha['image'],
                            rudraksha['info'],
                            rudraksha['url']
                        ), unsafe_allow_html=True)
            else:
                st.error(f"Error fetching data: {result['error']}")

if __name__ == "__main__":
    main()