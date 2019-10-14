# Radius

A program that sends a list of profiles nearby.

Has a CLI version that uses **`data.csv`** as a "database" to query distance from.

HTTP interface has the following API endpoints defined:

| HTTP Method | End-point | Action |
|-------------|-----------|--------|
| POST | **`/api/profiles/create`** | Create a profile as<br/>**`{'longitude': longitude_in_degrees, 'latitude': latitude_in_degrees}`** |
|GET | **`/api/profiles/nearby/<int:profile_id>?distance=distKms`** | Retrieve profiles near a specified distance |
|PUT | **`/api/profiles/update/<int:profile_id>`** | Update a profile's location as<br/>**`{'longitude': longitude_in_degrees, 'latitude': latitude_in_degrees}`** |
|DELETE | **`/api/profiles/delete/<int:profile_id>`** | Delete a profile |

Useful resources regarding this project:

* [Great-circle distance - Wikipedia](https://en.wikipedia.org/wiki/Great-circle_distance)
* [Finding Points Within a Distance of a Latitude/Longitude Using Bounding Coordinates](http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates)
* [Designing a RESTful API with Python and Flask](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)
* [Examples -- PyMySQL 0.7.2 documentation ](https://pymysql.readthedocs.io/en/latest/user/examples.html)
* [PyMySQL tutorial - Python MySQL programming with PyMySQL module](http://zetcode.com/python/pymysql/)
* [What is CRUD | Codecademy](https://www.codecademy.com/articles/what-is-crud)
