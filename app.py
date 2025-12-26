import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO
import textwrap

COMMUNITY_NAME = "Communitive Dentistry Üsküdar"
WEBSITE_URL = "https://worp.me/communitiveuudhf"
WEBSITE_LABEL = "worp.me/communitiveuudhf"
INSTAGRAM_URL = "https://www.instagram.com/communitive.uudhf/"
INSTAGRAM_HANDLE = "@communitive.uudhf"
LOGO_URL = "https://i.imgur.com/EydFZfb.jpeg"
INSTAGRAM_ICON_URL = "https://i.imgur.com/OWdUupI.png"
LOCAL_FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Helvetica.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:\\Windows\\Fonts\\arial.ttf",
]

# --- SAYFA AYARLARI ---
st.set_page_config(page_title=f"{COMMUNITY_NAME} Bingo", page_icon="🦷", layout="centered")

# --- CSS İLE GÖRÜNÜMÜ GÜZELLEŞTİRME ---
st.markdown("""
    <style>
    .stApp {
        background-color: #1a0505;
    }
    h1, h2, h3, p, label {
        color: white !important;
        font-family: 'Helvetica', sans-serif;
    }
    .stButton>button {
        background-color: #8B0000;
        color: #ffffff;
        border-radius: 20px;
        width: 100%;
        border: 1px solid #ffffff;
        font-weight: 700;
    }
    .stDownloadButton>button {
        background-color: #8B0000;
        color: #ffffff;
        border-radius: 20px;
        width: 100%;
        border: 1px solid #ffffff;
        font-weight: 700;
    }
    .stButton>button:hover,
    .stDownloadButton>button:hover {
        background-color: #b30000;
        color: #ffffff;
        border: 1px solid #ffffff;
    }
    .brand-block {
        margin: 10px 0 0 0;
    }
    .brand-title {
        color: #fffdd0;
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .brand-links {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        align-items: center;
        font-size: 0.95rem;
    }
    .brand-links a {
        color: #ffcc00;
        text-decoration: none;
    }
    .brand-links a:hover {
        text-decoration: underline;
    }
    .brand-links img {
        width: 18px;
        height: 18px;
        margin-right: 6px;
        vertical-align: -3px;
    }
    .brand-divider {
        color: rgba(255, 255, 255, 0.4);
    }
    /* Checkbox boyutlarını büyüt */
    .stCheckbox {
        background-color: rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- YARDIMCI FONKSİYONLAR ---

@st.cache_data
def load_image_from_url(url):
    response = requests.get(url)
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

def make_circle(img):
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)
    result = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    result.putalpha(mask)
    return result

def wrap_text(text, font, max_width):
    lines = []
    if font.getlength(text) <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0
        while i < len(words):
            line = ''
            while i < len(words) and font.getlength(line + words[i]) <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines

# --- GÖRSEL OLUŞTURMA MOTORU ---
def create_bingo_card(selected_items, user_name):
    # 1. Canvas Oluştur (1080x1920 - Instagram Story)
    W, H = 1080, 1920
    img = Image.new('RGBA', (W, H), color='#3a0505')
    draw = ImageDraw.Draw(img)

    # 2. Arka Planı Yükle (Öğrenci Masası Teması)
    bg_url = "https://i.imgur.com/8yX0qXy.jpeg" 
    try:
        bg = load_image_from_url(bg_url).convert("RGBA")
        bg = ImageOps.fit(bg, (W, H))
        # Kırmızı filtre ekle
        overlay = Image.new('RGBA', (W, H), (60, 10, 10, 180))
        img = Image.alpha_composite(bg, overlay)
        draw = ImageDraw.Draw(img) # Draw nesnesini güncelle
    except:
        pass # Yüklenemezse düz renk kalır

    # 3. Fontları Yükle (Google Fonts'tan direkt çekiyoruz)
    # Başlık fontu: Mountains of Christmas
    title_font_url = "https://github.com/google/fonts/raw/main/apache/mountainsofchristmas/MountainsofChristmas-Bold.ttf"
    # Yazı fontu: Poppins veya Roboto
    body_font_url = "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-SemiBold.ttf"
    
    font_header = load_font_with_fallback(title_font_url, 120, LOCAL_FONT_PATHS)
    font_sub = load_font_with_fallback(title_font_url, 80, LOCAL_FONT_PATHS)
    font_tagline = load_font_with_fallback(body_font_url, 60, LOCAL_FONT_PATHS)
    font_bingo = load_font_with_fallback(body_font_url, 40, LOCAL_FONT_PATHS)
    font_footer = load_font_with_fallback(body_font_url, 35, LOCAL_FONT_PATHS)

    # 4. Logo Yerleşimi (Kar Küresi Efekti)
    logo_url = LOGO_URL
    try:
        logo = load_image_from_url(logo_url).convert("RGBA")
        logo = make_circle(logo)
        logo = logo.resize((300, 300))
        # Beyaz ve Kırmızı Çerçeve
        logo_bg = Image.new("RGBA", (320, 320), (255, 255, 255, 255))
        draw_logo_bg = ImageDraw.Draw(logo_bg)
        draw_logo_bg.ellipse((0, 0, 320, 320), fill=(255,255,255), outline=(139,0,0), width=10)
        
        # Logoyu ortala
        logo_x = (W - 320) // 2
        logo_y = 150
        
        # Maskeleyerek yapıştır
        mask = Image.new("L", (320, 320), 0)
        d_mask = ImageDraw.Draw(mask)
        d_mask.ellipse((0,0,320,320), fill=255)
        
        img.paste(logo_bg, (logo_x, logo_y), mask)
        img.paste(logo, (logo_x + 10, logo_y + 10), logo)
    except:
        pass

    # 5. Başlıklar
    draw.text((W/2, 500), "COMMUNITIVE", font=font_header, fill="#fffdd0", anchor="mm")
    draw.text((W/2, 590), "DENTISTRY ÜSKÜDAR", font=font_sub, fill="white", anchor="mm")
    draw.text((W/2, 670), "2025 BINGO", font=font_tagline, fill="white", anchor="mm")

    # 6. Izgara (Grid) Sistemi
    start_y = 750
    grid_gap = 40
    box_size = 280
    start_x = (W - (3 * box_size + 2 * grid_gap)) // 2

    # Bingo Maddeleri
    items = [
        "Etkinlikte Story Attım", "Elimi/Önlüğümü Yaktım", "Sabun Değil Diş Yontuyorum",
        "Vizeden Önce Uyumadım", "Anakalbi Anaokuluna Gittim", "Hasta Gelmeyince Sevindim",
        "Sülaleye Diş Sözü Verdim", "Not Dilendim", "Grubu Sabitledim"
    ]

    tick_url = "https://i.imgur.com/Pk74M3p.png"
    try:
        tick_img = load_image_from_url(tick_url).convert("RGBA")
        tick_img = tick_img.resize((200, 200))
    except:
        tick_img = None

    for i, item_text in enumerate(items):
        row = i // 3
        col = i % 3
        
        x = start_x + col * (box_size + grid_gap)
        y = start_y + row * (box_size + grid_gap)

        # Kutu Arka Planı
        is_selected = selected_items[i]
        
        box_color = (189, 46, 46, 200) if not is_selected else (100, 10, 10, 230)
        border_color = (255, 255, 255, 100) if not is_selected else (255, 204, 0, 255)
        
        # Kutuyu Çiz
        draw.rounded_rectangle([x, y, x+box_size, y+box_size], radius=20, fill=box_color, outline=border_color, width=3)

        # Metni Yaz (Wrap işlemi)
        wrapped = textwrap.wrap(item_text, width=12) # Satır başı karakter sayısı
        current_h = y + (box_size - (len(wrapped) * 45)) // 2 # Dikey ortalama
        
        for line in wrapped:
            draw.text((x + box_size/2, current_h), line, font=font_bingo, fill="white", anchor="mm")
            current_h += 45

        # Tik İşareti
        if is_selected and tick_img:
            tick_x = x + (box_size - 200) // 2
            tick_y = y + (box_size - 200) // 2
            img.paste(tick_img, (int(tick_x), int(tick_y)), tick_img)

    # 7. Alt Bilgi (Footer)
    if user_name:
        footer_text = f"@{user_name} x {INSTAGRAM_HANDLE}"
        footer_color = "#ffcc00"
    else:
        footer_text = INSTAGRAM_HANDLE
        footer_color = "white"
    draw.text((W/2, 1750), footer_text, font=font_footer, fill=footer_color, anchor="mm")
        
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

items_list = [
    "Etkinlikte Story Attım", "Elimi/Önlüğümü Yaktım", "Sabun Değil Diş Yontuyorum",
    "Vizeden Önce Uyumadım", "Anakalbi Anaokuluna Gittim", "Hasta Gelmeyince Sevindim",
    "Sülaleye Diş Sözü Verdim", "Not Dilendim", "Grubu Sabitledim"
]

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
        
        # Ekranda önizleme göster (daha küçük boyutta)
        # GÜNCELLENMİŞ SATIR BURADA:
        st.image(final_image, caption="Communitive Dentistry Üsküdar Bingo Kartın Hazır!", use_column_width=True)
        
        # İndirme Butonu
        buf = BytesIO()
        final_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="📥 RESMİ İNDİR (HD KALİTE)",
            data=byte_im,
            file_name="communitive_dentistry_uskudar_bingo_2025.png",
            mime="image/png"
        )
        st.success(f"İndirdiğin resmi Instagram'da bizi etiketleyerek paylaşmayı unutma! {INSTAGRAM_HANDLE} 🎄")

st.write("---")
col_logo, col_info = st.columns([1, 3], gap="small")
with col_logo:
    st.image(LOGO_URL, width=120)
with col_info:
    st.markdown(
        f"""
        <div class="brand-block">
            <div class="brand-title">{COMMUNITY_NAME}</div>
            <div class="brand-links">
                <a href="{WEBSITE_URL}" target="_blank">{WEBSITE_LABEL}</a>
                <span class="brand-divider">•</span>
                <a href="{INSTAGRAM_URL}" target="_blank">
                    <img src="{INSTAGRAM_ICON_URL}" alt="Instagram" />
                    {INSTAGRAM_HANDLE}
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
