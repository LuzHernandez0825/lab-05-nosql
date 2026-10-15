#!/usr/bin/env python3
"""This script connects to MongoDB Atlas and prints the bookstore report."""

import os
import logging
from pymongo import MongoClient

#configures logging to report system statuses and errors
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

#reads the Atlas variables from your terminal environment (do not hardcode)
MONGODB_ATLAS_URL = os.environ.get("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.environ.get("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.environ.get("MONGODB_ATLAS_PWD")


def main():
    """Main function that connects to the database and prints the report."""
    
    #checks if variables are missing and log an error if they are
    if not all([MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD]):
        logging.error("Missing required environment variables. Please check your Atlas shell settings.")
        return

    #builds the connection string using the environment variables
    connection_uri = f"mongodb+srv://{MONGODB_ATLAS_USER}:{MONGODB_ATLAS_PWD}@{MONGODB_ATLAS_URL}"

    #opens the connection to MongoDB Atlas
    logging.info("Connecting to MongoDB Atlas...")
    client = MongoClient(connection_uri)
    
    try:
        #selects the database and the collections
        db = client["bookstore"]
        authors_col = db["authors"]
        books_col = db["books"]
        
        #logs the connections success status
        logging.info("Connection successful! Generating bookstore report...\n")
        
        #defines the list of target author IDs (including our new step 7 author)
        target_authors = ["author_002", "author_003", "author_004"]
        
        #counts how many target authors are actually in the database and print it
        author_count = authors_col.count_documents({"_id": {"$in": target_authors}})
        
        #print is used for the report layout itself
        print(f"Authors: {author_count}\n")
        
         #loops through each author ID to find their name and matching books
        for author_id in target_authors:
            #finds the author's document in the files
            author = authors_col.find_one({"_id": author_id})
            
            if author:
                #prints the author's name
                print(author["name"])
                
                #finds all books that list this author's ID inside their author_ids array
                linked_books = books_col.find({"author_ids": author_id})
                
                #prints each book title and year indented under the author name
                for book in linked_books:
                    print(f"  {book['title']} ({book['published_year']})")
                
                #add a blank space between authors for cleaner formatting
                print()
                
    except Exception as e:
        #logs the error if something breaks during the database lookups
        logging.error(f"An error occurred during database operations: {e}")
        
    finally:
        #closes the connection safely for the person
        client.close()
        logging.info("MongoDB connection closed safely.")


if __name__ == "__main__":
    main()
