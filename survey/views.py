from django.shortcuts import render, redirect
from .queries import *
from .forms import HtmlForms
from .serializer import serializer, USER_CHOICE
from quiz.services import *


def home(request):
    all_questions = list(all_question_list())
    first_question = min(all_questions)
    context = {
        'all_question': all_questions,
        'first_question': first_question,
    }
    return render(request, template_name='survey/home.html', context=context)


def index(request, pk=None):
    # request.session.flush()  Стереть session key
    check_box_label = True
    last_index = False
    get_session(request)
    session_key = request.session.session_key
    all_question = all_question_list()

    if pk > max(all_question):
        pk -= 1
        last_index = True

    current_page = pk
    next_page = current_page + 1
    first_question = min_question()
    question = get_question(pk)
    choice = get_choice(question)

    if question.pk == 4 or question.pk == 5:
        check_box_label = False

    if request.method == 'POST':
        form = HtmlForms(request.POST)
        if USER_CHOICE not in form.data.dict():
            return redirect('index', pk - 1)
        else:
            if form.is_valid():
                print(check_box_label)
                if check_box_label:
                    serializer(form.data.getlist(USER_CHOICE)[0], choice.values_list('question'),
                               session_key, question, last_index, check_box_label)
                else:
                    serializer(form.data.getlist(USER_CHOICE)[0], choice.values_list('question'),
                               session_key, question, last_index, check_box_label)

                    if len(form.data.getlist(USER_CHOICE)) > 1:
                        second_answer = True
                        serializer(form.data.getlist(USER_CHOICE)[1], choice.values_list('question'),
                                   session_key, question, last_index, check_box_label, second_answer)

                if last_index:
                    return redirect('result')
                return redirect('index', current_page)
    else:
        form = HtmlForms()

    context = {
        'question_id': pk,
        'all_question': all_question,
        'form': form,
        'question': question,
        'choice': choice,
        'next_page': next_page,
        'first_question': first_question,
        'check_box_label': check_box_label,
    }
    return render(request, template_name='survey/index.html', context=context)


def result(request):
    session_key = request.session.session_key
    questions = all_questions()
    question_dto = dto_questions(questions)
    quiz_dto = dto_quiz(question_dto)
    list_answer_dto = answer_list_dto(questions, session_key)
    answers_dto = dto_answers(list_answer_dto, quiz_dto.uuid)

    quiz_result = QuizResultService(quiz_dto, answers_dto)
    res = quiz_result.get_result()

    first_question = min(list(all_question_list()))

    context = {
        'result': int(res * 100),
        'first_question': first_question
    }

    return render(request, template_name='survey/result.html', context=context)
