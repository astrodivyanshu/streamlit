import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# Purpose options with formatted display names
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

def format_date(date):
    """Convert date to required format YYYY/MM/DD"""
    return date.strftime('%Y/%m/%d')

def format_time(time):
    """Convert time to required format HH:MM"""
    return time.strftime('%H:%M')

def create_card_html(name, image_url, info, product_url):
    """Create HTML for a Rudraksha card"""
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

def call_rudraksha_api(date, time, name, purpose):
    """Call the Rudraksha recommendation API"""
    base_url = "https://api.astroarunpandit.org/get-recommended-rudraksha"
    
    formatted_date = format_date(date)
    formatted_time = format_time(time)
    encoded_name = requests.utils.quote(name)
    
    # Include purpose in the API call if it's not 'general'
    url = f"{base_url}?date={formatted_date}&time={formatted_time}&name={encoded_name}"
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
        name = st.text_input("Enter Name", "Dev Gupta")
        date = st.date_input("Select Date", datetime(1999, 8, 1))
        
    with col2:
        time = st.time_input("Select Time", datetime(2023, 1, 1, 12, 5).time())
        # Purpose dropdown with formatted display names
        purpose_display_name = st.selectbox(
            "Select Purpose",
            options=list(PURPOSE_OPTIONS.keys()),
            format_func=lambda x: PURPOSE_OPTIONS[x],
            index=0
        )
        
    if st.button("Get Recommendation"):
        with st.spinner("Fetching recommendation..."):
            result = call_rudraksha_api(date, time, name, purpose_display_name)
            
            if 'error' not in result:
                # Display selected purpose
                st.info(f"Selected Purpose: {PURPOSE_OPTIONS[purpose_display_name]}")
                
                # Display Moon Information
                st.subheader("Moon Details")
                moon_data = pd.DataFrame({
                    'Parameter': ['Nakshatra', 'Lord'],
                    'Value': [result['moon']['nakshatra'], result['moon']['lord']]
                })
                st.table(moon_data)
                
                # Display House Information
                st.subheader("House Details")
                house_data = pd.DataFrame({
                    'Parameter': ['Rashi', 'Lord'],
                    'Value': [result['House11th']['rashi'], result['House11th']['lord']]
                })
                st.table(house_data)
                
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