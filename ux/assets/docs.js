// Behaviour for generated manual pages: role-path banner, path-aware pager,
// copy buttons on code blocks, and the mobile menu.
(function () {
  const body = document.body;
  const page = body.dataset.page;          // e.g. "start" or "review/non-technical-fitness"
  const root = body.dataset.root || "";    // relative prefix back to ux/
  const ROLES = window.RHO_ROLES || [];
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const store = {
    get() { try { return localStorage.getItem("rho-path"); } catch (e) { return null; } },
    set(v) { try { v ? localStorage.setItem("rho-path", v) : localStorage.removeItem("rho-path"); } catch (e) {} }
  };

  // Which path is the reader on? ?path= wins, then the remembered one.
  const fromUrl = new URLSearchParams(location.search).get("path");
  if (fromUrl) store.set(fromUrl);
  const role = ROLES.find(r => r.id === (fromUrl || store.get()));
  const docHref = p => root + "docs/" + p + ".html";

  if (role) {
    const idx = role.steps.findIndex(s => s.page === page);

    // Banner
    const bar = document.createElement("div");
    bar.className = "pathbar";
    bar.innerHTML = `
      <span class="who">Your path · <strong>${esc(role.short)}</strong></span>
      <ol>${role.steps.map((s, i) => `<li>${
        i === idx ? `<span class="here" aria-current="step">${i + 1}. ${esc(s.title)}</span>`
                  : `<a href="${docHref(s.page)}">${i + 1}. ${esc(s.title)}</a>`}</li>`).join("")}</ol>
      <button class="leave" type="button">Leave path ×</button>`;
    const main = document.querySelector("main");
    main.insertBefore(bar, main.firstChild);
    bar.querySelector(".leave").addEventListener("click", () => { store.set(null); location.href = location.pathname; });

    // Path-aware pager, only on pages that are part of the path
    if (idx !== -1) {
      const pager = document.querySelector(".pager");
      const prev = role.steps[idx - 1], next = role.steps[idx + 1];
      let html = "";
      if (prev) html += `<a class="prev" href="${docHref(prev.page)}"><div class="dir">← Step ${idx}</div><div class="t">${esc(prev.title)}</div></a>`;
      else html += `<a class="prev" href="${root}index.html#${role.id}"><div class="dir">← Back</div><div class="t">Your path</div></a>`;
      if (next) {
        html += `<a class="next primary" href="${docHref(next.page)}"><div class="dir">Next · Step ${idx + 2} of ${role.steps.length}</div><div class="t">${esc(next.title)} →</div></a>`;
        pager.innerHTML = html;
      } else {
        pager.innerHTML = html;
        const done = document.createElement("section");
        done.className = "done";
        done.innerHTML = `
          <h3>You've finished the ${esc(role.short.toLowerCase())} path.</h3>
          <p>Keep exploring the manual, or pick another path.</p>
          <a class="cta primary" href="${root}docs/index.html">Browse the manual <span class="arrow">→</span></a>
          <a class="cta" href="${root}index.html" style="margin-left:8px">Choose another path</a>`;
        pager.after(done);
      }
    }
  }

  // Copy buttons
  document.querySelectorAll(".prose pre").forEach(pre => {
    const wrap = document.createElement("div");
    wrap.className = "codeblock";
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);
    const btn = document.createElement("button");
    btn.className = "copy"; btn.type = "button"; btn.textContent = "Copy";
    btn.addEventListener("click", async () => {
      try { await navigator.clipboard.writeText(pre.innerText.replace(/\n$/, "")); btn.textContent = "Copied"; }
      catch (e) { btn.textContent = "Select & copy"; }
      setTimeout(() => (btn.textContent = "Copy"), 1500);
    });
    wrap.appendChild(btn);
  });

  // Mobile menu
  const toggle = document.querySelector(".menu-toggle");
  const side = document.querySelector(".sidebar");
  if (toggle && side) toggle.addEventListener("click", () => {
    const open = side.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open);
  });
})();
