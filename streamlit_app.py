import streamlit as st
from mistralai import Mistral
from markdown import markdown
import os

rules = """You are an instruction-following assistant. Only do exactly what the user explicitly requests..."""

def llm(prompt):
    prompt = "Strict Rules: " + rules + '\n' + prompt + '\n\nResponse:'
    with Mistral(api_key=os.environ.get("MISTRAL_API_KEY")) as mistral:
        res = mistral.chat.complete(
            model="mistral-small-latest",
            messages=[{"content": prompt, "role": "user"}],
            stream=False
        )
    return res.choices[0].message.content

pdf = '''<button id="printBtn">Download PDF</button>
<script>
document.getElementById('printBtn').addEventListener('click', function () {
  window.print();
});
</script>
'''

head = lambda name: f'<html><head><link rel="stylesheet" href="styles.css"><title>{name}\'s Resume</title></head><body>'
contact = lambda data: f'*[+91-{data[0]}](tel:+91-{data[0]})|[{data[1]}](mailto:{data[1]})|[Github:{data[2]}](https://github.com/{data[2]})|[Linkedin:{data[3]}](https://www.linkedin.com/in/{data[3]})*'
tile = lambda txt: f'<h2>{txt}</h2>'
tail = lambda: '</body></html>'

class cvmaster:
    def __init__(self):
        self.rules = rules
        self.llm = llm

    def summarise(self, prompt):
        return llm('Act as a professional and based on the below description write a professional Resume Summary: ' + prompt)

    def project(self, prompt):
        return llm('Act as a professional and based on the below description write a professional project Description in 3 bullet points. Description: ' + prompt)

    def milestone(self, prompt):
        return llm('Act as a professional and based on the below description write a professional Achievements Description in 3 bullet points. Description: ' + prompt)

    def expert(self, prompt):
        return llm('Act as a professional and based on the below description write a professional Experience Description in 3 bullet points. Description: ' + prompt)

    def finalize(self, username, name, data, summary, education, skills, achievements, projects, experience):
        with open(username + '.html', 'w') as file:
            file.write(head(name.upper()))
            file.write(markdown('# ' + name.upper()))
            file.write(markdown(contact(data)))
            file.write(markdown('___'))
            file.write(markdown('## SUMMARY'))
            file.write(markdown(summary))
            file.write(markdown('___'))
            file.write(markdown('## EDUCATION'))
            for i in education:
                file.write(markdown("##### " + i + " | " + f'Course Results: **{education[i]}**'))
            file.write(markdown('___'))
            file.write(markdown('## SKILLS'))
            file.write(markdown(skills.replace('\n', ' | ')))
            file.write(markdown('___'))
            file.write(markdown('## Achievements'))
            for i in achievements:
                file.write(markdown('### ' + i))
                file.write(markdown(achievements[i]))
            file.write(markdown('___'))
            file.write(markdown('## PROJECTS'))
            for i in projects:
                file.write(markdown('### ' + i))
                file.write(markdown(projects[i]))
            file.write(markdown('___'))
            file.write(markdown('## Experience'))
            for i in experience:
                file.write(markdown('### ' + i))
                file.write(markdown(experience[i]))
            file.write(pdf)
            file.write(tail())


# ---------------- Streamlit UI ---------------- #
st.set_page_config(page_title="Agentic CV Generator", layout="centered")
st.title("Agentic CV Generator")

if "education" not in st.session_state:
    st.session_state.education = {}
if "achievements" not in st.session_state:
    st.session_state.achievements = {}
if "projects" not in st.session_state:
    st.session_state.projects = {}
if "experience" not in st.session_state:
    st.session_state.experience = {}

with st.form("cv_form"):
    username = st.text_input("UserName")
    name = st.text_input("Full Name")
    contact_number = st.text_input("Contact Number")
    email = st.text_input("Email Address")
    github = st.text_input("GitHub Username")
    linkedin = st.text_input("LinkedIn Username")

    st.subheader("Summary")
    summary_input = st.text_area("Describe your professional profile")
    auto_summary = st.checkbox("Generate AI Summary")

    st.subheader("Education")
    edu_title = st.text_input("Education Title")
    edu_institute = st.text_input("Institute")
    edu_dates = st.text_input("Dates (e.g. 2018-2022)")
    edu_result = st.text_input("Result/Grade")
    if st.form_submit_button("Add Education"):
        key = f"{edu_title} | {edu_institute} | {edu_dates}"
        st.session_state.education[key] = edu_result

    st.subheader("Skills")
    skills = st.text_area("List your skills (comma or line separated)")

    st.subheader("Achievements")
    ach_title = st.text_input("Achievement Title")
    ach_date = st.text_input("Achievement Date")
    ach_desc = st.text_area("Description")
    if st.form_submit_button("Add Achievement"):
        cv = cvmaster()
        st.session_state.achievements[f"{ach_title} | {ach_date}"] = cv.milestone(ach_desc)

    st.subheader("Projects")
    proj_title = st.text_input("Project Title")
    proj_date = st.text_input("Project Date")
    proj_desc = st.text_area("Description")
    if st.form_submit_button("Add Project"):
        cv = cvmaster()
        st.session_state.projects[f"{proj_title} | {proj_date}"] = cv.project(proj_desc)

    st.subheader("Experience")
    exp_title = st.text_input("Experience Title")
    exp_dates = st.text_input("Dates (e.g. 2020-2023)")
    exp_desc = st.text_area("Description")
    if st.form_submit_button("Add Experience"):
        cv = cvmaster()
        st.session_state.experience[f"{exp_title} | {exp_dates}"] = cv.expert(exp_desc)

    submitted = st.form_submit_button("Generate Resume")

if submitted:
    cv = cvmaster()
    summary = cv.summarise(summary_input) if auto_summary else summary_input
    data = (contact_number, email, github, linkedin)

    cv.finalize(
        username=username,
        name=name,
        data=data,
        summary=summary,
        education=st.session_state.education,
        skills=skills,
        achievements=st.session_state.achievements,
        projects=st.session_state.projects,
        experience=st.session_state.experience,
    )

    st.success(f"Resume for {name} generated as {username}.html")
