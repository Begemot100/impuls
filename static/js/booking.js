function getAvailableSlots() {
    const clientName = document.getElementById("client_name").value;
    const procedureId = document.getElementById("procedure").value;
    const doctorId = document.getElementById("doctor").value;
    const date = document.getElementById("date").value;

    if (!clientName || !procedureId || !doctorId || !date) {
        alert("Пожалуйста, заполните все поля.");
        return;
    }

    fetch(`/get_slots?master_id=${doctorId}&date=${date}`)
        .then(response => response.json())
        .then(data => {
            const slotsContainer = document.getElementById("slots");
            slotsContainer.innerHTML = ""; // Очищаем контейнер

            if (data.slots.length === 0) {
                slotsContainer.innerHTML = "<p>Нет доступных слотов.</p>";
            } else {
                data.slots.forEach(slot => {
                    const slotElement = document.createElement("button");
                    slotElement.textContent = slot;
                    slotElement.classList.add("slot-button");
                    slotElement.addEventListener("click", () => createBooking(clientName, procedureId, doctorId, date, slot));
                    slotsContainer.appendChild(slotElement);
                });
            }
        })
        .catch(error => console.error("Ошибка при получении слотов:", error));
}

function createBooking(clientName, procedureId, doctorId, date, time) {
    const datetime = `${date} ${time}:00`;

    fetch("/create_booking", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            client_name: clientName,
            procedure_id: procedureId,
            doctor_id: doctorId,
            datetime: datetime
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Запись успешно создана!");
        } else {
            alert("Ошибка при создании записи. Пожалуйста, попробуйте снова.");
        }
    })
    .catch(error => console.error("Ошибка при создании записи:", error));
}
