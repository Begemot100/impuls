let currentEmployeeId = null;

function openProcedureModal(employeeId) {
    fetch(`/get_employee_procedures/${employeeId}`)
        .then(response => response.json())
        .then(data => {
            document.querySelectorAll("#procedureList input[type='checkbox']").forEach(checkbox => {
                checkbox.checked = data.procedures.includes(parseInt(checkbox.value));
            });
            document.getElementById("procedureModal").style.display = "block";
            document.getElementById("procedureForm").dataset.employeeId = employeeId; 
        });
}

function closeProcedureModal() {
    document.getElementById("procedureModal").style.display = "none";
}

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
            location.reload();  
        } else {
            alert("Ошибка при обновлении процедур");
        }
    });
}
