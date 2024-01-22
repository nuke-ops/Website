// on load

$(function () { load_cookies() });
$(function () { updateTable() });
$(function () { dark_mode() });

// cookies

function deleteAllCookies() {
    startLoading("#clearButton");
    Cookies.remove('user_data');
    stopLoading("#clearButton");
}

function save_cookies() {
    let userData = {
        name: $("#name").val(),
        dark_theme: $('#dark-mode_button').is(":checked"),
        cus: $("#cus_input").val(),
        str: $("#str_input").val(),
        dex: $("#dex_input").val(),
        con: $("#con_input").val(),
        int: $("#int_input").val(),
        wis: $("#wis_input").val(),
        cha: $("#cha_input").val(),
    };

    Cookies.set('user_data', JSON.stringify(userData));
}

function load_cookies() {
    let userData = Cookies.get('user_data');
    if (userData) {
        userData = JSON.parse(userData);
        $("#name").val(userData.name);
        $("#cus_input").val(userData.cus);
        $("#str_input").val(userData.str);
        $("#dex_input").val(userData.dex);
        $("#con_input").val(userData.con);
        $("#int_input").val(userData.int);
        $("#wis_input").val(userData.wis);
        $("#cha_input").val(userData.cha);
        let darkModeButton = $("#dark-mode_button");
        if (darkModeButton.length > 0) {
            darkModeButton[0].checked = userData.dark_theme;
        }
    }
}

// socket

let protocol = 'ws://';
if (window.location.protocol === 'https:') {
    protocol = 'wss://';
}
const socket = new WebSocket(`${protocol}${window.location.host}/ws/dice/`);

socket.onopen = function open() {
    console.log('WebSockets connection created.');
};

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    if (data["message"] === "update_dice_roll") {
        updateTable();
    }
    if (data["message"] === "update_mbs") {
        getMbs();
    }
};

// mbs

async function getMbs() {
    try {
        const response = await fetch('/api/get_mbs/');
        const data = await response.json();
        document.getElementById('mbs_textbox').innerText = data.value;
    } catch (error) {
        console.error('Error fetching and updating MBS data:', error);
    }
}

async function updateMbs() {
    startLoading("mbs_textbox");
    try {
        const key = await fetch('/api/get_mbs/?refresh=true')
        socket.send(JSON.stringify({ 'update_mbs': key }));
    } catch (error) {
        console.error('Error triggering MBS update:', error);
    } finally {
        stopLoading("mbs_textbox");
    }
}

// dice

function updateTable() {
    fetch('/api/get_dice_rolls/')
        .then(response => response.json())
        .then(data => {
            const sortedData = Object.values(data).sort((a, b) => b.id - a.id);
            const tableBody = document.querySelector('#json_table tbody');
            tableBody.innerHTML = "";
            sortedData.forEach(record => {
                const row = tableBody.insertRow();
                row.innerHTML = `
                    <td>${record.name}</td>
                    <td>${record.dice}</td>
                    <td>${record.sides}</td>
                    <td>${record.throws}</td>
                    <td>${record.modifier}</td>
                    <td>${record.sum}</td>
                    <td>${formatDate(record.date)}</td>
                `;
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}

function formatDate(dateTimeString) {
    const originalDate = new Date(dateTimeString);
    const formattedDate = originalDate.toLocaleDateString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
    });

    const formattedTime = originalDate.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: false,
    });
    return `${formattedDate}<br>${formattedTime}`;
}


function sendDiceRoll() {
    startLoading("#formSubmit");
    const form = document.getElementById("dice_form");

    // form values
    let name = form.elements["name"].value;
    let dice = parseInt(form.elements["dice"].value);
    let sides = parseInt(form.elements["sides"].value);
    // Error handlers
    const formErrors = new Array();
    // name
    if (!name) {
        formErrors.push("You must enter a name");
    }
    else if (!alphanumeric(name)) {
        formErrors.push("Name must be alphanumeric");
    }
    else if (name.length > 35) {
        formErrors.push("Name length limit: 35");
    }
    //dice
    if (dice > 50) {
        formErrors.push("Max amount of dice: 50");
    }
    if (sides > 100) {
        formErrors.push("Max amount of sides: 100");
    }
    if (dice < 1 || !dice) {
        formErrors.push("There must be at leas 1 dice");
    }
    if (sides <= 1 || !sides) {
        formErrors.push("Dice must have at least 2 sides");
    }
    if (formErrors.length > 0) {
        formError(formErrors);
        return;
    }

    const formData = new FormData(form);

    // check if there's modifier
    let raw_modifier = 0;
    let modifier = "";
    if (!$("input[id='non_radio']:checked").val()) {
        let modifiers = ["cus", "str", "dex", "con", "int", "wis", "cha"];
        for (mod of modifiers) {
            if ($("input[id='" + mod + "_radio']:checked").val()) {  // if radio button is checked
                raw_modifier = $("#" + mod + "_input").val(); //^ add it's value to roll
                // assemble string eg. str(+2)
                modifier = mod + "(";
                if (raw_modifier > 0) {
                    modifier += "+"
                };
                modifier += raw_modifier + ")"
            };
        }
        formData.append('modifier', modifier);
        formData.append('raw_modifier', raw_modifier);
    }

    fetch('/api/insert_dice_roll/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken'),
        },
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            socket.send(JSON.stringify({ 'update_dice_roll': data }));
        })
        .catch(error => {
            console.error('Error:', error);
        })
        .finally(() => {
            stopLoading("#formSubmit");
        });
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
    const letterNumber = /^[0-9a-zA-Z ]+$/;
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
    $("#formErrorHead").css({ "margin-top": "25px" });
    $("#formErrorHead").html("Error <button class='delete' onclick='closeError();'/>");
    $("#formErrorBody").addClass("message-body");
    $("#formErrorBody").html(output);
    stopLoading("#formSubmit");
}
function closeError() {
    $("#formErrorHead").removeClass("message-header");
    $("#formErrorHead").css({ "margin-top": "25px" });
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
    }
    catch (error) {
        $("#calculator_input").val("");
        $("#calculator_input").attr("placeholder", "Invalid input");
    }
    finally {
        stopLoading("#calculator_button");
    }
}

function set_dice_values(dice, sides) {
    $("#dice").val(dice);
    $("#sides").val(sides);
}

function dark_mode() {
    if ($("#dark-mode_button").is(':checked')) {
        $("#dark-mode_label").removeClass("is-outlined");
        $("#dark-mode").html(`
        <style>
            .box, .input, .table{
                background-color: white !important;
                color: #121212 !important;
            }
            th:nth-child(n), td:nth-child(n){
                color: #121212;
            }
        </style>
        `);
    } else {
        $("#dark-mode_label").addClass("is-outlined");
        $("#dark-mode").html(``);
    }
}
