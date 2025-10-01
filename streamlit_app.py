with st.form("cv_form"):
    username = st.text_input("UserName", key="username")
    name = st.text_input("Full Name", key="fullname")
    contact_number = st.text_input("Contact Number", key="contact")
    email = st.text_input("Email Address", key="email")
    github = st.text_input("GitHub Username", key="github")
    linkedin = st.text_input("LinkedIn Username", key="linkedin")

    st.subheader("Summary")
    summary_input = st.text_area("Describe your professional profile", key="summary_input")
    auto_summary = st.checkbox("Generate AI Summary", key="auto_summary")

    st.subheader("Education")
    edu_title = st.text_input("Education Title", key="edu_title")
    edu_institute = st.text_input("Institute", key="edu_institute")
    edu_dates = st.text_input("Dates (e.g. 2018-2022)", key="edu_dates")
    edu_result = st.text_input("Result/Grade", key="edu_result")
    if st.form_submit_button("Add Education", key="add_edu"):
        key = f"{edu_title} | {edu_institute} | {edu_dates}"
        st.session_state.education[key] = edu_result

    st.subheader("Skills")
    skills = st.text_area("List your skills (comma or line separated)", key="skills")

    st.subheader("Achievements")
    ach_title = st.text_input("Achievement Title", key="ach_title")
    ach_date = st.text_input("Achievement Date", key="ach_date")
    ach_desc = st.text_area("Description", key="ach_desc")
    if st.form_submit_button("Add Achievement", key="add_ach"):
        cv = cvmaster()
        st.session_state.achievements[f"{ach_title} | {ach_date}"] = cv.milestone(ach_desc)

    st.subheader("Projects")
    proj_title = st.text_input("Project Title", key="proj_title")
    proj_date = st.text_input("Project Date", key="proj_date")
    proj_desc = st.text_area("Description", key="proj_desc")
    if st.form_submit_button("Add Project", key="add_proj"):
        cv = cvmaster()
        st.session_state.projects[f"{proj_title} | {proj_date}"] = cv.project(proj_desc)

    st.subheader("Experience")
    exp_title = st.text_input("Experience Title", key="exp_title")
    exp_dates = st.text_input("Dates (e.g. 2020-2023)", key="exp_dates")
    exp_desc = st.text_area("Description", key="exp_desc")
    if st.form_submit_button("Add Experience", key="add_exp"):
        cv = cvmaster()
        st.session_state.experience[f"{exp_title} | {exp_dates}"] = cv.expert(exp_desc)

    submitted = st.form_submit_button("Generate Resume", key="submit_resume")
