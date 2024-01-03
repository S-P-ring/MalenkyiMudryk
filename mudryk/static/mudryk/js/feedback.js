$(document).ready(function () {
    var page = 2;
    var $loadMoreButton = $('#load-more');
    var totalLoadedItems = 0

    function loadMoreFeedback() {
        $.ajax({
            url: window.location.href,
            data: {'page': page},
            dataType: 'html',
            success: function (data) {
                $('#feedback-list').append($(data).find('.feedback-item'));
                var $feedbackItems = $(data).find('.feedback-item');
                totalLoadedItems += $feedbackItems.length;
                page++;
                console.log($(data).find('#load-more').length)
                if ($(data).find('#load-more').length > 0 && totalLoadedItems % 5 === 0) {
                    $loadMoreButton.appendTo('#feedback-list');
                } else {
                    $loadMoreButton.remove();
                }
            }
        });
    }

    $loadMoreButton.click(loadMoreFeedback);
});


$(document).ready(function () {
    $('#feedbackForm').submit(function (event) {
        event.preventDefault();
        var form = this;

        fetch(form.action, {
            method: form.method,
            body: new FormData(form),
            headers: {
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    $('#confirmationMessage').fadeIn();

                    setTimeout(function () {
                        $('#confirmationMessage').fadeOut();
                    }, 4000);

                    form.reset();
                } else {
                    alert('Ошибка при отправке формы');
                }
            })
            .catch(error => {
                console.error('Ошибка при отправке формы:', error);
            });
    });
});