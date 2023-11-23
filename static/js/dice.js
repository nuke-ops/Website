
// cookies

$(function () { getCookies() }); // load cookies on page load

function deleteAllCookies() {
    startLoading("#clearButton");
    Cookies.remove('name');
    Cookies.remove('cus');
    Cookies.remove('str');
    Cookies.remove('dex');
    Cookies.remove('con');
    Cookies.remove('int');
    Cookies.remove('wis');
    Cookies.remove('cha');
    Cookies.remove('dark');
    stopLoading("#clearButton");
}

function setCookies() {
    Cookies.set('name', $("#name").val());
    Cookies.set('cus', $("#cus_input").val());
    Cookies.set('str', $("#str_input").val());
    Cookies.set('dex', $("#dex_input").val());
    Cookies.set('con', $("#con_input").val());
    Cookies.set('int', $("#int_input").val());
    Cookies.set('wis', $("#wis_input").val());
    Cookies.set('cha', $("#cha_input").val());
    if ($('#dark-mode_button').is(":checked")) {
        Cookies.set('dark', true);
    }
    else {
        Cookies.set('dark', false);
    }
}

function getCookies() {
    $("#name").attr("value", Cookies.get("name"));
    $("#cus_input").attr("value", Cookies.get("cus"));
    $("#str_input").attr("value", Cookies.get("str"));
    $("#dex_input").attr("value", Cookies.get("dex"));
    $("#con_input").attr("value", Cookies.get("con"));
    $("#int_input").attr("value", Cookies.get("int"));
    $("#wis_input").attr("value", Cookies.get("wis"));
    $("#cha_input").attr("value", Cookies.get("cha"));
    $("#dark-mode_button")[0].checked = (Cookies.get("dark") === 'true');
}

// socket

const socket = new WebSocket(socketBaseUrl);

socket.onopen = (event) => {
    console.log("WebSocket connection opened:", event);
};

socket.onmessage = function (event) {
    if (event.data === "update") {
        // console.log("WebSocket message received:", event.data);
        updateTable();
    }
};

socket.onclose = (event) => {
    console.log("WebSocket connection closed:", event);
};

// dice

function updateTable() {
    fetch('/api/get_dice_rolls')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#json_table tbody');
            tableBody.innerHTML = "";

            data.forEach(record => {
                const row = tableBody.insertRow();
                row.innerHTML = `
                    <td>${record.name}</td>
                    <td>${record.dice}</td>
                    <td>${record.sides}</td>
                    <td>${record.throws}</td>
                    <td>${record.sum}</td>
                    <td>${record.modifier}</td>
                    <td>${record.date}</td>
                `;
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}

function sendDiceRoll() {
    startLoading("#formSubmit");
    const form = document.getElementById("dice_form");

    // form values
    let name = form.elements["name"].value;
    let dice = form.elements["dice"].value;
    let sides = form.elements["sides"].value;
    // Error handlers
    const formErrors = new Array();
    // name
    if (!name) { // No name
        formErrors.push("You must enter a name");
    }
    else if (!alphanumeric(name)) { // Illegal characters
        formErrors.push("Illegal characters in name");
    }
    else if (name.length >= 35) { // name to long
        formErrors.push("Name length limit: 35");
    }
    //dice
    if (dice > 50) { // Too many dice
        formErrors.push("Max amount of dice: 50");
    }
    if (sides > 100) { // Too many sides
        formErrors.push("Max amount of sides: 100");
    }
    if (dice < 1 || !dice) { // Negative dice
        formErrors.push("There must be at leas one dice");
    }
    if (sides < 2 || !sides) { // Negative sides
        formErrors.push("Dice must have at least 2 sides");
    }
    if (formErrors.length > 0) {
        formError(formErrors);
        return;
    }

    // check if there's modifier
    let raw_modifier = 0;
    let modifier = "";

    if (!$("input[id='non_radio']:checked").val()) {
        let modifiers = ["cus", "str", "dex", "con", "int", "wis", "cha"];
        for (mod of modifiers) {
            if ($("input[id='" + mod + "_radio']:checked").val()) {  // if radio button is checked
                raw_modifier = $("#" + mod + "_input").val();           // add it's value to roll
                // assemble string eg. str(+5)
                modifier = mod + "(";
                if (raw_modifier > 0) {
                    modifier += "+"
                };
                modifier += raw_modifier + ")"
            };
        }
    }

    // roll
    let throws = [];
    for (let i = 1; i <= dice; i++) {
        throws.push(Math.floor((Math.random() * sides) + 1));
    }

    // sum
    let sum = 0;
    for (const x of throws) {
        sum += x;
    } sum += raw_modifier * 1;

    const diceRollData = {
        name: name,
        dice: dice,
        sides: sides,
        throws: throws,
        sum: sum,
        modifier: modifier
    };
    socket.send(JSON.stringify(diceRollData));
    $.ajax({
        type: "POST",
        url: "/api/insert_dice_roll",
        contentType: "application/json",
        data: JSON.stringify({
            name: name,
            dice: dice,
            sides: sides,
            throws: throws,
            sum: sum,
            modifier: modifier
        }),
    })
    stopLoading("#formSubmit");
}

// rest of the stuff

function showProgressBar() {
    $("#formSubmitDiv").fadeOut();
    $("#progressBar").fadeIn();
    $("#progressBar").addClass("progress");
}
function hideProgressBar() {
    $("#progressBar").removeClass("progress");
    $("#progressBar").fadeOut();
    $("#formSubmitDiv").fadeIn();
    progressBar("#progressBar", 0);
}


function alphanumeric(inputtxt) {
    var letterNumber = /^[0-9a-zA-Z ]+$/;
    if (inputtxt.match(letterNumber)) {
        return true;
    } else {
        return false;
    }
}

function formError(errors) {
    let output = "";
    for (const x of errors) {
        output += x + "<br/>";
    }

    $("#formErrorHead").addClass("message-header");
    $("#formErrorHead").css({ "margin-top": "10px" });
    $("#formErrorHead").html("Error <button class='delete' onclick='closeError();'/>");
    $("#formErrorBody").addClass("message-body");
    $("#formErrorBody").html(output);
    stopLoading("#formSubmit");
}
function closeError() {
    $("#formErrorHead").removeClass("message-header");
    $("#formErrorHead").css({ "margin-top": "10px" });
    $("#formErrorBody").removeClass("message-body");
    $("#formErrorHead, #formErrorBody").html("");
}

function calc() {
    startLoading("#calculator_button");
    try {
        let input = document.getElementById("calculator_input").value;
        if (input.indexOf(',') > -1) {
            input = input.replace(",", ".");
        }
        let output = math.evaluate(input)
        $("#calculator_input").val(output);
        stopLoading("#calculator_button");
    } catch (error) {
        $("#calculator_input").val("");
        $("#calculator_input").attr("placeholder", "Invalid input");
        stopLoading("#calculator_button");
    }
}

function set_dice(dice, sides) {
    $("#dice").val(dice);
    $("#sides").val(sides);
}

function dark_mode() {
    if (!$("#dark-mode_button").is(':checked')) {
        $("#dark-mode_label").removeClass("is-outlined");
        $("#dark-mode").html(`
        <style>
            input::placeholder{
                color: rgba(63, 61, 61, 0.651) !important;
            }
            .box, .input, .table{
                background-color: #121212 !important;
                color: white !important;
            }
            th:nth-child(n), td:nth-child(n){
                color: white;
            }
        </style>
        `);
    } else {
        $("#dark-mode_label").addClass("is-outlined");
        $("#dark-mode").html(``);
    }
}
