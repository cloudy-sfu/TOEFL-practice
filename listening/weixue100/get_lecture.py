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
from check_windows_filename import sanitize_filename

with open("listening/weixue100/listening_articles.txt") as f:
    lectures = f.readlines()
with open("reading/weixue100/_https_header.json") as f:
    chrome120 = json.load(f)

session = Session()
session.trust_env = False
remove_tag = re.compile(r'<[^>]+>')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toefl_practice.settings')
django.setup()
from listening.models import Lecture, ListeningQuestion

for lecture in tqdm(lectures):
    lecture = lecture.removesuffix('\n')
    if Lecture.objects.filter(source=lecture).exists():
        continue
    response = session.get(lecture, headers=chrome120)
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
                original_text = data.get('originalText', '')
                recording_url = data.get('mp3Url', {}).get('url')
                recording_response = session.get(recording_url)
                recording_response.raise_for_status()

                if (('conversation' in title.lower()) or ('passage' in title.lower()) \
                        or re.match(r'^L\d+$', title) or
                        re.match(r'^C\d+$', title)) or ('lecture' in title.lower()):
                    title = data.get('name', '') + ' ' + title
                if Lecture.objects.filter(title=title).exists():
                    print(f"Title \"{title}\" is not unique.")
                    break
                new_lecture = Lecture(title=title, source=lecture,
                                      original_text=original_text)
                new_lecture.recording.save(
                    sanitize_filename(title) + '.mp3',
                    django.core.files.base.ContentFile(recording_response.content),
                    save=True
                )

                questions = data.get('exercises', [])
                n_questions = len(questions)
                for q_id, question_dict in enumerate(questions):
                    question_items = question_dict.get('item', [{}])[0]
                    options = question_items.get('question', {}).get('options', [])
                    options_6 = []
                    answer = ''
                    for i in range(6):
                        if i < len(options):
                            options_6.append(options[i].get('text', ''))
                            if options[i].get('isRight', 0) == 1:
                                answer += string.ascii_uppercase[i]
                        else:
                            options_6.append('')
                    choice_a, choice_b, choice_c, choice_d, choice_e, choice_f = options_6
                    idx = q_id + 1
                    question_text = question_dict.get('text', '')
                    new_question = ListeningQuestion(
                        lecture=new_lecture,
                        idx=idx,
                        question=question_text,
                        choice_a=choice_a,
                        choice_b=choice_b,
                        choice_c=choice_c,
                        choice_d=choice_d,
                        choice_e=choice_e,
                        choice_f=choice_f,
                        answer=answer
                    )
                    if 'listeningFrontUrl' in question_items.keys():
                        listen_again_url = (question_items.get('listeningFrontUrl', {})
                                            .get('url'))
                    elif 'listeningBackUrl' in question_items.keys():
                        listen_again_url = (question_items.get('listeningBackUrl', {})
                                            .get('url'))
                    elif ('listen again' in question_text.lower()) or (
                            'professor say this' in question_text.lower()):
                        listen_again_url = (question_items.get('listeningUrl', {})
                                            .get('url'))
                    else:
                        listen_again_url = None

                    if listen_again_url is None:
                        new_question.save()
                    else:
                        listen_again_response = session.get(listen_again_url)
                        listen_again_response.raise_for_status()
                        new_question.listen_again.save(
                            sanitize_filename(title) + '-listen-again.mp3',
                            django.core.files.base.ContentFile(listen_again_response.content),
                            save=True
                        )
                break
