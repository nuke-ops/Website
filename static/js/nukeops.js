// loading
function startLoading(buttonClass) {
    $(buttonClass).addClass("is-loading");
    $(buttonClass).prop('disabled', true);
}
function stopLoading(buttonClass) {
    $(buttonClass).removeClass("is-loading");
    $(buttonClass).prop('disabled', false);
}

function progressBar(barClass, value) {
    $(barClass).val(value)
}

// other
function copyToClipboard(inputId, popupId, popupDuration) {
    var copyText = document.getElementById(inputId).value;
    navigator.clipboard.writeText(copyText).then(() => {
        popup(popupId, popupDuration);
    });
}
function popup(elementId, duration) {
    $(`#${elementId}`).fadeIn();
    setTimeout(function () {
        $(`#${elementId}`).fadeOut();
    }, duration);
};