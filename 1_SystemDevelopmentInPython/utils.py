def input_with_validation(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"The value must be between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input, please try again.")
