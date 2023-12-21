const browserCanvas = document.getElementById("browserChart").getContext("2d");
const browserData = document.querySelectorAll('#browserChart input[type="hidden"]');

const osCanvas = document.getElementById("osChart").getContext("2d");
const osData = document.querySelectorAll('#osChart input[type="hidden"]');

const countryCanvas = document.getElementById("countryChart").getContext("2d");
const countryData = document.querySelectorAll('#countryChart input[type="hidden"]');

const cityCanvas = document.getElementById("cityChart").getContext("2d");
const cityData = document.querySelectorAll('#cityChart input[type="hidden"]');

[
  [browserCanvas, browserData],
  [osCanvas, osData],
  [countryCanvas, countryData],
  [cityCanvas, cityData],
].forEach(elem => {
  let labels = [];
  let data = [];

  elem[1].forEach(input => {
    labels.push(input.getAttribute("data-key"));
    data.push(input.getAttribute("data-value"));
  });

  new Chart(elem[0], {
    type: "pie",
    data: {
      labels: labels,
      datasets: [{
        data: data,
        borderWidth: 1
      }]
    },
    options: {
      plugins: {
        legend: {
          display: false
        },
      },
      responsive: true,
    }
  });
});