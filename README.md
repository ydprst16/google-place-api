# Google Place API Data Scraper

## Description
This project is a Python script that retrieves location data from various strategic points in Dumai using the **Google Places API**. The script collects information such as place name, address, subdistrict, district, rating, number of reviews, business status, phone number, and website.

## Features
- Fetch data from **Google Places API** based on location coordinates.
- Search for various types of places such as restaurants, banks, schools, and more.
- Save results in **Excel (.xlsx)** and **CSV (.csv)** formats.
- Supports **pagination** to retrieve more data from the API.
- Extract **subdistrict** and **district** from addresses using regular expressions.

## Prerequisites
Ensure you have:
- **Python 3.x** installed on your system.
- An API Key from **Google Places API**.
- Required Python modules installed:
  ```bash
  pip install requests pandas openpyxl
  ```

## Usage
1. **Replace your API Key** in the script:
   ```python
   API_KEY = "YOUR_API_KEY"
   ```
2. **Run the Python script** using the command:
   ```bash
   python script.py
   ```
3. The data will be saved in the following formats:
   - `g_places_data_YYYY-MM-DD.xlsx`
   - `g_places_data_YYYY-MM-DD.csv`

## Data Structure
The script collects the following information for each place:
- **Place Name**
- **Full Address**
- **Subdistrict**
- **District**
- **Rating**
- **Number of Reviews**
- **Business Status**
- **Phone Number**
- **Website**
- **Coordinates (Latitude & Longitude)**

## Covered Locations
By default, the script retrieves data from various strategic points in **Dumai**, such as **Bagan Besar, Bukit Kayu Kapur, Kampung Baru**, and more.

## Place Types Searched
The script fetches various place categories from the Google Places API, such as:
- **Restaurants, Banks, Gas Stations, Schools, Hospitals, Pharmacies, Supermarkets, Hotels**, and more.

## Notes
- Google Places API has a **daily quota limit**. Ensure you monitor your quota usage.
- If the returned data is insufficient, the script will use **pagination** to fetch additional data.

## License
This project is licensed under the **MIT License**. Feel free to use and modify it as needed.

---
