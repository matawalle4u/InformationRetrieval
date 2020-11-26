# from __future__ import division
# import math
# import nltk

# """
# This uses the traditional retrieval
# Algorithm that uses number of co-occurance
# of Key terms of the user query to retrieve
# Relevant Documents


# """

# def proc_query(sentence):

#     sentence = rem_stp_words(sentence)
#     collections = {
#         'doc1':{
#             'id':'1',
#             'content':'Nigerian Petroleum Nigerian'
#         },
#         'doc2':{
#             'id':'2',
#             'content':'Nigerian and their gas economy in Nigerian'
#         },
#         'doc3':{
#             'id':'3',
#             'content':'Nigerian Petroleum industry'
#         },
#         'doc4':{
#             'id':'4',
#             'content':'Ghanian oil politics in real politics'
#         },
#         'doc5':{
#             'id':'5',
#             'content':'Petroleum Petroleum crisis industry crisis'
#         },
#         'doc6':{
#             'id':'6',
#             'content':'Niger delta oil region'
#         }
#     }
    
#     #tokenize the sentence and iterate
    
#     print("\n This is the tokenized USER QUERY ", sentence, "\n")

#     w_weight=0
#     for w1 in sentence:

#         other_words = [word for word in sentence if word !=w1]
#         print(w1,"Other words --> ", other_words)
#         no_of_docs=0
#         word_appearance=0
#         other_word_appearance=0
#         #iterate through collections
#         for doc in collections:
#             doc_contents = rem_stp_words(collections[doc]['content'])
#             if w1 in doc_contents:
#                 no_of_docs+=1
#                 #iterate through docs and find Ntimes the word appeared
#                 for ka in doc_contents:
#                     if w1==ka:
#                         word_appearance+=1
#                     else:
#                         pass
#                 #iterate each of the other words to find their appearances
#                 for w in other_words:
#                     if w in doc_contents:
#                         other_word_appearance+=find_occ(w, doc_contents)
#                     else:
#                         pass
#                 print(doc_contents)
#             else:
#                 pass
#         if word_appearance==0:
#             cal = (no_of_docs/1)*(other_word_appearance)
#             #cal = math.log(cal)
#         else:
#             cal =(no_of_docs/word_appearance)*(other_word_appearance)
#             #cal = math.log(cal)

#         w_weight+=cal
#         print('Documents: {}, Total Appearance :{}, Other words:{}'.format(no_of_docs, word_appearance, other_word_appearance))
#         print("\n")

#     print(w_weight)

# def rem_stp_words(sentence):
#     sentence = nltk.word_tokenize(sentence)
#     stp_w = nltk.corpus.stopwords.words('english')
#     return [sabo for sabo in sentence if sabo not in stp_w]

# def find_occ(val, collec):
#     oc=0
#     for i in range(0, len(collec)):
#         if val==collec[i]:
#             oc+=1
#         else:
#             oc+=0
#     return oc

# def get_doc_qty(word, colle):
#     doc_counter=0
#     for col in colle:
#         coll_sent = rem_stp_words(colle[col]['content'])
#         if word in coll_sent:
#             doc_counter+=1
#         else:
#             doc_counter+=0
#     return doc_counter

# def get_relev_doc(word, coll):
#     rel_docs =[]
#     for col in coll:
#         coll_sent = rem_stp_words(coll[col]['content'])
#         if word in coll_sent:
#             rel_docs.append(coll[col]['id'])
#         else:
#             pass
#     return rel_docs

# proc_query("Petroleum is the fuel for Nigerian Political crisis ")

"""
Traditional retrieval 
Algorithm using co_occurance
Author Adam Mustapha
"""

import json

class Co_occurance:

    def __init__(self, file, jum, interval):

        self.jump = jum
        self.raw_query = input('Query: ')
        self.occurance = []
        self.interval = interval
        self.collection = json.load(open(file, 'r'))
        self.doc_ids = []
        self.user_query = self.token_nize(self.raw_query)
        self.relevant_colls ={}
        
        
    
    def token_nize(self, sentence):
        stp_w = json.load(open("stp_words.json", 'r'))
        sentence = sentence.lower().split(" ")
        return [sabo for sabo in sentence if sabo not in stp_w]
        
    def slice_sen(self, sentence, st, end):
        return sentence[st:end]

    def get_relevant_docs(self):

        for col in self.collection:
            sentence = self.token_nize(self.collection[col]['content'])
            start = 0
            end = self.jump
            sliced = self.slice_sen(sentence, start, end)
            while len(sliced)==self.jump:
                sliced = self.slice_sen(sentence, start, end)
                start +=1
                end +=1
                st2 =0
                end2=self.jump
                query = self.slice_sen(self.user_query, st2, end2)
                while len(query)==self.jump:
                    query = self.slice_sen(self.user_query, st2, end2)
                    if query==sliced:
                        new_col ={
                            col:{
                                "id":self.collection[col]['id'],
                                "content":self.collection[col]['content'],
                            },
                        }
                        self.relevant_colls.update(new_col)
                    st2 +=1
                    end2 +=1
        
        for col in self.relevant_colls:
            sentence = self.token_nize(self.relevant_colls[col]['content'])
            st = 0
            end = self.jump
            sliced = self.slice_sen(sentence, st, end)
            occurance =0
            while len(sliced)==self.jump:
                sliced = self.slice_sen(sentence, st, end)
                st +=1
                end +=1
                st2 =0
                end2=self.jump
                query = self.slice_sen(self.user_query, st2, end2)
                while len(query)==self.jump:
                    query = self.slice_sen(self.user_query, st2, end2)
                    if query==sliced:
                        occurance+=1   
                    st2+=1
                    end2+=1
            self.occurance.append(occurance)
            self.doc_ids.append(self.relevant_colls[col]['id'])
        return self.relevant_colls



    def get_position(self, scores):
        no_of_rel_doc = range(1, self.interval+1)
        filtered_doc = []
        for value in scores:
            ind = scores.index(value)
            position =1
            for score in scores:
                if value>=score:
                    pass
                else:
                    position+=1
            if position in no_of_rel_doc:
                filtered_doc.append(ind)
        return filtered_doc


    def get_documents(self):
        final_ids =[]
        for do in self.get_position(self.occurance):
            final_ids.append(self.doc_ids[do])
        if len(self.get_position(self.occurance))>0:
            for col in self.relevant_colls:
                if self.relevant_colls[col]['id'] in final_ids:
                    print('Document{}: {}'.format(self.relevant_colls[col]['id'], self.relevant_colls[col]['content']))
        else:
            print('No relevant document found')
            
while True:
    try:
     c_occ= Co_occurance("out.json", 3, 3)
     docs = c_occ.get_relevant_docs()
     c_occ.get_documents()
    
    except(KeyboardInterrupt, EOFError, SystemExit):
        break