from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from questionnaire.settings import BASE_DIR

register = template.Library()


@register.simple_tag
def questions_tag(*args):
    print(args[0])
    return render_to_string(
                f"{BASE_DIR}/form/templates/form/question.html",
                context={'questions': args[0]}
            )


# @register.simple_tag
# def questions_tag(*args):
#     html = mark_safe(collect_questions(args[0]))
#     print(html)
#     return html
#
#
# def collect_questions(questions):
#     html = ''
#     print(questions)
#
#     for question in questions:
#
#         widget = question.get('type', 'question')
#
#         html += render_to_string(
#                 f"{BASE_DIR}/form/templates/form/widgets/{widget}.html",
#                 context={'question': question}
#             )
#         if question.get('questions'):
#             html += collect_questions(question['questions'])
#
#     return html



    # for question in questions:
    #
    #     for key, item in question.items():
    #
    #         widget = item if key == 'type' else 'question'
    #
    #         if key == "questions":
    #             html += collect_questions(question['questions'])
    #
    #         html += render_to_string(
    #             f"{BASE_DIR}/form/templates/form/widgets/{widget}.html",
    #             context={'question': question}
    #         )
    #
    #         print(html)
    # return html


# @register.simple_tag
# def questions_tag(questions):
#     return mark_safe(collect_questions(questions))
#
#
# def collect_questions(questions):
#     html = ""
#     for question in questions:
#         if 'type' in question:
#             widget = question['type']
#         else:
#             widget = 'question'
#
#         if widget == 'question':
#             if 'questions' in question:
#                 nested_html = collect_questions(question['questions'])
#                 html += nested_html
#
#         html += render_to_string(
#             f"{BASE_DIR}/form/templates/form/widgets/{widget}.html",
#             context={'question': question}
#         )
#
#     return html