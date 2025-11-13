const root = document.documentElement;
const themeToggle = document.querySelector('.toggle-theme');
const sections = document.querySelectorAll('.section, .card, .timeline-card, .small-card');
const navLinks = document.querySelectorAll('.site-nav a[href^="#"]');
const modals = document.querySelectorAll('.modal');
const modalTriggers = document.querySelectorAll('[data-modal]');
const contactForm = document.querySelector('[data-form]');
const formStatus = document.querySelector('.form-status');
const soundToggle = document.querySelector('[data-sound-toggle]');
const soundCaption = document.getElementById('sound-caption');
const cafeAudio = document.getElementById('cafe-audio');
const particlesCanvas = document.getElementById('matcha-particles');
const heroSection = document.getElementById('hero');

const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
const storedTheme = localStorage.getItem('theme');
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

const setTheme = (mode) => {
  root.setAttribute('data-theme', mode);
  localStorage.setItem('theme', mode);
};

if (storedTheme) {
  setTheme(storedTheme);
} else if (prefersDark.matches) {
  setTheme('dark');
}

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const isDark = root.getAttribute('data-theme') === 'dark';
    setTheme(isDark ? 'light' : 'dark');
  });
}

navLinks.forEach((link) => {
  link.addEventListener('click', (event) => {
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      event.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

const updateSoundCaption = (playing) => {
  if (!soundCaption) return;
  soundCaption.textContent = playing
    ? 'Café ambience playing: gentle chatter, soft rain, lo-fi hum.'
    : 'Café ambience muted. Captions: gentle chatter, soft rain, subtle lo-fi.';
};

soundToggle?.addEventListener('click', async () => {
  if (!cafeAudio) return;
  try {
    if (cafeAudio.paused) {
      await cafeAudio.play();
      soundToggle.setAttribute('aria-pressed', 'true');
      updateSoundCaption(true);
    } else {
      cafeAudio.pause();
      soundToggle.setAttribute('aria-pressed', 'false');
      updateSoundCaption(false);
    }
  } catch (error) {
    console.error('Audio playback blocked', error);
  }
});

const initParticles = () => {
  if (!particlesCanvas || !heroSection || prefersReducedMotion.matches) return;
  const ctx = particlesCanvas.getContext('2d');
  const particles = [];
  const particleCount = 28;

  const resize = () => {
    particlesCanvas.width = heroSection.clientWidth;
    particlesCanvas.height = heroSection.clientHeight;
  };

  const createParticles = () => {
    particles.length = 0;
    for (let i = 0; i < particleCount; i += 1) {
      particles.push({
        x: Math.random() * particlesCanvas.width,
        y: Math.random() * particlesCanvas.height,
        radius: Math.random() * 2 + 0.5,
        speed: Math.random() * 0.4 + 0.1,
        alpha: Math.random() * 0.5 + 0.2,
      });
    }
  };

  const draw = () => {
    ctx.clearRect(0, 0, particlesCanvas.width, particlesCanvas.height);
    particles.forEach((particle) => {
      ctx.beginPath();
      ctx.fillStyle = `rgba(168, 214, 109, ${particle.alpha})`;
      ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      ctx.fill();
      particle.y -= particle.speed;
      if (particle.y < -10) {
        particle.y = particlesCanvas.height + 10;
        particle.x = Math.random() * particlesCanvas.width;
      }
    });
    requestAnimationFrame(draw);
  };

  resize();
  createParticles();
  draw();
  window.addEventListener('resize', () => {
    resize();
    createParticles();
  });
};

initParticles();

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.15, rootMargin: '0px 0px -50px 0px' }
);

sections.forEach((section) => {
  section.classList.add('reveal');
  observer.observe(section);
});

modalTriggers.forEach((button) => {
  const modalId = button.getAttribute('data-modal');
  const modal = document.getElementById(modalId);
  if (!modal) return;
  button.addEventListener('click', () => {
    modal.setAttribute('data-open', 'true');
    modal.setAttribute('aria-hidden', 'false');
  });
});

modals.forEach((modal) => {
  const closeBtn = modal.querySelector('[data-close]');
  const closeModal = () => {
    modal.removeAttribute('data-open');
    modal.setAttribute('aria-hidden', 'true');
  };
  closeBtn?.addEventListener('click', closeModal);
  modal.addEventListener('click', (event) => {
    if (event.target === modal) {
      closeModal();
    }
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && modal.getAttribute('data-open') === 'true') {
      closeModal();
    }
  });
});

contactForm?.addEventListener('submit', (event) => {
  event.preventDefault();
  const formData = new FormData(contactForm);
  const name = formData.get('name');

  formStatus.textContent = `Thanks${name ? `, ${name}` : ''}! Your note is on its way.`;
  contactForm.reset();
  setTimeout(() => {
    formStatus.textContent = '';
  }, 4000);
});
