from selenium import webdriver
from bs4 import BeautifulSoup as bs


## create browser to request page data
browser = webdriver.Chrome()


class AmazonScrapper:
    base_url = "https://www.amazon.in/s?k="

    def __init__(self, search_term, sleep_time=2):
        self.sleep_time = sleep_time
        self.search_term = search_term

    #Get http request wrapper using chromedriver
    def get_amazon_search_results(self):
        try:
            url = AmazonScrapper.base_url+self.search_term
            browser.get(url)
            page_html = browser.page_source

            if "api-services-support@amazon.com" in page_html:
                raise Exception("CAPTCHA is not bypassed")
            return page_html

        except Exception as e:
            raise Exception(f"get_amazon_search_results-Error: {str(e)}")

    # Exctract ASIN numbers from the search result page
    def get_asin(self):
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
        url = "https://www.amazon.in/dp/" + asin
        try:
            browser.get(url)
            asin_html = browser.page_source

            if "api-services-support@amazon.com" not in asin_html:
                soup = bs(asin_html, 'html.parser')
                for a in soup.find_all("a", {'data-hook': "see-all-reviews-link-foot"}):
                    return a['href']
        except Exception as e:
            raise Exception(f"get_asin_reviewlink: error - {str(e)}")

    # Extract reviews
    def get_reviews(self, review_link, page_nr):
        reviews_list = []

        url = "https://www.amazon.in" + review_link + '&pageNumber=' + str(page_nr)
        # print(url)
        try:
            browser.get(url)
            page = browser.page_source
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
                            #print(size)
                        elif "Size: " in ele2:
                            size = ele2.replace("Size: ", "")
                            #print(size)
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
        url = "https://www.amazon.in" + review_link + '&pageNumber=' + str(page_nr)

        try:
            browser.get(url)
            page = browser.page_source

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












