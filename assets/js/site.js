(function () {
  "use strict";

  const hookClasses = [
    "home-advantage-card",
    "home-advantage-card__head",
    "detail-info-card",
    "detail-cta"
  ];

  const DEFAULT_MAILTO = {
    subject: "Powerlink Energy Inquiry",
    messageHeading: "Message:",
    fields: {
      name: "Name",
      company: "Company",
      country: "Country",
      email: "Email",
      whatsapp: "WhatsApp",
      application: "Application",
      "product-interest": "Product Interest"
    }
  };

  function renderCaseFrameworkCard(card) {
    return card;
  }

  function renderCaseHero(hero) {
    return hero;
  }

  function renderCaseGallery(items) {
    return items || [];
  }

  function renderCaseMedia(item) {
    return item || null;
  }

  function setNavState(button, nav, expanded) {
    button.setAttribute("aria-expanded", expanded ? "true" : "false");
    nav.classList.toggle("is-open", expanded);
  }

  function setupNavigation() {
    const button = document.querySelector(".nav-toggle");
    const nav = document.querySelector(".site-nav");

    if (!button || !nav) {
      return;
    }

    button.addEventListener("click", function () {
      const expanded = button.getAttribute("aria-expanded") === "true";
      setNavState(button, nav, !expanded);
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 760) {
        nav.classList.remove("is-open");
        button.setAttribute("aria-expanded", "false");
      }
    });
  }

  function getMailtoConfig() {
    const body = document.body;
    const subject = body.getAttribute("data-mailto-subject") || DEFAULT_MAILTO.subject;
    const messageHeading = body.getAttribute("data-mailto-message-heading") || DEFAULT_MAILTO.messageHeading;
    const rawFields = body.getAttribute("data-mailto-fields");

    if (!rawFields) {
      return {
        subject: subject,
        messageHeading: messageHeading,
        fields: DEFAULT_MAILTO.fields
      };
    }

    try {
      const parsed = JSON.parse(rawFields);
      return {
        subject: subject,
        messageHeading: messageHeading,
        fields: Object.assign({}, DEFAULT_MAILTO.fields, parsed)
      };
    } catch (error) {
      return {
        subject: subject,
        messageHeading: messageHeading,
        fields: DEFAULT_MAILTO.fields
      };
    }
  }

  function buildMailtoBody(values, mailto) {
    const fields = mailto.fields;
    return [
      fields.name + ": " + (values.name || ""),
      fields.company + ": " + (values.company || ""),
      fields.country + ": " + (values.country || ""),
      fields.email + ": " + (values.email || ""),
      fields.whatsapp + ": " + (values.whatsapp || ""),
      fields.application + ": " + (values.application || ""),
      fields["product-interest"] + ": " + (values["product-interest"] || ""),
      "",
      mailto.messageHeading,
      values.message || ""
    ].join("\n");
  }

  function setupInquiryForm() {
    const form = document.querySelector(".inquiry-form");
    const status = document.querySelector("[data-form-status]");
    const formMode = document.querySelector("[data-form-mode]");
    const formNote = document.body.getAttribute("data-form-note");
    const formStatusText = document.body.getAttribute("data-form-status-text");
    const mailto = getMailtoConfig();

    if (!form) {
      return;
    }

    if (formMode && formNote && !formMode.textContent.trim()) {
      formMode.textContent = formNote;
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();

      const formData = new FormData(form);
      const values = Object.fromEntries(formData.entries());
      const subject = encodeURIComponent(mailto.subject);
      const body = encodeURIComponent(buildMailtoBody(values, mailto));

      if (status && formStatusText) {
        status.textContent = formStatusText;
      }

      window.location.href = "mailto:Bob-Wang@power-linkenergy.com?subject=" + subject + "&body=" + body;
    });
  }

  function setupLanguagePrompt() {
    const body = document.body;
    if (body.getAttribute("data-page") !== "home" || body.getAttribute("data-locale") !== "en") {
      return;
    }

    if (window.sessionStorage.getItem("language-prompt-dismissed") === "1") {
      return;
    }

    const browserLanguage = (navigator.language || "").toLowerCase();
    const targets = [
      { match: /^zh/, href: "/zh/", label: "查看中文站" },
      { match: /^fr/, href: "/fr/", label: "Voir le site en français" },
      { match: /^ru/, href: "/ru/", label: "Открыть сайт на русском" }
    ];
    const target = targets.find(function (entry) {
      return entry.match.test(browserLanguage);
    });

    if (!target) {
      return;
    }

    const banner = document.createElement("div");
    banner.className = "language-prompt";
    banner.innerHTML =
      '<p>Your browser language suggests another site version may fit better.</p>' +
      '<div class="language-prompt__actions">' +
      '<a class="button button--primary" href="' + target.href + '">' + target.label + "</a>" +
      '<button class="button button--ghost" type="button" data-language-prompt-dismiss>Stay in English</button>' +
      "</div>";

    body.appendChild(banner);

    banner.querySelector("[data-language-prompt-dismiss]").addEventListener("click", function () {
      window.sessionStorage.setItem("language-prompt-dismissed", "1");
      banner.remove();
    });
  }

  function initVisualHooks() {
    document.documentElement.setAttribute("data-hooks-ready", hookClasses.join(" "));
    window.renderCaseFrameworkCard = renderCaseFrameworkCard;
    window.renderCaseHero = renderCaseHero;
    window.renderCaseGallery = renderCaseGallery;
    window.renderCaseMedia = renderCaseMedia;
  }

  document.addEventListener("DOMContentLoaded", function () {
    initVisualHooks();
    setupNavigation();
    setupInquiryForm();
    setupLanguagePrompt();
  });
})();
