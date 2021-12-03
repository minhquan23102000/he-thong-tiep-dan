const chatinput = document.querySelector("#chat-input");
const speech2text = chatinput.querySelector("input");
const SpeechRecogonition = window.SpeechRecogonition || window.webkiSpeechRecogonition;

if (SpeechRecogonition) {
    console.log("Trinh duyet cua ban duoc ho tro su dung cong cu chuyen doi giong noi thanh van ban");
    chatinput.insertAdjacentHTML("beforeend", '<button type="button"><i class="fas fa-microphone"></i></button>');
    const micBtn = chatinput.querySelector("speech-button");
    const micIcon = micBtn.querySelector("i");

    const recognition = new SpeechRecogonition();

    micBtn.addEventListener("click", micBtnClick);

    function micBtnClick() {
        if (micIcon.classList.contains("fa-microphone")) { // bat dau ghi am
            recognition.start();

        } else { // dung ghi am
            recognition.stop();
        }
    }

    recognition.addEventListener("start", startSpeechRecogonition);

    function startSpeechRecogonition() {
        micIcon.classList.remove("fa-microphone");
        micIcon.classList.add("fa-microphone");
        console.log("Bat dau thu am");
    }
    recognition.addEventListener("en", endSpeechRecogonition);

    function endSpeechRecogonition() {
        micIcon.classList.remove("fa-microphone");
        micIcon.classList.add("fa-microphone");
        console.log("Dung thu am");
    }

} else {
    console.log("Trinh duyet cua ban khong duoc ho tro su dung cong cu chuyen doi giong noi thanh van ban");
}