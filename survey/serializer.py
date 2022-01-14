from .models import *
from .queries import save_answer
USER_CHOICE = 'user_choice'



def serializer(form: list, choice: dict, session_key: str, question: Question, last_index: bool, check_box_lable: bool, second_answer=None):
    clear_data = {}
    if last_index:
        clear_question = Question.objects.get(pk=question.pk)
    else:
        clear_question = Question.objects.get(pk=question.pk-1)

    clear_choice = Choice.objects.get(pk=form)
    clear_data = {'uuid': session_key, 'choice': clear_choice, 'question': clear_question}
    save_answer(clear_data, second_answer)

