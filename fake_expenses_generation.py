from faker import Faker
import pandas as pd
import random
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("BINGCHILLING")

fake = Faker()
data = []

def get_ip_risk_score(ip):
    url = f"https://ipqualityscore.com/api/json/ip/{API_KEY}/{ip}"
    try:
        response = requests.get(url)
        result = response.json()

        return {
            "fraud_score": result.get("fraud_score", 0),  # returns a number from 0 (safe) to 100 (risky)
            "is_proxy": result.get("proxy", False),  # true/false if proxy
            "is_vpn": result.get("vpn", False),  # true/false if vpn
            "is_tor": result.get("tor", False)  # true/false if tor was used
        }
    except Exception as e:
        print(f"API Error for IP {ip}: {e}")
        return {"fraud_score": 0, "is_proxy": False, "is_vpn": False, "is_tor": False} # returns safe values if there is an error

# loop to create fake transaction data, restricted to 100 due to API rate limits
for _ in range(100):
    ip = fake.ipv4_public()
    risk = get_ip_risk_score(ip)
    data.append({
        'date': fake.date_this_year(),
        'vendor': fake.company(),
        'amount': round(random.uniform(5, 500), 2),
        'category': random.choice(['Food', 'Travel', 'Utilities', 'Shopping', 'Health']),
        'ip_addresss': ip,
        'fraud_score': risk['fraud_score'],
        'is_proxy': risk['is_proxy'],
        'is_vpn': risk['is_vpn'],
        'is_tor': risk['is_tor']
    })
    time.sleep(1) #prevents hitting rate limits

example_table = pd.DataFrame(data)
example_table.to_csv("ip_for_expenses.csv", index=False)
print("Data generated and saved to ip_for_expenses.csv")
