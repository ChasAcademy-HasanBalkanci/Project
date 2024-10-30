def validate_percentage_input(prompt):
    while True:
        try:
            percentage = int(input(prompt))
            if 0 <= percentage <= 100:
                return percentage
            else:
                print("Invalid input. Percentage must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_user_input(prompt, valid_choices):
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_choices:
            return choice
        else:
            print(f"Invalid choice. Please enter one of {', '.join(valid_choices)}.")
