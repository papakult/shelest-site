/* Общий JS SEO-посадочных (build_seo.py): FAQ, шапка, бургер, RU/EN для шапки и футера, сохранённая тема. */
(function(){
  try{
    var t = localStorage.getItem('sh-theme') || 'gold', f = localStorage.getItem('sh-font') || 'serif';
    document.documentElement.setAttribute('data-theme', t);
    document.documentElement.setAttribute('data-font', f);
  }catch(e){}
  document.querySelectorAll('.faq__q').forEach(function(btn){
    btn.addEventListener('click', function(){
      var item = btn.closest('.faq__item');
      var open = item.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  var yr = document.getElementById('yr'); if (yr) yr.textContent = new Date().getFullYear();
  var hdr = document.getElementById('hdr');
  window.addEventListener('scroll', function(){ if (hdr) hdr.classList.toggle('is-scrolled', window.scrollY > 10); }, {passive:true});
  var btn = document.getElementById('burgerBtn'), nav = document.querySelector('.hdr__nav');
  if (btn && nav){
    btn.addEventListener('click', function(){ var o = nav.classList.toggle('is-open'); btn.classList.toggle('is-open', o); });
    nav.querySelectorAll(':scope > a').forEach(function(a){ a.addEventListener('click', function(){ nav.classList.remove('is-open'); btn.classList.remove('is-open'); }); });
    nav.querySelectorAll('.hdr__drop').forEach(function(drop){
      var l = drop.querySelector(':scope > a');
      l.addEventListener('click', function(e){ if (window.innerWidth <= 860){ e.preventDefault(); drop.classList.toggle('is-open'); } });
    });
  }
  var EN = {'nav.about':'About','nav.pricing':'Pricing','nav.services':'Services','nav.reviews':'Reviews','nav.contact':'Contact','nav.cta':'Book a call',
    'nav.articles':'Articles','nav.enc':'Encyclopedias','nav.enc.sn':'Sport nutrition','nav.enc.sn.d':'AIS ABCD supplement ratings',
    'nav.enc.di':'Dietology','nav.enc.di.d':'5 evidence-based diets compared','nav.enc.mb':'Gut microbiome','nav.enc.mb.d':'History, sport, testing, myths',
    'ftr.bio':'World Champion, degree in human ecology, competing athlete. Online coaching across Russia.','ftr.pay':'Payment arranged via Telegram',
    'ftr.link1':'Sport nutrition','ftr.link2':'Dietology','ftr.link3':'Gut microbiome'};
  var RU = {}; document.querySelectorAll('[data-i18n]').forEach(function(el){ RU[el.getAttribute('data-i18n')] = el.innerHTML; });
  var lang = 'ru', lb = document.getElementById('langBtn');
  if (lb) lb.addEventListener('click', function(){
    lang = lang === 'ru' ? 'en' : 'ru';
    lb.textContent = lang === 'ru' ? 'EN' : 'RU';
    var d = lang === 'ru' ? RU : EN;
    document.querySelectorAll('[data-i18n]').forEach(function(el){ var k = el.getAttribute('data-i18n'); if (d[k] !== undefined) el.innerHTML = d[k]; });
  });
})();
