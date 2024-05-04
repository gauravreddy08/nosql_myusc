# Let's use the Faker library to generate the rest of the dataset more dynamically
from faker import Faker
import json
import random

fake = Faker()
students_data_1 = {
    "101": {
        "Address": "1248 W 20th St, Los Angeles, CA 90007",
        "Age": 22,
        "Degree": "Masters",
        "Email": "john.doe@example.com",
        "Name": "John Doe",
        "Phone Number": 2132137899,
        "Specialization": "Computer Science"
    }
}
students_data_2 = {}

# Adjust the student ID assignment based on the degree
def generate_student(student_id):
    age = random.randint(22, 35)
    degree = random.choice(["Masters", "Postdoc"])
    student_id += 100 if degree == "Postdoc" else 0
    email = fake.email()
    name = fake.name()
    phone_number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    specialization = fake.job()
    address = fake.address().replace('\n', ', ')
    
    return {
        str(student_id): {
            "Address": address,
            "Age": age,
            "Degree": degree,
            "Email": email,
            "Name": name,
            "Phone Number": int(phone_number),
            "Specialization": specialization
        }
    }

# Generate and sort student data
for i in range(102, 150):  # Generate from ID 102 to 150
    new_student = generate_student(i)
    student_id = next(iter(new_student))  # Get the first (and only) key in the new_student dictionary
    if student_id.startswith('1'):
        students_data_1.update(new_student)
    elif student_id.startswith('2'):
        students_data_2.update(new_student)

# Writing the data to two separate JSON files
with open('Students_Data_1.json', 'w') as f1:
    json.dump(students_data_1, f1, indent=4)
with open('Students_Data_2.json', 'w') as f2:
    json.dump(students_data_2, f2, indent=4)

