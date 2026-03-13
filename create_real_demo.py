#!/usr/bin/env python3
"""
OilExam.tech - Real iPhone Demo Video
Uses actual screenshots from the live website.
Smooth scroll, realistic touch, natural timing.
"""

from PIL import Image, ImageDraw, ImageFont
from pro_utils import *
import subprocess, tempfile, shutil

# Target: 1080x1920 (Instagram Reel)
# Source screenshots: 1179 wide, need to scale to fit

LANDING_IMG = Image.open('/tmp/oilexam_real/landing_full.png')
PRICING_IMG = Image.open('/tmp/oilexam_real/pricing_full.png')

# Scale screenshots to 1080 wide
SCALE = 1080 / LANDING_IMG.width
LANDING_SCALED = LANDING_IMG.resize(
    (1080, int(LANDING_IMG.height * SCALE)), Image.LANCZOS)
PRICING_SCALED = PRICING_IMG.resize(
    (1080, int(PRICING_IMG.height * SCALE)), Image.LANCZOS)

print(f"Landing scaled: {LANDING_SCALED.size}")
print(f"Pricing scaled: {PRICING_SCALED.size}")

# Viewport height for the phone screen
VIEWPORT_H = 1920


def crop_viewport(full_img, scroll_y):
    """Crop a 1080x1920 viewport from the full page at scroll position."""
    max_scroll = max(0, full_img.height - VIEWPORT_H)
    scroll_y = max(0, min(scroll_y, max_scroll))
    return full_img.crop((0, scroll_y, 1080, scroll_y + VIEWPORT_H))


def smooth_scroll(start, end, p):
    """Natural iOS-like scroll with deceleration."""
    # iOS uses a deceleration curve
    t = ease_in_out(p)
    return int(start + (end - start) * t)


def draw_touch(img, x, y, size=50, opacity=0.3):
    """Draw a realistic finger touch indicator on the image."""
    draw = ImageDraw.Draw(img)
    # Outer glow
    for r in range(size, 0, -2):
        ratio = r / size
        alpha = opacity * (1 - ratio) * 0.5
        c = lerp_color((128, 128, 128), (200, 200, 200), ratio)
        c = tuple(int(c[i] * (1 - alpha) + 180 * alpha) for i in range(3))
        draw.ellipse([(x-r, y-r), (x+r, y+r)], fill=c)
    # Inner circle
    inner_r = 18
    draw.ellipse([(x-inner_r, y-inner_r), (x+inner_r, y+inner_r)],
                 fill=(180, 180, 180))
    return img


def add_swipe_indicator(img, x, y1, y2, p):
    """Draw a swipe motion trail."""
    draw = ImageDraw.Draw(img)
    trail_len = int(abs(y2 - y1) * p)
    cy = int(y1 + (y2 - y1) * p)
    # Fading trail
    for i in range(min(trail_len, 80)):
        alpha = max(0, 0.15 * (1 - i / 80))
        ty = cy + i  # trail going up
        if 0 <= ty < VIEWPORT_H:
            c = lerp_color((200, 200, 200), (255, 255, 255), alpha)
            r = int(15 * (1 - i / 80))
            if r > 1:
                draw.ellipse([(x-r, ty-r), (x+r, ty+r)], fill=c)
    # Current finger position
    draw_touch(img, x, cy, size=40, opacity=0.25)
    return img


# ════════════════════════════════════════════
#  QUIZ PAGE (recreated from user screenshots)
# ════════════════════════════════════════════

def create_quiz_categories_image():
    """Create quiz categories page matching the real app UI."""
    img = Image.new('RGB', (1080, 3200), (243, 244, 246))
    draw = ImageDraw.Draw(img)

    # Nav bar
    draw.rectangle([(0, 0), (1080, 180)], fill=(255, 255, 255))
    draw.line([(0, 180), (1080, 180)], fill=(229, 231, 235), width=2)
    f_logo = ImageFont.truetype(EN_BOLD, 56)
    draw.text((40, 55), "OilExam", font=f_logo, fill=(59, 130, 246))
    f_ar = ImageFont.truetype(EN_REG, 36)
    draw.rounded_rectangle([(820, 55), (920, 110)], radius=16, fill=(243, 244, 246))
    draw.text((850, 63), "AR", font=f_ar, fill=(0, 0, 0))
    # Hamburger
    for i in range(3):
        draw.rounded_rectangle([(960, 62+i*20), (1030, 68+i*20)], radius=2, fill=(60, 60, 67))

    y = 220

    categories = [
        ("Vocabulary", "157 questions", (59, 130, 246), "Test your knowledge of oil industry vocabulary with multiple-choice questions."),
        ("Reading Comprehension", "29 passages", (16, 185, 129), "Practice reading comprehension with oil industry-related passages and questions."),
        ("Phrasal Verbs", "159 verbs", (168, 85, 247), "Study common phrasal verbs used in the oil industry with flashcards."),
        ("Grammar", "130 questions", (245, 158, 11), "Practice grammar rules and usage with targeted questions."),
        ("Exam Questions", "50 questions", (239, 68, 68), "Take practice exams that simulate the real oil industry English test."),
    ]

    f_cat_title = ImageFont.truetype(EN_BOLD, 48)
    f_cat_count = ImageFont.truetype(EN_REG, 32)
    f_cat_desc = ImageFont.truetype(EN_REG, 28)
    f_btn = ImageFont.truetype(EN_BOLD, 34)

    for title, count, color, desc in categories:
        card_h = 380
        # Card
        draw.rounded_rectangle([(36, y), (1044, y+card_h)], radius=28, fill=(255, 255, 255))

        # Color indicator bar
        draw.rounded_rectangle([(36, y), (48, y+card_h)], radius=6, fill=color)

        # Icon circle
        draw.ellipse([(80, y+30), (150, y+100)], fill=lerp_color(color, (255,255,255), 0.75))
        f_icon = ImageFont.truetype(EN_BOLD, 40)
        icon_letter = title[0]
        ib = draw.textbbox((0,0), icon_letter, font=f_icon)
        draw.text((115-(ib[2]-ib[0])//2, y+45), icon_letter, font=f_icon, fill=color)

        # Title & count
        draw.text((175, y+35), title, font=f_cat_title, fill=(0, 0, 0))
        draw.text((175, y+95), count, font=f_cat_count, fill=(99, 99, 102))

        # Description
        draw.text((80, y+160), desc[:50], font=f_cat_desc, fill=(99, 99, 102))
        if len(desc) > 50:
            draw.text((80, y+200), desc[50:], font=f_cat_desc, fill=(99, 99, 102))

        # Start button
        btn_w = 200
        btn_x = (1080 - btn_w) // 2
        btn_y = y + card_h - 90
        draw.rounded_rectangle([(btn_x, btn_y), (btn_x+btn_w, btn_y+60)], radius=14, fill=color)
        bb = draw.textbbox((0,0), "Start", font=f_btn)
        draw.text((btn_x+(btn_w-(bb[2]-bb[0]))//2, btn_y+12), "Start", font=f_btn, fill=(255, 255, 255))

        y += card_h + 30

    return img


QUIZ_IMG = create_quiz_categories_image()


# ════════════════════════════════════════════
#  SCENES
# ════════════════════════════════════════════

def scene_open_site(p):
    """Site loads - fade in from white."""
    if p < 0.3:
        # White loading
        img = Image.new('RGB', (1080, 1920), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        # Loading bar
        bar_w = int(1080 * (p / 0.3))
        draw.rectangle([(0, 0), (bar_w, 6)], fill=(59, 130, 246))
        return img
    else:
        # Fade in real page
        alpha = min(1, (p - 0.3) * 2.5)
        real = crop_viewport(LANDING_SCALED, 0)
        white = Image.new('RGB', (1080, 1920), (255, 255, 255))
        return Image.blend(white, real, alpha)


def scene_browse_landing(p):
    """Smooth scroll through the real landing page."""
    max_scroll = LANDING_SCALED.height - VIEWPORT_H
    scroll = smooth_scroll(0, int(max_scroll * 0.35), p)
    img = crop_viewport(LANDING_SCALED, scroll)

    # Touch/swipe on scroll
    if 0.2 < p < 0.8:
        sp = (p - 0.2) / 0.6
        add_swipe_indicator(img, 540, 1400, 600, sp)

    return img


def scene_browse_features(p):
    """Continue scrolling to features section."""
    max_scroll = LANDING_SCALED.height - VIEWPORT_H
    start = int(max_scroll * 0.35)
    end = int(max_scroll * 0.7)
    scroll = smooth_scroll(start, end, p)
    img = crop_viewport(LANDING_SCALED, scroll)

    if 0.15 < p < 0.7:
        sp = (p - 0.15) / 0.55
        add_swipe_indicator(img, 540, 1300, 700, sp)

    return img


def scene_browse_cta(p):
    """Scroll to CTA and footer."""
    max_scroll = LANDING_SCALED.height - VIEWPORT_H
    start = int(max_scroll * 0.7)
    end = max_scroll
    scroll = smooth_scroll(start, end, p)
    img = crop_viewport(LANDING_SCALED, scroll)

    if 0.1 < p < 0.6:
        sp = (p - 0.1) / 0.5
        add_swipe_indicator(img, 540, 1200, 800, sp)

    return img


def scene_navigate_quiz(p):
    """Tap menu, navigate to quiz page."""
    if p < 0.2:
        # Still on landing bottom, finger goes to nav
        max_scroll = LANDING_SCALED.height - VIEWPORT_H
        img = crop_viewport(LANDING_SCALED, max_scroll)
        # Scroll back up to tap nav
        return img
    elif p < 0.35:
        # Quick scroll to top
        max_scroll = LANDING_SCALED.height - VIEWPORT_H
        scroll = smooth_scroll(max_scroll, 0, (p - 0.2) / 0.15)
        img = crop_viewport(LANDING_SCALED, scroll)
        return img
    elif p < 0.5:
        # Tap on hamburger menu area
        img = crop_viewport(LANDING_SCALED, 0)
        tap_p = (p - 0.35) / 0.15
        draw_touch(img, 1000, 80, size=int(45*ease_out(tap_p)), opacity=0.3)
        return img
    elif p < 0.6:
        # Transition - white flash
        alpha = min(1, (p - 0.5) / 0.1)
        img1 = crop_viewport(LANDING_SCALED, 0)
        img2 = Image.new('RGB', (1080, 1920), (243, 244, 246))
        return Image.blend(img1, img2, alpha)
    else:
        # Quiz page loading
        load_p = (p - 0.6) / 0.4
        if load_p < 0.3:
            img = Image.new('RGB', (1080, 1920), (243, 244, 246))
            draw = ImageDraw.Draw(img)
            bar_w = int(1080 * (load_p / 0.3))
            draw.rectangle([(0, 0), (bar_w, 6)], fill=(59, 130, 246))
            return img
        else:
            alpha = min(1, (load_p - 0.3) * 2.5)
            real = crop_viewport(QUIZ_IMG, 0)
            bg = Image.new('RGB', (1080, 1920), (243, 244, 246))
            return Image.blend(bg, real, alpha)


def scene_browse_quiz(p):
    """Scroll through quiz categories."""
    max_scroll = max(0, QUIZ_IMG.height - VIEWPORT_H)
    scroll = smooth_scroll(0, max_scroll, p)
    img = crop_viewport(QUIZ_IMG, scroll)

    if 0.15 < p < 0.7:
        sp = (p - 0.15) / 0.55
        add_swipe_indicator(img, 540, 1400, 600, sp)

    return img


def scene_tap_start(p):
    """Tap Start on Vocabulary quiz."""
    img = crop_viewport(QUIZ_IMG, 0)

    if p < 0.4:
        # Finger moves to Start button
        tp = p / 0.4
        fx = 540
        fy = int(1200 * (1 - ease_out(tp)) + 520 * ease_out(tp))
        draw_touch(img, fx, fy, size=int(40*ease_out(tp)))
    elif p < 0.6:
        # Button press
        draw_touch(img, 540, 520, size=50, opacity=0.4)
    else:
        # Transition to branded outro
        alpha = min(1, (p - 0.6) / 0.2)
        outro_img = branded_outro(0)
        return Image.blend(img, outro_img, alpha)

    return img


def scene_pricing(p):
    """Show pricing page."""
    if p < 0.15:
        # Transition in
        alpha = min(1, p / 0.15)
        real = crop_viewport(PRICING_SCALED, 0)
        bg = Image.new('RGB', (1080, 1920), (243, 244, 246))
        return Image.blend(bg, real, alpha)
    else:
        max_scroll = max(0, PRICING_SCALED.height - VIEWPORT_H)
        scroll = smooth_scroll(0, max_scroll, (p - 0.15) / 0.85)
        img = crop_viewport(PRICING_SCALED, scroll)

        if 0.25 < p < 0.75:
            sp = (p - 0.25) / 0.5
            add_swipe_indicator(img, 540, 1300, 700, sp)

        return img


def scene_outro(p):
    """Branded outro CTA."""
    return branded_outro(p)


# ════════════════════════════════════════════
#  BUILD
# ════════════════════════════════════════════

def main():
    print("+" + "="*54 + "+")
    print("|  OilExam - REAL Website iPhone Demo                  |")
    print("|  Using actual screenshots from oilexam.tech          |")
    print("+" + "="*54 + "+")

    out_dir = "/root/OilexamVideo"

    build_video("real_iphone_demo", [
        ("Site Opens",         scene_open_site,       2.0),
        ("Browse Landing",     scene_browse_landing,  3.5),
        ("Browse Features",    scene_browse_features, 3.0),
        ("Browse CTA",         scene_browse_cta,      2.5),
        ("Navigate to Quiz",   scene_navigate_quiz,   3.0),
        ("Browse Quiz",        scene_browse_quiz,     3.5),
        ("Tap Start",          scene_tap_start,       2.5),
        ("Pricing Page",       scene_pricing,         3.5),
        ("CTA Outro",          scene_outro,           4.0),
    ], f"{out_dir}/pro_reel_real_demo.mp4")

    print("\n  REAL DEMO REEL COMPLETE!")


if __name__ == "__main__":
    main()
