/* ============================================
   MAGAR — JavaScript funcional
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* --- Hero testimonial carousel --- */
  const heroTestis = document.querySelectorAll('.hero-testi');
  const htDots = document.querySelectorAll('.htdot');
  let htCurrent = 0;
  if (heroTestis.length) {
    const showTesti = (i) => {
      heroTestis[htCurrent].classList.remove('active');
      htDots[htCurrent].classList.remove('active');
      htCurrent = i % heroTestis.length;
      heroTestis[htCurrent].classList.add('active');
      htDots[htCurrent].classList.add('active');
    };
    htDots.forEach((dot, i) => dot.addEventListener('click', () => showTesti(i)));
    setInterval(() => showTesti(htCurrent + 1), 4000);
  }

  /* --- Navbar scroll --- */
  const navbar = document.getElementById('navbar');
  const onScroll = () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* --- Hamburger --- */
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('navLinks');
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navLinks.classList.toggle('active');
    document.body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
  });
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('active');
      navLinks.classList.remove('active');
      document.body.style.overflow = '';
    });
  });

  /* --- Matrices tooltip --- */
  const matricesBox = document.getElementById('matricesBox');
  const openMatrices = (e) => {
    e.preventDefault();
    matricesBox.classList.add('visible');
    matricesBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };
  document.getElementById('matricesBtn').addEventListener('click', openMatrices);
  document.getElementById('matricesBtn2').addEventListener('click', openMatrices);
  document.getElementById('matricesBtn3').addEventListener('click', openMatrices);
  document.getElementById('matricesClose').addEventListener('click', () => {
    matricesBox.classList.remove('visible');
  });

  /* --- File upload --- */
  const fileInput = document.getElementById('archivo');
  const fileDrop = document.getElementById('fileDrop');
  const fileName = document.getElementById('fileName');

  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
      const file = fileInput.files[0];
      const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
      fileName.textContent = `${file.name} (${sizeMB} MB)`;
    } else {
      fileName.textContent = '';
    }
  });

  // Drag & drop
  ['dragenter', 'dragover'].forEach(evt => {
    fileDrop.addEventListener(evt, (e) => {
      e.preventDefault();
      fileDrop.style.borderColor = '#c8a45e';
      fileDrop.style.background = 'rgba(200,164,94,.08)';
    });
  });
  ['dragleave', 'drop'].forEach(evt => {
    fileDrop.addEventListener(evt, (e) => {
      e.preventDefault();
      fileDrop.style.borderColor = '';
      fileDrop.style.background = '';
    });
  });
  fileDrop.addEventListener('drop', (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const ext = files[0].name.split('.').pop().toLowerCase();
      if (ext === 'doc' || ext === 'docx') {
        fileInput.files = files;
        fileInput.dispatchEvent(new Event('change'));
      } else {
        fileName.textContent = 'Solo se aceptan archivos .doc o .docx';
        fileName.style.color = '#ef5350';
        setTimeout(() => { fileName.textContent = ''; fileName.style.color = ''; }, 3000);
      }
    }
  });

  /* --- Form validation & submit --- */
  const form = document.getElementById('contactForm');
  const submitBtn = document.getElementById('submitBtn');
  const formSuccess = document.getElementById('formSuccess');

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    // Basic validation
    const nombre = form.nombre.value.trim();
    const email = form.email.value.trim();
    const servicio = form.servicio.value;
    const mensaje = form.mensaje.value.trim();
    const privacidad = form.privacidad.checked;

    // Reset styles
    form.querySelectorAll('input, select, textarea').forEach(el => {
      el.style.borderColor = '';
    });

    let valid = true;
    const markInvalid = (el) => {
      el.style.borderColor = '#ef5350';
      valid = false;
    };

    if (!nombre) markInvalid(form.nombre);
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) markInvalid(form.email);
    if (!servicio) markInvalid(form.servicio);
    if (!mensaje) markInvalid(form.mensaje);
    if (!privacidad) {
      form.privacidad.parentElement.style.color = '#ef5350';
      valid = false;
    }

    if (!valid) return;

    // Simulate submission
    submitBtn.disabled = true;
    submitBtn.textContent = 'Enviando...';

    setTimeout(() => {
      submitBtn.textContent = 'Enviar solicitud';
      submitBtn.disabled = false;
      formSuccess.classList.add('visible');
      form.reset();
      fileName.textContent = '';

      setTimeout(() => { formSuccess.classList.remove('visible'); }, 6000);
    }, 1500);
  });

  /* --- Smooth reveal on scroll (IntersectionObserver) --- */
  const revealEls = document.querySelectorAll(
    '.service-card, .step, .course-card, .novel-card, .blog-card, .blog-featured-main, .blog-featured-small, .about-content, .about-image, .contact-info, .contact-form'
  );

  const revealStyle = document.createElement('style');
  revealStyle.textContent = `
    .reveal-hidden { opacity: 0; transform: translateY(32px); }
    .reveal-visible { opacity: 1; transform: translateY(0); transition: opacity .6s ease, transform .6s ease; }
  `;
  document.head.appendChild(revealStyle);

  revealEls.forEach((el, i) => {
    el.classList.add('reveal-hidden');
    el.style.transitionDelay = `${(i % 4) * .1}s`;
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.remove('reveal-hidden');
        entry.target.classList.add('reveal-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: .15, rootMargin: '0px 0px -40px 0px' });

  revealEls.forEach(el => observer.observe(el));

  /* --- Active nav link on scroll --- */
  const sections = document.querySelectorAll('section[id]');
  const navItems = document.querySelectorAll('.nav-links a:not(.nav-cta)');

  const highlightNav = () => {
    const scrollY = window.scrollY + 100;
    sections.forEach(section => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');
      if (scrollY >= top && scrollY < top + height) {
        navItems.forEach(a => {
          a.style.color = '';
          if (a.getAttribute('href') === '#' + id) {
            a.style.color = '#1a1d2e';
          }
        });
      }
    });
  };
  window.addEventListener('scroll', highlightNav, { passive: true });

});
