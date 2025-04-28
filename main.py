import phonenumbers
from phonenumbers import carrier, geocoder, timezone, number_type, PhoneNumberFormat
import csv
import os
import requests

IPQS_API_KEY = "YOUR_API_KEY_HERE"

def ipqs_lookup(phone_number):
    url = f"https://www.ipqualityscore.com/api/json/phone/{IPQS_API_KEY}/{phone_number}"
    try:
        response = requests.get(url)
        data = response.json()

        if not data.get("success"):
            print("❗ IPQS error:", data.get("message", "Unknown error"))
            return {}

        return {
            "IPQS Formatted": data.get("formatted"),
            "Local Format": data.get("local_format"),
            "Valid (IPQS)": data.get("valid"),
            "Fraud Score": data.get("fraud_score"),
            "Recent Abuse": data.get("recent_abuse"),
            "VOIP": data.get("VOIP"),
            "Prepaid": data.get("prepaid"),
            "Risky": data.get("risky"),
            "Active": data.get("active"),
            "Active Status": data.get("active_status"),
            "Owner Name": data.get("name"),
            "Line Type": data.get("line_type"),
            "IPQS Carrier": data.get("carrier"),
            "Country": data.get("country"),
            "Region": data.get("region"),
            "City": data.get("city"),
            "Zip Code": data.get("zip_code"),
            "Timezone (IPQS)": data.get("timezone"),
            "Dialing Code": data.get("dialing_code"),
            "Do Not Call List": data.get("do_not_call"),
            "Spammer": data.get("spammer"),
            "Leaked": data.get("leaked"),
            "User Activity": data.get("user_activity"),
        }

    except Exception as e:
        print(f"❗ Error contacting IPQS: {e}")
        return {}

def get_number_info(mobileNo_str):
    try:
        mobileNo = phonenumbers.parse(mobileNo_str)
        info = {
            "Input": mobileNo_str,
            "Formatted": phonenumbers.format_number(mobileNo, PhoneNumberFormat.E164),
            "Time Zones": timezone.time_zones_for_number(mobileNo),
            "Carrier": carrier.name_for_number(mobileNo, "en"),
            "Region": geocoder.description_for_number(mobileNo, "en"),
            "Country Code": mobileNo.country_code,
            "Number Type": number_type(mobileNo),
            "Valid (Local)": phonenumbers.is_valid_number(mobileNo),
            "Possible": phonenumbers.is_possible_number(mobileNo)
        }

        # Add IPQS data
        ipqs_data = ipqs_lookup(mobileNo_str)
        info.update(ipqs_data)

        print("\n📞 Phone Number Details:")
        for key, value in info.items():
            print(f"{key}: {value}")

        return info

    except phonenumbers.NumberParseException as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❗ Unexpected error: {e}")
    return None

def save_to_csv(info, filename="phone_log.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=info.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(info)
        print("📁 Info saved to", filename)

if __name__ == "__main__":
    while True:
        number = input("\nEnter phone number in international format (or type 'exit'): ").strip()
        if number.lower() == 'exit':
            break
        info = get_number_info(number)
        if info:
            save = input("Do you want to save this info to CSV? (y/n): ").strip().lower()
            if save == 'y':
                save_to_csv(info)
