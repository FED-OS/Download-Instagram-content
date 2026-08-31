/* ============================================
   FED-GRAM Promotional Landing Page
   JavaScript
   ============================================ */

(function () {
    'use strict';

    /* ---------- Platform Data ---------- */
    const platforms = [
        { name: 'Instagram', icon: '📸', engine: 'instagram_engine' },
        { name: 'Threads', icon: '🧵', engine: 'instagram_engine' },
        { name: 'TikTok', icon: '🎵', engine: 'ytdlp_engine' },
        { name: 'YouTube', icon: '▶️', engine: 'ytdlp_engine' },
        { name: 'Reddit', icon: '🤖', engine: 'ytdlp_engine' },
        { name: 'Twitter / X', icon: '🐦', engine: 'ytdlp_engine' },
        { name: 'Facebook', icon: '👍', engine: 'ytdlp_engine' },
        { name: 'Pinterest', icon: '📌', engine: 'pinterest_engine' },
        { name: 'Twitch', icon: '🎮', engine: 'ytdlp_engine' },
        { name: 'Vimeo', icon: '🎬', engine: 'ytdlp_engine' },
        { name: 'Dailymotion', icon: '📡', engine: 'ytdlp_engine' },
        { name: 'SoundCloud', icon: '☁️', engine: 'ytdlp_engine' },
        { name: 'Imgur', icon: '🖼️', engine: 'imgur_engine' },
        { name: 'Bluesky', icon: '☁️', engine: 'generic_engine' },
        { name: 'Tumblr', icon: '✏️', engine: 'tumblr_engine' },
        { name: 'Snapchat', icon: '👻', engine: 'ytdlp_engine' },
        { name: 'LinkedIn', icon: '💼', engine: 'generic_engine' },
        { name: 'Streamable', icon: '🎥', engine: 'ytdlp_engine' },
    ];

    /* ---------- Build Platform Grid ---------- */
    function buildPlatformGrid() {
        const grid = document.getElementById('platformGrid');
        if (!grid) return;

        platforms.forEach(function (pf) {
            const tile = document.createElement('div');
            tile.className = 'platform-tile';
            tile.innerHTML =
                '<span class="pf-emoji">' + pf.icon + '</span>' +
                '<span class="pf-name">' + pf.name + '</span>';
            grid.appendChild(tile);
        });

        // Add fallback tile
        const fallback = document.createElement('div');
        fallback.className = 'platform-tile fallback';
        fallback.innerHTML =
            '<span class="pf-emoji">🌐</span>' +
            '<span class="pf-name">+ Any URL</span>';
        grid.appendChild(fallback);
    }

    /* ---------- Build Marquee ---------- */
    function buildMarquee() {
        const track = document.getElementById('marqueeTrack');
        if (!track) return;

        // Duplicate the list for seamless infinite scroll
        const items = platforms.concat(platforms);

        items.forEach(function (pf) {
            const item = document.createElement('div');
            item.className = 'marquee-item';
            item.innerHTML =
                '<span class="pf-icon">' + pf.icon + '</span>' +
                '<span>' + pf.name + '</span>';
            track.appendChild(item);
        });
    }

    /* ---------- Navbar Scroll Effect ---------- */
    function initNavbarScroll() {
        const navbar = document.getElementById('navbar');
        if (!navbar) return;

        let lastScroll = 0;

        window.addEventListener('scroll', function () {
            const currentScroll = window.scrollY;

            if (currentScroll > 60) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }

            lastScroll = currentScroll;
        }, { passive: true });
    }

    /* ---------- Mobile Menu Toggle ---------- */
    function initMobileMenu() {
        const toggle = document.getElementById('mobileToggle');
        const links = document.getElementById('navLinks');

        if (!toggle || !links) return;

        toggle.addEventListener('click', function () {
            links.classList.toggle('mobile-open');
        });

        // Close menu when a link is clicked
        links.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                links.classList.remove('mobile-open');
            });
        });
    }

    /* ---------- Code Tab Switching ---------- */
    function initCodeTabs() {
        const tabs = document.querySelectorAll('.code-tab');
        const blocks = document.querySelectorAll('.code-block');

        tabs.forEach(function (tab) {
            tab.addEventListener('click', function () {
                const target = tab.getAttribute('data-tab');

                tabs.forEach(function (t) { t.classList.remove('active'); });
                blocks.forEach(function (b) { b.classList.remove('active'); });

                tab.classList.add('active');
                const block = document.getElementById('tab-' + target);
                if (block) block.classList.add('active');
            });
        });
    }

    /* ---------- Copy Code ---------- */
    window.copyCode = function (blockId) {
        const block = document.getElementById(blockId);
        if (!block) return;

        // Get text content excluding the copy button text
        const clone = block.cloneNode(true);
        const btn = clone.querySelector('.copy-btn');
        if (btn) btn.remove();

        const text = clone.textContent.trim();

        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(function () {
                showCopyFeedback(blockId);
            }).catch(function () {
                fallbackCopy(text);
                showCopyFeedback(blockId);
            });
        } else {
            fallbackCopy(text);
            showCopyFeedback(blockId);
        }
    };

    function fallbackCopy(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
        } catch (e) {
            // ignore
        }
        document.body.removeChild(textarea);
    }

    function showCopyFeedback(blockId) {
        const block = document.getElementById(blockId);
        if (!block) return;
        const btn = block.querySelector('.copy-btn');
        if (!btn) return;

        const original = btn.textContent;
        btn.textContent = '✅ Copied!';
        btn.style.color = '#4ade80';

        setTimeout(function () {
            btn.textContent = original;
            btn.style.color = '';
        }, 2000);
    }

    /* ---------- FAQ Toggle ---------- */
    window.toggleFaq = function (element) {
        const item = element.parentElement;
        const wasActive = item.classList.contains('active');

        // Close all FAQ items
        document.querySelectorAll('.faq-item').forEach(function (faq) {
            faq.classList.remove('active');
        });

        // Reopen this one if it was previously closed
        if (!wasActive) {
            item.classList.add('active');
        }
    };

    /* ---------- Scroll Reveal ---------- */
    function initScrollReveal() {
        const elements = document.querySelectorAll('.reveal');

        if (!('IntersectionObserver' in window)) {
            // Fallback: show everything
            elements.forEach(function (el) {
                el.classList.add('visible');
            });
            return;
        }

        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -60px 0px'
        });

        elements.forEach(function (el) {
            observer.observe(el);
        });
    }

    /* ---------- Animated Counters ---------- */
    function animateCounter(element) {
        const target = parseInt(element.getAttribute('data-target'), 10);
        const suffix = element.getAttribute('data-suffix') || '';
        const duration = 1800;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Ease out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.round(eased * target);

            element.textContent = current + suffix;

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                element.textContent = target + suffix;
            }
        }

        requestAnimationFrame(update);
    }

    function initCounters() {
        const counters = document.querySelectorAll('.stat-number');
        if (counters.length === 0) return;

        if (!('IntersectionObserver' in window)) {
            counters.forEach(animateCounter);
            return;
        }

        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(function (counter) {
            observer.observe(counter);
        });
    }

    /* ---------- Smooth Scroll for Anchor Links ---------- */
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
            anchor.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                if (href === '#' || href.length < 2) return;

                const target = document.querySelector(href);
                if (!target) return;

                e.preventDefault();
                const offset = 80; // navbar height
                const top = target.getBoundingClientRect().top + window.scrollY - offset;

                window.scrollTo({
                    top: top,
                    behavior: 'smooth'
                });
            });
        });
    }

    /* ---------- Typing Animation for Demo Input ---------- */
    function initDemoTyping() {
        const demoInput = document.querySelector('.demo-input');
        if (!demoInput) return;

        const typedSpan = demoInput.querySelector('.demo-typed');
        if (!typedSpan) return;

        const fullText = 'https://www.instagram.com/p/CxYzAbC1234/';
        let index = 0;
        let hasTyped = false;

        function typeNext() {
            if (index < fullText.length) {
                typedSpan.textContent = fullText.substring(0, index + 1);
                index++;
                setTimeout(typeNext, 60 + Math.random() * 40);
            }
        }

        // Start typing when the demo section comes into view
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting && !hasTyped) {
                        hasTyped = true;
                        setTimeout(typeNext, 500);
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.3 });

            observer.observe(demoInput);
        } else {
            typedSpan.textContent = fullText;
        }
    }

    /* ---------- Demo Media Card Stagger Animation ---------- */
    function initDemoCards() {
        const cards = document.querySelectorAll('.demo-media-card');
        if (cards.length === 0) return;

        cards.forEach(function (card, index) {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        });

        if (!('IntersectionObserver' in window)) {
            cards.forEach(function (card) {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            });
            return;
        }

        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    cards.forEach(function (card, index) {
                        setTimeout(function () {
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, index * 150);
                    });
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });

        observer.observe(document.querySelector('.demo-window'));
    }

    /* ---------- Active Nav Link on Scroll ---------- */
    function initActiveNavLink() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');

        if (sections.length === 0 || navLinks.length === 0) return;

        function updateActive() {
            const scrollPos = window.scrollY + 100;

            sections.forEach(function (section) {
                const top = section.offsetTop;
                const height = section.offsetHeight;
                const id = section.getAttribute('id');

                if (scrollPos >= top && scrollPos < top + height) {
                    navLinks.forEach(function (link) {
                        const href = link.getAttribute('href');
                        if (href === '#' + id) {
                            link.style.color = 'var(--text-primary)';
                        } else if (!link.classList.contains('nav-cta')) {
                            link.style.color = '';
                        }
                    });
                }
            });
        }

        window.addEventListener('scroll', updateActive, { passive: true });
    }

    /* ---------- Initialize Everything ---------- */
    function init() {
        buildPlatformGrid();
        buildMarquee();
        initNavbarScroll();
        initMobileMenu();
        initCodeTabs();
        initScrollReveal();
        initCounters();
        initSmoothScroll();
        initDemoTyping();
        initDemoCards();
        initActiveNavLink();
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
