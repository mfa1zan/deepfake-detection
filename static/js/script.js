var swiper = new Swiper(".slide-content", {
    slidesPerView: 3,
    spaceBetween: 30,
    centeredSlides: false,
    centerSlide: 'true',
    fade: 'true',
    grabCursor: 'true',
    slidesPerGroupSkip: 1,
    grabCursor: true,
    loop: true,
    keyboard: {
      enabled: true,
    },
    breakpoints: {
      769: {
        slidesPerView: 4,
        slidesPerGroup: 1,
      },
    },
    
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    pagination: {
      el: ".swiper-pagination",
      dynamicBullets: true,
      clickable: true,
    },
  });



 

  
  document.addEventListener("DOMContentLoaded", () => {
      const fileInput = document.getElementById("fileInput");
      const fileNameDisplay = document.getElementById("fileName");
      const removeFileBtn = document.getElementById("removeFileBtn");
      const previewArea = document.getElementById("previewArea");
      const uploadForm = document.getElementById("uploadForm");
      const detectBtn = document.getElementById("detectBtn");
      const progressContainer = document.getElementById("progressContainer");
      const progressBar = document.getElementById("progressBar");
      const progressText = document.getElementById("progressText");
      const resultArea = document.getElementById("resultArea");
      const resultText = document.getElementById("resultText");
  
      let uploadedFileName = null;  // Track uploaded file to send later
  
      // ---------- FILE CHOSEN ----------
      fileInput.addEventListener("change", () => {
          const file = fileInput.files[0];
          if (file) {
              fileNameDisplay.textContent = file.name;
              removeFileBtn.style.display = "inline-block";
              previewArea.innerHTML = "";
  
              if (file.type.startsWith("video")) {
                  const video = document.createElement("video");
                  video.src = URL.createObjectURL(file);
                  video.controls = true;
                  previewArea.appendChild(video);
              } else if (file.type.startsWith("image")) {
                  const img = document.createElement("img");
                  img.src = URL.createObjectURL(file);
                  previewArea.appendChild(img);
              }
          }
      });
  
      // ---------- REMOVE FILE ----------
      removeFileBtn.addEventListener("click", () => {
          fileInput.value = "";
          fileNameDisplay.textContent = "No file chosen";
          removeFileBtn.style.display = "none";
          previewArea.innerHTML = "<b><p>No file uploaded yet.</p></b>";
          detectBtn.disabled = true;
          uploadedFileName = null;
      });
  
      // ---------- HANDLE UPLOAD ----------
      uploadForm.addEventListener("submit", async (e) => {
          e.preventDefault();
  
          const file = fileInput.files[0];
          if (!file) {
              alert("Please select a file to upload.");
              return;
          }
  
          const formData = new FormData();
          formData.append("file", file);
  
          try {
              const response = await fetch("/upload", {
                  method: "POST",
                  body: formData,
              });
  
              const data = await response.json();
  
              if (data.success) {
                  uploadedFileName = data.filename; // 🔁 Get file name from server
                  detectBtn.disabled = false;
                  alert("Upload successful! Now click Detect.");
              } else {
                  alert("Upload failed.");
              }
          } catch (err) {
              console.error("Upload error:", err);
              alert("An error occurred while uploading.");
          }
      });
  
      // ---------- HANDLE DETECT ----------
      detectBtn.addEventListener("click", async () => {
          if (!uploadedFileName) {
              alert("No uploaded file available.");
              return;
          }
  
          progressContainer.style.display = "block";
          progressBar.style.width = "0%";
          progressText.textContent = "0%";
          resultArea.style.display = "none";
  
          try {
              const response = await fetch("/detect", {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json",
                  },
                  body: JSON.stringify({ filename: uploadedFileName }),
              });
  
              if (!response.ok) {
                  throw new Error("Detection failed.");
              }
  
              // Simulated real progress (if no streaming from backend)
              let progress = 0;
              const interval = setInterval(() => {
                  progress += Math.random() * 20;
                  if (progress >= 100) {
                      progress = 100;
                      clearInterval(interval);
                  }
                  progressBar.style.width = `${progress}%`;
                  progressText.textContent = `${Math.floor(progress)}%`;
              }, 300);
  
              const data = await response.json();
            resultArea.style.display = "block";
            let labelClass = "";
            if (data.label === "Real") labelClass = "result-label result-real";
            if (data.label === "Fake") labelClass = "result-label result-fake";
            resultText.innerHTML = `
                <span class="${labelClass}">${data.label}</span>
                <span class="result-confidence" style="#1e3e62">Confidence: ${(data.confidence * 100).toFixed(2)}%</span>
            `;
            console.log("aaaaaaa",resultText.innerHTML);
            console.log("aaaaaaa",resultText.innerHTML);
            
              // Wait until 100% visual before showing result
              setTimeout(() => {
                  progressBar.style.width = "100%";
                  progressText.textContent = "100%";
  
                
              }, 3000);     
  
          } catch (err) {
              console.error("Detection error:", err);
              alert("An error occurred during detection.");
          }
      });
  });
  
  