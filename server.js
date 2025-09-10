import express from "express";
import cors from "cors";
const app = express();
app.use(cors());
app.use(express.json());

let sosRequests = [];

app.post("/sos", (req, res) => {
  sosRequests.push(req.body);
  console.log("SOS Received:", req.body);
  res.json({ msg: "SOS received" });
});

app.get("/alerts", (req, res) => {
  res.json(sosRequests);
});

app.listen(5000, () => console.log("🚀 Server running on http://localhost:5000"));
