// Cité de la Miséricorde — espace d'administration (interactions légères)
document.addEventListener("DOMContentLoaded", function () {
  var body = document.body;

  // Sidebar réductible (desktop)
  var sidebarToggle = document.getElementById("sidebar-toggle");
  if (sidebarToggle) {
    var saved = null;
    try { saved = localStorage.getItem("adm-sidebar-collapsed"); } catch (e) {}
    if (saved === "1") body.classList.add("adm-collapsed");
    sidebarToggle.addEventListener("click", function () {
      var collapsed = body.classList.toggle("adm-collapsed");
      try { localStorage.setItem("adm-sidebar-collapsed", collapsed ? "1" : "0"); } catch (e) {}
    });
  }

  // Sidebar mobile
  var mobileToggle = document.getElementById("mobile-sidebar-toggle");
  if (mobileToggle) {
    mobileToggle.addEventListener("click", function () {
      body.classList.toggle("adm-mobile-open");
    });
  }

  // Groupes de la sidebar (dépliage des modules)
  document.querySelectorAll(".adm-group-btn").forEach(function (btn) {
    if (btn.classList.contains("adm-group-empty")) return;
    btn.addEventListener("click", function () {
      btn.parentElement.classList.toggle("open");
      btn.setAttribute("aria-expanded", btn.parentElement.classList.contains("open"));
    });
  });

  // Menu profil
  var profile = document.querySelector(".adm-profile");
  var profileBtn = document.querySelector(".adm-profile-btn");
  if (profile && profileBtn) {
    profileBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      profile.classList.toggle("open");
      profileBtn.setAttribute("aria-expanded", profile.classList.contains("open"));
    });
    document.addEventListener("click", function (e) {
      if (!profile.contains(e.target)) profile.classList.remove("open");
    });
  }

  // Fermeture des toasts
  document.querySelectorAll(".adm-toast-close").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var toast = btn.closest(".adm-toast");
      if (toast) toast.style.display = "none";
    });
  });
  // Auto-fermeture des toasts
  document.querySelectorAll(".adm-toast").forEach(function (toast) {
    setTimeout(function () { toast.style.opacity = "0"; toast.style.transition = "opacity .4s"; setTimeout(function () { toast.style.display = "none"; }, 450); }, 5000);
  });
});