// Step 2:
// use bookstore
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json
db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)

// Step 4: load books.json
db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)

//Step 5: list authors and books
db.authors.find()
db.books.find()

// Step 6: insert two new books
db.books.insertMany([
   {
     title: "Emma",
     published_year: 1816,
     author_ids: ["author_001"]
   },
   {
     title: "It",
     published_year: 1986,
     author_ids: ["author_004"]
   }
])

// Step 7: add missing authors
db.authors.insertOne({
   "_id": "author_004",
   "name": "Stephen King",
   "nationality": "American",
   "bio": {
     "short": "An American author of horror and supernatural fiction.",
     "long": "Stephen King is one of the most prolific and celebrated contemporary authors, best known for his terrifying horror novels, suspense thrillers, and massive contributions to pop culture."
   }
 })

// Step 8: filter books by a list of authors
db.books.find({ author_ids: { $in: ["author_001", "author_004"] } })

