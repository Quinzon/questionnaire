import json
import copy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from .models import Form, Application
from .algorithm import create_application, paste_answers, check_answer, find_next_question_path


def form(request, form_name):
    try:
        form = Form.objects.get(name=form_name)
    except Form.DoesNotExist:
        return render(request, 'form/form.html')
    return render(request, 'form/form.html', {'form': form})


@csrf_exempt
@require_http_methods(["POST"])
def questions(request, form_name):
    data = json.loads(request.body)
    form = Form.objects.get(name=form_name)

    print('data', data)

    if not data['path']:
        application = Application(form=form)
        application.answer = create_application(copy.deepcopy(form.struct))

        path = [form.struct.get('questions')[0]['name']]
        application.email = data['answer'][next(iter(data['answer']))]
        for key, item in data['answer'].items():
            if application.answer['questions'][0]['name'] == key:
                application.answer['questions'][0]['answer'] = item

        application.save()
        application_id = application.id

    else:
        application_id = data['application_id']
        application = Application.objects.get(id=application_id)

        path = eval(data['path'])
        application.answer = paste_answers(application.answer, path, data['answer'])

        application.save()

    if data['action'] == 'complete':
        application.status = True
        application.save()
        return render(request, 'form/result.html', {'questions': application.answer['questions']})

    question, path = check_answer(application.answer, path)

    application_complete = True if find_next_question_path(application.answer, path) is None else False

    print('path', path)
    print('question', question)
    print('application.answer', application.answer)
    print()

    return render(request, 'form/question.html', {
                                                  'question': question,
                                                  'path': path,
                                                  'application_id': application_id,
                                                  'application_complete': application_complete})





# answer_dict = {
#   "questions": [
#     {
#       "name": "Ваша почта",
#       "questions": [
#         {
#           "name": "Почта",
#           "answer": "Почта"
#         }
#       ]
#     },
#     {
#       "name": "Тип вашего заведения",
#       "questions": [
#         {
#           "name": "Бар",
#           "answer": "true",
#           "questions": [
#             {
#               "name": "Что ещё есть в вашем баре?",
#               "questions": [
#                 {
#                   "name": "Библиотека",
#                   "answer": "true"
#                 },
#                 {
#                   "name": "Кухня",
#                   "answer": "true",
#                   "questions": [
#                     {
#                       "name": "Какая у вас кухня?",
#                       "questions": [
#                         {
#                           "name": "Православная",
#                           "answer": "true"
#                         },
#                         {
#                           "name": "Сухарики сами делаем",
#                           "answer": "false"
#                         },
#                         {
#                           "name": "Другое",
#                           "answer": "Другое"
#                         }
#                       ]
#                     }
#                   ]
#                 },
#                 {
#                   "name": "Бильярд",
#                   "answer": "false",
#                   "questions": [
#                     {
#                       "name": "Сколько столов?",
#                       "answer": "number"
#                     }
#                   ]
#                 },
#                 {
#                   "name": "Караоке",
#                   "answer": "true",
#                   "questions": [
#                     {
#                       "name": "Сколько комнат?",
#                       "answer": "number"
#                     }
#                   ]
#                 }
#               ]
#             },
#             {
#               "name": "Пиво какое наливаете?",
#               "questions": [
#                 {
#                   "name": "У нас разное есть: Портер, Стаут, Пилзер, ИПА, АПА и тд.",
#                   "answer": "true"
#                 },
#                 {
#                   "name": "У нас целых два вида: светлое и темное",
#                   "answer": "false"
#                 }
#               ]
#             }
#           ]
#         },
#         {
#           "name": "Ресторан",
#           "answer": "true"
#         }
#       ]
#       },
#     {
#       "name": "Ваш телефон",
#       "questions": [
#         {
#           "name": "Телефон",
#           "answer": "Телефон"
#         }
#       ]
#     }
#   ]
# }
# print(check_answer(answer_dict, ['Ваш телефон']))

# dictionary = {
#   "questions": [
#     {
#       "name": "Ваша почта",
#       "questions": [
#         {
#           "name": "Почта",
#           "type": "text"
#         }
#       ]
#     },
#     {
#       "name": "Тип вашего заведения",
#       "questions": [
#         {
#           "name": "Бар",
#           "type": "checkbox",
#           "questions": [
#             {
#               "name": "Что ещё есть в вашем баре?",
#               "questions": [
#                 {
#                   "name": "Кухня",
#                   "type": "checkbox",
#                   "questions": [
#                     {
#                       "name": "Библиотека",
#                       "type": "checkbox"
#                     },
#                     {
#                       "name": "Какая у вас кухня?",
#                       "questions": [
#                         {
#                           "name": "Православная",
#                           "type": "checkbox"
#                         },
#                         {
#                           "name": "Сухарики сами делаем",
#                           "type": "checkbox"
#                         },
#                         {
#                           "name": "Другое",
#                           "type": "text"
#                         }
#                       ]
#                     }
#                   ]
#                 },
#                 {
#                   "name": "Бильярд",
#                   "type": "checkbox",
#                   "questions": [
#                     {
#                       "name": "Сколько столов?",
#                       "type": "number"
#                     }
#                   ]
#                 },
#                 {
#                   "name": "Караоке",
#                   "type": "checkbox",
#                   "questions": [
#                     {
#                       "name": "Сколько комнат?",
#                       "type": "number"
#                     }
#                   ]
#                 }
#               ]
#             },
#             {
#               "name": "Пиво какое наливаете?",
#               "questions": [
#                 {
#                   "name": "У нас разное есть: Портер, Стаут, Пилзер, ИПА, АПА и тд.",
#                   "type": "radio"
#                 },
#                 {
#                   "name": "У нас целых два вида: светлое и темное",
#                   "type": "radio"
#                 }
#               ]
#             }
#           ]
#         },
#         {
#           "name": "Ресторан",
#           "type": "checkbox"
#         }
#       ]
#       },
#     {
#       "name": "Ваш телефон",
#       "questions": [
#         {
#           "name": "Телефон",
#           "type": "text"
#         }
#       ]
#     }
#   ]
# }
#
# for test_path in [['Ваша почта'],['Тип вашего заведения'],['Тип вашего заведения', 'Бар', 'Что ещё есть в вашем баре?']]:
#     print(find_next_question_path(dictionary, test_path))
#     print(define_question(dictionary, test_path))
#     print()
