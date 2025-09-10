// server.js
const express = require("express");
const app = express();
const port = 3000;

function randomNearby(base, variance = 0.01) {
  return base + (Math.random() - 0.5) * variance;
}

app.get("/crowd", (req, res) => {
  const baseLat = 25.4358; // Mahakumbh Mela (Prayagraj)
  const baseLng = 81.8463;

  const points = Array.from({ length: 10 }, () => ({
    lat: randomNearby(baseLat, 0.05),  // random nearby latitude
    lng: randomNearby(baseLng, 0.05),  // random nearby longitude
    weight: Math.floor(Math.random() * 5) + 1
  }));

  res.json(points);
});

app.use(express.static("public")); // serve frontend

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
