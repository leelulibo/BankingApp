import json

def txt_to_json(input_file, output_file, log_file):
    data = []
    malformed_lines = []

    with open(input_file, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            try:
                # Split each line by comma
                fields = line.strip().split(',')

                # Validate the number of fields
                if len(fields) < 7:
                    raise ValueError("Not enough fields")

                # Extract fields
                user_id = fields[0]
                firstname = fields[1]
                lastname = fields[2]
                phone = fields[3]
                email = fields[4]
                account_number = fields[5]
                password = fields[6]
                address = " ".join(fields[7:]) if len(fields) > 7 else None

                # Create user dictionary
                user = {
                    "user_id": user_id,
                    "firstname": firstname,
                    "lastname": lastname,
                    "phone": phone,
                    "email": email,
                    "account_number": account_number,
                    "password": password,
                    "address": address
                }

                # Append user dictionary to data list
                data.append(user)
            except Exception as e:
                # Log malformed line with line number and error message
                malformed_lines.append(f"Line {line_number}: {line.strip()} ({str(e)})")

    # Write valid data to JSON file
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # Write malformed lines to log file
    if malformed_lines:
        with open(log_file, 'w') as log:
            for malformed_line in malformed_lines:
                log.write(malformed_line + '\n')

# Call the function with input, output, and log file paths
txt_to_json("user_data.txt", "user_data.json", "malformed_lines.log")
