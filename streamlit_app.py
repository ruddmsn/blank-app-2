import streamlit as st

# -----------------------------
# Perfume Palette App (max 10 recommendations)
# -----------------------------

st.set_page_config(page_title="Perfume Palette", page_icon="🌸", layout="centered")
st.title("🌸 Perfume Palette")
st.caption("Select your preferred scent keywords and price range to get up to 10 recommended perfumes.")

# -----------------------------
# Sample perfume data with buy links
# -----------------------------
perfumes = [
    {"name": "Jo Malone Peony & Blush Suede", "notes": ["Floral (꽃)", "Romantic (로맨틱)"], "price": 180000,
     "link": "https://www.jomalone.com/product/12345/peony-blush-suede-cologne"},
    {"name": "Chanel No.5", "notes": ["Classic (클래식)", "Elegant (우아)"], "price": 250000,
     "link": "https://www.chanel.com/product/12345/no5"},
    {"name": "Dior Sauvage", "notes": ["Citrus (시트러스)", "Fresh (상쾌)"], "price": 150000,
     "link": "https://www.dior.com/product/12345/sauvage"},
    {"name": "Gucci Bloom", "notes": ["Floral (꽃)", "Feminine (여성스러움)"], "price": 170000,
     "link": "https://www.gucci.com/product/12345/bloom"},
    {"name": "CK One", "notes": ["Citrus (시트러스)", "Unisex (유니섹스)"], "price": 70000,
     "link": "https://www.calvinklein.com/product/12345/ckone"},
    {"name": "Davidoff Cool Water", "notes": ["Fresh (상쾌)", "Aqua (청량)"], "price": 60000,
     "link": "https://www.davidoff.com/product/12345/cool-water"},
    {"name": "Maison Margiela Replica Jazz Club", "notes": ["Woody (우디)", "Smoky (스모키)"], "price": 160000,
     "link": "https://www.maisonmargiela.com/product/12345/jazz-club"},
    {"name": "Tom Ford Black Orchid", "notes": ["Sensual (관능적)", "Intense (강렬)"], "price": 230000,
     "link": "https://www.tomford.com/product/12345/black-orchid"},
]

# -----------------------------
# Session state initialization
# -----------------------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "results" not in st.session_state:
    st.session_state.results = []

# -----------------------------
# 1. Scent keyword selection (multi-select)
# -----------------------------
st.subheader("🔹 Select preferred scent keywords (English with Korean)")
all_notes = sorted({note for p in perfumes for note in p["notes"]})
selected_notes = st.multiselect("Scent Keywords", options=all_notes)

# -----------------------------
# 2. Price range input
# -----------------------------
st.subheader("🔹 Price Range (KRW)")
col1, col2 = st.columns(2)
with col1:
    min_price = st.number_input("Minimum Price", min_value=0, value=0, step=1000)
with col2:
    max_price = st.number_input("Maximum Price", min_value=0, value=300000, step=1000)

# -----------------------------
# Recommendation logic
# -----------------------------
def recommend_perfumes(notes, min_p, max_p, limit=10):  # 최대 10개로 변경
    if not notes:
        return []
    filtered = [p for p in perfumes if any(n in p["notes"] for n in notes) and min_p <= p["price"] <= max_p]
    return filtered[:limit]

# -----------------------------
# Buttons
# -----------------------------
if st.button("Show Recommendations"):
    if not selected_notes:
        st.warning("Please select at least one scent keyword!")
    elif min_price > max_price:
        st.warning("Minimum price cannot exceed maximum price!")
    else:
        results = recommend_perfumes(selected_notes, min_price, max_price)
        st.session_state.results = results
        st.session_state.submitted = True

if st.button("Reset"):
    st.session_state.submitted = False
    st.session_state.results = []
    selected_notes = []
    min_price = 0
    max_price = 300000

# -----------------------------
# Result display
# -----------------------------
st.markdown("---")
st.subheader("💎 Recommended Perfumes")

if st.session_state.submitted:
    if st.session_state.results:
        for p in st.session_state.results:
            st.markdown(f"- **{p['name']}** ({', '.join(p['notes'])}) [{p['price']:,} KRW] - [Buy Here]({p['link']})")
    else:
        st.info("No perfumes match your selected keywords and price range. Try different options!")
else:
    st.write("Select scent keywords and price range, then click 'Show Recommendations'.")
