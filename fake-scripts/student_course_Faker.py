import json
import random

# Load student data
with open('Students_Data_2.json', 'r') as f:
    students_data = json.load(f)

# Load course data
with open('Combined_Courses.json', 'r') as f:
    courses_data = json.load(f)

# List of possible grades
grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D', 'F']

# Generate course details for each student
students_courses = {}
for student_id in students_data.keys():
    num_semesters = random.randint(2, 3)
    semesters = random.sample(['Fall 2022', 'Winter 2023', 'Spring 2023', 'Summer 2023'], num_semesters)
    semesters_courses = {}
    
    for semester in semesters:
        num_courses = random.randint(1, 5)  # Random number of courses per semester
        courses_list = []
        selected_courses = random.sample(list(courses_data.keys()), num_courses)
        
        for course in selected_courses:
            course_details = {
                "Course": course,
                "Credits": courses_data[course],
                "Grade": random.choice(grades)
            }
            courses_list.append(course_details)
        
        semesters_courses[semester] = courses_list

    students_courses[student_id] = semesters_courses

# Save the course enrollment details to JSON
with open('Student_Course_Details2.json', 'w') as f:
    json.dump(students_courses, f, indent=4)

print("Student course enrollment details have been generated and saved.")
