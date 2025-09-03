import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="River Crossing Puzzle", layout="wide")
st.title("🛶 River Crossing Puzzle")

st.markdown("""
### Rules:
- 👨 must always be in the boat to cross the river
- The boat can only carry 👨 and one item at a time
- If left alone, 🐺 will eat 🐐
- If left alone, 🐐 will eat 🥬
""")

# Initial game state (stored in session)
if "left" not in st.session_state:
    st.session_state.left = ["👨", "🐺", "🐐", "🥬"]
    st.session_state.right = []
    st.session_state.boat = []
    st.session_state.boat_side = "left"
    st.session_state.message = ""

# Game logic
def check_game_over():
    left = st.session_state.left.copy()
    right = st.session_state.right.copy()

    # Check left side danger
    if "🐺" in left and "🐐" in left and "👨" not in left:
        return "🐺 ate 🐐! Game Over."
    if "🐐" in left and "🥬" in left and "👨" not in left:
        return "🐐 ate 🥬! Game Over."

    # Check right side danger
    if "🐺" in right and "🐐" in right and "👨" not in right:
        return "🐺 ate 🐐! Game Over."
    if "🐐" in right and "🥬" in right and "👨" not in right:
        return "🐐 ate 🥬! Game Over."

    # Check win
    if sorted(st.session_state.right) == sorted(["👨", "🐺", "🐐", "🥬"]):
        return "🎉 You Win! All safely crossed."

    return ""

st.markdown("""
<style>
.zone {
    border: 3px solid #a16c43;
    border-radius: 15px;
    padding: 10px;
    background-color: #90ee90;
    text-align: center;
    font-size: 30px;
    height: 200px;
}
.river {
    background-color: #add8e6;
    padding: 20px;
    border-radius: 15px;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
}
.reset-btn button {
    background-color: #1E90FF;
    color: white;
    padding: 10px;
    font-size: 16px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# UI Layout
left_col, river_col, right_col = st.columns([3, 2, 3])

with left_col:
    st.markdown("#### 🌊 Left Bank")
    st.markdown(f'<div class="zone">{" ".join(st.session_state.left)}</div>', unsafe_allow_html=True)

with river_col:
    st.markdown("#### 🚣 Boat Area")
    st.markdown(f'<div class="river">{" ".join(st.session_state.boat)}<br><b>Boat is on the {st.session_state.boat_side} side</b></div>', unsafe_allow_html=True)

with right_col:
    st.markdown("#### Right Bank 🌊")
    st.markdown(f'<div class="zone">{" ".join(st.session_state.right)}</div>', unsafe_allow_html=True)

st.markdown("---")
st.subheader("🕹️ Controls")

# Move to boat
for item in st.session_state.left if st.session_state.boat_side == "left" else st.session_state.right:
    if len(st.session_state.boat) < 2 and item not in st.session_state.boat:
        if st.button(f"Put {item} in boat"):
            if st.session_state.boat_side == "left":
                st.session_state.left.remove(item)
            else:
                st.session_state.right.remove(item)
            st.session_state.boat.append(item)
            st.session_state.message = ""

# Remove from boat
for item in st.session_state.boat:
    if st.button(f"Remove {item} from boat"):
        if st.session_state.boat_side == "left":
            st.session_state.left.append(item)
        else:
            st.session_state.right.append(item)
        st.session_state.boat.remove(item)
        st.session_state.message = ""

# Cross river
if st.button("🚣 Cross the river"):
    if "👨" not in st.session_state.boat:
        st.session_state.message = "👨 must be in the boat to row."
    else:
        st.session_state.boat_side = "right" if st.session_state.boat_side == "left" else "left"
        for item in st.session_state.boat:
            if st.session_state.boat_side == "left":
                st.session_state.left.append(item)
            else:
                st.session_state.right.append(item)
        st.session_state.boat = []
        st.session_state.message = check_game_over()

# Reset
st.markdown("<div class='reset-btn'>", unsafe_allow_html=True)
if st.button("🔁 Reset Game"):
    st.session_state.left = ["👨", "🐺", "🐐", "🥬"]
    st.session_state.right = []
    st.session_state.boat = []
    st.session_state.boat_side = "left"
    st.session_state.message = ""
st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.message:
    st.markdown(f"### 📝 {st.session_state.message}")
