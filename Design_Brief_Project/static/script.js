document.addEventListener("DOMContentLoaded", function() {
    const copyButton = document.getElementById('copy-brief');
    const modifyButton = document.getElementById('modify-brief');
    const briefOutput = document.getElementById('brief-output');

    copyButton.addEventListener('click', function() {
        briefOutput.select();
        document.execCommand('copy');
        alert('Brief copied to clipboard');
    });

    modifyButton.addEventListener('click', function() {
        briefOutput.removeAttribute('readonly');
        briefOutput.focus();
    });
});
