export function init() {
  document.addEventListener("DOMContentLoaded", function () {
    const planSelect = document.getElementById("plan");
    const standardSection = document.getElementById("standard");
    const premiumSection = document.getElementById("premium");
    const termsSection = document.getElementById("terms-section");
    const termsCheckbox = document.getElementById("terms");
    const nextButton = document.getElementById("nextButton");

    // 切換方案顯示
    planSelect.addEventListener("change", function () {
      if (this.value === "standard") {
        standardSection.classList.remove("hidden");
        premiumSection.classList.add("hidden");
        termsSection.classList.add("hidden");
      } else if (this.value === "premium") {
        premiumSection.classList.remove("hidden");
        standardSection.classList.add("hidden");
        termsSection.classList.add("hidden");
      }
    });

    // 初始化顯示對應方案
    function initializePlanView() {
      const selectedPlan = planSelect.value;
      if (selectedPlan === "standard") {
        standardSection.classList.remove("hidden");
        premiumSection.classList.add("hidden");
      } else if (selectedPlan === "premium") {
        premiumSection.classList.remove("hidden");
        standardSection.classList.add("hidden");
      }
    }

    // 顯示購買須知
    window.showTerms = function () {
      termsSection.classList.remove("hidden");
      standardSection.classList.add("hidden");
      premiumSection.classList.add("hidden");
    };

    // 控制按鈕啟用狀態並顯示方案
    window.toggleSubmitButtonAndDisplayPlan = function () {
      nextButton.disabled = !termsCheckbox.checked;
      if (termsCheckbox.checked) {
        termsSection.classList.add("hidden"); // 隱藏購買須知
        const selectedPlan = planSelect.value;
        if (selectedPlan === "standard") {
          standardSection.classList.remove("hidden");
          premiumSection.classList.add("hidden");
        } else if (selectedPlan === "premium") {
          premiumSection.classList.remove("hidden");
          standardSection.classList.add("hidden");
        }
      }
    };

    initializePlanView();
  });
}
