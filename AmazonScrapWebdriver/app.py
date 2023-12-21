from AmazonReviewScrap import AmazonScrapper
import csv
import pandas as pd
from MongoDBOperations import MongoDBOps

search_term = input("Enter keywords separated with +: ")
ob = AmazonScrapper(search_term)
asins = ob.get_asin()


# For each ASIN extract reviews

output_review = open("Reviews.csv", 'a', encoding="utf-8", newline="")
writer = csv.DictWriter(output_review, fieldnames=['review_title', 'ratings', 'review_comment', 'size', 'asin'])
writer.writeheader()

for i in range(len(asins)):
    link = ob.get_asin_reviewlink(asin=asins[i])
    if link is not None:
        #print(link)
        page_nr = 1
        while page_nr > 0:
            reviews = ob.get_reviews(review_link=link, page_nr=page_nr)
            np_status = ob.get_np_status(review_link=link, page_nr=page_nr)
            if reviews:
                writer.writerows(reviews)
                #print(reviews)

            if np_status:
                page_nr += 1
            else:
                break

## Transfer data from csv to mongoDB database
df_rev = pd.read_csv('Reviews.csv', sep=",")
df_rev.drop_duplicates(inplace=True)
mongo_client = MongoDBOps(username="geetharv", pwd='mongo123')
db_name = 'Neemai'
collection_name = 'maternity_wear'
mongo_client.df_to_collection(db_name=db_name, collection_name=collection_name, df=df_rev)




