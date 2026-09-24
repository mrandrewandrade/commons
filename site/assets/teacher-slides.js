(function () {
  "use strict";

  function normalise(value) {
    return String(value || "").trim().toLowerCase();
  }

  function parseTags(card) {
    return String(card.dataset.tags || "")
      .split("|")
      .map(normalise)
      .filter(Boolean);
  }

  function init() {
    const cards = Array.from(document.querySelectorAll("[data-slide-card]"));
    const search = document.querySelector("[data-slide-search]");
    const collection = document.querySelector("[data-slide-collection]");
    const tagFilters = document.querySelector("[data-slide-tag-filters]");
    const resultCount = document.querySelector("[data-slide-result-count]");
    const clear = document.querySelector("[data-slide-clear]");
    const empty = document.querySelector("[data-slide-empty]");

    if (!cards.length || !search || !collection || !tagFilters) return;

    let activeTag = "";

    const tagCounts = new Map();
    cards.forEach(function (card) {
      parseTags(card).forEach(function (tag) {
        tagCounts.set(tag, (tagCounts.get(tag) || 0) + 1);
      });
    });

    Array.from(tagCounts.entries())
      .sort(function (a, b) {
        return a[0].localeCompare(b[0]);
      })
      .forEach(function (entry) {
        const button = document.createElement("button");
        button.type = "button";
        button.dataset.slideTag = entry[0];
        button.setAttribute("aria-pressed", "false");
        button.textContent = entry[0] + " ×" + entry[1];
        tagFilters.appendChild(button);
      });

    function update() {
      const query = normalise(search.value);
      const selectedCollection = normalise(collection.value);
      let visible = 0;

      cards.forEach(function (card) {
        const cardCollection = normalise(card.dataset.collection);
        const tags = parseTags(card);
        const haystack = normalise(
          [card.dataset.search, card.dataset.collection, card.textContent].join(" ")
        );

        const matchesQuery = !query || haystack.includes(query);
        const matchesCollection =
          !selectedCollection || cardCollection === selectedCollection;
        const matchesTag = !activeTag || tags.includes(activeTag);
        const show = matchesQuery && matchesCollection && matchesTag;

        card.hidden = !show;
        if (show) visible += 1;
      });

      if (resultCount) {
        resultCount.textContent =
          visible + (visible === 1 ? " deck" : " decks") + " shown";
      }

      if (empty) empty.hidden = visible !== 0;
      if (clear) {
        clear.hidden = !query && !selectedCollection && !activeTag;
      }
    }

    function setActiveTag(tag) {
      activeTag = normalise(tag);
      tagFilters.querySelectorAll("[data-slide-tag]").forEach(function (button) {
        const active = normalise(button.dataset.slideTag) === activeTag;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-pressed", active ? "true" : "false");
      });
      update();
    }

    search.addEventListener("input", update);
    collection.addEventListener("change", update);

    tagFilters.addEventListener("click", function (event) {
      const button = event.target.closest("[data-slide-tag]");
      if (!button) return;
      const next = normalise(button.dataset.slideTag);
      setActiveTag(next === activeTag ? "" : next);
    });

    document.addEventListener("click", function (event) {
      const button = event.target.closest("[data-slide-card-tag]");
      if (!button) return;
      const tag = normalise(button.dataset.slideCardTag);
      setActiveTag(tag);
      window.scrollTo({
        top: Math.max(0, search.getBoundingClientRect().top + window.scrollY - 110),
        behavior: "smooth"
      });
    });

    if (clear) {
      clear.addEventListener("click", function () {
        search.value = "";
        collection.value = "";
        setActiveTag("");
        search.focus();
      });
    }

    update();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
