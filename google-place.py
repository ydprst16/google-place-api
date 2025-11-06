import requests
import time
import pandas as pd
import re
from datetime import datetime

# GANTI DENGAN API KEY KAMU
API_KEY = "YOUR_API_KEYY"

# List titik koordinat strategis di Dumai
locations = [
    (1.588437, 101.3912735),  # Bagan Besar
    (1.5808259, 101.4005474),  # Bagan Besar Timur
    (1.5003627, 101.3468862),  # Bukit Kayu Kapur
    (1.5562285, 101.3866184),  # Bukit Nenas
    (1.5205067, 101.4757765),  # Gurun Panjang
    (1.5332851, 101.3927816),  # Kampung Baru
    (1.6856124, 101.370857),   # Bagan Keladi
    (1.6801355, 101.425387),   # Pangkalan Sesai
    (1.6989022, 101.4010688),  # Purnama, Dumai
    (1.6731389, 101.4198727),  # Simpang Tetap Darul Ichsan
    (1.6702754, 101.44686),    # Bintan
    (1.6806809, 101.4450199),  # Dumai Kota
    (1.6807341, 101.4392406),  # Laksamana
    (1.6728315, 101.4371615),  # Rimba Sekampung
    (1.6733689, 101.4446509),  # Sukajadi
    (1.6475861, 101.4094327),  # Bukit Datuk
    (1.627649, 101.3948427),   # Bukit Timah
    (1.6539581, 101.4386269),  # Bumi Ayu
    (1.6378145, 101.3780079),  # Mekar Sari
    (1.6662666, 101.420537),   # Ratu Sima
    (1.6445171, 101.4543235),  # Bukit Batrem
    (1.6819825, 101.4575975),  # Buluh Kasap
    (1.6589173, 101.4602774),  # Jaya Mukti
    (1.6660041, 101.4727817),  # Tanjung Palas
    (1.6724979, 101.4549201),  # Teluk Binjai
    (1.6339644, 101.5678567),  # Guntung
    (1.6573867, 101.5018794),  # Mundam
    (1.6237443, 101.586724),   # Pelintung
    (1.6388913, 101.5279494),  # Teluk Makmur
    (1.7271523, 101.3741413),  # Bangsal Aceh
    (1.9074315, 101.2497062),  # Basilam Baru
    (1.8638912, 101.2669618),  # Batu Teritip
    (1.7688131, 101.3513028),  # Lubuk Gaung
    (1.8066847, 101.3166349),  # Tanjung Penyembal
    (1.9446212,	101.3058045),  # Sungai Geniot

]

# List berbagai jenis tempat yang ingin diambil
place_types = [
    "accounting", "airport", "amusement_park", "aquarium", "art_gallery", "atm", "bakery", "bank", "bar",
    "beauty_salon", "bicycle_store", "book_store", "bowling_alley", "bus_station", "cafe", "campground",
    "car_dealer", "car_rental", "car_repair", "car_wash", "casino", "cemetery", "church", "city_hall",
    "clothing_store", "convenience_store", "courthouse", "dentist", "department_store", "doctor", "drugstore",
    "electrician", "electronics_store", "embassy", "fire_station", "florist", "funeral_home", "furniture_store",
    "gas_station", "gym", "hair_care", "hardware_store", "hindu_temple", "home_goods_store", "hospital",
    "insurance_agency", "jewelry_store", "laundry", "lawyer", "library", "light_rail_station", "liquor_store",
    "locksmith", "lodging", "meal_delivery", "meal_takeaway", "mosque", "movie_rental",
    "movie_theater", "moving_company", "museum", "night_club", "painter", "park", "parking", "pet_store", "pharmacy",
    "physiotherapist", "plumber", "police", "post_office", "primary_school", "real_estate_agency", "restaurant",
    "roofing_contractor", "rv_park", "school", "secondary_school", "shoe_store", "shopping_mall", "spa", "stadium",
    "storage", "store", "subway_station", "supermarket", "synagogue", "taxi_stand", "tourist_attraction",
    "train_station", "transit_station", "travel_agency", "university", "veterinary_care", "zoo"
]

# Endpoint Google Places API
NEARBY_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
DETAILS_API_URL = "https://maps.googleapis.com/maps/api/place/details/json"

# Simpan hasil dalam list
all_places = []

# Fungsi untuk ekstrak kelurahan dan kecamatan
def extract_kelurahan_kecamatan(address: str) -> tuple:
    """
    Ekstrak kelurahan dan kecamatan dari alamat tanpa mengubah format kelurahan.
    """
    match = re.search(r"\s*([\w\.]+\s*[A-Za-z\s]+?),\s*Kec\.\s*([A-Za-z\s]+)", address)
    
    if match:
        kelurahan = match.group(1).strip()  # Ambil kelurahan tanpa modifikasi
        kecamatan = match.group(2).strip()  # Ambil kecamatan tanpa "Kec."
        return kelurahan, kecamatan

    return None, None

# Fungsi untuk request data dari Nearby Search API
def fetch_places_nearby(lat, lng, place_type, next_page_token=None):
    params = {
        "location": f"{lat},{lng}",
        "rankby": "distance",
        #"radius": 10000,
        "type": place_type,
        "key": API_KEY
    }
    if next_page_token:
        params["pagetoken"] = next_page_token

    response = requests.get(NEARBY_SEARCH_URL, params=params)
    data = response.json()

    if "results" in data:
        for place in data["results"]:
            # Ambil detail tambahan dari Place Details API
            details = fetch_place_details(place["place_id"])
            full_address = details.get("formatted_address", place.get("vicinity", ""))

            # Ekstrak kelurahan dan kecamatan
            kelurahan, kecamatan = extract_kelurahan_kecamatan(full_address)

            all_places.append({
                "type": place_type,
                "place_id": place.get("place_id", ""),
                "name": place.get("name", ""),
                "address": full_address,
                "kelurahan": kelurahan,
                "kecamatan": kecamatan,
                "rating": place.get("rating", 0),
                "total_reviews": place.get("user_ratings_total", 0),
                "business_status": place.get("business_status", ""),
                "phone": details.get("formatted_phone_number", ""),
                "website": details.get("website", ""),
                "latitude": place["geometry"]["location"]["lat"],
                "longitude": place["geometry"]["location"]["lng"]
            })

    return data.get("next_page_token", None)

# Fungsi untuk mengambil nomor telepon & website dari Place Details API
def fetch_place_details(place_id):
    params = {
        "place_id": place_id,
        "fields": "formatted_phone_number,website,formatted_address",
        "key": API_KEY
    }
    response = requests.get(DETAILS_API_URL, params=params)
    data = response.json()
    return data.get("result", {})

# Looping untuk setiap type dan lokasi strategis di Dumai
for place_type in place_types:
    for lat, lng in locations:
        print(f"Fetching data for type '{place_type}' at location: {lat}, {lng}")

        next_page_token = None
        while True:
            next_page_token = fetch_places_nearby(lat, lng, place_type, next_page_token)
            if not next_page_token:
                break  # Jika tidak ada next_page_token, hentikan loop
            time.sleep(2)  # Kurangi delay agar lebih cepat

# Simpan ke DataFrame
df = pd.DataFrame(all_places)

# Format nama file berdasarkan tanggal
tanggal = datetime.now().strftime("%Y-%m-%d")

# Simpan ke Excel
excel_filename = f"g_places_data_{tanggal}.xlsx"
df.to_excel(excel_filename, index=False)

# Simpan ke CSV
csv_filename = f"g_places_data_{tanggal}.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8-sig")

print(f"Data tempat berhasil disimpan ke '{excel_filename}' dan '{csv_filename}'.")
print(f"Total data dikumpulkan: {len(all_places)}")
