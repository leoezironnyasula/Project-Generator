// Frontend logic for the Project Generator UI.
// Talks directly to the FastAPI backend on localhost:8000.

const API_BASE = "http://127.0.0.1:8000";

const generateBtn = document.getElementById("generate-btn");
const scaffoldBtn = document.getElementById("scaffold-btn");
const idleEl = document.getElementById("idle");
const resultEl = document.getElementById("result");
const errorEl = document.getElementById("error");
const statusEl = document.getElementById("status");

async function generateProject() {
  generateBtn.disabled = true;
  errorEl.classList.add("hidden");
  statusEl.textContent = "";

  try {
    const response = await fetch(`${API_BASE}/generate`);

    if (!response.ok) {
      const data = await response.json();
      showError(data.detail || "Something went wrong.");
      return;
    }

    const project = await response.json();
    showProject(project);
  } catch (err) {
    // Network-level failure -- almost always means the backend isn't running.
    showError("Could not reach the backend. Is the FastAPI server running?");
  } finally {
    generateBtn.disabled = false;
  }
}

async function scaffoldProject() {
  scaffoldBtn.disabled = true;
  statusEl.textContent = "Creating folder...";

  try {
    const response = await fetch(`${API_BASE}/scaffold`, { method: "POST" });

    if (!response.ok) {
      const data = await response.json();
      statusEl.textContent = `> error: ${data.detail}`;
      return;
    }

    const data = await response.json();
    statusEl.textContent = `> created at ${data.created_at}`;
    statusEl.classList.add("key"); // reuse the teal "key" color for success text
  } catch (err) {
    statusEl.textContent = "> could not reach the backend";
  } finally {
    scaffoldBtn.disabled = false;
  }
}

function showProject(project) {
  idleEl.classList.add("hidden");
  errorEl.classList.add("hidden");

  document.getElementById("title").textContent = project.title;
  document.getElementById("description").textContent = project.description;
  document.getElementById("domain").textContent = project.domain;
  document.getElementById("difficulty").textContent = project.difficulty;
  document.getElementById("stack").textContent = project.tech_stack;

  const list = document.getElementById("features");
  list.innerHTML = "";
  project.features.forEach((f) => {
    const li = document.createElement("li");
    li.textContent = f;
    list.appendChild(li);
  });

  resultEl.classList.remove("hidden");
  scaffoldBtn.classList.remove("hidden");
}

function showError(message) {
  idleEl.classList.add("hidden");
  resultEl.classList.add("hidden");
  scaffoldBtn.classList.add("hidden");

  errorEl.textContent = `> error: ${message}`;
  errorEl.classList.remove("hidden");
}

generateBtn.addEventListener("click", generateProject);