import json
import random

# Function to generate random fee details
def generate_fee_details():
    semesters = ['Fall', 'Winter', 'Spring', 'Summer']
    year = random.choice([2019, 2020, 2021, 2022, 2023])
    semester = random.choice(semesters)
    total_fee = random.randint(18000, 30000)
    balance = random.randint(0, total_fee)
    return f"{semester} {year}", {
        "Total Fee": total_fee,
        "Balance": balance
    }

# Load the student data from the provided JSON
with open('Students_Data_1.json', 'r') as file:
    students_data = json.load(file)

# Generate fee details for each student
fee_data = {}
for student_id in students_data.keys():
    student_fees = {}
    # Generate fee details for 2 to 4 semesters per student
    num_semesters = random.randint(2, 4)
    for _ in range(num_semesters):
        semester, fees = generate_fee_details()
        student_fees[semester] = fees
    fee_data[student_id] = student_fees

# Save the generated fee data to a JSON file
with open('Fee_Details1.json', 'w') as file:
    json.dump(fee_data, file, indent=4)

print("Fee details generated and saved successfully.")
