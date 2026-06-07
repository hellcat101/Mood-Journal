/**
 * Log page: mood selection and form submission.
 */
(function () {
  "use strict";

  let selectedMood = null;

  const noteSection = document.getElementById("noteSection");
  const noteInput   = document.getElementById("noteInput");
  const charCount   = document.getElementById("charCount");
  const submitBtn   = document.getElementById("submitBtn");

  // Mood button selection
  document.querySelectorAll(".mood-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".mood-btn").forEach((b) => b.classList.remove("selected"));
      btn.classList.add("selected");
      selectedMood = btn.dataset.mood;
      noteSection.style.display = "block";
      noteInput.focus();
    });
  });

  // Character counter
  noteInput.addEventListener("input", () => {
    charCount.textContent = noteInput.value.length;
  });

  // Submit entry
  submitBtn.addEventListener("click", async () => {
    if (!selectedMood) return;

    submitBtn.disabled = true;
    submitBtn.textContent = "Saving…";

    try {
      const res = await fetch("/api/entries", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mood: selectedMood, note: noteInput.value }),
      });

      if (!res.ok) {
        const err = await res.json();
        showToast(err.error || "Something went wrong.", "error");
        return;
      }

      showToast("Mood logged! 🌱");
      noteInput.value = "";
      charCount.textContent = "0";
      document.querySelectorAll(".mood-btn").forEach((b) => b.classList.remove("selected"));
      noteSection.style.display = "none";
      selectedMood = null;
    } catch {
      showToast("Network error. Please try again.", "error");
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = 'Save entry <span class="submit-arrow">→</span>';
    }
  });
})();
