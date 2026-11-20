#!/usr/bin/env python3
"""Compose entry.png: 'The Daily World' front page for Wednesday 19 November 2026.

A dense broadsheet in one 1024x1024 image: folio, masthead, date bar, the ICJ
lead, six panels and a three-column wire block. Layout is measure-first: every
block is wrapped and measured before it is drawn, a global type scale is
lowered until the whole page fits, and the script asserts nothing overflows.
Deterministic: same fonts + same text -> same bytes.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "fonts"
OUT = HERE / "entry.png"

W = H = 1024
MARGIN = 38
CW = W - 2 * MARGIN  # content width

PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (168, 12, 28)
GREY = (90, 86, 78)
WHITE = (250, 248, 243)

SERIF_DISP = FONTS / "NotoSerifDisplay-Black.ttf"
SERIF_BOLD = FONTS / "NotoSerif-Bold.ttf"
SANS = FONTS / "NotoSans-ExtraBold.ttf"
LIB = FONTS / "LiberationSerif-Regular.ttf"
LIB_IT = FONTS / "LiberationSerif-Italic.ttf"


def font(path, size, variation=None):
    f = ImageFont.truetype(str(path), int(round(size)))
    if variation:
        f.set_variation_by_name(variation)
    return f


def sans(size, weight):
    return font(SANS, size, weight)


def tw(draw, text, f):
    return draw.textlength(text, font=f)


def wrap(draw, text, f, width):
    """Greedy word wrap; returns list of lines. Asserts no single word overflows."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if tw(draw, trial, f) <= width:
            cur = trial
        else:
            assert tw(draw, word, f) <= width, f"word too wide: {word!r}"
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tracked_width(draw, text, f, tracking):
    return sum(tw(draw, ch, f) for ch in text) + tracking * max(0, len(text) - 1)


def draw_tracked(draw, x, y, text, f, fill, tracking):
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=f, fill=fill)
        cx += tw(draw, ch, f) + tracking
    return cx - tracking


# ---------------------------------------------------------------- content ---

LEAD = {
    "kicker": "THE HAGUE · INTERNATIONAL COURT OF JUSTICE",
    "banner": ["World Court: Myanmar committed", "genocide against the Rohingya"],
    "subhead": (
        "A 9–6 verdict, the first genocide finding against a state in the "
        "court’s history, over the 2017 crackdown. Rohingya refugees in "
        "Bangladesh cheered; Myanmar denies genocide."
    ),
}

PANELS = [
    {
        "kicker": "SHENZHEN · FIRST THREE-WAY SUMMIT",
        "headline": "Trump, Xi & Putin sign a peace declaration",
        "body": (
            "The three leaders meet on the APEC sidelines and sign a four-point "
            "pact. Berlin’s Merz warns against a new Yalta over Europe’s head."
        ),
    },
    {
        "kicker": "KERCH STRAIT · THE WAR",
        "headline": "Ukraine hits the Crimea Bridge a third time",
        "body": (
            "Kyiv strikes the bridge for the third time in four days; traffic is "
            "halted and a span damaged. Putin vows a far harsher reply."
        ),
    },
    {
        "kicker": "NEW YORK · THE RECORD IPO",
        "headline": "Anthropic closes +17% on a record debut",
        "body": (
            "The first pure-AI listing raised about $81 billion, the largest IPO "
            "ever — yet the S&P 500 still fell 2%, a fifth straight loss."
        ),
    },
    {
        "kicker": "SANTA CLARA · CHIP WARS",
        "headline": "Nvidia probed after Huang’s exit",
        "body": (
            "California’s attorney general subpoenas Nvidia over its China "
            "chip-risk disclosures after CEO Jensen Huang resigned. AMD fell 7%."
        ),
    },
    {
        "kicker": "RIYADH · MIDDLE EAST",
        "headline": "Houthi missile hits Riyadh’s tallest tower",
        "body": (
            "The Public Investment Fund tower’s windows shatter; no injuries. "
            "The Houthis say Saudi strikes killed 10 in Sanaa."
        ),
    },
    {
        "kicker": "BERLIN · EUROPE",
        "headline": "Allies in Berlin: ready to talk with Russia",
        "body": (
            "Ukraine’s European allies agree a united line for negotiations. "
            "Kushner floats NATO-style guarantees; Macron reopens the NATO question."
        ),
    },
]

WIRE = [
    ("HORMUZ", "Iran escalates tanker attacks; a tanker burns after hitting a mine."),
    ("WASHINGTON", "Senate rejects a bid to limit Trump’s Iran war powers, 51–48."),
    ("GAZA", "Israeli troops complete a ground operation beyond the Yellow Line."),
    ("PARIS", "IEA: the Iran war leaves lasting scars on energy markets; Brent at $89.72."),
    ("DHAKA", "Violence over Hasina’s planned return: two killed, some 300 arrested."),
    ("ANTALYA", "COP31 draft drops all fossil-fuel language."),
    ("CARACAS", "US and Venezuela sign a military cooperation deal."),
    ("INTERSTELLAR SPACE", "Voyager 1 reaches one light-day from Earth, 26 billion km out."),
    ("MERCURY", "BepiColombo enters orbit after an eight-year journey."),
    ("NEW YORK", "GTA VI launches after 13 years: about $2.36 billion on day one."),
    ("PORT-AU-PRINCE", "Police raid kills 34 gang members in Martissant."),
    ("WASHINGTON", "Democrats nominate Jeffries for House speaker."),
    ("WASHINGTON", "The US loses its measles elimination status."),
    ("MRIMA HILL, KENYA", "US consortium wins a $60 billion critical-minerals deal."),
    ("COPENHAGEN", "Denmark ratifies a US security deal on Greenland."),
    ("YENNE, SENEGAL", "Dozens missing as a migrant boat capsizes."),
    ("LONDON", "Nearly 1 in 4 children worldwide live in conflict zones."),
    ("MADRID", "Sánchez admits mistakes in Spain’s election debate."),
    ("TOKYO", "Core inflation hits a year high; the Nikkei falls 4.68%."),
    ("LONDON", "Gold falls to a 14-month low at $3,596."),
    ("BADME", "Drone and artillery strikes as Ethiopia and Eritrea mass forces."),
    ("YONGBYON", "IAEA: North Korea has expanded uranium enrichment."),
    ("DAR ES SALAAM", "Opposition leader Lissu convicted of sedition."),
    ("SUVA", "Fiji and Tonga declare El Niño drought emergencies."),
    ("BRUSSELS", "The European Commission confirms an AI-powered cyberattack."),
    ("JURF AL-NASR, IRAQ", "Baghdad orders Kataib Hezbollah out by Friday."),
    ("MEXICO CITY", "EU–Mexico deal removes 95% of farm tariffs."),
    ("EASTERN CONGO", "Strain-specific Ebola vaccines head into trials."),
]

STORY_COUNT = 1 + len(PANELS) + len(WIRE)


# ----------------------------------------------------------------- layout ---

def fit_size(draw, text, path, start, width, variation=None):
    size = start
    while size > 10 and tw(draw, text, font(path, size, variation)) > width:
        size -= 1
    return size


def rich_wrap(draw, segments, width):
    """Wrap [(text, font)] segments word by word; returns lines of (text, font) runs."""
    words = []
    for text, f in segments:
        for i, w in enumerate(text.split()):
            words.append((w, f, i == 0))
    lines, cur, cur_w = [], [], 0.0
    space_w = {}
    for w, f, _ in words:
        if f not in space_w:
            space_w[f] = tw(draw, " ", f)
        ww = tw(draw, w, f)
        add = ww if not cur else ww + space_w[cur[-1][1]]
        if cur and cur_w + add > width:
            lines.append(cur)
            cur, cur_w = [(w, f)], ww
        else:
            cur.append((w, f))
            cur_w += add
    if cur:
        lines.append(cur)
    return lines


def layout(draw, S):
    """Return (total_height, plan) for type scale S without drawing."""
    plan = {}
    y = 26 * S

    # folio
    plan["folio_y"] = y
    y += 15 * S + 8 * S
    plan["folio_rule_y"] = y
    y += 10 * S

    # masthead (fit to width)
    msize = fit_size(draw, "The Daily World", SERIF_DISP, 118 * S, CW, "Black")
    plan["masthead"] = (y, msize)
    y += msize * 1.04 + 8 * S

    # date bar
    plan["bar"] = (y, 44 * S)
    y += 44 * S + 14 * S

    # lead
    plan["lead_kicker_y"] = y
    y += 17 * S + 4 * S
    bsize = min(
        fit_size(draw, line, SERIF_DISP, 62 * S, CW, "Black") for line in LEAD["banner"]
    )
    plan["banner"] = (y, bsize)
    y += 2 * bsize * 1.04 + 6 * S
    sub_f = font(LIB_IT, 19 * S)
    sub_lines = wrap(draw, LEAD["subhead"], sub_f, CW)
    plan["subhead"] = (y, sub_lines, 19 * S)
    y += len(sub_lines) * 19 * S * 1.3 + 12 * S

    # panels: 3 rows of 2
    col_w = (CW - 30 * S) / 2
    plan["panels_start"] = y
    plan["panel_rows"] = []
    pk_f = sans(13 * S, "ExtraBold")
    ph_f = font(SERIF_BOLD, 25 * S)
    pb_f = font(LIB, 15 * S)
    for r in range(3):
        row = []
        row_h = 0
        for c in range(2):
            p = PANELS[r * 2 + c]
            hl = wrap(draw, p["headline"], ph_f, col_w)
            bl = wrap(draw, p["body"], pb_f, col_w)
            h = 13 * S + 5 * S + len(hl) * 25 * S * 1.14 + 3 * S + len(bl) * 15 * S * 1.3
            row.append((hl, bl))
            row_h = max(row_h, h)
        plan["panel_rows"].append((y, row, row_h))
        y += row_h + 11 * S
    y -= 11 * S
    y += 10 * S

    # wire header
    plan["wire_header_y"] = y
    y += 18 * S + 8 * S

    # wire columns: contiguous 3-way split balanced by measured height
    wcol_w = (CW - 2 * 22 * S) / 3
    text_w = wcol_w - 15 * S
    wp_f = sans(11.5 * S, "Bold")
    wb_f = font(LIB, 12.5 * S)
    briefs = []
    for place, body in WIRE:
        segs = [(place, wp_f), (" — ", wb_f), (body, wb_f)]
        lines = rich_wrap(draw, segs, text_w)
        briefs.append((place, lines, len(lines) * 12.5 * S * 1.3))
    best = None
    for i in range(1, len(briefs) - 1):
        for j in range(i + 1, len(briefs)):
            hs = [
                sum(b[2] for b in briefs[:i]) + 5 * S * (i - 1),
                sum(b[2] for b in briefs[i:j]) + 5 * S * (j - i - 1),
                sum(b[2] for b in briefs[j:]) + 5 * S * (len(briefs) - j - 1),
            ]
            m = max(hs)
            if best is None or m < best[0]:
                best = (m, i, j)
    plan["wire"] = (y, briefs, best[1], best[2], wcol_w, text_w)
    y += best[0] + 10 * S

    # footer
    plan["footer_y"] = y
    y += 14 * S
    return y, plan


def render():
    probe = ImageDraw.Draw(Image.new("RGB", (W, H)))
    S = 1.0
    while True:
        total, plan = layout(probe, S)
        if total <= H - 14 or S <= 0.7:
            break
        S -= 0.02
    assert total <= H - 8, f"page overflows at scale {S}: {total}"

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0 = MARGIN

    # folio
    fy = plan["folio_y"]
    f_f = sans(14 * S, "Bold")
    d.text((x0, fy), "THE DAY’S NEWS · ONE PAGE · ONE IMAGE", font=f_f, fill=GREY)
    right = f"{STORY_COUNT} STORIES · EST. 2026 — NO. 19"
    d.text((x0 + CW - tw(d, right, f_f), fy), right, font=f_f, fill=GREY)
    ry = plan["folio_rule_y"]
    d.line([(x0, ry), (x0 + CW, ry)], fill=INK, width=2)

    # masthead
    my, msize = plan["masthead"]
    mf = font(SERIF_DISP, msize, "Black")
    label = "The Daily World"
    d.text((x0 + (CW - tw(d, label, mf)) / 2, my), label, font=mf, fill=INK)
    rule_y = my + msize * 1.04 + 2
    d.line([(x0, rule_y), (x0 + CW, rule_y)], fill=INK, width=3)
    d.line([(x0, rule_y + 4), (x0 + CW, rule_y + 4)], fill=INK, width=1)

    # date bar
    by, bh = plan["bar"]
    d.rectangle([x0, by, x0 + CW, by + bh], fill=INK)
    bf = sans(23 * S, "Black")
    btxt = "WEDNESDAY · 19 NOVEMBER 2026"
    bw = tracked_width(d, btxt, bf, 3)
    draw_tracked(d, x0 + (CW - bw) / 2, by + bh / 2 - 23 * S * 0.62, btxt, bf, WHITE, 3)

    # lead
    kf = sans(16 * S, "ExtraBold")
    kw = tracked_width(d, LEAD["kicker"], kf, 1.2)
    draw_tracked(d, x0 + (CW - kw) / 2, plan["lead_kicker_y"], LEAD["kicker"], kf, RED, 1.2)
    byy, bsize = plan["banner"]
    banf = font(SERIF_DISP, bsize, "Black")
    for line in LEAD["banner"]:
        d.text((x0 + (CW - tw(d, line, banf)) / 2, byy), line, font=banf, fill=INK)
        byy += bsize * 1.04
    sy, sub_lines, sub_size = plan["subhead"]
    sf = font(LIB_IT, sub_size)
    for line in sub_lines:
        d.text((x0 + (CW - tw(d, line, sf)) / 2, sy), line, font=sf, fill=INK)
        sy += sub_size * 1.3

    # panels
    col_w = (CW - 30 * S) / 2
    pk_f = sans(13 * S, "ExtraBold")
    ph_f = font(SERIF_BOLD, 25 * S)
    pb_f = font(LIB, 15 * S)
    rows = plan["panel_rows"]
    for idx, (ryy, row, row_h) in enumerate(rows):
        if idx > 0:
            d.line([(x0, ryy - 6 * S), (x0 + CW, ryy - 6 * S)], fill=GREY, width=1)
        mid = x0 + col_w + 15 * S
        d.line([(mid, ryy + 2), (mid, ryy + row_h - 2)], fill=GREY, width=1)
        for c, (hl, bl) in enumerate(row):
            p = PANELS[idx * 2 + c]
            px = x0 if c == 0 else x0 + col_w + 30 * S
            py = ryy
            draw_tracked(d, px, py, p["kicker"], pk_f, RED, 0.8)
            py += 13 * S + 5 * S
            for line in hl:
                d.text((px, py), line, font=ph_f, fill=INK)
                py += 25 * S * 1.14
            py += 3 * S
            for line in bl:
                d.text((px, py), line, font=pb_f, fill=INK)
                py += 15 * S * 1.3

    # wire header
    wy = plan["wire_header_y"]
    wf = sans(17 * S, "Black")
    wtxt = "THE WIRE — MORE OF WEDNESDAY"
    ww = tracked_width(d, wtxt, wf, 1.5)
    hx = x0 + (CW - ww) / 2
    mid_y = wy + 8 * S
    d.line([(x0, mid_y), (hx - 14, mid_y)], fill=INK, width=2)
    d.line([(hx + ww + 14, mid_y), (x0 + CW, mid_y)], fill=INK, width=2)
    draw_tracked(d, hx, wy, wtxt, wf, INK, 1.5)

    # wire columns
    wyy, briefs, i, j, wcol_w, text_w = plan["wire"]
    wp_f = sans(11.5 * S, "Bold")
    wb_f = font(LIB, 12.5 * S)
    cols = [briefs[:i], briefs[i:j], briefs[j:]]
    for ci, col in enumerate(cols):
        cx = x0 + ci * (wcol_w + 22 * S)
        cy = wyy
        for place, lines, bh in col:
            d.rectangle([cx, cy + 3.5 * S, cx + 7 * S, cy + 10.5 * S], fill=RED)
            ly = cy
            for line in lines:
                lx = cx + 15 * S
                for wtxt2, wf2 in line:
                    d.text((lx, ly), wtxt2, font=wf2, fill=INK if wf2 is wb_f else RED)
                    lx += tw(d, wtxt2, wf2) + tw(d, " ", wf2)
                ly += 12.5 * S * 1.3
            cy += bh + 5 * S

    # footer
    ff = font(LIB_IT, 13.5 * S)
    ftxt = "Compiled from the day’s reporting by Reuters, the BBC and international news wires."
    fy2 = plan["footer_y"]
    d.line([(x0, fy2 - 5 * S), (x0 + CW, fy2 - 5 * S)], fill=GREY, width=1)
    d.text((x0 + (CW - tw(d, ftxt, ff)) / 2, fy2), ftxt, font=ff, fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    print(f"scale={S:.2f} total_height={total:.0f} stories={STORY_COUNT} -> {OUT}")


if __name__ == "__main__":
    render()
