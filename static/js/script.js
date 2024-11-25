// Add Master
async function addMaster() {
    const name = document.getElementById('master-name').value;
    if (!name) {
        alert('Master name is required.');
        return;
    }

    const response = await fetch('/add_master', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name }),
    });

    const data = await response.json();
    if (response.ok) {
        alert(data.message);
        location.reload(); // Reload to update master list
    } else {
        alert(data.error);
    }
}

// Add Procedure
async function addProcedure() {
    const name = document.getElementById('procedure-name').value;
    const duration = document.getElementById('procedure-duration').value;
    const price = document.getElementById('procedure-price').value;
    const master_id = document.getElementById('procedure-master').value;

    if (!name || !duration || !price || !master_id) {
        alert('All fields are required.');
        return;
    }

    const response = await fetch('/add_procedure', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, duration, price, master_id }),
    });

    const data = await response.json();
    if (response.ok) {
        alert(data.message);
        location.reload(); // Reload to update procedure list
    } else {
        alert(data.error);
    }
}

// Редактировать мастера
function editMaster(masterId, currentName) {
    const newName = prompt("Enter new name for the master:", currentName);
    if (!newName) return;

    fetch(`/edit_master/${masterId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newName }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);
                location.reload();
            }
        });
}

// Удалить мастера
function deleteMaster(masterId) {
    if (!confirm("Are you sure you want to delete this master?")) return;

    fetch(`/delete_master/${masterId}`, {
        method: "DELETE",
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);
                location.reload();
            }
        });
}

// Редактировать процедуру
function editProcedure(procedureId, currentName, currentDuration, currentPrice, currentMasterId) {
    const newName = prompt("Enter new name for the procedure:", currentName) || currentName;
    const newDuration = prompt("Enter new duration (minutes):", currentDuration) || currentDuration;
    const newPrice = prompt("Enter new price (€):", currentPrice) || currentPrice;

    fetch(`/edit_procedure/${procedureId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: newName,
            duration: newDuration,
            price: newPrice,
            master_id: currentMasterId,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);
                location.reload();
            }
        });
}

// Удалить процедуру
function deleteProcedure(procedureId) {
    if (!confirm("Are you sure you want to delete this procedure?")) return;

    fetch(`/delete_procedure/${procedureId}`, {
        method: "DELETE",
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);
                location.reload();
            }
        });
}
