// Wait for the document to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', function () {
    // Find the timer element in the HTML
    const timerElement = document.getElementById('elapsed-timer');

    // If the timer element doesn't exist, do nothing.
    // This prevents errors on pages where the timer isn't active.
    if (!timerElement) {
        return;
    }

    // Get the start time from the 'data-start-time' attribute we will add
    const startTimeString = timerElement.getAttribute('data-start-time');
    if (!startTimeString) {
        console.error("Timer element is missing the 'data-start-time' attribute.");
        return;
    }

    // Convert the timestamp string (in seconds) to a Date object (in milliseconds)
    const startTime = new Date(parseInt(startTimeString, 10) * 1000);

    function pad(num) {
        return num.toString().padStart(2, '0');
    }

    function updateTimer() {
        const now = new Date();
        let diff = now - startTime;
        if (diff < 0) diff = 0;

        const totalSeconds = Math.floor(diff / 1000);
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        // Note: The original code had a 'days' calculation, which is good.
        // Let's keep it for long-running tasks.
        const days = Math.floor(totalSeconds / 86400);
        const displayHours = Math.floor((totalSeconds % 86400) / 3600);

        const formatted = days > 0
            ? `${days}d ${pad(displayHours)}:${pad(minutes)}:${pad(seconds)}`
            : `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;

        timerElement.textContent = formatted;
    }

    // Run the timer immediately and then every second
    updateTimer();
    setInterval(updateTimer, 1000);
});