// По мотивам https://codelab.pro/sozdaem-prostoj-kviz-na-javascript/

const data = JSON.parse(document.getElementById('data').textContent);
const questions = data.questions;

let cur_step = 0;
let recall_results = Object();

function renderStep() {
    const word_span = document.getElementById("word");
    word_span.innerText = questions[cur_step]["lexeme"];

    const input_div = document.getElementById("input_div");
    const input = document.createElement("input")
    input.type = "text"
    input_div.innerHTML = ""
    input_div.appendChild(input)
    input.focus()

    const info_div = document.getElementById("infobar");
    info_div.innerHTML = "";
    console.log(info_div.parentElement.classList);
    info_div.parentElement.classList.remove("green3", "red3");

    const button = document.getElementById("action_button");
    button.classList.remove("error");
    button.classList.add("green");
    button.innerText = "Проверить";
    button.onclick = checkAnswer;
}

function checkAnswer() {
    const input_div = document.getElementById("input_div");
    var input_val = input_div.firstChild.value.toLowerCase();
    const answers = questions[cur_step]["translations"];

    const correct = answers.includes(input_val);
    const other_answers = answers.filter(word => word.toLowerCase() != input_val);
    recall_results[questions[cur_step]["lexeme_id"]] = correct

    const result = document.createElement("div");
    result.classList.add("padding");

    const info_div = document.getElementById("infobar");
    const feedback = document.createElement("p")
    
    const button = document.getElementById("action_button");
    
    if (correct) {
        var result_html = `<span class="large-text green-text">${input_val}</span>`;
        if (other_answers.length > 0) {result_html += ", ";}
        info_div.parentElement.classList.add("green3")
        feedback.innerText = "Верно!"
    } else {
        var result_html = `<span class="large-text error-text">${input_val}</span>`;
        if (other_answers.length > 0) {result_html += "<br>";}
        info_div.parentElement.classList.add("red3")
        feedback.innerText = "Неверно"
        button.classList.remove("green");
        button.classList.add("error")
    }
    
    result_html += other_answers.join(", ");
    result.innerHTML = result_html;
    input_div.innerHTML = "";
    input_div.appendChild(result);

    info_div.innerHTML = ""
    info_div.appendChild(feedback);

    if (cur_step < questions.length - 1) {
        button.innerText = "Продолжить";
        button.onclick = nextStep;
    } else {
        button.innerText = "Закончить";
        button.onclick = results;
        const form = document.getElementById("quiz_form")
        form.method = "POST"
        form.action = `/quiz/${data.language_id}`
        const data_field = document.createElement("input")
        data_field.type = "hidden"
        data_field.name = "data"
        data_field.value = JSON.stringify(recall_results)
        form.appendChild(data_field)
    }
}

function nextStep() {
    cur_step += 1;
    renderStep();
}

function results() {
    const button = document.getElementById("action_button")
    button.type = "submit"
}

document.addEventListener("DOMContentLoaded", renderStep);
document.addEventListener(
    "keydown", 
    e => {if (e.code=="Enter") {e.preventDefault(); $("#action_button").click()}}
)