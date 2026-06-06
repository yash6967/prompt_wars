import streamlit as st

TRANSLATIONS = {
    "English": {
        "nav_dashboard": "📊 Dashboard",
        "nav_mood": "📝 Mood Check-In",
        "nav_assessment": "📋 Assessment",
        "nav_ai_story": "📖 AI Story",
        "nav_ai_chat": "💬 AI Chat",
        "nav_calendar": "📅 Exam Calendar",
        "nav_activity": "⏳ Activity Break",
        "nav_subtle_ally": "🤝 Subtle Ally",
        "welcome": "Welcome to Saathi",
        "target": "Your Target",
        "logout": "Logout",
        "login": "Login",
        "register": "Register",
        "email": "Email Address",
        "password": "Password",
        "name": "Full Name",
        "exam_target": "Target Exam",
        "exam_date": "Exam Date",
        "daily_tip": "Daily Tip",
        # Dashboard
        "dash_title": "📊 Student Wellness Dashboard",
        "student": "Student",
        "avg_mood": "Average Mood (14d)",
        "avg_energy": "Average Energy (14d)",
        "avg_sleep": "Average Sleep (14d)",
        "avg_study": "Average Study (14d)",
        "trends_title": "📈 Wellness Trends Over Time",
        "sleep_title": "Sleep Hours per Day",
        "study_title": "Study Hours per Day",
        "screen_reader_alt": "👁️ View Text Alternative for Screen Readers & Low Bandwidth",
        "summary_table": "Daily Wellness Logs Summary Table",
        "no_logs": "Log your daily mood check-in to see wellness charts!",
        "urgent_escalation": "🚨 Urgent: Student Safety Escalation Active",
        "escalation_p1": "Recent self-reports or stress indicators suggest you are experiencing extremely high pressure or distress.",
        "flagged_reasons": "Reasons flagged:",
        "support_helplines": "You do not have to walk this path alone. Please reach out to one of the following confidential support resources immediately:",
        # Mood Check-In
        "mood_title": "📝 Daily Mood Check-In",
        "mood_desc": "Taking a moment to log how you feel helps visualize patterns and keeps you grounded.",
        "mood_q": "How is your mood today?",
        "energy_q": "What is your current energy level?",
        "sleep_q": "How many hours did you sleep last night?",
        "study_q": "How many hours did you study today?",
        "emotion_tags": "Emotion Tags",
        "select_emotions": "Select emotions matching your current state:",
        "journal_notes": "Write down any thoughts or journal notes:",
        "journal_placeholder": "What is causing stress or helping you study today?",
        "submit_entry": "Submit Entry",
        "mood_success": "Mood logged successfully! Check the Dashboard to see your trends.",
        "mood_fail": "Failed to log mood. Please try again.",
        # Assessment Page Specifics
        "assess_title": "📋 Wellness Assessment",
        "assess_desc": "This non-clinical assessment combined of validated scales helps track your levels of PHQ-9 (Depression), GAD-7 (Anxiety), and PSS-4 (Perceived stress). Your answers are confidential.",
        "assess_sec1": "Section 1: General Mood & Wellness (PHQ-9)",
        "assess_sec2": "Section 2: Anxiety & Stress Response (GAD-7)",
        "assess_sec3": "Section 3: Perceived Coping & Pressures (PSS-4)",
        "assess_caption_2weeks": "Over the last 2 weeks, how often have you been bothered by any of the following problems?",
        "assess_caption_month": "In the last month, how often have you felt...",
        "assess_submit": "Submit Assessment & Calculate Results",
        "assess_success": "Assessment submitted successfully!",
        "assess_severe_warn": "⚠️ Your results suggest severe pressure. We highly encourage talking to one of our listed advisors, or visiting the Resources and Subtle Ally sections.",
        "assess_moderate_info": "💡 You are experiencing moderate stress. Consider scheduling regular activity breaks via the Activity Break page.",
        "assess_mild_info": "✨ Great job maintaining a low stress preparation routine! Continue logging your moods to track ongoing trends.",
        "assess_result_hdr": "Assessment Result",
        "assess_pressure_lvl": "Pressure Level",
        "assess_breakdown_lbl": "Below is your wellness index breakdown:",
        "opt_not_at_all": "Not at all",
        "opt_several_days": "Several days",
        "opt_more_than_half": "More than half the days",
        "opt_nearly_every_day": "Nearly every day",
        "opt_never": "Never",
        "opt_almost_never": "Almost Never",
        "opt_sometimes": "Sometimes",
        "opt_fairly_often": "Fairly Often",
        "q1": "Little interest or pleasure in doing things?",
        "q2": "Feeling down, depressed, or hopeless?",
        "q3": "Trouble falling or staying asleep, or sleeping too much?",
        "q4": "Feeling tired or having little energy?",
        "q5": "Poor appetite or overeating?",
        "q6": "Feeling bad about yourself — or that you are a failure or have let yourself or your family down?",
        "q7": "Trouble concentrating on things, such as reading or watching television?",
        "q8": "Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual?",
        "q9": "Thoughts that you would be better off dead, or of hurting yourself in some way?",
        "q10": "Feeling nervous, anxious or on edge?",
        "q11": "Not being able to stop or control worrying?",
        "q12": "Worrying too much about different things?",
        "q13": "Trouble relaxing?",
        "q14": "Being so restless that it is hard to sit still?",
        "q15": "Becoming easily annoyed or irritable?",
        "q16": "Feeling afraid as if something awful might happen?",
        "q17": "In the last month, how often have you felt that you were unable to control the important things in your life?",
        "q18": "In the last month, how often have you felt confident about your ability to handle your personal problems?",
        "q19": "In the last month, how often have you felt that things were going your way?",
        "q20": "In the last month, how often have you felt difficulties were piling up so high that you could not overcome them?"
    },
    "Hindi (हिन्दी)": {
        "nav_dashboard": "📊 डैशबोर्ड",
        "nav_mood": "📝 मनोदशा लॉग",
        "nav_assessment": "📋 मूल्यांकन",
        "nav_ai_story": "📖 एआई कहानी",
        "nav_ai_chat": "💬 एआई चैट",
        "nav_calendar": "📅 परीक्षा कैलेंडर",
        "nav_activity": "⏳ गतिविधि ब्रेक",
        "nav_subtle_ally": "🤝 गुप्त सहायक",
        "welcome": "साथी में आपका स्वागत है",
        "target": "आपका लक्ष्य",
        "logout": "लॉगआउट",
        "login": "लॉगिन",
        "register": "रजिस्टर",
        "email": "ईमेल पता",
        "password": "पासवर्ड",
        "name": "पूरा नाम",
        "exam_target": "लक्षित परीक्षा",
        "exam_date": "परीक्षा तिथि",
        "daily_tip": "दैनिक सलाह",
        # Dashboard
        "dash_title": "📊 छात्र कल्याण डैशबोर्ड",
        "student": "छात्र",
        "avg_mood": "औसत मनोदशा (14d)",
        "avg_energy": "औसत ऊर्जा (14d)",
        "avg_sleep": "औसत नींद (14d)",
        "avg_study": "औसत पढ़ाई (14d)",
        "trends_title": "📈 समय के साथ कल्याण रुझान",
        "sleep_title": "प्रति दिन नींद के घंटे",
        "study_title": "प्रति दिन पढ़ाई के घंटे",
        "screen_reader_alt": "👁️ स्क्रीन रीडर और कम बैंडविड्थ के लिए वैकल्पिक पाठ देखें",
        "summary_table": "दैनिक कल्याण लॉग सारांश तालिका",
        "no_logs": "कल्याण चार्ट देखने के लिए अपने दैनिक मनोदशा की जांच लॉग करें!",
        "urgent_escalation": "🚨 तत्काल: छात्र सुरक्षा चेतावनी सक्रिय",
        "escalation_p1": "हाल की स्व-रिपोर्ट या तनाव संकेतक बताते हैं कि आप अत्यधिक दबाव या संकट का अनुभव कर रहे हैं।",
        "flagged_reasons": "चिह्नित कारण:",
        "support_helplines": "आपको इस रास्ते पर अकेले चलने की ज़रूरत नहीं है। कृपया तुरंत निम्नलिखित गोपनीय सहायता संसाधनों में से किसी एक से संपर्क करें:",
        # Mood Check-In
        "mood_title": "📝 दैनिक मनोदशा लॉग (मूड चेक-इन)",
        "mood_desc": "आप कैसा महसूस करते हैं, इसे लॉग करने के लिए एक क्षण लेने से पैटर्न देखने में मदद मिलती है और आप केंद्रित रहते हैं।",
        "mood_q": "आज आपका मूड कैसा है?",
        "energy_q": "आपका वर्तमान ऊर्जा स्तर क्या है?",
        "sleep_q": "कल रात आप कितने घंटे सोए?",
        "study_q": "आज आपने कितने घंटे पढ़ाई की?",
        "emotion_tags": "भावना टैग",
        "select_emotions": "अपनी वर्तमान स्थिति से मेल खाती भावनाओं का चयन करें:",
        "journal_notes": "कोई भी विचार या जर्नल नोट्स लिखें:",
        "journal_placeholder": "आज क्या तनाव पैदा कर रहा है या आपको अध्ययन करने में मदद कर रहा है?",
        "submit_entry": "प्रविष्टि जमा करें",
        "mood_success": "मनोदशा सफलतापूर्वक लॉग की गई! अपने रुझान देखने के लिए डैशबोर्ड देखें।",
        "mood_fail": "मनोदशा लॉग करने में विफल। कृपया पुन: प्रयास करें।",
        # Assessment Page Specifics
        "assess_title": "📋 कल्याण मूल्यांकन",
        "assess_desc": "यह गैर-नैदानिक मूल्यांकन आपके PHQ-9 (अवसाद), GAD-7 (चिंता), और PSS-4 (तनाव) के स्तर को ट्रैक करने में मदद करता है। आपके उत्तर गोपनीय हैं।",
        "assess_sec1": "भाग 1: सामान्य मनोदशा और कल्याण (PHQ-9)",
        "assess_sec2": "भाग 2: चिंता और तनाव प्रतिक्रिया (GAD-7)",
        "assess_sec3": "भाग 3: कथित मुकाबला और दबाव (PSS-4)",
        "assess_caption_2weeks": "पिछले 2 हफ्तों में, आप निम्नलिखित में से किसी भी समस्या से कितनी बार परेशान रहे हैं?",
        "assess_caption_month": "पिछले महीने में, आपको कितनी बार ऐसा महसूस हुआ...",
        "assess_submit": "मूल्यांकन जमा करें और परिणाम देखें",
        "assess_success": "मूल्यांकन सफलतापूर्वक सबमिट किया गया!",
        "assess_severe_warn": "⚠️ आपके परिणाम गंभीर मानसिक दबाव का संकेत देते हैं। हम आपको हमारे सूचीबद्ध सलाहकारों में से किसी एक से बात करने या संसाधन और सहायक अनुभागों पर जाने के लिए प्रोत्साहित करते हैं।",
        "assess_moderate_info": "💡 आप मध्यम तनाव का अनुभव कर रहे हैं। गतिविधि ब्रेक पेज के माध्यम से नियमित ब्रेक निर्धारित करने पर विचार करें।",
        "assess_mild_info": "✨ कम तनावपूर्ण तैयारी दिनचर्या बनाए रखने के लिए बहुत बढ़िया काम! कल्याण रुझानों को ट्रैक करने के लिए मनोदशा लॉग करना जारी रखें।",
        "assess_result_hdr": "मूल्यांकन परिणाम",
        "assess_pressure_lvl": "दबाव स्तर",
        "assess_breakdown_lbl": "नीचे आपका कल्याण सूचकांक विश्लेषण दिया गया है:",
        "opt_not_at_all": "बिल्कुल नहीं",
        "opt_several_days": "कई दिन",
        "opt_more_than_half": "आधे से अधिक दिन",
        "opt_nearly_every_day": "लगभग हर दिन",
        "opt_never": "कभी नहीं",
        "opt_almost_never": "लगभग कभी नहीं",
        "opt_sometimes": "कभी-कभी",
        "opt_fairly_often": "अक्सर",
        "q1": "चीजों को करने में बहुत कम रुचि या आनंद होना?",
        "q2": "उदास, निराश या असहाय महसूस करना?",
        "q3": "सोने में परेशानी या बहुत अधिक सोना?",
        "q4": "थका हुआ या कम ऊर्जा महसूस करना?",
        "q5": "कम भूख लगना या बहुत अधिक खाना?",
        "q6": "अपने बारे में बुरा महसूस करना — या कि आप एक असफल व्यक्ति हैं या आपने खुद को या अपने परिवार को निराश किया है?",
        "q7": "चीजों पर ध्यान केंद्रित करने में परेशानी, जैसे कि पढ़ना या टीवी देखना?",
        "q8": "इतनी धीमी गति से चलना या बोलना कि अन्य लोगों ने ध्यान दिया हो? या इसके विपरीत — इतना बेचैन होना कि आप सामान्य से बहुत अधिक घूम रहे हों?",
        "q9": "यह सोचना कि आपका मर जाना बेहतर होगा, या किसी तरह खुद को चोट पहुँचाना?",
        "q10": "घबराहट, चिंता या तनाव महसूस करना?",
        "q11": "चिंता करना बंद या नियंत्रित न कर पाना?",
        "q12": "विभिन्न चीजों के बारे में बहुत अधिक चिंता करना?",
        "q13": "आराम करने में परेशानी?",
        "q14": "इतना बेचैन होना कि शांत बैठना मुश्किल हो?",
        "q15": "आसानी से चिढ़ जाना या चिड़चिड़ा हो जाना?",
        "q16": "डर महसूस होना जैसे कि कुछ भयानक होने वाला है?",
        "q17": "पिछले महीने में, आपको कितनी बार ऐसा महसूस हुआ कि आप अपने जीवन की महत्वपूर्ण चीजों को नियंत्रित करने में असमर्थ थे?",
        "q18": "पिछले महीने में, आपने अपनी व्यक्तिगत समस्याओं को संभालने की अपनी क्षमता के बारे में कितनी बार आश्वस्त महसूस किया?",
        "q19": "पिछले महीने में, आपको कितनी बार ऐसा महसूस हुआ कि चीजें आपके अनुसार चल रही थीं?",
        "q20": "पिछले महीने में, आपको कितनी बार ऐसा महसूस हुआ कि कठिनाइयां इतनी अधिक बढ़ रही थीं कि आप उन्हें पार नहीं कर सके?"
    }
}

def t(key):
    lang = st.session_state.get("language", "English")
    return TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, key)

from babel.dates import format_date, format_datetime
from datetime import datetime

def fd(date_val, format="medium"):
    if isinstance(date_val, str):
        try:
            # Handle possible ISO formats
            date_val = datetime.fromisoformat(date_val.replace("Z", "+00:00"))
        except ValueError:
            return date_val
    lang = st.session_state.get("language", "English")
    locale = "hi" if lang == "Hindi (हिन्दी)" else "en"
    try:
        return format_date(date_val, format=format, locale=locale)
    except Exception:
        return str(date_val)

def fdt(datetime_val, format="medium"):
    if isinstance(datetime_val, str):
        try:
            datetime_val = datetime.fromisoformat(datetime_val.replace("Z", "+00:00"))
        except ValueError:
            return datetime_val
    lang = st.session_state.get("language", "English")
    locale = "hi" if lang == "Hindi (हिन्दी)" else "en"
    try:
        return format_datetime(datetime_val, format=format, locale=locale)
    except Exception:
        return str(datetime_val)

