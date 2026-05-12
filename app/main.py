from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from .database import init_db, engine
from .models import AdminUser
from .frontend import router as frontend_router
from .admin import router as admin_router

app = FastAPI(title="Panchnad Shodh Sansthan")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


SEED_VERSION = 5  # bump this to force re-seed on next deploy

@app.on_event("startup")
def on_startup():
    import os
    from .database import DB_PATH
    # Force re-seed if version changed (delete old DB and recreate engine)
    version_file = DB_PATH.parent / ".seed_version"
    current = int(version_file.read_text().strip()) if version_file.exists() else 0
    if current < SEED_VERSION:
        if DB_PATH.exists():
            engine.dispose()
            os.remove(DB_PATH)
            print(f"[SEED] Deleted old DB at {DB_PATH}, re-seeding v{SEED_VERSION}")
        version_file.write_text(str(SEED_VERSION))
    init_db()
    with Session(engine) as s:
        if not s.exec(select(AdminUser)).first():
            _seed(s)
            print(f"[SEED] Database seeded successfully (v{SEED_VERSION})")


def _seed(s: Session):
    """Seed initial data on first run."""
    from datetime import date
    from .models import Centre, Post, Person, Publication, AnnualLecture, GalleryImage
    from .auth import hash_password

    s.add(AdminUser(username="admin", password_hash=hash_password("panchnad2025")))

    for c in [
        Centre(name="Panchnad Adhyayan Kendra", location="Panjab University, Chandigarh"),
        Centre(name="Panchnad Adhyayan Kendra", location="Chandigarh"),
        Centre(name="पंचनद शोध संस्थान (Panchnad Shodh Sansthan)", location="Hisar, Haryana"),
        Centre(name="Panchnad Adhyayan Kendra", location="Kurukshetra, Haryana"),
        Centre(name="Panchnad Adhyayan Kendra", location="Solan, Himachal Pradesh"),
        Centre(name="Adhyayan Kendra", location="Himachal Pradesh University, Shimla"),
    ]:
        s.add(c)

    s.add(Person(name="Prof. Brij Kishore Kuthiala", role="President (Adhyaksh), Panchnad Shodh Sansthan",
        bio="Born 1948. Chairman of Haryana State Higher Education Council. Former Vice-Chancellor, Makhanlal Chaturvedi National University. Over 51 years in media teaching and academic management."))
    s.add(Person(name="Justice T. U. Mehta", role="Founding Chairman (1984)",
        bio="Former Chief Justice of Himachal Pradesh High Court. Founded Panchnad Research Institute in 1984."))

    posts_data = [
        ("देश की प्रगति में महिलाओं का अभूतपूर्व योगदान — क्षेत्रीय अभ्यास वर्ग महिला आयाम, हिसार",
         "पंचनद शोध संस्थान (प्रज्ञा प्रवाह) क्षेत्रीय अभ्यास वर्ग महिला आयाम की बैठक दो सत्रों में आयोजित की गई।\n\n"
         "प्रथम सत्र: 'पराधीनता से स्वाधीनता और स्वतंत्रता की ओर भारत — महिलाओं का योगदान'\n"
         "मुख्य प्रस्तोता: डॉ. मुदिता वर्मा (पंचनद शोध संस्थान महिला आयाम प्रमुख)\n"
         "विशिष्ट अतिथि: डॉ. निष्ठा (सह प्रभारी, महिला आयाम उत्तरी क्षेत्र)\n"
         "अध्यक्षता: डॉ. ऋषि गोयल (उपाध्यक्ष)\n\n"
         "डॉ. मुदिता वर्मा ने बताया कि भारत का स्वतंत्रता संग्राम केवल पुरुषों के साहस और बलिदान की कहानी नहीं है, बल्कि यह भारतीय महिलाओं के त्याग, संघर्ष और राष्ट्र प्रेम का भी स्वर्णिम इतिहास रहा है। "
         "उन्होंने झांसी की रानी लक्ष्मीबाई, बेगम हजरत महल, सरोजिनी नायडू, कस्तूरबा गांधी तथा अरुणा आसफ अली जैसी अनेक महिलाओं के उदाहरण देकर महिलाओं की शौर्य गाथा पर विस्तार से प्रकाश डाला। "
         "उन्होंने कहा कि स्वतंत्र भारत में भी महिलाओं ने शिक्षा, स्वास्थ्य, विज्ञान, राजनीति, खेलकूद और अंतरिक्ष जैसे क्षेत्रों में देश का नाम रोशन किया है।\n\n"
         "द्वितीय सत्र: 'बौद्धिक विमर्श — प्रक्रिया और परिणाम'\n"
         "प्रस्तोता: प्रो. बी.के. कुठियाला (अध्यक्ष, प्रज्ञा प्रवाह एवं पंचनद शोध संस्थान)\n"
         "अध्यक्षता: श्रीमती ज्योति बैंदा (सदस्य, हरियाणा लोक सेवा आयोग)\n\n"
         "प्रो. कुठियाला ने बताया कि तर्क, ज्ञान, अनुभव और विचारों के आधार पर गंभीर चर्चा करना बौद्धिक विमर्श में शामिल है। यह केवल बहस नहीं होती, बल्कि सत्य की खोज, समस्याओं के समाधान और समाज के विकास का माध्यम होती है। "
         "उन्होंने कहा कि लोकतंत्र में शिक्षा, विज्ञान, साहित्य और समाज सुधार सभी क्षेत्रों में बौद्धिक विमर्श की महत्वपूर्ण भूमिका होती है।\n\n"
         "इस अवसर पर पंचनद शोध संस्थान प्रज्ञा प्रवाह हिसार के अध्यक्ष प्रो. जगबीर सिंह, संरक्षक ज्ञानचंद बंसल व अलग-अलग राज्यों से महिलाओं ने भाग लिया।",
         date(2026, 5, 9), "Event"),
        ("भारत में महिलाओं से संबंधित कानून — गोष्ठी, हिसार",
         "चौधरी चरण सिंह हरियाणा कृषि विश्वविद्यालय के इंदिरा चक्रवर्ती सामुदायिक विज्ञान महाविद्यालय एवं पंचनद शोध संस्थान (प्रज्ञा प्रवाह) महिला आयाम द्वारा "
         "'भारत में महिलाओं से संबंधित कानून' विषय पर गोष्ठी का शुभारंभ हुआ।\n\n"
         "अध्यक्षता: प्रो. बी.के. कुठियाला (पूर्व अध्यक्ष, हरियाणा राज्य उच्च शिक्षा परिषद पंचकूला; अध्यक्ष, पंचनद शोध संस्थान चंडीगढ़)\n"
         "मुख्य वक्ता: अधिवक्ता मोनिका अरोड़ा (सर्वोच्च न्यायालय की वरिष्ठ अधिवक्ता एवं प्रज्ञा प्रवाह महिला आयाम प्रमुख)\n"
         "मंच पर उपस्थित: डॉ. मुदिता वर्मा (पंचनद महिला आयाम प्रमुख), डॉ. मदन खीचड़ (छात्र कल्याण निदेशक)\n\n"
         "अधिवक्ता मोनिका अरोड़ा ने भारतीय संस्कृति और प्राचीन काल में महिलाओं की स्थिति पर विस्तार से बताया। उन्होंने कहा कि हमारी संस्कृति में नारी को देवी स्वरूप माना गया है — "
         "मां दुर्गा को शक्ति, मां सरस्वती को ज्ञान और मां लक्ष्मी को समृद्धि की देवी के रूप में पूजते हैं। "
         "उन्होंने बताया कि संविधान में महिलाओं को सुरक्षा, सम्मान और समानता प्रदान करने के लिए विभिन्न कानून बनाए गए हैं — "
         "दहेज निषेध अधिनियम 1961, घरेलू हिंसा संरक्षण अधिनियम 2005, कार्यस्थल पर यौन उत्पीड़न रोकथाम अधिनियम 2013 तथा बाल विवाह प्रतिषेध अधिनियम 2006। "
         "महिलाओं को अपने अधिकारों के प्रति जागरूक होना बहुत जरूरी है।\n\n"
         "प्रो. बी.के. कुठियाला ने कहा कि नारी केवल परिवार की शक्ति नहीं, बल्कि समाज एवं राष्ट्र के नवनिर्माण में भी उनकी महत्वपूर्ण भूमिका है। "
         "किसी भी देश की प्रगति का वास्तविक मापदंड वहां की महिलाओं की स्थिति से लगाया जा सकता है। "
         "संविधान के अनुच्छेद 14, 15 और 16 महिलाओं को पुरुषों के समान अधिकार प्रदान करते हैं। "
         "उन्होंने कहा — यत्र नार्यस्तु पूज्यन्ते, रमन्ते तत्र देवता — जहां नारी का सम्मान और पूजन होता है वहां देवताओं का निवास होता है।\n\n"
         "इस अवसर पर पंचनद शोध संस्थान अध्ययन केंद्र हिसार के अध्यक्ष डॉ. जगबीर सिंह, संरक्षक ज्ञानचंद बंसल सहित पदाधिकारी, "
         "विश्वविद्यालय की महिला शिक्षक, छात्राएं और गणमान्य नागरिक उपस्थित रहे।",
         date(2026, 5, 11), "Seminar"),
        ("31st Annual Panchnad Lecture — Truth of Partition of India",
         "31वाँ वार्षिक पंचनद व्याख्यान — विषय: भारत के विभाजन का सच. मुख्य अतिथि: पंजाब के राज्यपाल श्री गुलाब चंद कटारिया. मुख्य वक्ता: श्री प्रशांत पॉल. विचार प्रवाह तथा Human Values and Rights in Quran पुस्तकों का विमोचन।",
         date(2025, 1, 5), "Annual Lecture"),
        ("जलती पराली, पर्यावरण, खेती एवं सेहत की बदहाली",
         "ऑनलाइन गोष्ठी — प्रस्तोता: उमेन्द्र दत्त; अध्यक्षता: प्रो. बृज किशोर कुठियाला. आयोजक: पंचनद अध्ययन केंद्र, पंजाब विश्वविद्यालय चंडीगढ़.",
         date(2023, 11, 16), "Seminar"),
        ("भारत के स्वर्णिम इतिहास पर प्रो. महेंद्र सिंह",
         "विदेशी शक्तियों द्वारा भारत के इतिहास के तथ्यहीन प्रस्तुतीकरण पर लेख का साझा.",
         date(2023, 9, 5), "Article"),
        ("श्रद्धांजलि: वीरेश्वर द्विवेदी जी",
         "राष्ट्रीय स्वयंसेवक संघ के वरिष्ठ प्रचारक एवं राष्ट्रधर्म पत्रिका के पूर्व सम्पादक के निधन पर शोक.",
         date(2023, 9, 4), "Tribute"),
        ("अध्ययन केंद्र, हिसार की गतिविधियाँ",
         "पंचनद शोध संस्थान, अध्ययन केंद्र-हिसार से अद्यतन.",
         date(2023, 9, 3), "Update"),
        ("डॉ. कृष्ण गोपाल जी का व्याख्यान",
         "विषय: प्राचीन भारत में अध्ययन के विविध आयाम.",
         date(2023, 2, 18), "Lecture"),
        ("लोकमंथन – 2022 के पूर्व विमर्श",
         "करनाल में लोकमंथन-2022 के पूर्व विमर्श का आयोजन. लोकमंथन 2022 गुवाहाटी में 21-24 सितम्बर को लोकपरम्परा विषय पर आयोजित हुआ.",
         date(2022, 8, 10), "Event"),
        ("वर्तमान संदर्भ में समान नागरिक संहिता का महत्व",
         "ऑनलाइन मासिक गोष्ठी — आयोजक: पंचनद अध्ययन केंद्र, कुरुक्षेत्र.",
         date(2022, 7, 27), "Seminar"),
        ("संयुक्त गोष्ठी — सोलन व शिमला",
         "अध्ययन केंद्र, सोलन तथा हिमाचल प्रदेश विश्वविद्यालय, शिमला के संयुक्त तत्वाधान में.",
         date(2022, 7, 23), "Seminar"),
    ]
    for title, body, d, tag in posts_data:
        s.add(Post(title=title, body=body, posted_on=d, tag=tag))

    pubs = [
        ("Vichar Pravah (विचार प्रवाह)",
         "Collection of thought essays published by Panchnad Shodh Sansthan. Released by Punjab Governor Gulab Chand Kataria at the 31st Annual Panchnad Lecture in Chandigarh.",
         2025, "Panchnad Shodh Sansthan"),
        ("Human Values and Rights in Quran",
         "A study on human values and rights as expressed in the Quran. Released at the 31st Annual Panchnad Lecture by Punjab Governor.",
         2025, "Panchnad Shodh Sansthan"),
        ("Bharat 2047 — A Collective Vision",
         "Edited by Prof. B. K. Kuthiala, co-published by Prabhat Prakashan, New Delhi. Presents a comprehensive dialogue about the future of India at 100 years of independence. "
         "The English edition (ISBN 9789355620330, 352 pp.) carries the collective vision of 20 experts covering rural life, global threats, dharma, sanskriti, technology, economics, finance and defence. "
         "Hindi edition published 4 March 2022 (232 pp.). Available on Flipkart, Amazon.in and leading bookstores.",
         2022, "Prof. Brij Kishore Kuthiala (Editor)"),
        ("Hindu Nationalism — A Contemporary Perspective",
         "Built around Mohan Bhagwat's 2008 Panchnad Lecture. Introduction by Dr. Murli Manohar Joshi making a case for the revival of sanskriti as the basis for re-emergence of Indian society. "
         "Explores the quality of intellectual debate in post-independence India.",
         2008, "Shyam Khosla & B. K. Kuthiala (Editors)"),
        ("The Dangs (Gujarat) — Field Study Report",
         "A detailed field study into Christians-Vanvasi clashes in Dangs district of Gujarat in 1999. Team: Dr. N. K. Trikha, Shri Shyam Khosla, Dr. B. L. Gupta, and Dr. K. S. Arya. "
         "A signed copy was presented to Union Home Minister Shri L. K. Advani. Released at a public function presided over by Justice D. S. Tewatia, former Chief Justice of Calcutta High Court.",
         1999, "Panchnad Research Institute"),
        ("Panchnad Research Journal (Annual)",
         "Annual research journal published by the institute. Confirmed issues include 1988 (Punjab Crisis dialogue papers) and 1989 (Pakistani infiltration in Rajasthan). "
         "Distribution is institutional.",
         1988, "Panchnad Research Institute"),
        ("Terrorism in Punjab — Cause and Cure",
         "Papers presented at a seminar organised by the institute in Delhi, 1985. Contributors include Justice H. R. Khanna ('Diagnosis and Prescription'), "
         "Khushwant Singh ('A Lasting Solution'), K. R. Malkani ('Inconvenient Questions'), and five more sections. "
         "Bilingual (Hindi-English), 130 pages. Held at University of Michigan library.",
         1987, "Justice Hans Raj Khanna & Panchnad Research Institute"),
        ("Facts Speak for Themselves",
         "Field study report on the 1984 anti-Sikh riots — investigative research documenting ground realities. "
         "Authors: Shyam Khosla, Krishan Lal Maini, Dr. Sunil Khetrapal, and Hemant Vishnoi. Published as an in-house monograph by the institute.",
         1985, "Shyam Khosla, K. L. Maini, Dr. S. Khetrapal & H. Vishnoi"),
    ]
    for title, desc, year, author in pubs:
        s.add(Publication(title=title, description=desc, year=year, author_or_editor=author))

    lectures_data = [
        (2025, "Prashant Paul", "Truth of Partition of India"),
        (2008, "Mohan Bhagwat", "National security and cultural issues"),
        (2005, "Devinder Swarup", "Contemporary national discourse"),
        (2003, "Arun Jaitley", "Constitutional law and governance"),
        (2001, "K. P. S. Gill", "Internal security challenges"),
        (1999, "K. N. Govindacharya", "Socio-political thought"),
        (1997, "Samdong Rinpoche", "Tibetan culture and Indian heritage"),
        (1993, "Dr. M. M. Joshi", "Education and national identity"),
        (1990, "Justice D. S. Tewatia", "Judiciary and constitutional values"),
        (1987, "Lt. Gen. S. K. Sinha", "National security perspectives"),
    ]
    for year, speaker, topic in lectures_data:
        s.add(AnnualLecture(year=year, speaker=speaker, topic=topic))

    gallery_data = [
        ("ऑनलाइन गोष्ठी: जलती पराली, पर्यावरण, खेती एवं सेहत की बदहाली", "पंजाब विश्वविद्यालय, चंडीगढ़", date(2023, 11, 19), "483877419_1040475818114173_748127478562764536_n.jpg", "पंजाब विश्वविद्यालय, चंडीगढ़"),
        ("संयुक्त संगोष्ठी: लोक परंपराओं में भारत बोध", "अध्ययन केंद्र, शिमला", date(2022, 8, 10), "484316214_2716947118498008_3847684584397874365_n.jpg", "अध्ययन केंद्र, शिमला"),
        ("ई-गोष्ठी: बढ़ता आतंकवाद — कारण और समाधान", "अध्ययन केंद्र, सोलन-शिमला", date(2022, 7, 24), "482135980_2716193115240075_5834294651086192713_n.jpg", "अध्ययन केंद्र, सोलन-शिमला"),
        ("Panel Discussion: Udaipur Incident & Talibani Mindset — A Wakeup Call", "Study Centre, Amritsar", date(2022, 7, 10), "482191334_2714108652115188_8253010821037281469_n.jpg", "Study Centre, Amritsar"),
        ("Webinar: WTO and India's Concerns on Future of Agriculture", "अध्ययन केंद्र, फरीदाबाद", date(2022, 7, 9), "482252440_2714107385448648_8495339197087478593_n.jpg", "अध्ययन केंद्र, फरीदाबाद"),
        ("गोष्ठी: अग्निपथ योजना का विश्लेषण", "अध्ययन केंद्र, हिसार", date(2022, 7, 7), "482233521_2714100978782622_3155344884052050399_n.jpg", "अध्ययन केंद्र, हिसार"),
        ("मासिक गोष्ठी: अग्नीपथ योजना का विश्लेषण", "पंजाब विश्वविद्यालय, चंडीगढ़", date(2022, 6, 23), "482212760_2713315682194485_3211705066653246355_n.jpg", "पंजाब विश्वविद्यालय, चंडीगढ़"),
        ("Webinar: Russia-Ukraine Conflict — Impacts on Global Order", "चंडीगढ़", date(2022, 3, 13), "480408658_2695829437276443_585454282456598877_n.jpg", "चंडीगढ़"),
        ("वार्षिकोत्सव गोष्ठी: माँ, मातृभूमि, मातृभाषा — कोई विकल्प नहीं", "दक्षिण दिल्ली अध्ययन केंद्र", date(2022, 3, 12), "480741183_2695827310609989_7528943846725312231_n.jpg", "दक्षिण दिल्ली अध्ययन केंद्र"),
        ("ई-गोष्ठी: Diversity in Unity OR Unity in Diversity", "अध्ययन केंद्र, शिमला", date(2022, 3, 11), "480331013_2695646740628046_4246148268235940101_n.jpg", "अध्ययन केंद्र, शिमला"),
        ("ई-गोष्ठी: गीता का प्रथम शब्द धर्म — विमर्श और विवेचना", "अध्ययन केंद्र, हिसार", date(2022, 3, 1), "480316642_2693982500794470_262313530085543104_n.jpg", "अध्ययन केंद्र, हिसार"),
        ("तरंग-गोष्ठी: गुरु रविदास जी महाराज की शिक्षाए और समरस भारतीय समाज", "अध्ययन केंद्र, यमुनानगर", date(2022, 2, 16), "476250611_2686715804854473_2173086050691679656_n.jpg", "अध्ययन केंद्र, यमुनानगर"),
        ("व्याख्यान श्रृंखला: भारतीय जीवन और संस्कार परम्परा, भाग-2", "पूर्वी दिल्ली अध्ययन केंद्र", date(2020, 8, 16), "117732738_1467575240101875_3804341879268345467_n.jpg", "पूर्वी दिल्ली अध्ययन केंद्र"),
        ("व्याख्यान श्रृंखला: भारतीय जीवन और संस्कार परम्परा, भाग-1", "पूर्वी दिल्ली अध्ययन केंद्र", date(2020, 8, 9), "117444729_1467858433406889_7012850492520342147_n.jpg", "पूर्वी दिल्ली अध्ययन केंद्र"),
        ("परिचर्चा: आत्मनिर्भर भारत — जरुरत और मायने", "Study Centre, Pathankot", date(2020, 5, 27), "98447763_1399428733583193_443380400362881024_n.jpg", "Study Centre, Pathankot"),
        ("वेब-गोष्ठी: नियंत्रण रेखा के पार का भारत — गिलगित, बाल्टिस्तान और मुज़फ़्फ़राबाद", "पश्चिमी दिल्ली अध्ययन केंद्र", date(2020, 5, 14), "97971894_1388710031321730_5468388722460327936_n.jpg", "पश्चिमी दिल्ली अध्ययन केंद्र"),
        ("Webinar: Self Regulation in Corona and Post Corona Period", "Study Centre, Batala", date(2020, 5, 7), "96119435_1382863118573088_2439177597448355840_n.jpg", "Study Centre, Batala"),
        ("Webinar: Tablighi Jamaat — Background and the Challenges", "Study Centre, Amritsar", date(2020, 4, 28), "94228619_1374161742776559_7021214206795972608_n.jpg", "Study Centre, Amritsar"),
        ("ई-विचार गोष्ठी: लॉकडाउन में जीवनचर्या परिवर्तन एवम् भविष्य में प्रभाव", "अध्ययन केंद्र, रोहतक", date(2020, 4, 18), "93419749_1367531943439539_7089621971985498112_n.jpg", "अध्ययन केंद्र, रोहतक"),
        ("Webinar: Evolving Methodologies to Create Post COVID Narrative", "Panchnad Research Institute", date(2020, 4, 15), "92710587_1364912467034820_933497771552407552_n.jpg", "Panchnad Research Institute"),
        ("ई-गोष्ठी: कोरोना संकट में सेवा कार्य", "अध्ययन केंद्र, कुरुक्षेत्र", date(2020, 4, 14), "92245882_1362233710636029_5905465214639276032_n.jpg", "अध्ययन केंद्र, कुरुक्षेत्र"),
        ("गोष्ठी: वर्तमान सामाजिक चुनौतियां", "अध्ययन केंद्र, जालंधर", date(2020, 3, 1), "87880574_1324126881113379_5423142139645132800_n.jpg", "अध्ययन केंद्र, जालंधर"),
        ("Discussion: Present Social Challenges", "Study Centre, Pathankot", date(2020, 3, 1), "88230734_1326157064243694_4306977957294899200_n.jpg", "Study Centre, Pathankot"),
        ("मासिक गोष्ठी: दिल्ली जनादेश 2020 के मायने", "पूर्वी दिल्ली अध्ययन केंद्र", date(2020, 2, 23), "86685504_1317638691762198_8447200656816603136_n.jpg", "पूर्वी दिल्ली अध्ययन केंद्र"),
        ("गोष्ठी: विकास की अवधारणा", "अध्ययन केंद्र, कुरुक्षेत्र", date(2020, 2, 15), "84600455_1314786955380705_529550694294749184_n.jpg", "अध्ययन केंद्र, कुरुक्षेत्र"),
        ("गोष्ठी एवं पुस्तक प्रस्तुति: हिन्दुत्व - बदलते परिवेश में", "चंडीगढ़", date(2020, 1, 24), "82365193_1295459600646774_2701296187348090880_n.jpg", "चंडीगढ़"),
        ("मासिक गोष्ठी: नागरिकता संशोधन अधिनियम - 2019", "अध्ययन केंद्र, गुरुग्राम", date(2020, 1, 11), "81975167_1289998827859518_8603887347311837184_n.jpg", "अध्ययन केंद्र, गुरुग्राम"),
        ("मासिक गोष्ठी: नागरिकता संशोधन अधिनियम - 2019", "अध्ययन केंद्र, कुरुक्षेत्र", date(2020, 1, 4), "81554762_1277351495790918_1898050523181875200_n.jpg", "अध्ययन केंद्र, कुरुक्षेत्र"),
        ("मासिक गोष्ठी: नागरिकता संशोधन अधिनियम - 2019", "अध्ययन केंद्र, फरीदाबाद", date(2019, 12, 23), "80428310_1271934352999299_964819975904690176_n.jpg", "अध्ययन केंद्र, फरीदाबाद"),
        ("चेतना अभियान: हरियाणा की लोक-संस्कृति और भावी पीढ़ी का दायित्व", "अध्ययन केंद्र, यमुनानगर", date(2019, 12, 20), "80244660_1254082668117801_1789234872447926272_n.jpg", "अध्ययन केंद्र, यमुनानगर"),
        ("मासिक गोष्ठी: श्रीराम जन्मभूमि पर सुप्रीम कोर्ट का निर्णय", "अध्ययन केंद्र, भिवानी", date(2019, 11, 25), "75550493_1236656276527107_6649809701603115008_n.jpg", "अध्ययन केंद्र, भिवानी"),
        ("विशेष व्याख्यान: संस्कृत और विज्ञान", "दिल्ली प्रान्त", date(2019, 11, 24), "74940234_1226389470887121_6151701019773370368_n.jpg", "दिल्ली प्रान्त"),
        ("गोष्ठी: सच्चा सौदा-वंड छको की वर्तमान प्रासंगिकता", "पंजाब विश्वविद्यालय, चंडीगढ़", date(2019, 11, 19), "77071353_1231028200423248_6803454661899583488_n.jpg", "पंजाब विश्वविद्यालय, चंडीगढ़"),
        ("मासिक गोष्ठी: आर्यों का मूलस्थान", "अध्ययन केंद्र, रोहतक", date(2019, 11, 14), "75640794_1224083981117670_193025927750352896_n.jpg", "अध्ययन केंद्र, रोहतक"),
        ("मासिक गोष्ठी: आर्यों का मूलनिवास", "अध्ययन केंद्र, कुरुक्षेत्र", date(2019, 11, 10), "71830869_1220998748092860_7038806079307776000_n.jpg", "अध्ययन केंद्र, कुरुक्षेत्र"),
        ("ई-गोष्ठी: दूसरी लहर उपरांत व तीसरी लहर पूर्व तनाव प्रबंधन", "पंचनद अध्ययन केंद्र, रोहतक", date(2021, 6, 19), "event_rohtak_jun19.jpg", "पंचनद अध्ययन केंद्र, रोहतक"),
        ("ई-गोष्ठी: कोविड-19 से उत्पन्न समस्याओं का योग से निदान", "पंचनद शोध संस्थान", date(2021, 6, 21), "event_yogday_jun21.jpg", "पंचनद शोध संस्थान"),
        ("Webinar: Psychological Aspect of Media Coverage During Covid Epidemic", "Study Centre, Amritsar", date(2021, 6, 27), "event_amritsar_jun27.jpg", "Study Centre, Amritsar"),
        ("ई-गोष्ठी: बंगाल चुनाव परिणाम के बाद उपजी हिंसा", "दक्षिण दिल्ली अध्ययन केन्द्र", date(2021, 6, 28), "event_delhi_jun28.jpg", "दक्षिण दिल्ली अध्ययन केन्द्र"),
        ("ई-गोष्ठी: ध्यान के माध्यम से क्रोध पर नियंत्रण", "पंचनद अध्ययन केंद्र, रोहतक", date(2021, 10, 31), "event_rohtak_oct31.jpg", "पंचनद अध्ययन केंद्र, रोहतक"),
    ]
    for title, desc, d, filename, centre in gallery_data:
        s.add(GalleryImage(title=title, description=desc, event_date=d, image_filename=filename, centre=centre))

    s.commit()


app.include_router(frontend_router)
app.include_router(admin_router, prefix="/admin")
