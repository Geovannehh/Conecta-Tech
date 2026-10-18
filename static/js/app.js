(() => {
  "use strict";

  const dataElement = document.getElementById("campus-data");
  if (!dataElement) return;
  const data = JSON.parse(dataElement.textContent);
  let profile = "calouro";
  let category = "Todos";
  let search = "";
  let selectedHelp = data.helpItems[0];
  const completedMissions = new Set();

  const journeyGrid = document.getElementById("journey-grid");
  const helpGrid = document.getElementById("help-grid");
  const helpEmpty = document.getElementById("help-empty");
  const resultsMeta = document.getElementById("results-meta");
  const searchInput = document.getElementById("help-search");

  document.querySelectorAll("[data-profile]").forEach((button) => {
    button.addEventListener("click", () => chooseProfile(button.dataset.profile));
  });

  document.querySelectorAll("[data-category]").forEach((button) => {
    button.addEventListener("click", () => {
      category = button.dataset.category;
      document.querySelectorAll("[data-category]").forEach((item) => item.classList.toggle("active", item === button));
      renderHelp();
    });
  });

  searchInput.addEventListener("input", (event) => {
    search = event.target.value;
    renderHelp();
  });

  const menuButton = document.querySelector(".menu-button");
  const nav = document.querySelector(".main-nav");
  menuButton?.addEventListener("click", () => {
    const open = nav.classList.toggle("is-open");
    menuButton.setAttribute("aria-expanded", String(open));
  });
  nav?.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => nav.classList.remove("is-open")));

  document.querySelectorAll(".mission-card").forEach((card) => {
    card.addEventListener("click", () => {
      const mission = card.dataset.mission;
      const done = completedMissions.has(mission);
      if (done) completedMissions.delete(mission);
      else {
        completedMissions.add(mission);
        track("mission_completed", "acolhimento", mission);
      }
      card.classList.toggle("done", !done);
      card.querySelector(".mission-icon").textContent = done ? card.dataset.icon : "✓";
      card.querySelector(".mission-action").innerHTML = done ? "Marcar como concluída <b>→</b>" : "Missão concluída <b>→</b>";
      renderProgress();
    });
  });

  bindForm("suggestion-form", "/api/suggestions", "Sugestão enviada. Obrigado por participar!", (form) => ({
    profile,
    category: form.elements.category.value,
    message: form.elements.message.value,
  }));
  bindForm("rating-form", "/api/ratings", "Avaliação registrada. Obrigado!", (form) => ({
    sector: form.elements.sector.value,
    score: Number(new FormData(form).get("score")),
    comment: form.elements.comment.value,
  }));

  function chooseProfile(nextProfile) {
    if (!['calouro', 'professor'].includes(nextProfile)) return;
    profile = nextProfile;
    category = "Todos";
    document.querySelectorAll("[data-profile]").forEach((button) => button.classList.toggle("active", button.dataset.profile === profile));
    document.querySelectorAll("[data-category]").forEach((button) => button.classList.toggle("active", button.dataset.category === "Todos"));
    document.getElementById("profile-chip").textContent = `Para ${profile === "calouro" ? "calouro" : "professor"}`;
    document.getElementById("help-profile-copy").textContent = `Busque por uma dúvida ou escolha uma categoria. As orientações estão adaptadas ao perfil de ${profile === "calouro" ? "calouro" : "professor ingressante"}.`;
    renderJourneys();
    renderHelp();
    track("profile_selected", "perfil", profile);
  }

  function renderJourneys() {
    journeyGrid.replaceChildren();
    data.journeys[profile].forEach((step, index) => {
      const article = element("article", "journey-card");
      const number = element("span", "step-number", step.number);
      const line = element("div", "step-line");
      const lineProgress = document.createElement("span");
      lineProgress.style.width = `${(index + 1) * 20}%`;
      line.append(lineProgress);
      const heading = element("h3", "", step.title);
      const text = element("p", "", step.text);
      const button = element("button", "", "Ver orientações ");
      button.type = "button";
      button.append(element("span", "", "↗"));
      button.addEventListener("click", () => {
        track("journey_viewed", "manual", step.title);
        document.getElementById("ajuda").scrollIntoView({ behavior: "smooth" });
      });
      article.append(number, line, heading, text, button);
      journeyGrid.append(article);
    });
  }

  function renderHelp() {
    const query = normalize(search);
    const items = data.helpItems.filter((item) => item.profiles.includes(profile)
      && (category === "Todos" || item.category === category)
      && (!query || normalize([item.title, item.summary, item.sector, ...item.tags].join(" ")).includes(query)));
    helpGrid.replaceChildren();
    resultsMeta.replaceChildren(element("strong", "", String(items.length)), document.createTextNode(items.length === 1 ? " orientação encontrada" : " orientações encontradas"));
    helpEmpty.hidden = items.length !== 0;
    items.forEach((item) => helpGrid.append(helpCard(item)));
    if (!items.includes(selectedHelp) && items.length) selectHelp(items[0], false);
  }

  function helpCard(item) {
    const article = element("article", "help-card");
    const top = element("div", "help-card-top");
    top.append(element("span", "", item.category), element("b", "", categoryLetter(item.category)));
    const heading = element("h3", "", item.title);
    const summary = element("p", "", item.summary);
    const sector = element("div", "sector-label");
    sector.append(element("small", "", "Setor responsável"), element("strong", "", item.sector));
    const button = element("button", "", "Ver orientação completa ");
    button.type = "button";
    button.append(element("span", "", "→"));
    button.addEventListener("click", () => selectHelp(item, true));
    article.append(top, heading, summary, sector, button);
    return article;
  }

  function selectHelp(item, scroll) {
    selectedHelp = item;
    setText("guidance-title", item.title);
    setText("guidance-category", item.category);
    setText("guidance-sector", item.sector);
    setText("guidance-location", item.location);
    setText("guidance-contact", item.contact);
    const steps = document.getElementById("guidance-steps");
    steps.replaceChildren(...item.steps.map((step) => element("li", "", step)));
    if (scroll) {
      track("help_viewed", item.category, item.id);
      document.getElementById("orientacao-detalhada").scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }

  function renderProgress() {
    const progress = Math.round(completedMissions.size / 4 * 100);
    setText("mission-count", `${completedMissions.size} de 4 missões`);
    setText("mission-percent", `${progress}% concluído nesta visita`);
    document.getElementById("mission-progress").style.width = `${progress}%`;
  }

  function bindForm(id, url, successMessage, serialize) {
    const form = document.getElementById(id);
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const button = form.querySelector("button[type='submit']");
      const status = form.querySelector(".form-status");
      const original = button.innerHTML;
      button.disabled = true;
      button.textContent = "Enviando…";
      status.textContent = "";
      status.className = "form-status";
      try {
        const response = await postJson(url, serialize(form));
        if (!response.ok) throw new Error("Não foi possível enviar.");
        form.reset();
        status.textContent = `✓ ${successMessage}`;
        status.classList.add("success");
      } catch {
        status.textContent = "Não foi possível enviar. Tente novamente.";
        status.classList.add("error");
      } finally {
        button.disabled = false;
        button.innerHTML = original;
      }
    });
  }

  function track(type, eventCategory, reference) {
    postJson("/api/interactions", { type, profile, category: eventCategory, reference }).catch(() => {});
  }

  function postJson(url, body) {
    return fetch(url, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(body) });
  }

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function setText(id, text) {
    document.getElementById(id).textContent = text;
  }

  function normalize(value) {
    return value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  }

  function categoryLetter(value) {
    return { Tecnologia: "TI", Acadêmico: "AC", Financeiro: "FI", Biblioteca: "BI", Localização: "LO", Docência: "DO" }[value] || "AJ";
  }

  renderJourneys();
  renderHelp();
  selectHelp(selectedHelp, false);
})();
