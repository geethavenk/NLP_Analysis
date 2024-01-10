from selenium import webdriver
from bs4 import BeautifulSoup as bs


class AmazonScrapper:
    """
    A class for scraping reviews from Amazon India.

    Parameters:
        search_term (str): The search term used on Amazon
        sleep_time (float): Time delay between HTTP requests to avoid being blocked (default is 2 seconds)
    """


    def __init__(self, search_term, sleep_time=2):
        """
        Initialize the AmazonScrapper object.
        Parameters:
            search_term (str): The search term used on Amazon
            sleep_time (float): Time delay between HTTP requests to avoid being blocked (default is 2 seconds)
        """
        self.base_url = "https://www.amazon.in/s?k="
        self.sleep_time = sleep_time
        self.search_term = search_term
        self.browser = webdriver.Chrome()

    #Get http request wrapper using chromedriver
    def get_amazon_search_results(self):
        """
        Get HTTP request wrapper using chromedriver.
        Returns:
            str: The HTML content of the Amazon search results page.

        """
        try:
            url = self.base_url+self.search_term
            self.browser.get(url)
            page_html = self.browser.page_source

            if "api-services-support@amazon.com" in page_html:
                raise Exception("CAPTCHA is not bypassed")
            return page_html

        except Exception as e:
            raise Exception(f"get_amazon_search_results-Error: {str(e)}")

    # Extract ASIN numbers from the search result page
    def get_asin(self):
        """
        Extract ASIN numbers from the search result page
        Returns:
            list: A list of ASIN numbers

        """
        asin_list = []
        try:
            response = self.get_amazon_search_results()
            soup = bs(response, 'html.parser')
            for item in soup.findAll("div", {'data-component-type': 's-search-result'}):
                asin_list.append(item['data-asin'])
            return asin_list

        except Exception as e:
            raise Exception(f"get_asin-Error: {str(e)}")

    # Get review page for the asin
    def get_asin_reviewlink(self, asin):
        """

        Parameters:
            asin (str): The ASIN number for which review link to be extracted

        Returns:
            str: a URL that contains the reviews

        """
        url = "https://www.amazon.in/dp/" + asin
        try:
            self.browser.get(url)
            asin_html = self.browser.page_source

            if "api-services-support@amazon.com" not in asin_html:
                soup = bs(asin_html, 'html.parser')
                for a in soup.find_all("a", {'data-hook': "see-all-reviews-link-foot"}):
                    return a['href']
        except Exception as e:
            raise Exception(f"get_asin_reviewlink: error - {str(e)}")

    # Extract reviews
    def get_reviews(self, review_link, page_nr):
        """
        Extract reviews for the given link and page number
        Parameters:
            review_link (str): A URL which contains the reviews
            page_nr (int): page number

        Returns:
            list: A list of reviews in the given URL and page number

        """
        reviews_list = []

        url = "https://www.amazon.in" + review_link + '&pageNumber=' + str(page_nr)
        # print(url)
        try:
            self.browser.get(url)
            page = self.browser.page_source
            if "api-services-support@amazon.com" not in page:
                soup = bs(page, 'html.parser')
                reviews = soup.find_all('div', {'data-hook': 'review'})
                for item in reviews:

                    try:
                        review_title = item.find('a', {'data-hook': 'review-title'}).text.split("\n")[1]
                    except:
                        review_title = 'no title'

                    try:
                        ratings = float(
                            item.find('i', {'data-hook': 'review-star-rating'}).text.replace(' out of 5 stars', ''))
                    except:
                        ratings = 'no ratings'

                    try:
                        review_body = item.find('span', {'data-hook': 'review-body'}).text.strip()
                    except:
                        review_body = 'no review'

                    try:
                        ele1 = item.find('i', {'class': 'a-icon a-icon-text-separator'}).next_sibling
                        ele2 = item.find('i', {'class': 'a-icon a-icon-text-separator'}).previous_sibling
                        if "Size: " in ele1:
                            size = ele1.replace("Size: ", "")
                        elif "Size: " in ele2:
                            size = ele2.replace("Size: ", "")
                    except:
                        size = 'no size'

                    review = {'review_title': review_title,
                              'ratings': ratings,
                              'review_comment': review_body,
                              'size': size,
                              'asin': review_link.split("/")[3]}

                    reviews_list.append(review)
                return reviews_list

        except Exception as e:
            raise Exception(f"get_reviews: Error- {str(e)}")

    # Get next page status
    def get_np_status(self, review_link, page_nr):
        """
        Get next page status i.e., if next page of review exists or not
        Parameters:
            review_link (str): A URL which contains the reviews
            page_nr (int): page number

        Returns:
            bool: True or False. Returns False if next page does not exist, True if next page exists.

        """
        url = "https://www.amazon.in" + review_link + '&pageNumber=' + str(page_nr)

        try:
            self.browser.get(url)
            page = self.browser.page_source

            if "api-services-support@amazon.com" not in page:
                soup = bs(page, 'html.parser')
                if not soup.find('ul', {'class': 'a-pagination'}):
                    return False
                elif soup.find('li', {'class': 'a-disabled a-last'}):
                    return False
                else:
                    return True

        except Exception as e:
            raise Exception(f"get_np_status: Error - {str(e)}")
