# kasatomaru
Facilitate access, search and analysis of japanese immigration to Brazil

TODO List:
- Extracted family pages, but there are gaps in there
- Need to resolve the gaps. I started getting data from japanese names pages in order to check if the japanese name matches, but it does not seen to be working well. As a next step, we need to check how to combine main data with family data in order to have all data together and useful.


# HOW TO

# First Step - Get the pages (Crawler):

execute:
```
PYTHONPATH=. python crawler/exec.py
```
Consider these options in the __main__:
## 1) get the main pages of portuguese language
```
get_main_pages(PORTUGUESE)
```
## 2) get the main pages of japanese language
```
get_main_pages(JAPANESE)
```
## 3) get the family pages
```
get_family_pages()
```

# Second Step (Process):

Create the sqlite database:
Uncomment create_db() method in db.py __main__.
execute:
```
PYTHONPATH=. python db.py
```

## Then uncomment in process/extract.py:
You have to uncomment the following methods in __main__ in process/extract.py in order to have the results described in the numbered items below and execute:
```
PYTHONPATH=. python process/extract.py
```

### 1) extract the main pages of portuguese language and insert into table person in kasatomaru.db
- extract_main_pages(PORTUGUESE)

### 2) extract the main pages of japanese language and insert into table person_jp in kasatomaru.db

- extract_main_pages(JAPANESE)

### 3) extract the family content (only farm and station) and insert into table person in kasatomaru.db

- extract_family_content()


# Third Step:

Insert kanji names into person table:

Uncomment the following method in __main__ in db.py: 
- insert_japanese_name_into_person() 

And execute:
```
PYTHONPATH=. python db.py
```

################################

# To run the webserver

- uvicorn app.main:app --reload

###############################

# TODO

- Query of families based on date
- Query based on ship
- Query based on origin
- Query based on destination
