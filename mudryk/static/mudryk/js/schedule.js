var selected_course
var dates

document.addEventListener('DOMContentLoaded', function () {
    // Находим форму по ее id
    var form = document.getElementById('course-form');
    // Добавляем обработчик события отправки формы
    form.addEventListener('submit', function (event) {
        // Отменяем стандартное действие формы, чтобы страница не перезагружалась
        event.preventDefault();
        // Получаем данные формы
        var formData = new FormData(form);
        selected_course = formData.get('selected_option')

        // Отправляем данные на сервер
        fetch('/get_course_days/', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                // Проверяем ответ от сервера
                if (data.success === true) {
                    // Скрываем первую форму
                    form.style.display = 'none';

                    // Находим вторую форму по ее id
                    var secondForm = document.getElementById('course-day-form');

                    // Показываем вторую форму
                    secondForm.style.display = 'block';

                    // Заполняем вторую форму данными
                    var selectOption = secondForm.querySelector('#selectOption');
                    selectOption.innerHTML = ''; // Очищаем текущие опции
                    dates = data.days_list
                    // Добавляем новые опции на основе данных от сервера
                    for (var i = 0; i < data.days_list.length; i++) {
                        var option = document.createElement('option');
                        option.value = data.days_list[i].date;
                        option.textContent = data.days_list[i].day_str;
                        selectOption.appendChild(option);
                    }
                } else {
                    console.log(data)
                    // В случае неудачи можно выполнить какие-то дополнительные действия
                    console.error('Ошибка на сервере');
                }
            })
            .catch(error => {
                console.error('Ошибка при отправке данных на сервер', error);
            });
    });
});


var selected_date

document.addEventListener('DOMContentLoaded', function () {
    // Находим форму по ее id

    var form = document.getElementById('course-day-form');
    // Добавляем обработчик события отправки формы
    form.addEventListener('submit', function (event) {
        // Отменяем стандартное действие формы, чтобы страница не перезагружалась
        event.preventDefault();

        // Получаем данные формы
        var formData = new FormData(form);
        selected_date = formData.get('selected_option')
        var times
        for (var i = 0; i < dates.length; i++) {
            date_with_times = dates[i].date;
            if (selected_date === dates[i].date) {
                times = dates[i].times
            }
        }


        form.style.display = 'none';
        var secondForm = document.getElementById('course-time-form');
        secondForm.style.display = 'block';

        var selectOption = secondForm.querySelector('#selectOption');
        selectOption.innerHTML = ''; // Очищаем текущие опции
        for (var i = 0; i < times.length; i++) {
            var option = document.createElement('option');
            option.value = times[i];
            option.textContent = times[i];
            selectOption.appendChild(option);
        }
    });
});


var selected_time
document.addEventListener('DOMContentLoaded', function () {
    // Находим форму по ее id
    var form = document.getElementById('course-time-form');
    // Добавляем обработчик события отправки формы
    form.addEventListener('submit', function (event) {
        // Отменяем стандартное действие формы, чтобы страница не перезагружалась
        event.preventDefault();
        // Получаем данные формы
        var formData = new FormData(form);
        selected_time = formData.get('selected_option')
        // Отправляем данные на сервер

        form.style.display = 'none';
        var secondForm = document.getElementById('record-form');
        secondForm.style.display = 'block';
    });
});


document.addEventListener('DOMContentLoaded', function () {
    // Находим форму по ее id
    var form = document.getElementById('record-form');
    // Добавляем обработчик события отправки формы
    form.addEventListener('submit', function (event) {
        // Отменяем стандартное действие формы, чтобы страница не перезагружалась
        event.preventDefault();

        // Получаем данные формы
        var formData = new FormData(form);
        formData.append('selected_course', selected_course);
        formData.append('selected_day', selected_date);
        formData.append('selected_time', selected_time);

        selected_course = formData.get('selected_option')
        // Отправляем данные на сервер
        fetch('/submit_record/', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                // Проверяем ответ от сервера
                if (data.success === true) {
                    var secondForm = document.getElementById('record-form');
                    secondForm.style.display = 'none';
                    var container = document.getElementById('form-container');
                    container.style.display = 'none';
                    var success_mesage = document.getElementById('success-message');
                    success_mesage.style.display = 'block';
                } else {
                    console.log(data.error)
                    // В случае неудачи можно выполнить какие-то дополнительные действия
                    console.error('Ошибка на сервере');
                }
            })
            .catch(error => {
                console.error('Ошибка при отправке данных на сервер', error);
            });
    });
});