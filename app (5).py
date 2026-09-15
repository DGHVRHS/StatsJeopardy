import streamlit as st

st.set_page_config(page_title="Jeopardy!", layout="wide")

# Game Data with 5 Categories
JEOPARDY_DATA = {
    "Take Me Home Country Roads": [
        {"val": 200, "q": "This city serves as the capital of West Virginia.", "a": "Charleston"},
        {"val": 400, "q": "The state motto 'Montani Semper Liberi' translates to this in English.", "a": "Mountaineers Are Always Free"},
        {"val": 600, "q": "This famous bridge hosts an annual festival where extreme sports enthusiasts BASE jump off it.", "a": "New River Gorge Bridge"},
        {"val": 800, "q": "West Virginia officially split from Virginia and became a state in this year during the Civil War.", "a": "1863"},
        {"val": 1000, "q": "This native West Virginia apple variety was discovered in Clay County in 1905.", "a": "Golden Delicious"}
    ],
    "Observation or Experiment": [
        {"val": 200, "q": "In this type of study, researchers merely observe and record data without imposing any treatment on subjects.", "a": "Observational Study"},
        {"val": 400, "q": "In this type of study design, researchers deliberately apply treatments to subjects to establish cause-and-effect.", "a": "Experiment"},
        {"val": 600, "q": "A setup where neither the subjects nor the researchers evaluating the outcomes know who received which treatment.", "a": "Double-Blind Study"},
        {"val": 800, "q": "This term refers to an unmeasured variable associated with both the explanatory and response variables that distorts results.", "a": "Confounding Variable"},
        {"val": 1000, "q": "An inactive treatment given to a control group (like a sugar pill) to isolate psychological effects.", "a": "Placebo"}
    ],
    "Gone Fishing": [
        {"val": 200, "q": "This fish loves lingering at the bottom of the tank, has long 'whiskers' (barbels), and cleans up every scrap of food.", "a": "Catfish"},
        {"val": 400, "q": "This energetic fish has a huge mouth, loves showing off, and is North America's most popular freshwater game fish.", "a": "Largemouth Bass"},
        {"val": 600, "q": "This fish sports a multicolored stripe down its side while swimming upstream through cold, clear streams.", "a": "Rainbow Trout"},
        {"val": 800, "q": "This mysterious deep-sea fish carries its own bioluminescent glowing flashlight lure right on top of its head.", "a": "Anglerfish"},
        {"val": 1000, "q": "This sensitive fish inflates like a spiky balloon whenever it feels threatened or stressed.", "a": "Pufferfish (or Blowfish)"}
    ],
    "Bias": [
        {"val": 200, "q": "This sampling method lets individuals choose whether to participate (e.g., online polls), leading to strong opinions over-representing results.", "a": "Voluntary Response Sampling"},
        {"val": 400, "q": "This bias occurs when certain groups within the population are systematically left out of the sample selection process.", "a": "Undercoverage Bias"},
        {"val": 600, "q": "This non-random sampling technique selects individuals who are easiest to reach, such as surveying people nearby at a single location.", "a": "Convenience Sampling"},
        {"val": 800, "q": "This bias occurs when selected individuals refuse or are unable to participate in the survey.", "a": "Nonresponse Bias"},
        {"val": 1000, "q": "This concept describes how much sample statistics naturally differ from sample to sample, which can be reduced by increasing sample size.", "a": "Sampling Variability"}
    ],
    "Poker Night": [
        {"val": 200, "q": "What is the probability of drawing a Red card from a standard deck?\n\n*Hint: Deck has 52 cards total (26 Red, 26 Black).*", "a": "26/52 = 1/2 (50%)"},
        {"val": 400, "q": "What is the probability of drawing an Ace on a single draw?\n\n*Hint: There are 4 Aces in a 52-card deck.*", "a": "4/52 = 1/13 (≈ 7.69%)"},
        {"val": 600, "q": "What is the probability of drawing a Face Card (Jack, Queen, or King)?\n\n*Hint: There are 3 face cards per suit across 4 suits.", "a": "12/52 = 3/13 (≈ 23.08%)"},
        {"val": 800, "q": "You draw 2 cards without replacement. What is the probability that BOTH are Aces?\n\n*Hint: P(1st Ace) × P(2nd Ace).", "a": "12/2652 = 1/221 (≈ 0.45%)"},
        {"val": 1000, "q": "What is the probability of drawing either a Heart OR a King?\n\n*Hint: Use Addition Rule: P(Heart) + P(King) - P(King of Hearts).", "a": "16/52 = 4/13 (≈ 30.77%)"}
    ]
}

# Session State Initialization
if "scores" not in st.session_state:
    st.session_state.scores = {"Team 1": 0, "Team 2": 0, "Team 3": 0, "Team 4": 0}
if "used_questions" not in st.session_state:
    st.session_state.used_questions = set()
if "active_q" not in st.session_state:
    st.session_state.active_q = None

st.title("🏆 Stats Jeopardy!")

# Scoreboard Sidebar
st.sidebar.header("Scoreboard")
for team in st.session_state.scores:
    st.session_state.scores[team] = st.sidebar.number_input(
        f"{team}", value=st.session_state.scores[team], step=100
    )

if st.sidebar.button("Reset Entire Game"):
    st.session_state.scores = {"Team 1": 0, "Team 2": 0, "Team 3": 0, "Team 4": 0}
    st.session_state.used_questions = set()
    st.session_state.active_q = None
    st.rerun()

# Active Question Display
if st.session_state.active_q:
    q_data = st.session_state.active_q
    st.info(f"**Category:** {q_data['cat']} | **Value:** ${q_data['val']}")
    
    st.markdown(f"### {q_data['q']}")
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Show Answer"):
            st.success(f"**Answer:** {q_data['a']}")
    
    st.write("### Award Points:")
    score_cols = st.columns(4)
    for idx, team in enumerate(st.session_state.scores):
        if score_cols[idx].button(f"+${q_data['val']} to {team}"):
            st.session_state.scores[team] += q_data['val']
            st.session_state.active_q = None
            st.rerun()
            
    if st.button("Close Question without Points"):
        st.session_state.active_q = None
        st.rerun()

else:
    # Jeopardy Board Grid
    categories = list(JEOPARDY_DATA.keys())
    cols = st.columns(len(categories))

    for cat_idx, cat in enumerate(categories):
        with cols[cat_idx]:
            st.markdown(f"### {cat}")
            for q_idx, item in enumerate(JEOPARDY_DATA[cat]):
                q_id = f"{cat}_{q_idx}"
                if q_id in st.session_state.used_questions:
                    st.button(f"---", key=q_id, disabled=True, use_container_width=True)
                else:
                    if st.button(f"${item['val']}", key=q_id, use_container_width=True):
                        st.session_state.used_questions.add(q_id)
                        st.session_state.active_q = {**item, "cat": cat}
                        st.rerun()
