
function pollOutput(logId) {
    const outputContainer = document.getElementById("live-output");
    const statusLabel = document.getElementById("command-status");
    const interval = setInterval(() => {
        fetch(`/admin/django_admin_command_runner/commandlog/${logId}/live/`, {
            method: "POST",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
        })
        .then(res => res.json())
        .then(data => {
            if (data.output) {
                outputContainer.innerHTML = data.output.join('<br>');
            }
            if (data.status) {
                statusLabel.textContent = data.status;
            }
            if (data.finished) {
                clearInterval(interval);
            }
        });
    }, 2000);
}

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
