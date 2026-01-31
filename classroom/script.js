const fileInput = document.querySelector(".upload-box input");
const scanBtn = document.querySelector(".scan-btn");

const originalImg = document.getElementById("originalImg");
const flippedImg = document.getElementById("flippedImg");
const uploadText = document.getElementById("uploadText");

let selectedFile = null;

/* show original image */
fileInput.addEventListener("change", () => {
  selectedFile = fileInput.files[0];

  if (selectedFile) {
    originalImg.src = URL.createObjectURL(selectedFile);
    originalImg.style.display = "block";

    // hide upload text permanently
    uploadText.style.display = "none";
  }
});

/* upload → flip → show flipped image */
scanBtn.addEventListener("click", () => {
  if (!selectedFile) {
    alert("Select a file first");
    return;
  }

  const formData = new FormData();
  formData.append("xray", selectedFile);

  fetch("http://127.0.0.1:5000/upload", {
    method: "POST",
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      const filename = data.file_path.split("/").pop();

      return fetch("http://127.0.0.1:5000/flip", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename })
      });
    })
    .then(res => res.json())
    .then(flipData => {
      flippedImg.src =
        "http://127.0.0.1:5000/uploads/" + flipData.flipped;
      flippedImg.style.display = "block";
    })
    .catch(err => {
      console.error(err);
      alert("Something went wrong");
    });
});


