# Radius

A program that sends a list of profiles nearby.

| HTTP Method | End-point | Action |
|-------------|-----------|--------|
| POST | **`/api/profiles/create`** | Create a profile as<br/>**`{'longitude': longitude_in_degrees, 'latitude': latitude_in_degrees}`** |
|GET | **`/api/profiles/nearby/<int:profile_id>?distance=distKms`** | Retrieve profiles near a specified distance |
|PUT | **`/api/profiles/update/<int:profile_id>`** | Update a profile's location as<br/>**`{'longitude': longitude_in_degrees, 'latitude': latitude_in_degrees}`** |
|DELETE | **`/api/profiles/delete/<int:profile_id>`** | Delete a profile |
