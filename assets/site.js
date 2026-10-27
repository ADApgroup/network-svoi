(function(){
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Мобильное меню
  var btn = document.querySelector(".menu-btn"), nav = document.getElementById("nav");
  if (btn && nav) {
    btn.addEventListener("click", function(){
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.textContent = open ? "Закрыть" : "Меню";
      document.body.style.overflow = open ? "hidden" : "";
    });
    nav.addEventListener("click", function(e){ if (e.target.closest("a")) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); btn.textContent = "Меню"; document.body.style.overflow = ""; } });
  }

  // Мягкое появление только для того, что ниже первого экрана
  if (!reduce && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if (e.isIntersecting) { e.target.classList.remove("pre"); io.unobserve(e.target); } });
    }, {rootMargin: "0px 0px -8% 0px"});
    document.querySelectorAll(".rv").forEach(function(el){
      if (el.getBoundingClientRect().top > innerHeight * 0.92) { el.classList.add("pre"); io.observe(el); }
    });
  }

  // Подсветка карточек за курсором
  document.querySelectorAll(".card").forEach(function(c){
    c.addEventListener("pointermove", function(e){
      var r = c.getBoundingClientRect();
      c.style.setProperty("--mx", (e.clientX - r.left) + "px");
      c.style.setProperty("--my", (e.clientY - r.top) + "px");
    });
  });

  // Длины линий для анимации рисования печати
  document.querySelectorAll(".seal .draw").forEach(function(p){
    try { p.style.setProperty("--len", Math.ceil(p.getTotalLength())); } catch(e){}
  });

  // Кольца устройства
  var rings = document.querySelectorAll(".rings .ring"), tiers = document.querySelectorAll(".tier");
  function pick(k){
    rings.forEach(function(r){ r.classList.toggle("on", r.dataset.k === k); });
    tiers.forEach(function(t){ var on = t.dataset.k === k; t.classList.toggle("on", on); t.setAttribute("aria-pressed", on ? "true" : "false"); });
    var box = document.querySelector(".tiers"); if (box) box.classList.toggle("dim", !!k);
  }
  rings.forEach(function(r){
    r.addEventListener("mouseenter", function(){ pick(r.dataset.k); });
    r.addEventListener("click", function(){ pick(r.dataset.k); });
  });
  tiers.forEach(function(t){
    t.addEventListener("mouseenter", function(){ pick(t.dataset.k); });
    t.addEventListener("focus", function(){ pick(t.dataset.k); });
    t.addEventListener("click", function(){ pick(t.dataset.k); });
  });
  var rw = document.querySelector(".rings-wrap"); if (rw) rw.addEventListener("mouseleave", function(){ pick(null); });

  // Карта отделений
  var map = document.querySelector(".map-svg");
  if (map) {
    var info = window.CITIES || {}, panel = document.getElementById("map-panel");
    var cities = map.querySelectorAll(".city"), arcs = map.querySelectorAll(".arc");
    function show(id){
      var c = info[id]; if (!c || !panel) return;
      cities.forEach(function(el){ el.classList.toggle("sel", el.dataset.id === id); });
      panel.querySelector("[data-f=eyebrow]").textContent = c.phase;
      panel.querySelector("[data-f=name]").textContent = c.name;
      panel.querySelector("[data-f=role]").textContent = c.role;
      panel.querySelector("[data-f=bridges]").textContent = c.bridges;
    }
    cities.forEach(function(el){
      el.addEventListener("click", function(){ show(el.dataset.id); });
      el.addEventListener("keydown", function(e){ if (e.key === "Enter" || e.key === " ") { e.preventDefault(); show(el.dataset.id); } });
    });
    document.querySelectorAll(".map-bar .chip").forEach(function(ch){
      ch.addEventListener("click", function(){
        document.querySelectorAll(".map-bar .chip").forEach(function(o){ o.setAttribute("aria-pressed", o === ch ? "true" : "false"); });
        var f = ch.dataset.f;
        cities.forEach(function(el){ el.classList.toggle("off", f !== "all" && el.dataset.ph !== f); });
        arcs.forEach(function(a){ a.classList.toggle("off", f !== "all" && a.dataset.ph !== f); });
      });
    });
    show("msk");
  }

  // Ритуал принятия кодекса
  var oath = document.querySelector(".oath");
  if (oath) {
    var rules = window.CODE || [], i = -1;
    var stage = oath.querySelector(".stage"), go = oath.querySelector("[data-act=go]"), pips = oath.querySelector(".pips");
    rules.forEach(function(){ pips.appendChild(document.createElement("i")); });
    var roman = ["I","II","III","IV","V","VI","VII","VIII","IX","X"];
    function render(){
      stage.classList.remove("swap"); void stage.offsetWidth; stage.classList.add("swap");
      pips.querySelectorAll("i").forEach(function(p, k){ p.classList.toggle("on", k <= i); });
      if (i < rules.length) {
        stage.innerHTML = '<span class="k">Правило ' + roman[i] + ' из X</span><h3></h3><p></p>';
        stage.querySelector("h3").textContent = rules[i][0];
        stage.querySelector("p").textContent = rules[i][1];
        go.textContent = i === rules.length - 1 ? "Даю слово" : "Принимаю";
      } else {
        stage.innerHTML = '<span class="k">Слово дано</span><h3>Так начинается каждый свой</h3><p>На настоящем принятии кодекс читают вслух перед кругом, а поручитель, привратник и хранитель отделения скрепляют слово рукопожатием.</p>';
        go.textContent = "Пройти ещё раз";
        oath.classList.add("done");
      }
    }
    go.addEventListener("click", function(){
      if (i >= rules.length) { i = -1; oath.classList.remove("done"); }
      i++; render();
    });
  }

  // Конверт с приглашением
  var env = document.querySelector(".env");
  if (env) {
    var wax = env.querySelector(".wax"), hint = document.querySelector(".env-cta");
    wax.addEventListener("click", function(){
      env.classList.add("open");
      if (hint) hint.textContent = "Печать сломана. Читайте письмо";
    });
  }

  // Путь участника: линия заполняется при прокрутке
  var path = document.querySelector(".path");
  if (path) {
    var fill = path.querySelector(".fill"), steps = path.querySelectorAll(".step");
    var tick = function(){
      var r = path.getBoundingClientRect(), mid = innerHeight * 0.6;
      var p = Math.max(0, Math.min(1, (mid - r.top) / r.height));
      fill.style.setProperty("--p", (p * 100).toFixed(1) + "%");
      steps.forEach(function(s){ s.classList.toggle("lit", s.getBoundingClientRect().top < mid); });
    };
    if (reduce) { fill.style.setProperty("--p", "100%"); steps.forEach(function(s){ s.classList.add("lit"); }); }
    else { addEventListener("scroll", tick, {passive: true}); addEventListener("resize", tick); tick(); }
  }
})();
