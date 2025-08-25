import streamlit as st

# -----------------------------
# Perfume Palette 앱 (객관식 키워드 + 가격 범위 추천)
# -----------------------------

st.set_page_config(page_title="Perfume Palette", page_icon="🌸", layout="centered")
st.title("🌸 Perfume Palette")
# -----------------------------
# 샘플 향수 데이터 (가격 단위: 원)
# -----------------------------
perfumes = [
    {"name": "Jo Malone Peony & Blush Suede", "notes": ["꽃", "로맨틱"], "price": 180000},
    {"name": "Chanel No.5", "notes": ["클래식", "우아"], "price": 250000},
    {"name": "Dior Sauvage", "notes": ["시트러스", "상쾌"], "price": 150000},
    {"name": "Gucci Bloom", "notes": ["꽃", "여성스러움"], "price": 170000},
    {"name": "CK One", "notes": ["시트러스", "유니섹스"], "price": 70000},
    {"name": "Davidoff Cool Water", "notes": ["상쾌", "청량"], "price": 60000},
    {"name": "Maison Margiela Replica Jazz Club", "notes": ["우디", "스모키"], "price": 160000},
    {"name": "Tom Ford Black Orchid", "notes": ["관능적", "강렬"], "price": 230000},
]

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "results" not in st.session_state:
    st.session_state.results = []

# -----------------------------
# 1. 향 키워드 선택 (체크박스 멀티셀렉트)
# -----------------------------
st.subheader("🔹 원하는 향 키워드 선택 (여러 개 선택 가능)")
all_notes = sorted({note for p in perfumes for note in p["notes"]})
selected_notes = st.multiselect("향 키워드", options=all_notes)

# -----------------------------
# 2. 가격 범위 입력
# -----------------------------
st.subheader("🔹 가격 범위 입력 (원)")
col1, col2 = st.columns(2)
with col1:
    min_price = st.number_input("최소 가격", min_value=0, value=0, step=1000)
with col2:
    max_price = st.number_input("최대 가격", min_value=0, value=300000, step=1000)

# -----------------------------
# 추천 로직
# -----------------------------
def recommend_perfumes(notes, min_p, max_p, limit=3):
    if not notes:
        return []
    filtered = [p for p in perfumes if any(n in p["notes"] for n in notes) and min_p <= p["price"] <= max_p]
    return filtered[:limit]

# -----------------------------
# 버튼 처리
# -----------------------------
if st.button("결과 보기"):
    if not selected_notes:
        st.warning("향 키워드를 최소 1개 선택해주세요!")
    elif min_price > max_price:
        st.warning("최소 가격이 최대 가격보다 클 수 없습니다!")
    else:
        results = recommend_perfumes(selected_notes, min_price, max_price)
        st.session_state.results = results
        st.session_state.submitted = True

if st.button("다시 하기"):
    st.session_state.submitted = False
    st.session_state.results = []
    selected_notes = []
    min_price = 0
    max_price = 300000

# -----------------------------
# 결과 출력
# -----------------------------
st.markdown("---")
st.subheader("💎 추천 향수 결과")

if st.session_state.submitted:
    if st.session_state.results:
        for p in st.session_state.results:
            st.write(f"- {p['name']} ({', '.join(p['notes'])}) [{p['price']:,}원]")
    else:
        st.info("해당 조건에 맞는 향수를 찾을 수 없습니다. 다른 키워드나 가격 범위를 선택해보세요!")
else:
    st.write("향 키워드와 가격 범위를 선택하고 '결과 보기' 버튼을 눌러주세요.")
