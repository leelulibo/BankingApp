# utils.py
def register_user(id_number, firstname, lastname, phone, email, account_number, password):
    with open("user_data.txt", "a") as file:
        file.write(f"{id_number},{firstname},{lastname},{phone},{email},{account_number},{password}\n")

def login_user(email, password):
    with open("user_data.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if data[4] == email and data[6] == password:
                return True
    return False
