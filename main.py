import streamlit as st
import pandas as pd

# Configure the page
st.set_page_config(
    page_title="LeetCode Viewer",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #e2e8f0;
    }
    
    /* Headers and text */
    h1, h2, h3, h4, h5, h6 {
        color: #e2e8f0 !important;
    }
    
    p {
        color: #cbd5e1 !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Difficulty badges */
    .difficulty-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 500;
        display: inline-block;
    }
    .difficulty-easy {
        background-color: rgba(34, 197, 94, 0.2);
        color: #4ade80;
    }
    .difficulty-medium {
        background-color: rgba(234, 179, 8, 0.2);
        color: #facc15;
    }
    .difficulty-hard {
        background-color: rgba(239, 68, 68, 0.2);
        color: #fb7185;
    }
    
    /* Cards and containers */
    .stMarkdown {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #e2e8f0 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.05);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: 1px solid #334155;
        border-radius: 8px;
        color: #e2e8f0;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #3b82f6;
    }
    
    /* Dataframe */
    [data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* Divider */
    hr {
        border-color: #334155;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.05);
        border-right: 1px solid #334155;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px;
    }
    
    /* Search input */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid #334155;
        color: #e2e8f0;
    }
    
    /* Multiselect */
    .stMultiSelect [data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid #334155;
    }
    
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #3b82f6;
    }
    
    /* Problem details container */
    .problem-details {
        max-width: 100% !important;
        width: 100% !important;
        margin: 1rem 0;
    }
    
    /* Make containers full width */
    .stMarkdown, .stCodeBlock, [data-testid="stExpander"] {
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Adjust code block width */
    pre {
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Make tabs container full width */
    .stTabs [data-baseweb="tab-list"] {
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Adjust tab content width */
    .stTabs [data-baseweb="tab-panel"] {
        max-width: 100% !important;
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load the Excel sheet
@st.cache_data
def load_data():
    df = pd.read_excel("problems.xlsx")
    return df.fillna("")

df = load_data()

# Main title with custom styling
st.markdown("""
    <h1 style='text-align: center; color: #e2e8f0; margin-bottom: 2rem;'>
        📘 LeetCode Problem Viewer
    </h1>
""", unsafe_allow_html=True)

# Sidebar Filters
with st.sidebar:
    st.markdown("### 🔍 Filters")
    
    # Difficulty filter
    difficulties = df['difficulty'].unique().tolist()
    selected_difficulty = st.multiselect(
        "Select Difficulty",
        difficulties,
        default=difficulties,
        help="Choose one or more difficulty levels"
    )
    
    # Search by problem title
    search_query = st.text_input(
        "🔎 Search Problems",
        placeholder="Enter problem title...",
        help="Search for specific problems by title"
    )
    
    # Simple Analytics
    st.markdown("### 📊 Analytics")
    diff_counts = df['difficulty'].value_counts()
    for diff, count in diff_counts.items():
        st.metric(diff, count)

# Filter the dataframe
filtered_df = df[
    (df['difficulty'].isin(selected_difficulty)) &
    (df['title'].str.contains(search_query, case=False, na=False))
]

# Display problem count
st.markdown(f"### 📝 Showing {len(filtered_df)} problems")

# Create tabs for problem details
if 'current_problem' not in st.session_state:
    st.session_state.current_problem = None

# Main table view
table_tab, details_tab = st.tabs(["📊 Problems Table", "📝 Problem Details"])

with table_tab:
    # Prepare the dataframe with custom columns
    display_df = filtered_df.copy()
    
    # Function to create difficulty badge HTML
    def get_difficulty_badge(difficulty):
        colors = {
            'Easy': '#4ade80',
            'Medium': '#facc15',
            'Hard': '#fb7185'
        }
        bg_colors = {
            'Easy': 'rgba(34, 197, 94, 0.2)',
            'Medium': 'rgba(234, 179, 8, 0.2)',
            'Hard': 'rgba(239, 68, 68, 0.2)'
        }
        return f"""
            <div style="
                background-color: {bg_colors[difficulty]};
                color: {colors[difficulty]};
                padding: 4px 12px;
                border-radius: 20px;
                font-weight: 500;
                display: inline-block;
                text-align: center;
            ">
                {difficulty}
            </div>
        """

    # Add difficulty badges to the dataframe
    display_df['difficulty_badge'] = display_df['difficulty'].apply(
        lambda x: get_difficulty_badge(x)
    )

    # Display problems in a custom table layout
    for index, row in display_df.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"**{row['title']}**")
        
        with col2:
            st.markdown(row['difficulty_badge'], unsafe_allow_html=True)
        
        with col3:
            if st.button("View Details", key=f"btn_{index}", type="primary"):
                st.session_state.current_problem = row['title']
                st.rerun()
        
        st.markdown("---")

    # Add table styling
    st.markdown("""
        <style>
        .stMarkdown {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 10px;
            margin: 5px 0;
        }
        
        .stButton button {
            width: 100%;
            padding: 6px 12px;
            background: rgba(59, 130, 246, 0.1);
            color: #3b82f6;
            border: 1px solid #3b82f6;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background: rgba(59, 130, 246, 0.2);
            transform: translateY(-1px);
        }
        
        hr {
            margin: 0;
            border-color: rgba(255, 255, 255, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

with details_tab:
    if st.session_state.current_problem:
        problem = filtered_df[filtered_df['title'] == st.session_state.current_problem].iloc[0]
        
        # Add a back button
        if st.button("← Back to Problems", type="secondary"):
            st.session_state.current_problem = None
            st.rerun()
        
        # Problem header
        st.markdown(f"""
            <h2 style='color: #e2e8f0;'>{problem['title']}</h2>
            {get_difficulty_badge(problem['difficulty'])}
        """, unsafe_allow_html=True)
        
        # Problem content
        st.markdown("### Problem Description")
        st.markdown(problem['content'])
        
        # Code solutions in tabs
        if problem['java_code'] or problem['cpp_code']:
            code_tab1, code_tab2 = st.tabs(["Java Solution", "C++ Solution"])
            
            with code_tab1:
                if problem['java_code']:
                    st.code(problem['java_code'], language='java')
                    if problem['java_explanation']:
                        with st.expander("View Explanation"):
                            st.markdown(problem['java_explanation'])
            
            with code_tab2:
                if problem['cpp_code']:
                    st.code(problem['cpp_code'], language='cpp')
    else:
        st.info("👈 Select a problem from the table to view its details")

# Footer
st.markdown("""
    <div style='text-align: center; color: #64748b; padding: 2rem;'>
        Made with ❤️ for LeetCode enthusiasts
    </div>
""", unsafe_allow_html=True)
