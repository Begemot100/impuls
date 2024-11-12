let currentEmployeeId = null;

// Открыть модальное окно и загрузить процедуры сотрудника
function openProcedureModal(employeeId) {
    fetch(`/get_employee_procedures/${employeeId}`)
        .then(response => response.json())
        .then(data => {
            // Отметить уже выбранные процедуры
            document.querySelectorAll("#procedureList input[type='checkbox']").forEach(checkbox => {
                checkbox.checked = data.procedures.includes(parseInt(checkbox.value));
            });
            document.getElementById("procedureModal").style.display = "block";
            document.getElementById("procedureForm").dataset.employeeId = employeeId; // Сохраняем ID сотрудника
        });
}

// Закрытие модального окна
function closeProcedureModal() {
    document.getElementById("procedureModal").style.display = "none";
}

// Сохранение выбранных процедур
function saveProcedures() {
    const employeeId = document.getElementById("procedureForm").dataset.employeeId;
    const selectedProcedures = Array.from(document.querySelectorAll("#procedureList input[type='checkbox']"))
        .filter(checkbox => checkbox.checked)
        .map(checkbox => parseInt(checkbox.value));

    fetch(`/save_procedures/${employeeId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ procedures: selectedProcedures })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Процедуры успешно обновлены");
            closeProcedureModal();
            location.reload();  // Перезагрузить страницу для обновления списка процедур
        } else {
            alert("Ошибка при обновлении процедур");
        }
    });
}
