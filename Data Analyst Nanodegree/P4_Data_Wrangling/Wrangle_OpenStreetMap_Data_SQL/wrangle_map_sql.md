
# Wrangle OpenStreetMap Data

The purpose of this project is to audit, clean, improve and analyse the data of a large map xml file applying:
* Python 3.6.0 techniques, and
* SQL queries.

## Map Area

San Jose, California, United States map extract from Mapzen website:
* [https://mapzen.com/data/metro-extracts/metro/san-jose_california/](https://mapzen.com/data/metro-extracts/metro/san-jose_california/)

Although I live in Thessaloniki city, Greece, the map extract of this area is quite small and incomplete for the purposes of this project. So, I chose to investigate San Jose map area.

## Get Sample Data

The original uncompressed map extract file size (san-jose_california.osm) is quite large (352.6 MB). In order to audit the map for problems, a smaller sample of this file was generated with "get_sample.py".

## Problems Found from Auditing the Map

After creating the "sample.osm" file and running it against a provisional "data_init.py" file, the following major problems were addressed.
### Overabbreviated street names
Auditing the database, it can be found many instances with street names in various formats such as "Palm Valley Blvd" and "Santa Teresa Boulevard".


```python
SELECT tags.value 
FROM (SELECT * FROM nodes_tags 
      UNION ALL 
      SELECT * FROM ways_tags) as tags
WHERE tags.key='street';
```

### Inconsistent phone numbers

Querying the database, it was found several phone number entries in different formats.


```python
SELECT tags.value 
FROM (SELECT * FROM nodes_tags 
      UNION ALL 
      SELECT * FROM ways_tags) as tags
WHERE tags.key='phone';
```

408-377-0190

(408)224-3293

+1-408-654-9860

4087388761

408 358 5895

+1 408 9745050

### Inconsistent postcodes

Querying for postcodes, most of the entries seems to be in the right format. However, there are still some codes in different format.


```python
SELECT tags.value 
FROM (SELECT * FROM nodes_tags 
      UNION ALL 
      SELECT * FROM ways_tags) as tags
WHERE tags.key='postcode';
```

95014-2522

CA 95110

95008

## Clean the Data
### Update Street Names
Using the following mapping, streets were updated before imported to the database. Data cleaning was applied with "data.py" script and then, the created csv files were imported to "san-jose_california.db" using "create_db_from_csv.py" file.


```python
mapping = {'Ave'   : 'Avenue',
           'ave'   : 'Avenue',
           'Blvd'  : 'Boulevard',
           'Cir'   : 'Circle',
           'Ct'    : 'Court',
           'court' : 'Court',
           'Dr'    : 'Drive',
           'Hwy'   : 'Highway',
           'Ln'    : 'Lane',
           'Rd'    : 'Road',
           'Sq'    : 'Square',
           'St'    : 'Street',
           'street': 'Street',
           }
```

### Fix the Phone Numbers
Phone numbers were converted to the international format:

+1 XXX-XXX-XXXX

using the following code:


```python
def update_phone(phone):
    # Remove non number characters, such as "(".
    phone = re.sub('\D', '', phone)
    # Add USA phone code "+1".
    if len(phone) == 11:
        phone = '+' + phone
    if len(phone) == 10:
        phone = '+1' + phone
    
    if len(phone) == 12:
        phone = phone[0:2] + ' ' + phone[2:5] + '-' + phone[5:8] + '-' + phone[8:12]
    
    return phone
```

### Update Postcodes
Codes with 5-digits or the ZIP+4 Code 9-digits format are considered valid. Only the codes with "CA" prefix were updated to the 5-digits format.


```python
def update_postcode(postcode):
    # Remove "CA".
    if re.findall('CA ', postcode):
        postcode = re.sub('CA ', '', postcode)
    return postcode
```

## Data Overview
### Files


```python
san-jose_california.osm       336M
san-jose_california.db        188M
nodes.csv                     128M
ways_nodes.csv                43M
ways_tags.csv                 23M
ways.csv                      12M
nodes_tags.csv                3M
```

### Queries
Query San Jose database and get useful information running "quiries.py" script.
#### Number of nodes


```python
SELECT COUNT(*) FROM nodes;
```

1617471

#### Number of ways


```python
SELECT COUNT(*) FROM ways;
```

213531

#### Number of unique users


```python
SELECT COUNT(DISTINCT(e.uid))
FROM (SELECT uid FROM nodes
      UNION ALL
      SELECT uid FROM ways) as e;
```

1375

#### Number of users appearing only once


```python
SELECT COUNT(*)
FROM (SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes
      UNION ALL SELECT user FROM ways) as e
GROUP BY e.user HAVING num=1)  u;
```

306

#### Top 5 contributing users


```python
SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes
      UNION ALL SELECT user FROM ways) as e
GROUP BY e.user ORDER BY num DESC LIMIT 5;
```

andygol

nmixter

mk408

Bike Mapper

samely

#### Top 5 amenities


```python
SELECT value, COUNT(*) as num
FROM nodes_tags WHERE key="amenity"
GROUP BY value ORDER BY num DESC LIMIT 5;
```

restaurant

fast_food

bench

cafe

place_of_worship

#### Top 5 cuisine


```python
SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value ="restaurant") as i
ON nodes_tags.id = i.id WHERE nodes_tags.key ="cuisine"
GROUP BY nodes_tags.value ORDER BY num DESC LIMIT 5;
```

chinese

vietnamese

mexican

pizza

japanese

#### Top 5 cafes


```python
SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value ="cafe") as i
ON nodes_tags.id = i.id WHERE nodes_tags.key ="name"
GROUP BY nodes_tags.value ORDER BY num DESC LIMIT 5;
```

Starbucks

Peet's Coffee & Tea

Subway

Peet's Coffee

Starbucks Coffee

#### Top 3 banks


```python
SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value ="bank") as i
ON nodes_tags.id = i.id WHERE nodes_tags.key ="name"
GROUP BY nodes_tags.value ORDER BY num DESC LIMIT 3;
```

Chase

Bank of America

Wells Fargo

#### Top 2 religions


```python
SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value ="place_of_worship") as i
ON nodes_tags.id = i.id WHERE nodes_tags.key ="religion"
GROUP BY nodes_tags.value ORDER BY num DESC LIMIT 2;
```

christian

buddhist

#### Top 10 users contribution percentage


```python
query1 = 'SELECT SUM(num) FROM (SELECT e.user, COUNT(*) as num FROM \
        (SELECT user FROM nodes UNION ALL SELECT user FROM ways) as e \
        GROUP BY e.user ORDER BY num DESC LIMIT 10);'

query2 = 'SELECT SUM(num) FROM (SELECT e.user, COUNT(*) as num FROM \
        (SELECT user FROM nodes UNION ALL SELECT user FROM ways) as e \
        GROUP BY e.user);'

c.execute(query1)
top10 = c.fetchone()[0]
    
c.execute(query2)
total = c.fetchone()[0]

percentage = round(top10*100/total, 0)
```

65.0%

## Conclusions
San Jose map is quite large, complete and clean. However, after auditing, it was still found and fixed several problems such as:
* Overabbreviated street names
* Inconsistent phone numbers
* Inconsistent postcodes

Areas of improvement:
* Apply an automatic system of language spelling correction to prevent from inevitable user errors.
* Promote standard ways of data input.

As it was shown, probably there isn't any standard way to enter streets, phone numbers, postcodes or even websites:


```python
SELECT tags.value 
FROM (SELECT * FROM nodes_tags 
      UNION ALL 
      SELECT * FROM ways_tags) as tags
WHERE tags.key='website';
```

www.moorevalue.com

http://7-eleven.com

### Suggested Solutions, Benefits and Anticipated Issues
* Required fields combined with drop down lists, which for example can hold valid values for adding a street type (e.g. Avenue, Way, Street etc.), could help users entering data in a particular format.
* An additional way to enforce valid syntax could be using patterns inside input fields.

As OpenStreetMap is an open source project done by volunteers, anybody can enter anything he or she wishes. The previous suggested solutions could be integrated into a general management system of "Good Practice" methods. This system could increase the quality and value of map data. However, since nobody is forced to follow it, there might be cases where the solutions don't apply, or even contradict each other. Moreover, restricted actions such as the required fields and patterns, might discourage users from contribution. As other classmates suggested, "gamification" could improve user engagement and input quality, albeit this might arise extra potential costs and efforts for implementation, maintenance and monitoring.

## References
[https://discussions.udacity.com](https://discussions.udacity.com)

[https://gist.github.com](https://gist.github.com)

[https://stackoverflow.com](https://stackoverflow.com)

[https://www.sqlite.org/datatype3.html](https://www.sqlite.org/datatype3.html)

[http://hosseinkaz.blogspot.gr/2014/11/importing-csv-file-into-sqlite3-python.html](http://hosseinkaz.blogspot.gr/2014/11/importing-csv-file-into-sqlite3-python.html)

[http://www.sqlitetutorial.net/sqlite-python/create-tables/](http://www.sqlitetutorial.net/sqlite-python/create-tables/)

[https://www.dotnetperls.com/sort-file-size-python](https://www.dotnetperls.com/sort-file-size-python)

[https://en.wikipedia.org/wiki/List_of_postal_codes](https://en.wikipedia.org/wiki/List_of_postal_codes)
