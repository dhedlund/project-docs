/* Diagram zoom — adds a fullscreen, scroll-to-zoom / drag-to-pan view to
   Mermaid and D2 diagrams, which otherwise shrink to fit the column.

   Self-contained: no external libraries, works offline. Loaded via
   `extra_javascript` in mkdocs.yml.

   Mermaid note: Material renders each Mermaid diagram into a *closed* shadow root
   on a <div class="mermaid">, so its <svg> can't be reached, measured, or cloned
   from the page. We therefore zoom by moving the whole diagram container into a
   wrapper we control (.dz-content) with a definite width, and transforming the
   wrapper. The same path handles D2 (a <div class="d2">). */
(function () {
  "use strict";

  // ── Shadow-DOM shim ────────────────────────────────────────────────────────
  // Material renders Mermaid into a *closed* shadow root, so (a) its arrowhead
  // theming gap can't be patched from page CSS and (b) we can't read the diagram.
  // Coerce new shadow roots to "open". This runs on script load — before
  // Material's document$ pipeline first renders Mermaid — so the override is in
  // place in time, and it persists across instant-navigation re-renders.
  if (!window.__dzShadowPatched && Element.prototype.attachShadow) {
    var _attachShadow = Element.prototype.attachShadow;
    Element.prototype.attachShadow = function (init) {
      if (init && init.mode === "closed") {
        init = Object.assign({}, init, { mode: "open" });
      }
      return _attachShadow.call(this, init);
    };
    window.__dzShadowPatched = true;
  }

  // Inject the one rule Material's shadow CSS omits: the flowchart arrowhead
  // *fill*. Material themes the lines and the arrowhead stroke but not its fill,
  // so arrows go dark (invisible in dark mode). Custom properties inherit through
  // the shadow boundary, so --md-mermaid-edge-color resolves correctly here. We
  // scope to flowchart point markers to avoid disturbing class/sequence diagrams,
  // which Material colours deliberately.
  function fixArrows(host) {
    var sr = host.shadowRoot;
    if (!sr || sr.querySelector("style[data-dz-arrows]")) return;
    var s = document.createElement("style");
    s.setAttribute("data-dz-arrows", "1");
    s.textContent =
      'marker[id*="flowchart-point"] path,marker[id*="flowchart-circle"] path,' +
      'marker[id*="flowchart-cross"] path{fill:var(--md-mermaid-edge-color)!important;stroke:none}';
    sr.appendChild(s);
  }

  // Zoom-out floor, as a fraction of the viewport in the diagram's dominant
  // dimension (initial fit is ~0.92, so this lets you shrink it a bit smaller to
  // pan content out from behind the close button). Zoom-in cap is a multiple of
  // the fit scale. Both are easy to tune.
  var MIN_FRAC = 0.55;
  var MAX_ZOOM_MULT = 10;

  var EXPAND_ICON =
    '<svg viewBox="0 0 24 24" aria-hidden="true">' +
    '<path d="M5 5h5V3H3v7h2V5m14 0v5h2V3h-7v2h5M5 14H3v7h7v-2H5v-5m16 0h-2v5h-5v2h7v-7z"/>' +
    "</svg>";

  // Map Mermaid's SVG aria-roledescription (and D2) to a section anchor in the
  // "Reading the diagrams" guide. Type-level only — robust across versions; we do
  // NOT inspect individual symbols.
  var TYPE_ANCHOR = {
    "flowchart-v2": "flowchart", flowchart: "flowchart", graph: "flowchart",
    sequence: "sequence", er: "er",
    stateDiagram: "state", "stateDiagram-v2": "state", state: "state",
    classDiagram: "class", class: "class",
  };

  function readingURL(anchor) {
    // Resolve the guide's URL from the site root (the header logo links home),
    // so it works at any page depth.
    var logo = document.querySelector(".md-logo");
    var home = (logo && logo.getAttribute("href")) || ".";
    var url = new URL("reading-diagrams/", new URL(home, location.href));
    return url.href + (anchor ? "#" + anchor : "");
  }

  function diagramAnchor(el) {
    if (el.matches(".d2") || el.querySelector(".d2-light, .d2-dark")) return "d2";
    var svg = el.querySelector("svg") || (el.shadowRoot && el.shadowRoot.querySelector("svg"));
    var role = svg && svg.getAttribute("aria-roledescription");
    return (role && TYPE_ANCHOR[role]) || "";
  }

  // The Key panel pulls its content from the guide page itself — one source of
  // truth, no duplicated legend to drift. Cached after first fetch.
  var _docCache = null;
  function fetchReadingDoc() {
    if (_docCache) return Promise.resolve(_docCache);
    return fetch(readingURL("")).then(function (r) { return r.text(); }).then(function (html) {
      _docCache = new DOMParser().parseFromString(html, "text/html");
      return _docCache;
    });
  }
  function sectionFragment(doc, anchor) {
    if (!anchor) return null;
    var heading = doc.getElementById(anchor);
    if (heading && !/^H[1-6]$/.test(heading.tagName)) heading = heading.closest("h1,h2,h3,h4,h5,h6");
    if (!heading) return null;
    var level = +heading.tagName.charAt(1);
    var frag = document.createElement("div");
    frag.appendChild(heading.cloneNode(true));
    var n = heading.nextElementSibling;
    while (n) {
      var m = /^H([1-6])$/.exec(n.tagName);
      if (m && +m[1] <= level) break;
      frag.appendChild(n.cloneNode(true));
      n = n.nextElementSibling;
    }
    frag.querySelectorAll(".headerlink").forEach(function (a) { a.remove(); });
    frag.querySelectorAll("[id]").forEach(function (x) { x.removeAttribute("id"); });
    return frag;
  }

  // Lazily-created singleton modal, reused for every diagram.
  function getModal() {
    var modal = document.querySelector(".dz-modal");
    if (modal) return modal;

    modal = document.createElement("div");
    modal.className = "dz-modal";
    modal.hidden = true;
    modal.innerHTML =
      '<div class="dz-stage"><div class="dz-content"></div></div>' +
      '<button class="dz-close" type="button" aria-label="Close">✕</button>' +
      '<aside class="dz-panel" hidden></aside>' +
      '<div class="dz-bar">' +
      '<button class="dz-key" type="button">Key</button>' +
      '<a class="dz-help" target="_blank" rel="noopener">How to read this diagram ↗</a>' +
      '<span class="dz-hint">scroll to zoom · drag to pan · Esc to close</span>' +
      "</div>";
    document.body.appendChild(modal);

    var stage = modal.querySelector(".dz-stage");
    var content = modal.querySelector(".dz-content");
    var panel = modal.querySelector(".dz-panel");
    var keyBtn = modal.querySelector(".dz-key");
    var helpLink = modal.querySelector(".dz-help");
    var curAnchor = "";
    var box = null, placeholder = null;        // the diagram + where it came from
    var baseW = 1, baseH = 1;                   // content size at scale 1
    var scale = 1, fitScale = 1, minScale = 1, maxScale = 1;
    var tx = 0, ty = 0;
    var dragging = false, startX = 0, startY = 0;
    var downTarget = null, downX0 = 0, downY0 = 0, moved = false;

    function apply() {
      scale = clamp(scale, minScale, maxScale);
      var r = stage.getBoundingClientRect();
      var iw = baseW * scale, ih = baseH * scale;
      // Keep the diagram overlapping the viewport: when larger than the stage its
      // edges stay flush (pan to any part incl. the centre); when smaller it
      // stays fully inside.
      tx = clamp(tx, Math.min(0, r.width - iw), Math.max(0, r.width - iw));
      ty = clamp(ty, Math.min(0, r.height - ih), Math.max(0, r.height - ih));
      content.style.transform = "translate(" + tx + "px," + ty + "px) scale(" + scale + ")";
    }

    function close() {
      if (box && placeholder && placeholder.parentNode) {
        placeholder.parentNode.replaceChild(box, placeholder);
      }
      content.innerHTML = "";
      content.removeAttribute("style");
      panel.hidden = true;
      box = null;
      placeholder = null;
      modal.hidden = true;
    }

    modal.querySelector(".dz-close").addEventListener("click", close);
    document.addEventListener("keydown", function (e) {
      if (!modal.hidden && e.key === "Escape") close();
    });

    // "Key" — toggle a side panel showing the legend for this diagram's type,
    // pulled from the reading guide page (single source of truth).
    keyBtn.addEventListener("click", function () {
      if (!panel.hidden) { panel.hidden = true; return; }
      panel.hidden = false;
      if (panel.dataset.loaded === curAnchor) return;
      panel.dataset.loaded = curAnchor;
      panel.innerHTML = '<p class="dz-panel-note">Loading…</p>';
      fetchReadingDoc().then(function (doc) {
        var frag = sectionFragment(doc, curAnchor);
        panel.innerHTML = "";
        if (frag) panel.appendChild(frag);
        else panel.innerHTML = '<p class="dz-panel-note">No legend for this diagram type yet.</p>';
        var more = document.createElement("p");
        more.className = "dz-panel-more";
        more.innerHTML = '<a href="' + helpLink.href + '" target="_blank" rel="noopener">Full reading guide ↗</a>';
        panel.appendChild(more);
      }).catch(function () {
        panel.dataset.loaded = "";
        panel.innerHTML = '<p class="dz-panel-note">Can’t load the key here (try over <code>make serve</code>). ' +
          '<a href="' + helpLink.href + '" target="_blank" rel="noopener">Open the reading guide ↗</a></p>';
      });
    });

    stage.addEventListener(
      "wheel",
      function (e) {
        if (modal.hidden) return;
        e.preventDefault();
        var r = stage.getBoundingClientRect();
        var px = e.clientX - r.left, py = e.clientY - r.top;
        var next = clamp(scale * (e.deltaY < 0 ? 1.15 : 1 / 1.15), minScale, maxScale);
        var f = next / scale;
        tx = px - (px - tx) * f;
        ty = py - (py - ty) * f;
        scale = next;
        apply();
      },
      { passive: false }
    );
    stage.addEventListener("pointerdown", function (e) {
      if (modal.hidden) return;
      downTarget = e.target;
      downX0 = e.clientX;
      downY0 = e.clientY;
      moved = false;
      dragging = true;
      startX = e.clientX - tx;
      startY = e.clientY - ty;
      stage.classList.add("dz-dragging");
      stage.setPointerCapture(e.pointerId);
    });
    stage.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      if (Math.abs(e.clientX - downX0) > 5 || Math.abs(e.clientY - downY0) > 5) moved = true;
      tx = e.clientX - startX;
      ty = e.clientY - startY;
      apply();
    });
    function endDrag() {
      dragging = false;
      stage.classList.remove("dz-dragging");
      // Close only on a genuine click (no real drag) that landed outside the
      // diagram itself — i.e. on the dark backdrop. Clicking or dragging the
      // diagram never closes. (Pointer capture makes the native click target the
      // stage, so we judge by the pointerdown target instead.)
      if (!moved && downTarget && box && !box.contains(downTarget)) close();
      downTarget = null;
    }
    stage.addEventListener("pointerup", endDrag);
    stage.addEventListener("pointercancel", endDrag);

    // Move `el` into the controlled wrapper, size it to the stage, centre it.
    modal.open = function (el) {
      placeholder = document.createComment("dz");
      el.parentNode.insertBefore(placeholder, el);
      content.appendChild(el);
      box = el;

      // Type-aware "how to read" target (and reset the key panel for this diagram).
      curAnchor = diagramAnchor(el);
      helpLink.href = readingURL(curAnchor);
      panel.hidden = true;

      // Show the modal BEFORE measuring — a hidden (display:none) modal reports
      // zero sizes, which would collapse the fit/zoom/pan math.
      modal.hidden = false;

      var r = stage.getBoundingClientRect();
      // Render at full stage width first so the diagram's percentage-width SVG
      // lays out at a real size (instead of collapsing), then measure the actual
      // SVG and shrink the wrapper to hug it — so there's dark backdrop on all
      // sides. The shadow shim makes Mermaid's SVG reachable; D2's is light-DOM.
      content.style.width = r.width + "px";
      content.style.transform = "none";
      var svg = box.querySelector("svg") || (box.shadowRoot && box.shadowRoot.querySelector("svg"));
      var dw = 0, dh = 0;
      if (svg) { var sb = svg.getBoundingClientRect(); dw = sb.width; dh = sb.height; }
      if (!dw || !dh) { var cb = content.getBoundingClientRect(); dw = cb.width; dh = cb.height; }
      content.style.width = Math.min(dw, r.width) + "px";

      var b = content.getBoundingClientRect();
      baseW = b.width || 1;
      baseH = b.height || 1;
      // Fit ~90% of the viewport in the limiting dimension, then centre.
      fitScale = Math.min((r.width * 0.92) / baseW, (r.height * 0.9) / baseH) || 1;
      minScale = Math.min((r.width * MIN_FRAC) / baseW, (r.height * MIN_FRAC) / baseH) || fitScale;
      maxScale = Math.max(fitScale * MAX_ZOOM_MULT, 12);
      scale = fitScale;
      tx = (r.width - baseW * scale) / 2;
      ty = (r.height - baseH * scale) / 2;

      apply();
    };
    return modal;
  }

  function clamp(v, lo, hi) {
    return v < lo ? lo : v > hi ? hi : v;
  }

  // Give each diagram an expand button. Detection differs by type:
  //  - Mermaid: Material replaces <pre class="mermaid"> with a rendered
  //    <div class="mermaid"> (closed shadow) — a *div* is the ready signal.
  //  - D2: <div class="d2"> with a light-DOM <svg> once rendered.
  function enhance() {
    var boxes = document.querySelectorAll("div.mermaid, .d2");
    for (var i = 0; i < boxes.length; i++) {
      var el = boxes[i];
      if (el.dataset.dz) continue;
      var isMermaid = el.matches("div.mermaid");
      if (!isMermaid && !el.querySelector("svg")) continue; // d2 not rendered yet
      el.dataset.dz = "1";
      if (isMermaid) fixArrows(el);

      var wrap = document.createElement("div");
      wrap.className = "dz-wrap";
      el.parentNode.insertBefore(wrap, el);
      wrap.appendChild(el);

      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "dz-btn";
      btn.title = "Expand diagram";
      btn.setAttribute("aria-label", "Expand diagram");
      btn.innerHTML = EXPAND_ICON;
      (function (container) {
        btn.addEventListener("click", function (e) {
          e.preventDefault();
          getModal().open(container);
        });
      })(el);
      wrap.appendChild(btn);
    }
  }

  // Diagrams render asynchronously and Material swaps content on instant
  // navigation — re-run on both, with a debounced observer as a safety net.
  var pending = null;
  function schedule() {
    if (pending) return;
    pending = setTimeout(function () { pending = null; enhance(); }, 250);
  }
  if (window.document$ && window.document$.subscribe) {
    window.document$.subscribe(schedule);
  } else if (document.readyState !== "loading") {
    schedule();
  } else {
    document.addEventListener("DOMContentLoaded", schedule);
  }
  new MutationObserver(schedule).observe(document.documentElement, {
    childList: true,
    subtree: true,
  });
})();
