from googlesearch import search
from .text_rewrite import *
from newspaper import Article, Config
from .summarize_nltk import summarize_para
from .email import send_email
from background_task import background
from .proxies import *
import concurrent.futures
import json
import re
import spacy
import en_core_web_md


class Sentence:
    
    def __init__(self, text, similarity):
        self.text=text
        self.similarity=similarity
        pass
    
    def __repr__(self):
        return self.text+' '+str(self.similarity)
 
def sort_by_similarity(element):
    return element.similarity

def paraphrase(input):
    rephrased = TextRewrite(input).work()
    return rephrased

NEWLINES_RE = re.compile(r"\n{2,}")  # two or more "\n" characters

def get_paragraphs(input):
    no_newlines = input.strip("\n")  # remove leading and trailing "\n"
    split_text = NEWLINES_RE.split(no_newlines)  # regex splitting
    paragraphs = [p + "\n" for p in split_text if p.strip()]
    # p + "\n" ensures that all lines in the paragraph end with a newline
    # p.strip() == True if paragraph has other characters than whitespace
    return (paragraphs)

def paragraphs_count(input):
    no_newlines = input.strip("\n")  # remove leading and trailing "\n"
    split_text = NEWLINES_RE.split(no_newlines)  # regex splitting
    paragraphs = [p + "\n" for p in split_text if p.strip()]
    # p + "\n" ensures that all lines in the paragraph end with a newline
    # p.strip() == True if paragraph has other characters than whitespace
    return len(paragraphs)

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 25


def get_article_nlp(url):
    data={}
    config.proxies = proxyDict
    try:
        article = Article(url,config=config,memorize_articles=False)
        article.download()
        article.parse()
        data['title']=article.title
        data['content']=article.text
        data['videoURLs']=article.movies
        data['authors']=article.authors
        data['imageURL']=article.top_image
        data['imageURLs']=list(article.images)
        article.nlp()
        data['summary']=article.summary
        data['keywords']=article.keywords
        return data
    except Exception as e:
        return {}
        pass



def get_main_article(documents):
    temp_article=''
    for content in documents:
        if paragraphs_count(content)>3 and (3800<len(content)<8000):
            temp_article=content
            documents.remove(content)
        if temp_article=='':
            documents.remove(documents[0])
            return documents[0]
        return temp_article
             
        

def get_main_paragraphs(main_article):  
    nlp = en_core_web_md.load()
    paragraphs=[]
    sentence_list=main_article.replace('\n','').split('.')
    for i in range(0,len(sentence_list)):
        if len(sentence_list)>i+1:
            sentence_doc=nlp(sentence_list[i])
            paragraph_doc=nlp(sentence_list[i+1])
            cleaned_doc1 = nlp(' '.join([str(t) for t in sentence_doc if not t.is_stop]))
            cleaned_doc2 = nlp(' '.join([str(t) for t in paragraph_doc if not t.is_stop]))
            similarity=cleaned_doc1.similarity(cleaned_doc2)
            if similarity>0.55:
                if len(paragraphs)==0:
                    paragraphs.append(sentence_list[i])
                else:    
                    paragraphs[-1]+='.'+(sentence_list[i])
            else:
                paragraphs.append(sentence_list[i])

    cleaned_paragraphs=[]

    for paragraph in paragraphs:
        if len(paragraph)>50 and '.' in paragraph:
            cleaned_paragraphs.append(paragraph)

    return cleaned_paragraphs        

def parse_final_document(cleaned_paragraphs,documents,temperature):
    nlp = en_core_web_md.load()
    notes=[]
    for paragraph in cleaned_paragraphs:
        notes.append(summarize_para(paragraph,temperature))
    for content in documents:
        content_lines=content.replace('\n','').split('.')
        for main_line in content_lines:
            if main_line!='':
                points={}
                points[main_line]=Sentence('hey',0)
                for other_line in notes:
                    if other_line!='':
                        doc1=nlp(main_line)
                        doc2=nlp(other_line)
                        cleaned_doc1 = nlp(' '.join([str(t) for t in doc1 if not t.is_stop]))
                        cleaned_doc2 = nlp(' '.join([str(t) for t in doc2 if not t.is_stop]))
                        similarity=cleaned_doc1.similarity(cleaned_doc2)
                        if similarity>points[main_line].similarity and similarity>0.82 and main_line not in other_line:
                            points[main_line]=(Sentence(other_line,similarity))
                try:       
                    index=notes.index(points[main_line].text)
                    notes[index]+='.'+(summarize_para(main_line))
                except:
                    pass
    return notes

def remove_urls (vTEXT):
    text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%|\-)*\b', '', vTEXT, flags=re.MULTILINE)
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'/[\u006E\u00B0\u00B2\u00B3\u00B9\u02AF\u0670\u0711\u2121\u213B\u2207\u29B5\uFC5B-\uFC5D\uFC63\uFC90\uFCD9\u2070\u2071\u2074-\u208E\u2090-\u209C\u0345\u0656\u17D2\u1D62-\u1D6A\u2A27\u2C7C]+/g', '', text)
    return text

@background(schedule=0)
def get_document(query,email,temperature):
    links=search(query,num_results=10) 
    articles=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        data=executor.map(get_article_nlp,links)
        articles=list(data)
    contents=[]
    for article in articles:
        if article.get('content')!=None:
            contents.append(remove_urls(article['content']))
    contents.sort(key=paragraphs_count)
    main_article=get_main_article(contents)
    print(main_article)
    paragraphs=get_main_paragraphs(main_article)
    list_para= parse_final_document(paragraphs,contents,temperature)
    print(list_para)
    article='\n\n'.join(list_para)
    # article_paraphrased=paraphrase(article)
    send_email('Temperature: '+str(temperature)+' - '+query,str(article),email)
    return article
