# from django_cloud_tasks.decorators import task
# from .helpers import *
# from .keypoints import *



# @task(queue='tasks-queue')
# def get_document(query,email,temperature):
#     contents=get_contents(query)
#     print(len(contents))
#     contents.sort(key=paragraphs_count)
#     try:
#         main_article=get_main_article(contents)
#         print('main article: '+main_article)
#         paragraphs=get_main_paragraphs(main_article)
#         list_para= parse_final_document(paragraphs,contents,temperature)
#         print('list para '+str(len(list_para)))
#         article='\n\n'.join(list_para)
#         # article_paraphrased=paraphrase(article)
#         user=User.objects.filter(email=email)
#         article=Article(user=user,title=query,content=article)
#         article.save()
#         user.update(credits_used=F('credits_used') + 1)
#         send_email('Temperature: '+str(temperature)+' - '+query,str(contents),email)
#     except:
#         send_email('An error occured while generating '+query,'Please try again or contact support when you need it',email)
#     return 'done'

# # @task(queue='tasks-queue')
# # def summarize(query,email):
# #     contents=get_contents(query)
# #     no_of_lines=30
# #     clean_sentences,sentences=clean_all_sentences(contents)
# #     word_embeddings=extract_word_vectors()
# #     sentence_vectors = []
# #     for i in clean_sentences:
# #         if len(i) != 0:
# #             v = sum([word_embeddings.get(w, np.zeros((50,))) for w in i.split()])/(len(i.split())+0.001)
# #         else:
# #             v = np.zeros((50,))
# #         sentence_vectors.append(v)
# #     # similarity matrix
# #     sim_mat = np.zeros([len(sentences), len(sentences)])
# #     for i in range(len(sentences)):
# #         for j in range(len(sentences)):
# #             if i != j:
# #                 sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,50), sentence_vectors[j].reshape(1,50))[0,0]
# #        #textrank 
# #     nx_graph = nx.from_numpy_array(sim_mat)
# #     scores = nx.pagerank(nx_graph)
# #     ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
# #     # Extract top n sentences as the summary
# #     if len(ranked_sentences)<30:
# #         no_of_lines=len(ranked_sentences)
# #     summary=''
# #     for i in range(no_of_lines):
# #       summary+=ranked_sentences[i][1]+' %0A '
# #     user=User.objects.filter(email=email)
# #     article=Article(user=user,title='KeyPoints: %0A'+query,content=summary)
# #     article.save()
# #     user.update(credits_used=F('credits_used') + 1)  
# #     send_email('This is a summary', summary, email)    
# #     return 'done'  