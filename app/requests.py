import urllib.request, json
from .models import Quote
from datetime import datetime

#get base url
base_url = None


def configure_request(app):
  
    base_url = app.config['API_BASE_URL']
    
def get_quotes():
    
    '''
    Function that gets the json response to our url request
    '''
    get_quotes_url = base_url

    with urllib.request.urlopen('http://quotes.stormconsultancy.co.uk/random.json') as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)

        quote_results = None

        quote_list = get_quotes_response
        id = quote_list['id']
        author = quote_list["author"]
        quote = quote_list["quote"]
        quote_object= Quote(id,author,quote)
        
    return quote_object