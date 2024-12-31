function toggleSubmitButton() {
  const termsCheckbox = document.getElementById("terms");
  const nextButton = document.getElementById("nextButton");
  nextButton.disabled = !termsCheckbox.checked;
}
//payment_form.html plan切換
function togglePlanView(selectedPlan) {
  const standardSection = document.getElementById("standard");
  const premiumSection = document.getElementById("premium");

  if (selectedPlan === "standard") {
    standardSection.classList.remove("hidden");
    premiumSection.classList.add("hidden");
  } else if (selectedPlan === "premium") {
    premiumSection.classList.remove("hidden");
    standardSection.classList.add("hidden");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const planSelect = document.getElementById("plan");
  togglePlanView(planSelect.value); // 初始化根據選擇的方案切換顯示
});
