from datetime import date
from sqlmodel import Session
from app.database import engine, init_db
from app.models import Centre, Post, Person, Publication, AnnualLecture, GalleryImage, AdminUser
from app.auth import hash_password

init_db()

admin = AdminUser(username="admin", password_hash=hash_password("panchnad2025"))

centres = [
    Centre(name="Panchnad Adhyayan Kendra", location="Panjab University, Chandigarh"),
    Centre(name="Panchnad Adhyayan Kendra", location="Chandigarh"),
    Centre(name="पंचनद शोध संस्थान (Panchnad Shodh Sansthan)", location="Hisar, Haryana"),
    Centre(name="Panchnad Adhyayan Kendra", location="Kurukshetra, Haryana"),
    Centre(name="Panchnad Adhyayan Kendra", location="Solan, Himachal Pradesh"),
    Centre(name="Adhyayan Kendra", location="Himachal Pradesh University, Shimla"),
]

people = [
    Person(
        name="Prof. Brij Kishore Kuthiala",
        role="President (Adhyaksh), Panchnad Shodh Sansthan",
        bio="Born 1948. Trained at Film & Television Institute of India, Pune and Indian Institute of Mass Communication, New Delhi. "
            "Chairman of Haryana State Higher Education Council. Former Vice-Chancellor, Makhanlal Chaturvedi National University of "
            "Journalism and Communication, Bhopal. Former academic staff at Kurukshetra University. "
            "Awarded Honorary D.Litt. by Maharshi Dayanand University. Over 51 years in media teaching and academic management.",
    ),
    Person(
        name="Justice T. U. Mehta",
        role="Founding Chairman (1984)",
        bio="Former Chief Justice of Himachal Pradesh High Court. Founded Panchnad Research Institute in 1984 and served as its first Chairman.",
    ),
]

posts = [
    Post(
        title="हिसार पंचनद अध्ययन केंद्र — क्षेत्रीय अभ्यास वर्ग महिला आयाम एवं हरियाणा प्रांतीय बैठक",
        body="हिसार पंचनद अध्ययन केंद्र द्वारा आयोजित क्षेत्रीय अभ्यास वर्ग महिला आयाम एवं हरियाणा प्रांतीय बैठक, "
             "डॉ. ब्रिज किशोर कुठियाला, डॉ. जगबीर सिंह, डॉ. मुदीता वर्मा एवं आदरणीय ज्ञानचंद बंसल जी के प्रेरणादायी "
             "मार्गदर्शन एवं सान्निध्य में अत्यंत गरिमामयी, सुव्यवस्थित एवं यशस्वी रूप से संपन्न हुई।\n\n"
             "इस आयोजन ने संगठनात्मक क्षमता, अनुशासन, वैचारिक प्रतिबद्धता एवं सामूहिक समर्पण का उत्कृष्ट उदाहरण प्रस्तुत किया। "
             "कार्यक्रम का सफल संचालन न केवल हिसार पंचनद अध्ययन केंद्र की सक्रिय एवं कर्मठ कार्यकारिणी की दक्षता को प्रदर्शित करता है, "
             "बल्कि यह भी सिद्ध करता है कि समर्पित प्रयासों से किसी भी आयोजन को प्रेरणादायी एवं ऐतिहासिक बनाया जा सकता है।\n\n"
             "इस भव्य एवं सफल आयोजन हेतु हिसार पंचनद अध्ययन केंद्र की समस्त कार्यकारिणी, आयोजक मंडल एवं सहयोगी कार्यकर्ताओं को "
             "हार्दिक बधाई एवं अनंत शुभकामनाएँ। आप सभी का परिश्रम, समन्वय एवं संगठन के प्रति निष्ठा वास्तव में प्रशंसनीय एवं अनुकरणीय है।\n\n"
             "पूर्ण विश्वास है कि भविष्य में भी आप सभी इसी प्रकार राष्ट्र एवं समाजहित में उत्कृष्ट, प्रभावशाली एवं प्रेरणास्पद कार्यक्रमों का "
             "सफल आयोजन करते रहेंगे तथा संगठन को नई ऊँचाइयों तक पहुँचाने में अपना अमूल्य योगदान निरंतर देते रहेंगे।\n\n"
             "पुनः इस यशस्वी एवं गरिमामयी आयोजन के लिए आप सभी को हार्दिक अभिनंदन, शुभकामनाएँ एवं साधुवाद।",
        posted_on=date(2026, 5, 9),
        tag="Event",
    ),
    Post(
        title="31st Annual Panchnad Lecture — Truth of Partition of India",
        body="31वाँ वार्षिक पंचनद व्याख्यान — विषय: 'भारत के विभाजन का सच'. मुख्य अतिथि: पंजाब के राज्यपाल एवं चंडीगढ़ प्रशासक श्री गुलाब चंद कटारिया. "
             "मुख्य वक्ता: श्री प्रशांत पॉल. इस अवसर पर 'विचार प्रवाह' तथा 'Human Values and Rights in Quran' पुस्तकों का विमोचन किया गया. "
             "स्थान: सेक्टर 26, चंडीगढ़.",
        posted_on=date(2025, 1, 5),
        tag="Annual Lecture",
    ),
    Post(
        title="जलती पराली, पर्यावरण, खेती एवं सेहत की बदहाली",
        body="ऑनलाइन गोष्ठी — प्रस्तोता: उमेन्द्र दत्त; अध्यक्षता: प्रो. बृज किशोर कुठियाला. आयोजक: पंचनद अध्ययन केंद्र, पंजाब विश्वविद्यालय चंडीगढ़.",
        posted_on=date(2023, 11, 16),
        tag="Seminar",
    ),
    Post(
        title="भारत के स्वर्णिम इतिहास पर प्रो. महेंद्र सिंह",
        body="विदेशी शक्तियों द्वारा भारत के इतिहास के तथ्यहीन प्रस्तुतीकरण पर लेख का साझा.",
        posted_on=date(2023, 9, 5),
        tag="Article",
    ),
    Post(
        title="श्रद्धांजलि: वीरेश्वर द्विवेदी जी",
        body="राष्ट्रीय स्वयंसेवक संघ के वरिष्ठ प्रचारक एवं राष्ट्रधर्म पत्रिका के पूर्व सम्पादक के निधन पर शोक.",
        posted_on=date(2023, 9, 4),
        tag="Tribute",
    ),
    Post(
        title="अध्ययन केंद्र, हिसार की गतिविधियाँ",
        body="पंचनद शोध संस्थान, अध्ययन केंद्र-हिसार से अद्यतन.",
        posted_on=date(2023, 9, 3),
        tag="Update",
    ),
    Post(
        title="डॉ. कृष्ण गोपाल जी का व्याख्यान",
        body="विषय: प्राचीन भारत में अध्ययन के विविध आयाम.",
        posted_on=date(2023, 2, 18),
        tag="Lecture",
    ),
    Post(
        title="लोकमंथन – 2022 के पूर्व विमर्श",
        body="करनाल में लोकमंथन-2022 के पूर्व विमर्श का आयोजन. लोकमंथन 2022 गुवाहाटी में 21-24 सितम्बर को 'लोकपरम्परा' विषय पर आयोजित हुआ.",
        posted_on=date(2022, 8, 10),
        tag="Event",
    ),
    Post(
        title="वर्तमान संदर्भ में समान नागरिक संहिता का महत्व",
        body="ऑनलाइन मासिक गोष्ठी — आयोजक: पंचनद अध्ययन केंद्र, कुरुक्षेत्र.",
        posted_on=date(2022, 7, 27),
        tag="Seminar",
    ),
    Post(
        title="संयुक्त गोष्ठी — सोलन व शिमला",
        body="अध्ययन केंद्र, सोलन तथा हिमाचल प्रदेश विश्वविद्यालय, शिमला के संयुक्त तत्वाधान में.",
        posted_on=date(2022, 7, 23),
        tag="Seminar",
    ),
]

publications = [
    Publication(
        title="Vichar Pravah (विचार प्रवाह)",
        description="Collection of thought essays published by Panchnad Shodh Sansthan. Released by Punjab Governor Gulab Chand Kataria at the 31st Annual Lecture.",
        year=2025, author_or_editor="Panchnad Shodh Sansthan",
    ),
    Publication(
        title="Human Values and Rights in Quran",
        description="A study on human values and rights as expressed in the Quran. Released at the 31st Annual Panchnad Lecture by Punjab Governor.",
        year=2025, author_or_editor="Panchnad Shodh Sansthan",
    ),
    Publication(
        title="Bharat 2047 — A Collective Vision",
        description="Collective vision of 20 experts covering rural life, global threats, dharma, sanskriti, technology, economics, finance and defence. "
                    "Organized through a unique dialogue by Panchnad Research Institute.",
        year=2022, author_or_editor="Prof. Brij Kishore Kuthiala (Editor)",
    ),
    Publication(
        title="Facts Speak for Themselves",
        description="Field study report on the 1984 anti-Sikh riots — investigative research documenting ground realities.",
        year=1985, author_or_editor="Panchnad Research Institute",
    ),
]

lectures = [
    AnnualLecture(year=2025, speaker="Prashant Paul", topic="Truth of Partition of India"),
    AnnualLecture(year=2008, speaker="Mohan Bhagwat", topic="National security and cultural issues"),
    AnnualLecture(year=2005, speaker="Devinder Swarup", topic="Contemporary national discourse"),
    AnnualLecture(year=2003, speaker="Arun Jaitley", topic="Constitutional law and governance"),
    AnnualLecture(year=2001, speaker="K. P. S. Gill", topic="Internal security challenges"),
    AnnualLecture(year=1999, speaker="K. N. Govindacharya", topic="Socio-political thought"),
    AnnualLecture(year=1997, speaker="Samdong Rinpoche", topic="Tibetan culture and Indian heritage"),
    AnnualLecture(year=1993, speaker="Dr. M. M. Joshi", topic="Education and national identity"),
    AnnualLecture(year=1990, speaker="Justice D. S. Tewatia", topic="Judiciary and constitutional values"),
    AnnualLecture(year=1987, speaker="Lt. Gen. S. K. Sinha", topic="National security perspectives"),
]

gallery_images = [
    GalleryImage(
        title="ई-गोष्ठी: दूसरी लहर उपरांत व तीसरी लहर पूर्व तनाव प्रबंधन",
        description="पंचनद अध्ययन केंद्र, रोहतक नगर। प्रस्तोता: प्रो. प्रोमिला बत्रा प्रभा जी। "
                    "अध्यक्षता: प्रो. बृज किशोर कुठियाला जी। निर्देशक: डॉ कृष्ण चंद पांडे जी।",
        event_date=date(2021, 6, 19),
        image_filename="event_rohtak_jun19.jpg",
        centre="पंचनद अध्ययन केंद्र, रोहतक",
    ),
    GalleryImage(
        title="ई-गोष्ठी: कोविड-19 से उत्पन्न समस्याओं का योग से निदान",
        description="अंतरराष्ट्रीय योग दिवस पर आयोजित। प्रस्तोता: प्रो. कृष्ण सिंह आर्य जी, डॉ मेहर सिंह देसवाल जी। "
                    "अध्यक्षता: प्रो. बृज किशोर कुठियाला। निर्देशक: डॉ कृष्ण चंद पांडे जी।",
        event_date=date(2021, 6, 21),
        image_filename="event_yogday_jun21.jpg",
        centre="पंचनद शोध संस्थान",
    ),
    GalleryImage(
        title="Webinar: Psychological Aspect of Media Coverage During Covid Epidemic",
        description="Panchnad Research Institute, Study Centre Amritsar. Speaker: Professor Davinder Singh. "
                    "Presided by Prof. B.K. Kuthiala, President PRI.",
        event_date=date(2021, 6, 27),
        image_filename="event_amritsar_jun27.jpg",
        centre="Study Centre, Amritsar",
    ),
    GalleryImage(
        title="ई-गोष्ठी: बंगाल चुनाव परिणाम के बाद उपजी हिंसा",
        description="दक्षिण दिल्ली अध्ययन केन्द्र द्वारा आयोजित। प्रस्तोता: श्री विनोद दिवाकर (अपर महाधिवक्ता, सर्वोच्च न्यायालय)। "
                    "अध्यक्षता: डा. कृष्ण चन्द्र पाण्डे (निदेशक, पंचनद शोध संस्थान)।",
        event_date=date(2021, 6, 28),
        image_filename="event_delhi_jun28.jpg",
        centre="दक्षिण दिल्ली अध्ययन केन्द्र",
    ),
    GalleryImage(
        title="ई-गोष्ठी: ध्यान के माध्यम से क्रोध पर नियंत्रण",
        description="पंचनद अध्ययन केंद्र, रोहतक नगर एवं साइंस ऑफ स्पिरिचूऐलिटी द्वारा संयुक्त आयोजन। "
                    "प्रस्तोता: डॉ. नीतू अर्नेजा (मैत्रेयी कॉलेज, दिल्ली विश्वविद्यालय)। अध्यक्षता: प्रो. कृष्ण सिंह आर्य जी।",
        event_date=date(2021, 10, 31),
        image_filename="event_rohtak_oct31.jpg",
        centre="पंचनद अध्ययन केंद्र, रोहतक",
    ),
]

with Session(engine) as s:
    s.add(admin)
    for item in centres + people + posts + publications + lectures + gallery_images:
        s.add(item)
    s.commit()

print("Database seeded successfully!")
print("Admin login: username=admin, password=panchnad2025")
