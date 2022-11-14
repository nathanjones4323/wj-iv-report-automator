from utils import *
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import streamlit as st
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

# Page Title and Descriptions
st.title("👩‍🏫 Woodcock-Johnson IV Report Automator 🤖")
st.markdown("""
**This app is a tool to automatically generate and fill out reports for students being evaluated for an [IEP](https://en.wikipedia.org/wiki/Individualized_Education_Program)**

The reports use data gathered and generated under the [Woodcock–Johnson Tests of Academic Achievement (WJ IV)](https://riversideinsights.com/woodcock_johnson_iv) framework to assess a student's cognitive abilities.

This application can be used by educators under the following assumptions:
1. Your school uses [Riverside Score](https://riversidescore.com/) to generate Woodcock–Johnson Tests of Academic Achievement and Oral Language
2. You have 1+ saved *Examinees* in the "My Recent Examinees" table 👇
""")
st.image("readme_images/woodcock_johnson_dashboard.png")
st.markdown("""
3. You want to run reports for **WJ IV Tests of Achievement Form A and Extended** (Opposed to **WJ IV Tests of Oral Language**, etc.)
""")
st.warning("The generated report will be highlighted where the script made edits, or where you can put an in depth ancedote on the student")

# Selenium Options
options = Options()
options.headless = True

# User Inputs
resource_sepcialist_name, student_last_names, username, password, scoring_template_name = init_user_inputs()
if st.button("Run it !"):
    with st.spinner("⏳ Please wait while we fetch the data... (This might take a minute so grab a coffee ☕)"):
        t1 = time.time()
        driver = webdriver.Remote(
            "http://selenium:4444/wd/hub", options=options)
        # Login to Homepage
        login(driver, username, password)

        # Get URLs for students to report on
        urls = get_student_urls(driver, student_last_names)

        # Create and Complete Reports
        generate_and_fill_report(
            driver, urls, scoring_template_name, resource_sepcialist_name)
        t2 = time.time()
        st.markdown(
            f"### ✅ All reports completed. Process took {(t2-t1):.2f}s")
        st.markdown(
            f"You can view the completed reports inside the woodcock_johnson_reports folder located at {os.getcwd()}/woodcock_johnson_reports")
        driver.quit()
