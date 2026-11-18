MIXPAD = '''<svg class="fig" viewBox="0 0 220 280" role="img" aria-label="Sketch of the MixPad top plate with an OLED, five knobs and eight keys">
<rect x="4" y="4" width="212" height="262" rx="10" class="stroke" stroke-width="1.5"/>
<rect x="56" y="20" width="108" height="46" rx="3" class="acc-soft" stroke-width="1.2"/>
<text x="66" y="36" class="acc-text">GAME</text><rect x="66" y="40" width="70" height="4" class="acc-fill"/><text x="66" y="54" class="acc-text">MIC MUTED</text>
<circle cx="184" cy="43" r="5" class="acc" stroke-width="1.5"/><text x="172" y="62">mic</text>
<g class="stroke" stroke-width="1.4"><circle cx="40" cy="104" r="15"/><circle cx="86" cy="104" r="15"/><circle cx="134" cy="104" r="15"/><circle cx="180" cy="104" r="15"/>
<line x1="40" y1="92" x2="40" y2="100"/><line x1="86" y1="92" x2="86" y2="100"/><line x1="134" y1="92" x2="134" y2="100"/><line x1="180" y1="92" x2="180" y2="100"/>
<circle cx="110" cy="158" r="22"/><line x1="110" y1="140" x2="110" y2="150"/></g>
<text x="29" y="132">app 1</text><text x="75" y="132">app 2</text><text x="123" y="132">app 3</text><text x="169" y="132">app 4</text><text x="94" y="192" class="ink">master</text>
<g class="fill-surface" stroke-width="1.2"><rect x="22" y="202" width="34" height="26" rx="3"/><rect x="70" y="202" width="34" height="26" rx="3"/><rect x="118" y="202" width="34" height="26" rx="3"/><rect x="166" y="202" width="34" height="26" rx="3"/>
<rect x="22" y="234" width="34" height="26" rx="3"/><rect x="70" y="234" width="34" height="26" rx="3"/><rect x="118" y="234" width="34" height="26" rx="3"/><rect x="166" y="234" width="34" height="26" rx="3"/></g>
<text x="30" y="219" class="ink">mic</text></svg>'''

LATENCY = '''<svg class="fig" viewBox="0 0 320 178" role="img" aria-label="Timing diagram: the timer runs from the click until screen brightness crosses the threshold">
<text x="8" y="44" class="ink">click</text><path d="M52 52 H96 V30 H300" class="stroke" stroke-width="1.6"/>
<text x="8" y="112" class="ink">screen</text><path d="M52 120 H206 C 214 120, 218 84, 230 80 S 260 76, 300 76" class="stroke" stroke-width="1.6"/>
<line x1="52" y1="106" x2="300" y2="106" class="soft" stroke-width="1" stroke-dasharray="4 4"/><text x="234" y="100">threshold</text>
<line x1="96" y1="30" x2="96" y2="150" class="soft" stroke-width="0.8" stroke-dasharray="2 3"/><line x1="213" y1="106" x2="213" y2="150" class="soft" stroke-width="0.8" stroke-dasharray="2 3"/>
<path d="M96 150 H213" class="acc" stroke-width="2"/><path d="M96 145 V155 M213 145 V155" class="acc" stroke-width="2"/>
<text x="118" y="168" class="acc-text">measured latency</text></svg>'''

def _box(x, y, w, label, hi=False):
    cls = 'acc-soft' if hi else 'fill-surface'
    tcls = 'acc-text' if hi else 'ink'
    return f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="4" class="{cls}" stroke-width="1.2"/><text x="{x + w/2}" y="{y + 19}" text-anchor="middle" class="{tcls}">{label}</text>'

EXCAVATOR = ('<svg class="fig" viewBox="0 0 320 190" role="img" aria-label="Excavator energy and control chain">'
  '<defs><marker id="exc-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="soft-fill"/></marker></defs>'
  '<text x="8" y="26">energy</text><text x="8" y="124">control and safety</text>'
  + _box(8, 36, 60, 'H2 tank') + _box(86, 36, 66, 'Fuel cell') + _box(170, 36, 84, '48 V LiFePO4', True) + _box(272, 36, 42, 'Drive')
  + _box(170, 134, 84, '48 V to 5 V') + _box(86, 134, 66, 'Pi hub', True) + _box(8, 134, 60, 'Arduinos', True)
  + '<g class="soft" stroke-width="1.2"><path d="M68 51 H84" marker-end="url(#exc-ar)"/><path d="M152 51 H168" marker-end="url(#exc-ar)"/><path d="M254 51 H270" marker-end="url(#exc-ar)"/>'
  '<path d="M212 66 V132" marker-end="url(#exc-ar)"/><path d="M170 149 H154" marker-end="url(#exc-ar)"/><path d="M86 149 H70" marker-end="url(#exc-ar)"/></g>'
  '<text x="218" y="104">5 V for control</text></svg>')

def _sdr():
    levels = {3: 40, 1: 80, -1: 120, -3: 160}
    seq = [1, 3, -1, -3, 1, -1, 3, -3, -1, 1]
    xs = [52 + i * 28 for i in range(len(seq))]
    pts = ' '.join(f'{x},{levels[v]}' for x, v in zip(xs, seq))
    lines = ''.join(f'<line x1="44" y1="{y}" x2="312" y2="{y}" class="soft" stroke-width="0.8" stroke-dasharray="3 4"/><text x="10" y="{y + 3}" class="ink">{("+" if v > 0 else "")}{v}</text>' for v, y in levels.items())
    dots = ''.join(f'<circle cx="{x}" cy="{levels[v]}" r="3.2" class="acc-fill"/>' for x, v in zip(xs, seq))
    return (f'<svg class="fig" viewBox="0 0 320 190" role="img" aria-label="4-PAM symbols on four amplitude levels">{lines}'
            f'<polyline points="{pts}" class="stroke" stroke-width="1.3" stroke-linejoin="round"/>{dots}'
            '<text x="44" y="184">one symbol per dot, 2 bits per symbol</text></svg>')
SDR = _sdr()

VR = ('<svg class="fig" viewBox="0 0 320 200" role="img" aria-label="Three spell cards: fire, ice and water">'
  '<g transform="rotate(-8 100 110)"><rect x="60" y="45" width="80" height="120" rx="8" class="fill-surface" stroke-width="1.4"/><text x="100" y="110" text-anchor="middle" class="ink">FIRE</text></g>'
  '<g><rect x="120" y="38" width="80" height="120" rx="8" class="acc-soft" stroke-width="1.6"/><text x="160" y="102" text-anchor="middle" class="acc-text">ICE</text></g>'
  '<g transform="rotate(8 220 110)"><rect x="180" y="45" width="80" height="120" rx="8" class="fill-surface" stroke-width="1.4"/><text x="220" y="110" text-anchor="middle" class="ink">WATER</text></g>'
  '<text x="160" y="190" text-anchor="middle">each element beats one and loses to one</text></svg>')

FIRE = '<canvas class="fire-canvas" width="250" height="250" aria-label="A 50 by 50 forest grid with a fire front spreading down towards a firebreak"></canvas>'
FIRE_LEGEND = '<div class="legend"><span style="--c: var(--tree)">tree</span><span style="--c: var(--fire)">burning</span><span style="--c: var(--ground)">empty or burnt</span></div>'
