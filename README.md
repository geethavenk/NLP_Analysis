# NLP Analysis

This project, undertaken for Neemai, a clothing brand in India, aims to identify the sentiments surrounding maternity wear in the country. To achieve this, customer review data for maternity wear dresses was scraped from Amazon India. Sentiment analysis was performed on this data, and specifically, bi-grams and tri-grams were identified. The word clouds generated from the review data provided valuable insights into customer opinions.

### Dataset

Review data was scraped from Amazon India and the data was stored in MongoDB database.

### Analysis

- Extract data from MongoDB database.
- Perform exploratory analysis to remove duplicates if they exist, check data distribution with respect to customer ratings and dress sizes.
- Perform Sentiment analysis using Roberta Pretrained Model.
- Generated word clouds.

### Technologies used

- Python
- BeautifulSoup for web scraping
- pymongo to save the data in a MongoDB database and to access the data from the database
- seaborn and matplotlib for data visualization
- NLTK and transformers for NLP analysis
  
