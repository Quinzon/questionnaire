def check_answer(struct, path):
    """Ищет какой следующий вопрос показать"""
    question = define_question(struct, path)

    next_path = find_next_question_path(struct, path)
    next_answer = define_question(struct, next_path)
    if next_path is None:
        return question, path

    if 'answer' not in next_answer:
        return next_answer, next_path

    if 'questions' in question:
        path = check_next_question(struct, path)
        if path is None:
            question = struct['questions'][(struct['questions'].index(question)) + 1]

            return question, [question['name']]

    question = define_question(struct, path)
    if 'answer' in question:
        path = find_next_question_path(struct, path)
        question = define_question(struct, path)

    next_path = find_next_question_path(struct, path)
    if next_path is None:
        return question, path

    return question, path


def check_next_question(struct, path, question_id=0, answer_id=0) -> list or None:
    """Определяет следующий доступный вопрос. Возвращает path"""
    question = define_question(struct, path)

    if len(path) == 1 and question['questions'] == answer_id+1:
        return None

    if len(question['questions']) == question_id:
        parent_question = define_question(struct, path[:-1])
        answer_id = parent_question['questions'].index(question)
        return check_next_question(struct, path[:-1], 0, answer_id + 1)

    if len(path) % 2 == 0:
        path += [question['questions'][question_id]['name']]
        return path
    else:
        parent_answer = define_question(struct, path[:-1])
        question_id = parent_answer['questions'].index(question)
    if all(not _['answer'] or not (_['answer'] and 'questions' in _) for _ in question['questions'][answer_id:]):
        return check_next_question(struct, path[:-1], question_id + 1)

    for quest in question['questions'][answer_id:]:
        if not quest['answer'] or not (quest['answer'] and 'questions' in quest):
            continue
        return path + [quest['name']]


def paste_answers(struct, path, answer) -> dict:
    """Записывает ответ на вопрос по пути path в структуру struct"""
    if not path:
        for question in struct['questions']:
            for key, item in answer.items():
                if question['name'] == key:
                    question['answer'] = item
        return struct

    for question in struct.get('questions', []):
        if question.get('name') == path[0]:
            paste_answers(question, path[1:], answer)

    return struct


def define_question(struct, path=None) -> dict:
    """Определяет вопрос по пути path из struct"""
    if len(path) == 0:
        return struct

    for question in struct['questions']:
        if question['name'] == path[0]:
            return define_question(question, path[1:])


def create_application(dictionary) -> dict:
    """Создает пустую анкету ответа на основе формы"""
    for key, value in list(dictionary.items()):
        if isinstance(value, list):
            for element in value:
                if isinstance(element, dict):
                    create_application(element)
        if key == 'type':
            dictionary['answer'] = None

    return dictionary


def find_next_question_path(struct, path, current_path=None) -> list or None:
    """Находит следующий path по struct"""
    if current_path is None:
        current_path = []

    if not path:
        return None

    if len(path) == 1:
        for i, question in enumerate(struct['questions']):
            if question['name'] == path[0]:
                if 'questions' in question:
                    for child_question in question['questions']:
                        if 'questions' in child_question:
                            return current_path + path + [child_question['name']]

                while i + 1 < len(struct['questions']):
                    if 'questions' in struct['questions'][i + 1]:
                        return current_path + [struct['questions'][i + 1]['name']]
                    i += 1
                else:
                    return None
        return None

    for i, question in enumerate(struct['questions']):
        if question['name'] == path[0]:
            if 'questions' in question:
                sub_path = find_next_question_path(question, path[1:], current_path + [question['name']])
                if sub_path is not None:
                    return sub_path

            while i + 1 < len(struct['questions']):
                if 'questions' in struct['questions'][i + 1]:
                    return current_path + [struct['questions'][i + 1]['name']]
                i += 1
            else:
                return None
    return None
