# Radius

A program that matches property listing to requirements and Vice Versa. The project has two interfaces HTTP and CLI. Currently HTTP interface is a work in progress and CLI is functional.

## Set-up

(Runs on Python 2.7)
1. Install **`mysql-server`**, **`python-mysqldb`** and **`redis`**.
```bash
sudo apt install mysql-server python-mysqldb redis
```
2. Install python dependencies.
```bash
pip install --upgrade -r requirements.txt
```

## Usage

1. Run MySQL as root and create a user at **`localhost`** with root privileges. Create a database named **'radius'**.
```bash
sudo mysql
mysql > CREATE USER '{user}'@'localhost' INDENTIFIED BY '{password}';
mysql > GRANT ALL PRIVILEGES ON * . * TO '{user}'@'localhost';
mysql > FLUSH PRIVILEGES;
mysql > CREATE DATABASE radius;
```
2. Run **`radius.sql`**.
```bash
mysql -u{user} radius -p < radius.sql
```
2. Create a .env file within the directory as follows:
```
DB_USER='{user}'
DB_HOST='localhost'
DB_PASSWORD='{password}'
DB_NAME='radius'
```
3. Run **`insert_demo_data.py`**, then **`cli.py`** for the CLI interface.
```bash
python insert_demo_data.py
python cli.py
```

## Radius in action

![Screenshot of CLI in action](https://uc56affad0d497d944cc2682cfe4.previews.dropboxusercontent.com/p/thumb/AAgdIXUhcIjPL5HD9BSaxoU6bMHDzUBn01jWPR0ANkzQxeQ6p62dms333sOxa7DnK18IkjcbStgzMjupuXG3uOImIOFbDpNshXh1KioelnunaKl364xVF0rHd9XGjSQrzIITssYgCFcANeD1qEn-TnDfMF968QoFyQEK36iZbE2Yp396jKy03yT_vrVcC7WWQIrjLPfdrUjpsy4qDiuVz3BLIzRzoJ2EmKsBUSL67J-ZbWlQH-LqQcCTCaAMJVgWtD9U_saEt2DDkSu_LaD_hNgJNMRoS6-Iho7JzunrIshIY35AnUfBV_cjWAEP1IdJNjqwWimliWMncOUX5MGf65U-G8PgkhJFge-34LZv3gnQTiwmZ4m8b15_zpwuPGaslFJrWb6d6HIxqo9dFHz92YEd1bmGTzyL51eLebTU2sLmJjZVM9hFB4ANY9waI2tkrpZmdpZlqHk6OUs_iXjuZOkZ/p.png?fv_content=true&size_mode=5)
[Link to screenshot.](https://www.dropbox.com/s/762f5h2h2yjwv1x/Screenshot%202019-02-10%2023.32.55.png?dl=0)

## Dataset

Have used Location data set of starbucks in US to generate dummy data for requirements and properties.

## Distance Calculation

This program uses Bounding box method for filtering out most of the non matching locations and once the working set is limited, Haversine Formula is used to calculate distance. All the lat/long are stored in radians to avoid doing the conversions at runtime on SQL server.

## Database Indexes

Properties and requirements both have (long,lat,id) as primary key. The Btree indexes make the range queries exetremely performant. Other than the primary index the tables also have secondary B-Tree index on price,bedroom,bathroom. And Hash Index on id for fast lookup by ID.

## Performance

Tested for 8 Million Properties and 1 million Requirements on 1GB/Single Core/SSD server
<ol type="A">
	<li>Response time Without Cache  ~13.02 ms</li>
	<li>Response time with cache but cache miss ~22.34 ms</li>
	<li>Response time when cache hit ~2ms</li>
</ol>

### Scope of improvement -
<ol type="A">
	<li>Mysql query performance can be improved to some extent by using int instead of float/double to store lat/long</li>
	<li>Response time in cache miss can be improved by choosing a more compact and fast data serialization to and from redis</li>
	<li>Response time in case of Cache hit can be improved by caching requirements by id, however that will need more memory</li>
</ol>

## Improvement in % Cache hits

Currently the results from SQL are cached with md5 of sql query. Cache hits can be increased by careful and more granular caching of results.

## Alternate Approach

If blazing fast queries are a necessitiy and there is scope for prewarming the cache then queries to SQL server can be completely avoided by Storing everything in sorted sets and building the cache incrementally as and when the requirements/properties come in. Works best if the system is not write heavy. Difficult to maintain and in case of server failure warming the cache takes time. Can be Used only when you have another server up and running on hot standby.

I have been using a variant of this approach in production for serving 2.5 billion responses per day in a geo distributed system. This approach seems like an overkill for the problem statement in consideration hence not chosen.
