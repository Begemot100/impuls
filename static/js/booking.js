async function fetchProcedures() {
    const masterId = document.getElementById("master").value;

    if (!masterId) {
        alert("Please select a specialist.");
        return;
    }

    const response = await fetch(`/api/get_procedures?master_id=${masterId}`);
    const data = await response.json();

    const procedureSelect = document.getElementById("procedure");
    procedureSelect.innerHTML = "<option value='' disabled selected>Select a procedure</option>";

    if (data.error) {
        alert(data.error);
        return;
    }

    if (data.procedures && data.procedures.length > 0) {
        data.procedures.forEach(procedure => {
            const option = document.createElement("option");
            option.value = procedure.id;
            option.textContent = `${procedure.name} (${procedure.duration} min)`;
            procedureSelect.appendChild(option);
        });

        document.getElementById("procedure-container").style.display = "block";
        document.getElementById("check-slots-btn").style.display = "block";
    } else {
        alert("No procedures available for this specialist.");
        document.getElementById("procedure-container").style.display = "none";
        document.getElementById("check-slots-btn").style.display = "none";
    }
}
async function fetchSlots() {
    const date = document.getElementById("date").value;
    const masterId = document.getElementById("master").value;
    const procedureId = document.getElementById("procedure").value;

    if (!date || !masterId || !procedureId) {
        alert("Please fill out all fields.");
        return;
    }

    const response = await fetch(`/api/get_slots?master_id=${masterId}&date=${date}&procedure_id=${procedureId}`);
    const data = await response.json();

    const slotsDiv = document.getElementById("slots");
    slotsDiv.innerHTML = "";

    if (data.error) {
        alert(data.error);
        slotsDiv.innerHTML = "<p>No available slots for the selected date.</p>";
        return;
    }

    if (data.slots && data.slots.length > 0) {
        data.slots.forEach(slot => {
            const button = document.createElement("button");
            button.textContent = `Book ${slot.start.slice(11, 16)} - ${slot.end.slice(11, 16)}`;
            button.classList.add("slot-button");
            button.onclick = () => initiatePayment(slot.start, slot.end, masterId, date, procedureId);
            slotsDiv.appendChild(button);
        });
    } else {
        slotsDiv.innerHTML = "<p>No available slots for the selected date.</p>";
    }
}

async function initiatePayment(start, end, masterId, date, procedureId) {
    const email = document.getElementById("email").value.trim();
    const clientName = document.getElementById("client-name").value.trim();

    console.log("Start Time:", start);
    console.log("End Time:", end);
    console.log("Master ID:", masterId);
    console.log("Date:", date);
    console.log("Procedure ID:", procedureId);
    console.log("Email:", email);
    console.log("Client Name:", clientName);

    if (!start || !end || !masterId || !date || !procedureId || !email || !clientName) {
        alert("Please fill out all fields, including name and email.");
        return;
    }

    try {
        const response = await fetch('/api/create_payment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                start_time: start,
                end_time: end,
                master_id: masterId,
                date: date,
                procedure_id: procedureId,
                email: email,
                client_name: clientName
            })
        });

        const data = await response.json();

        if (data.error) {
            alert(`Payment error: ${data.error}`);
            return;
        }

        document.getElementById('payment-section').style.display = 'block';
        alert("Payment initiated. Complete the payment to confirm your booking.");
    } catch (err) {
        console.error("Error initiating payment:", err);
        alert("An error occurred while initiating payment.");
    }
}


function showPaymentSection() {
    document.getElementById('slots').style.display = 'none';
    document.getElementById('payment-section').style.display = 'block';
}

function redirectToStripe() {
    const stripePaymentLink = "https://buy.stripe.com/test_5kA4h48kP5Ei5Fu3cc"; // Ваш платёжный линк
    window.location.href = stripePaymentLink;
}
function validateClientInfo() {
    const name = document.getElementById("client-name").value.trim();
    const email = document.getElementById("email").value.trim();

    if (!name || !email) {
        alert("Please fill out all fields, including your name and email.");
        return false;
    }

    return { name, email };
}
