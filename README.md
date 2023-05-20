# Firebase Emulation
Personal Expense Tracker App - Firebase Emulator with a RESTful server using Flask and MongoDB Atlas

<br>
By <strong>Shih-Min (Julia) Huang</strong>

<br>

By using Python with Flask and MongoDB, this project aims to build a database server similar to Firebase. With the RESTful server, Users will be able to interact with the database - create, query, update, and delete the data - through the command-line interface.
The personal expense tracker app uses MongoDB as the database and leverages Flask to build RESTful APIs. Users will be able to enter their name, the product they purchased, the category and price of the product, and the date of the purchase.


<br>

## RESTful API and Filtering Functions:
Designed and implemented RESTful APIs based on CRUD operations to perform POST, GET, PUT, PATCH, and DELETE actions

<br>

### POST
- post_doc()
  - Create a new document and automatically generate its unique _id for identification
  - Command format:
    - curl -X POST http://127.0.0.1:9000/add/\<name>/\<date>/\<category>/\<item>/\<price>
  - Example command: 
    - curl -X POST http://127.0.0.1:9000/add/Sofia/2023-01-04/Transportation/Gas/40

  

### GET

- get_one_doc_id()
  - Search for one document by its _id
  - Command format:
    - curl -X GET http://127.0.0.1:9000/id/\<id>
  - Example command: 
    - curl -X GET http://127.0.0.1:9000/id/642cf26f714bb5917baa3730


- filter_doc()
  - Search for all documents with options to filter documents by "orderby", "limit", "skip", "asc", "startAt", "endAt":
    - orderby: set the ordering parameter
    - limit: limit the output documents
    - skip: skip the output documents
    - asc: default 1 for ascending, set -1 for descending
    - startAt: filter value larger than
    - endAt: filter value smaller than
  - Command format:
    - curl -X GET http://127.0.0.1:9000/filter?\<queryparam>
    - Example commands: 
      - curl -X GET http://127.0.0.1:9000/filter
      - curl -X GET 'http://127.0.0.1:9000/filter?orderby=date&asc=-1&skip=2&limit=4'
      - curl -X GET 'http://127.0.0.1:9000/filter?orderby=price&endAt=90&limit=3'
      - curl -X GET 'http://127.0.0.1:9000/filter?name=Jackson'
  
### PUT
- put_doc()
  - Write a new document with defined id
  - Command format:
    - curl -X PUT http://127.0.0.1:9000/add/\<id>/\<name>/\<date>/\<category>/\<item>/\<price>
  - Example command: 
    - curl -X PUT http://127.0.0.1:9000/add/16888/Anna/2023-01-04/Transportation/Gas/40



### PATCH
- update_doc()
  - Update an existing document, identified by its _id
  - Command format:
    - curl -X PATCH http://127.0.0.1:9000/update/\<id>/\<name>/\<date>/\<category>/\<item>/\<price>
  - Example command: 
    - curl -X PATCH http://127.0.0.1:9000/update/642cf25b714bb5917baa372e/Alice/2022-09-30/Transportation/Uber/20



### DELETE
- delete_doc()
  - Delete a document, identified by its _id
  - Command format:
    - curl -X DELETE http://127.0.0.1:9000/\<id>
  - Example command: 
    - curl -X DELETE http://127.0.0.1:9000/642b662a9e7bab58ac120cc6
