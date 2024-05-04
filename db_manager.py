import streamlit as st
import requests
import json
import pandas as pd

DB_URLS = ['https://masterdatabase-4a5d1-default-rtdb.firebaseio.com/',
           'https://phddatabase-636da-default-rtdb.firebaseio.com/']

with open('serviceAccountKey.json', 'r') as file:
    API_KEY = json.load(file)

def add_course(course_id, units):
    """Add a new course to the database."""
    response = requests.patch(f'https://masterdatabase-4a5d1-default-rtdb.firebaseio.com/admin/course_list.json', json={course_id: units})
    response = requests.patch(f'https://phddatabase-636da-default-rtdb.firebaseio.com/admin/course_list.json', json={course_id: units})
    return response.json()

def delete_course(course_id):
    requests.delete(f'https://masterdatabase-4a5d1-default-rtdb.firebaseio.com/admin/course_list/{course_id}.json?auth={API_KEY}')
    requests.delete(f'https://phddatabase-636da-default-rtdb.firebaseio.com/admin/course_list/{course_id}.json?auth={API_KEY}')

def add_student(student_id, data):
    """Add a new student to the database."""
    endpoint = f'{DB_URLS[int(str(student_id)[0])-1]}students/{student_id}.json?auth={API_KEY}'
    response = requests.patch(endpoint, json=data)

def delete_student(student_id):
    """Delete a student from the database."""
    endpoint = f'{DB_URLS[int(str(student_id)[0])-1]}students/{student_id}.json?auth={API_KEY}'
    response = requests.delete(endpoint)
    return response.json()

courses, registration, students, records, fee = st.tabs(['Courses', 'Registration', 'Students', 'Student Records', 'Student Payments'])

with fee:
    studentf_id = st.text_input('Enter a USC ID', key='fee records')
    if studentf_id:

        updatedf_data = st.data_editor(pd.DataFrame(requests.get(f"{DB_URLS[int(str(studentf_id)[0])-1]}fees/{studentf_id}.json?auth={API_KEY}").json()).T, 
                    use_container_width=True,
                    column_order=['Total Fee', 'Balance'], num_rows='dynamic')
        if st.button("Update Student Payments"):
            endpoint = f'{DB_URLS[int(str(studentf_id)[0])-1]}fees/{studentf_id}.json?auth={API_KEY}'
            response = requests.patch(endpoint, json=updatedf_data.T.to_dict())
            st.success("Update Sucessful")


with records:
    studentr_id = st.text_input('Enter a USC ID', key='student records')
    if studentr_id:
        course_semester = st.selectbox('Choose Semester',requests.get(f"{DB_URLS[int(str(studentr_id)[0])-1]}courses/{studentr_id}.json?auth={API_KEY}").json().keys())
        updatedr_data = st.data_editor(requests.get(f"{DB_URLS[int(str(studentr_id)[0])-1]}courses/{studentr_id}.json?auth={API_KEY}").json()[course_semester], 
                    use_container_width=True,
                    column_order=['Course', 'Credits', 'Grade'], num_rows='dynamic')
        if st.button("Update Student Record"):
            endpoint = f'{DB_URLS[int(str(studentr_id)[0])-1]}courses/{studentr_id}.json?auth={API_KEY}'
            response = requests.patch(endpoint, json={course_semester: updatedr_data})
            st.success("Update Sucessful")

with students:
    choice = st.selectbox("Choose Action", ["Add Student", "View Students", 'Update Student', "Delete Student"])

    if choice == "Add Student":
        st.subheader("Add a New Student")
        
        new_id = st.text_input("Student ID")
        new_name = st.text_input("Name")
        new_age = st.text_input("Age")
        new_degree = st.text_input("Degree")
        new_email = st.text_input("Email")
        new_phone = st.text_input("Phone Number")
        new_address = st.text_input("Address")
        new_specialization = st.text_input("Specialization")
        if st.button('Add'):
            new_student_data = {
                "Name": new_name,
                "Age": new_age,
                "Degree": new_degree,
                "Email": new_email,
                "Phone Number": new_phone,
                "Address": new_address,
                "Specialization": new_specialization
            }
            result = add_student(new_id, new_student_data)
            st.write(result)

    elif choice == "View Students":
        masters_read, phd_read = st.columns(2)
        mr = masters_read.button('Display Master\'s Students', use_container_width=True)
        pr = phd_read.button('Display PhD\'s Students', use_container_width=True)
        endpoint = f'{DB_URLS[0]}students.json?auth={API_KEY}'
        if mr:
            endpoint = f'{DB_URLS[0]}students.json?auth={API_KEY}'
            
        elif pr:
            endpoint = f'{DB_URLS[1]}students.json?auth={API_KEY}'

        response = requests.get(endpoint)
        st.json(response.json())

    elif choice == "Update Student":
        student_id = st.text_input('Enter a USC ID')
        retrieve = st.button('Retireve')
        if student_id:
            updated_data = st.data_editor(requests.get(f"{DB_URLS[int(str(student_id)[0])-1]}students/{student_id}.json?auth={API_KEY}").json(), 
                            use_container_width=True)
            sub = st.button('Submit')
            if sub:
                add_student(student_id, updated_data)
                st.success('Edited Sucessfully')

    elif choice == "Delete Student":
        st.subheader("Delete a Student")
        delete_id = st.text_input("Enter Student ID to Delete")
        if st.button('Delete Student'):
            result = delete_student(delete_id)
            st.write(result)

with registration:
    masters_reg, phd_reg = st.columns(2)
    masters_reg_status = masters_reg.toggle('Master\'s Registration')
    phd_reg_status = phd_reg.toggle('PhD\'s Registration')

    if st.button('Update Registration Status', use_container_width=True):
        requests.put(f'https://masterdatabase-4a5d1-default-rtdb.firebaseio.com/admin/course_registration.json?auth={API_KEY}', json=masters_reg_status)
        requests.put(f'https://phddatabase-636da-default-rtdb.firebaseio.com/admin/course_registration.json?auth={API_KEY}', json=phd_reg_status)
        st.success(f'**Masters:** {masters_reg_status}\n\n**PhD:** {phd_reg_status}')

with courses:

    st.markdown('##### **Add/Update a New Course**')
    col1, col2 = st.columns(2)
    course_id = col1.text_input('Enter Course ID')
    course_units = col2.number_input('Enter Course Units', min_value=0, max_value=10, step=1)
    if st.button('Add Course'):
        add_result = add_course(course_id, course_units)
        st.write(add_result)

    st.markdown('##### Current Courses')
    if st.button('Show Courses'):
        courses = requests.get('https://masterdatabase-4a5d1-default-rtdb.firebaseio.com/admin/course_list.json?auth={API_KEY}').json()
        st.json(courses)

    st.markdown('##### Delete a Course')
    # del_dropdown = st.empty()
    # with del_dropdown:
    delete_id = st.selectbox('Select a Course ID to Delete', requests.get('https://masterdatabase-4a5d1-default-rtdb.firebaseio.com/admin/course_list.json?auth={API_KEY}').json().keys())
    if st.button('Delete Course'):
        delete_result = delete_course(delete_id)
        st.error(f"Deleted {delete_id}")
        # with del_dropdown:
        #     delete_id = del_dropdown.selectbox('Select a Course ID to Delete', requests.get('https://masterdatabase-4a5d1-default-rtdb.firebaseio.com/admin/course_list.json?auth={API_KEY}').json().keys())
