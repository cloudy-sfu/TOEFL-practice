import django
import json
import os
import random
import re
import string
import time
from bs4 import BeautifulSoup
from requests import Session
from tqdm import tqdm

with open("reading/weixue100/reading_articles.txt") as f:
    articles = f.readlines()
with open("reading/weixue100/_https_header.json") as f:
    chrome120 = json.load(f)

session = Session()
session.trust_env = False
remove_tag = re.compile(r'<[^>]+>')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toefl_practice.settings')
django.setup()
k = len('■')
m = len('<br>')
from reading.models import Passage, ReadingQuestion

for article_ in tqdm(articles):
    if Passage.objects.filter(source=article_).exists():
        continue
    response = session.get(article_, headers=chrome120)
    time.sleep(round(random.uniform(0.5, 1.5), 1))
    if response.ok:
        text = BeautifulSoup(response.text, features='html.parser')
        for x in text.find_all('script'):
            if x.text.startswith("_data"):
                data = x.text
                data = data.removesuffix(";\n_currentQid = 0;").removeprefix("_data = ")
                data = json.loads(data)
                data = data.get('contents', [{}])[0]

                title = data.get('title', '')
                article = data.get('originalText', '')
                if Passage.objects.filter(title=title).exists():
                    print(f"Title \"{title}\" is not unique.")
                    break
                new_passage = Passage(title=title, article=article, source=article_)
                new_passage.save()

                questions = data.get('exercises', [])
                n_questions = len(questions)
                for q_id, question_dict in enumerate(questions):
                    question_type = question_dict.get('type', 1)
                    if question_type == 3:  # choose 3 from 6 question
                        question_text = question_dict.get('text', '').removesuffix('\n')
                        question_citation = question_text.rsplit('<br>', 1)
                        if len(question_citation) == 1:
                            question_citation = question_text.rsplit('\n', 1)
                        if len(question_citation) > 1:
                            question, citation = question_citation
                            question = remove_tag.sub('', question)
                            citation = remove_tag.sub('', citation)
                        else:
                            question = remove_tag.sub('', question_citation[0])
                            citation = ''
                        question = question.removesuffix('\n')
                    elif question_type == 11:  # ranking question
                        question = remove_tag.sub('', question_dict.get('text', ''))
                        citation = question_dict.get('item', [{}])[0].get('insertText', '')
                    else:
                        question = remove_tag.sub('', question_dict.get('text', ''))
                        citation = ''
                    options = question_dict.get('item', [{}])[0].get('question', {}).get(
                        'options', [])
                    options_6 = []
                    answer = ''
                    if question_type == 11:
                        positions = []
                        for i, option in enumerate(options):
                            if option.get('position'):
                                positions.append(option.get('position'))
                            if option.get('isRight', 0) == 1:
                                answer += string.ascii_uppercase[i]
                        paragraph_start = article.rfind('<br>', 0, min(positions))
                        if paragraph_start == -1:
                            paragraph_start = 0
                        else:
                            paragraph_start += m
                        paragraph_end = article.find('<br>', max(positions))
                        if paragraph_end == -1:
                            paragraph_end = len(article)
                        citation = article[paragraph_start:paragraph_end]
                        i = 0
                        for i, position in enumerate(positions):
                            rp = position - paragraph_start  # relative position
                            citation = citation[:rp+i] + '■' + citation[rp+i:]
                            end_of_sentence = citation.find('.', rp+i)
                            if end_of_sentence == -1:
                                options_6.append('[End of the paragraph]')
                            else:
                                options_6.append(citation[rp+i+k:end_of_sentence+k])
                        for j in range(i+1, 6):
                            options_6.append('')
                    else:
                        for i in range(6):
                            if i < len(options):
                                options_6.append(options[i].get('text', ''))
                                if options[i].get('isRight', 0) == 1:
                                    answer += string.ascii_uppercase[i]
                            else:
                                options_6.append('')
                    choice_a, choice_b, choice_c, choice_d, choice_e, choice_f = options_6
                    idx = q_id + 1
                    new_question = ReadingQuestion(
                        passage=new_passage,
                        idx=idx,
                        citation=citation,
                        question=question,
                        choice_a=choice_a,
                        choice_b=choice_b,
                        choice_c=choice_c,
                        choice_d=choice_d,
                        choice_e=choice_e,
                        choice_f=choice_f,
                        answer=answer
                    )
                    new_question.save()
                break
