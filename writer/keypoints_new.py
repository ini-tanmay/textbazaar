# # from googlesearch import search
# # from .text_rewrite import *
# from newspaper import Article, Config
# # from .summarize_nltk import summarize_para
# # from .email import send_email
# # from django.db.models import F
# # from background_task import background
# # from .proxies import *
# import concurrent.futures
# import json
# import re
# # import spacy
# # import en_core_web_md
# # from .models import User, Article
# from duckpy import Client

# client = Client()


# user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
# config = Config()
# config.browser_user_agent = user_agent
# config.request_timeout = 15

# proxyDict={
# "http":"http://191.96.42.80:8080",
# "http":"http://198.199.86.11:3128",
# "http":"http://161.35.4.201:80",
# "http":"http://138.68.60.8:8080",
# "http":"http://209.97.150.167:8080",
# }

# def get_article_nlp(url):
#     data={}
#     config.proxies = proxyDict

#     try:
#         article = Article(url,config=config,memoize_articles=False)
#         article.download()
#         article.parse()
#         data['title']=article.title
#         data['content']=article.text
#         data['videoURLs']=article.movies
#         data['authors']=article.authors
#         data['imageURL']=article.top_image
#         data['imageURLs']=list(article.images)
#         # article.nlp()
#         # data['summary']=article.summary
#         # data['keywords']=article.keywords
#         return data
#     except Exception as e:
#         return {}
#         pass


# def search(query):
#     data=[]
#     links = client.search(query)
#     for link in links[:10]:
#         link_href = link.url
#         print(link_href)
#         data.append(link_href)
#     return data    

# def remove_urls(vTEXT):
#     text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%|\-)*\b', '', vTEXT, flags=re.MULTILINE)
#     text = re.sub(r'\[\d+\]', '', text)
#     text = re.sub(r'/[\u006E\u00B0\u00B2\u00B3\u00B9\u02AF\u0670\u0711\u2121\u213B\u2207\u29B5\uFC5B-\uFC5D\uFC63\uFC90\uFCD9\u2070\u2071\u2074-\u208E\u2090-\u209C\u0345\u0656\u17D2\u1D62-\u1D6A\u2A27\u2C7C]+/g', '', text)
#     return text

# def get_contents(request):
#     query=request.args.get('query')
#     links=search(query) 
#     print(len(links))
#     articles=[]
#     # for link in links:
#     #   articles.append(get_article_nlp(link))
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         data=executor.map(get_article_nlp,links)
#         articles=list(data)
#     contents=[]
#     for article in articles:
#         if article.get('content')!=None:
#             contents.append(remove_urls(article['content']))
#     print(len(contents))
#     print(str(contents))
#     return str(contents)
