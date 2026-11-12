"""Single source for the talk script.

Run:  python notes/script.py
It writes the notes into each slide of index.html (press N, R for practice mode, or P for
presenter view) and builds speaker-notes.html, a printable version of the same script.
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Each slide: (id, title, time, point, [lines]).
# Lines starting with "[" are stage directions; "Q:" lines are questions for the class;
# "If asked:" lines are backup answers. A "[Click" line starts the part said after that click.
SLIDES = [
    ("open", "Clean water & sanitation", "0:15", "Say who you are, the goal, and what you will cover.", [
        "Hi, I’m Anders. My topic is UN Goal 6: clean water and sanitation.",
        "Today I’m going to talk about how farms, AI and cities use water, and what businesses can do about it.",
        "[Click: a drop falls into the water and the Earth appears.]",
    ]),
    ("title", "How much water is there?", "0:25", "There is very little water we can actually use.", [
        "First, how much water is there actually?",
        "[Click: the water spheres come out of the Earth.]",
        "If you rolled all the water on Earth into one ball, it would be about 860 miles across. The Earth is almost 8,000.",
        "All the fresh water that isn’t frozen would be about 170 miles, and most of that is underground.",
        "The lakes and rivers we actually use are the tiny dot with the ring. 35 miles. That’s what everyone shares.",
    ]),
    ("goal", "The goal", "0:35", "What SDG 6 aims for, and how far off we are.", [
        "SDG 6 is the UN’s goal for clean water and sanitation for everyone by 2030. Three big parts.",
        "Safe drinking water. 2.1 billion people still don’t have it, and progress would need to be six times faster.",
        "Safe toilets. 3.4 billion people don’t have them. Progress needs to be five times faster.",
        "Handwashing at home. 1.7 billion people don’t have it. Three times faster.",
        "There’s also a target about using water efficiently, so places don’t run short. That’s what the rest of my talk is about.",
        "[Click: the bottom line appears.]",
        "At today’s pace, we miss this goal.",
        "If asked: “safe” drinking water means water at home, available when you need it, and not contaminated. A lot of people have water that doesn’t meet all three.",
    ]),
    ("terms", "Key terms", "0:30", "Four words you need for the rest of the talk.", [
        "[Wait for the chapter card to pass.]",
        "A few words you need for the rest of this.",
        "Withdrawal is water we take from a river, a lake or underground. A lot of it goes back.",
        "Consumption is water that doesn’t come back. It evaporates or ends up in a product.",
        "Water stress means a place is using almost all the water it has.",
        "A water footprint is all the water behind something you buy. One cotton T-shirt takes about 2,700 liters.",
    ]),
    ("equal", "Not all water use is equal", "0:50", "What matters is where and when, not just how much.", [
        "First, look at the units. Farms and power plants are per day. Data centers are per year.",
        "Power plants take the most water, 133 billion gallons a day, but only about 3% gets used up. The rest goes back into the river, just warmer.",
        "Farms use up about 62% of what they take.",
        "Data center cooling towers evaporate 70 to 80%, and it comes out of one town’s supply.",
        "Water doesn’t disappear. It evaporates and falls somewhere else. So what matters is where you take it from, and when. A gallon in Seattle isn’t the same as a gallon in Phoenix during a drought.",
    ]),
    ("versus", "ChatGPT vs. almonds", "0:45", "A comparison everyone can picture.", [
        "[Let the scale wobble. Don’t hint at the answer.]",
        "Now a more specific comparison.",
        "A is every question the whole world asks ChatGPT, for a full year. That’s about 2.5 billion questions a day.",
        "B is every almond orchard in California, for one month.",
        "Q: So what do you guys think, A or B? Hands up for A. Now B. It might be closer than you’d think.",
        "[Click when you’ve counted hands: the scale tips.]",
        "It isn’t close. A year of ChatGPT is about 78 million gallons. A month of almonds is about 76 billion. Almonds use about a thousand times more.",
        "[Click: the 30-year line.]",
        "If you ran ChatGPT for 30 years straight, it would still use less water than California’s almonds use in one day.",
        "If asked: the ChatGPT number is OpenAI’s own, and it only covers answering questions, not training the AI or the power plants. Researchers estimate about four times more. Even then it’s about 8 years of ChatGPT for one day of almonds.",
        "If asked: the almond number is the almond industry’s own estimate, and it’s the lowest one. It’s based on 2013, when there were fewer orchards. Other groups estimate almost twice as much.",
    ]),
    ("live", "Live: right now", "0:25", "The same gap, happening in real time.", [
        "[Wait for the camera to land.]",
        "These counters started when this slide opened. They use the same numbers.",
        "ChatGPT uses about 2.5 gallons a second. That’s the drip on the left.",
        "Almonds use almost 29,000 gallons a second. That fills an Olympic pool every 23 seconds. Each full pool lifts out and joins the row in front.",
        "At ChatGPT’s rate, filling one pool would take about three days.",
        "If asked: these are yearly averages. Almond orchards use more water in summer and less in winter.",
    ]),
    ("hook", "AI’s real problem", "0:40", "AI’s water problem is local. The real problem is electricity.", [
        "So is AI off the hook? Not totally.",
        "Data centers and farms both use fresh water. They just often get it from different places. Data centers often use treated water from the town’s taps. Almonds use water straight from rivers and underground.",
        "So AI’s water problem is local. It hits a few towns, often in dry places like Arizona and Texas.",
        "[Click: the electricity side.]",
        "The real problem is electricity. Data centers used about 4.4% of all US electricity in 2023, and that could be as much as 12% by 2028.",
        "Most of that power still comes from burning natural gas and coal. One study found US data centers put out about 105 million tons of CO2 in a year.",
        "So if you want to criticize AI, start with the electricity and the pollution it causes.",
        "If asked: the 105 million tons is from a 2024 study led by Harvard researchers. It covers September 2023 to August 2024, and it’s about 2% of all US emissions.",
        "If asked: not every data center uses town water. Some, like some of Google’s, use recycled wastewater.",
    ]),
    ("real", "The real problem", "0:50", "Farms use most of our fresh water, and waste a lot of it.", [
        "[Wait for the chapter card to pass.]",
        "So where is the real problem? Farms.",
        "71% of all the fresh water people take goes to farming. That’s way more than cities, factories or data centers.",
        "And a lot of it gets wasted. Most farms still flood their fields. With flooding, about 40% of the water never reaches the plant’s roots. It runs off or evaporates. Drip irrigation gets about 90% of it there.",
        "But in Asia, which has most of the world’s irrigated farmland, only about 7% of it uses drip.",
        "So the biggest fix is simple: get the water to the roots, not the whole field.",
        "Q: Why do you guys think more farms don’t switch to drip?",
        "If asked: drip costs more to install, and a lot of small farmers can’t afford it. That’s what the companies on the next slide are working on.",
        "If asked: the 40% is the field-level number from the UN’s farm agency, the FAO. If you count water lost in canals on the way, flood irrigation is closer to half lost.",
    ]),
    ("business", "Who’s fixing it", "0:55", "Companies helping farms water smarter, plus one in tech.", [
        "[Wait for the chapter card to pass.]",
        "So who’s actually fixing this? Mostly companies that help farms water smarter.",
        "Netafim makes drip irrigation. Instead of flooding a field, tubes drip water right at each plant’s roots. One California farm that switched cut its water use by 25 to 30%.",
        "N-Drip makes drip irrigation that runs on gravity, so there’s no pump. It’s cheap enough for small farms. In a rice trial it used 57% less water.",
        "CropX puts sensors in the soil that tell farmers exactly when and how much to water. On one Indiana corn farm it cut pumped water by about 28%.",
        "And in tech, Microsoft’s new data centers cool their chips by reusing the same water in a closed loop. That saves about 125 million liters per site each year.",
        "All of these save water, and they save money too, because water and pumping cost money.",
        "If asked: these are results from specific farms and trials. How much a farm saves depends on the crop and how it watered before.",
        "If asked: farmers sometimes use the water they save to plant more. So saving water only works if there are also limits on total use.",
    ]),
    ("moves", "Three moves", "0:45", "My recommendations, using People, Profit and Planet.", [
        "[Wait for the Earth to rise.]",
        "So what should businesses do? Three things.",
        "People: build where there’s enough water, and put money back into the local water system.",
        "Profit: treat water as a business risk. Droughts can shut down factories, and leaky pipes waste about 39 billion dollars a year.",
        "Planet: focus on farms, since they use 71% of the water. Help suppliers switch to drip irrigation, and reuse water.",
        "To sum up: water problems are local, but supply chains are global. The headlines are about AI, but the biggest gains are on farms.",
        "Q: So what do you guys think, would you build a data center in Arizona? Why or why not?",
        "[Take two or three answers.]",
    ]),
    ("aiuse", "How I used AI", "0:20", "Required by the assignment. Be specific.", [
        "The assignment asks how I used AI. I used Claude, made by Anthropic.",
        "It helped me find sources, pointed out where they disagreed, helped plan the timing, and built this website.",
        "I picked the topic and the outline, and I checked the numbers against the original sources.",
    ]),
    ("sources", "Works cited", "0:05", "Finish and take questions.", [
        "These are my sources. The links work on the website.",
        "Thanks. Any questions?",
    ]),
]


def plain(lines):
    return "\n".join(lines)


def update_deck():
    path = ROOT / "index.html"
    src = path.read_text(encoding="utf-8")
    for sid, title, time, point, lines in SLIDES:
        body = f"({time}) Point: {point}\n\n" + plain([l[2:].lstrip() if l.startswith("Q:") else l for l in lines])
        pat = re.compile(r'(<section[^>]*\bid="%s"[\s\S]*?<template class="notes">)[\s\S]*?(</template>)' % re.escape(sid))
        src, n = pat.subn(lambda m: m.group(1) + html.escape(body, quote=False) + m.group(2), src, count=1)
        if n != 1:
            raise SystemExit(f"notes not found for slide {sid}")
    path.write_text(src, encoding="utf-8")


def line_html(t):
    e = html.escape(t, quote=False)
    if t.startswith("["):
        return f'<p class="cue">{e}</p>'
    if t.startswith("Q:"):
        return f'<p class="q">{e[2:].lstrip()}</p>'
    if t.startswith("If asked:"):
        return f'<p class="ifq"><b>If asked:</b>{e[9:]}</p>'
    return f"<p>{e}</p>"


def build_page():
    total = sum(int(t.split(":")[0]) * 60 + int(t.split(":")[1]) for _, _, t, _, _ in SLIDES)
    cards = []
    for k, (sid, title, time, point, lines) in enumerate(SLIDES, 1):
        cards.append(
            f'<section class="s"><header><span class="n">{k:02d}</span><h2>{html.escape(title)}</h2>'
            f'<span class="t">{time}</span><a href="index.html#{k}" class="go">Open slide</a></header>'
            f'<p class="pt">{html.escape(point)}</p>' + "".join(line_html(l) for l in lines) + "</section>")
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Speaker Notes · Follow the Water</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500..700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@500&display=swap">
<style>
:root{{--ink:#0B2A3C;--teal:#0B6F6A;--ember:#C2412D;--slate:#4A6170;--rule:#D3E3E2;--bg:#F8FBFA}}
*{{box-sizing:border-box;margin:0}}
body{{background:var(--bg);color:var(--ink);font:17px/1.6 Inter,Arial,sans-serif;padding:40px 16px 80px}}
main{{max-width:760px;margin:0 auto}}
h1{{font:700 40px/1.1 Fraunces,Georgia,serif;letter-spacing:-.01em}}
.sub{{color:var(--slate);margin:10px 0 8px}}
.tips{{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:16px 20px;margin:20px 0 32px;font-size:15px}}
.tips li{{margin:4px 0 4px 18px}}
.s{{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:22px 24px;margin:0 0 18px;break-inside:avoid}}
.s header{{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:6px}}
.n{{font:500 13px "JetBrains Mono",monospace;color:var(--teal)}}
h2{{font:650 24px/1.2 Fraunces,Georgia,serif;flex:1}}
.t{{font:500 13px "JetBrains Mono",monospace;background:#E3F0EE;color:var(--teal);padding:3px 9px;border-radius:999px}}
.go{{font-size:13px;color:var(--slate)}}
.pt{{font-weight:600;color:var(--teal);margin-bottom:10px}}
.s p{{margin:0 0 8px}}
.cue{{font:500 13px "JetBrains Mono",monospace;color:var(--slate);background:#F1F5F4;border-radius:8px;padding:4px 10px;display:inline-block}}
.q{{border-left:3px solid var(--ember);padding-left:12px}}
.q b{{color:var(--ember)}}
.ifq{{font-size:15px;color:var(--slate)}}
@media print{{body{{padding:0;background:#fff;font-size:13px}}.tips,.go{{display:none}}.s{{border:0;border-bottom:1px solid var(--rule);border-radius:0;padding:10px 0;margin:0}}h1{{font-size:26px}}}}
</style></head><body><main>
<h1>Follow the Water: speaker notes</h1>
<p class="sub">SDG 6 · Clean Water &amp; Sanitation · Anders Imbrie · about {total // 60}:{total % 60:02d} plus class discussion</p>
<ul class="tips">
<li><b>Grey boxes</b> are clicks and stage directions. Lines with a <b>red bar</b> are questions for the class.</li>
<li>Some slides reveal extra parts on a click. The script marks each one.</li>
<li><b>Practice mode:</b> open the website with <b>?practice</b> at the end of the address, or press <b>R</b>. The slides shrink and these notes sit underneath, with the part for each click highlighted.</li>
<li>Present with <b>P</b> to get these notes, a timer and the next slide on your laptop while the slides are on the projector.</li>
</ul>
{''.join(cards)}
</main></body></html>
"""
    (ROOT / "speaker-notes.html").write_text(page, encoding="utf-8")
    return total


if __name__ == "__main__":
    update_deck()
    t = build_page()
    print(f"notes updated for {len(SLIDES)} slides, total {t // 60}:{t % 60:02d}")
