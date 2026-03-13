import googlemaps
import time
import requests
import re
from utils.phone_utils import clean_phone_number
from utils.geo_utils import get_region_from_location

from utils.email_extractor import extract_email

API_KEY = "GOOGLE_MAPS_API_KEY"

gmaps = googlemaps.Client(key=API_KEY)


def get_places(query, location, num_leads):

    all_results = []
    next_page_token = None

    while len(all_results) < num_leads:

        if next_page_token:
            places = gmaps.places(
                query=f"{query} in {location}",
                page_token=next_page_token
            )
        else:
            places = gmaps.places(
                query=f"{query} in {location}"
            )

        results = places.get("results", [])

        all_results.extend(results)

        next_page_token = places.get("next_page_token")

        if not next_page_token:
            break

        time.sleep(2)

    return all_results[:num_leads]


def get_place_details(place_id):

    details = gmaps.place(
        place_id=place_id,
        fields=[
            "name",
            "formatted_address",
            "formatted_phone_number",
            "website",
            "rating",
            "user_ratings_total",
            "url"
        ]
    )

    return details.get("result", {})


def scrape_leads(search_query, num_leads):
    location = search_query
    region = get_region_from_location(search_query)
    query = search_query
    places = get_places(query, location, num_leads)

    leads = []
    seen = set()

    for place in places:

        place_id = place.get("place_id")

        if place_id in seen:
            continue

        seen.add(place_id)

        details = get_place_details(place_id)

        name = details.get("name")
        address = details.get("formatted_address")
        raw_phone = details.get("formatted_phone_number")
        phone = clean_phone_number(raw_phone, region)
        website = details.get("website")
        rating = details.get("rating")
        reviews = details.get("user_ratings_total")
        maps_url = details.get("url")

        email = None

        # if website:
        #     email = extract_email(website)

        whatsapp_link = None

        if phone:
            whatsapp_link = f"https://wa.me/{phone.replace('+','')}"

        lead = {
            "Name": name,
            "Address": address,
            "Phone": phone,
            "Website": website,
            "Email": email,
            "Rating": rating,
            "Reviews": reviews,
            "Google Maps": maps_url
        }

        leads.append(lead)

    return leads

def enrich_emails(leads):
    enriched = []
    for lead in leads:
        website = lead.get("Website")
        email = lead.get("Email")
        if not email and website:
            try:
                email = extract_email(website)
            except:
                email = None
        lead["Email"] = email
        enriched.append(lead)

    return enriched