import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Chintu's AI Chatbot",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* =====================================================
       MAIN PAGE
       ===================================================== */

    .main {
        background-color: #0e1117;
    }

    .chat-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 25px;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background-color: #20212a;
    }


    /* Sidebar main content */

    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.8rem;
        padding-bottom: 0.5rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
        overflow-y: auto;
    }


    /* Sidebar buttons */

    section[data-testid="stSidebar"] button {
        border-radius: 10px;
        min-height: 36px;
        padding-top: 4px;
        padding-bottom: 4px;
        transition: 0.2s ease;
    }


    /* =====================================================
       SIDEBAR HEADINGS
       ===================================================== */

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        margin-top: 8px;
        margin-bottom: 10px;
    }


    /* =====================================================
       SEARCH BOX
       ===================================================== */

    section[data-testid="stSidebar"] input {
        border-radius: 10px;
    }


    /* =====================================================
       CHAT HISTORY
       ===================================================== */

    .history-label {
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 5px;
    }


    /* =====================================================
       CHAT HISTORY SCROLL AREA
       ===================================================== */

    section[data-testid="stSidebar"]
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 10px;
    }


    /* =====================================================
       CHAT SETTINGS
       ===================================================== */

    section[data-testid="stSidebar"]
    [data-testid="stTextInput"] {
        margin-bottom: 8px;
    }


    /* =====================================================
       DIVIDERS
       ===================================================== */

    section[data-testid="stSidebar"] hr {
        margin-top: 8px;
        margin-bottom: 8px;
    }


    /* =====================================================
       CHAT INPUT
       ===================================================== */

    div[data-testid="stChatInput"] {
        border-radius: 14px;
    }

    div[data-testid="stChatInput"] textarea {
        font-size: 16px;
    }


    /* =====================================================
       CHAT MESSAGES
       ===================================================== */

    div[data-testid="stChatMessage"] {
        padding-top: 10px;
        padding-bottom: 10px;
    }


    /* Message content */

    div[data-testid="stChatMessage"] p {
        font-size: 16px;
        line-height: 1.65;
    }


    /* Headings inside AI responses */

    div[data-testid="stChatMessage"] h1,
    div[data-testid="stChatMessage"] h2,
    div[data-testid="stChatMessage"] h3 {
        margin-top: 12px;
        margin-bottom: 8px;
    }


    /* Lists */

    div[data-testid="stChatMessage"] ul,
    div[data-testid="stChatMessage"] ol {
        padding-left: 25px;
    }


    /* Inline code */

    div[data-testid="stChatMessage"] code {
        border-radius: 5px;
        padding: 2px 5px;
    }


    /* Code blocks */

    div[data-testid="stChatMessage"] pre {
        border-radius: 10px;
        padding: 15px;
        overflow-x: auto;
    }


    /* Links */

    div[data-testid="stChatMessage"] a {
        text-decoration: none;
    }


    /* Horizontal lines */

    div[data-testid="stChatMessage"] hr {
        margin-top: 15px;
        margin-bottom: 15px;
    }


    /* =====================================================
       STATUS TEXT
       ===================================================== */

    .status-text {
        color: #9ca3af;
        font-size: 14px;
    }


    /* =====================================================
       SCROLLBAR
       ===================================================== */

    section[data-testid="stSidebar"]::-webkit-scrollbar {
        width: 7px;
    }

    section[data-testid="stSidebar"]::-webkit-scrollbar-track {
        background: #20212a;
    }

    section[data-testid="stSidebar"]::-webkit-scrollbar-thumb {
        background: #555866;
        border-radius: 10px;
    }

    section[data-testid="stSidebar"]::-webkit-scrollbar-thumb:hover {
        background: #70727e;
    }


    /* =====================================================
       CHAT HISTORY BUTTON TEXT
       ===================================================== */

    section[data-testid="stSidebar"] button p {
        font-size: 14px;
    }
    /* =====================================================
   MOBILE RESPONSIVE DESIGN
   ===================================================== */

@media (max-width: 768px) {

    /* Main page */
    .main {
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }

    /* Chat title */
    .chat-title {
        font-size: 28px;
        margin-bottom: 18px;
    }

    /* Chat messages */
    div[data-testid="stChatMessage"] {
        padding-top: 6px;
        padding-bottom: 6px;
    }

    div[data-testid="stChatMessage"] p {
        font-size: 15px;
        line-height: 1.5;
    }

    /* Chat input */
    div[data-testid="stChatInput"] {
        border-radius: 12px;
    }

    div[data-testid="stChatInput"] textarea {
        font-size: 15px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] .block-container {
        padding-left: 0.6rem;
        padding-right: 0.6rem;
    }

    /* Sidebar buttons */
    section[data-testid="stSidebar"] button {
        min-height: 40px;
        font-size: 13px;
    }

    /* Search box */
    section[data-testid="stSidebar"] input {
        font-size: 14px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD API KEY
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:

    st.error("❌ Gemini API key not found.")

    st.stop()


client = genai.Client(
    api_key=api_key
)


# =========================================================
# GEMINI MODEL
# =========================================================

MODEL_NAME = "gemini-3.5-flash-lite"


# =========================================================
# CHAT STORAGE
# =========================================================

CHAT_FILE = "chats.json"


def load_chats():

    if os.path.exists(CHAT_FILE):

        try:

            with open(
                CHAT_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                chats = json.load(file)

                if (
                    isinstance(chats, list)
                    and chats
                ):

                    return chats

        except Exception:

            pass


    return [
        {
            "title": "New Chat",
            "messages": []
        }
    ]


def save_chats(chats):

    try:

        with open(
            CHAT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                chats,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as e:

        st.error(
            f"❌ Could not save chats: {e}"
        )


# =========================================================
# SESSION STATE
# =========================================================

if "chats" not in st.session_state:

    st.session_state.chats = load_chats()


if "current_chat" not in st.session_state:

    st.session_state.current_chat = 0


# =========================================================
# SAFETY CHECK
# =========================================================

if not st.session_state.chats:

    st.session_state.chats = [
        {
            "title": "New Chat",
            "messages": []
        }
    ]

    st.session_state.current_chat = 0

    save_chats(
        st.session_state.chats
    )


# Make sure current chat index is valid

if (
    st.session_state.current_chat < 0
    or
    st.session_state.current_chat >= len(
        st.session_state.chats
    )
):

    st.session_state.current_chat = 0


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("💬 Chat History")


    # =====================================================
    # NEW CHAT
    # =====================================================

    if st.button(
        "🆕 New Chat",
        use_container_width=True
    ):

        new_chat = {
            "title": "New Chat",
            "messages": []
        }

        st.session_state.chats.append(
            new_chat
        )

        st.session_state.current_chat = (
            len(st.session_state.chats) - 1
        )

        save_chats(
            st.session_state.chats
        )

        st.rerun()


    st.divider()


    # =====================================================
    # SEARCH CHATS
    # =====================================================

    search_text = st.text_input(
        "🔍 Search chats",
        placeholder="Search chat history..."
    )


    # =====================================================
    # SCROLLABLE CHAT HISTORY
    #
    # IMPORTANT:
    # Smaller height prevents the entire sidebar
    # from becoming scrollable.
    # =====================================================

    history_container = st.container(
        height=145,
        border=False
    )


    with history_container:

        visible_chats = 0


        for i, chat_item in enumerate(
            st.session_state.chats
        ):

            title = chat_item.get(
                "title",
                "New Chat"
            )


            if not title:

                title = "New Chat"


            # -------------------------------------------------
            # SEARCH FILTER
            # -------------------------------------------------

            if (
                search_text
                and
                search_text.lower()
                not in title.lower()
            ):

                continue


            visible_chats += 1


            # -------------------------------------------------
            # CHAT + DELETE COLUMNS
            # -------------------------------------------------

            col1, col2 = st.columns(
                [5, 1],
                gap="small"
            )


            # =================================================
            # OPEN CHAT
            # =================================================

            with col1:

                if (
                    i
                    ==
                    st.session_state.current_chat
                ):

                    button_text = (
                        f"🟢 {title}"
                    )

                else:

                    button_text = (
                        f"💬 {title}"
                    )


                if st.button(
                    button_text,
                    key=f"open_chat_{i}",
                    use_container_width=True
                ):

                    st.session_state.current_chat = i

                    st.rerun()


            # =================================================
            # DELETE CHAT
            # =================================================

            with col2:

                if st.button(
                    "🗑️",
                    key=f"delete_chat_{i}",
                    help="Delete this chat"
                ):

                    # -----------------------------------------
                    # Don't delete the only chat
                    # -----------------------------------------

                    if (
                        len(
                            st.session_state.chats
                        )
                        ==
                        1
                    ):

                        st.warning(
                            "You must keep at least one chat."
                        )


                    else:

                        st.session_state.chats.pop(i)


                        # -------------------------------------
                        # Fix current chat index
                        # -------------------------------------

                        if (
                            st.session_state.current_chat
                            >
                            i
                        ):

                            st.session_state.current_chat -= 1


                        elif (
                            st.session_state.current_chat
                            >=
                            len(
                                st.session_state.chats
                            )
                        ):

                            st.session_state.current_chat = (
                                len(
                                    st.session_state.chats
                                )
                                -
                                1
                            )


                        save_chats(
                            st.session_state.chats
                        )

                        st.rerun()


        # =====================================================
        # NO SEARCH RESULTS
        # =====================================================

        if visible_chats == 0:

            st.caption(
                "No chats found."
            )


    # =====================================================
    # CHAT SETTINGS
    # =====================================================

    st.divider()

    st.subheader(
        "⚙️ Chat Settings"
    )


    current_sidebar_chat = (
        st.session_state.chats[
            st.session_state.current_chat
        ]
    )


    # =====================================================
    # RENAME CHAT
    # =====================================================

    rename_value = st.text_input(
        "Rename current chat",
        value=current_sidebar_chat.get(
            "title",
            "New Chat"
        ),
        key=f"rename_input_{st.session_state.current_chat}"

    )


    if st.button(
        "✏️ Save Chat Name",
        use_container_width=True
    ):

        rename_value = rename_value.strip()


        if rename_value:

            current_sidebar_chat["title"] = (
                rename_value[:50]
            )

            save_chats(
                st.session_state.chats
            )

            st.success(
                "✅ Chat renamed."
            )

            st.rerun()


        else:

            st.warning(
                "Chat name cannot be empty."
            )


    # =====================================================
    # CLEAR CURRENT CHAT
    # =====================================================

    if st.button(
        "🧹 Clear Current Chat",
        use_container_width=True
    ):

        current_sidebar_chat["messages"] = []

        current_sidebar_chat["title"] = (
            "New Chat"
        )

        save_chats(
            st.session_state.chats
        )

        st.rerun()


# =========================================================
# CURRENT CHAT
# =========================================================

current_chat = st.session_state.chats[
    st.session_state.current_chat
]


messages = current_chat.get(
    "messages",
    []
)


# =========================================================
# MAIN TITLE
# =========================================================

st.markdown(
    '<div class="chat-title">'
    '🤖 Chintu\'s AI Chatbot'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in messages:

    role = message.get(
        "role",
        "assistant"
    )


    content = message.get(
        "content",
        ""
    )


    if not content:

        continue


    # Only valid Streamlit roles

    if role not in [
        "user",
        "assistant"
    ]:

        role = "assistant"


    with st.chat_message(role):

        st.markdown(content)


# =========================================================
# CHAT INPUT
# =========================================================

user_message = st.chat_input(
    "Type your message..."
)


# =========================================================
# PROCESS USER MESSAGE
# =========================================================

if user_message:

    user_message = user_message.strip()


    if not user_message:

        st.stop()


    # =====================================================
    # SAVE USER MESSAGE
    # =====================================================

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # =====================================================
    # AUTOMATIC CHAT TITLE
    # =====================================================

    if (
        current_chat.get("title")
        ==
        "New Chat"
    ):

        title = user_message[:40]


        if len(user_message) > 40:

            title += "..."


        current_chat["title"] = title


    # =====================================================
    # SAVE USER MESSAGE
    # =====================================================

    save_chats(
        st.session_state.chats
    )


    # =====================================================
    # DISPLAY USER MESSAGE
    # =====================================================

    with st.chat_message("user"):

        st.markdown(
            user_message
        )


    # =====================================================
    # BUILD GEMINI HISTORY
    # =====================================================

    history = []


    # Current message is excluded.
    # It will be sent separately.

    previous_messages = messages[:-1]


    for message in previous_messages:

        content = message.get(
            "content",
            ""
        )


        if not content:

            continue


        role = message.get(
            "role",
            "assistant"
        )


        if role == "user":

            gemini_role = "user"

        else:

            gemini_role = "model"


        history.append(
            types.Content(
                role=gemini_role,
                parts=[
                    types.Part.from_text(
                        text=content
                    )
                ]
            )
        )


    # =====================================================
    # CLEAN GEMINI HISTORY
    # =====================================================

    # History must start with USER

    while (
        history
        and
        history[0].role != "user"
    ):

        history.pop(0)


    # History must not end with MODEL
    # because the current user message comes next.

    while (
        history
        and
        history[-1].role == "model"
    ):

        history.pop()


    # =====================================================
    # SEND MESSAGE TO GEMINI
    # =====================================================

    try:

        with st.chat_message("assistant"):

            with st.spinner(
                "🤖 Chintu AI is thinking..."
            ):

                chat = client.chats.create(
                    model=MODEL_NAME,
                    history=history
                )


                bot_response = ""

                response_stream = chat.send_message_stream(
                    message=user_message
                )

                response_placeholder = st.empty()

                for chunk in response_stream:

                   if chunk.text:

                      bot_response += chunk.text

                      response_placeholder.markdown(
                         bot_response
                        )


                if not bot_response:

                    bot_response = (
                        "Sorry, I couldn't "
                        "generate a response."
                    )


            st.markdown(
                bot_response
            )


        # =================================================
        # SAVE AI RESPONSE
        # =================================================

        messages.append(
            {
                "role": "assistant",
                "content": bot_response
            }
        )


        save_chats(
            st.session_state.chats
        )


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        error_message = str(e)


        # =================================================
        # QUOTA ERROR
        # =================================================

        if (
            "429" in error_message
            or
            "RESOURCE_EXHAUSTED"
            in error_message
        ):

            st.error(
                "⚠️ Gemini API quota has been reached.\n\n"
                "Please wait for the quota to reset "
                "before sending another message."
            )


        # =================================================
        # SERVER ERROR
        # =================================================

        elif (
            "503" in error_message
            or
            "UNAVAILABLE"
            in error_message
        ):

            st.error(
                "⚠️ Gemini is temporarily unavailable.\n\n"
                "Please try again in a few moments."
            )


        # =================================================
        # INVALID ARGUMENT
        # =================================================

        elif (
            "400" in error_message
            or
            "INVALID_ARGUMENT"
            in error_message
        ):

            st.error(
                "⚠️ Gemini rejected the conversation.\n\n"
                "Please start a new chat and try again."
            )


        # =================================================
        # OTHER ERRORS
        # =================================================

        else:

            st.error(
                f"❌ Error: {error_message}"
            )