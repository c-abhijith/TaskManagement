document.addEventListener("DOMContentLoaded", function () {
  const filter = document.getElementById("statusFilter");
  const notAssignedCheckbox = document.getElementById("notAssignedOnly");
  const cards = document.querySelectorAll(".task-card");

  function updateFilter() {
    const selectedStatus = filter.value.toLowerCase();
    const showNotAssigned = notAssignedCheckbox.checked;

    cards.forEach(card => {
      const status = card.getAttribute("data-status");
      const assigned = card.getAttribute("data-assigned");

      const matchesStatus = (selectedStatus === "all" || status === selectedStatus);
      const matchesAssigned = (!showNotAssigned || assigned === "none");

      card.style.display = (matchesStatus && matchesAssigned) ? "block" : "none";
    });
  }

  filter.addEventListener("change", updateFilter);
  notAssignedCheckbox.addEventListener("change", updateFilter);
});
