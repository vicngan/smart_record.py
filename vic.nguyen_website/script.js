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
const ambientPlayer = document.querySelector('.ambient-player');

const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
const storedTheme = localStorage.getItem('theme');
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const prefersFinePointer = window.matchMedia('(pointer: fine)');

if ('scrollRestoration' in history) {
  history.scrollRestoration = 'manual';
}

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

const navObservers = (() => {
  if (!navLinks.length) return null;

  const targets = Array.from(navLinks)
    .map((link) => {
      const id = link.getAttribute('href')?.replace('#', '');
      if (!id) return null;
      const section = document.getElementById(id);
      return section ? { link, section } : null;
    })
    .filter(Boolean);

  if (!targets.length) return null;

  let activeLink = null;
  const setActiveLink = (link) => {
    if (link === activeLink) return;
    navLinks.forEach((item) => item.removeAttribute('aria-current'));
    link.setAttribute('aria-current', 'page');
    activeLink = link;
  };

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const match = targets.find((target) => target.section === entry.target);
        if (match) {
          setActiveLink(match.link);
        }
      });
    },
    { threshold: 0.5 }
  );

  setActiveLink(targets[0].link);
  targets.forEach(({ section }) => observer.observe(section));
  return observer;
})();

const heroTilt = (() => {
  if (!heroSection || prefersReducedMotion.matches || !prefersFinePointer.matches) return null;
  const maxTilt = 6;
  const updateTilt = (event) => {
    const rect = heroSection.getBoundingClientRect();
    const normalizedX = (event.clientX - rect.left) / rect.width - 0.5;
    const normalizedY = (event.clientY - rect.top) / rect.height - 0.5;
    root.style.setProperty('--hero-tiltX', `${normalizedX * maxTilt}deg`);
    root.style.setProperty('--hero-tiltY', `${normalizedY * -maxTilt}deg`);
  };
  const resetTilt = () => {
    root.style.setProperty('--hero-tiltX', '0deg');
    root.style.setProperty('--hero-tiltY', '0deg');
  };
  heroSection.addEventListener('pointermove', updateTilt);
  heroSection.addEventListener('pointerleave', resetTilt);
  return { destroy: resetTilt };
})();

const initCarousels = () => {
  const carousels = document.querySelectorAll('[data-carousel]');
  if (!carousels.length) return;

  carousels.forEach((carousel) => {
    const track = carousel.querySelector('[data-carousel-track]');
    const prev = carousel.querySelector('[data-carousel-prev]');
    const next = carousel.querySelector('[data-carousel-next]');
    const dotsHost =
      carousel.nextElementSibling && carousel.nextElementSibling.matches('[data-carousel-dots]')
        ? carousel.nextElementSibling
        : null;

    if (!track) return;
    const cards = Array.from(track.children);
    if (!cards.length) return;

    let currentIndex = 0;
    let scrollRAF;

    const setDots = (index) => {
      if (!dotsHost) return;
      dotsHost.querySelectorAll('button').forEach((dot, idx) => {
        dot.setAttribute('aria-current', idx === index ? 'true' : 'false');
      });
    };

    if (dotsHost) {
      dotsHost.innerHTML = '';
      cards.forEach((_, idx) => {
        const dot = document.createElement('button');
        dot.type = 'button';
        dot.setAttribute('aria-label', `Jump to project ${idx + 1}`);
        dotsHost.appendChild(dot);
        dot.addEventListener('click', () => {
          scrollToIndex(idx);
        });
      });
    }

    const updateControls = () => {
      if (prev) prev.disabled = currentIndex === 0;
      if (next) next.disabled = currentIndex === cards.length - 1;
      setDots(currentIndex);
    };

    const scrollToIndex = (index, smooth = true) => {
      const clamped = Math.max(0, Math.min(index, cards.length - 1));
      const behavior = smooth ? 'smooth' : 'auto';
      const card = cards[clamped];
      const trackRect = track.getBoundingClientRect();
      const cardRect = card.getBoundingClientRect();
      const offsetWithinTrack = cardRect.left - trackRect.left;
      const target =
        offsetWithinTrack - track.clientWidth / 2 + card.clientWidth / 2 + track.scrollLeft;
      const clampedTarget = Math.max(
        0,
        Math.min(target, track.scrollWidth - track.clientWidth)
      );
      track.scrollTo({ left: clampedTarget, behavior });
      currentIndex = clamped;
      updateControls();
    };

    prev?.addEventListener('click', () => scrollToIndex(currentIndex - 1));
    next?.addEventListener('click', () => scrollToIndex(currentIndex + 1));

    track.addEventListener('scroll', () => {
      if (scrollRAF) cancelAnimationFrame(scrollRAF);
      scrollRAF = requestAnimationFrame(() => {
        const trackCenter = track.scrollLeft + track.clientWidth / 2;
        let nearestIndex = 0;
        let minDistance = Infinity;
        cards.forEach((card, idx) => {
          const cardCenter = card.offsetLeft + card.clientWidth / 2;
          const distance = Math.abs(cardCenter - trackCenter);
          if (distance < minDistance) {
            minDistance = distance;
            nearestIndex = idx;
          }
        });
        if (nearestIndex !== currentIndex) {
          currentIndex = nearestIndex;
          updateControls();
        }
      });
    });

    updateControls();
    scrollToIndex(0, false);
  });
};

initCarousels();

const updateSoundCaption = (playing) => {
  if (!soundCaption) return;
  soundCaption.textContent = playing
    ? 'Café ambience playing: gentle chatter, soft rain, lo-fi hum.'
    : 'Café ambience muted. Captions: gentle chatter, soft rain, subtle lo-fi.';
};

const setAmbientToggleState = (expanded) => {
  soundToggle?.setAttribute('aria-pressed', expanded ? 'true' : 'false');
  ambientPlayer?.classList.toggle('ambient-player--hidden', !expanded);
  updateSoundCaption(expanded);
};

const isAmbientExpanded = () => soundToggle?.getAttribute('aria-pressed') === 'true';

if (soundToggle) {
  setAmbientToggleState(isAmbientExpanded());
}

soundToggle?.addEventListener('click', async () => {
  const nextState = !isAmbientExpanded();
  if (cafeAudio) {
    try {
      if (nextState) {
        await cafeAudio.play();
      } else {
        cafeAudio.pause();
      }
    } catch (error) {
      console.error('Audio playback blocked', error);
    }
  }
  setAmbientToggleState(nextState);
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

const shouldSnapToHero = () => {
  const hash = window.location.hash;
  return !hash || hash === '#hero';
};

const snapHeroIntoView = () => {
  if (!shouldSnapToHero()) return;
  requestAnimationFrame(() => {
    window.scrollTo({ top: 0, behavior: 'auto' });
    if (window.location.hash !== '#hero') {
      history.replaceState(null, '', '#hero');
    }
  });
};

if (document.readyState === 'complete' || document.readyState === 'interactive') {
  snapHeroIntoView();
} else {
  window.addEventListener('DOMContentLoaded', snapHeroIntoView, { once: true });
}
window.addEventListener('load', snapHeroIntoView);
window.addEventListener('pageshow', (event) => {
  if (event.persisted) {
    snapHeroIntoView();
  }
});

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

contactForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!formStatus) return;

  const submitButton = contactForm.querySelector('button[type="submit"]');
  const formData = new FormData(contactForm);
  const payload = {
    name: formData.get('name'),
    email: formData.get('email'),
    message: formData.get('message'),
  };

  formStatus.textContent = 'Sending your note...';
  submitButton?.setAttribute('disabled', 'true');

  try {
    const response = await fetch('https://formsubmit.co/ajax/Vicngan@umich.edu', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Form submission failed with status ${response.status}`);
    }

    formStatus.textContent = `Thanks${payload.name ? `, ${payload.name}` : ''}! Your note is on its way.`;
    contactForm.reset();
  } catch (error) {
    console.error(error);
    formStatus.textContent = 'Hmm, something went wrong. Feel free to email me directly instead!';
  } finally {
    submitButton?.removeAttribute('disabled');
    setTimeout(() => {
      formStatus.textContent = '';
    }, 6000);
  }
});
