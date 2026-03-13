document.getElementById('loanForm').addEventListener('submit', async function (e) { 
    e.preventDefault();

    const personalCode = document.getElementById('personalCode').value;
    const loanAmount = parseFloat(document.getElementById('loanAmount').value);
    const loanPeriod = parseInt(document.getElementById('loanPeriod').value);

    const resultContainer = document.getElementById('resultContainer');
    const decisionTitle = document.getElementById('decisionTitle');
    const decisionMessage = document.getElementById('decisionMessage');
    const offerDetails = document.getElementById('offerDetails');

    const payload = {
        personalCode: personalCode,
        loanAmount: loanAmount,
        loanPeriod: loanPeriod
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/api/decision', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        resultContainer.classList.remove('hidden');

        if (response.ok) {
            decisionMessage.textContent = 'data.message';

            if (data.approved){
                decisionTitle.textContent = 'Decosopm: Approved';
                decisionTitle.style.color = 'green';
                offerDetails.classList.remove('hidden');
                document.getElementById('resAmount').textContent = data.amount;
                document.getElementById('resPeriod').textContent = data.period;
            }
            else {
                decisionTitle.textContent = 'Decision: Rejected';
                decisionTitle.style.color = 'red';
                offerDetails.classList.add('hidden');
            }
        } else {
            decisionTitle.textContent = 'Error';
            decisionTitle.style.color = 'red';
            decisionMessage.textContent = data.detail || 'An error occurred while processing your request.';
            offerDetails.classList.add('hidden');
        } 
    }catch (error) {
            console.error('Error:', error);
            alert('Could not connect to the backend. Is the server running?');
    }
}); 
