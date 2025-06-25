document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("convert-form");
  const errorMsg = document.getElementById("error-msg");
  const fileInput = document.getElementById("files");
  const preview = document.getElementById("preview-container");

  // File preview listener
  fileInput.addEventListener("change", updatePreviews);

  function updatePreviews() {
    preview.innerHTML = "";
    Array.from(fileInput.files).forEach((file) => {
      const fileDiv = document.createElement("div");
      fileDiv.className = "preview-file";

      const name = document.createElement("p");
      name.textContent = file.name;
      fileDiv.appendChild(name);

      if (file.type.startsWith("audio/")) {
        const audio = document.createElement("audio");
        audio.controls = true;
        audio.src = URL.createObjectURL(file);
        audio.ontimeupdate = () => {
          if (audio.currentTime >= 30) {
            audio.pause();
            audio.currentTime = 0;
          }
        };
        fileDiv.appendChild(audio);
      } else {
        const warning = document.createElement("div");
        warning.className = "warning";
        warning.textContent = "⚠️ Not a recognized audio file.";
        fileDiv.appendChild(warning);
      }

      preview.appendChild(fileDiv);
    });
  }

  // Drag & drop support
  ["dragenter", "dragover"].forEach((event) => {
    window.addEventListener(event, (e) => {
      e.preventDefault();
      document.body.classList.add("dragover-page");
    });
  });

  ["dragleave", "drop"].forEach((event) => {
    window.addEventListener(event, (e) => {
      e.preventDefault();
      document.body.classList.remove("dragover-page");
    });
  });

  window.addEventListener("drop", (e) => {
    e.preventDefault();
    document.body.classList.remove("dragover-page");
    if (e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
      updatePreviews();
    }
  });
});

// 👇 This function is global and used by the form onsubmit handler
function validateAndShowSpinner() {
  const fileInput = document.getElementById("files");
  const errorMsg = document.getElementById("error-msg");

  if (!fileInput.files.length) {
    errorMsg.textContent = "Please upload at least one file.";
    errorMsg.style.display = "block";
    return false;
  }

  errorMsg.style.display = "none";
  showStatus("processing", "Processing..");
  return true; // allow form to submit
}

function showStatus(type, message) {
  const statusBox = document.getElementById("status-box");
  const statusText = document.getElementById("status-text");
  const statusIcon = document.getElementById("status-icon");

  statusBox.style.display = "flex";
  statusText.textContent = message;
  statusBox.classList.remove("status-success", "status-error", "status-processing");

  if (type === "processing") {
    statusBox.classList.add("status-processing");
    statusIcon.innerHTML = `
      <svg class="spinner-icon" viewBox="0 0 40 50">
        <circle cx="20" cy="25" r="15" stroke="#eee" stroke-width="5" fill="none"/>
        <circle cx="20" cy="25" r="15" stroke="#6a1b9a" stroke-width="5" fill="none" stroke-linecap="round"/>
      </svg>`;
  } else if (type === "success") {
    statusBox.classList.add("status-success");
    statusIcon.innerHTML = `
      <svg class="checkmark-icon" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20 6L9 17l-5-5"/>
      </svg>`;
  } else if (type === "error") {
    statusBox.classList.add("status-error");
    statusIcon.innerHTML = `
      <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="red" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>`;
  }
}
