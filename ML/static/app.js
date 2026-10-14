/**
 * AgriFertilizer AI - Frontend Interactive Application
 * Precision Soil Analysis & Dynamic Fertilizer Recommendation
 * Authors: Sai Snehith & Harshith Reddy
 */

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const form = document.getElementById("predictionForm");
  const presetsContainer = document.getElementById("presetsContainer");
  const livePredictToggle = document.getElementById("livePredictToggle");
  const btnRandomize = document.getElementById("btnRandomize");
  const btnReset = document.getElementById("btnReset");
  const btnCopyReport = document.getElementById("btnCopyReport");
  const copyAlert = document.getElementById("copyAlert");
  const toggleExplain = document.getElementById("toggleExplain");
  const explainContent = document.getElementById("explainContent");

  // Output elements
  const resultHeroCard = document.getElementById("resultHeroCard");
  const statusBadge = document.getElementById("statusBadge");
  const gaugeMeter = document.getElementById("gaugeMeter");
  const gaugeProbability = document.getElementById("gaugeProbability");
  const decisionTitle = document.getElementById("decisionTitle");
  const decisionDescription = document.getElementById("decisionDescription");
  const probMarker = document.getElementById("probMarker");

  const prescribedFertilizer = document.getElementById("prescribedFertilizer");
  const prescribedFormula = document.getElementById("prescribedFormula");
  const applicationProtocol = document.getElementById("applicationProtocol");
  const fertHeroBox = document.getElementById("fertHeroBox");

  // Nutrient cards elements
  const dispNVal = document.getElementById("dispNVal");
  const dispNStatus = document.getElementById("dispNStatus");
  const barFillN = document.getElementById("barFillN");

  const dispPVal = document.getElementById("dispPVal");
  const dispPStatus = document.getElementById("dispPStatus");
  const barFillP = document.getElementById("barFillP");

  const dispKVal = document.getElementById("dispKVal");
  const dispKStatus = document.getElementById("dispKStatus");
  const barFillK = document.getElementById("barFillK");

  // pH strip
  const phBadge = document.getElementById("phBadge");
  const phStatusTitle = document.getElementById("phStatusTitle");
  const phStatusText = document.getElementById("phStatusText");

  // Sliders and inputs pairs
  const controls = [
    { range: "rangeN", num: "inputN", max: 150, bar: barFillN, class: "n-bar-fill" },
    { range: "rangeP", num: "inputP", max: 120, bar: barFillP, class: "p-bar-fill" },
    { range: "rangeK", num: "inputK", max: 120, bar: barFillK, class: "k-bar-fill" },
    { range: "rangePH", num: "inputPH", max: 14 },
    { range: "rangeMoisture", num: "inputMoisture", max: 100 },
    { range: "rangeTemp", num: "inputTemp", max: 50 },
    { range: "rangeHumidity", num: "inputHumidity", max: 100 },
    { range: "rangeRainfall", num: "inputRainfall", max: 400 }
  ];

  // Default Baseline Form Values
  const defaultValues = {
    Nitrogen: 28.0,
    Phosphorus: 18.0,
    Potassium: 38.0,
    pH: 6.50,
    Soil_Moisture: 45.0,
    Temperature: 28.0,
    Humidity: 62.0,
    Rainfall: 115.0,
    Soil_Type: "Loamy",
    Crop_Type: "Rice"
  };

  let debounceTimer = null;
  let lastPredictionData = null;

  // Setup Two-Way Binding for Sliders & Number Inputs
  controls.forEach(ctrl => {
    const rangeEl = document.getElementById(ctrl.range);
    const numEl = document.getElementById(ctrl.num);

    if (rangeEl && numEl) {
      rangeEl.addEventListener("input", (e) => {
        numEl.value = e.target.value;
        onFormModified();
      });

      numEl.addEventListener("input", (e) => {
        rangeEl.value = e.target.value;
        onFormModified();
      });
    }
  });

  // Select dropdown changes
  document.getElementById("cropSelect").addEventListener("change", onFormModified);
  document.getElementById("soilSelect").addEventListener("change", onFormModified);

  function onFormModified() {
    if (livePredictToggle && livePredictToggle.checked) {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        triggerPrediction();
      }, 150);
    }
  }

  // Fetch and Load Presets
  async function loadPresets() {
    try {
      const response = await fetch("/api/presets");
      if (!response.ok) throw new Error("Failed to load presets");
      const presets = await response.json();

      presetsContainer.innerHTML = "";
      presets.forEach((preset, index) => {
        const chip = document.createElement("button");
        chip.type = "button";
        chip.className = "preset-chip";
        chip.id = `preset-${preset.id}`;
        chip.innerHTML = `
          <span>${preset.title}</span>
          <span class="preset-pill-tag">${preset.expected_fertilizer}</span>
        `;
        chip.addEventListener("click", () => {
          applyPreset(preset);
          document.querySelectorAll(".preset-chip").forEach(c => c.classList.remove("active"));
          chip.classList.add("active");
        });
        presetsContainer.appendChild(chip);
      });
    } catch (err) {
      console.error("Presets error:", err);
      presetsContainer.innerHTML = `<span style="font-size:12px;color:#f87171;">Presets temporarily unavailable</span>`;
    }
  }

  // Apply a Preset to Form
  function applyPreset(preset) {
    const d = preset.data;
    setFieldValues(d);
    triggerPrediction();
  }

  function setFieldValues(d) {
    document.getElementById("inputN").value = d.Nitrogen;
    document.getElementById("rangeN").value = d.Nitrogen;

    document.getElementById("inputP").value = d.Phosphorus;
    document.getElementById("rangeP").value = d.Phosphorus;

    document.getElementById("inputK").value = d.Potassium;
    document.getElementById("rangeK").value = d.Potassium;

    document.getElementById("inputPH").value = d.pH;
    document.getElementById("rangePH").value = d.pH;

    document.getElementById("inputMoisture").value = d.Soil_Moisture;
    document.getElementById("rangeMoisture").value = d.Soil_Moisture;

    document.getElementById("inputTemp").value = d.Temperature;
    document.getElementById("rangeTemp").value = d.Temperature;

    document.getElementById("inputHumidity").value = d.Humidity;
    document.getElementById("rangeHumidity").value = d.Humidity;

    document.getElementById("inputRainfall").value = d.Rainfall;
    document.getElementById("rangeRainfall").value = d.Rainfall;

    if (d.Soil_Type) document.getElementById("soilSelect").value = d.Soil_Type;
    if (d.Crop_Type) document.getElementById("cropSelect").value = d.Crop_Type;
  }

  // Randomize realistic soil parameters
  btnRandomize.addEventListener("click", () => {
    const crops = ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane", "Pulses", "Barley", "Soybean", "Groundnut", "Mustard"];
    const soils = ["Black", "Clayey", "Red", "Loamy", "Laterite", "Sandy"];

    const randCrop = crops[Math.floor(Math.random() * crops.length)];
    const randSoil = soils[Math.floor(Math.random() * soils.length)];

    const randomData = {
      Nitrogen: +(Math.random() * 85 + 10).toFixed(1),
      Phosphorus: +(Math.random() * 70 + 8).toFixed(1),
      Potassium: +(Math.random() * 75 + 10).toFixed(1),
      pH: +(Math.random() * 3.5 + 5.0).toFixed(2),
      Soil_Moisture: +(Math.random() * 65 + 20).toFixed(1),
      Temperature: +(Math.random() * 20 + 18).toFixed(1),
      Humidity: +(Math.random() * 50 + 40).toFixed(1),
      Rainfall: +(Math.random() * 180 + 50).toFixed(1),
      Soil_Type: randSoil,
      Crop_Type: randCrop
    };

    document.querySelectorAll(".preset-chip").forEach(c => c.classList.remove("active"));
    setFieldValues(randomData);
    triggerPrediction();
  });

  // Reset to default baseline
  btnReset.addEventListener("click", () => {
    document.querySelectorAll(".preset-chip").forEach(c => c.classList.remove("active"));
    setFieldValues(defaultValues);
    triggerPrediction();
  });

  // Submit Handler
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    triggerPrediction();
  });

  // Trigger Prediction Request
  async function triggerPrediction() {
    const payload = {
      Nitrogen: parseFloat(document.getElementById("inputN").value),
      Phosphorus: parseFloat(document.getElementById("inputP").value),
      Potassium: parseFloat(document.getElementById("inputK").value),
      pH: parseFloat(document.getElementById("inputPH").value),
      Soil_Moisture: parseFloat(document.getElementById("inputMoisture").value),
      Temperature: parseFloat(document.getElementById("inputTemp").value),
      Humidity: parseFloat(document.getElementById("inputHumidity").value),
      Rainfall: parseFloat(document.getElementById("inputRainfall").value),
      Soil_Type: document.getElementById("soilSelect").value,
      Crop_Type: document.getElementById("cropSelect").value
    };

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Prediction request failed");
      }

      const data = await response.json();
      lastPredictionData = data;
      renderResults(data);
    } catch (err) {
      console.error("Prediction error:", err);
      statusBadge.textContent = "Error";
      decisionTitle.textContent = "Inference Failure";
      decisionDescription.textContent = err.message;
    }
  }

  // Render Visual Results
  function renderResults(data) {
    const prob = data.probability;
    const probPercent = data.probability_percentage;
    const req = data.fertilizer_required;
    const threshold = data.threshold_percentage;

    // 1. Radial Gauge Animation
    // Circumference = 2 * PI * 68 ≈ 427.26
    const circumference = 427.26;
    const offset = circumference - (circumference * prob);
    gaugeMeter.style.strokeDashoffset = offset;
    gaugeProbability.textContent = `${probPercent}%`;

    // Marker position on reference line
    probMarker.style.left = `${Math.min(100, Math.max(0, probPercent))}%`;

    // 2. Verdict Badge & Colors
    if (req) {
      statusBadge.textContent = "Fertilizer Required";
      statusBadge.className = "status-indicator-badge badge-required";
      gaugeMeter.style.stroke = prob > 0.75 ? "var(--rose-danger)" : "var(--amber-warning)";
      resultHeroCard.style.borderColor = prob > 0.75 ? "rgba(244, 63, 94, 0.4)" : "rgba(245, 158, 11, 0.4)";
      probMarker.style.borderColor = prob > 0.75 ? "var(--rose-danger)" : "var(--amber-warning)";

      decisionTitle.innerHTML = `<span style="color:${prob > 0.75 ? '#fb7185' : '#fbbf24'};">⚠️ Soil Nutrient Depletion Detected</span>`;
      decisionDescription.textContent = `Probability of nutrient deficit is ${probPercent}%, which exceeds the optimal classification boundary (${threshold}%). Targeted fertilizer intervention is required to prevent yield loss.`;
    } else {
      statusBadge.textContent = "Nutrients Adequate";
      statusBadge.className = "status-indicator-badge badge-optimal";
      gaugeMeter.style.stroke = "var(--emerald-primary)";
      resultHeroCard.style.borderColor = "rgba(16, 185, 129, 0.35)";
      probMarker.style.borderColor = "var(--emerald-primary)";

      decisionTitle.innerHTML = `<span style="color:#6ee7b7;">✅ Optimal Soil Fertility Status</span>`;
      decisionDescription.textContent = `Calculated requirement probability is ${probPercent}%, remaining safely below the critical intervention threshold of ${threshold}%. Existing mineral reserves are sufficient for target growth.`;
    }

    // 3. Prescribed Fertilizer
    const p = data.prescription;
    prescribedFertilizer.textContent = p.fertilizer;
    prescribedFormula.textContent = p.formula;
    applicationProtocol.textContent = p.application;

    if (req) {
      fertHeroBox.style.background = "rgba(245, 158, 11, 0.08)";
      fertHeroBox.style.borderColor = "rgba(245, 158, 11, 0.4)";
      prescribedFertilizer.style.color = "#fbbf24";
    } else {
      fertHeroBox.style.background = "rgba(16, 185, 129, 0.08)";
      fertHeroBox.style.borderColor = "rgba(16, 185, 129, 0.4)";
      prescribedFertilizer.style.color = "#6ee7b7";
    }

    // 4. Macro-Nutrient Diagnostics (N - P - K)
    const n = data.nutrient_analysis.nitrogen;
    dispNVal.textContent = `${n.value} kg/ha`;
    dispNStatus.textContent = n.status;
    dispNStatus.className = `nutri-status ${getStatusClass(n.status)}`;
    barFillN.style.width = `${Math.min(100, (n.value / 120) * 100)}%`;
    barFillN.className = "nutri-bar-fill n-bar-fill";

    const pNutri = data.nutrient_analysis.phosphorus;
    dispPVal.textContent = `${pNutri.value} kg/ha`;
    dispPStatus.textContent = pNutri.status;
    dispPStatus.className = `nutri-status ${getStatusClass(pNutri.status)}`;
    barFillP.style.width = `${Math.min(100, (pNutri.value / 80) * 100)}%`;
    barFillP.className = "nutri-bar-fill p-bar-fill";

    const kNutri = data.nutrient_analysis.potassium;
    dispKVal.textContent = `${kNutri.value} kg/ha`;
    dispKStatus.textContent = kNutri.status;
    dispKStatus.className = `nutri-status ${getStatusClass(kNutri.status)}`;
    barFillK.style.width = `${Math.min(100, (kNutri.value / 90) * 100)}%`;
    barFillK.className = "nutri-bar-fill k-bar-fill";

    // 5. pH Advisory Strip
    const ph = data.nutrient_analysis.ph;
    phBadge.textContent = `pH ${ph.value.toFixed(2)}`;
    phStatusTitle.textContent = ph.status;
    phStatusText.textContent = ph.advice;
  }

  function getStatusClass(status) {
    if (status.includes("Deficient")) return "status-def";
    if (status.includes("Low")) return "status-low";
    if (status.includes("Optimal")) return "status-opt";
    return "status-high";
  }

  // Accordion Toggle for Explainability
  toggleExplain.addEventListener("click", () => {
    const isHidden = explainContent.style.display === "none";
    explainContent.style.display = isHidden ? "flex" : "none";
    document.querySelector(".accordion-arrow").classList.toggle("rotated", isHidden);
  });

  // Copy Advisory Summary Report
  btnCopyReport.addEventListener("click", () => {
    if (!lastPredictionData) return;
    const d = lastPredictionData;
    const inp = d.input_summary;
    const report = `=====================================================
🌾 AGRIFERTILIZER AI - PRECISION ADVISORY REPORT
=====================================================
Target Crop:        ${inp.Crop_Type}
Soil Type:          ${inp.Soil_Type}
Evaluation Verdict: ${d.fertilizer_required ? "FERTILIZER REQUIRED" : "NUTRIENTS ADEQUATE"}
Confidence Score:   ${d.probability_percentage}% (Optimal Threshold: ${d.threshold_percentage}%)
Risk Urgency:       ${d.urgency}

--- NUTRIENT PROFILE ---
• Nitrogen (N):    ${inp.Nitrogen} kg/ha (${d.nutrient_analysis.nitrogen.status})
• Phosphorus (P):  ${inp.Phosphorus} kg/ha (${d.nutrient_analysis.phosphorus.status})
• Potassium (K):   ${inp.Potassium} kg/ha (${d.nutrient_analysis.potassium.status})
• Soil pH:         ${inp.pH} (${d.nutrient_analysis.ph.status})
• Soil Moisture:   ${inp.Soil_Moisture}%

--- PRESCRIBED ACTION ---
• Recommended:     ${d.prescription.fertilizer}
• Composition:     ${d.prescription.formula}
• Protocol:        ${d.prescription.application}

Generated by AgriFertilizer AI
Authors: Sai Snehith & Harshith Reddy (CSIT)
=====================================================`;

    navigator.clipboard.writeText(report).then(() => {
      copyAlert.classList.add("show");
      setTimeout(() => copyAlert.classList.remove("show"), 2500);
    });
  });

  // Initial Load
  loadPresets();
  triggerPrediction();
});
