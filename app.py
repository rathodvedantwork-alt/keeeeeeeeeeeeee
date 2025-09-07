from flask import Flask, request, jsonify, render_template_string, redirect, url_for

app = Flask(__name__)

# --- Demo content (you can replace with DB/models later) ---
COMPANY = {
    "name": "NebulaStack Labs",
    "tagline": "We craft future-ready digital systems",
    "pillars": ["AI", "Cloud", "Data", "Security"],
}

SERVICES = [
    {
        "icon": "💡",
        "title": "AI Solutions",
        "desc": "Custom LLMs, RAG, vision models, and MLOps pipelines for real-world ROI.",
    },
    {
        "icon": "☁️",
        "title": "Cloud & DevOps",
        "desc": "Scalable infra on AWS/GCP/Azure, Kubernetes, observability, and CI/CD.",
    },
    {
        "icon": "🧱",
        "title": "Product Engineering",
        "desc": "SaaS apps, APIs, and microservices with high performance and quality.",
    },
    {
        "icon": "🛡️",
        "title": "Security Engineering",
        "desc": "AppSec, threat modeling, SAST/DAST, and compliance-ready architectures.",
    },
]

PROJECTS = [
    {
        "name": "Helios Analytics",
        "stack": ["Python", "FastAPI", "React", "Snowflake"],
        "summary": "Self-serve analytics with semantic layer and row-level security.",
        "img": "https://images.unsplash.com/photo-1551281044-8d8e145ed9f9?q=80&w=1600&auto=format&fit=crop",
        "link": "#",
    },
    {
        "name": "Orion EdgeAI",
        "stack": ["PyTorch", "ONNX", "Rust", "WebGPU"],
        "summary": "Edge inference runtime with sub-50ms latency on consumer devices.",
        "img": "https://images.unsplash.com/photo-1518779578993-ec3579fee39f?q=80&w=1600&auto=format&fit=crop",
        "link": "#",
    },
    {
        "name": "Nimbus DevOps",
        "stack": ["Terraform", "Kubernetes", "Grafana", "ArgoCD"],
        "summary": "Zero-downtime deploys and golden-path platform engineering.",
        "img": "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1600&auto=format&fit=crop",
        "link": "#",
    },
]

TESTIMONIALS = [
    {
        "quote": "NebulaStack rebuilt our data stack and doubled analytics velocity.",
        "author": "Anika Rao",
        "role": "CPO, QuantaPay",
    },
    {
        "quote": "From PoC to production in 10 weeks. Flawless execution.",
        "author": "Marcus Lee",
        "role": "CTO, FleetIQ",
    },
    {
        "quote": "Security by design. Passed audit in one go.",
        "author": "Sara Kim",
        "role": "Head of Risk, Meridia",
    },
]

MESSAGES = []  # in-memory demo store


def render_page(active="home"):
    return render_template_string(
        """
<!doctype html>
<html lang="en" x-data="ui()" :class="{ 'dark': dark }" class="scroll-smooth">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{{ company.name }} · {{ company.tagline }}</title>
  <!-- Tailwind via CDN for rapid prototyping -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: { display: ['Inter','ui-sans-serif','system-ui'] },
          animation: { 'spin-slow': 'spin 8s linear infinite' },
          boxShadow: {
            'glow': '0 0 80px rgba(99,102,241,0.35)',
            'inner-lg': 'inset 0 2px 20px rgba(255,255,255,0.06)'
          },
        }
      }
    }
  </script>
  <!-- Alpine.js for interactivity -->
  <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
  <!-- GSAP for buttery animations -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
  <meta name="color-scheme" content="dark light">
  <style>
    /* Subtle grain texture */
    .grain { position: relative; }
    .grain:before {
      content: ""; position: absolute; inset: 0; pointer-events:none;
      background-image: url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"160\" height=\"160\" viewBox=\"0 0 160 160\"><filter id=\"n\"><feTurbulence type=\"fractalNoise\" baseFrequency=\"0.65\" numOctaves=\"2\" stitchTiles=\"stitch\"/></filter><rect width=\"100%\" height=\"100%\" filter=\"url(%23n)\" opacity=\"0.035\"/></svg>');
      mix-blend-mode: overlay; opacity:.45;
    }
    /* Glassmorphism */
    .glass { backdrop-filter: blur(10px); background: rgba(255,255,255,.06); }
    .glass-dark { backdrop-filter: blur(10px); background: rgba(0,0,0,.25); }
  </style>
</head>
<body class="bg-zinc-50 dark:bg-[#0b0b12] text-zinc-900 dark:text-zinc-100 font-display grain">
  <!-- Floating gradient blobs -->
  <div class="fixed -z-10 inset-0 overflow-hidden">
    <div class="absolute -top-40 -left-32 h-96 w-96 rounded-full bg-gradient-to-tr from-indigo-500 to-fuchsia-500 opacity-30 blur-3xl animate-pulse"></div>
    <div class="absolute -bottom-40 -right-20 h-[28rem] w-[28rem] rounded-full bg-gradient-to-tr from-sky-500 to-emerald-500 opacity-30 blur-3xl animate-pulse"></div>
  </div>

  <!-- Nav -->
  <header class="sticky top-0 z-50">
    <div class="mx-auto max-w-7xl px-4 py-3 flex items-center justify-between">
      <a href="#home" class="flex items-center gap-2">
        <div class="h-9 w-9 rounded-2xl bg-gradient-to-tr from-indigo-500 to-fuchsia-500 shadow-glow grid place-items-center text-white">NS</div>
        <span class="font-semibold tracking-wide">{{ company.name }}</span>
      </a>
      <nav class="hidden md:flex items-center gap-6 text-sm">
        <a href="#services" class="hover:opacity-80">Services</a>
        <a href="#work" class="hover:opacity-80">Work</a>
        <a href="#testimonials" class="hover:opacity-80">Love</a>
        <a href="#contact" class="hover:opacity-80">Contact</a>
      </nav>
      <div class="flex items-center gap-2">
        <button @click="toggleTheme" class="px-3 py-2 rounded-xl glass dark:glass-dark border border-white/10">
          <span x-show="!dark">🌙</span><span x-show="dark">☀️</span>
        </button>
        <a href="#contact" class="hidden sm:inline-flex px-4 py-2 rounded-xl bg-zinc-900 text-white dark:bg-white dark:text-zinc-900 hover:opacity-90">Get a quote</a>
      </div>
    </div>
  </header>

  <!-- Hero -->
  <section id="home" class="relative">
    <div class="max-w-7xl mx-auto px-4 py-24 md:py-32 grid md:grid-cols-2 gap-10 items-center">
      <div>
        <h1 class="text-4xl md:text-6xl font-extrabold leading-tight">
          {{ company.tagline }}<br>
          <span class="bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-fuchsia-500">for ambitious teams</span>
        </h1>
        <p class="mt-6 text-lg/7 text-zinc-600 dark:text-zinc-300 max-w-xl">
          We ship world-class software with daring design, measurable outcomes, and security-first engineering.
        </p>
        <div class="mt-8 flex gap-3">
          <a href="#work" class="px-5 py-3 rounded-xl bg-indigo-600 text-white hover:opacity-90 shadow-lg">See our work</a>
          <a href="#services" class="px-5 py-3 rounded-xl border border-zinc-200 dark:border-white/10 hover:bg-white/5">Explore services</a>
        </div>
        <div class="mt-10 flex items-center gap-4 text-sm text-zinc-500 dark:text-zinc-400">
          <span class="inline-flex items-center gap-2"><span class="h-2 w-2 rounded-full bg-emerald-400 animate-ping"></span> 99.9% uptime</span>
          <span>ISO 27001-ready</span>
          <span>Trusted by 40+ orgs</span>
        </div>
      </div>
      <div class="relative">
        <div class="aspect-[4/3] rounded-3xl border border-white/10 glass dark:glass-dark shadow-2xl p-6">
          <div class="grid grid-cols-2 gap-4 h-full">
            <div class="rounded-2xl bg-gradient-to-br from-indigo-500/30 to-fuchsia-500/30 border border-white/10 p-4">
              <p class="text-sm">LLM Ops Pipeline</p>
              <div class="mt-6 h-24 rounded-xl bg-black/60 text-emerald-300 p-3 font-mono text-xs overflow-auto">$ make deploy\n✓ build\n✓ tests\n✓ push image\n✓ rollout</div>
            </div>
            <div class="rounded-2xl bg-gradient-to-br from-emerald-500/30 to-sky-500/30 border border-white/10 p-4">
              <p class="text-sm">K8s Cluster</p>
              <div class="mt-6 h-24 rounded-xl bg-black/60 text-sky-300 p-3 font-mono text-xs overflow-auto">apiVersion: v1\nkind: Service\nmetadata:\n  name: api\nspec:\n  type: ClusterIP</div>
            </div>
            <div class="col-span-2 rounded-2xl bg-gradient-to-br from-zinc-900/60 to-zinc-800/60 border border-white/10 p-4 flex items-center justify-between">
              <div>
                <p class="text-sm text-zinc-400">Delivery Speed</p>
                <p class="text-3xl font-bold">10x</p>
              </div>
              <div class="h-16 w-16 rounded-full border border-white/10 grid place-items-center animate-spin-slow">⚙️</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Services -->
  <section id="services" class="py-20">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex items-end justify-between">
        <h2 class="text-3xl md:text-4xl font-bold">What we do</h2>
        <div class="text-sm text-zinc-500 dark:text-zinc-400">Strategy → Build → Scale</div>
      </div>
      <div class="mt-10 grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {% for s in services %}
        <div class="group rounded-2xl p-6 border border-zinc-200 dark:border-white/10 glass dark:glass-dark hover:shadow-glow transition">
          <div class="text-3xl">{{ s.icon }}</div>
          <h3 class="mt-4 text-xl font-semibold">{{ s.title }}</h3>
          <p class="mt-2 text-sm text-zinc-600 dark:text-zinc-300">{{ s.desc }}</p>
          <a href="#contact" class="mt-6 inline-flex items-center gap-2 text-indigo-500">Start a project →</a>
        </div>
        {% endfor %}
      </div>
    </div>
  </section>

  <!-- Work / Projects -->
  <section id="work" class="py-20">
    <div class="max-w-7xl mx-auto px-4">
      <h2 class="text-3xl md:text-4xl font-bold">Selected work</h2>
      <div class="mt-10 grid md:grid-cols-3 gap-6">
        {% for p in projects %}
        <a href="{{ p.link }}" class="group block rounded-2xl overflow-hidden border border-white/10 bg-white/5">
          <div class="relative">
            <img src="{{ p.img }}" alt="{{ p.name }}" class="h-52 w-full object-cover group-hover:scale-105 transition" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
          </div>
          <div class="p-5">
            <div class="text-sm text-zinc-400">{{ p.stack|join(', ') }}</div>
            <div class="mt-1 text-xl font-semibold">{{ p.name }}</div>
            <p class="mt-2 text-sm text-zinc-300">{{ p.summary }}</p>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>
  </section>

  <!-- Testimonials (scroll-snap carousel) -->
  <section id="testimonials" class="py-20">
    <div class="max-w-6xl mx-auto px-4">
      <h2 class="text-3xl md:text-4xl font-bold">Clients love us</h2>
      <div class="mt-8 overflow-x-auto snap-x snap-mandatory flex gap-6 pb-6">
        {% for t in testimonials %}
        <div class="min-w-[22rem] md:min-w-[28rem] snap-center rounded-2xl p-6 border border-white/10 glass dark:glass-dark">
          <p class="text-lg">“{{ t.quote }}”</p>
          <div class="mt-4 text-sm text-zinc-400">— {{ t.author }}, {{ t.role }}</div>
        </div>
        {% endfor %}
      </div>
    </div>
  </section>

  <!-- CTA / Badges -->
  <section class="py-16">
    <div class="max-w-7xl mx-auto px-4">
      <div class="rounded-3xl border border-white/10 p-8 md:p-12 glass dark:glass-dark grid md:grid-cols-2 gap-6 items-center">
        <div>
          <h3 class="text-2xl md:text-3xl font-bold">Build with a partner who ships.</h3>
          <p class="mt-2 text-zinc-400">We obsess over outcomes, not vanity metrics. Let's align on impact.</p>
        </div>
        <div class="flex flex-wrap gap-3 justify-end">
          {% for p in company.pillars %}
          <span class="px-4 py-2 rounded-full border border-white/10 bg-white/5">{{ p }}</span>
          {% endfor %}
        </div>
      </div>
    </div>
  </section>

  <!-- Contact -->
  <section id="contact" class="py-20">
    <div class="max-w-4xl mx-auto px-4">
      <h2 class="text-3xl md:text-4xl font-bold">Tell us about your project</h2>
      <form method="post" action="{{ url_for('contact') }}" class="mt-8 grid md:grid-cols-2 gap-4">
        <input required name="name" placeholder="Your name" class="px-4 py-3 rounded-xl border border-white/10 bg-white/5 outline-none focus:ring-2 focus:ring-indigo-500" />
        <input required type="email" name="email" placeholder="Email" class="px-4 py-3 rounded-xl border border-white/10 bg-white/5 outline-none focus:ring-2 focus:ring-indigo-500" />
        <input name="company" placeholder="Company (optional)" class="md:col-span-2 px-4 py-3 rounded-xl border border-white/10 bg-white/5 outline-none focus:ring-2 focus:ring-indigo-500" />
        <textarea required name="message" rows="4" placeholder="What are you building?" class="md:col-span-2 px-4 py-3 rounded-xl border border-white/10 bg-white/5 outline-none focus:ring-2 focus:ring-indigo-500"></textarea>
        <button class="md:col-span-2 px-5 py-3 rounded-xl bg-indigo-600 text-white hover:opacity-90">Send message</button>
      </form>

      {% if messages %}
      <div class="mt-8">
        <h3 class="text-xl font-semibold">Recent inquiries (demo)</h3>
        <ul class="mt-3 space-y-2 text-sm text-zinc-400">
          {% for m in messages[-5:]|reverse %}
          <li class="rounded-xl border border-white/10 p-4 glass dark:glass-dark">
            <div class="font-medium text-zinc-200">{{ m.name }} · {{ m.email }} {% if m.company %}· {{ m.company }}{% endif %}</div>
            <div class="mt-1">{{ m.message }}</div>
          </li>
          {% endfor %}
        </ul>
      </div>
      {% endif %}
    </div>
  </section>

  <!-- Footer -->
  <footer class="py-10 border-t border-white/10">
    <div class="max-w-7xl mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="h-8 w-8 rounded-xl bg-gradient-to-tr from-indigo-500 to-fuchsia-500 grid place-items-center text-white">NS</div>
        <div class="text-sm">© {{ company.name }} · All rights reserved</div>
      </div>
      <div class="text-sm text-zinc-500">Made with Python · Flask · Tailwind</div>
    </div>
  </footer>

  <script>
    // Alpine state for theme
    function ui(){
      return {
        dark: localStorage.getItem('theme') === 'dark' || window.matchMedia('(prefers-color-scheme: dark)').matches,
        toggleTheme(){ this.dark = !this.dark; localStorage.setItem('theme', this.dark ? 'dark' : 'light'); }
      }
    }

    // GSAP reveal animations
    document.addEventListener('DOMContentLoaded', () => {
      gsap.registerPlugin(ScrollTrigger);
      gsap.utils.toArray('#services .group').forEach((card, i) => {
        gsap.from(card, { y: 24, opacity: 0, duration: .6, delay: i * 0.08, scrollTrigger: { trigger: card, start: 'top 85%' }})
      })
      gsap.from('#work h2', { y: 20, opacity: 0, duration: .6, scrollTrigger: { trigger: '#work', start: 'top 80%' }})
      gsap.utils.toArray('#work a').forEach((it, i) => {
        gsap.from(it, { y: 28, opacity: 0, duration: .6, delay: i * 0.06, scrollTrigger: { trigger: it, start: 'top 85%' }})
      })
    })
  </script>
</body>
</html>
        """,
        company=COMPANY,
        services=SERVICES,
        projects=PROJECTS,
        testimonials=TESTIMONIALS,
        messages=MESSAGES,
        active=active,
    )


@app.get("/")
def home():
    return render_page("home")


@app.post("/contact")
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    company = request.form.get("company", "").strip()
    message = request.form.get("message", "").strip()

    if not (name and email and message):
        return redirect(url_for('home') + '#contact')

    MESSAGES.append({
        "name": name,
        "email": email,
        "company": company,
        "message": message,
    })
    return redirect(url_for('home') + '#contact')


if __name__ == "__main__":
    # Run the app
    app.run(debug=True, host="0.0.0.0", port=5000)

