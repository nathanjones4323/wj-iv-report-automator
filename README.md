# 👩‍🏫 Woodcock-Johnson IV Report Automator 🤖

## Introduction

This app is a tool to automatically generate and fill out reports for student's with an [IEP](https://en.wikipedia.org/wiki/Individualized_Education_Program)

The reports use data gathered and generated under the [Woodcock–Johnson Tests of Cognitive Abilities (WJ IV)](https://riversideinsights.com/woodcock_johnson_iv) framework to assess a student's cognitive abilities.

---
## Assumptions

This application can be used by educators **under the following assumptions:**

1. Your school uses Riverside Score to generate Woodcock–Johnson Tests of Cognitive Abilities

2. You have 1+ saved Examinees in the "My Recent Examinees" table 👇

![My Recent Examinees](app/readme_images/woodcock_johnson_dashboard.png?raw=true "My Recent Examinees")

3. You want to run reports for WJ IV Tests of Achievement Form A and Extended (Opposed to WJ IV Tests of Oral Language, etc.)

4. You have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed for the correct OS (Window, Mac, Linux)

> :warning: After generating the reports you check them and see the highlighted words / phrases to spot check that the app input them correctly.

---
## Setup

1. Install Docker Desktop and make sure it's running

2. Open your `terminal` (Mac) or `command prompt` (Windows)

* For Mac users, you can hit ⌘ (command) + Space to pull up **Spotlight Search**. Type in "terminal" and open the default terminal app.
![Spotlight Search](app/readme_images/spotlight_search.png?raw=true "Spotlight Search")

* For Windows users, you can [open command prompt following these instructions](https://www.wikihow.com/Open-Terminal-in-Windows)

3. Copy and paste the following command into the newly opened terminal or command prompt and hit Enter
```
git clone https://github.com/nathanjones4323/wj-iv-report-automator.git
```
4. Copy and paste the following command into the same terminal or command prompt
```
cd wj-iv-report-automator && docker compose build && docker compose up
```

Step 4 might take a few minutes if this is the first time setting it up.

5. Check Docker Desktop and you should see 2 "images" in use

![Docker Desktop Image Confirmation](app/readme_images/spotlight_search.png?raw=true "Docker Desktop Image Confirmation")

6. Open your internet browser and paste in the following url to access the app and follow the instructions to automate your reports !
```
http://localhost:8501/
```

![Streamlit App](app/readme_images/streamlit-app.png?raw=true "Streamlit App")

---
## Example Usage

* TODO