from .models import *
import operator
from django.shortcuts import render

MY_LAST_TEST = MyTest()
MT = None

def get_questions_in_lvl(current_lvl):
    if (current_lvl == 6):
        pass

    allQRs = QuestionResult.objects.all().filter(mytest_id=MY_LAST_TEST.id, question__lvl=current_lvl)

    wrong_answered_questions = list()

    for qr in allQRs:
        if (qr.selected_answer != qr.question.correct_answer):
            wrong_answered_questions.append(qr.question)

    question_num_in_lvl = Question.objects.all().filter(lvl=current_lvl, test_id=MY_LAST_TEST.test.id).count()
    correct_count = round(question_num_in_lvl / 3)  # 1/3 из всего кол-во вопросов в уровне
    wrong_answered_questions = wrong_answered_questions[:math.ceil(correct_count * 2 / 3)]
    wrong_count = round(correct_count / 3)  # (1/3)/3 из всего кол-во вопросов в уровне

    questions_in_lvl = Question.objects.all().filter(lvl=current_lvl, test_id=MY_LAST_TEST.test.id)

    rest_questions_in_lvl = list()

    for question in questions_in_lvl:
        if question not in wrong_answered_questions:
            rest_questions_in_lvl.append(question)

    asked_question_result__list = list()
    not_asked_questions_list = list()

    for i in rest_questions_in_lvl:
        j = QuestionResult()
        j = QuestionResult.objects.all().filter(question_id=i.id)
        if j != None:
            asked_question_result__list.append(j.order_by('-mytest__date').first())

        else:
            not_asked_questions_list.append(i)

    asked_question_result__list.sort(key=operator.attrgetter('mytest.date'))
    asked_question_result__list.reverse()

    asked_question_list = list()
    for i in asked_question_result__list:
        asked_question_list.append(i.question)

    rest_questions_list = list()
    for i in not_asked_questions_list:
        rest_questions_list.append(i)

    for i in asked_question_list:
        rest_questions_list.append(i)

    rest_questions_list = rest_questions_list[0: correct_count - len(wrong_answered_questions)]

    all_questions_set = set(wrong_answered_questions + rest_questions_list)
    global QUESTIONS
    QUESTIONS = all_questions_set

    new_question = QUESTIONS.pop()
    # return render(request, '.question_page.html', new_question)

    preaperead_questions = {
        'QUESTIONS': QUESTIONS,
        'correct_count': correct_count,
        'wrong_count': wrong_count

    }

    return preaperead_questions


def check_answer(question, useranswer):
    if (question.correct_answer == useranswer):
        return True
    else:
        return False


def main1():
    lvl = 1
    while (True):
        preapered_questions = get_questions_in_lvl(lvl)

        QUESTIONS = preapered_questions['QUESTIONS']
        wrong_count = preapered_questions['wrong_count']
        correct_count = preapered_questions['correct_count']

        for i in QUESTIONS:
            yield i.correct_answer

        while (True):
            question = QUESTIONS.pop()

            user_answer = 'be'  # ответ пользователя из формы берем



            if (check_answer(question, user_answer)):
                correct_count -=1
            else:
                wrong_count -=1

            if (wrong_count == 0):
                lvl -= 1
                break

            if (correct_count == 0):
                lvl += 1
                break

        if lvl == 0:
            print("Ваш уровень 1")
            break
        if lvl == 6:
            print("Ваш уровень 5")
            break

def main():
    for i in range (0, 10):
        yield i
        yield




