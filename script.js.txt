document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('coaches-container');

    // Fetch the data from our JSON file
    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                container.innerHTML = "<p>No team data found.</p>";
                return;
            }

            // Loop through each team's data
            data.forEach(team => {
                // Create a 'card' element for each team
                const card = document.createElement('div');
                card.className = 'coach-card';

                // Populate the card with the team's info
                card.innerHTML = `
                    <h2>${team.teamName}</h2>
                    <p><strong>Record:</strong> ${team.record}</p>
                    <a href="${team.sourceUrl}" target="_blank">View on MaxPreps</a>
                `;

                // Add the new card to the container
                container.appendChild(card);
            });
        })
        .catch(error => {
            console.error('Error fetching or parsing data:', error);
            container.innerHTML = "<p>Could not load team data.</p>";
        });
});