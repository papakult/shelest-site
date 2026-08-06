/* SHELESTFIT premium layer: scroll progress, reveal, back-to-top */
(function(){
  "use strict";
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- золотая полоса прогресса чтения ---- */
  var bar = document.createElement("div");
  bar.className = "pg-progress";
  bar.setAttribute("aria-hidden", "true");
  document.body.appendChild(bar);
  var ticking = false;
  function paint(){
    ticking = false;
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    var p = max > 0 ? (h.scrollTop || document.body.scrollTop) / max : 0;
    bar.style.transform = "scaleX(" + p + ")";
  }
  window.addEventListener("scroll", function(){
    if (!ticking){ ticking = true; requestAnimationFrame(paint); }
  }, { passive:true });
  paint();

  /* ---- кнопка «наверх» ---- */
  var top = document.createElement("button");
  top.className = "pg-top";
  top.type = "button";
  top.setAttribute("aria-label", "Наверх");
  top.innerHTML = "&#8593;";
  document.body.appendChild(top);
  top.addEventListener("click", function(){
    window.scrollTo({ top:0, behavior: reduced ? "auto" : "smooth" });
  });
  window.addEventListener("scroll", function(){
    top.classList.toggle("is-on", (window.scrollY || 0) > 600);
  }, { passive:true });

  /* ---- reveal-анимации при скролле ---- */
  if (reduced || !("IntersectionObserver" in window)) return;
  var sels = ["section", ".card", ".bento", ".kase", ".post", ".faq__item",
              ".rail__c", ".team__m", "figure", ".price", ".tarif"];
  var seen = new Set();
  var els = [];
  sels.forEach(function(s){
    document.querySelectorAll(s).forEach(function(el){
      if (seen.has(el)) return;
      var r = el.getBoundingClientRect();
      if (r.height < 20 || r.height > window.innerHeight * 1.4) return;
      seen.add(el); els.push(el);
    });
  });
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if (e.isIntersecting){
        e.target.classList.add("rv-in");
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
  els.forEach(function(el){
    var r = el.getBoundingClientRect();
    if (r.top < window.innerHeight * 0.9){ el.classList.add("rv-in"); return; }
    el.classList.add("rv");
    io.observe(el);
  });
})();
