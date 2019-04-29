import math
import operator
import random

from . import views
from .models import *


def getinfo(text, someth, *args):
    print('------------')
    print(text + ':')
    if someth:
        print(someth)
    if len(args) > 0:
        print(len(args))

        for i in args:
            print('||||', i)
    print('------------')


def start_test(request, userid, testid):

    request.session['current_lvl'] = 1
    request.session['wrong_count'] = 0
    request.session['correct_count'] = 0
    request.session['test_id'] = 0
    request.session['QUESTIONS_ID'] = []
    request.session['MY_LAST_TEST_ID'] = 0
    request.session['MT_ID'] = 0
    request.session['current_question_id'] = 0

    global test_id
    test_id = testid

    # getinfo('User', User.objects.get(id=userid))


    MY_LAST_TEST_ID = MyTest.objects.all().filter(test_id=testid, user_id=userid).order_by('-date')
    if MY_LAST_TEST_ID:
        MY_LAST_TEST_ID = MY_LAST_TEST_ID.first().id
    else:
        MY_LAST_TEST_ID = 0
    request.session['MY_LAST_TEST_ID'] = MY_LAST_TEST_ID
    global MT
    MT = MyTest(test_id=testid, user_id=userid)
    MT.save()
    request.session['MT_ID'] = MT.id

    # getinfo('My new test', MT.id)

    get_questions_in_lvl(request)


def get_questions_in_lvl(request):
    current_lvl = request.session['current_lvl']
    getinfo('In get_questions_in_lvl, LVL is', current_lvl)

    if current_lvl > 5:
        return views.end_test(request)

    MY_LAST_TEST_ID = request.session['MY_LAST_TEST_ID']
    if MY_LAST_TEST_ID > 0:
        allQRs = QuestionResult.objects.all().filter(mytest_id=MY_LAST_TEST_ID, question__lvl=current_lvl)
    else:
        allQRs = []
    getinfo('Get allQRs', None, *allQRs)

    wrong_answered_questions = list()

    for qr in allQRs:
        if (qr.selected_answer.id != qr.question.correct_answer.id):
            wrong_answered_questions.append(qr.question)

    getinfo('Wrong', False, *wrong_answered_questions)
    MT = MyTest.objects.get(id=request.session['MT_ID'])
    getinfo('MT', MT)
    questions_in_lvl = Question.objects.all().filter(lvl=current_lvl,
                                                     test_id=MT.test.id)
    getinfo('Questions_in_lvl', None, *questions_in_lvl)
    question_num_in_lvl = questions_in_lvl.count()
    # getinfo('Question_num_in_lvl', question_num_in_lvl)
    all_count = math.ceil(question_num_in_lvl / 3)
    getinfo('All_count', all_count)
    wrong_answered_questions = wrong_answered_questions[:math.ceil(all_count * 2 / 3)]
    # getinfo('Wrong_answered_questions', *wrong_answered_questions)
    request.session['wrong_count'] = math.ceil(all_count / 3)
    getinfo('Wrong_count', request.session['wrong_count'])

    rest_questions_in_lvl = list()

    for question in questions_in_lvl:
        if question not in wrong_answered_questions:
            rest_questions_in_lvl.append(question)

    getinfo('Rest_questions_in_lvl', None, *rest_questions_in_lvl)

    asked_question_result__list = list()
    not_asked_questions_list = list()

    for i in rest_questions_in_lvl:
        j = QuestionResult.objects.all().filter(question_id=i.id)
        if len(j) != 0:
            asked_question_result__list.append(j.order_by('-mytest__date').first())
        else:
            not_asked_questions_list.append(i)

    getinfo('Not_asked_questions_list ', None, *not_asked_questions_list)

    asked_question_result__list.sort(key=operator.attrgetter('mytest.date'))

    asked_question_result__list.reverse()

    asked_question_list = list()
    for i in asked_question_result__list:
        asked_question_list.append(i.question)

    getinfo('Asked_question_list', None, *asked_question_list)
    random.shuffle(not_asked_questions_list)
    all_rest_questions_list = list()
    for i in not_asked_questions_list:
        all_rest_questions_list.append(i)

    for i in asked_question_list:
        all_rest_questions_list.append(i)

    getinfo('All_rest_questions_list', None, *all_rest_questions_list)
    all_rest_questions_list = all_rest_questions_list[: all_count - len(wrong_answered_questions)]
    all_rest_questions_list_id = []
    QUESTIONS = wrong_answered_questions + all_rest_questions_list
    QUESTIONS_ID = []
    for i in QUESTIONS:
        QUESTIONS_ID.append(i.id)
    if len(QUESTIONS_ID) == 0:
        getinfo('QUESTIONS', 'Is EMPTY')
        request.session['current_lvl'] += 1
        getinfo('Current lvl now is', request.session['current_lvl'])
        get_questions_in_lvl(request)
        return

    else:
        request.session['QUESTIONS_ID'] = QUESTIONS_ID
        getinfo('QUESTIONS_ID now is', request.session['QUESTIONS_ID'])
        return

def make(request, selected_answer_id):
    print('Зашел в make')

    # print('quest:', question)
    correct_count = request.session['correct_count']
    wrong_count = request.session['wrong_count']
    MT_ID = request.session['MT_ID']
    question = Question.objects.get(id=request.session['current_question_id'])
    # selected_answer2 = Answer.objects.filter(question_id=question.id)
    # print('Достал selected_answer2 :', selected_answer2)
    # getinfo('Selected_answer_id', selected_answer_id)
    selected_answer = Answer.objects.all().get(id=selected_answer_id)
    # getinfo('Make question', question)

    qr = QuestionResult(question_id=question.id, mytest_id=MT_ID, selected_answer_id=selected_answer_id)
    getinfo('New QR', qr)

    qr.save()
    question.all_answers_num += 1

    if selected_answer.id == question.correct_answer.id:
        getinfo('Answer is', 'Correct')
        question.correct_answers_num += 1
        question.save()
        change_lvl_of_questions(question)
        if (len(request.session['QUESTIONS_ID']) == 0):
            request.session['current_lvl'] += 1
            getinfo('Current lvl now is', request.session['current_lvl'])
            get_questions_in_lvl(request)
    else:
        question.save()
        change_lvl_of_questions(question)
        getinfo('Answer is', 'Wrong')
        request.session['wrong_count'] -= 1
        getinfo('wrong_count', request.session['wrong_count'])
        if (request.session['wrong_count'] == 0):
            request.session['current_lvl'] -= 1
            getinfo('Current lvl now is', request.session['current_lvl'])
            return views.end_test(request)

    return False

def change_lvl_of_questions(question):
    getinfo('In change_lvl_of_questions', False)

    all = question.all_answers_num
    correct = question.correct_answers_num
    num = correct / all
    if num < 0.2:
        question.lvl = 5
    elif num < 0.4:
        question.lvl = 4
    elif num < 0.6:
        question.lvl = 3
    elif num < 0.8:
        question.lvl = 2
    else:
        question.lvl = 1
    question.save()
