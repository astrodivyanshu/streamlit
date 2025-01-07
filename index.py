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
                <p style="color: #666;">Planet: {info}</p>
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

def call_rudraksha_api(date, time, name, purpose, suggestion_type):
    """Call the Rudraksha recommendation API"""
    base_url = "https://api.astroarunpandit.org/get-recommended-rudraksha"
    
    formatted_date = format_date(date)
    encoded_name = requests.utils.quote(name)
    
    # Build URL without time if not provided
    url = f"{base_url}?date={formatted_date}&name={encoded_name}&chart_type={suggestion_type}"
    
    # Add time parameter only if provided
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

def main():
    st.title("Rudraksha Recommendation API Tester")
    
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
    
    # Validate time format if time is provided
    if time_input and not unknown_time:
        if not is_valid_time(time_input):
            st.error("Please enter a valid time in 24-hour format (HH:MM)")
            return
        
    if st.button("Get Recommendation"):
        with st.spinner("Fetching recommendation..."):
            # Pass None as time if unknown_time is checked
            result = call_rudraksha_api(
                date, 
                None if unknown_time else time_input, 
                name, 
                purpose_display_name,
                suggestion_type
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