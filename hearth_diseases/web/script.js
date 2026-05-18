const form = document.getElementById("predictionForm");

form.addEventListener("submit", async function (event) {
  event.preventDefault();

  const data = {
    age: Number(document.getElementById("age").value),
    sex: Number(document.getElementById("sex").value),
    cp: Number(document.getElementById("cp").value),
    trestbps: Number(document.getElementById("trestbps").value),
    chol: Number(document.getElementById("chol").value),
    fbs: Number(document.getElementById("fbs").value),
    restecg: Number(document.getElementById("restecg").value),
    thalach: Number(document.getElementById("thalach").value),
    exang: Number(document.getElementById("exang").value),
    oldpeak: Number(document.getElementById("oldpeak").value),
    slope: Number(document.getElementById("slope").value),
    ca: Number(document.getElementById("ca").value),
    thal: Number(document.getElementById("thal").value)
  };

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    const resultBox = document.getElementById("resultBox");
    const resultText = document.getElementById("resultText");
    const probabilityText = document.getElementById("probabilityText");
    const riskLevelText = document.getElementById("riskLevelText");

    if (result.status === "success") {
      resultBox.classList.remove("hidden");
      resultText.innerText = "Hasil: " + result.result;
      probabilityText.innerText = "Probabilitas Risiko: " + (result.probability * 100).toFixed(2) + "%";
      riskLevelText.innerText = "Tingkat Risiko: " + result.risk_level;
    } else {
      resultBox.classList.remove("hidden");
      resultText.innerText = "Terjadi kesalahan: " + result.message;
      probabilityText.innerText = "";
      riskLevelText.innerText = "";
    }

  } catch (error) {
    const resultBox = document.getElementById("resultBox");
    const resultText = document.getElementById("resultText");
    const probabilityText = document.getElementById("probabilityText");
    const riskLevelText = document.getElementById("riskLevelText");

    resultBox.classList.remove("hidden");
    resultText.innerText = "API belum berjalan atau tidak dapat diakses.";
    probabilityText.innerText = "";
    riskLevelText.innerText = "";
  }
});
