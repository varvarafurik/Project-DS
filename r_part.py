import streamlit as st

st.header("The analysis of offenses in Kansas in 2020")

HtmlFile = open("r_code.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()

st.markdown(source_code, unsafe_allow_html=True)