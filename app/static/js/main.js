/**
 * Shared utility functions for Moodly frontend.
 */

/**
 * Show a toast notification.
 * @param {string} message
 * @param {"success"|"error"} type
 */
function showToast(message, type = "success") {
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.textContent = message;
  toast.className = `toast ${type}`;
  setTimeout(() => { toast.className = "toast"; }, 3500);
}

/**
 * Format an ISO datetime string to a human-readable format.
 * @param {string} dateStr
 * @returns {string}
 */
function formatDate(dateStr) {
  const d = new Date(dateStr.replace(" ", "T") + "Z");
  return d.toLocaleString(undefined, {
    month: "short", day: "numeric",
    hour: "2-digit", minute: "2-digit",
  });
}
