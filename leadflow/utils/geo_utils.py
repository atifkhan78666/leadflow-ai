def get_region_from_location(location):

    if not location:
        return None

    location = location.lower()

    if "india" in location or "delhi" in location or "mumbai" in location:
        return "IN"

    if "dubai" in location or "uae" in location:
        return "AE"

    if "united states" in location or "usa" in location or "new york" in location:
        return "US"

    if "uk" in location or "london" in location or "england" in location:
        return "GB"

    if "canada" in location or "toronto" in location:
        return "CA"

    if "australia" in location or "sydney" in location:
        return "AU"

    return None