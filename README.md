# Radius

A program that matches property listing to requirements and Vice Versa
## Dataset
Have used Location data set of starbucks in US to generate dummy data for requirements and properties

## Distance Calculation

This program uses Bounding box method for filtering out most of the non matching locations and once the working set is limited,
Hoversine Formula is used to calculate distance. All the lat/long are stored in radians to avoid doing the conversions at 
runtime on SQL server

## Database Indexes

Properties and requirements both have (long,lat,id) as primary key. The Btree indexes make the range queries exetremely performant. Other than the
primary index the tables also have secondary B-Tree index on price,bedroom,bathroom. And Hash Index on id for fast lookup by ID


## Performance

Tested for 8 Million Properties and 1 million Requirements
- (A) - Response time Without Cache  ~13.02 ms
- (B) - Response time with cache but cache miss ~22.34 ms
- (C) - Response time when cache hit ~2ms

### Scope of improvement -
- (A) - Mysql query performance can be improved to some extent by using int instead of float/double to store lat/long
- (B) - Response time in cache miss can be improved by choosing a more compact and fast data serialization to and from redis
- (C) - Response time in case of Cache hit can be improved by caching requirements by id, however that will need more memory

### Improvement in % Cache hits -
Currently the results from SQL are cached with md5 of sql query. Cache hits can be increased by careful and more 
granular caching of results

### Alternate Approach -

If blazing fast queries are a necessitiy and there is scope for prewarming the cache then queries to SQL server can be completely
Avoided by Storing everything in sorted sets and building the cache incrementally as and when the requirements/properties come in.
Works best if the system is not write heavy. Difficult to maintain and in case of server failure warming the cache takes time.
Can be Used only when you have another server up and running on hot standby

I have been using a variant of this approach in production for serving 2.5 billion responses per day in a geo distributed system.
This approach seems like an overkill for the problem statement in consideration hence not chosen.

