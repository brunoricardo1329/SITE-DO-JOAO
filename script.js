// script.js

function submitForm() {
    var formData = {
        operator: document.getElementById('operator').value,
        machineType: document.getElementById('machineType').value,
        repairDate: document.getElementById('repairDate').value,
        repairTime: document.getElementById('repairTime').value,
        repairer: document.getElementById('repairer').value
    };

    fetch('submit_form.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);  // Mensagem de sucesso
            // Aqui você pode adicionar qualquer outra ação de sucesso desejada
        } else {
            alert('Erro: ' + data.error);  // Mensagem de erro
            // Aqui você pode adicionar qualquer outra ação de tratamento de erro desejada
        }
    })
    .catch((error) => {
        console.error('Erro:', error);
        alert('Erro ao processar a solicitação. Verifique o console para mais informações.');
        // Aqui você pode adicionar qualquer outra ação de tratamento de erro desejada
    });
}
