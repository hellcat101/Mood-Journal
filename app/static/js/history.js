/**
 * History page: delete entries with confirmation.
 */
(function () {
  "use strict";

  document.querySelectorAll(".delete-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const id   = btn.dataset.id;
      const card = btn.closest(".entry-card");

      if (!confirm("Delete this entry?")) return;

      try {
        const res = await fetch(`/api/entries/${id}`, { method: "DELETE" });
        if (!res.ok) throw new Error("Failed");

        card.style.opacity   = "0";
        card.style.transform = "translateX(20px)";
        setTimeout(() => card.remove(), 300);
      } catch {
        alert("Could not delete entry. Please try again.");
      }
    });
  });
})();
