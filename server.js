function addMessage(text, sender = "bot", isLink = false) {
  const chatBox = document.getElementById("chat-box");
  const msg = document.createElement("div");
  msg.className = sender === "bot" ? "bot-msg" : "user-msg";

  if (isLink) {
    const link = document.createElement("a");
    link.href = text;
    link.textContent = "🗺️ Open Best Route (Click Here)";
    link.target = "_blank";
    link.style.color = "#e67e22";
    link.style.fontWeight = "bold";
    msg.appendChild(link);
  } else {
    msg.textContent = text;
  }

  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function showInfo(type) {
  let response = "";
  let isLink = false;

  switch (type) {
    case "bathing":
      response = "🚿 Bathing Dates: 5th, 12th, 18th & 26th May 2028.";
      break;
    case "bhasma":
      response = "🪔 Bhasma Aarti: Daily 4:00 AM at Mahakaleshwar Temple.";
      break;
    case "dress":
      response = "👕 Dress Code: Traditional attire recommended, white preferred.";
      break;
    case "navigate":
      getUserLocation();
      return; // we will handle navigation separately
  }
  addMessage(response, "bot", isLink);
}

function getUserLocation() {
  if (!navigator.geolocation) {
    addMessage("❌ Geolocation is not supported by your browser.");
    return;
  }

  addMessage("📍 Getting your location...");
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;
      // Google Maps route from user's location to Ram Ghat
      const mapsURL = `https://www.google.com/maps/dir/?api=1&origin=${lat},${lon}&destination=Ram+Ghat+Ujjain&travelmode=driving`;
      addMessage(mapsURL, "bot", true);
    },
    (error) => {
      addMessage("⚠️ Unable to get location. Please enable GPS.");
    }
  );
}

function sendMessage() {
  const input = document.getElementById("user-input");
  if (input.value.trim() === "") return;
  addMessage(input.value, "user");
  addMessage("🙏 I will try to get more info about: " + input.value);
  input.value = "";
}
