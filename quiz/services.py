from .dto import ChoiceDTO, QuestionDTO, QuizDTO, AnswerDTO, AnswersDTO
from typing import List


class QuizResultService():
    def __init__(self, quiz_dto: QuizDTO, answers_dto: AnswersDTO):
        self.quiz_dto = quiz_dto
        self.answers_dto = answers_dto

    def get_result(self) -> float:
        list_answers = []
        dto_questions = self.quiz_dto.questions
        answers = {
            item.question_uuid: item.choices
            for item in self.answers_dto.answers
        }
        questions = {
            item.uuid: item.choices
            for item in dto_questions
        }

        for question_uuid, answer_coices in answers.items():
            choices = questions[question_uuid]
            choices_correct = correct_choices(choices)

            if answer_coices == choices_correct:
                list_answers.append(1)
        res = list_answers.count(1) / len(dto_questions)
        return res

def correct_choices(choices):
    choice_correct = []
    for item in choices:
        if item.is_correct:
            choice_correct.append(item.uuid)
    return choice_correct
