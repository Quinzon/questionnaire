function handleButtonClick(action) {
    const name = document.querySelector('.question__name').id;
    const questionElement = document.querySelector('.question');
    const elements = document.querySelectorAll('.question__answer');
    const pathValue = questionElement.dataset.path;
    const applicationIdValue = questionElement.dataset.id;
    let answerDictionary = {}; // Используем объект для хранения пар ключ-значение
    elements.forEach(element => {
        const inputElements = element.querySelectorAll('input');
        inputElements.forEach(input => {
            console.log(input);
            let value;
            if (input.type === 'checkbox' || input.type === 'radio') {
                value = input.checked;
            } else {
                value = input.value;
            }
            answerDictionary[input.id] = value;
        });
    });
    let data = {
        'application_id': applicationIdValue,
        'path': pathValue,
        'name': name,
        'answer': answerDictionary,
        'action': action
    };

    fetch('questions', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (response.ok) {
            return response.text();
        }
        throw new Error('Network response was not ok.');
    })
    .then(html => {
        document.querySelector('.form__wrapper').innerHTML = html;
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(event) {
        if (event.target.id === 'button-next') {
            handleButtonClick('next');
        } else if (event.target.id === 'button-complete') {
            handleButtonClick('complete');
        }
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
