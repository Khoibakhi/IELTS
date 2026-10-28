import streamlit as st
import json
import os
import glob

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="IELTS Practice",
    page_icon="📚",
    layout="wide"
)

DATA_DIR = "data"
AUDIO_DIR = "audio"


# =========================
# LOAD DATA
# =========================

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Không thể đọc file: {path}")
        st.error(str(e))
        return None


def get_tests(skill):
    folder = os.path.join(DATA_DIR, skill)

    if not os.path.exists(folder):
        return []

    files = sorted(glob.glob(os.path.join(folder, "*.json")))

    tests = []

    for file in files:
        data = load_json(file)

        if data:
            tests.append({
                "file": file,
                "data": data
            })

    return tests


# =========================
# SESSION STATE
# =========================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "skill" not in st.session_state:
    st.session_state.skill = None

if "selected_test" not in st.session_state:
    st.session_state.selected_test = None


# =========================
# CSS
# =========================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 700;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #666;
    margin-bottom: 40px;
}

.skill-card {
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #ddd;
    text-align: center;
    margin-bottom: 20px;
}

.question-box {
    padding: 20px;
    border-radius: 12px;
    background-color: #f7f7f7;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HOME
# =========================

def home():

    st.markdown(
        '<div class="main-title">IELTS PRACTICE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Practice IELTS whenever you want</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="skill-card"><h2>📖 Reading</h2>'
            '<p>Practice IELTS Reading</p></div>',
            unsafe_allow_html=True
        )

        if st.button("Start Reading", use_container_width=True):
            st.session_state.page = "tests"
            st.session_state.skill = "reading"
            st.rerun()

    with col2:

        st.markdown(
            '<div class="skill-card"><h2>🎧 Listening</h2>'
            '<p>Practice IELTS Listening</p></div>',
            unsafe_allow_html=True
        )

        if st.button("Start Listening", use_container_width=True):
            st.session_state.page = "tests"
            st.session_state.skill = "listening"
            st.rerun()

    col3, col4 = st.columns(2)

    with col3:

        st.markdown(
            '<div class="skill-card"><h2>✍️ Writing</h2>'
            '<p>Practice IELTS Writing</p></div>',
            unsafe_allow_html=True
        )

        if st.button("Start Writing", use_container_width=True):
            st.session_state.page = "tests"
            st.session_state.skill = "writing"
            st.rerun()

    with col4:

        st.markdown(
            '<div class="skill-card"><h2>🗣️ Speaking</h2>'
            '<p>Practice IELTS Speaking</p></div>',
            unsafe_allow_html=True
        )

        if st.button("Start Speaking", use_container_width=True):
            st.session_state.page = "tests"
            st.session_state.skill = "speaking"
            st.rerun()


# =========================
# TEST SELECTION
# =========================

def test_selection():

    skill = st.session_state.skill

    skill_names = {
        "reading": "📖 Reading",
        "listening": "🎧 Listening",
        "writing": "✍️ Writing",
        "speaking": "🗣️ Speaking"
    }

    st.title(skill_names[skill])

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.session_state.skill = None
        st.rerun()

    st.divider()

    tests = get_tests(skill)

    if not tests:
        st.warning(
            f"Hiện chưa có đề {skill_names[skill]}. "
            "Bạn hãy thêm file JSON vào thư mục data."
        )
        return

    st.subheader("Chọn đề")

    for index, test in enumerate(tests):

        data = test["data"]

        title = data.get(
            "title",
            f"{skill_names[skill]} Test {index + 1}"
        )

        description = data.get(
            "description",
            ""
        )

        col1, col2 = st.columns([4, 1])

        with col1:

            st.markdown(f"### {title}")

            if description:
                st.write(description)

        with col2:

            if st.button(
                "Start",
                key=f"start_{skill}_{index}",
                use_container_width=True
            ):

                st.session_state.selected_test = data
                st.session_state.page = "test"
                st.rerun()

        st.divider()


# =========================
# READING
# =========================

def reading_test(data):

    st.title("📖 IELTS Reading")

    if st.button("← Back to Tests"):
        st.session_state.page = "tests"
        st.session_state.selected_test = None
        st.rerun()

    st.divider()

    st.header(data.get("title", "Reading Test"))

    passage = data.get("passage", "")

    st.subheader("Reading Passage")

    st.markdown(
        f"""
        <div style="
            padding:25px;
            border:1px solid #ddd;
            border-radius:12px;
            line-height:1.8;
        ">
        {passage}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    questions = data.get("questions", [])

    st.subheader("Questions")

    answers = {}

    for i, q in enumerate(questions):

        st.markdown(
            f"### Question {i + 1}"
        )

        st.write(q["question"])

        q_type = q.get("type", "multiple_choice")

        if q_type == "multiple_choice":

            options = q.get("options", [])

            answers[i] = st.radio(
                "Choose your answer:",
                options,
                key=f"reading_q_{i}"
            )

        elif q_type == "text":

            answers[i] = st.text_input(
                "Your answer:",
                key=f"reading_q_{i}"
            )

        st.write("")

    if st.button(
        "Submit Answers",
        type="primary",
        use_container_width=True
    ):

        score = 0

        for i, q in enumerate(questions):

            correct = str(
                q.get("answer", "")
            ).strip().lower()

            user_answer = str(
                answers.get(i, "")
            ).strip().lower()

            if user_answer == correct:
                score += 1

        st.success(
            f"Bạn đúng {score}/{len(questions)} câu."
        )


# =========================
# LISTENING
# =========================

def listening_test(data):

    st.title("🎧 IELTS Listening")

    if st.button("← Back to Tests"):
        st.session_state.page = "tests"
        st.session_state.selected_test = None
        st.rerun()

    st.divider()

    st.header(data.get("title", "Listening Test"))

    audio_file = data.get("audio")

    if audio_file:

        audio_path = os.path.join(
            AUDIO_DIR,
            audio_file
        )

        if os.path.exists(audio_path):

            with open(audio_path, "rb") as f:
                audio_bytes = f.read()

            st.audio(
                audio_bytes,
                format="audio/mp3"
            )

        else:

            st.warning(
                f"Không tìm thấy file audio: {audio_file}"
            )

    questions = data.get("questions", [])

    answers = {}

    for i, q in enumerate(questions):

        st.markdown(
            f"### Question {i + 1}"
        )

        st.write(q["question"])

        options = q.get("options")

        if options:

            answers[i] = st.radio(
                "Choose your answer:",
                options,
                key=f"listening_q_{i}"
            )

        else:

            answers[i] = st.text_input(
                "Your answer:",
                key=f"listening_q_{i}"
            )

    if st.button(
        "Submit Answers",
        type="primary",
        use_container_width=True
    ):

        score = 0

        for i, q in enumerate(questions):

            correct = str(
                q.get("answer", "")
            ).strip().lower()

            user_answer = str(
                answers.get(i, "")
            ).strip().lower()

            if user_answer == correct:
                score += 1

        st.success(
            f"Bạn đúng {score}/{len(questions)} câu."
        )


# =========================
# WRITING
# =========================

def writing_test(data):

    st.title("✍️ IELTS Writing")

    if st.button("← Back to Tests"):
        st.session_state.page = "tests"
        st.session_state.selected_test = None
        st.rerun()

    st.divider()

    st.header(data.get("title", "Writing Test"))

    task = data.get("task", "")

    st.markdown("### Question")

    st.info(task)

    answer = st.text_area(
        "Write your answer here:",
        height=400
    )

    words = len(answer.split())

    st.write(f"**Word count: {words}**")

    if st.button(
        "Submit",
        type="primary",
        use_container_width=True
    ):

        st.success("Đã nộp bài!")

        st.write(
            "Bạn có thể tích hợp AI chấm Writing "
            "ở bước phát triển tiếp theo."
        )


# =========================
# SPEAKING
# =========================

def speaking_test(data):

    st.title("🗣️ IELTS Speaking")

    if st.button("← Back to Tests"):
        st.session_state.page = "tests"
        st.session_state.selected_test = None
        st.rerun()

    st.divider()

    st.header(data.get("title", "Speaking Test"))

    questions = data.get("questions", [])

    for i, question in enumerate(questions):

        st.markdown(
            f"### Question {i + 1}"
        )

        st.info(question)

    st.divider()

    st.write(
        "Bạn có thể thêm chức năng ghi âm Speaking "
        "ở phiên bản tiếp theo."
    )


# =========================
# ROUTING
# =========================

if st.session_state.page == "home":

    home()

elif st.session_state.page == "tests":

    test_selection()

elif st.session_state.page == "test":

    skill = st.session_state.skill
    data = st.session_state.selected_test

    if skill == "reading":

        reading_test(data)

    elif skill == "listening":

        listening_test(data)

    elif skill == "writing":

        writing_test(data)

    elif skill == "speaking":

        speaking_test(data)
