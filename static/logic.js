function refreshPage() {
    window.location.reload();
}

function updateCountdown(seconds) {
    document.getElementById('countdown').textContent = seconds;
    if (seconds > 0) {
        setTimeout(function() {
            updateCountdown(seconds - 1);
        }, 1000);
    } else {
        window.location.reload(); // Refresh when countdown reaches 0
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var initialCountdown = 30
    updateCountdown(initialCountdown);
});
