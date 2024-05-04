# Installation

Before running the application, you need to install the necessary dependencies. Run the following command:

```
pip install -r requirements.txt
```

## Running the Application

To run the application, you will use Streamlit. Follow these steps:

1. Navigate to the directory containing `app.py`.
2. Run the application using the following command:

```
streamlit run app.py
```

## Utilizing the Database Manager

To manage your database directly, you can use `db_manager.py`. Ensure you are in the same directory as `db_manager.py` and execute:

```
streamlit run db_manager.py
```

## File Information
- **`app.py`**: This is likely the main script that runs the Streamlit application. It handles the user interface, including navigation between different functionalities like login, profile management, course registration, and fee payment.
- **`db_manager.py`**: This script probably contains higher-level functions for managing database interactions. It could include functions to add, update, or delete student and course data, handling these operations in a way that abstracts the complexity away from the main application logic.
- **`db_utils.py`**: This utility script is essential for direct interactions with the Firebase database. It likely includes functions for reading, writing, and updating data, as well as possibly managing connections and ensuring data integrity.

