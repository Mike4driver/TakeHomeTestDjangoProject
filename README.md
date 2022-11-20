# TestDjangoProject
This is a project made to the specifications of a companies take home assesment.
It is using Django rest framwork for the api and pytest for the testing portion and is using postgres for the database

To start the project make sure you have docker-compose installed then run:
`docker-compose up`

the api will run on port 8000 and the postgres port is 5432
You can open your `localhost:8000` in browser to interact with the API
No .env files where used for this project since it is only using default values
To run the tests that I have writen for the project while the containers are running run the following command:

`docker exec -it djangoservice pytest`

Finally here is an explination of all the api routes:
## Incrementer Routes
`/incrementer/` for keyvalue creation. Takes a post request

request:

`{
  "key":"SomeStringValue"
  "value":1 //some int value
}`

response:

`{
  "key":"SomeStringValue"
  "value":1 //some int value
}`

`/incrementer/list/` to get all keyvalue pairs. Takes a GET request.

response:
`[
  {
    "key":"SomeStringValue"
    "value":1 //some int value
  }
 ]`
 
 `/incrementer/inc/<key>/` increments value of given key. Takes PUT request
 
 response http 204 status code
 
 `/incrementer/key/<key>/` Used to preform various key operations. Takes GET, PUT, DELETE
 
 GET: returns record of key
 response:
 
`{
  "key":"SomeStringValue"
  "value":1 //some int value
}`

PUT: returns updated record of key
request:

`{
  "key":"SomeStringValue"
  "value":1 //some int value
}`

response:

`{
  "key":"SomeStringValue"
  "value":1 //some int value
}`

DELETE: deletes record
response 204 status code


## Dog Routes
`/dog/populate/` populates the database with dogs. Takes POST

response 201 status code

`/dog/list/` returns list of dogs. Takes GET

response:
`[
  {
    "uuid":"SomeUUID"
    "dog_image":"somedogimage.url"
  }
]`

`/dog/show/<uuid>/` downloads a zip file containing the original dogs image and the dogs image flipped. Takes GET

response 200 status code, response with content_type application/force-download

`/dog/show/` downloads a zip file containing a random dogs image and the random dogs image flipped. Takes GET

response 200 status code, response with content_type application/force-download

`/dog/delete/<uuid>/` deletes the record. Takes DELETE

response 204 status code
