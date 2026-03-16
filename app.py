import streamlit as st
from model import predict_mental_health
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="🧠 Mental Health AI", layout="wide")

st.title("🧠 AI Mental Health Detector")
st.markdown("---")

# Sidebar
st.sidebar.header("📝 Analyze Your Text")
user_input = st.sidebar.text_area(
    "Apnar feelings likhun:",
    placeholder="Ami khub stress e achi exam er jonno...",
    height=150
)

# Analyze button
if st.sidebar.button("🔍 Analyze", type="primary"):
    if user_input:
        with st.spinner("AI analyzing..."):
            result = predict_mental_health(user_input)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Emotion", result['emotion'], delta="HIGH RISK" if result['risk_level']=='HIGH' else "Safe")
        with col2:
            st.metric("Confidence", result['confidence'])
        with col3:
            st.metric("Risk Level", result['risk_level'])
        
        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 80 if result['risk_level']=='HIGH' else 20,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Stress Level"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "red" if result['risk_level']=='HIGH' else "green"},
                'steps': [
                    {'range': [0, 50], 'color': 'green'},
                    {'range': [50, 80], 'color': 'orange'}, 
                    {'range': [80, 100], 'color': 'red'}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
        
        # Suggestions
        st.markdown("### 💡 Suggestions:")
        if 'HIGH' in result['risk_level']:
            st.error("🚨 **High Risk**: Friend/family ke bolun, professional help nao")
            st.info("🌿 Try: Deep breathing, 10 min walk, water khan")
        else:
            st.success("✅ Good mental state rakhte thakun!")
    
    else:
        st.warning("Text input din!")

# Demo examples
st.markdown("---")
st.subheader("💬 Demo Examples")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("😟 'Stressed about exams'"):
        st.session_state.demo_text = "Stressed about exams"
with col2:
    if st.button("😊 'Feeling great!'"):
        st.session_state.demo_text = "Feeling great today!"
with col3:
    if st.button("😢 'Want to give up'"):
        st.session_state.demo_text = "I want to give up on life"

if 'demo_text' in st.session_state:
    st.info(f"Demo: {st.session_state.demo_text}")

st.markdown("---")
st.caption("🤖 Powered by HuggingFace AI")