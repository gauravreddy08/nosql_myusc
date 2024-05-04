import streamlit as st
from db_utils import manage_data
import json 
import pandas as pd

st.header('MyUSC: NoSQL Student Management System')

DB_URLS = ['https://masterdatabase-4a5d1-default-rtdb.firebaseio.com/',
           'https://phddatabase-636da-default-rtdb.firebaseio.com/']


login, profile, courses, fees = st.tabs(["Login", "Profile", "Courses", "Fees"])

if 'usc_id' not in st.session_state:
    st.session_state['usc_id'] = None
    st.session_state['db_url'] = None

with login:
    usc_id = st.text_input("Enter your USC ID", )
    submit = st.button('Submit')
    if submit:
        if not usc_id: st.warning("Enter a valid USC ID")
        else: 
            st.session_state['usc_id'] = usc_id
            st.session_state['db_url'] = DB_URLS[int(str(st.session_state['usc_id'])[0])-1]

            st.session_state['student_data'] = manage_data('students', 'read', str(st.session_state['usc_id']), database_url=st.session_state['db_url'])
            st.session_state['student_data'] = st.session_state['student_data'].decode('utf-8')
            st.session_state['student_data'] = json.loads(st.session_state['student_data'])

            st.session_state['fees_data'] = manage_data('fees', 'read', st.session_state['usc_id'], database_url=st.session_state['db_url'])
            st.session_state['fees_data'] = st.session_state['fees_data'].decode('utf-8')
            st.session_state['fees_data'] = pd.DataFrame(json.loads(st.session_state['fees_data'])).T

            st.session_state['courses'] = manage_data('courses', 'read', st.session_state['usc_id'], database_url=st.session_state['db_url'])
            st.session_state['courses'] = st.session_state['courses'].decode('utf-8')
            st.session_state['courses'] = json.loads(st.session_state['courses'])

with profile:
    if st.session_state['usc_id']:
        EDIT_MODE = False
        EDIT_MODE = st.toggle('Edit Mode', value=False)

        # st.markdown('#### Student Details')

        updated_data = st.data_editor(st.session_state['student_data'], 
                       disabled=not EDIT_MODE, use_container_width=True, 
                       column_config={'value': f'USC ID: {st.session_state['usc_id']}'})
       
        
        if EDIT_MODE:
            profile_submit = st.button('Submit', key='profilesubmit')
            if profile_submit:
                st.success('Update sucessful')
                
                manage_data('students', 'update', 
                            st.session_state['usc_id'], 
                            updates=updated_data,
                            database_url=st.session_state['db_url'])
        
    else:
        st.error("Enter a valid USC ID")



with courses:
    if st.session_state['usc_id']:
        # st.markdown(f"###### Student ID: {st.session_state['usc_id']}")
        # st.markdown('#### Course Details')

        course_semester = st.selectbox('Choose Semester', st.session_state['courses'].keys())

        cl = st.empty()
        cl.dataframe(st.session_state['courses'][course_semester], 
                       use_container_width=True,
                       column_order=['Course', 'Credits', 'Grade'])
        
        registration_check = st.toggle('Course Registration')
        if registration_check:
            if manage_data('admin', 'read', 'course_registration', database_url=st.session_state['db_url']).decode('utf-8').lower() == 'true':

                st.warning(f"**Semester:** {course_semester}")
                selected_course = st.selectbox("Select Course", json.loads(manage_data('admin', 'read', 'course_list').decode('utf-8')).keys())

                register = st.button("Register")
                if register:
                    manage_data('courses', 'update', st.session_state['usc_id'], 
                                updates={f"{course_semester}/{len(st.session_state['courses'][course_semester])}": {
                                        'Course': selected_course, 
                                        'Credits': json.loads(manage_data('admin', 'read', 'course_list').decode('utf-8'))[selected_course]}},
                                        database_url=st.session_state['db_url'])
                    
                    st.session_state['courses'] = manage_data('courses', 'read', st.session_state['usc_id'], database_url=st.session_state['db_url'])
                    st.session_state['courses'] = st.session_state['courses'].decode('utf-8')
                    st.session_state['courses'] = json.loads(st.session_state['courses'])

                    cl.dataframe(st.session_state['courses'][course_semester], 
                        use_container_width=True,
                        column_order=['Course', 'Credits', 'Grade'])
                    
                    st.success('Registered Sucessfully')
            else:
                st.warning('Course Registration not opened yet')

    else:
        st.error("Enter a valid USC ID")






with fees:
    if st.session_state['usc_id']:
        # st.markdown(f"###### Student ID: {st.session_state['usc_id']}")
        # st.markdown('#### Tuition Fee Details')

        fd = st.empty()

        fd.dataframe(st.session_state['fees_data'], 
                       use_container_width=True,
                       column_order=['Total Fee', 'Balance'])
        
        st.markdown('#### Fee Payment')
        pay1, pay2 = st.columns(2)
        with pay1:
            semester= st.selectbox('Choose Semester', st.session_state['fees_data'].index, key='fee_payment_semester')
        with pay2:
            amt = st.number_input("Enter Amount")
        
        fee_pay = st.button('Pay', use_container_width=True)
        if fee_pay and amt and semester:
            st.success('Payment sucessful')
            st.session_state['fees_data'].loc[semester].Balance = max(0, st.session_state['fees_data'].loc[semester].Balance-amt)
            manage_data('fees', 'update', st.session_state['usc_id'], updates=st.session_state['fees_data'].T.to_dict(), database_url=st.session_state['db_url'])

            st.session_state['fees_data'] = manage_data('fees', 'read', st.session_state['usc_id'], database_url=st.session_state['db_url'])
            st.session_state['fees_data'] = st.session_state['fees_data'].decode('utf-8')
            st.session_state['fees_data'] = pd.DataFrame(json.loads(st.session_state['fees_data'])).T

            fd.dataframe(st.session_state['fees_data'], 
                       use_container_width=True,
                       column_order=['Total Fee', 'Balance'])

    else:
        st.error("Enter a valid USC ID")
    
    
    

