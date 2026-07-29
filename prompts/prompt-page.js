/**
 * Prompt detail page enhancements: sticky TOC active state + copy prompt.
 */
(function () {
  const tocLinks = Array.from(document.querySelectorAll(".toc nav a[href^='#']"));
  const sections = tocLinks
    .map((a) => {
      const id = a.getAttribute("href").slice(1);
      return { a, el: document.getElementById(id) };
    })
    .filter((x) => x.el);

  function setActive() {
    if (!sections.length) return;
    const y = window.scrollY + 120;
    let current = sections[0];
    for (const s of sections) {
      if (s.el.offsetTop <= y) current = s;
    }
    tocLinks.forEach((a) => a.classList.toggle("is-active", a === current.a));
  }

  window.addEventListener("scroll", setActive, { passive: true });
  setActive();

  const copyBtn = document.getElementById("copy-prompt");
  const status = document.getElementById("copy-status");
  const promptEl = document.getElementById("prompt-source");
  if (copyBtn && promptEl) {
    copyBtn.addEventListener("click", async () => {
      const text = promptEl.innerText || promptEl.textContent || "";
      try {
        await navigator.clipboard.writeText(text);
        if (status) {
          status.textContent = "Copied";
          status.classList.add("show");
          setTimeout(() => status.classList.remove("show"), 1600);
        }
      } catch {
        if (status) {
          status.textContent = "Copy failed";
          status.classList.add("show");
        }
      }
    });
  }
})();
