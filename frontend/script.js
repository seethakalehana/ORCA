
const API = "http://127.0.0.1:8000";

const placeInput = document.getElementById("place");
const searchForm = document.getElementById("searchForm");
const locationBtn = document.getElementById("locationBtn");
const analyzeBtn = document.getElementById("analyzeBtn");

const latitudeDisplay = document.getElementById("latitude");
const longitudeDisplay = document.getElementById("longitude");
const selectedPlaceDisplay = document.getElementById("selectedPlace");

const statusText = document.getElementById("status");
const results = document.getElementById("results");

let selectedLocation = null;
let marker = null;


// Create interactive map
const map = L.map("map").setView([13.0827, 80.2707], 5);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap contributors"
}).addTo(map);


// Select location and update coordinates
function selectLocation(latitude, longitude, name = "Map selection") {
    selectedLocation = {
        latitude: Number(latitude),
        longitude: Number(longitude),
        name: name
    };

    latitudeDisplay.textContent = selectedLocation.latitude.toFixed(5);
    longitudeDisplay.textContent = selectedLocation.longitude.toFixed(5);
    selectedPlaceDisplay.textContent = name;

    if (marker) {
        map.removeLayer(marker);
    }

    marker = L.marker([latitude, longitude]).addTo(map);

    marker.bindPopup(
        `${name}<br>Latitude: ${latitude.toFixed(5)}<br>Longitude: ${longitude.toFixed(5)}`
    ).openPopup();

    analyzeBtn.disabled = false;
    statusText.textContent = "Location selected. You can now analyze marine conditions.";
    results.hidden = true;
}


// Search place name
searchForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    const place = placeInput.value.trim();

    if (!place) {
        statusText.textContent = "Please enter a place name.";
        return;
    }

    statusText.textContent = "Searching for location...";
    analyzeBtn.disabled = true;

    try {
        const response = await fetch(
            `${API}/geocode?place=${encodeURIComponent(place)}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Location not found.");
        }

        selectLocation(
            data.latitude,
            data.longitude,
            data.place
        );

        map.setView([data.latitude, data.longitude], 8);

    } catch (error) {
        statusText.textContent = error.message;
    }
});


// Select a location by clicking the map
map.on("click", function(event) {
    selectLocation(
        event.latlng.lat,
        event.latlng.lng,
        "Selected map location"
    );
});


// Use browser GPS
locationBtn.addEventListener("click", function() {
    if (!navigator.geolocation) {
        statusText.textContent = "Your browser does not support location detection.";
        return;
    }

    statusText.textContent = "Requesting your location permission...";

    navigator.geolocation.getCurrentPosition(
        function(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            selectLocation(latitude, longitude, "My Location");

            map.setView([latitude, longitude], 8);
        },

        function(error) {
            const messages = {
                1: "Location permission was denied.",
                2: "Your location could not be determined.",
                3: "Location request timed out."
            };

            statusText.textContent =
                messages[error.code] || "Unable to detect your location.";
        },

        {
            enableHighAccuracy: true,
            timeout: 10000
        }
    );
});


// Request marine report

// Request report based on selected intelligence mode
analyzeBtn.addEventListener("click", async function() {
    if (!selectedLocation) {
        statusText.textContent = "Please select a location first.";
        return;
    }

    const { latitude, longitude } = selectedLocation;

    const mode = document.querySelector(
    'input[name="analysisMode"]:checked'
)?.value || "marine";

    const endpoint = mode === "marine"
        ? "/marine-report"
        : "/inland-report";

    statusText.textContent = "Retrieving data. Please wait...";
    results.hidden = true;
    analyzeBtn.disabled = true;

    try {
        const response = await fetch(
            `${API}${endpoint}?latitude=${latitude}&longitude=${longitude}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Analysis failed.");
        }

        if (mode === "marine") {
            document.getElementById("conditions").textContent =
                JSON.stringify(data.ocean_conditions, null, 2);

            document.getElementById("risk").textContent =
                JSON.stringify(data.risk_assessment, null, 2);

            document.getElementById("explanation").textContent =
                typeof data.explanation === "string"
                    ? data.explanation
                    : JSON.stringify(data.explanation, null, 2);

            document.getElementById("source").textContent =
                `Data source: ${data.data_source || "Copernicus Marine"}`;

        } else {
            document.getElementById("conditions").textContent =
                JSON.stringify(data.weather_conditions, null, 2);

            document.getElementById("risk").textContent =
    JSON.stringify(data.risk_assessment, null, 2);

            document.getElementById("explanation").textContent =
               data.ai_explanation || "AI explanation is unavailable." 
            document.getElementById("source").textContent =
                `Data source: ${data.data_source || "Open-Meteo"}`;
        }

        results.hidden = false;
        statusText.textContent = `${mode === "marine" ? "Marine" : "Inland"} report retrieved successfully.`;

    } catch (error) {
        statusText.textContent = error.message;
    } finally {
        analyzeBtn.disabled = false;
    }
});
