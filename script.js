/**
 * Ngarmodeng Freeman - Portfolio Scripts
 * Static Version compatible with InfinityFree / Static Hosting
 */

window.PORTFOLIO = {
  email: "freemanng139@gmail.com",
  github: "https://github.com/freemanng139",
  linkedin: "https://www.linkedin.com/in/freemanng139/",
  roles: [
    "Licence Pro ICT4D · Sécurité Informatique",
    "BTS Réseaux & Sécurité",
    "Administration Système & Réseau",
    "Sécurité des Infrastructures"
  ],
  urls: { lab: "#", home: "#home" }
};

if (history.scrollRestoration) {
  history.scrollRestoration = "manual";
}
if (!location.hash || location.hash === "#home" || location.hash === "#") {
  window.scrollTo(0, 0);
}
window.addEventListener("load", () => {
  if (!location.hash || location.hash === "#home" || location.hash === "#") {
    window.scrollTo(0, 0);
  }
});

const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const P = window.PORTFOLIO;

function toast(msg) {
  const t = $("#toast");
  if (!t) return;
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(toast._t);
  toast._t = setTimeout(() => t.classList.remove("show"), 2800);
}
window.toast = toast;

const menuBtn = $("#menu-toggle"), navbar = $("#navbar");
if (menuBtn && navbar) {
  menuBtn.addEventListener("click", () => {
    const open = navbar.classList.toggle("open");
    menuBtn.setAttribute("aria-expanded", open);
  });
  $$(".navbar a, .btn-header-contact").forEach(a => a.addEventListener("click", () => {
    navbar.classList.remove("open");
    menuBtn.setAttribute("aria-expanded", "false");
  }));
  document.addEventListener("click", e => {
    if (navbar.classList.contains("open") && !navbar.contains(e.target) && !menuBtn.contains(e.target)) {
      navbar.classList.remove("open");
      menuBtn.setAttribute("aria-expanded", "false");
    }
  });
}

const header = $("#header"), progress = $("#scroll-progress");
function onScroll() {
  const y = scrollY, h = document.documentElement.scrollHeight - innerHeight;
  if (header) header.classList.toggle("scrolled", y > 20);
  if (progress) progress.style.width = (h > 0 ? (y / h) * 100 : 0) + "%";
}
addEventListener("scroll", onScroll, { passive: true }); onScroll();

function fillBars(scope = document) {
  $$(".meter-bar span", scope).forEach(b => { b.style.width = (b.dataset.width || 0) + "%"; });
}

const reveals = $$(".reveal");
if ("IntersectionObserver" in window) {
  const revealIo = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add("visible");
        revealIo.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  reveals.forEach(el => revealIo.observe(el));

  const skillsSec = $("#skills");
  if (skillsSec) {
    const skillsIo = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          fillBars(skillsSec);
          skillsIo.unobserve(e.target);
        }
      });
    }, { threshold: 0.2 });
    skillsIo.observe(skillsSec);
  }
} else {
  reveals.forEach(el => el.classList.add("visible"));
  fillBars();
}

const typing = $("#typing");
if (typing) {
  let r = 0, i = 0, del = false;
  (function tick() {
    const word = P.roles[r];
    typing.textContent = word.slice(0, i);
    if (!del && i === word.length) { del = true; return setTimeout(tick, 1600); }
    if (del && i === 0) { del = false; r = (r + 1) % P.roles.length; }
    i += del ? -1 : 1;
    setTimeout(tick, del ? 40 : 80);
  })();
}

const tilt = $("#tilt");
if (tilt && matchMedia("(hover: hover)").matches) {
  tilt.addEventListener("mousemove", e => {
    const r = tilt.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
    tilt.style.transform = `perspective(900px) rotateY(${x * 14}deg) rotateX(${-y * 14}deg)`;
  });
  tilt.addEventListener("mouseleave", () => tilt.style.transform = "");
}

$$(".tab").forEach(tab => tab.addEventListener("click", () => {
  $$(".tab").forEach(t => t.classList.toggle("active", t === tab));
  $$(".tab-panel").forEach(p => {
    const on = p.id === tab.dataset.tab;
    p.classList.toggle("active", on);
    if (on) { $$(".meter-bar span", p).forEach(b => b.style.width = 0); requestAnimationFrame(() => setTimeout(() => fillBars(p), 30)); }
  });
}));

$$(".filter").forEach(btn => btn.addEventListener("click", () => {
  $$(".filter").forEach(b => b.classList.toggle("active", b === btn));
  $$(".project-card").forEach(c => c.classList.toggle("hide", btn.dataset.filter !== "all" && c.dataset.category !== btn.dataset.filter));
}));
$$(".project-card").forEach(c => c.addEventListener("mousemove", e => {
  const r = c.getBoundingClientRect();
  c.style.setProperty("--mx", e.clientX - r.left + "px");
  c.style.setProperty("--my", e.clientY - r.top + "px");
}));

async function copy(text, msg) {
  try { await navigator.clipboard.writeText(text); toast(msg); }
  catch { toast(text); }
}
$$("[data-copy-email]").forEach(b => b.addEventListener("click", () => copy(P.email, "📋 E-mail copié : " + P.email)));
$$("[data-copy-target]").forEach(b => b.addEventListener("click", () => copy($("#" + b.dataset.copyTarget).textContent, "📋 Copié !")));

const form = $("#contact-form");
if (form) {
  const msg = $("#cf-message"), count = $("#cf-count");
  if (msg && count) {
    msg.addEventListener("input", () => count.textContent = `${msg.value.length} / 2000`);
  }
  form.addEventListener("submit", async e => {
    e.preventDefault();
    $$(".field", form).forEach(f => { f.classList.remove("invalid"); const s = $("small", f); if (s) s.textContent = ""; });
    const btn = $("button[type=submit]", form), label = btn ? $(".btn-label", btn) : null;
    if (btn) btn.disabled = true;
    if (label) label.textContent = "Envoi en cours…";
    
    // In static mode without a server backend, direct email via mailto is supported
    toast("ℹ️ Site statique : Veuillez utiliser le lien e-mail direct ou WhatsApp.");
    window.location.href = `mailto:${P.email}?subject=Contact&body=${encodeURIComponent(msg ? msg.value : "")}`;
    
    if (btn) btn.disabled = false;
    if (label) label.textContent = "Envoyer le message";
  });
}

const contactModal = $("#contact-modal");
const openModalBtns = $$(".open-contact-modal-btn, [data-open-contact-modal]");
const closeModalBtn = $("#contact-modal-close");

function openContactModal(e) {
  if (e && typeof e.preventDefault === "function") e.preventDefault();
  if (!contactModal) return;
  contactModal.classList.add("open");
  contactModal.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
  closeModalBtn?.focus();
}

function closeContactModal() {
  if (!contactModal) return;
  contactModal.classList.remove("open");
  contactModal.setAttribute("aria-hidden", "true");
  document.body.style.overflow = "";
}

window.openContactModal = openContactModal;
window.closeContactModal = closeContactModal;

if (contactModal) {
  openModalBtns.forEach(btn => btn.addEventListener("click", openContactModal));
  if (closeModalBtn) closeModalBtn.addEventListener("click", closeContactModal);

  contactModal.addEventListener("click", e => {
    if (e.target === contactModal) closeContactModal();
  });

  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && contactModal.classList.contains("open")) {
      closeContactModal();
    }
  });
}

const VALID_VIEWS = ["home", "about", "skills", "projects", "vision", "contact"];
const DEFAULT_VIEW = "home";

function getActiveViewFromHash() {
  const hash = (location.hash || "").replace(/^#/, "");
  return VALID_VIEWS.includes(hash) ? hash : DEFAULT_VIEW;
}

function switchView(viewId, updateHistory = true) {
  if (!VALID_VIEWS.includes(viewId)) {
    viewId = DEFAULT_VIEW;
  }

  const targetSection = document.getElementById(viewId);
  if (!targetSection) return;

  const allSections = document.querySelectorAll(".section-view");
  if (!allSections.length) return;

  allSections.forEach(s => s.classList.remove("is-active"));
  targetSection.classList.add("is-active");

  document.querySelectorAll("[data-nav-view]").forEach(el => {
    const v = el.dataset.navView;
    el.classList.toggle("active", v === viewId);
  });

  targetSection.querySelectorAll(".reveal").forEach(el => {
    el.classList.add("visible");
  });

  if (viewId === "skills") {
    fillBars(targetSection);
  }

  if (typeof updateCardHeaderAlignment === "function") {
    requestAnimationFrame(updateCardHeaderAlignment);
  }

  window.scrollTo({ top: 0, behavior: "instant" });

  if (updateHistory) {
    const newHash = "#" + viewId;
    if (location.hash !== newHash) {
      if (history.pushState) {
        history.pushState(null, "", newHash);
      } else {
        location.hash = newHash;
      }
    }
  }
}

function initSpaNavigation() {
  const sectionViews = document.querySelectorAll(".section-view");
  if (!sectionViews.length) return;

  const initialView = getActiveViewFromHash();
  switchView(initialView, false);

  window.addEventListener("hashchange", () => {
    switchView(getActiveViewFromHash(), false);
  });

  document.addEventListener("click", e => {
    const link = e.target.closest("a");
    if (!link) return;

    let targetView = link.dataset.navView;
    if (!targetView) {
      const href = link.getAttribute("href") || "";
      const match = href.match(/#([a-zA-Z0-9_-]+)$/);
      if (match && VALID_VIEWS.includes(match[1])) {
        const isCurrentPage = link.pathname === location.pathname || href.startsWith("#");
        if (isCurrentPage) {
          targetView = match[1];
        }
      }
    }

    if (targetView && VALID_VIEWS.includes(targetView)) {
      e.preventDefault();
      switchView(targetView, true);
      if (navbar && navbar.classList.contains("open")) {
        navbar.classList.remove("open");
        if (menuBtn) menuBtn.setAttribute("aria-expanded", "false");
      }
    }
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initSpaNavigation);
} else {
  initSpaNavigation();
}

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  const lightBtns = document.querySelectorAll('[data-theme-btn="light"]');
  const darkBtns = document.querySelectorAll('[data-theme-btn="dark"]');
  const isDark = theme === "dark";
  lightBtns.forEach(btn => {
    btn.classList.toggle("active", !isDark);
    btn.setAttribute("aria-pressed", (!isDark).toString());
  });
  darkBtns.forEach(btn => {
    btn.classList.toggle("active", isDark);
    btn.setAttribute("aria-pressed", isDark.toString());
  });

  const footerEl = document.querySelector(".site-footer");
  if (footerEl) {
    footerEl.style.backgroundColor = "";
  }
}

function setTheme(theme) {
  try {
    localStorage.setItem("freeman-theme", theme);
  } catch (e) {}
  applyTheme(theme);
}

function initTheme() {
  let currentTheme = "dark";
  try {
    const saved = localStorage.getItem("freeman-theme");
    if (saved === "light" || saved === "dark") {
      currentTheme = saved;
    } else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches) {
      currentTheme = "light";
    }
  } catch (e) {}
  applyTheme(currentTheme);

  document.querySelectorAll(".theme-switch").forEach(switchEl => {
    switchEl.addEventListener("click", e => {
      const btn = e.target.closest("[data-theme-btn]");
      if (btn) {
        setTheme(btn.dataset.themeBtn);
      } else {
        const cur = document.documentElement.getAttribute("data-theme") || "dark";
        setTheme(cur === "dark" ? "light" : "dark");
      }
    });
  });

  window.addEventListener("storage", e => {
    if (e.key === "freeman-theme" && (e.newValue === "light" || e.newValue === "dark")) {
      applyTheme(e.newValue);
    }
  });

  try {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", e => {
      if (!localStorage.getItem("freeman-theme")) {
        applyTheme(e.matches ? "dark" : "light");
      }
    });
  } catch (e) {}
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initTheme);
} else {
  initTheme();
}

const cardSelectors = ".contact-compact-item, .contact-modal-item, .skill-card-box, .trait-card, .approach-pillar, .project-card, .project-item-card, .lab-card";

function toggleCardActive(card) {
  if (!card) return;
  document.querySelectorAll(cardSelectors).forEach(c => {
    if (c !== card) c.classList.remove("is-clicked");
  });
  card.classList.toggle("is-clicked");
}

document.addEventListener("click", e => {
  const card = e.target.closest(cardSelectors);
  if (card) {
    toggleCardActive(card);
  } else {
    document.querySelectorAll(cardSelectors).forEach(c => c.classList.remove("is-clicked"));
  }
});

document.addEventListener("keydown", e => {
  if (e.key === "Enter" || e.key === " ") {
    const activeEl = document.activeElement;
    if (activeEl && activeEl.matches(cardSelectors) && !activeEl.matches("button, a, input, textarea")) {
      if (e.key === " ") e.preventDefault();
      toggleCardActive(activeEl);
    }
  }
});

function updateCardHeaderAlignment() {
  document.querySelectorAll(".skill-box-header").forEach(header => {
    const title = header.querySelector(".skill-box-title, .project-card-title, h3, h4");
    if (!title) return;
    const computed = window.getComputedStyle(title);
    const fontSize = parseFloat(computed.fontSize) || 16;
    const parsedLineHeight = parseFloat(computed.lineHeight);
    const lineHeight = isNaN(parsedLineHeight) ? (fontSize * 1.35) : parsedLineHeight;
    const isSingleLine = title.offsetHeight <= lineHeight * 1.35;
    header.classList.toggle("is-single-line", isSingleLine);
    header.classList.toggle("is-multiline", !isSingleLine);
    const card = header.closest(".skill-card-box, .project-item-card, .trait-card, .approach-pillar");
    if (card) {
      card.classList.toggle("is-single-line", isSingleLine);
      card.classList.toggle("is-multiline", !isSingleLine);
    }
  });
}

window.addEventListener("load", updateCardHeaderAlignment);
window.addEventListener("resize", () => {
  requestAnimationFrame(updateCardHeaderAlignment);
  if (window.innerWidth > 992 && navbar && navbar.classList.contains("open")) {
    navbar.classList.remove("open");
    if (menuBtn) menuBtn.setAttribute("aria-expanded", "false");
  }
});
window.addEventListener("orientationchange", () => {
  setTimeout(updateCardHeaderAlignment, 150);
});
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", updateCardHeaderAlignment);
} else {
  updateCardHeaderAlignment();
}
if (document.fonts && document.fonts.ready) {
  document.fonts.ready.then(updateCardHeaderAlignment);
}

// Lab / Interactive Utilities (safely guarded)
function triggerTerminalToast() {
  if (typeof toast === "function") toast("💻 Terminal : fonctionnalités disponibles dans les sections dédiées");
}
$$("[data-open-terminal]").forEach(btn => btn.addEventListener("click", triggerTerminalToast));
document.addEventListener("keydown", e => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
    e.preventDefault();
    triggerTerminalToast();
  }
});
