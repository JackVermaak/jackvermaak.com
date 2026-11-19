import hashlib, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from figs import MIXPAD, LATENCY, SDR, FIRE, FIRE_LEGEND, VR

EMAIL = 'jackdrcvermaak@gmail.com'
LINKEDIN = 'https://www.linkedin.com/in/jack-vermaak/'
GITHUB = 'https://github.com/JackVermaak'
EXT = 'target="_blank" rel="noopener"'
# Fonts are self-hosted in site/fonts and declared at the top of styles.css. The two used above the fold are preloaded.
FONTS = ('<link rel="preload" href="/fonts/plex-sans-400.woff2" as="font" type="font/woff2" crossorigin>'
         '<link rel="preload" href="/fonts/source-serif-4.woff2" as="font" type="font/woff2" crossorigin>')
REPOS = {'Pico MixPad': 'https://github.com/JackVermaak/pico-mixpad',
         'Pico Latency Tester': 'https://github.com/JackVermaak/pico-latency-tester',
         'O-Grader': 'https://github.com/JackVermaak/ograder',
         'Forest fire spread simulation': 'https://github.com/JackVermaak/ForestFireSpreadSim',
         'Morning phone lock': 'https://github.com/JackVermaak/morning-lock'}

def url(path):
    """Root-absolute, extension-free URLs (Cloudflare Pages serves about.html at /about), so links never redirect
    and assets load the same from every page."""
    if path.startswith('/'):
        return path
    if path.startswith('http') or path.endswith('.pdf'):
        return path if path.startswith('http') else '/' + path
    path = path[:-5] if path.endswith('.html') else path
    return '/' if path == 'index' else '/' + path

def version(name):
    """Short content hash, so browsers can cache styles.css and site.js for a year and still get every change."""
    return hashlib.sha1(open(os.path.join(HERE, '..', 'site', name), 'rb').read()).hexdigest()[:8]
THEME_BOOT = "<script>try{var t=localStorage.getItem('theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>"

SUN = '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M4.6 4.6l1.6 1.6M17.8 17.8l1.6 1.6M2.5 12h2.2M19.3 12h2.2M4.6 19.4l1.6-1.6M17.8 6.2l1.6-1.6"/></svg>'
MOON = '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>'
BARS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'

def head(title, desc, root):
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{THEME_BOOT}
<link rel="stylesheet" href="/styles.css?v={version('styles.css')}">
{FONTS}
<script src="/site.js?v={version('site.js')}" defer></script>'''

def header(root, cur):
    def a(name, href):
        cu = ' aria-current="page"' if name == cur else ''
        return f'<a href="{url(href)}"{cu}>{name}</a>'
    nav = a('Home', 'index.html') + a('Projects', 'projects.html') + a('About', 'about.html') + a('Contact', 'contact.html') + f'<a href="/Jack_Vermaak_CV.pdf" {EXT}>CV &#8599;</a>'
    return (f'<header class="site-header"><div class="wrap"><a class="wordmark" href="/">Jack Vermaak</a>'
            f'<div class="header-right"><nav class="site-nav" aria-label="Main">{nav}</nav>'
            f'<button class="icon-btn theme-toggle" type="button" aria-label="Switch theme">{SUN}{MOON}</button>'
            f'<button class="icon-btn menu-toggle" type="button" aria-label="Open menu" aria-expanded="false">{BARS}</button></div></div></header>')

def footer(root):
    return (f'<footer class="site-footer"><div class="wrap"><span>&copy; <span id="year">2026</span> Jack Vermaak &middot; NRW, Germany</span>'
            f'<nav aria-label="Elsewhere"><a class="ig" href="{INSTAGRAM}" {EXT} aria-label="Instagram, @jack_vermaak">{CAMERA}<span>@jack_vermaak</span></a><a href="{LINKEDIN}" {EXT}>LinkedIn &#8599;</a><a href="{GITHUB}" {EXT}>GitHub &#8599;</a><a href="/Jack_Vermaak_CV.pdf" {EXT}>CV &#8599;</a></nav>'
            f'</div></footer>')

def page(path, title, desc, cur, main):
    root = '/'  # root-absolute links; see url()
    return dict(path=path, headhtml=head(title, desc, root),
                body=header(root, cur) + '\n<main>\n' + main(root) + '\n</main>\n' + footer(root))

INSTAGRAM = 'https://www.instagram.com/jack_vermaak/'
CAMERA = '<span class="ico ig-ico" aria-hidden="true"></span>'
IG_POSTS = ['https://www.instagram.com/p/De9qyoEiBQq/', 'https://www.instagram.com/p/Deb5K3tDCui/', 'https://www.instagram.com/p/DeMMiuXERHr/']
NATHAN = 'https://www.instagram.com/nathanphillipsclimbing/'

# slug/link, year, kind, title, one-liner, stack
PROJECTS = [
 ('projects/mixpad.html', '2026', 'Personal', 'Pico MixPad',
  'A USB controller that sets Windows volume per application, with its own firmware, desktop app and case.',
  'RP2350 &middot; CircuitPython &middot; Python'),
 ('projects/latency-tester.html', '2026', 'Personal', 'Pico Latency Tester',
  'A device that measures the delay between a mouse click and the screen changing.',
  'RP2350 &middot; C++ &middot; TinyUSB'),
 ('projects/hydrogen-excavator.html', '2025/26', 'University', 'Hydrogen-powered excavator',
  'Battery system and control platform for an excavator converted to run from a hydrogen fuel cell.',
  '48 V LiFePO4 &middot; Raspberry Pi &middot; CAN'),
 ('projects/sdr-receiver.html', '2025/26', 'University', 'Software-defined radio receiver',
  'A MATLAB receiver that decodes corrupted radio recordings back into text.',
  'MATLAB &middot; 4-PAM &middot; DSP'),
 ('projects/fire-simulation.html', '2025', 'University', 'Forest fire spread simulation',
  'A Python wildfire model with wind, firebreaks and a Monte Carlo forecast.',
  'Python &middot; NumPy &middot; Matplotlib'),
 ('projects/vr-card-game.html', '2024', 'University', 'Virtual reality card game',
  'A VR card duel in Unity where you pick up and play cards against a computer opponent.',
  'Unity &middot; C# &middot; Oculus XR'),
 ('/ograder/', '2026', 'Personal', 'O-Grader',
  'Shows Adam Ondra\'s ascents on his O-grade scale, using scraped ascent data, with an estimator for any grade.',
  'Cloudflare Workers &middot; scraped data'),
 ('https://synapse.nrw', 'Ongoing', 'Work', 'synapse.nrw',
  'The website for the Synapse student space at my university. I built it and maintain it.',
  'TYPO3 v13 &middot; PHP &middot; Git'),
]

DISPLAY = ['synapse.nrw', 'O-Grader', 'Pico MixPad', 'Pico Latency Tester', 'Hydrogen-powered excavator',
           'Software-defined radio receiver', 'Forest fire spread simulation', 'Virtual reality card game']
SORTED = sorted(PROJECTS, key=lambda p: DISPLAY.index(p[3]))
FEATURED = [p for p in PROJECTS if p[3] in ('Pico MixPad', 'Pico Latency Tester', 'Hydrogen-powered excavator')]

def card(root, p):
    link, year, kind, title, short, stack = p
    ext = link.startswith('http')
    live = ext or link.startswith('/')
    attrs = f' {EXT}' if live else ''
    go = (f'Visit {link.split("//")[1]} &#8599;' if ext else f'Open the {title} &#8599;') if live else 'Read the write-up &rarr;'
    code = f'<a class="card-code" href="{REPOS[title]}" {EXT} aria-label="{title} code on GitHub">GitHub &#8599;</a>' if title in REPOS else ''
    return (f'<li class="card" data-kind="{kind.lower()}"><a class="card-main" href="{url(link)}"{attrs}>'
            f'<span class="card-top"><span class="label">{kind}</span><span class="label">{year}</span></span>'
            f'<h3>{title}</h3><p>{short}</p><span class="stack">{stack}</span><span class="go">{go}</span></a>{code}</li>')

BENCH = [
 ('In progress and planned', [
   ('Steam balance finder', 'In progress', 'A site that finds CS2 skins on third-party markets that sell for more on the Steam market, after Steam\'s 15% fee.'),
   ('Homelab', 'In progress', 'An old PC turned Linux server for self-hosting, Docker and network services.'),
   ('Local AI game builder', 'In progress', 'A setup that lets local AI models build and test a small game overnight on my own hardware.'),
   ('MixPad desktop app in C++', 'Planned', 'A C++ version of the MixPad desktop app to replace the current Python one.'),
   ('Pico MixPad v2', 'Planned', 'A custom circuit board with hot-swap key sockets in place of the hand wiring.'),
   ('CS2 second-screen companion', 'Planned', 'A second-screen site for CS2 that automatically shows the key smoke lineups and minimap callouts for your current map and side.'),
 ]),
 ('Parked', [
   ('Morning phone lock', 'On hold', 'An app that gives you 20 minutes of phone time in the morning, then locks the phone to a few apps until you finish set tasks. It is complete but not currently in use.'),
   ('Home NAS', 'On hold', 'Network storage for the homelab, on hold while storage prices remain high.'),
   ('Pocket reference assistant', 'On hold', 'A pocket-sized offline device that answers short spoken questions from open knowledge bases.'),
   ('Boulder Bounty', 'Shelved', f'A site where climbers put bounties on boulder projects they want to see sent. The idea came from <a href="{NATHAN}" {EXT}>Nathan Phillips</a>, a pro climber from the UK.'),
   ('SkinVault', 'Shelved', 'A CS2-skin-backed token and website, built with a friend. Shelved after a CS2 update in October 2025 caused the skin market to collapse.'),
 ]),
]

def bench():
    out = []
    for title, items in BENCH:
        lis = ''.join(f'<li><div class="bench-row"><strong>{n}</strong><span class="label">{s}</span></div><p>{d}'
                      + (f' <a href="{REPOS[n]}" {EXT}>Code on GitHub &#8599;</a>' if n in REPOS else '') + '</p></li>' for n, s, d in items)
        out.append(f'<div class="bench-card"><h3>{title}</h3><ul>{lis}</ul></div>')
    return '<div class="bench">' + ''.join(out) + '</div>'

EXPERIENCE = [
 ('Apr 2026 &ndash; now', 'Student Assistant, TransRegINT', 'Hochschule Rhein-Waal &middot; Kamp-Lintfort',
  'Python tools for a regional energy project, one using the Google Places API, that found more than 500 companies in the region and collected their public contact details. Also compiled German energy prices from 2016 to 2026 and built an internal site for comparing them.'),
 ('Sep 2025 &ndash; now', 'Web Developer, Synapse student space', 'Hochschule Rhein-Waal &middot; Kamp-Lintfort',
  f'Built and maintain <a href="https://synapse.nrw" {EXT}>synapse.nrw</a> on TYPO3 v13 as its only developer, including a custom extension for the site\'s design. Updates go out over SSH with Composer.'),
 ('Oct &ndash; Dec 2024', 'Reverse Logistics Associate', 'Amazon fulfilment centre, via GI Group &middot; Germany',
  'Processed customer returns in Amazon\'s internal systems. Offered a nine-month extension at the end of the three-month placement.'),
 ('Feb 2020 &ndash; Aug 2022', 'Functional Analyst / ERP Consultant', 'Virtual Resource &middot; Cape Town',
  'Implemented and supported Workday HR and finance for three multinational clients. Gathered requirements, wrote functional documentation, tested rollouts and fixed data integration and reporting issues.'),
]

def timeline(with_text):
    out = []
    for when, role, where, what in EXPERIENCE:
        w = f'<p class="what">{what}</p>' if with_text else ''
        out.append(f'<li><span class="when">{when}</span><div><h3>{role}</h3><p class="where">{where}</p>{w}</div></li>')
    return '<ol class="timeline">' + ''.join(out) + '</ol>'

def copyline(id_):
    return f'<span class="copyline"><span class="addr" id="{id_}">{EMAIL}</span><button type="button" data-copy="{id_}">Copy</button></span>'

def home(root):
    cards = ''.join(card(root, p) for p in FEATURED)
    tiles = ''.join(f'<li><a href="{u}" {EXT} aria-label="Instagram post {i + 1} by @jack_vermaak"><span class="ph label">Post {i + 1}</span><img src="/photos/ig-{i + 1}.jpg" alt="" width="720" height="720" loading="lazy" decoding="async" onerror="this.remove()"></a></li>' for i, u in enumerate(IG_POSTS))
    return f'''<section class="wrap hero hero-solo">
<div>
<p class="label">Infotronic Systems Engineering student</p>
<h1>Jack Vermaak</h1>
<p class="intro">I am studying engineering at Hochschule Rhein-Waal in Germany. My main interests are software, hardware and electronics, particularly where the three meet. Outside of my studies, I am an avid boulderer and have been climbing for over 12 years.</p>
<div class="actions"><a class="btn primary" href="/projects">See my projects</a><a class="btn" href="/Jack_Vermaak_CV.pdf" {EXT}>Read my CV &#8599;</a></div>
</div>
</section>
<section class="wrap section">
<div class="section-head"><h2>Featured projects</h2><a class="more" href="/projects">All {len(PROJECTS)} projects &rarr;</a></div>
<ul class="cards three">{cards}</ul>
</section>
<section class="wrap section">
<div class="section-head"><h2>Recent posts</h2><a class="more ig" href="{INSTAGRAM}" {EXT}>{CAMERA}<span>@jack_vermaak</span></a></div>
<ul class="photos">{tiles}</ul>
</section>
<section class="wrap section contact-band">
<div><h2>Get in touch</h2><p>Email is the quickest way to reach me.</p></div>
{copyline('email-home')}
</section>'''

def projects(root):
    rows = ''.join(card(root, p) for p in SORTED)
    kinds = ['Personal', 'University', 'Work']
    chips = f'<button class="chip" type="button" data-filter="all" aria-pressed="true">All<span class="n">{len(PROJECTS)}</span></button>' + ''.join(
        f'<button class="chip" type="button" data-filter="{k.lower()}" aria-pressed="false">{k}<span class="n">{sum(1 for p in PROJECTS if p[2] == k)}</span></button>' for k in kinds)
    return f'''<section class="wrap page-intro"><p class="crumbs">Projects</p><h1>My projects</h1>
<p class="lede">Personal, university and work projects across embedded systems, electronics, signal processing and the web.</p></section>
<section class="wrap" style="padding-block: 0 56px">
<div class="filters" role="group" aria-label="Filter projects">{chips}</div>
<ul class="cards">{rows}</ul>
</section>
<section class="wrap section" style="padding-bottom: 72px">
<div class="section-head"><h2>On the bench</h2></div>
{bench()}
</section>'''

def about(root):
    return f'''<section class="wrap page-intro about-centre"><p class="crumbs">About</p><h1>About me</h1>
<p class="lede">Engineering student, former ERP consultant and long-time boulderer.</p></section>
<section class="wrap about-single about-centre">
<div class="prose">
<p>I am Jack Vermaak, an Infotronic Systems Engineering student at Hochschule Rhein-Waal in Germany. The degree combines electronics, computer engineering and software, and I expect to finish in late 2027.</p>
<p>My main interest is where hardware and software meet: what runs on a microcontroller, what runs on a computer, and how the two communicate. Recent projects include a USB audio controller, a click-to-screen latency tester, a software radio receiver and the electrical system for a hydrogen-powered excavator.</p>
<p>I grew up in South Africa and spent two and a half years in Cape Town as a Workday ERP consultant before moving to Germany to study. That work taught me to gather requirements from clients, document processes, test changes carefully and resolve data problems.</p>
<p>Outside of study and work, I have been bouldering for over 12 years, with several outdoor problems up to V11 (8A).</p>
</div>
</section>
<section class="wrap section" id="experience">
<div class="section-head"><h2>Experience</h2><a class="more" href="/Jack_Vermaak_CV.pdf" {EXT}>Full CV &#8599;</a></div>
{timeline(True)}
</section>
<section class="wrap section">
<div class="section-head"><h2>Education</h2></div>
<ol class="timeline"><li><span class="when">Sep 2022 &ndash; 2027</span><div><h3>B.Sc. Infotronic Systems Engineering</h3><p class="where">Hochschule Rhein-Waal &middot; Kamp-Lintfort &middot; Taught in English</p>
<p class="what">Current average 2.3 on the German scale, where 1.0 is the best grade. Strongest modules: Machine Learning (top grade in the class), Communication Systems (2nd of 18) and Computer Networks (5th of 38).</p></div></li></ol>
</section>
<section class="wrap section" style="padding-bottom: 72px">
<div class="section-head"><h2>Tools I use</h2></div>
<dl class="skills">
<div><dt>Languages</dt><dd>Python, C++, C#, Java, PHP, HTML/CSS</dd></div>
<div><dt>Embedded</dt><dd>Raspberry Pi Pico 2 (RP2350), Arduino, Raspberry Pi, CircuitPython, TinyUSB, USB HID, I2C</dd></div>
<div><dt>Engineering</dt><dd>MATLAB, Simulink, OpenSCAD, NumPy, Matplotlib</dd></div>
<div><dt>Web and tooling</dt><dd>TYPO3, Git, GitHub Actions, Linux over SSH, pytest, Unity, Claude Code</dd></div>
</dl>
</section>'''

def contact(root):
    return f'''<section class="wrap page-intro"><p class="crumbs">Contact</p><h1>Get in touch</h1>
<p class="lede">Please email me about projects, internships or anything on this site. I usually reply within two working days.</p></section>
<section class="wrap" style="padding-block: 0 80px">
<div class="contact-list">
<div><span class="label">Email</span>{copyline('email')}</div>
<div><span class="label">Instagram</span><a class="ig" href="{INSTAGRAM}" {EXT}>{CAMERA}<span>@jack_vermaak &#8599;</span></a></div>
<div><span class="label">LinkedIn</span><a href="{LINKEDIN}" {EXT}>linkedin.com/in/jack-vermaak &#8599;</a></div>
<div><span class="label">GitHub</span><a href="{GITHUB}" {EXT}>github.com/JackVermaak &#8599;</a></div>
<div><span class="label">CV</span><a href="/Jack_Vermaak_CV.pdf" {EXT}>View the PDF &#8599;</a></div>
<div><span class="label">Location</span><span>NRW, Germany</span></div>
</div>
</section>'''

ORDER = [(p[0], p[3]) for p in PROJECTS if not p[0].startswith('http')]

def proj(root, i, lede, facts, body, links=()):
    link, year, kind, title, short, stack = PROJECTS[i]
    f = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in facts)
    lk = ''.join(f'<p><a href="{u}" {EXT}>{t} &#8599;</a></p>' for t, u in links)
    prev = ORDER[i - 1] if i > 0 else None
    nxt = ORDER[i + 1] if i < len(ORDER) - 1 else None
    pg = (f'<a class="prev" href="{url(prev[0])}"><span class="label">&larr; Previous</span><strong>{prev[1]}</strong></a>' if prev else '<span></span>') + \
         (f'<a class="next" href="{url(nxt[0])}"><span class="label">Next &rarr;</span><strong>{nxt[1]}</strong></a>' if nxt else '<span></span>')
    return f'''<section class="wrap page-intro"><p class="crumbs"><a href="/projects">Projects</a> / {kind} / {year}</p>
<h1>{title}</h1><p class="lede">{lede}</p></section>
<section class="wrap article">
<div class="prose">{body}{lk}</div>
<aside class="spec" aria-label="Project details"><div class="spec-head"><span class="label">Spec sheet</span></div><dl>{f}</dl></aside>
</section>
<nav class="wrap pager" aria-label="More projects">{pg}</nav>'''

def mixpad(root):
    body = f'''<figure>{MIXPAD}<figcaption>The top plate: display and mic light, four app knobs, the main volume knob and eight keys.</figcaption></figure>
<p>I wanted a quicker way to balance game, voice chat and music than opening the Windows volume mixer, so I built a controller for it. It has a main volume knob, four knobs for individual apps, eight mechanical keys and a small screen that shows what each knob controls. Pressing any knob mutes it, and one key mutes the microphone.</p>
<h2>How it works</h2>
<p>The pad connects over USB and appears as a keyboard, a media controller and a serial port at the same time, so the main volume knob and media keys work on any computer with nothing installed. A Python app on the PC adds per-app control through the Windows audio API and communicates with the pad over a simple text protocol I designed.</p>
<p>The firmware is written in CircuitPython, and the Pico's programmable I/O reads the knobs in hardware so no steps are missed. The knobs send how far they were turned rather than a fixed position, so changing a volume in Windows never fights the hardware. The desktop app has 11 unit tests that run without the pad attached.</p>
<h3>Serial messages</h3>
<div class="table-scroll"><table><thead><tr><th>From</th><th>Message</th><th>Meaning</th></tr></thead><tbody>
<tr><td>PC</td><td><code>?</code></td><td>Is a pad connected?</td></tr>
<tr><td>Pad</td><td><code>HELLO MACROPAD</code></td><td>Yes, with its version</td></tr>
<tr><td>Pad</td><td><code>E ch delta</code></td><td>A knob was turned</td></tr>
<tr><td>Pad</td><td><code>P ch</code></td><td>A knob was pressed</td></tr>
<tr><td>PC</td><td><code>V ch vol muted label</code></td><td>What to show for a knob</td></tr>
<tr><td>PC</td><td><code>MIC 1|0</code></td><td>Mic state, for the light</td></tr>
</tbody></table></div>
<p>The PC repeats the full state every second. If the pad receives nothing for five seconds, it continues as a plain volume controller.</p>
<h2>Next steps</h2>
<p>A custom circuit board with hot-swap key sockets instead of hand wiring, and a C++ version of the desktop app to replace the Python one.</p>'''
    facts = [('Year', '2026'), ('Type', 'Personal project'), ('MCU', 'Raspberry Pi Pico 2 (RP2350)'), ('Inputs', '5 rotary encoders, 8 Cherry MX keys'), ('Display', 'SSD1306 OLED'), ('Software', 'CircuitPython, Python, pytest'), ('Case', 'Parametric, OpenSCAD')]
    return proj(root, 0, 'A USB controller for setting Windows volume per application.', facts, body, [('Code on GitHub', REPOS['Pico MixPad'])])

def latency(root):
    body = f'''<figure>{LATENCY}<figcaption>One measurement: the timer starts with the click and stops when the screen's brightness crosses a threshold.</figcaption></figure>
<p>This device measures the time between a mouse click and the screen actually changing. That delay includes the USB connection, the operating system, the game, the graphics card and the monitor, which makes it a useful way to compare game and display settings. It also confirms that a device such as the MixPad does not add any delay.</p>
<h2>How it works</h2>
<ol>
<li>Read the screen's brightness and noise with a light sensor held against the monitor.</li>
<li>Send a click as a 1000 Hz USB mouse and start a microsecond timer.</li>
<li>Stop the timer when the brightness moves past a threshold set from the measured noise.</li>
</ol>
<p>Each run takes 100 measurements with random pauses in between, so the clicks never line up with the monitor's refresh. The device shows the average and spread on its display, and a Python script can log every measurement to a CSV file.</p>
<h2>Why C++</h2>
<p>I first planned to use CircuitPython, but its source code showed that it only reports USB input every 8 milliseconds. That would have added up to 8 ms of error to every measurement, so I wrote the firmware in C++ with TinyUSB, which reports every millisecond.</p>'''
    facts = [('Year', '2026'), ('Type', 'Personal project'), ('MCU', 'Raspberry Pi Pico 2 W'), ('Sensor', 'ALS-PT19 light sensor'), ('USB rate', '1000 Hz'), ('Samples', '100 per run'), ('Software', 'C++, TinyUSB, Python')]
    return proj(root, 1, 'A small device that measures the delay between a mouse click and the screen changing.', facts, body, [('Code on GitHub', REPOS['Pico Latency Tester'])])

def excavator(root):
    body = '''<figure>
<p class="chain-label">Power</p>
<ul class="chain"><li>Hydrogen tank</li><li>Fuel cell</li><li>Boost converter</li><li class="hi">48 V battery + BMS</li><li>Motor controller</li><li>Hydraulics</li></ul>
<p class="chain-label">Control</p>
<ul class="chain"><li>5 V supply</li><li class="hi">Raspberry Pi</li><li class="hi">Arduinos</li><li>CAN bus</li></ul>
<figcaption>How the excavator is powered and controlled. The highlighted parts are the ones my group worked on.</figcaption>
</figure>
<p>A university project across two campuses to take a plug-in electric excavator that had been unused for about ten years and make it run without a mains connection. A hydrogen fuel cell charges a 48 V LiFePO4 battery, and the battery drives the motor that powers the hydraulics.</p>
<p>I was one of four students in the electrical engineering group during the design phase. We chose the battery, a separate battery management system and the voltage converters, and designed the control platform: a Raspberry Pi coordinating several Arduinos that talk to the excavator's parts over CAN bus.</p>
<h2>Keeping it safe</h2>
<p>The Raspberry Pi is not designed for safety-critical work, so the shutdown logic runs on the Arduinos. If the Pi crashes or loses contact, they can still switch the system off on their own. We also chose to monitor the hydraulics rather than control them from software.</p>
<h2>Outcome</h2>
<p>The team built the excavator during a five-day Makeathon in February 2026, and it ran successfully. I also helped design the project poster and presented the project at the university.</p>'''
    facts = [('Year', '2025/26'), ('Type', 'University team project'), ('My part', 'Battery system and control design'), ('Battery', '48 V LiFePO4, 5.1 kWh'), ('Control', 'Raspberry Pi, Arduinos, CAN bus'), ('Grade', '1.3')]
    return proj(root, 2, 'Converting an old electric excavator to run on a battery charged by a hydrogen fuel cell.', facts, body)

def sdr(root):
    body = f'''<figure>{SDR}<figcaption>The signal uses four amplitude levels, so each symbol carries two bits.</figcaption></figure>
<p>A project for my Communication Systems course. We were given three recorded radio signals, each damaged in different ways, and had to write a receiver in MATLAB that turned them back into readable text. Mine decoded all three.</p>
<h2>How it works</h2>
<p>The receiver works in stages. It filters out interference, locks onto the carrier, finds the right moment to sample each symbol, corrects for distortion with an adaptive equaliser, and finds where each block of data starts. Some stages started from the course textbook's example code, which I adapted and combined with my own.</p>
<h2>A difficult bug</h2>
<p>The decoded text alternated between correct and unreadable on every other block. The stage that locks onto the carrier can lock on upside down, which flips every symbol. I fixed it by checking each block against its known header and flipping it back when needed.</p>'''
    facts = [('Year', '2025/26'), ('Type', 'University project'), ('Modulation', '4-PAM, 2 bits per symbol'), ('Built with', 'MATLAB'), ('Result', '3 of 3 recordings decoded'), ('Grade', '2.3, second of 18')]
    return proj(root, 3, 'A MATLAB receiver that decodes corrupted radio recordings back into text.', facts, body)

def fire(root):
    body = f'''<figure>{FIRE}{FIRE_LEGEND}<figcaption>A run of the same rules, drawn in your browser. The fire started near the top with the wind blowing down, and the bare strip is a firebreak.</figcaption></figure>
<p>A project for a modelling and simulation course. The forest is a 50 by 50 grid of trees and empty ground. Each step, a tree next to a fire has a chance of catching, burning trees burn out, and wind makes the fire more likely to spread in one direction.</p>
<p>You can start a fire by clicking a tree, switch wind and a firebreak on and off, and run a forecast that simulates 50 possible futures to show where the fire is most likely to reach.</p>
<h2>Improvements since the course</h2>
<p>The forecast now shows the chance of each cell burning across all runs, an optional random seed makes runs repeatable, and the default wind direction matches the controls. The next step is to speed it up for larger forests.</p>'''
    facts = [('Year', '2025'), ('Type', 'Individual university project'), ('Model', 'Stochastic cellular automaton'), ('Grid', '50 &times; 50 cells'), ('Forecast', '50 Monte Carlo runs'), ('Built with', 'Python, NumPy, Matplotlib'), ('Grade', '2.0')]
    return proj(root, 4, 'A Python model of how a wildfire spreads, with wind and firebreaks.', facts, body, [('Code on GitHub', REPOS['Forest fire spread simulation'])])

def vr(root):
    body = f'''<figure>{VR}<figcaption>The spell cards: each element beats one of the others and loses to the third.</figcaption></figure>
<p>A team project for the Innovative Technologies course. Four of us built a card duel game in virtual reality with Unity and Oculus XR. You stand at a table, physically pick up cards and play them against a computer opponent.</p>
<p>The project got a 1.3, the highest grade in the class.</p>'''
    facts = [('Year', 'Summer 2024'), ('Type', 'University team project'), ('Team', '4 students'), ('Built with', 'Unity (C#), Oculus XR'), ('Grade', '1.3, highest in the class')]
    return proj(root, 5, 'A card duel you play with your hands in VR.', facts, body)

D = 'Jack Vermaak is an engineering student in Germany interested in software, hardware and electronics.'
PAGES = [
 page('index.html', 'Jack Vermaak', D, 'Home', home),
 page('projects.html', 'Projects | Jack Vermaak', 'Embedded systems, electronics and software projects by Jack Vermaak.', 'Projects', projects),
 page('about.html', 'About | Jack Vermaak', 'About Jack Vermaak: background, experience, education and tools.', 'About', about),
 page('contact.html', 'Contact | Jack Vermaak', 'How to contact Jack Vermaak.', 'Contact', contact),
 page('projects/mixpad.html', 'Pico MixPad | Jack Vermaak', 'A USB volume controller built on the Raspberry Pi Pico 2.', 'Projects', mixpad),
 page('projects/latency-tester.html', 'Pico Latency Tester | Jack Vermaak', 'A click-to-screen latency tester built on the Raspberry Pi Pico 2.', 'Projects', latency),
 page('projects/hydrogen-excavator.html', 'Hydrogen-powered excavator | Jack Vermaak', 'Battery and control design for a hydrogen-electric excavator.', 'Projects', excavator),
 page('projects/sdr-receiver.html', 'Software-defined radio receiver | Jack Vermaak', 'A 4-PAM software radio receiver in MATLAB.', 'Projects', sdr),
 page('projects/fire-simulation.html', 'Forest fire spread simulation | Jack Vermaak', 'A wildfire spread model in Python.', 'Projects', fire),
 page('projects/vr-card-game.html', 'Virtual reality card game | Jack Vermaak', 'A VR card duel game built in Unity.', 'Projects', vr),
]

FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#1d6a51"/><text x="32" y="43" text-anchor="middle" font-family="Georgia, serif" font-size="30" font-weight="600" fill="#f4f6f5">JV</text></svg>'''


SITE = os.path.join(HERE, '..', 'site')

def write_all(outdir=SITE):
    """Regenerate the HTML pages in site/. styles.css, site.js, favicon.svg, the CV and photos/ are edited in site/ directly."""
    for p in PAGES:
        path = os.path.join(outdir, p['path'])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        html = f'<!doctype html>\n<html lang="en">\n<head>\n{p["headhtml"]}\n</head>\n<body>\n{p["body"]}\n</body>\n</html>\n'
        open(path, 'w').write(html)

if __name__ == '__main__':
    write_all(); print('Pages written to site/')
