from .models import *
from quiz.dto import *


def all_question_list() -> list:
    all_question = Question.objects.values_list('pk', flat=True)
    return all_question


def all_questions():
    questions = Question.objects.all()
    return questions

def get_session(request):
    if not request.session.session_key:
        request.session.save()


def get_choice(question: Question):
    choice = Choice.objects.filter(question=question.pk)
    return choice


def get_question(pk: int) -> Question:
    question = Question.objects.get(pk=pk)
    return question


def save_answer(answer: dict, second_answer=None):
    if not second_answer:
        if answer_exists(answer):
            delete_answer_in_db(answer)

    answer, create = Answer.objects.update_or_create(uuid=answer['uuid'], choice=answer['choice'],
                                                     question=answer['question'])
    answer.save()
    return answer.question


def answer_exists(answer: dict):
    answer_exist = Answer.objects.filter(uuid=answer['uuid'], question=answer['question']).exists()
    return answer_exist


def delete_answer_in_db(answer: dict):
    exist_answer = Answer.objects.filter(uuid=answer['uuid'], question=answer['question'])
    for item in exist_answer:
        item.delete()


def min_question() -> Question:
    all_question_list = Question.objects.values_list('id', flat=True)
    return Question.objects.get(pk=min(all_question_list))


def choces_dto(question):
    dto_choices = [
        ChoiceDTO(item.pk, item.text, item.is_correct)
        for item in question.choice_set.all()
    ]
    return dto_choices


def dto_questions(questions):
    dto_question = [
        QuestionDTO(item.pk, item.text, choces_dto(item))
        for item in questions
    ]
    return dto_question

def dto_quiz(question_dto):
    quiz_dto = QuizDTO('1','quiz', question_dto)
    return quiz_dto

def choices_from_answer(answer):
    choices = answer.choice.pk
    return [choices]

def answer_dto(choices, question_pk):
    dto_answer = AnswerDTO(question_pk, choices)
    return dto_answer


def answer_list_dto(questions, session_key):
    list_answer_dto = []
    for item in questions:
        choices = []
        answers = item.answer_set.all().filter(uuid=session_key)

        for answer in answers:
            choices += choices_from_answer(answer)
        list_answer_dto.append(answer_dto(choices,item.pk))

    return list_answer_dto

def dto_answers(list_answer_dto, quiz_dto_uuid):
    answers_dto = AnswersDTO(quiz_dto_uuid, list_answer_dto)
    return answers_dto
