// Auto-submit project state form
document.getElementById('project-state-select').addEventListener('change', function () {
    document.getElementById('project-state-form').submit();
});

// Auto-submit task state forms
document.querySelectorAll('.auto-submit-select').forEach(function (select) {
    select.addEventListener('change', function () {
        this.form.submit();
    });
});