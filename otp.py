import pyotp
import vonage
import time
from datetime import datetime, timedelta

# generate a otp using pyotp
def generate_otp():
    # generate a secret key
    secret_key = pyotp.random_base32()
    # create a totp object using the secret key
    totp = pyotp.TOTP(secret_key)
    # generate an otp
    otp = totp.now()
    # Get the first timestamp when otp is generated
    timestamp1 = time.time()
    timestamp_otp_generated = datetime.fromtimestamp(timestamp1)
    return otp , timestamp_otp_generated

# take contact number as input from user
def contact_number_input():
    while True:
        try:
            users_contact_number = input("Enter your contact number: +91 ")
            # check contact field is empty or not
            if users_contact_number:
                # check if the contact number contains only digits
                if users_contact_number.isdigit():
                    # check contact number contains 10 digits or not
                    if len(users_contact_number) == 10:
                        print(f"Contact number is valid: {users_contact_number}")
                        return users_contact_number # Return the valid contact number
                    else:
                        print("Error: Contact number must be exactly 10 digits long.")
                else:
                    print("Error: Please enter a valid numeric contact number. Do not include any non-numeric characters.")
            else:
                print("Error: Please enter your contact number.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unwanted error occurred: {e}")

# send otp to user (instructions are provided on Vonage's  website how to use there API)
def send_opt(otp,user_contact_no):
    user_contact_no = f"91{user_contact_no}"
    try:
        message=f"Testing otp {otp}"
        # replace key and secred with your own key and secret
        client = vonage.Client(key="", secret="")
        sms = vonage.Sms(client)
        responseData = sms.send_message({
            "from": "my_project",
            "to": user_contact_no,
            "text": message,
        })

        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
    except Exception as e:
        print(f"Error: {e}")

# take OTP as input from user
def otp_input():
    # user can You can only try three times.
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        try:
            user_otp = input("Enter your OTP: ")
            # Get the second timestamp when otp is entered by user
            timestamp2 = time.time()
            timestamp_otp_submitted_by_user = datetime.fromtimestamp(timestamp2)
            # check otp field is empty or not
            if user_otp:
                # check if the otp contains only digits
                if user_otp.isdigit():
                    # check contact number contains 10 digits or not
                    if len(user_otp) == 6:
                        print("OTP submitted successfully")
                        return user_otp,timestamp_otp_submitted_by_user
                    else:
                        print("Error: OTP must be exactly 6 gigits long.")
                else:
                    print("Error: Please enter a valid numeric OTP. Do not include any non-numeric characters.")
            else:
                print("Error: Please enter your OTP.")
            attempts +=1
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unwanted error occurred: {e}")
    print(f"Error: Exceeded maximum attempts ({max_attempts}). Please try again later.")

# Validates the user-inputted OTP
def validate_otp(otp_generated,otp_entererd_by_user,timestamp_otp_generated,timestamp_otp_submitted_by_user):
    
    try:
        # Calculate the time difference
        time_difference = timestamp_otp_submitted_by_user - timestamp_otp_generated

        # Define the expiration threshold as 5 minutes (300 seconds)
        expiration_threshold = timedelta(seconds=300)

        # Check if the time difference is greater than or equal to the expiration threshold
        if time_difference >= expiration_threshold:
            print("Error: OTP expired")
            exit()

        # Validates the user-inputted OTP against the expected OTP.
        if otp_generated == otp_entererd_by_user:
            print("Success: OTP is valid. Access granted!")  # Print a success message
        else:
            print("OoPs: OTP is not valid.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    user_contact_number = contact_number_input()
    otp_generated,timestamp_otp_generated = generate_otp()
    send_opt(otp_generated,user_contact_number)
    otp_entererd_by_user, timestamp_otp_submitted_bu_user= otp_input()
    validate_otp(otp_generated,otp_entererd_by_user,timestamp_otp_generated,timestamp_otp_submitted_bu_user)