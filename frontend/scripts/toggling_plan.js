export function init() {
  document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("toggle-premium-plan-btn");
    const premiumContainer = document.getElementById("premium-plan-container");
  
    // Update button text based on the initial state
    if (!premiumContainer.classList.contains("hidden")) {
      toggleBtn.textContent = "收回專業方案";
    }
  
    toggleBtn.addEventListener("click", function () {
      if (premiumContainer.classList.contains("hidden")) {
        premiumContainer.classList.remove("hidden");
        toggleBtn.textContent = "收回專業方案";
      } else {
        premiumContainer.classList.add("hidden");
        toggleBtn.textContent = "新增專業方案";
  
        // Clear premium plan fields
        const premiumFields = premiumContainer.querySelectorAll("input, textarea");
        premiumFields.forEach((field) => {
          field.value = "";
        });
      }
    });
  })
}
