
let TOKEN = null;

// REGISTER
async function register() {
  const username = document.getElementById("reg-username").value;
  const password = document.getElementById("reg-password").value;

  const res = await fetch(`${API}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  document.getElementById("reg-msg").innerText =
    data.message || data.detail || "Greška";
}

// LOGIN
async function login() {
  const username = document.getElementById("log-username").value;
  const password = document.getElementById("log-password").value;

  const res = await fetch(`${API}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  TOKEN = data.token || null;
  document.getElementById("token").innerText = TOKEN || "nema";
}

// LOGOUT
function logout() {
  TOKEN = null;
  document.getElementById("token").innerText = "nema";
}

// UPLOAD CSV
async function uploadCSV() {
  const fileInput = document.getElementById("csv-file");
  if (!fileInput.files.length) return alert("Izaberi CSV fajl");

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const res = await fetch(`${API}/upload-csv`, {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  document.getElementById("result").innerText =
    JSON.stringify(data, null, 2);
}
const BACKEND = "http://127.0.0.1:8000";

document.getElementById("registerBtn").addEventListener("click", async () => {
  const username = document.getElementById("reg-username").value.trim();
  const password = document.getElementById("reg-password").value.trim();

  document.getElementById("reg-msg").innerText = "Šaljem...";

  const url = `${BACKEND}/register?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;

  const res = await fetch(url, { method: "POST" });
  const data = await res.json();

  document.getElementById("reg-msg").innerText = JSON.stringify(data);
});