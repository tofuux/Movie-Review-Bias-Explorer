let data = [];
let chart;

// Load real data
async function loadRealData() {
  const res = await fetch('real_data.json');
  data = await res.json();
  updateUI();
}

// Simulate bias
function simulateBias() {
  data = data.map(d => {
    if (d.gender === 'female') {
      return { ...d, rating: d.rating - Math.random() * 0.5 };
    }
    return d;
  });
  updateUI();
}

// Update UI
function updateUI() {
  const female = data.filter(d => d.gender === 'female').map(d => d.rating);
  const male = data.filter(d => d.gender === 'male').map(d => d.rating);

  const mean = arr => arr.reduce((a,b)=>a+b,0)/arr.length;

  const fMean = mean(female);
  const mMean = mean(male);

  document.getElementById("stats").innerHTML =
    `Women Avg: ${fMean.toFixed(2)} | Men Avg: ${mMean.toFixed(2)}<br>
     Difference: ${(fMean - mMean).toFixed(2)}`;

  drawChart(fMean, mMean);
}

// Draw chart
function drawChart(f, m) {
  const ctx = document.getElementById('chart');

  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Women', 'Men'],
      datasets: [{
        label: 'Average Ratings',
        data: [f, m]
      }]
    }
  });
}

// Regression explanation
function runRegression() {
  document.getElementById("stats").innerHTML += `
  <br><br>
  📊 Regression Model:<br>
  rating ~ gender + year + votes<br>
  Controls for confounders → more accurate bias detection
  `;
}