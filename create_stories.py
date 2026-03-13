#!/usr/bin/env python3
"""
OilExam.tech - 3 New Instagram Stories (Different Ideas)
Story 6: "Quiz Challenge" - Interactive quiz teaser
Story 7: "Testimonial / Score Reveal" - Student success story
Story 8: "Daily Word Flashcard" - Learn one word today
"""

from PIL import Image, ImageDraw, ImageFont
import subprocess, os, math, tempfile, shutil

WIDTH, HEIGHT = 1080, 1920
FPS = 24

# ═══ BRAND COLORS ═══
PRIMARY    = (67, 97, 238)
MID_BLUE   = (90, 123, 245)
LIGHT_BLUE = (123, 147, 248)
PALE_BLUE  = (168, 186, 255)
DARK_BG    = (26, 35, 50)
WHITE      = (255, 255, 255)
GREEN      = (72, 187, 120)
RED        = (229, 62, 62)
ORANGE     = (246, 173, 85)
PINK       = (237, 100, 166)
YELLOW     = (250, 204, 21)
GOLD       = (255, 215, 0)
DARK_GREEN = (20, 60, 45)
TEAL       = (56, 178, 172)

# ═══ FONTS ═══
FONT_DIR  = "/root/OilexamVideo/fonts"
AR_BLACK  = f"{FONT_DIR}/Tajawal-Black.ttf"
AR_BOLD   = f"{FONT_DIR}/Tajawal-ExtraBold.ttf"
AR_REG    = f"{FONT_DIR}/Tajawal-Regular.ttf"
EN_BOLD   = f"{FONT_DIR}/PlusJakartaSans-Bold.ttf"
EN_REG    = f"{FONT_DIR}/PlusJakartaSans-Regular.ttf"


# ═══ UTILITIES ═══

def gradient_bg(w, h, c1, c2):
    img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        r = y / h
        color = tuple(int(c1[i]*(1-r) + c2[i]*r) for i in range(3))
        draw.line([(0, y), (w, y)], fill=color)
    return img


def radial_gradient(img, cx, cy, radius, center_color, edge_color):
    draw = ImageDraw.Draw(img)
    for r in range(radius, 0, -2):
        ratio = r / radius
        c = tuple(int(center_color[i]*(1-ratio) + edge_color[i]*ratio) for i in range(3))
        draw.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=c)


def center_text(draw, text, y, font, fill=WHITE):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (WIDTH - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def ease_out(t):
    return 1 - (1 - min(1.0, t)) ** 3


def ease_in_out(t):
    t = min(1.0, t)
    return 3*t*t - 2*t*t*t


def lerp_color(c1, c2, t):
    t = max(0, min(1, t))
    return tuple(int(c1[i]*(1-t) + c2[i]*t) for i in range(3))


def brand_bg(dark_shift=0):
    c1 = tuple(max(0, c - dark_shift) for c in DARK_BG)
    c2 = tuple(max(0, min(255, c + 15 - dark_shift)) for c in DARK_BG)
    return gradient_bg(WIDTH, HEIGHT, c1, c2)


def render_scene(func, dur, frame_dir, start_idx):
    n = int(dur * FPS)
    for i in range(n):
        p = i / n
        img = func(p)
        img.save(os.path.join(frame_dir, f"frame_{start_idx+i:05d}.png"))
    return start_idx + n


def encode_video(frame_dir, output):
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS),
        "-i", os.path.join(frame_dir, "frame_%05d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "medium", "-crf", "20",
        "-movflags", "+faststart", output
    ], check=True, capture_output=True)


def build_video(name, scenes, output):
    print(f"\n{'='*55}")
    print(f"  Building: {name}")
    print(f"{'='*55}")
    frame_dir = tempfile.mkdtemp(prefix=f"story_{name}_")
    idx = 0
    total_dur = 0
    for sname, func, dur in scenes:
        print(f"  > {sname} ({dur}s)...")
        idx = render_scene(func, dur, frame_dir, idx)
        total_dur += dur
    print(f"  Total: {idx} frames / {total_dur}s")
    print(f"  Encoding MP4...")
    encode_video(frame_dir, output)
    shutil.rmtree(frame_dir)
    size = os.path.getsize(output) / (1024*1024)
    print(f"  Done: {output} ({size:.1f} MB)")


# ════════════════════════════════════════════════════════════════
#  STORY 6: "Quiz Challenge" - تحدّي: تعرف الجواب؟
#  Concept: Show an oil exam question, options appear one by one,
#  timer ticks, then reveal the correct answer with celebration
# ════════════════════════════════════════════════════════════════

def s6_hook(p):
    """Hook: Challenge intro"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    e = ease_out(p * 3)

    # Pulsing question mark glow
    pulse = 0.7 + 0.3 * math.sin(p * 12)
    glow_r = int(250 * e * pulse)
    if glow_r > 5:
        radial_gradient(img, WIDTH//2, HEIGHT//2 - 250, glow_r,
                        lerp_color((0,0,0), PRIMARY, 0.5), (0,0,0))
        draw = ImageDraw.Draw(img)

    f_huge = ImageFont.truetype(EN_BOLD, 300)
    f_ar = ImageFont.truetype(AR_BLACK, 85)
    f_sub = ImageFont.truetype(AR_BOLD, 50)

    # Big question mark
    if e > 0.1:
        a = min(1, e * 1.5)
        c = lerp_color((0,0,0), PRIMARY, a)
        bbox = draw.textbbox((0,0), "?", font=f_huge)
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH-tw)//2, HEIGHT//2-450), "?", font=f_huge, fill=c)

    if e > 0.35:
        center_text(draw, "تحدّي سريع", HEIGHT//2-50, f_ar, WHITE)

    if p > 0.45:
        a = min(1, (p-0.45)*4)
        c = lerp_color((0,0,0), ORANGE, a)
        center_text(draw, "!تعرف الجواب", HEIGHT//2+80, f_sub, c)

    if p > 0.7:
        f_brand = ImageFont.truetype(EN_BOLD, 36)
        a = min(1, (p-0.7)*4)
        c = lerp_color((0,0,0), (80,100,140), a)
        center_text(draw, "oilexam.tech", 1700, f_brand, c)

    return img


def s6_question(p):
    """Show the question with options"""
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    f_q_label = ImageFont.truetype(EN_BOLD, 38)
    f_question = ImageFont.truetype(EN_BOLD, 52)
    f_q_ar = ImageFont.truetype(AR_BOLD, 42)
    f_option = ImageFont.truetype(EN_BOLD, 42)
    f_option_ar = ImageFont.truetype(AR_REG, 36)
    f_letter = ImageFont.truetype(EN_BOLD, 44)
    f_timer = ImageFont.truetype(EN_BOLD, 64)

    e = ease_out(p * 2.5)

    # Top badge
    if e > 0.1:
        badge_w, badge_h = 320, 60
        bx = (WIDTH - badge_w) // 2
        draw.rounded_rectangle([(bx, 150), (bx+badge_w, 150+badge_h)],
                               radius=30, fill=PRIMARY)
        center_text(draw, "OIL EXAM QUIZ", 158, f_q_label, WHITE)

    # Question card
    if e > 0.2:
        card_y = 280
        card_c = (35, 48, 68)
        draw.rounded_rectangle([(60, card_y), (WIDTH-60, card_y+320)],
                               radius=24, fill=card_c)
        # Top accent
        draw.rounded_rectangle([(60, card_y), (WIDTH-60, card_y+8)],
                               radius=4, fill=ORANGE)

    if e > 0.3:
        center_text(draw, "What does \"downstream\"", 320, f_question, WHITE)
        center_text(draw, "mean in the oil industry?", 385, f_question, WHITE)
        center_text(draw, "شنو معنى هالكلمة بصناعة النفط؟", 470, f_q_ar, PALE_BLUE)

    # Options
    options = [
        ("A", "Refining & Distribution", "التكرير والتوزيع", GREEN),
        ("B", "Drilling & Exploration", "الحفر والاستكشاف", MID_BLUE),
        ("C", "Pipeline Construction", "بناء الأنابيب", ORANGE),
        ("D", "Well Maintenance", "صيانة الآبار", PINK),
    ]

    for i, (letter, en_text, ar_text, color) in enumerate(options):
        th = 0.25 + i * 0.12
        if p > th:
            a = min(1, (p-th)*5)
            ep = ease_out((p-th)*3)
            y = 680 + i * 185

            xo = int((1-ep) * 300)

            # Option card
            card_c = lerp_color(DARK_BG, (35, 48, 68), a)
            draw.rounded_rectangle([(80+xo, y), (WIDTH-80, y+155)],
                                   radius=18, fill=card_c)

            # Letter circle
            letter_c = lerp_color(DARK_BG, color, a)
            draw.ellipse([(110+xo, y+20), (180+xo, y+90)], fill=letter_c)
            lb = draw.textbbox((0,0), letter, font=f_letter)
            lw = lb[2]-lb[0]
            draw.text((145+xo-lw//2, y+25), letter, font=f_letter,
                      fill=lerp_color(DARK_BG, WHITE, a))

            # Text
            tc = lerp_color(DARK_BG, WHITE, a)
            draw.text((200+xo, y+22), en_text, font=f_option, fill=tc)
            arc = lerp_color(DARK_BG, PALE_BLUE, a)
            draw.text((200+xo, y+80), ar_text, font=f_option_ar, fill=arc)

    # Timer at bottom
    if p > 0.6:
        timer_val = max(0, int(10 - (p-0.6)*25))
        timer_str = f":{timer_val:02d}"
        pulse = 0.85 + 0.15*math.sin(p*15)
        tc = RED if timer_val < 4 else WHITE
        center_text(draw, timer_str, 1520, f_timer, tc)

        # Timer bar
        bar_pct = max(0, timer_val / 10)
        bar_y = 1610
        bx = (WIDTH-700)//2
        draw.rounded_rectangle([(bx, bar_y), (bx+700, bar_y+12)],
                               radius=6, fill=(40,52,72))
        bw = int(700 * bar_pct)
        if bw > 6:
            bc = RED if timer_val < 4 else PRIMARY
            draw.rounded_rectangle([(bx, bar_y), (bx+bw, bar_y+12)],
                                   radius=6, fill=bc)

    return img


def s6_reveal(p):
    """Reveal the correct answer"""
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(AR_BLACK, 70)
    f_answer = ImageFont.truetype(EN_BOLD, 56)
    f_answer_ar = ImageFont.truetype(AR_BLACK, 52)
    f_letter = ImageFont.truetype(EN_BOLD, 80)
    f_explain = ImageFont.truetype(AR_REG, 40)
    f_brand = ImageFont.truetype(EN_BOLD, 36)

    e = ease_out(p * 3)

    # Celebration glow
    glow_r = int(300 * e)
    if glow_r > 5:
        radial_gradient(img, WIDTH//2, HEIGHT//2-200, glow_r,
                        lerp_color(DARK_BG, GREEN, 0.35), DARK_BG)
        draw = ImageDraw.Draw(img)

    if e > 0.1:
        center_text(draw, "!الجواب الصحيح", int(250+(1-e)*60), f_title, GREEN)

    # Big answer card
    if e > 0.25:
        card_y = 420
        draw.rounded_rectangle([(70, card_y), (WIDTH-70, card_y+380)],
                               radius=28, fill=(30, 55, 45))
        draw.rounded_rectangle([(70, card_y), (WIDTH-70, card_y+10)],
                               radius=5, fill=GREEN)

        # A circle
        draw.ellipse([(WIDTH//2-60, card_y+40), (WIDTH//2+60, card_y+160)],
                     fill=GREEN)
        center_text(draw, "A", card_y+55, f_letter, WHITE)

        center_text(draw, "Refining & Distribution", card_y+190, f_answer, WHITE)
        center_text(draw, "التكرير والتوزيع", card_y+270, f_answer_ar, GREEN)

    # Explanation
    if p > 0.4:
        a = min(1, (p-0.4)*4)
        c = lerp_color(DARK_BG, PALE_BLUE, a)
        center_text(draw, "Downstream = مرحلة التكرير", 880, f_explain, c)
        center_text(draw, "والتوزيع والبيع للمستهلك", 940, f_explain, c)

    # Decorative sparkles
    if p > 0.3:
        sparkle_positions = [(200, 350), (880, 320), (150, 900), (930, 880),
                            (300, 1100), (780, 1050)]
        for i, (sx, sy) in enumerate(sparkle_positions):
            th = 0.3 + i*0.06
            if p > th:
                sa = min(1, (p-th)*6)
                size = int(8 * sa * (0.7 + 0.3*math.sin(p*10+i*2)))
                sc = lerp_color(DARK_BG, GOLD, sa)
                draw.ellipse([(sx-size, sy-size), (sx+size, sy+size)], fill=sc)

    # CTA
    if p > 0.6:
        a = min(1, (p-0.6)*4)
        f_cta = ImageFont.truetype(AR_BLACK, 52)
        c = lerp_color(DARK_BG, WHITE, a)
        center_text(draw, "أسئلة أكثر على", 1200, f_cta, c)
        cb = lerp_color(DARK_BG, PRIMARY, a)
        f_site = ImageFont.truetype(EN_BOLD, 60)
        center_text(draw, "oilexam.tech", 1300, f_site, cb)

    if p > 0.75:
        a = min(1, (p-0.75)*4)
        f_link = ImageFont.truetype(AR_BOLD, 42)
        c = lerp_color(DARK_BG, ORANGE, a)
        center_text(draw, "الرابط بالبايو", 1500, f_link, c)
        cs = lerp_color(DARK_BG, (80,95,120), a)
        center_text(draw, "Powered by Trimind Company", 1700, f_brand, cs)

    return img


# ════════════════════════════════════════════════════════════════
#  STORY 7: "Score Reveal / Testimonial" - شوف نتيجتك
#  Concept: Simulated test result reveal with score climbing,
#  categories breakdown, and celebration
# ════════════════════════════════════════════════════════════════

def s7_hook(p):
    """Hook: Score reveal teaser"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    e = ease_out(p * 3)

    f_ar = ImageFont.truetype(AR_BLACK, 85)
    f_sub = ImageFont.truetype(AR_BOLD, 55)
    f_brand = ImageFont.truetype(EN_BOLD, 40)

    # Animated reveal bar going up
    bar_w = 120
    bar_max_h = int(800 * e)
    bx = (WIDTH - bar_w) // 2
    by = HEIGHT // 2 + 100

    # Bar glow
    if bar_max_h > 10:
        for dx in range(-20, 21):
            intensity = max(0, 1 - abs(dx) / 20)
            gc = lerp_color((0,0,0), PRIMARY, intensity * 0.3 * e)
            draw.line([(bx + bar_w//2 + dx, by), (bx + bar_w//2 + dx, by - bar_max_h)],
                      fill=gc)

        # Gradient bar
        for y in range(bar_max_h):
            ratio = y / max(bar_max_h, 1)
            c = lerp_color(GREEN, PRIMARY, ratio)
            draw.line([(bx, by - y), (bx + bar_w, by - y)], fill=c)

        # Score text on top of bar
        f_score = ImageFont.truetype(EN_BOLD, 60)
        score = int(92 * min(1, e * 1.3))
        center_text(draw, f"{score}%", by - bar_max_h - 70, f_score, GREEN)

    if e > 0.3:
        center_text(draw, "شوف كم تحصّل", by + 100, f_ar, WHITE)

    if p > 0.45:
        a = min(1, (p-0.45)*4)
        c = lerp_color((0,0,0), PRIMARY, a)
        center_text(draw, "بعد ما تدرس معانا", by + 220, f_sub, c)

    if p > 0.7:
        a = min(1, (p-0.7)*4)
        c = lerp_color((0,0,0), (80,100,140), a)
        center_text(draw, "oilexam.tech", 1720, f_brand, c)

    return img


def s7_score_climb(p):
    """Animated score climbing from 0 to 92%"""
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    f_label = ImageFont.truetype(AR_BLACK, 52)
    f_score = ImageFont.truetype(EN_BOLD, 240)
    f_pct = ImageFont.truetype(EN_BOLD, 100)
    f_sub = ImageFont.truetype(AR_BOLD, 46)

    # Score animation
    if p < 0.7:
        score = int(92 * ease_out(p / 0.7 * 1.2))
    else:
        score = 92

    # Dynamic color based on score
    if score < 40:
        score_color = RED
    elif score < 70:
        score_color = ORANGE
    else:
        score_color = GREEN

    # Glow behind score
    glow_intensity = min(1, p * 2)
    glow_r = int(320 * glow_intensity)
    if glow_r > 5:
        radial_gradient(img, WIDTH//2, HEIGHT//2-250, glow_r,
                        lerp_color(DARK_BG, score_color, 0.3), DARK_BG)
        draw = ImageDraw.Draw(img)

    # "Your Score" label
    center_text(draw, "نتيجتك", 250, f_label, WHITE)

    # Big score number
    score_str = str(score)
    nb = draw.textbbox((0,0), score_str, font=f_score)
    nw = nb[2] - nb[0]
    nx = (WIDTH - nw) // 2 - 40
    # Shadow
    draw.text((nx+5, 405), score_str, font=f_score, fill=(0,0,0))
    draw.text((nx, 400), score_str, font=f_score, fill=score_color)

    # Percent sign
    draw.text((nx + nw + 10, 450), "%", font=f_pct, fill=score_color)

    # Circular progress ring
    cx, cy = WIDTH // 2, 1100
    ring_r = 180
    ring_w = 18

    # Background ring
    for angle_deg in range(360):
        angle = math.radians(angle_deg - 90)
        x1 = cx + int(math.cos(angle) * (ring_r - ring_w))
        y1 = cy + int(math.sin(angle) * (ring_r - ring_w))
        x2 = cx + int(math.cos(angle) * ring_r)
        y2 = cy + int(math.sin(angle) * ring_r)
        draw.line([(x1, y1), (x2, y2)], fill=(35, 48, 68), width=2)

    # Filled ring
    fill_deg = int(360 * (score / 100))
    for angle_deg in range(fill_deg):
        angle = math.radians(angle_deg - 90)
        ratio = angle_deg / 360
        c = lerp_color(PRIMARY, GREEN, ratio)
        x1 = cx + int(math.cos(angle) * (ring_r - ring_w))
        y1 = cy + int(math.sin(angle) * (ring_r - ring_w))
        x2 = cx + int(math.cos(angle) * ring_r)
        y2 = cy + int(math.sin(angle) * ring_r)
        draw.line([(x1, y1), (x2, y2)], fill=c, width=2)

    # Text in ring
    f_ring = ImageFont.truetype(AR_BOLD, 40)
    center_text(draw, "ممتاز", cy - 25, f_ring, score_color)

    # Subtitle
    if p > 0.75:
        a = min(1, (p-0.75)*5)
        c = lerp_color(DARK_BG, PALE_BLUE, a)
        center_text(draw, "!مستعد لاختبار النفط", 1380, f_sub, c)

    return img


def s7_breakdown(p):
    """Score breakdown by category"""
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(AR_BLACK, 58)
    f_cat = ImageFont.truetype(AR_BOLD, 44)
    f_score = ImageFont.truetype(EN_BOLD, 48)
    f_bar_label = ImageFont.truetype(EN_REG, 32)

    center_text(draw, "تفاصيل النتيجة", 180, f_title, WHITE)
    draw.line([(WIDTH//2-200, 260), (WIDTH//2+200, 260)], fill=PRIMARY, width=2)

    categories = [
        ("المفردات", "Vocabulary", 88, PRIMARY),
        ("الأفعال المركّبة", "Phrasal Verbs", 91, MID_BLUE),
        ("القواعد", "Grammar", 95, ORANGE),
        ("القراءة", "Reading", 85, GREEN),
        ("الاختبار التجريبي", "Mock Exam", 96, PINK),
    ]

    for i, (ar_name, en_name, target_score, color) in enumerate(categories):
        th = i * 0.12 + 0.05
        if p > th:
            a = min(1, (p-th)*4)
            ep = ease_out((p-th)*3)
            y = 340 + i * 260

            cur_score = int(target_score * min(1, ep * 1.3))
            xo = int((1-ep) * 250)

            # Card
            card_c = lerp_color(DARK_BG, (35, 48, 68), a)
            draw.rounded_rectangle([(70+xo, y), (WIDTH-70, y+220)],
                                   radius=20, fill=card_c)

            # Color accent
            draw.rounded_rectangle([(WIDTH-85, y+15), (WIDTH-70, y+205)],
                                   radius=6, fill=lerp_color(DARK_BG, color, a))

            # Category name
            tc = lerp_color(DARK_BG, WHITE, a)
            bb = draw.textbbox((0,0), ar_name, font=f_cat)
            tw = bb[2] - bb[0]
            draw.text((WIDTH-110-tw+xo, y+20), ar_name, font=f_cat, fill=tc)

            # English name
            ec = lerp_color(DARK_BG, PALE_BLUE, a)
            eb = draw.textbbox((0,0), en_name, font=f_bar_label)
            ew = eb[2] - eb[0]
            draw.text((WIDTH-110-ew+xo, y+80), en_name, font=f_bar_label, fill=ec)

            # Score
            sc = lerp_color(DARK_BG, color, a)
            draw.text((100+xo, y+25), f"{cur_score}%", font=f_score, fill=sc)

            # Progress bar
            bar_y = y + 140
            bar_x = 100 + xo
            bar_w = WIDTH - 200
            draw.rounded_rectangle([(bar_x, bar_y), (bar_x+bar_w, bar_y+24)],
                                   radius=12, fill=(30, 40, 58))
            fill_w = int(bar_w * cur_score / 100)
            if fill_w > 12:
                draw.rounded_rectangle([(bar_x, bar_y), (bar_x+fill_w, bar_y+24)],
                                       radius=12, fill=lerp_color(DARK_BG, color, a))

    return img


def s7_cta(p):
    """CTA for score reveal"""
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    f_huge = ImageFont.truetype(AR_BLACK, 78)
    f_brand = ImageFont.truetype(EN_BOLD, 70)
    f_btn = ImageFont.truetype(AR_BLACK, 48)
    f_ar = ImageFont.truetype(AR_BOLD, 42)
    f_small = ImageFont.truetype(EN_REG, 32)

    e = ease_out(p * 3)
    pulse = 0.88 + 0.12 * math.sin(p * 10)

    radial_gradient(img, WIDTH//2, 450, int(300*e), (40, 60, 95), DARK_BG)
    draw = ImageDraw.Draw(img)

    center_text(draw, "حقّق نفس النتيجة", int(280+(1-e)*70), f_huge, WHITE)

    if p > 0.12:
        center_text(draw, "!ابدأ تدريبك اليوم", 410, f_huge, GREEN)

    if p > 0.25:
        center_text(draw, "oilexam.tech", 580, f_brand, PRIMARY)

    if p > 0.35:
        bw, bh = 700, 120
        bx, by = (WIDTH-bw)//2, 730
        bc = tuple(int(c*pulse) for c in GREEN)
        draw.rounded_rectangle([(bx-4,by-4),(bx+bw+4,by+bh+4)],
                               radius=60, fill=bc)
        draw.rounded_rectangle([(bx,by),(bx+bw,by+bh)],
                               radius=58, fill=GREEN)
        center_text(draw, "جرّب الحين مجاني", by+28, f_btn, WHITE)

    if p > 0.5:
        stats = [
            ("92%", "معدل النجاح", GREEN),
            ("525+", "سؤال وتمرين", PRIMARY),
            ("7", "أيام للجاهزية", ORANGE),
        ]
        for i, (num, label, color) in enumerate(stats):
            th = 0.5 + i*0.08
            if p > th:
                a = min(1, (p-th)*5)
                y = 960 + i * 140

                # Stat card
                cc = lerp_color(DARK_BG, (35, 48, 68), a)
                draw.rounded_rectangle([(120, y), (WIDTH-120, y+110)],
                                       radius=16, fill=cc)

                nc = lerp_color(DARK_BG, color, a)
                f_num = ImageFont.truetype(EN_BOLD, 52)
                draw.text((160, y+22), num, font=f_num, fill=nc)

                tc = lerp_color(DARK_BG, WHITE, a)
                bb = draw.textbbox((0,0), label, font=f_ar)
                tw = bb[2]-bb[0]
                draw.text((WIDTH-160-tw, y+28), label, font=f_ar, fill=tc)

    if p > 0.75:
        a = min(1, (p-0.75)*4)
        c = lerp_color(DARK_BG, ORANGE, a)
        center_text(draw, "الرابط بالبايو", 1480, f_ar, c)
        cs = lerp_color(DARK_BG, (80,95,120), a)
        center_text(draw, "Powered by Trimind Company", 1700, f_small, cs)

    return img


# ════════════════════════════════════════════════════════════════
#  STORY 8: "Daily Word Flashcard" - كلمة اليوم
#  Concept: Beautiful flashcard animation - word appears in English,
#  flips to show Arabic meaning, usage in sentence, then CTA
# ════════════════════════════════════════════════════════════════

def s8_hook(p):
    """Hook: Daily word intro"""
    img = gradient_bg(WIDTH, HEIGHT, (15, 20, 40), (25, 35, 55))
    draw = ImageDraw.Draw(img)
    e = ease_out(p * 3)

    f_ar = ImageFont.truetype(AR_BLACK, 80)
    f_sub = ImageFont.truetype(AR_BOLD, 50)
    f_day = ImageFont.truetype(EN_BOLD, 42)
    f_hash = ImageFont.truetype(EN_BOLD, 36)

    # Animated book/card icon (simple geometric)
    cx, cy = WIDTH//2, HEIGHT//2 - 300
    card_w = int(280 * e)
    card_h = int(180 * e)
    if card_w > 20:
        # Shadow
        draw.rounded_rectangle(
            [(cx-card_w//2+8, cy-card_h//2+8), (cx+card_w//2+8, cy+card_h//2+8)],
            radius=16, fill=(10, 15, 30))
        # Card
        draw.rounded_rectangle(
            [(cx-card_w//2, cy-card_h//2), (cx+card_w//2, cy+card_h//2)],
            radius=16, fill=TEAL)
        # Lines on card
        if card_w > 100:
            for i in range(3):
                ly = cy - 40 + i * 35
                lx1 = cx - card_w//2 + 30
                lx2 = cx + card_w//2 - 30 - i*20
                draw.line([(lx1, ly), (lx2, ly)], fill=WHITE, width=3)

    if e > 0.3:
        center_text(draw, "كلمة اليوم", HEIGHT//2-60, f_ar, WHITE)

    if p > 0.35:
        a = min(1, (p-0.35)*4)
        c = lerp_color((15,20,40), TEAL, a)
        center_text(draw, "تعلّم كلمة جديدة كل يوم", HEIGHT//2+60, f_sub, c)

    if p > 0.55:
        a = min(1, (p-0.55)*4)
        c = lerp_color((15,20,40), PALE_BLUE, a)
        center_text(draw, "#OilExam_Word", HEIGHT//2+180, f_hash, c)

    if p > 0.7:
        a = min(1, (p-0.7)*4)
        c = lerp_color((15,20,40), (80,100,140), a)
        f_brand = ImageFont.truetype(EN_BOLD, 36)
        center_text(draw, "oilexam.tech", 1720, f_brand, c)

    return img


def s8_word_english(p):
    """Show the English word with pronunciation"""
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    f_word = ImageFont.truetype(EN_BOLD, 100)
    f_type = ImageFont.truetype(EN_REG, 36)
    f_phonetic = ImageFont.truetype(EN_REG, 42)
    f_label = ImageFont.truetype(AR_BOLD, 40)

    e = ease_out(p * 2.5)

    # Floating card
    card_y = 350
    card_h = 550
    if e > 0.1:
        # Card shadow
        draw.rounded_rectangle(
            [(75, card_y+8), (WIDTH-65, card_y+card_h+8)],
            radius=28, fill=(15, 22, 38))
        # Main card
        draw.rounded_rectangle(
            [(70, card_y), (WIDTH-70, card_y+card_h)],
            radius=28, fill=(32, 44, 65))
        # Top gradient accent
        for y_off in range(8):
            ratio = y_off / 8
            c = lerp_color(TEAL, (32,44,65), ratio)
            draw.line([(70, card_y+y_off), (WIDTH-70, card_y+y_off)], fill=c)

    # "ENGLISH" label
    if e > 0.2:
        badge_w, badge_h = 220, 50
        bx = (WIDTH - badge_w) // 2
        draw.rounded_rectangle([(bx, card_y+30), (bx+badge_w, card_y+30+badge_h)],
                               radius=25, fill=TEAL)
        center_text(draw, "ENGLISH", card_y+35, f_type, WHITE)

    # The word
    if e > 0.3:
        center_text(draw, "Refinery", card_y+140, f_word, WHITE)

    if e > 0.45:
        center_text(draw, "/rɪˈfaɪnəri/", card_y+280, f_phonetic, PALE_BLUE)

    if e > 0.55:
        center_text(draw, "( noun )", card_y+350, f_type, TEAL)

    # Usage sentence
    if p > 0.5:
        a = min(1, (p-0.5)*4)
        f_sentence = ImageFont.truetype(EN_REG, 36)
        f_sent_label = ImageFont.truetype(AR_BOLD, 36)

        sent_y = card_y + card_h + 60
        c_label = lerp_color(DARK_BG, TEAL, a)
        center_text(draw, ":مثال", sent_y, f_sent_label, c_label)

        c_sent = lerp_color(DARK_BG, WHITE, a)
        center_text(draw, "\"The refinery processes", sent_y+60, f_sentence, c_sent)
        center_text(draw, "crude oil into fuel.\"", sent_y+110, f_sentence, c_sent)

    # Swipe hint
    if p > 0.75:
        a = min(1, (p-0.75)*4)
        f_hint = ImageFont.truetype(AR_REG, 38)
        c = lerp_color(DARK_BG, ORANGE, a)
        # Arrow animation
        arrow_y = 1500 + int(10 * math.sin(p * 8))
        center_text(draw, "شوف الترجمة العربية", arrow_y, f_hint, c)

    return img


def s8_word_arabic(p):
    """Flip to Arabic meaning"""
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    f_word_en = ImageFont.truetype(EN_BOLD, 60)
    f_word_ar = ImageFont.truetype(AR_BLACK, 100)
    f_meaning = ImageFont.truetype(AR_BOLD, 46)
    f_type = ImageFont.truetype(EN_REG, 36)
    f_example = ImageFont.truetype(AR_REG, 38)

    e = ease_out(p * 2.5)

    # Card with flip effect (scale horizontally)
    card_y = 280
    card_h = 700

    if e > 0.1:
        # Shadow
        draw.rounded_rectangle(
            [(75, card_y+8), (WIDTH-65, card_y+card_h+8)],
            radius=28, fill=(15, 22, 38))
        # Main card - greenish tint for Arabic side
        draw.rounded_rectangle(
            [(70, card_y), (WIDTH-70, card_y+card_h)],
            radius=28, fill=(25, 45, 42))
        # Top accent
        for y_off in range(8):
            ratio = y_off / 8
            c = lerp_color(GREEN, (25,45,42), ratio)
            draw.line([(70, card_y+y_off), (WIDTH-70, card_y+y_off)], fill=c)

    # "ARABIC" label
    if e > 0.2:
        badge_w, badge_h = 220, 50
        bx = (WIDTH - badge_w) // 2
        draw.rounded_rectangle([(bx, card_y+30), (bx+badge_w, card_y+30+badge_h)],
                               radius=25, fill=GREEN)
        f_badge = ImageFont.truetype(AR_BOLD, 34)
        center_text(draw, "عربي", card_y+35, f_badge, WHITE)

    # English word (smaller)
    if e > 0.25:
        center_text(draw, "Refinery", card_y+110, f_word_en, PALE_BLUE)

    # Arabic translation (big)
    if e > 0.4:
        center_text(draw, "مصفاة", card_y+250, f_word_ar, WHITE)

    # Detailed meaning
    if e > 0.55:
        center_text(draw, "مكان تكرير النفط الخام", card_y+410, f_meaning, GREEN)

    if e > 0.65:
        center_text(draw, "وتحويله إلى منتجات بترولية", card_y+480, f_meaning, PALE_BLUE)

    # Example in Arabic
    if p > 0.5:
        a = min(1, (p-0.5)*4)
        sent_y = card_y + card_h + 50
        f_ex_label = ImageFont.truetype(AR_BOLD, 36)
        c = lerp_color(DARK_BG, TEAL, a)
        center_text(draw, ":مثال", sent_y, f_ex_label, c)
        ec = lerp_color(DARK_BG, WHITE, a)
        center_text(draw, "\"المصفاة تحوّل النفط الخام", sent_y+55, f_example, ec)
        center_text(draw, "إلى وقود للاستخدام\"", sent_y+105, f_example, ec)

    # Word count badge
    if p > 0.7:
        a = min(1, (p-0.7)*4)
        f_count = ImageFont.truetype(AR_BOLD, 36)
        c = lerp_color(DARK_BG, ORANGE, a)
        center_text(draw, "١ من ١٥٧ كلمة على OilExam", 1500, f_count, c)

    return img


def s8_cta(p):
    """CTA for daily word"""
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    f_huge = ImageFont.truetype(AR_BLACK, 75)
    f_brand = ImageFont.truetype(EN_BOLD, 68)
    f_btn = ImageFont.truetype(AR_BLACK, 46)
    f_ar = ImageFont.truetype(AR_BOLD, 42)
    f_small = ImageFont.truetype(EN_REG, 32)
    f_stat = ImageFont.truetype(EN_BOLD, 56)

    e = ease_out(p * 3)
    pulse = 0.88 + 0.12 * math.sin(p * 10)

    radial_gradient(img, WIDTH//2, 420, int(280*e), (30, 50, 80), DARK_BG)
    draw = ImageDraw.Draw(img)

    center_text(draw, "تبي تتعلّم أكثر؟", int(260+(1-e)*70), f_huge, WHITE)

    if p > 0.1:
        center_text(draw, "كل الكلمات موجودة", 400, f_huge, TEAL)

    if p > 0.2:
        center_text(draw, "oilexam.tech", 560, f_brand, PRIMARY)

    if p > 0.3:
        bw, bh = 680, 120
        bx, by = (WIDTH-bw)//2, 710
        bc = tuple(int(c*pulse) for c in TEAL)
        draw.rounded_rectangle([(bx-4,by-4),(bx+bw+4,by+bh+4)],
                               radius=60, fill=bc)
        draw.rounded_rectangle([(bx,by),(bx+bw,by+bh)],
                               radius=58, fill=TEAL)
        center_text(draw, "تعلّم الحين", by+28, f_btn, WHITE)

    # Word stats
    if p > 0.45:
        stats = [
            ("157", "كلمة مفردات", PRIMARY),
            ("159", "فعل مركّب", MID_BLUE),
            ("130", "سؤال قواعد", ORANGE),
        ]
        for i, (num, label, color) in enumerate(stats):
            th = 0.45 + i*0.08
            if p > th:
                a = min(1, (p-th)*5)
                y = 930 + i * 120

                nc = lerp_color(DARK_BG, color, a)
                draw.text((160, y), num, font=f_stat, fill=nc)

                tc = lerp_color(DARK_BG, WHITE, a)
                bb = draw.textbbox((0,0), label, font=f_ar)
                tw = bb[2]-bb[0]
                draw.text((WIDTH-180-tw, y+5), label, font=f_ar, fill=tc)

                # Separator line
                if i < len(stats)-1:
                    lc = lerp_color(DARK_BG, (40,55,75), a)
                    draw.line([(160, y+90), (WIDTH-160, y+90)], fill=lc, width=1)

    if p > 0.7:
        a = min(1, (p-0.7)*4)
        c = lerp_color(DARK_BG, ORANGE, a)
        center_text(draw, "الرابط بالبايو", 1450, f_ar, c)

    if p > 0.8:
        a = min(1, (p-0.8)*4)
        fc = lerp_color(DARK_BG, TEAL, a)
        center_text(draw, "#OilExam_Word", 1560, f_small, fc)
        cs = lerp_color(DARK_BG, (80,95,120), a)
        center_text(draw, "Powered by Trimind Company", 1700, f_small, cs)

    return img


# ════════════════════════════════════════════════════════════════
#  BUILD
# ════════════════════════════════════════════════════════════════

def main():
    print("+" + "="*54 + "+")
    print("|  OilExam.tech - 3 New Instagram Stories              |")
    print("|  Story 6: Quiz  |  Story 7: Score  |  Story 8: Word  |")
    print("+" + "="*54 + "+")
    print(f"Resolution: {WIDTH}x{HEIGHT} | FPS: {FPS}")

    out_dir = "/root/OilexamVideo"

    # Story 6: Quiz Challenge
    build_video("story6_quiz", [
        ("Hook - تحدّي",         s6_hook,       3.5),
        ("Question + Options",   s6_question,   6.0),
        ("Answer Reveal",        s6_reveal,     5.5),
    ], f"{out_dir}/story_6_quiz_challenge.mp4")

    # Story 7: Score Reveal
    build_video("story7_score", [
        ("Hook - النتيجة",       s7_hook,        3.5),
        ("Score Climbing",       s7_score_climb, 5.0),
        ("Category Breakdown",   s7_breakdown,   5.5),
        ("CTA",                  s7_cta,         5.0),
    ], f"{out_dir}/story_7_score_reveal.mp4")

    # Story 8: Daily Word Flashcard
    build_video("story8_word", [
        ("Hook - كلمة اليوم",    s8_hook,         3.5),
        ("English Side",         s8_word_english, 5.0),
        ("Arabic Side",          s8_word_arabic,  5.0),
        ("CTA",                  s8_cta,          4.5),
    ], f"{out_dir}/story_8_daily_word.mp4")

    print("\n+" + "="*54 + "+")
    print("|         ALL 3 NEW STORIES COMPLETE!                   |")
    print("+" + "="*54 + "+")


if __name__ == "__main__":
    main()
