from datetime import datetime, date
from bs4 import BeautifulSoup
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import time
import random
from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st
from docxtpl import DocxTemplate

st.title("👩‍🏫 Woodcock-Johnson IV Report Automator 🤖")
st.markdown("""
**This app is a tool to automatically generate and fill out reports for student's with an [IEP](https://en.wikipedia.org/wiki/Individualized_Education_Program)**

The reports use data gathered and generated under the [Woodcock–Johnson Tests of Cognitive Abilities (WJ IV)](https://riversideinsights.com/woodcock_johnson_iv) framework to assess a student's cognitive abilities.

This application can be used by educators under the following assumptions:
1. Your school uses [Riverside Score](https://riversidescore.com/) to generate Woodcock–Johnson Tests of Cognitive Abilities
2. You have 1+ saved *Examinees* in the "My Recent Examinees" table 👇
""")
st.image("woodcock_johnson_dashboard.png")
st.markdown("""
3. You want to run reports for **WJ IV Tests of Achievement Form A and Extended** (Opposed to **WJ IV Tests of Oral Language**, etc.)
""")
st.warning(
    "After generating the reports you must **manually edit the test dates (DATES)** text in the doc which appears in this line:\n\n**Administered by: {{ resource_sepcialist_name }} DATES**")
resource_sepcialist_name = st.text_input(
    "Enter the name of the Resource Specialist (Likely your name)", value="Lizette Juarez")
student_last_names = st.text_input(
    "Enter a Comma Seperated List of your student's last names only", help="**For Example:** `Jones, Juarez, ...`")
student_last_names = [name.lower().strip()
                      for name in student_last_names.split(',')]
username = st.text_input(
    "Enter your Riverside Score Username", help="[Riverside Score Website](https://riversidescore.com/)")
password = st.text_input("Enter your Riverside Score Password",
                         help="[Riverside Score Website](https://riversidescore.com/)")
scoring_template_name = st.text_input("Enter the scoring template you wish to use for the generated report",
                                      help="The template name must match exactly with what is shown online", value='Lizette_MyTemplate')
if st.button("Run it !"):
    with st.spinner("⏳ Please wait while we fetch the data... (This might take a minute so grab a coffee ☕)"):
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()))
        # Go to Webpage
        driver.get("https://riversidescore.com/")
        time.sleep(random.randint(2, 5))
        riverside_score_username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'fld_tb_3')))
        riverside_score_username.send_keys(username)
        riverside_score_password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'fld_tb_18')))
        riverside_score_password.send_keys(password)
        login = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div > div.login-page-cls > div.login-right > form > div.field-wrapper > button')))
        login.click()
        time.sleep(random.randint(2, 5))
        woodcock = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div > div:nth-child(1) > div.product-ribbon > button')))
        woodcock.click()
        time.sleep(5)
        # 1. Select a student name from "My Recent Examinees"
        # Send GET request
        html = driver.page_source
        # convert to beautiful soup object
        soup = BeautifulSoup(html, 'html.parser')

        time.sleep(5)
        # Find all HTML tables with class "search-results"
        # Get the 1st table
        table = soup.find_all('table', class_="search-results")[0]
        urls = []
        for a in table.find_all('a', href=True):
            # Replace with Last Names of the all desired students
            if any(ext in a.text.lower() for ext in student_last_names):
                url = "https://wjscore.com/" + a['href']
                urls.append(url)

        # For each student go to the report section and generate the reports
        for url in urls:
            driver.get(url)
            # 3. Scroll to bottom and "Run Report"
            report = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, 'WJ IV Tests of Achievement Form A and Extended')))
            report.click()
            time.sleep(1)
            run_report = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'btnRunReport')))
            run_report.click()
            # Let the webpage autofill student information
            time.sleep(4)

            # 4. Select "Lizette_MyTemplate" under "Score Selection Template"
            scoring_template = Select(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'score-report-template-select'))))
            # select by visible text
            scoring_template.select_by_visible_text(scoring_template_name)

            # 5. Select "List tests under clusters and also in numerical order." under "Grouping Option"
            scoring_group = Select(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'score-group-option'))))
            # select by visible text
            scoring_group.select_by_visible_text(
                'List tests under clusters and also in numerical order.')

            # 6. Select "Webpage" under "Output Format"
            output_format = Select(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'score-output-format'))))
            # select by visible text
            output_format.select_by_visible_text(
                'Web Page')

            # 7. Click "Run Report"
            run_final_report = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'score-run-report-button')))
            run_final_report.click()

            # 8. Scrape all Table Data
            time.sleep(2)
            html = driver.page_source
            # convert to beautiful soup object
            soup = BeautifulSoup(html, 'html.parser')
            bday = soup.select_one('td:contains("Date of Birth:")').text.replace(
                '\xa0', '').split(':')[1]
            name_list = soup.select_one('td:contains("Name:")').text.replace(
                '\xa0', '').replace("Name:", "").split(',')
            students_name = f"{name_list[1].strip()}{' '}{name_list[0].strip()}"
            students_gender = soup.select_one('td:contains("Sex:")').text.replace(
                '\xa0', '').replace("Sex:", "").split(',')[0]
            if students_gender == "Male":
                students_gender_his_her = "his"
            else:
                students_gender_his_her = "her"
            students_age = date.today().year - datetime.strptime(bday, "%m/%d/%Y").date().year
            # Find all of the tables
            tables = soup.find_all('table', class_="search-results")
            result_tables = []
            i = 1
            for tab in tables:
                try:
                    scraped_table = pd.read_html(tab.prettify())[0]
                    scraped_table["table_number"] = i
                    result_tables.append(scraped_table)
                    i = i + 1
                except Exception as e:
                    print(f"Couldn't read table #{tables.index(tab)}")
                    i = i + 1
            combined_table = pd.concat(
                result_tables[0:22]).reset_index(drop=True)
            # Convert PR to float
            combined_table["PR"] = combined_table["PR"].astype(str).str.replace(
                '<', '').astype(float)
            # Remove Hypens in CLUSTER/Test
            combined_table["CLUSTER/Test"] = combined_table["CLUSTER/Test"].str.replace(
                '-', ' ').str.lower()
            # Remove Duplicate Rows
            combined_table.drop_duplicates(
                subset=["CLUSTER/Test", "SS Classification", "SS", "PR"], inplace=True)
            # Clean up decimals
            combined_table["PR"] = [str(x) if x < 1 else str(
                int(x)) for x in combined_table["PR"]]
            st.write("Data pulled from Woodcock Johnson for")
            st.write(f"Student: {students_name}")
            st.write(f"Birth Date: {bday}")

            # Read in Word template and fill it out
            tpl = DocxTemplate('WJ-IV Report Template_For Nate.docx')
            # Context dictionary (Key Values to replace in Word Doc)
            context = {
                "resource_sepcialist_name": resource_sepcialist_name,
                "students_gender_his_her": students_gender_his_her,
                "students_name": students_name,
                "students_age": students_age
            }
            combined_table["cluster_in_jinja_format"] = [element.replace(
                ' ', '_') for element in combined_table["CLUSTER/Test"]]
            for key in combined_table["cluster_in_jinja_format"]:
                # Get SS
                ss_key = key + "_score"
                ss_value = combined_table[combined_table['cluster_in_jinja_format']
                                          == key]['SS'].values[0]
                context[ss_key] = ss_value
                # Get PR
                pr_key = key + "_percentile"
                pr_value = combined_table[combined_table['cluster_in_jinja_format']
                                          == key]['PR'].values[0]
                context[pr_key] = pr_value
                # Get SS Classification
                classification_key = key + "_classification"
                classification_value = combined_table[combined_table['cluster_in_jinja_format']
                                                      == key]['SS Classification'].values[0]
                context[classification_key] = classification_value

            tpl.render(context)
            students_name_file_formatted = students_name.lower().replace(' ', '_')
            if not os.path.exists(f"{os.getcwd()}/woodcock_johnson_reports"):
                os.makedirs(f"{os.getcwd()}/woodcock_johnson_reports")
            tpl.save(
                f"{os.getcwd()}/woodcock_johnson_reports/{students_name_file_formatted}_{datetime.today().strftime('%Y-%m-%d')}.docx")
            st.write(
                f"Saved report for {students_name} inside `{os.getcwd()}/woodcock_johnson_reports` !")
            st.markdown("## ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐")
            time.sleep(4)
        st.markdown(f"### ✅ All reports completed")
        st.markdown(
            f"You can view the completed reports inside the woodcock_johnson_reports folder located at {os.getcwd()}/woodcock_johnson_reports")
