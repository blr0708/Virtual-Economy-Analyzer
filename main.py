import requests
from bs4 import BeautifulSoup
import time
import json
import os
import re

TARGET_ITEMS = ["Kamień", "Runa", "Kryształ", "TM", "TR"]

def get_market_data(session, category, max_pages):
    items = []
    print(f"\nSkanowanie kategorii: [{category.upper()}]")

    for page in range(1, max_pages + 1):
        url = f"https://gra.pokewars.pl/targ/{category}/{page}"
        resp = session.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')

        table = soup.find('table', class_='center')

        if not table: break

        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')

            if len(cols) >= 4:
                raw_name = cols[1].get_text(separator=' ', strip=True)
                name = ' '.join(raw_name.split())

                price_cell = cols[3].get_text(separator=' ', strip=True)

                link_tag = cols[-1].find('a', href=True)
                offer_id = re.search(r'/(\d+)$', link_tag['href']).group(1) if link_tag else None

                if offer_id:
                    yen_match = re.search(r'([\d.]+)\s*¥', price_cell)
                    ph_match = re.search(r'([\d.]+)\s*£', price_cell)

                    item_info = {"id": offer_id, "name": name}

                    if yen_match: item_info["price_yen"] = int(yen_match.group(1).replace('.', ''))
                    if ph_match: item_info["price_ph"] = int(ph_match.group(1).replace('.', ''))

                    items.append(item_info)

        time.sleep(0.3)

    return items


print("Witaj w PokeBot!")
user_input = input("Ile stron targu chcesz przeskanowac w kazdej kategorii? (Wcisnij Enter, aby domyslnie 10): ")
max_pages = int(user_input) if user_input.isdigit() else 10
print(f"Rozpoczynam skanowanie {max_pages} stron...")

session = requests.Session()

login_data = {"login": "YOUR_EMAIL", "pass": "YOUR_PASSWORD", "zaloguj": "Zaloguj"}
session.post("https://gra.pokewars.pl/auth", data=login_data)

current_market = (
        get_market_data(session, "przedmioty", max_pages) +
        get_market_data(session, "tm", max_pages) +
        get_market_data(session, "tr", max_pages)
)

print("\nAnaliza sprzedanych towarow:")
sold_report = []

if os.path.exists("market_memory.json"):
    with open("market_memory.json", "r", encoding='utf-8') as f:
        old_market = json.load(f)

    old_items_dict = {item['id']: item['name'] for item in old_market if 'id' in item}

    current_ids = {item['id'] for item in current_market}
    sold_ids = set(old_items_dict.keys()) - current_ids

    for s_id in sold_ids:
        sold_report.append(old_items_dict[s_id])

    if sold_report:
        print(f"  KUPIONO W SUMIE: {len(sold_report)} szt.")
        for name in set(sold_report):
            print(f"    - {name}: {sold_report.count(name)} szt.")
    else:
        print("  Brak nowej sprzedazy.")
else:
    print("  Pamiec pusta. Zaczynam monitorowac.")

with open("market_memory.json", "w", encoding='utf-8') as f:
    json.dump(current_market, f, ensure_ascii=False)

best_deals = []

for item in current_market:
    if "price_yen" in item and "price_ph" in item:
        if any(target in item["name"] for target in TARGET_ITEMS):
            ratio = item["price_yen"] / item["price_ph"]

            if ratio > 1000:
                best_deals.append((item['name'], item['price_yen'], ratio))

best_deals.sort(key=lambda x: x[2], reverse=True)

with open("last_report.txt", "w", encoding='utf-8') as f:
    f.write("RAPORT Z TARGU POKEWARS\n\n")

    if sold_report:
        f.write(f"Zanotowano sprzedaz {len(sold_report)} przedmiotow od ostatniego skanowania.\n")
        f.write("Kupione przedmioty:\n")
        for name in set(sold_report):
            f.write(f"- {name}: {sold_report.count(name)} szt.\n")
    else:
        f.write("Brak nowych sprzedazy.\n")

    f.write("\nNAJLEPSZE INWESTYCJE PUNKTOW HONORU W YENY:\n")
    for name, price, ratio in best_deals[:15]:
        f.write(f"Przedmiot: {name}. Kurs: {int(ratio)} Yen za 1 PH.\n")

print("\nSkrypt zakonczyl prace.")
print("Raport zapisany w pliku last_report.txt")