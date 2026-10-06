import streamlit as st
import pandas as pd
import random
import time
import textwrap
import requests
from datetime import datetime

# GPS component
from streamlit_geolocation import streamlit_geolocation


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AcciDetect",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# HTML HELPER
# ============================================================

def html(content):
    st.html(textwrap.dedent(content).strip())


# ============================================================
# BACKGROUND COLOR
# ============================================================

if "background_color" not in st.session_state:
    st.session_state.background_color = "#071321"


# ============================================================
# GET NORMAL LOCATION NAME
# ============================================================

@st.cache_data(ttl=300)
def get_location_name(latitude, longitude):
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={
                "lat": latitude,
                "lon": longitude,
                "format": "json",
                "zoom": 18
            },
            headers={"User-Agent": "AcciDetect/1.0"},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("display_name", "Location not available")

    except Exception:
        pass

    return "Location not available"


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    :root {
        --app-bg: #071321;
    }

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: var(--app-bg);
        color: white;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 18px;
        padding-bottom: 50px;
    }

    #MainMenu,
    header,
    footer {
        visibility: hidden;
    }

    /* Completely hide sidebar */
    section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* ========================================================
       TOP NAVIGATION
       ======================================================== */

    @media (max-width: 1100px) {

        .top-brand-title {
            font-size: 23px;
        }

        .top-brand-sub {
            font-size: 9px;
        }

    }

    @media (max-width: 850px) {

        .top-brand-sub {
            display: none;
        }

        div[data-testid="stHorizontalBlock"] .nav-btn button {
            font-size: 10px !important;
            padding: 6px 5px !important;
        }

    }


    .top-navigation {
        background:
            linear-gradient(
                145deg,
                #10243a,
                #091727
            );

        border:
            1px solid
            rgba(0, 212, 255, 0.16);

        border-radius: 20px;

        padding: 14px 16px;

        margin-bottom: 24px;

        box-shadow:
            0 12px 35px
            rgba(0,0,0,0.22);
    }

    .top-brand {
        padding: 5px 0 0 4px;
    }

    .top-brand-title {
        font-size: 28px;
        font-weight: 800;
        line-height: 1.0;
        color: white;
    }

    .top-brand-title span {
        color: #00d9ff;
    }

    .top-brand-sub {
        color: #8ca5bd;
        font-size: 10px;
        margin-top: 7px;
        white-space: nowrap;
    }

    .top-user {
        text-align: right;
        color: #8ca5bd;
        font-size: 11px;
        margin-top: 6px;
    }

    .top-user strong {
        color: white;
    }

    .online {
        color: #00e49a;
        font-weight: 700;
    }

    /* Top nav buttons */
    div[data-testid="stHorizontalBlock"] .nav-btn button {
        min-height: 44px !important;
        height: 44px !important;
        padding: 8px 9px !important;
        border-radius: 11px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: rgba(255,255,255,0.035) !important;
        color: #9bb0c3 !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        white-space: nowrap !important;
    }

    div[data-testid="stHorizontalBlock"] .nav-btn button:hover {
        background: rgba(0,212,255,0.12) !important;
        border-color: rgba(0,212,255,0.30) !important;
        color: #00d9ff !important;
    }

    .nav-active button {
        background:
            linear-gradient(
                135deg,
                rgba(0,212,255,0.18),
                rgba(0,120,180,0.14)
            ) !important;

        border-color:
            rgba(0,212,255,0.42) !important;

        color: #00d9ff !important;

        box-shadow:
            0 0 16px
            rgba(0,212,255,0.08);
    }

    .top-divider {
        height: 1px;
        background: rgba(255,255,255,0.07);
        margin: 10px 0 14px 0;
    }

    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        background:
            linear-gradient(
                135deg,
                rgba(0,212,255,0.13),
                rgba(255,50,80,0.08)
            ),
            #0c1b2e;

        border:
            1px solid
            rgba(0,212,255,0.18);

        border-radius: 24px;
        padding: 35px;
        margin-bottom: 25px;
    }

    .badge {
        display: inline-block;
        background: rgba(0,212,255,0.10);
        border: 1px solid rgba(0,212,255,0.25);
        color: #00d9ff;
        padding: 7px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .hero h1 {
        font-size: 44px;
        font-weight: 800;
        margin: 0;
    }

    .hero h1 span {
        color: #00d9ff;
    }

    .hero p {
        color: #91a9bf;
        font-size: 16px;
        line-height: 1.7;
        max-width: 800px;
    }

    /* ========================================================
       METRICS
       ======================================================== */

    .metric-card {
        background:
            linear-gradient(
                145deg,
                #10263d,
                #0a192b
            );

        border:
            1px solid
            rgba(255,255,255,0.07);

        border-radius: 18px;
        padding: 20px;
        min-height: 135px;
    }

    .metric-icon {
        font-size: 28px;
    }

    .metric-label {
        color: #8ba3b9;
        font-size: 13px;
        margin-top: 8px;
    }

    .metric-number {
        color: white;
        font-size: 27px;
        font-weight: 800;
        margin-top: 5px;
    }

    /* ========================================================
       CARDS
       ======================================================== */

    .card {
        background: #0d1e32;
        border:
            1px solid
            rgba(255,255,255,0.07);

        border-radius: 18px;
        padding: 23px;
        height: 100%;
    }

    .card-title {
        color: white;
        font-size: 18px;
        font-weight: 700;
    }

    .card-text {
        color: #8ca5bc;
        font-size: 13px;
        line-height: 1.6;
    }

    /* ========================================================
       CAMERA
       ======================================================== */

    .camera {
        height: 350px;
        border-radius: 20px;
        position: relative;
        overflow: hidden;

        background:
            linear-gradient(
                rgba(0,0,0,0.15),
                rgba(0,0,0,0.5)
            ),
            linear-gradient(
                180deg,
                #19364d 0%,
                #07121e 100%
            );

        border:
            1px solid
            rgba(0,212,255,0.20);
    }

    .camera-grid {
        position: absolute;
        inset: 0;

        background-image:
            linear-gradient(
                rgba(255,255,255,0.035) 1px,
                transparent 1px
            ),
            linear-gradient(
                90deg,
                rgba(255,255,255,0.035) 1px,
                transparent 1px
            );

        background-size: 40px 40px;
    }

    .cctv-label {
        position: absolute;
        top: 15px;
        left: 15px;
        z-index: 5;

        background: rgba(0,0,0,0.60);
        padding: 8px 13px;
        border-radius: 8px;

        color: white;
        font-size: 12px;
    }

    .live-dot {
        color: #ff3d5b;
        animation: blink 1s infinite;
    }

    @keyframes blink {
        50% {
            opacity: 0.2;
        }
    }

    .road {
        position: absolute;
        width: 65%;
        height: 100%;
        left: 17.5%;
        bottom: -5%;

        background: #151d25;

        transform:
            perspective(350px)
            rotateX(8deg);

        border-left: 3px solid #29343d;
        border-right: 3px solid #29343d;
    }

    .lane {
        position: absolute;
        width: 7px;
        height: 50px;
        background: #ddd;
        left: 50%;

        transform:
            translateX(-50%);
    }

    .l1 { bottom: 20px; }
    .l2 { bottom: 100px; }
    .l3 { bottom: 180px; }
    .l4 { bottom: 260px; }

    .car {
        position: absolute;
        width: 70px;
        height: 42px;
        background: #e73551;
        border-radius: 10px 10px 5px 5px;
        left: 30%;
        bottom: 65px;
    }

    .car2 {
        position: absolute;
        width: 70px;
        height: 42px;
        background: #1e8ddd;
        border-radius: 10px;
        left: 58%;
        bottom: 145px;
    }

    .car3 {
        position: absolute;
        width: 60px;
        height: 38px;
        background: #e5a52e;
        border-radius: 9px;
        left: 43%;
        bottom: 230px;
    }

    /* ========================================================
       STATUS
       ======================================================== */

    .status-danger {
        background:
            rgba(255,45,70,0.12);

        border:
            1px solid
            rgba(255,45,70,0.30);

        color: #ff5068;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        font-weight: 800;
        margin: 20px 0;
    }

    .status-safe {
        background:
            rgba(0,220,140,0.10);

        border:
            1px solid
            rgba(0,220,140,0.25);

        color: #00e49a;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        font-weight: 800;
        margin: 20px 0;
    }

    /* ========================================================
       ALERT
       ======================================================== */

    .alert-card {
        background:
            linear-gradient(
                135deg,
                rgba(255,45,70,0.15),
                rgba(100,20,40,0.15)
            );

        border:
            1px solid
            rgba(255,50,75,0.30);

        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
    }

    .alert-card h2 {
        color: #ff526a;
    }

    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        margin-top: 50px;
        padding: 30px;
        text-align: center;
        color: #6e8498;

        border-top:
            1px solid
            rgba(255,255,255,0.07);
    }

    .footer strong {
        color: #00d9ff;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "total_detections" not in st.session_state:
    st.session_state.total_detections = 0

if "accidents_detected" not in st.session_state:
    st.session_state.accidents_detected = 0

if "alerts_sent" not in st.session_state:
    st.session_state.alerts_sent = 0

if "gps_lat" not in st.session_state:
    st.session_state.gps_lat = 17.4065

if "gps_lon" not in st.session_state:
    st.session_state.gps_lon = 78.4772

if "gps_accuracy" not in st.session_state:
    st.session_state.gps_accuracy = 0

if "gps_location_name" not in st.session_state:
    st.session_state.gps_location_name = "Location not available"

if "page" not in st.session_state:
    st.session_state.page = "🏠 Dashboard"


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    html(
        """
        <div class="hero"
             style="max-width:500px;margin:70px auto 25px;text-align:center;">

            <div style="
                font-size:40px;
                font-weight:800;
            ">
                Acci<span>Detect</span>
            </div>

            <p style="margin:12px auto 0;">
                AI Road Accident Detection System
            </p>

        </div>
        """
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown("### 🔐 Secure Login")

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        if st.button(
            "🔓 LOGIN",
            use_container_width=True
        ):

            if (
                username == "admin"
                and password == "admin123"
            ):

                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

        st.info(
            "Demo login:\n\n"
            "Username: `admin`\n\n"
            "Password: `admin123`"
        )

    st.stop()


# ============================================================
# GET GPS LOCATION
# ============================================================

location_data = streamlit_geolocation()

if location_data:

    latitude = location_data.get("latitude")
    longitude = location_data.get("longitude")
    accuracy = location_data.get("accuracy")

    if (
        latitude is not None
        and longitude is not None
    ):

        st.session_state.gps_lat = float(latitude)
        st.session_state.gps_lon = float(longitude)

        if accuracy is not None:
            st.session_state.gps_accuracy = float(accuracy)

        st.session_state.gps_location_name = (
            get_location_name(
                st.session_state.gps_lat,
                st.session_state.gps_lon
            )
        )


# ============================================================
# TOP NAVIGATION
# ============================================================

NAV_ITEMS = [
    ("🏠", "Dashboard"),
    ("📹", "Live Detection"),
    ("📍", "Accident Location"),
    ("🚨", "Emergency Center"),
    ("🗺️", "Accident Hotspots"),
    ("📋", "Accident History"),
    ("⚙️", "System Information"),
]

st.markdown(
    '<div class="top-navigation">',
    unsafe_allow_html=True
)

# Brand row
brand_col, user_col = st.columns([2, 8])

with brand_col:

    st.markdown(
        """
        <div class="top-brand">
            <div class="top-brand-title">
                Acci<span>Detect</span>
            </div>
            <div class="top-brand-sub">
                AI Road Accident Detection System
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with user_col:

    st.markdown(
        f"""
        <div class="top-user">
            👤 Logged in as
            <strong>{st.session_state.username}</strong>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <span class="online">● AI Engine Online</span>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <span class="online">● GPS Ready</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    '<div class="top-divider"></div>',
    unsafe_allow_html=True
)

# Actual top navigation buttons
nav_columns = st.columns(
    [1.0, 1.15, 1.25, 1.25, 1.25, 1.15, 1.35]
)

for index, ((icon, label), nav_col) in enumerate(
    zip(NAV_ITEMS, nav_columns)
):

    with nav_col:

        active = (
            st.session_state.page
            == f"{icon} {label}"
        )

        if active:

            st.markdown(
                '<div class="nav-btn nav-active">',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                '<div class="nav-btn">',
                unsafe_allow_html=True
            )

        if st.button(
            f"{icon} {label}",
            key=f"top_nav_{index}",
            use_container_width=True
        ):

            st.session_state.page = (
                f"{icon} {label}"
            )

            st.rerun()

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# TOP RIGHT CONTROLS
# ============================================================

control_left, control_middle, control_right = st.columns(
    [6.4, 1.1, 2.5]
)

with control_middle:

    st.session_state.background_color = st.color_picker(
        "Background",
        st.session_state.background_color,
        key="top_background_picker",
        label_visibility="collapsed"
    )

with control_right:

    st.markdown(
        """
        <style>
        div[data-testid="stButton"] button {
            min-height: 40px !important;
            min-width: 130px !important;
            width: 100% !important;
            border-radius: 10px !important;
            overflow: visible !important;
        }

        div[data-testid="stButton"] button p {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            color: white !important;
            font-size: 12px !important;
            font-weight: 800 !important;
            white-space: nowrap !important;
            overflow: visible !important;
            text-overflow: clip !important;
            text-align: center !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🚪  LOGOUT",
        key="top_logout",
        use_container_width=True,
        help="Logout"
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()


# Apply selected background
st.markdown(
    f"""
    <style>

    :root {{
        --app-bg: {st.session_state.background_color};
    }}

    .stApp {{
        background: {st.session_state.background_color} !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background: {st.session_state.background_color} !important;
    }}

    [data-testid="stHeader"] {{
        background: {st.session_state.background_color} !important;
    }}

    [data-testid="stMainBlockContainer"] {{
        background: transparent !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GENERATE ACCIDENT
# ============================================================

def generate_accident():

    detected = random.choice(
        [True, True, True, False]
    )

    confidence = random.randint(
        88,
        99
    )

    plates = [
        "TS09AB1234",
        "TS10CD5678",
        "TS08EF4321",
        "AP28GH9087",
        "TS07JK3322"
    ]

    if detected:

        severity = random.choice(
            [
                "Minor",
                "Moderate",
                "Severe",
                "Critical"
            ]
        )

        vehicles = random.randint(
            2,
            5
        )

        injured = random.randint(
            0,
            4
        )

        fire = random.choice(
            [True, False, False]
        )

        smoke = random.choice(
            [True, False, False]
        )

        license_plate = random.choice(
            plates
        )

    else:

        severity = "N/A"
        vehicles = 0
        injured = 0
        fire = False
        smoke = False
        license_plate = "N/A"

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    accident_id = (
        "ACC-"
        + datetime.now().strftime(
            "%Y%m%d%H%M%S"
        )
    )

    return {

        "id": accident_id,

        "timestamp": timestamp,

        "detected": detected,

        "confidence": confidence,

        "severity": severity,

        "vehicles": vehicles,

        "injured": injured,

        "fire": fire,

        "smoke": smoke,

        "license_plate": license_plate,

        "latitude":
            st.session_state.gps_lat,

        "longitude":
            st.session_state.gps_lon,

        "gps_accuracy":
            st.session_state.gps_accuracy,

        "status":
            (
                "ACCIDENT DETECTED"
                if detected
                else "NO ACCIDENT"
            )
    }


def save_detection_result(result):

    st.session_state.total_detections += 1

    st.session_state.last_result = result

    if result["detected"]:

        st.session_state.accidents_detected += 1

        st.session_state.history.append(
            result
        )


def camera_view(label):

    html(
        f"""
        <div class="camera">

            <div class="camera-grid"></div>

            <div class="cctv-label">

                <span class="live-dot">
                    ●
                </span>

                {label}

            </div>

            <div class="road">

                <div class="lane l1"></div>
                <div class="lane l2"></div>
                <div class="lane l3"></div>
                <div class="lane l4"></div>

                <div class="car"></div>
                <div class="car2"></div>
                <div class="car3"></div>

            </div>

        </div>
        """
    )


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "🏠 Dashboard":

    html(
        """
        <div class="hero">

            <div class="badge">
                ● AI SAFETY MONITORING SYSTEM
            </div>

            <h1>
                Welcome to
                <span>AcciDetect</span>
            </h1>

            <p>
                Intelligent road accident detection,
                GPS tracking and emergency response.
            </p>

        </div>
        """
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        html(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    📡
                </div>

                <div class="metric-label">
                    Total Detections
                </div>

                <div class="metric-number">
                    {st.session_state.total_detections}
                </div>

            </div>
            """
        )

    with c2:

        html(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    🚨
                </div>

                <div class="metric-label">
                    Accidents Detected
                </div>

                <div class="metric-number">
                    {st.session_state.accidents_detected}
                </div>

            </div>
            """
        )

    with c3:

        html(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    🚑
                </div>

                <div class="metric-label">
                    Emergency Alerts
                </div>

                <div class="metric-number">
                    {st.session_state.alerts_sent}
                </div>

            </div>
            """
        )

    html(
        """
        <div style="
            margin-top:30px;
            margin-bottom:18px;
            font-size:27px;
            font-weight:800;
        ">
            Live Monitoring
        </div>
        """
    )

    left, right = st.columns(
        [1.3, 1]
    )

    with left:
        camera_view("CCTV CAMERA 01 — LIVE")

    with right:

        html(
            """
            <div class="card">

                <div class="card-title">
                    🤖 AI Detection Engine
                </div>

                <br>

                <div class="card-text">
                    The accident location will be captured
                    using the current GPS position when
                    detection is triggered.
                </div>

            </div>
            """
        )

        if st.button(
            "🚨 START AI DETECTION",
            use_container_width=True
        ):

            with st.spinner(
                "AI analyzing CCTV footage..."
            ):

                time.sleep(1.5)

            result = generate_accident()

            save_detection_result(result)

            st.rerun()

    if st.session_state.last_result:

        result = st.session_state.last_result

        html(
            """
            <div style="
                margin-top:30px;
                margin-bottom:15px;
                font-size:27px;
                font-weight:800;
            ">
                Latest AI Analysis
            </div>
            """
        )

        if result["detected"]:

            html(
                f"""
                <div class="status-danger">

                    🚨 ACCIDENT DETECTED

                    <br><br>

                    AI Confidence:
                    {result['confidence']}%

                    <br>

                    📍 Accident Location:
                    {
                        get_location_name(
                            result['latitude'],
                            result['longitude']
                        )
                    }

                </div>
                """
            )

        else:

            html(
                f"""
                <div class="status-safe">

                    🟢 NO ACCIDENT DETECTED

                    <br><br>

                    AI Confidence:
                    {result['confidence']}%

                </div>
                """
            )

        a, b, c, d = st.columns(4)

        with a:
            st.metric(
                "Severity",
                result["severity"]
            )

        with b:
            st.metric(
                "Vehicles",
                result["vehicles"]
            )

        with c:
            st.metric(
                "Injured",
                result["injured"]
            )

        with d:
            st.metric(
                "AI Confidence",
                f"{result['confidence']}%"
            )

        if result["detected"]:

            st.markdown(
                "### 📍 Accident Spot"
            )

            accident_map = pd.DataFrame(
                {
                    "latitude": [
                        result["latitude"]
                    ],
                    "longitude": [
                        result["longitude"]
                    ]
                }
            )

            st.map(
                accident_map,
                latitude="latitude",
                longitude="longitude",
                zoom=15
            )

            st.info(
                "🚨 Accident detected at "
                "Location: "
                + get_location_name(
                    result["latitude"],
                    result["longitude"]
                )
            )


# ============================================================
# LIVE DETECTION
# ============================================================

elif st.session_state.page == "📹 Live Detection":

    html(
        """
        <div class="hero">

            <div class="badge">
                📹 LIVE CCTV ANALYSIS
            </div>

            <h1>
                Real-Time
                <span>Detection</span>
            </h1>

            <p>
                Monitor road scenes and run AI accident analysis.
            </p>

        </div>
        """
    )

    left, right = st.columns(
        [1.3, 1]
    )

    with left:
        camera_view("CAMERA 01 — LIVE FEED")

    with right:

        html(
            """
            <div class="card">

                <div class="card-title">
                    🎯 AI Control Center
                </div>

                <br>

                <div class="card-text">
                    Run accident detection. The current
                    GPS position will be attached to
                    the detected accident.
                </div>

            </div>
            """
        )

        if st.button(
            "▶ RUN ACCIDENT DETECTION",
            use_container_width=True
        ):

            progress = st.progress(0)

            for i in range(100):

                time.sleep(0.01)

                progress.progress(
                    i + 1
                )

            result = generate_accident()

            save_detection_result(result)

            st.success(
                "Detection completed."
            )

            if result["detected"]:

                st.error(
                    "🚨 ACCIDENT DETECTED"
                )

                st.write(
                    "📍 Accident Location:",
                    get_location_name(
                        result["latitude"],
                        result["longitude"]
                    )
                )

                accident_map = pd.DataFrame(
                    {
                        "latitude": [
                            result["latitude"]
                        ],
                        "longitude": [
                            result["longitude"]
                        ]
                    }
                )

                st.map(
                    accident_map,
                    zoom=15
                )

            else:

                st.success(
                    "🟢 NO ACCIDENT DETECTED"
                )


# ============================================================
# ACCIDENT LOCATION
# ============================================================

elif st.session_state.page == "📍 Accident Location":

    html(
        """
        <div class="hero">

            <div class="badge">
                📍 GPS LOCATION TRACKING
            </div>

            <h1>
                Accident
                <span>Location</span>
            </h1>

            <p>
                The map displays the location where the
                latest accident was detected.
            </p>

        </div>
        """
    )

    result = st.session_state.last_result

    if result and result["detected"]:

        st.markdown(
            "### 🚨 Latest Accident Spot"
        )

        col1, col2 = st.columns(
            [2, 1]
        )

        with col1:

            st.markdown(
                "### 📍 "
                + get_location_name(
                    result["latitude"],
                    result["longitude"]
                )
            )

            st.caption(
                "Accident location"
            )

        with col2:

            if result["gps_accuracy"]:

                st.metric(
                    "Accuracy",
                    f"{result['gps_accuracy']:.1f} m"
                )

            else:

                st.metric(
                    "Accuracy",
                    "Unknown"
                )

        accident_map = pd.DataFrame(
            {
                "latitude": [
                    result["latitude"]
                ],
                "longitude": [
                    result["longitude"]
                ]
            }
        )

        st.map(
            accident_map,
            latitude="latitude",
            longitude="longitude",
            zoom=16
        )

        st.success(
            "📍 Accident spot: "
            + get_location_name(
                result["latitude"],
                result["longitude"]
            )
        )

    else:

        st.info(
            "No accident has been detected yet."
        )

        st.write(
            "Once an accident is detected, "
            "its exact GPS position will appear here."
        )


# ============================================================
# EMERGENCY CENTER
# ============================================================

elif st.session_state.page == "🚨 Emergency Center":

    html(
        """
        <div class="hero">

            <div class="badge">
                🚨 EMERGENCY RESPONSE
            </div>

            <h1>
                Emergency
                <span>Center</span>
            </h1>

            <p>
                Send emergency notifications using
                the detected accident location.
            </p>

        </div>
        """
    )

    result = st.session_state.last_result

    if result and result["detected"]:

        html(
            f"""
            <div class="alert-card">

                <h2>
                    🚨 Accident Requires Response
                </h2>

                <p>
                    Accident ID:
                    <strong>{result['id']}</strong>
                </p>

                <p>
                    Severity:
                    <strong>{result['severity']}</strong>
                </p>

                <p>
                    📍 Accident Location:
                    <strong>
                        {
                            get_location_name(
                                result['latitude'],
                                result['longitude']
                            )
                        }
                    </strong>
                </p>

            </div>
            """
        )

        st.markdown(
            "### 📱 Emergency Contact"
        )

        phone = st.text_input(
            "Emergency phone number",
            placeholder="+91 XXXXX XXXXX"
        )

        email = st.text_input(
            "Emergency email",
            placeholder="emergency@example.com"
        )

        if st.button(
            "🚑 SEND EMERGENCY ALERT",
            use_container_width=True
        ):

            if phone or email:

                st.session_state.alerts_sent += 1

                st.success(
                    "Emergency alert sent."
                )

                st.info(
                    "📍 Location included: "
                    + get_location_name(
                        result["latitude"],
                        result["longitude"]
                    )
                )

                if phone:

                    st.info(
                        f"📱 SMS simulated for {phone}"
                    )

                if email:

                    st.info(
                        f"📧 Email simulated for {email}"
                    )

            else:

                st.warning(
                    "Enter a phone number or email."
                )

    else:

        st.success(
            "🟢 No active accident."
        )


# ============================================================
# ACCIDENT HOTSPOTS
# ============================================================

elif st.session_state.page == "🗺️ Accident Hotspots":

    html(
        """
        <div class="hero">

            <div class="badge">
                🗺️ ACCIDENT HOTSPOT MAPPING
            </div>

            <h1>
                Accident
                <span>Hotspots</span>
            </h1>

            <p>
                All detected accident locations are displayed
                on the map.
            </p>

        </div>
        """
    )

    if st.session_state.history:

        points = pd.DataFrame(
            [
                {
                    "latitude": x["latitude"],
                    "longitude": x["longitude"]
                }
                for x in st.session_state.history
            ]
        )

        st.map(
            points,
            latitude="latitude",
            longitude="longitude",
            zoom=12
        )

        st.markdown(
            "### 📊 Accident Locations"
        )

        history_df = pd.DataFrame(
            st.session_state.history
        )

        history_df["Location"] = history_df.apply(
            lambda row:
                get_location_name(
                    row["latitude"],
                    row["longitude"]
                ),
            axis=1
        )

        st.dataframe(
            history_df[
                [
                    "id",
                    "timestamp",
                    "severity",
                    "Location"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No accident hotspots available yet."
        )


# ============================================================
# ACCIDENT HISTORY
# ============================================================

elif st.session_state.page == "📋 Accident History":

    html(
        """
        <div class="hero">

            <div class="badge">
                📋 INCIDENT DATABASE
            </div>

            <h1>
                Accident
                <span>History</span>
            </h1>

            <p>
                Review detected accidents and their exact locations.
            </p>

        </div>
        """
    )

    if not st.session_state.history:

        st.info(
            "No accidents detected yet."
        )

    else:

        df = pd.DataFrame(
            st.session_state.history
        )

        df["Location"] = df.apply(
            lambda row:
                get_location_name(
                    row["latitude"],
                    row["longitude"]
                ),
            axis=1
        )

        st.dataframe(
            df[
                [
                    "id",
                    "timestamp",
                    "severity",
                    "confidence",
                    "vehicles",
                    "injured",
                    "license_plate",
                    "Location"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown(
            "### 📄 Accident Reports"
        )

        for result in reversed(
            st.session_state.history
        ):

            report = f"""
ACCIDETECT ACCIDENT REPORT

Accident ID: {result['id']}
Date: {result['timestamp']}

Status: {result['status']}
Confidence: {result['confidence']}%
Severity: {result['severity']}

Vehicles: {result['vehicles']}
Injured Persons: {result['injured']}

License Plate: {result['license_plate']}

ACCIDENT LOCATION
Location: {get_location_name(result['latitude'], result['longitude'])}
GPS Accuracy: {result['gps_accuracy']} meters

Fire: {'YES' if result['fire'] else 'NO'}
Smoke: {'YES' if result['smoke'] else 'NO'}

Generated by AcciDetect.
"""

            st.download_button(
                f"📄 Download {result['id']}",
                data=report,
                file_name=f"{result['id']}.txt",
                mime="text/plain",
                key=f"download_{result['id']}"
            )


# ============================================================
# SYSTEM INFORMATION
# ============================================================

elif st.session_state.page == "⚙️ System Information":

    html(
        """
        <div class="hero">

            <div class="badge">
                ⚙️ SYSTEM INFORMATION
            </div>

            <h1>
                AcciDetect
                <span>System</span>
            </h1>

            <p>
                AI-based road accident monitoring platform.
            </p>

        </div>
        """
    )

    st.markdown(
        "### 🔐 Login System"
    )

    st.write(
        "Username: admin"
    )

    st.write(
        "Demo password: admin123"
    )

    st.markdown(
        "### 📍 GPS System"
    )

    st.write(
        "The application requests the browser's "
        "current location."
    )

    st.write(
        "When an accident is detected, the current "
        "latitude and longitude are stored with the "
        "accident record."
    )

    st.markdown(
        "### 🧠 Detection System"
    )

    st.warning(
        "The current accident detection is simulated. "
        "A real deployment should connect a computer "
        "vision model and CCTV/video stream."
    )


# ============================================================
# FOOTER
# ============================================================

html(
    """
    <div class="footer">

        <strong>AcciDetect</strong>

        <br>

        AI Road Accident Detection &
        Emergency Response System

        <br><br>

        © 2026 AcciDetect

    </div>
    """
)
