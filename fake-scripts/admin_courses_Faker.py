import json
import random

# Constants
prefixes = ["CSCI", "DSCI", "ITP"]
level_500 = range(500, 600)
level_600 = range(600, 700)
credits = [2, 3, 4]

# Function to generate unique courses
def generate_courses(prefixes, levels, count):
    courses = {}
    while len(courses) < count:
        prefix = random.choice(prefixes)
        level = random.choice(levels)
        course_id = f"{prefix}{level}"
        course_credits = random.choice(credits)
        courses[course_id] = course_credits
    return courses

# Generate 15 courses for 500-level and 600-level
courses_500 = generate_courses(prefixes, level_500, 15)
courses_600 = generate_courses(prefixes, level_600, 15)

# Combine both dictionaries
combined_courses = {**courses_500, **courses_600}

# Save the combined courses to a JSON file
with open('Combined_Courses.json', 'w') as file:
    json.dump(combined_courses, file, indent=4)

print("Courses have been saved to 'Combined_Courses.json'.")
