import html
import os
import random
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO

COMMUNITY_NAME = "Communitive Dentistry Üsküdar"
WEBSITE_URL = "https://worp.me/communitiveuudhf"
WEBSITE_LABEL = "worp.me/communitiveuudhf"
INSTAGRAM_URL = "https://www.instagram.com/communitive.uudhf/"
INSTAGRAM_HANDLE = "@communitive.uudhf"
LOGO_URL = "https://i.imgur.com/EydFZfb.jpeg"
LOCAL_FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Helvetica.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:\\Windows\\Fonts\\arial.ttf",
]
BINGO_ITEMS = [
    "Etkinlikte Story Attım",
    "Elimi/Önlüğümü Yaktım",
    "Sabun Değil Diş Yontuyorum",
    "Vizeden Önce Uyumadım",
    "Anakalbi Anaokuluna Gittim",
    "Hasta Gelmeyince Sevindim",
    "Sülaleye Diş Sözü Verdim",
    "Not Dilendim",
    "Grubu Sabitledim",
]

# --- SAYFA AYARLARI ---
st.set_page_config(page_title=f"{COMMUNITY_NAME} Bingo", page_icon="🦷", layout="centered")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&display=swap');

    :root {
        --ink-strong: #f2f7ff;
        --ink: #d6e6ff;
        --ink-muted: #b7c9e6;
        --accent: #7fc9ff;
        --button-bg: #1b5fc2;
        --button-hover: #2a7be0;
        --button-border: rgba(255, 255, 255, 0.6);
    }

    .stApp {
        background-color: #071432;
        background-image:
            radial-gradient(circle at 20% 15%, rgba(255,255,255,0.25) 0 1px, transparent 2px),
            radial-gradient(circle at 80% 25%, rgba(255,255,255,0.18) 0 1px, transparent 2px),
            radial-gradient(circle at 35% 70%, rgba(255,255,255,0.18) 0 1px, transparent 2px),
            linear-gradient(180deg, #0c3a87 0%, #0a2b64 40%, #071432 100%);
        background-size: 140px 140px, 180px 180px, 220px 220px, cover;
        background-attachment: fixed;
        font-family: 'Sora', sans-serif;
    }

    .block-container {
        max-width: 900px;
        background: rgba(8, 16, 40, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 22px;
        padding: 2.2rem 2rem 2rem;
        box-shadow: 0 20px 50px rgba(4, 10, 24, 0.45);
        backdrop-filter: blur(6px);
    }

    h1, h2, h3 {
        color: var(--ink-strong) !important;
        letter-spacing: 0.4px;
    }

    p, label, .stMarkdown, .stMarkdown p, .stMarkdown span {
        color: var(--ink) !important;
    }

    .stCaption {
        color: var(--ink-muted) !important;
    }

    .stMarkdown a {
        color: var(--accent) !important;
    }

    .stButton>button,
    .stDownloadButton>button {
        background-color: var(--button-bg);
        color: #ffffff;
        border-radius: 16px;
        border: 1px solid var(--button-border);
        font-weight: 600;
    }

    .stButton>button:hover,
    .stDownloadButton>button:hover {
        background-color: var(--button-hover);
        border-color: #ffffff;
        color: #ffffff;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1.6rem 1.2rem 1.8rem;
            border-radius: 18px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- YARDIMCI FONKSİYONLAR ---

@st.cache_data
def load_image_from_url(url):
    response = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

@st.cache_data
def load_font(url, size):
    response = requests.get(url, timeout=8)
    response.raise_for_status()
    return ImageFont.truetype(BytesIO(response.content), size)

def load_font_with_fallback(url, size, local_paths):
    try:
        return load_font(url, size)
    except Exception:
        for path in local_paths:
            if path and os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue
    return ImageFont.load_default()

def create_gradient_background(size, top_color, bottom_color):
    try:
        gradient = Image.linear_gradient("L").resize(size)
        return ImageOps.colorize(gradient, top_color, bottom_color).convert("RGBA")
    except Exception:
        width, height = size
        top_r, top_g, top_b = ImageColor.getrgb(top_color)
        bot_r, bot_g, bot_b = ImageColor.getrgb(bottom_color)
        base = Image.new("RGBA", size, top_color)
        draw = ImageDraw.Draw(base)
        for y in range(height):
            ratio = y / max(height - 1, 1)
            r = int(top_r + (bot_r - top_r) * ratio)
            g = int(top_g + (bot_g - top_g) * ratio)
            b = int(top_b + (bot_b - top_b) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        return base

def add_snow(draw, width, height, count=260, seed=42):
    rng = random.Random(seed)
    for _ in range(count):
        x = rng.randint(0, width)
        y = rng.randint(0, height)
        r = rng.choice([1, 1, 2, 2, 3])
        alpha = rng.choice([80, 120, 160, 200])
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, alpha))
    for _ in range(18):
        x = rng.randint(0, width)
        y = rng.randint(0, height)
        r = rng.randint(4, 8)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(180, 220, 255, 90))

def draw_tick_mark(draw, box_bounds, color, width):
    x0, y0, x1, y1 = box_bounds
    size = x1 - x0
    start = (x0 + size * 0.28, y0 + size * 0.62)
    mid = (x0 + size * 0.44, y0 + size * 0.76)
    end = (x0 + size * 0.78, y0 + size * 0.38)
    draw.line([start, mid, end], fill=color, width=width, joint="curve")

def make_circle(img):
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)
    result = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    result.putalpha(mask)
    return result

def wrap_text(text, font, max_width):
    def text_width(value):
        if hasattr(font, "getlength"):
            return font.getlength(value)
        if hasattr(font, "getbbox"):
            box = font.getbbox(value)
            return box[2] - box[0]
        return font.getsize(value)[0]

    lines = []
    if text_width(text) <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0
        while i < len(words):
            line = ''
            while i < len(words) and text_width(line + words[i]) <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines

def build_card_html(items, selected_items, user_name):
    safe_items = [html.escape(item) for item in items]
    cells = []
    for item, selected in zip(safe_items, selected_items):
        class_name = "cell selected" if selected else "cell"
        cells.append(f'<div class="{class_name}"><span>{item}</span></div>')

    if user_name:
        footer_text = f"@{user_name} x {INSTAGRAM_HANDLE}"
    else:
        footer_text = INSTAGRAM_HANDLE
    footer_text = html.escape(footer_text)

    return f"""
    <div class="card-wrap">
      <div class="card">
        <div class="logo-ring">
          <img src="{LOGO_URL}" alt="Logo" />
        </div>
        <div class="title">COMMUNITIVE DENTISTRY</div>
        <div class="subtitle">ÜSKÜDAR</div>
        <div class="year">2025</div>
        <div class="bingo">BINGO</div>
        <div class="grid">
          {''.join(cells)}
        </div>
        <div class="footer">
          <img src="{LOGO_URL}" alt="Logo" />
          <span>{footer_text}</span>
        </div>
      </div>
    </div>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&display=swap');

      html, body {{
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
      }}
      .card-wrap {{
        display: flex;
        justify-content: center;
        width: 100%;
        padding: 0;
      }}
      .card {{
        width: min(520px, 96vw);
        aspect-ratio: 9 / 16;
        background-image:
          radial-gradient(circle at 20% 15%, rgba(255,255,255,0.18) 0 2px, transparent 3px),
          radial-gradient(circle at 80% 25%, rgba(255,255,255,0.12) 0 2px, transparent 3px),
          radial-gradient(circle at 35% 70%, rgba(255,255,255,0.12) 0 2px, transparent 3px),
          linear-gradient(180deg, #0c3a87 0%, #071432 100%);
        border-radius: 26px;
        padding: 22px 20px 20px;
        box-sizing: border-box;
        color: #f7fbff;
        font-family: 'Sora', sans-serif;
        position: relative;
        overflow: hidden;
        box-shadow: 0 26px 60px rgba(4, 12, 28, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.15);
      }}
      .card::before {{
        content: "";
        position: absolute;
        inset: -10% -10% 40% -10%;
        background: radial-gradient(circle, rgba(140, 210, 255, 0.35), transparent 60%);
        opacity: 0.8;
        z-index: 0;
      }}
      .card::after {{
        content: "";
        position: absolute;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140' viewBox='0 0 140 140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)' opacity='.25'/%3E%3C/svg%3E");
        opacity: 0.12;
        mix-blend-mode: soft-light;
        pointer-events: none;
        z-index: 0;
      }}
      .card > * {{
        position: relative;
        z-index: 1;
      }}
      .logo-ring {{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 4px solid #cfe6ff;
        background: #0d2a60;
        margin: 0 auto 16px;
        overflow: hidden;
      }}
      .logo-ring img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
      }}
      .title {{
        text-align: center;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.5px;
      }}
      .subtitle {{
        text-align: center;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 4px;
        letter-spacing: 0.5px;
      }}
      .year {{
        text-align: center;
        font-size: 2.6rem;
        font-weight: 700;
        margin-top: 8px;
        text-shadow: 0 0 16px rgba(200, 240, 255, 0.7), 0 0 28px rgba(120, 200, 255, 0.45);
      }}
      .bingo {{
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        margin-top: 2px;
        letter-spacing: 1px;
      }}
      .grid {{
        margin-top: 20px;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
      }}
      .cell {{
        position: relative;
        background: linear-gradient(145deg, rgba(150, 205, 235, 0.8), rgba(90, 140, 190, 0.85));
        border: 1.5px solid rgba(255, 255, 255, 0.65);
        border-radius: 18px;
        padding: 10px;
        min-height: 88px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-size: 0.85rem;
        font-weight: 600;
        line-height: 1.2;
        box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.1), 0 8px 16px rgba(6, 14, 32, 0.35);
        backdrop-filter: blur(6px);
      }}
      .cell::before {{
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.18), rgba(255, 255, 255, 0));
        opacity: 0.9;
        pointer-events: none;
      }}
      .cell span {{
        position: relative;
        z-index: 1;
      }}
      .cell.selected {{
        border-color: rgba(255, 255, 255, 0.9);
        box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.2), 0 10px 18px rgba(10, 20, 40, 0.4);
      }}
      .cell.selected::after {{
        content: "SEÇTİM";
        position: absolute;
        right: 10px;
        bottom: 10px;
        font-size: 0.55rem;
        letter-spacing: 1px;
        padding: 4px 6px;
        border: 2px dashed #ff8ec0;
        border-radius: 999px;
        color: #ff8ec0;
        background: rgba(12, 22, 40, 0.5);
        text-transform: uppercase;
        transform: rotate(-12deg);
      }}
      .footer {{
        margin-top: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        font-size: 0.9rem;
        opacity: 0.9;
      }}
      .footer img {{
        width: 22px;
        height: 22px;
        border-radius: 50%;
        border: 1px solid rgba(255, 255, 255, 0.7);
      }}
    </style>
    """

# --- GÖRSEL OLUŞTURMA MOTORU ---
def create_bingo_card(selected_items, user_name):
    # 1. Canvas Oluştur (1080x1920 - Instagram Story)
    W, H = 1080, 1920
    img = create_gradient_background((W, H), "#0c3a87", "#071432")
    draw = ImageDraw.Draw(img)

    # 2. Kış temalı yıldız/snow efekti
    add_snow(draw, W, H, count=200, seed=24)

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((W // 2 - 240, 70, W // 2 + 240, 560), fill=(120, 200, 255, 60))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # 3. Fontları Yükle (Google Fonts'tan direkt çekiyoruz)
    # Başlık fontu: Mountains of Christmas
    title_font_url = "https://github.com/google/fonts/raw/main/apache/mountainsofchristmas/MountainsofChristmas-Bold.ttf"
    # Yazı fontu: Poppins veya Roboto
    body_font_url = "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-SemiBold.ttf"
    
    font_header = load_font_with_fallback(body_font_url, 60, LOCAL_FONT_PATHS)
    font_sub = load_font_with_fallback(body_font_url, 52, LOCAL_FONT_PATHS)
    font_tagline = load_font_with_fallback(body_font_url, 120, LOCAL_FONT_PATHS)
    font_bingo_title = load_font_with_fallback(title_font_url, 110, LOCAL_FONT_PATHS)
    font_bingo = load_font_with_fallback(body_font_url, 40, LOCAL_FONT_PATHS)
    font_footer = load_font_with_fallback(body_font_url, 34, LOCAL_FONT_PATHS)

    # 4. Logo Yerleşimi (Kar Küresi Efekti)
    logo_url = LOGO_URL
    logo_size = 260
    ring_size = 300
    logo_x = (W - ring_size) // 2
    logo_y = 140

    logo_bg = Image.new("RGBA", (ring_size, ring_size), (0, 0, 0, 0))
    draw_logo_bg = ImageDraw.Draw(logo_bg)
    draw_logo_bg.ellipse(
        (0, 0, ring_size - 1, ring_size - 1),
        fill=(18, 45, 95, 210),
        outline=(210, 235, 255, 255),
        width=6,
    )
    draw_logo_bg.ellipse(
        (6, 6, ring_size - 7, ring_size - 7),
        outline=(120, 200, 255, 255),
        width=3,
    )
    img.paste(logo_bg, (logo_x, logo_y), logo_bg)

    logo_offset = (ring_size - logo_size) // 2
    try:
        logo = load_image_from_url(logo_url).convert("RGBA")
        logo = make_circle(logo).resize((logo_size, logo_size))
        img.paste(logo, (logo_x + logo_offset, logo_y + logo_offset), logo)
    except Exception:
        placeholder = Image.new("RGBA", (logo_size, logo_size), (12, 36, 80, 200))
        placeholder_draw = ImageDraw.Draw(placeholder)
        placeholder_draw.ellipse(
            (2, 2, logo_size - 3, logo_size - 3),
            outline=(120, 200, 255, 200),
            width=2,
        )
        img.paste(placeholder, (logo_x + logo_offset, logo_y + logo_offset), placeholder)
        draw.text(
            (logo_x + ring_size / 2, logo_y + ring_size / 2),
            "COMMUNITIVE",
            font=font_sub,
            fill="#cfe6ff",
            anchor="mm",
            stroke_width=2,
            stroke_fill="#0b1e44",
        )

    # 5. Başlıklar
    draw.text(
        (W / 2, 470),
        "COMMUNITIVE DENTISTRY",
        font=font_header,
        fill="#e9f6ff",
        anchor="mm",
        stroke_width=2,
        stroke_fill="#0b1e44",
    )
    draw.text(
        (W / 2, 535),
        "ÜSKÜDAR",
        font=font_sub,
        fill="#e9f6ff",
        anchor="mm",
        stroke_width=2,
        stroke_fill="#0b1e44",
    )
    draw.text(
        (W / 2, 650),
        "2025",
        font=font_tagline,
        fill="#ffffff",
        anchor="mm",
        stroke_width=2,
        stroke_fill="#0b1e44",
    )
    draw.text(
        (W / 2, 780),
        "BINGO",
        font=font_bingo_title,
        fill="#d8f1ff",
        anchor="mm",
        stroke_width=2,
        stroke_fill="#0b1e44",
    )

    # 6. Izgara (Grid) Sistemi
    start_y = 880
    grid_gap = 30
    box_size = 280
    start_x = (W - (3 * box_size + 2 * grid_gap)) // 2

    # Bingo Maddeleri
    items = BINGO_ITEMS

    box_radius = 24
    shadow_offset = 6
    shadow_color = (3, 8, 20, 100)
    box_color = (72, 120, 170, 230)
    box_color_selected = (72, 120, 170, 230)
    border_color = (220, 240, 255, 230)
    border_color_selected = (255, 255, 255, 255)
    tick_color = (255, 120, 175, 190)
    text_color = "#f7fbff"
    text_stroke = "#1a355f"
    max_text_width = box_size - 36
    try:
        bbox = font_bingo.getbbox("Ag")
        line_height = bbox[3] - bbox[1] + 8
    except Exception:
        line_height = 46

    for i, item_text in enumerate(items):
        row = i // 3
        col = i % 3
        
        x = start_x + col * (box_size + grid_gap)
        y = start_y + row * (box_size + grid_gap)

        # Kutu Arka Planı
        is_selected = selected_items[i]

        shadow_bounds = [x + shadow_offset, y + shadow_offset, x + box_size + shadow_offset, y + box_size + shadow_offset]
        draw.rounded_rectangle(shadow_bounds, radius=box_radius, fill=shadow_color)

        fill_color = box_color_selected if is_selected else box_color
        outline_color = border_color_selected if is_selected else border_color
        draw.rounded_rectangle([x, y, x + box_size, y + box_size], radius=box_radius, fill=fill_color, outline=outline_color, width=3)

        if is_selected:
            draw_tick_mark(draw, (x, y, x + box_size, y + box_size), tick_color, width=16)

        # Metni Yaz (Wrap işlemi)
        wrapped = wrap_text(item_text, font_bingo, max_text_width)
        current_h = y + (box_size - (len(wrapped) * line_height)) // 2

        for line in wrapped:
            draw.text(
                (x + box_size / 2, current_h),
                line,
                font=font_bingo,
                fill=text_color,
                anchor="mm",
                stroke_width=2,
                stroke_fill=text_stroke,
            )
            current_h += line_height

    # 7. Alt Bilgi (Footer)
    if user_name:
        footer_text = f"@{user_name} x {INSTAGRAM_HANDLE}"
        footer_color = "#d7efff"
    else:
        footer_text = INSTAGRAM_HANDLE
        footer_color = "#d7efff"
    draw.text((W / 2, 1820), footer_text, font=font_footer, fill=footer_color, anchor="mm")
        
    return img

# --- ARAYÜZ (FRONTEND) ---

st.title("🎄 Communitive Dentistry Üsküdar 2025 Bingo")
st.write("Communitive Dentistry Üsküdar topluluğu için sana uyan maddeleri seç, ismini yaz ve Instagram hikayesi için kartını oluştur!")

# Kullanıcı İsmi
username = st.text_input("Instagram Kullanıcı Adın (Opsiyonel)", placeholder="örn: mahir.dt")

st.write("---")
st.subheader("Senin Durumun Ne?")

# Checkbox Grid
col1, col2, col3 = st.columns(3)
checks = []

items_list = BINGO_ITEMS

with col1:
    c1 = st.checkbox(items_list[0])
    c4 = st.checkbox(items_list[3])
    c7 = st.checkbox(items_list[6])
with col2:
    c2 = st.checkbox(items_list[1])
    c5 = st.checkbox(items_list[4])
    c8 = st.checkbox(items_list[7])
with col3:
    c3 = st.checkbox(items_list[2])
    c6 = st.checkbox(items_list[5])
    c9 = st.checkbox(items_list[8])

# Sıralamayı düzelt (1,2,3... diye gitmesi için)
selection_state = [c1, c2, c3, c4, c5, c6, c7, c8, c9]

st.write("---")

if st.button("✨ HİKAYEMİ OLUŞTUR ✨", type="primary"):
    with st.spinner("Bingo kartın hazırlanıyor..."):
        final_image = create_bingo_card(selection_state, username)
        
        card_html = build_card_html(items_list, selection_state, username)
        components.html(card_html, height=960, scrolling=False)
        st.caption("Communitive Dentistry Üsküdar Bingo Kartın Hazır!")
        
        # İndirme Butonu
        rgb_image = final_image.convert("RGB") if final_image.mode != "RGB" else final_image
        buf_png = BytesIO()
        rgb_image.save(buf_png, format="PNG", optimize=True)
        png_bytes = buf_png.getvalue()

        buf_jpg = BytesIO()
        rgb_image.save(buf_jpg, format="JPEG", quality=95, optimize=True)
        jpg_bytes = buf_jpg.getvalue()

        st.download_button(
            label="📥 RESMİ İNDİR (HD KALİTE)",
            data=png_bytes,
            file_name="communitive_dentistry_uskudar_bingo_2025.png",
            mime="image/png"
        )
        st.download_button(
            label="📥 RESMİ İNDİR (iPhone için JPG)",
            data=jpg_bytes,
            file_name="communitive_dentistry_uskudar_bingo_2025.jpg",
            mime="image/jpeg"
        )
        st.success(f"İndirdiğin resmi Instagram'da bizi etiketleyerek paylaşmayı unutma! {INSTAGRAM_HANDLE} 🎄")

st.write("---")
col_logo, col_info = st.columns([1, 3], gap="small")
with col_logo:
    st.image(LOGO_URL, width=120)
with col_info:
    st.subheader(COMMUNITY_NAME)
    st.markdown(f"[{WEBSITE_LABEL}]({WEBSITE_URL})")
    st.markdown(f"[{INSTAGRAM_HANDLE}]({INSTAGRAM_URL})")
