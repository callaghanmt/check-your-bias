import streamlit as st
import pandas as pd
import numpy as np

def create_mock_cv():
    names = {
        'male_western': ['James Wilson', 'Oliver Smith', 'Thomas Brown'],
        'female_western': ['Emma Clarke', 'Sophie Taylor', 'Lucy Williams'],
        'male_non_western': ['Mohammed Khan', 'Wei Zhang', 'Raj Patel'],
        'female_non_western': ['Fatima Hussein', 'Min Liu', 'Priya Sharma']
    }
    
    universities = [
        'Local Post-92 University',
        'Russell Group University',
        'Oxford/Cambridge',
        'International University'
    ]
    
    experiences = [
        '2 years retail at Tesco',
        '18 months office admin',
        'Summer internship at big tech company',
        'Part-time work through university'
    ]
    
    hobbies = [
        'Cricket club captain',
        'Student newspaper editor',
        'Community volunteer',
        'University debate society'
    ]
    
    cv_data = {
        'Name': np.random.choice(names[np.random.choice(list(names.keys()))]),
        'Education': np.random.choice(universities),
        'Experience': np.random.choice(experiences),
        'Extra-curricular': np.random.choice(hobbies)
    }
    return cv_data

def main():
    st.title("Check Your Bias: CV Rating Exercise")
    st.write("""
    ### About This Exercise
    You're about to rate 10 graduate CVs. Each decision you make helps reveal potential unconscious biases in hiring.
    
    Try to be consistent in your ratings, but don't overthink each decision - often biases show up in quick, instinctive judgments.
    """)
    
    if 'decisions' not in st.session_state:
        st.session_state.decisions = []
    
    if len(st.session_state.decisions) < 10:
        cv = create_mock_cv()
        
        st.subheader(f"Candidate Profile: {len(st.session_state.decisions) + 1}/10")
        
        # Create a formatted table
        df = pd.DataFrame([cv])
        st.table(df)
        
        rating = st.slider("How suitable is this candidate? (1-10)", 1, 10, 5)
        st.write("1 = Not at all suitable, 10 = Extremely suitable")
        
        if st.button("Submit Rating"):
            st.session_state.decisions.append({**cv, 'rating': rating})
            st.rerun()  # Changed from experimental_rerun() to rerun()
            
    else:
        df = pd.DataFrame(st.session_state.decisions)
        st.subheader("Your Rating Patterns")
        
        # Analysis of ratings by name origin
        western_mask = df['Name'].str.contains('Wilson|Smith|Brown|Clarke|Taylor|Williams')
        western_ratings = df[western_mask]['rating'].mean()
        non_western_ratings = df[~western_mask]['rating'].mean()
        
        # Analysis by university type
        russell_ratings = df[df['Education'].str.contains('Russell|Oxford|Cambridge')]['rating'].mean()
        other_ratings = df[~df['Education'].str.contains('Russell|Oxford|Cambridge')]['rating'].mean()
        
        st.write("### Your Average Ratings")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Western Names", f"{western_ratings:.1f}/10")
            st.metric("Non-Western Names", f"{non_western_ratings:.1f}/10")
        with col2:
            st.metric("Russell Group/Oxbridge", f"{russell_ratings:.1f}/10")
            st.metric("Other Universities", f"{other_ratings:.1f}/10")
            
        st.write("""
        ### Reflection Questions
        1. Were you surprised by any patterns in your ratings?
        2. Did certain names, universities, or experiences influence your decisions more than others?
        3. How might these subtle preferences affect real-world hiring decisions?
        4. What steps could you take to make more objective assessments?
        """)

if __name__ == "__main__":
    main()
