
function pollOutput(logId) {
    fetch(`/admin/django_admin_command_runner/commandlog/${logId}/live/`, {
        method: "GET"
    })
    .then(response => {
        if (!response.ok) {
            document.getElementById("live-output").innerText = "Failed to load command output.";
            throw new Error("Network response was not ok");
        }
        return response.text();
    })
    .then(data => {
        document.getElementById("live-output").innerHTML = data;
        setTimeout(() => pollOutput(logId), 1000);
    })
    .catch(error => {
        console.error("Error polling command output:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    // Only run on the CommandLog changelist page (check if URL ends with /commandlog/)
    if (!window.location.pathname.endsWith("/commandlog/")) return;

    const rows = document.querySelectorAll("#result_list tr");
    rows.forEach(row => {
        const cells = row.querySelectorAll("td");
        if (cells.length && row.dataset.objectId) {
            const logId = row.dataset.objectId;
            const infoBtn = document.createElement("button");
            infoBtn.textContent = "ℹ️";
            infoBtn.onclick = () => showLiveOutput(logId);
            cells[cells.length - 1].appendChild(infoBtn);
        }
    });
});
