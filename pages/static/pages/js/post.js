function openWriteCommentModal(replyTo) {
    document.getElementById("modal-reply-to").innerHTML = document.getElementById(replyTo).innerHTML;
    document.getElementById("modal-reply-to-id").value = replyTo;
    document.getElementById("write-comment-modal").style.display = "block";
}


function dismissWriteCommentModal() {
    document.getElementById("write-comment-modal").style.display = "none";
    document.getElementById("id_text").value = "";
    const cmntErrors = document.getElementById("id_text_error");
    if (cmntErrors) {
        cmntErrors.style.display = "none";
    }
}


window.onclick = function(event) {
    if (event.target === document.getElementById("write-comment-modal")) {
        dismissWriteCommentModal();
    }
}
