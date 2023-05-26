import requests
import json
import win10toast
import sqlite3

toast = win10toast.ToastNotifier()

key = "e60c16bd-fcc3-4b8b-8e1b-d50cb0b6de09"

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"


headers = {
    "X-CMC_PRO_API_KEY": key,
    "Accept": "application/json"
}


params = {
    "limit": 10
}

response = requests.get(url, headers=headers, params=params)
cryptos = []

conn = sqlite3.connect("crypto.db")
cursor = conn.cursor() 

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cryptocurrencies (
        id INTEGER PRIMARY KEY,
        name TEXT,
        symbol TEXT,
        price REAL
    )
''')

if response.status_code == 200:
    data = response.json()

    if "data" in data:
        for crypto in data["data"]:
            name = crypto["name"]
            symbol = crypto["symbol"]
            price = crypto["quote"]["USD"]["price"]
            x = f"{name} ({symbol}): ${price:.2f}"
            cryptos.append(x)
            cursor.execute('INSERT INTO cryptocurrencies (name, symbol, price) VALUES (?, ?, ?)',
                           (name, symbol, price))
            print(x)



else:
    print("Error:", response.status_code)
top_one = cryptos[0]
toast.show_toast(title="Today's Top 1 Crypto is 💸", msg=top_one, duration=5)


conn.commit()
conn.close()

with open("crypto_data.json", "w") as file:
    json.dump(cryptos, file, indent=4)

