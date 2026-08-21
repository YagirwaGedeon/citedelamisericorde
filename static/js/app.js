// Cité de la Miséricorde — interactions légères (refonte 2026)
document.addEventListener("DOMContentLoaded", function () {
  var body = document.body;

  // Enregistrement du service worker PWA (https ou localhost uniquement)
  if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost" || location.hostname === "127.0.0.1")) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("/sw.js").catch(function () {});
    });
  }

  // Ombre du header au scroll
  var header = document.getElementById("site-header");
  function headerShadow() {
    if (header) header.classList.toggle("shadow-soft", window.scrollY > 8);
  }
  headerShadow();
  window.addEventListener("scroll", headerShadow, { passive: true });

  // --- Menu mobile (overlay plein écran) ---
  var overlay = document.getElementById("mobile-menu");
  var toggle = document.getElementById("menu-toggle");
  if (overlay && toggle) {
    function setMenu(open) {
      overlay.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      overlay.setAttribute("aria-hidden", open ? "false" : "true");
      body.classList.toggle("overflow-hidden", open);
    }
    toggle.addEventListener("click", function () {
      setMenu(!overlay.classList.contains("is-open"));
    });
    overlay.querySelectorAll("[data-close-mobile]").forEach(function (el) {
      el.addEventListener("click", function () { setMenu(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setMenu(false);
    });
  }

  // --- Accordéons du menu mobile ---
  var accButtons = document.querySelectorAll("[data-acc]");
  accButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var sub = btn.nextElementSibling;
      if (!sub) return;
      var willOpen = sub.classList.contains("hidden");
      accButtons.forEach(function (other) {
        var otherSub = other.nextElementSibling;
        if (otherSub && otherSub !== sub) {
          otherSub.classList.add("hidden");
          other.setAttribute("aria-expanded", "false");
          other.classList.remove("is-open");
        }
      });
      sub.classList.toggle("hidden", !willOpen);
      btn.classList.toggle("is-open", willOpen);
      btn.setAttribute("aria-expanded", willOpen ? "true" : "false");
    });
  });

  // --- Dropdowns desktop (hover + clic) ---
  var navTriggers = document.querySelectorAll("[data-nav-trigger]");
  navTriggers.forEach(function (trigger) {
    var li = trigger.closest("li");
    var dropdown = li ? li.querySelector("[data-nav-dropdown]") : null;
    if (!dropdown) return;
    function open() {
      dropdown.classList.add("is-open");
      trigger.setAttribute("aria-expanded", "true");
    }
    function close() {
      dropdown.classList.remove("is-open");
      trigger.setAttribute("aria-expanded", "false");
    }
    li.addEventListener("mouseenter", open);
    li.addEventListener("mouseleave", close);
    trigger.addEventListener("click", function (e) {
      e.stopPropagation();
      if (dropdown.classList.contains("is-open")) close(); else open();
    });
  });
  document.addEventListener("click", function (e) {
    document.querySelectorAll("[data-nav-dropdown].is-open").forEach(function (d) {
      var li = d.closest("li");
      if (li && !li.contains(e.target)) {
        d.classList.remove("is-open");
        var t = li.querySelector("[data-nav-trigger]");
        if (t) t.setAttribute("aria-expanded", "false");
      }
    });
  });

  // --- Animations au défilement (.reveal) ---
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    reveals.forEach(function (el) { observer.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  // --- Bouton retour en haut ---
  var backToTop = document.getElementById("back-to-top");
  if (backToTop) {
    function backTopState() { backToTop.classList.toggle("hidden", window.scrollY < 400); }
    backTopState();
    window.addEventListener("scroll", backTopState, { passive: true });
    backToTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
  }

  // --- Fermeture des toasts Django messages ---
  document.querySelectorAll(".toast-close").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var toast = btn.closest("[data-toast]");
      if (toast) toast.style.display = "none";
    });
  });
  document.querySelectorAll("[data-toast]").forEach(function (toast) {
    setTimeout(function () {
      toast.style.transition = "opacity .5s, transform .5s";
      toast.style.opacity = "0";
      toast.style.transform = "translateY(-8px)";
      setTimeout(function () { toast.style.display = "none"; }, 550);
    }, 6000);
  });

  // --- Presets de montant (donation) ---
  var presetButtons = document.querySelectorAll(".preset-btn");
  var amountInput = document.getElementById("id_amount");
  if (presetButtons.length && amountInput) {
    presetButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        amountInput.value = btn.dataset.amount;
        presetButtons.forEach(function (b) {
          b.classList.remove("bg-teal-700", "text-white", "border-teal-700");
        });
        btn.classList.add("bg-teal-700", "text-white", "border-teal-700");
      });
    });
  }
});