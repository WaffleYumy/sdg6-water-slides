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
    ("open", "Cold open", "0:20", "Start with a headline they have probably seen.", [
        "[Don’t click yet.]",
        "Has anyone seen a headline like this? ChatGPT “drinks” a bottle of water for every 20 to 50 questions.",
        "That’s from a real study at UC Riverside in 2023.",
        "[Click: the question appears.]",
        "So it’s true. But is AI really the main water problem? That’s what I looked into.",
        "[Click: the title appears.]",
    ]),
    ("title", "Follow the water", "0:30", "There is very little water we can actually use.", [
        "I’m Anders, and my topic is UN Goal 6: clean water and sanitation.",
        "[Click: the water spheres come out of the Earth.]",
        "If you rolled all the water on Earth into one ball, it would be about 860 miles across. The Earth is almost 8,000.",
        "All the fresh water that isn’t frozen would be about 170 miles, and most of that is underground.",
        "The lakes and rivers we actually use are the tiny dot with the ring. 35 miles. That’s what everyone shares.",
    ]),
    ("goal", "The goal", "0:35", "What SDG 6 is, how far off we are, and why it’s our problem.", [
        "Quick background on the goal itself. SDG 6 is the UN’s goal for clean water and sanitation for everyone by 2030. It has three main parts.",
        "Safe drinking water. 2.1 billion people still don’t have it.",
        "Safe toilets and handwashing. 3.4 billion people don’t have safe sanitation, and 354 million have no toilet at all.",
        "And using water more efficiently, so places don’t run short. That’s the part my talk focuses on.",
        "[Click: the bottom line appears.]",
        "At today’s pace, the world won’t make it. Progress on drinking water would have to be about six times faster. 2030 is only a few years away, so this is the world we’ll be working in.",
        "If asked: “safely managed” means water that’s at home, available when you need it, and not contaminated. Some people have a water source that doesn’t meet all three.",
    ]),
    ("terms", "Key terms + poll", "0:55", "Four words, then a guess from the class.", [
        "[Wait for the chapter card to pass.]",
        "A few words you need for the rest of this.",
        "Withdrawal is water we take from a river, a lake or underground. A lot of it goes back.",
        "Consumption is water that doesn’t come back. It evaporates or ends up in a product.",
        "Water stress means a place is using almost all the water it has.",
        "A water footprint is all the water behind something you buy. One cotton T-shirt takes about 2,700 liters.",
        "Q: Okay, what do you guys think? Take every data center in the US, running for a whole year. How long would it take US farms to use that much water? A, a week. B, a day. C, six hours. D, one hour.",
        "[Count hands. Tap each option once per hand.]",
        "[Click: the answer appears.]",
        "It’s C, about six hours.",
        "US data centers used about 17 billion gallons of water in 2023. US farms use about 73 billion gallons in one day. So a whole year of data centers is about five and a half hours of farming.",
        "Even if you count the water at the power plants that run them, it’s about three days.",
        "If asked: the two numbers are from different years, 2015 and 2023, so it’s a rough comparison. The gap is still huge.",
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
    ("hook", "Not off the hook", "0:40", "AI isn’t the big water problem, but it still matters.", [
        "That doesn’t mean AI has no water problem. Two things.",
        "First, data centers and almonds use water the same way. Both evaporate it. But they use different water.",
        "Data centers often use treated drinking water from the town. Almonds use river water and groundwater that took thousands of years to build up.",
        "[Click: the electricity side.]",
        "Second, the bigger issue is electricity. Data centers used about 4.4% of US electricity in 2023. By 2028 it could be as much as 12%.",
        "And the power plants behind them use about 12 times more water than the data centers do.",
        "So what would help most is clean power, and building data centers in places with enough water.",
        "If asked: not every data center uses drinking water. Some, like some of Google’s, use recycled wastewater. And almonds pump more groundwater in drought years.",
    ]),
    ("real", "The real problem", "0:55", "The real problem is farms, pipes and people.", [
        "[Wait for the chapter card to pass.]",
        "So where is the real problem? Three places.",
        "Farms. 71% of the fresh water people take goes to agriculture.",
        "Pipes. Cities lose 126 billion cubic meters of clean, treated water a year to leaks. That’s about four million liters a second. The counter started when this slide opened.",
        "People. 2.1 billion people, about one in four, don’t have safe drinking water at home. Each orange figure is one of them.",
        "And by 2030, demand for water is expected to be 40% higher than supply.",
        "Q: If you could fix one of these, which one would you pick?",
    ]),
    ("business", "Who’s fixing it", "1:05", "Tech is moving fastest. Farms need the most help.", [
        "[Wait for the chapter card to pass.]",
        "So what are companies actually doing?",
        "On the left, data centers. Since 2024, Microsoft’s new data center designs cool the chips in a closed loop. That saves about 125 million liters per site each year. Good for the planet, and it saves money.",
        "Amazon also reported its data center water use for the first time: 2.5 billion gallons in 2025. Being open about it helps with the towns they’re in.",
        "On the right, the bigger problem. N-Drip makes cheap drip irrigation for small farms that runs on gravity. In a rice trial it used 57% less water.",
        "And Levi’s cut the water used to finish jeans by up to 96%.",
        "Tech companies get the bad headlines, but they’re moving fastest. Farms use the most water and need the most help.",
        "If asked: farmers sometimes use the water they save to plant more. So saving water only works if there are also limits on total use.",
    ]),
    ("moves", "Three moves", "0:45", "My recommendations, using People, Profit and Planet.", [
        "[Wait for the Earth to rise.]",
        "So what should businesses do? Three things.",
        "People: build where there’s enough water, and put money back into the local water system.",
        "Profit: treat water as a business risk. Droughts can shut down factories, and leaky pipes waste about 39 billion dollars a year.",
        "Planet: focus on farms, since they use 71% of the water. Help suppliers switch to drip irrigation, and reuse water.",
        "To sum up: water problems are local, but supply chains are global. The headlines are about AI, but the biggest gains are on farms and in leaky pipes.",
        "Q: So what do you guys think, would you build a data center in Arizona? Why or why not?",
        "[Take two or three answers.]",
    ]),
    ("aiuse", "How I used AI", "0:20", "Required by the assignment. Be specific.", [
        "The assignment asks how I used AI. I used Claude, made by Anthropic.",
        "It helped me find sources, pointed out where they disagreed, helped plan the timing, and built this website.",
        "I picked the topic and the outline, and I checked the numbers against the original sources.",
        "One thing I learned: it sometimes gave different numbers for the same fact, so you have to check.",
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
