"""Single source for the talk script.

Run:  python notes/script.py
It writes the notes into each slide of index.html (press N, or P for presenter view)
and builds speaker-notes.html, a printable version of the same script.
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Each slide: (id, title, time, point, [lines]).
# Lines starting with "[" are stage directions; "Q:" lines are questions for the class;
# "If asked:" lines are backup answers.
SLIDES = [
    ("open", "Cold open", "0:20", "Hook them with a headline they’ve already seen.", [
        "[Wait a beat before you speak. Don’t click yet.]",
        "Raise your hand if you’ve seen a headline like this: ChatGPT “drinks” a bottle of water for every 20 to 50 questions.",
        "That comes from a real 2023 study at UC Riverside.",
        "[Click: the question appears.]",
        "So it’s real. But is AI actually THE water problem? Today I’m going to follow the water and show you where it really goes.",
        "[Click: a drop falls into the water and the title appears.]",
    ]),
    ("title", "Follow the water", "0:35", "Show how little usable water there actually is.", [
        "I’m Anders, and my goal is SDG 6: clean water and sanitation for everyone.",
        "[Click: the water spheres come out of the Earth.]",
        "First, some scale. If you rolled every drop of water on Earth into one ball, it would be 860 miles wide, next to an Earth almost 8,000 miles wide.",
        "All the liquid fresh water would be about 170 miles, and most of that is underground.",
        "The lakes and rivers we actually pull from? 35 miles. That little dot with the ring around it. That’s what everyone is fighting over.",
        "I’ll cover five things: the basics, the AI myth, the real problem, who’s fixing it, and what businesses should do.",
    ]),
    ("terms", "Key terms + poll", "0:45", "Give them the four words they need, then get them guessing.", [
        "[A chapter title card washes across the screen. Let it pass, then start.]",
        "Four words change this whole story.",
        "Withdrawal: water we take from a river, lake or aquifer. A lot of it goes back.",
        "Consumption: water that doesn’t come back. It evaporates or ends up inside a product.",
        "Water stress: when a place is using close to all the water it has. It’s always local.",
        "Water footprint: all the water behind something you buy, across its whole supply chain. One cotton T-shirt takes about 2,700 liters.",
        "Q: All the data centers in the US, running for a whole year. How long does it take US farms to use up that same amount of water? A, a month? B, a week? C, six hours?",
        "[Count hands. Tap each option once per hand.]",
        "Hold that thought.",
    ]),
    ("equal", "Not all water use is equal", "1:00", "It’s not how much water. It’s where and when.", [
        "Look at the units first. Farms and power plants are per DAY. Data centers are per YEAR.",
        "Now look at what happens to the water. Power plants take the most, 133 billion gallons a day, but only about 3% is used up. The rest goes back to the river, just warmer.",
        "Farms use up about 62% of what they take.",
        "Data-center cooling towers evaporate 70 to 80%, and it all comes out of one town’s supply.",
        "So the question isn’t how much. It’s where and when. A gallon in rainy Seattle isn’t the same as a gallon in Phoenix during a drought.",
    ]),
    ("ai", "AI and water", "1:15", "AI’s water use is small nationally but can hurt locally.", [
        "The answer is C: about six hours.",
        "All US data centers used about 17 billion gallons directly in 2023. US farms use up about 73 billion gallons in a single day. So a whole year of data centers is about five and a half hours of farming.",
        "[Click: the three rings appear.]",
        "Even if you add the water used by the power plants that run them, it’s about three days.",
        "[Click: downsides and upsides appear.]",
        "That doesn’t mean data centers don’t matter. They cluster in a few towns, often dry ones in places like Arizona and Texas. The water at the power plants behind them is about 12 times their direct use, and their water use could double or quadruple by 2028.",
        "But there’s good news too: new closed-loop designs use almost no cooling water, efficiency is improving fast, and host towns get tax revenue.",
        "Q: Did anyone come in thinking AI was the biggest water problem?",
        "If asked: the two numbers are from different years, 2015 and 2023, so it’s a rough comparison, but the gap is huge either way.",
    ]),
    ("versus", "ChatGPT vs. almonds", "0:45", "Make it personal: the AI everyone uses vs. a snack nobody worries about.", [
        "[Don’t give anything away. Let the scale wobble.]",
        "Let’s make it personal. Quick bet.",
        "A: every question the whole world asks ChatGPT, for an entire year. That’s about two and a half billion questions a day.",
        "B: every almond orchard in California, for just one month.",
        "Q: Hands up if you think A uses more. Now B. Think about it, this one’s closer than you’d expect.",
        "[Count hands, then click. The scale slams down on the almonds.]",
        "It’s not close at all. A whole year of ChatGPT: about 78 million gallons. One month of almonds: about 76 billion. The almonds win by about a thousand times.",
        "[Click: the punchline takes over the screen. Let the bars finish filling.]",
        "So let’s stretch it out. Run ChatGPT for 30 straight years, and it still uses less water than California’s almonds use in a single day.",
        "If asked: the ChatGPT number is OpenAI’s own, 0.000085 gallons per question, and it only counts answering questions, not training or the power plants. Independent researchers estimate about four times more. Even then it’s about 8 years of ChatGPT for one day of almonds.",
        "If asked: the almond number is the almond industry’s own estimate, the lowest one out there, and it’s based on 2013, when there were fewer orchards. Other groups estimate almost twice as much, so the real gap is probably even bigger.",
    ]),
    ("live", "Live: right now", "0:25", "Show the gap happening in real time.", [
        "[The camera swoops down from straight overhead. Let it land, then point at the counters. They started the moment the slide opened.]",
        "These counters started when this slide came up. They run at the same rates as the last slide.",
        "ChatGPT, the whole world using it: about two and a half gallons a second. That’s the drip on the left.",
        "California almonds: almost 29 thousand gallons a second. That’s a full Olympic swimming pool every 23 seconds.",
        "At ChatGPT’s rate, filling one pool would take about three days.",
        "Every time the almond pool fills, that whole pool of water lifts out and lines up in front. Watch the row grow while I talk.",
        "[Glance at the pools-filled count, then move on.]",
        "If asked: these are yearly averages, the yearly totals divided by the seconds in a year. Almond orchards use more in summer and less in winter.",
    ]),
    ("real", "The real problem", "1:00", "The real problem is farms, pipes and people.", [
        "[A chapter title card washes across the screen. Let it pass, then start.]",
        "So where IS the real problem? Three places.",
        "Farms: 71% of all the fresh water humans take goes to agriculture.",
        "Pipes: cities lose 126 billion cubic meters of treated, already-paid-for water every year to leaks. That’s about four million liters every second. That counter has been running since this slide opened.",
        "People: 2.1 billion people, one in four, still don’t have safe drinking water at home. Look at the crowd: every orange person is one of them.",
        "And it’s getting tighter. By 2030, demand is expected to be 40% higher than supply.",
        "Q: Which of these three would you fix first?",
    ]),
    ("business", "Who’s fixing it", "1:15", "Tech is moving fastest, but farms need the most help.", [
        "[A chapter title card washes across the screen. Let it pass, then start.]",
        "Business is moving, but on which problem?",
        "Left side, data centers. Since 2024, every new Microsoft data-center design cools the chips in a closed loop, saving about 125 million liters per site every year. That’s Planet, and also Profit, because water costs money.",
        "Amazon published its total data-center water use for the first time: 2.5 billion gallons in 2025. It says about two-thirds goes back to local communities. Being open about it is a People move.",
        "Right side, the real problem. N-Drip makes gravity-powered drip irrigation for small farms. In a rice trial it used 57% less water than flooding the field.",
        "And Levi’s cut the water used to finish jeans by up to 96%.",
        "My take: tech has the worst headlines, but it’s moving fastest. Farms, the biggest user, need the most help.",
        "If asked: farmers sometimes use saved water to plant more, so efficiency alone isn’t enough. It has to come with limits on total use.",
    ]),
    ("moves", "Three moves", "0:50", "My recommendations, using People, Profit and Planet.", [
        "[The Earth rises along the bottom of the slide. Let it land before you start.]",
        "So what should any business do? Three moves.",
        "People: build where water is plentiful, and invest back into the local water systems you draw from.",
        "Profit: treat water as a business risk. Droughts shut down factories, and leaky pipes waste about 39 billion dollars a year.",
        "Planet: go after the 71%. Help your farm suppliers switch to efficient irrigation, and reuse water wherever you can.",
        "My conclusion: water is a local problem with global supply chains. The headlines are about AI, but the biggest wins are on farms and in pipes.",
        "Q: Last question. Would you build your next data center in Arizona? Why or why not?",
        "[Let two or three people answer.]",
    ]),
    ("aiuse", "How I used AI", "0:20", "Required by the assignment: be specific and honest.", [
        "As the assignment asks, here’s how I used AI. I used Claude, made by Anthropic.",
        "It searched news, UN and USGS sources, flagged where sources disagreed, helped plan the timing, and built this website.",
        "I chose the angle, wrote the outline, and checked the numbers against their sources.",
        "Biggest lesson: AI gave me different numbers for the same fact, so you still have to check the original source.",
    ]),
    ("sources", "Works cited", "0:05", "Close and take questions.", [
        "All my sources are here, and the links work on the website.",
        "Thank you. Any questions?",
    ]),
]


def plain(lines):
    return "\n".join(lines)


def update_deck():
    path = ROOT / "index.html"
    src = path.read_text(encoding="utf-8")
    for sid, title, time, point, lines in SLIDES:
        body = f"({time}) Point: {point}\n\n" + plain(lines)
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
        return f'<p class="q"><b>Ask:</b>{e[2:]}</p>'
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
<li><b>Grey boxes</b> are clicks and stage directions. <b>Red lines</b> are questions to ask the class.</li>
<li>Slides 1, 2 and 5 reveal extra parts on a click. The script marks each one.</li>
<li>Present with <b>P</b> to get these notes, a timer and the next slide on your laptop while the slides are on the projector.</li>
<li>Running long? Shorten slide 4 (skip the Seattle line) and slide 7 (skip Amazon).</li>
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
