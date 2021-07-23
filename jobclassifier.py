import pandas as pd
import numpy as np
from pandas import DataFrame
import nltk

nltk.download('punkt')
import matplotlib.pyplot as plt
import spacy
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
import fr_core_news_md
import en_core_web_md
import re

pd.set_option('display.max_rows', 100000)

Listofposts = ["Stagiaire Conseil (H/F)", "Stagiaire SI Audit IT (H/F)",
               "Stagiaire Master RH - recrutement et animation communauté des coachs", "Gestionnaire de saisie (H/F)",
               "Stagiaire d'été - Développeur mobile", 'Chargé Service Client', "Maintenance Technician Japan",
               'Data Scientist',
               'Développeur fullstack', 'Product Manager', 'Développeur Full Stack / intégration partenaires',
               'Chef de projet confirmé segment MID', 'Stagiaire Digital Advertising', 'QA manager',
               'Account Executive Senior', 'Ingénieur d’Affaires Senior', 'Ingénieur Commercial Senior',
               'Support Clients Hispanophone', 'Support Clients Germanophone',
               'Inside Sales Representative Hispanophone', 'Business Development Representative ES/DE',
               'Account Executive Mid-Market', 'Développeur Mobile Senior',
               'Finance Project Manager', 'Business Process Engineer', 'Senior HR Officer', 'Senior HR Officer',
               'Senior HR Officer', 'Business Process Engineer', 'Corporate Finance and Treasury Analyst',
               'Corporate Finance and Treasury Analyst', 'Corporate Finance and Treasury Analyst',
               'Corporate Financial Analyst', 'Financial Business Analyst', 'Digital Marketing Officer',
               'Technical Group Financial Controller', 'Corporate Financial Analyst', 'Network Engineer (M/F)',
               'Data Engineer (M/F)', 'Product Owner M/F', 'Project Manager IT (M/F)', 'Business analyst M/F',
               'Back-end Developer', 'Chef de projet', 'CHEF DE PROJET DÉPLOIEMENT FTTH',
               'Chef de Projet Infrastructure', 'Conducteur de travaux FTTH', 'Data Engineer', 'Développeur Back-End',
               'Développeur Java Full-Stack', 'Ingénieur DEVOPS', 'INGÉNIEUR FTTH', 'Junior Developer',
               'Leader Technique',
               'Social and Media Manager', 'Stage : Chef de Projet Déploiement Réseau Mobile .', 'Technical Leader',
               'Technicien FTTH', 'Campus Recruitment Coordinator', 'Talent Acquisition Specialist',
               'Deputy Payroll Manager', 'Business Analyst/AMOA', 'Chef de Projet Infrastructure',
               'CHEF DE PROJET RADIO', 'CONDUCTEUR DE TRAVAUX RADIO',
               'Développeur C#', 'Développeur Cobol', 'Développeur Java', 'Développeur Mobile',
               'Devops consultant (M/F)', 'INGENIEUR RADIO', 'Ingénieur Système', 'Java Consultant (M/F)',
               'Java SE Developer', 'Junior trade marketing Consultant', 'Microsoft Consultant (M/F)',
               'Exploitation engineer L2 (M/F)', 'React JS developer', 'Sysops and cloud engineer (M/F)',
               'Business Developer', 'Business Developer', 'Business Developer', 'Business Developer', 'Manager',
               'Manager', 'Manager', 'Manager', 'Manager', 'Manager', 'Manager', 'Manager - HEMA', 'Manager - HEMA',
               'Manager - Portalia', 'Manager - Portalia', 'Solutions Sales Manager', 'Responsable Marketing',
               'Junior Legal Counsel (CDD)', 'Account Manager B2B Senior', 'Strategic & Branding Marketing Intern',
               'Bras Droit Sales Team Lead', 'Account Executive', "Commercial B2B - Account Manager en Start-up (H/F)",
               'Customer Success Manager', 'Network Account Executive', 'Sales Development Representative',
               'Senior Backend Developer', 'Head of Marketing France - Nantes', 'Mobile Developer - Paris',
               'Mobile Developer - Nantes', 'Head of Marketing France - Paris', 'Senior Backend Developper',
               'Full-Stack Developer - Paris', 'Growth Engineer', 'Stagiaire Business Consulting', 'Manager Data',
               'Jeune Docteur - Data', 'Data Engineer', 'Consultant(e) Confirmé(e) & Senior Data Science',
               "Architecte d'Entreprise (F/M)", 'Consultant(e) Technique Confirmé(e) & Senior Adobe Campaign',
               'Senior Manager (F/M) – Secteur Energie & Utilities', 'Senior Manager (F/M) – Secteur Industrie',
               'Senior Manager (F/M) – Secteur Public', 'Manager BI/Big Data (F/M)',
               'Senior Manager Stratégie Marketing (F/M)',
               'Senior Manager Organisation & Change (F/M)', 'Senior Manager Data Gouvernance (F/M)',
               'Consultant(e) Confirmé(e) & Senior Data Gouvernance / PO Data',
               'Senior Manager Transformation Digitale (F/M)',
               'Manager BI/Big Data (F/M)', 'Consultant(e) Confirmé(e) & Senior Salesforce',
               'Consultant(e) Technique Confirmé(e) & Senior Digital', 'Consultant(e) Gestionnaire de campagnes CRM',
               'Consultant(e) Confirmé(e) & Senior Business Consulting', 'Consultant Data (Stage)',
               'Consultant Data (CDI)',
               'Consultant Digital/Data Senior (CDI)', 'Consultant Digital/Data (CDI)',
               'Consultant Digital/Data (stage)',
               'Junior JS fullstack developer (internship)', 'Web designer / Graphiste', 'Stage - Marketing Digital',
               'Technicien réseau et supervision- Amiens H/F', "Ingénieur d'Affaires H/F",
               'Technicien de déploiement H/F', 'Technicien de maintenance et support utilisateurs N1 H/F',
               'Business Developer Strategic Alliances (H/F)', 'Directeur Commercial - CDI (H/F)',
               'Business Developer (H/F) - Moscou, Ukraine et pays de la CEI',
               'directeur', 'Director of Engineering - Payment/Fraud', 'Legal Manager & DPO', 'Legal Officer',
               'Industrial Digitalization Engineer (H/F)', 'Energy Efficiency Expert in Industry (H/F)', 'CFO',
               "COMMERCIAL LOGISTIQUE ZONE ASIE F/H"
               'Customer Advisor & CRM ',
               'Product Owner', 'Directeur de Projets', 'Directeur.trice Artistique Social Media Junior',
               'DIRECTEUR DE MISSION F/H', "juridique", "advocate", "webmarketing", "writer", "recruitement",
               "acquisition", "coaching",
               "Conseiller Clientèle H/F", "Conseiller de vente (H/F)", "Gestionnaire Trésorerie - Nantes (h/f)",
               "Assistant Comptabilité – Administratif - Financier", "formateur", "recruit",
               "Avocat(e) au sein du département social", "Assistant Business Developer F/H",
               "Assistant(e) commerciale H/F ANGLAIS", "coordinateur", "Marketing Analyst Intern H/F",
               'Marketing & Communication Intern - EdTech',
               'Bras droit CEO / COO', "Conducteur"
                                       'Partnerships & Alliances - Internship', 'Project Manager', 'Head of Product',
               'Senior Data Engineer',
               'Senior Account Executive - DACH', 'Account Executive SMB', 'Business Development Representative - DACH',
               'Customer Success Manager - EMEA', 'Senior Customer Success Manager - DACH & EMEA',
               'Solutions Engineer - DACH',
               'Senior Software Engineer - Distributed Systems', 'Tech Lead Front-end - DX Chapter',
               'Enterprise Account Executive - Netherlands', 'Enterprise Account Executive - Nordics',
               'Order Managment & Deal Desk Specialist', 'Senior Account Executive - Pacific Time Zone',
               "Alternant Commerce", "E-commerce specialist", "Expert commercetools h/f",
               'Senior Cloud Engineer - SRE', 'Senior Machine Learning Engineer',
               'Junior Frontend Software engineer - Dashboard Squad', 'Junior Software engineer - Dashboard Squad',
               'Technical Writer - DX Chapter', 'Recruiting Coordinator Intern - EMEA',
               'Business Development Representative - France', 'Business Development Representative - UK & Ireland',
               'Account Executive SMB', 'Customer Intelligence Intern', 'Partner Account Manager UK & Ireland',
               'Senior Cloud Engineer Azure - SRE', 'Partner Account Manager South EMEA',
               'Demo Engineering Internship EMEA',
               'Developer Support Engineer - EMEA', 'Senior NLP / ML Engineer - Team Lead',
               'Enterprise Account Executive - Central & Eastern Europe', 'Partner Solutions Engineer - EMEA',
               'Technical Account Manager - EMEA', 'Product Designer', 'Senior User Researcher - EMEA',
               'Enterprise Account Executive - Italy', 'Sales Development Representative - DACH',
               'SOFTWARE ENGINEER FULLSTACK JS', 'RESPONSABLE MARKETING', 'Senior Customer Success Manager (F/H)',
               'Alternance - Coordinateur Supply Chain H/F', 'Stage - Coordinateur Transport H/F',
               'Stage - Chargé.e de communication digitale', 'Alternance - UX/UI Designer H/F',
               'Stage - Assistant.e Achat', 'Responsable media'
                                            'Alternance - Assistant Achat F/H', 'Key Account Manager F/H H/F',
               'Developpeur PHP/Symfony [B2B / B2C] H/F',
               'Developpeur PHP fullstack Symfony & VueJS [Data Intelligence] – H/F', "legal",
               'Dev fullstack Senior Symfony & VueJS [ projet Saas] (H/F)', 'Consultant(e) Data Marketing',
               'Consultant(e) Marketing', 'Data scientist – Jeune docteur - Projet Innerve (H/F)',
               'Data Product Owner - SENIOR (F/H) - CDI', 'Data scientist – Jeune docteur - Projet SimAI (H/F) - CDI',
               'Data Scientist - Computer Vision - SENIOR (H/F) - CDI', 'Business Developer (H/F) - CDI',
               'Solution Architect (H/F) - CDI', 'Data Scientist - Time Series - SENIOR (H/F) - CDI',
               'Data Scientist - NLP - Confirmé (H/F) - CDI', 'Consultant en stratégie Data - SENIOR (H/F) - CDI',
               'Data Software Engineer - CONFIRME (H/F) - CDI', 'Chargé(e) de communication digitale Stage (H/F)',
               'Business Developper en stage H/F', 'Senior Full Stack Software Engineer - Fraud Detection App',
               'Senior Fullstack Developer', 'Senior Front-end Developer - Claim automation',
               "Commercial Marketing Digital",
               'Senior Developer Data Platform', "Legal Counsel (H/F)", "Legal Intern",
               'Full Stack Software Engineer - Fraud Detection App', 'Engineering Manager',
               'Communications/Social Media Intern', "Conseiller Clientèle Senior (H/F)",
               'Salesforce CRM Lead', 'Développeur/euse FullStack Expérimenté/ée (VueJS / NodeJS)',
               'Customer Success/Project Manager', 'Office Manager', 'Consultant Optimisation & Logistique',
               'Lead Dev Front ReactJS', 'Growth Marketing Product (H/F)', 'Chief Operating Officer (H/F)',
               'Data Analyst (H/F)', "Consultant en recrutement F/H",
               'Data Engineer (H/F)', 'SDR / Business Developer Spain (H/F)', 'Key Account Executive Spain (H/F)',
               'Business Development Representative Spain (H/F)', 'Head of Business Strategy (H/F)',
               'Robotics Engineer (H/F)', "Conseiller Clientèle Technique H/F - Nevers",
               'Key Account Executive (H/F)', 'Business Development Representative EN/FR (H/F)',
               'Warehouse Launcher (H/F)',
               'Lead Developer (H/F)', 'Software Engineer (H/F)', 'DevOps Engineer (H/F)',
               'Product Manager Robotics (H/F)',
               'Senior Product Manager (H/F)', 'Product Manager (H/F)', 'Talent Acquisition IT (H/F)',
               'Stage Data Analyst (H/F)',
               'Business Developer', 'Marketing Director', 'VP Engineering', 'Product Director', 'Product Manager',
               'Product Designer', 'Fullstack Developer - (Rails / React)', 'Backend Engineer',
               '(Lead) DevOps x Back-end Engineer', 'Business Development Representative - BDR (Europe)',
               "Commercial Grands Comptes",
               'Customer Onboarding Manager', 'Brand Marketing Manager', 'Chief of Staff', 'VP Sales',
               'Technicien de maintenance et support utilisateurs H/F',
               'Technicien SAV maintenance Informatique et Multimédia -Chatillon H/F',
               'Technicien helpdesk - Alternance- Noisy-le-Grand H/F', 'Technicien Déploiement H/F',
               "Négociateur location H/F", "Négociateur en immobilier H/F - Paris",
               'Technicien Data Center H/F',
               'Administrateur Base de données (H/F)', 'Technicien de support de proximité VIP H/F',
               'Techniciens de Support Qualité N2 - N3 H/F',
               'Technicien de maintenance et support utilisateurs VIP H/F',
               'Gestionnaire de parc informatique H/F',
               'Techniciens Helpdesk Trilingue ALLEMAND / ANGLAIS / FRANCAIS H/F',
               "Commercial Expert Crédit - Paris (CDI)",
               'Technicien Service Desk Trilingue Anglais/Allemand H/F', 'Technicien de supervision- Grenoble H/F',
               "Logistics Intern", "Marketing Digital - Stage",
               'Technicien de maintenance et support utilisateurs H/F', 'Ingénieur réseau H/F',
               'Ingénieur DevOps (H/F)', "COMMERCIAL SENIOR/SENIOR INSIDE SALES",
               'Technicien déploiement / Responsable Eligibilité / Moyens H/F H/F', 'Ingénieur réseau sécurité H/F',
               'Technicien Helpdesk-Lyon H/F', 'Opérateur Logistique H/F H/F', 'Planificateur H/F H/F',
               'Technicien Déploiement H/F H/F', 'Responsable Planification / Relations sites client H/F H/F',
               'Responsable Qualité / Méthodes / Sécurité H/F H/F', 'Contract Manager en alternance H/F',
               'Technicien de maintenance et support utilisateurs H/F',
               'Technician informatique confirmé / Responsable Préparation / Logistique H/F H/F',
               'Technicien de maintenance et support utilisateurs-Lyon H/F',
               "Commercial chargé de Service Clients (ALTERNANT, F/H)",
               'Techniciens de déploiement et support utilisateurs H/F', 'Technicien de Proximité H/F',
               'Technicien support expérimenté H/F', 'Incident manager H/F',
               'Technicien de maintenance et support utilisateurs H/F', "Planificateur OPC H/F",
               'Team Leader - Coordinateur Référent Projets H/F',
               'Technicien Réseaux et Sécurité H/F', 'Team Leader - Service Desk H/F',
               "Comptabilité - Gestion administrative et RH", "Comptabilité fournisseur / contrôle des achats",
               "Technicien comptabilité F/H - Alternance",
               'Team Leader - Référent Service Administrateur du SIE H/F', "Strategic Project Manager",
               'Team Leader - Référent service communications H/F', "Communication Google Project H/F",
               'Team Leader - Coordinateur Référent Opérations H/F', "Strategic Analyst ", "Strategic Analyst _ stage",
               'Technicien helpdesk H/F', 'Incident Manager H/F', 'Team Leader H/F', 'Technicien helpdesk H/F',
               "Formateur.rice en développement fullstack",
               'Technicien déploiement / Responsable Eligibilité / Moyens H/F H/F',
               'Technicien informatique confirmé / Responsable Préparation / Logistique H/F H/F', "formateur fullstack",
               "Formateur équipe commerciale H/F", "Formateur.trice en entrepreneuriat - Abidjan",
               "Formateur Développeur JS et/ou PHP - Nantes (H/F)",
               'Conseiller Support Technique- Issy-les-Moulineaux H/F',
               "Chargé communication & contenu / Chargé contenu et évènementiel", "Consultant Marketing Digital",
               'Technicien de maintenance et support utilisateurs- Paris 7 H/F',
               "Assistant achats et approvisionnement (H/F)",
               'Technicien de supervision (nuit)- Grenoble-H/F', "Recruitment Intern", "Commercial H/F"
                                                                                       'Technicien de maintenance et support utilisateurs H/F',
               "Consultant Achats IT", "Assistant Achats et Qualité",
               "chargé achats, logistique informatique (H/F) - Paris",
               'Technicien SAV maintenance Informatique et Multimédia -Chatillon H/F',
               'Technicien helpdesk - Alternance- Noisy-le-Grand H/F', 'Technicien Déploiement H/F',
               "responsable juridique plateforme culturelle", "Juriste - Animateur réseau d'avocats - STAGE",
               'Technicien Data Center H/F', 'Administrateur Base de données (H/F)', 'Entrepreneur-Consultant Senior',
               'Technicien de support de proximité VIP H/F', "Gestionnaire ADV",
               "Gestionnaire - Administration des Ventes (H/F)", "Gestionnaire Administration du Personnel (H/F)",
               'Techniciens de Support Qualité N2 - N3 H/F', 'Product Owner (H/F)',
               'Product owner - chef de projet agile', 'PRODUCT OWNER MARKETPLACE FINANCE F/H',
               "Assistant juridique H/F", "Responsable Juridique IT - H/F", "Collaborateur juridique H/F",
               'Technicien de maintenance et support utilisateurs VIP H/F', 'Formateur.rice en entrepreneuriat',
               "ASSISTANT RESSOURCES HUMAINES H/F",
               'Head of Finance - Q-Commerce', 'Head of HR / Directeur(ice) des ressources humaines',
               'Gestionnaire de parc informatique H/F', 'Chef de projet logiciel (H/F)',
               'Chef de Projet Marketing - Software & Data (H/F)', "Gestionnaire Administration du Personnel (H/F)",
               "Gestionnaire administratif et achats - F/H",
               'Techniciens Helpdesk Trilingue ALLEMAND / ANGLAIS / FRANCAIS H/F', "Human Resources Intern",
               'CFO / Directeur Administratif et Financier H/F', "Acquisition Specialist",
               "Acquisition & Traffic Manager", "Stagiaire ressources humaines", "Alternant Ressources Humaines", ""
                                                                                                                  'Technicien Service Desk Trilingue Anglais/Allemand H/F',
               'Technicien de supervision- Grenoble H/F',
               'Technicien de maintenance et support utilisateurs H/F', 'Ingénieur réseau H/F', "ERP Consultant - Brno",
               'Ingénieur DevOps (H/F)', 'Chef de Projet Dataviz', 'Chef(fe) de projet Innovation Données',
               "Coordinateur des opérations",
               'Assistant recrutement (H/F)', "GESTIONNAIRE DE PROJET WEB",
               "Consultant en Talent Management & Human Ressources H/F - People & Strategy",
               'Ingénieur réseau sécurité H/F', 'Technicien Helpdesk-Lyon H/F', 'Planificateur H/F H/F',
               "Technical Writer", 'Conseiller de Vente (H/F)', "Trésorier (H/F)",
               'Contrôleur/se de gestion et trésorier/re (H/F)', 'Comptable H/F - CDD (18 mois)',
               "Chargé de trésorerie F/H",
               'Business Developer - Entrepreneur - Santé [Paris] H/F', 'Consultant entrepreneur',
               'Assistant origination',
               'Technicien Déploiement H/F H/F', 'Project Management Officer (H/F)', 'Vice President, Growth Marketing',
               "Web Marketing e-commerce", "Recruiting Intern", "Talent Acquisition Partner - Business UK",
               "Marketing Digital",
               'Responsable Planification / Relations sites client H/F H/F', "Stage Recrutement Chasseur de Talents",
               "HR Intern", "rh",
               'Product Manager & futur entrepreneur ou associé de Wivoo H/F', "Assistante de Gestion h/f",
               "Assistant RH (H/F) en alternance", "Intégrateur ERP H/F",
               'Co-founder Growth & Operations Entrepreneur', 'Responsable Qualité / Méthodes / Sécurité H/F H/F',
               "E-Commerce Consultant High Tech (H/F)", "Commercial Marketing Digital",
               'Lead Developer Web', 'COMPTABLE GENERAL F/H', 'Executive Assistant of the CEO', 'CFO', "Commercial B2B",
               "Human Resources"
               'Contract Manager en alternance H/F', "Recruitment Intern", "Conseiller.e Clientele Essentiel",
               "Logistics / Supply Chain Manager (CDI)", "Planificateur H/F",
               'Technicien de maintenance et support utilisateurs H/F', "Responsable Recrutement",
               "Consultant Recrutement Juridique et Fiscal H/F",
               "Commercial Grands Comptes / Consultant Marketing Digital (h/f)",
               'Technicien de maintenance et support utilisateurs-Lyon H/F', 'Contract Manager - Dijon H/F',
               "COMMERCIAL LOGISTIQUE ", "Human Resources Manager", 'Assistant Achats',
               "Conseiller en conduite de projets et organisation, Accompagnateur Agile - Insee H", "Avant-vente (H/f)",
               "CONSEILLER DE VENTE CDD - TOULOUSE H/F"
               ]

df = DataFrame(set(Listofposts), columns=['headline'])
set(Listofposts)

production = ["microsoft", "Engineering", "développeur", "techniciens", "expert", "technique", "ingénieur", "editor",
              "projets",
              "scientist", "product", "enginnering", "computer", "website", "programmer", "bi", "statistiques",
              "ingenieure", "engeneering", "concepteur", "dev", "mobile", "graphiste", "developpements", "deploiement",
              "logiciel", "webanalytics", "react", "node", "flask", "ingenieurs", "chain", "net", "adobe", "graphisme",
              "mathematics", "mathematician", "chefs", "spring", "jee", "automatisation", "robotics", 'warehouse',
              "digital/data", "ui", "salesforce", "adobe", "network", "technicienne", "android", "java", "systems",
              "system", "r", "system", "graphiste", "iot", "telecoms", "dotnet", "tests", "cybersecurity", "webmaster",
              "Ingénieur", "Front-end", "tech", "réseau", "donnees", "base", "graphiste", "webdesigner", "systeme",
              "project", "informatique", "mathematiques", "security", "crm", "sql", "database", "ingenierie",
              "technicien", "technician", "software", "freelancer", "analyst", "devops", "developpement", "projet",
              "maintenance"
              "conception", "nlg", "controleur", "scrum", "scrummaster", "datascience", "reseau", "securite",
              "artificial", "intelligence", "control", "cloud", "engineer", "data", "ingenieur", "reseaux",
              "projectmanager", "data", "engineer", "web", "ia", "deep", "analytics", "cybersecurite", "roboticien",
              "roboticist", "cyber", "machinelearning", "integrateur", "machine", "learning", "nlp", "architect", "ml",
              "designer", "design", "controller", "testeur", "tester", "developper", "developpeuse", "statisticienne",
              "statisticien", "test", "developer", "developpeur", "analysis", "full", "development", "fullstack",
              "developpements", "researcher", "frontend", "deploiement", "back", "end", "front", "backend", "back-end",
              "web", "analyste", 'engineering', "consultant", 'consultante', 'consulting', 'conseil', "cybersecurity", ]

support = ["legal", "advisor", "media,""officer", "office", "commercial", "gestion", "recrutement", "achat", "achats",
           "juridique", "advocate", "webmarketing", "writer", "recruitement", "acquisition", "coaching", "clientele",
           "vente", "departement", "tresoriere", "talents", "comptabilite", "formateur", "recruit", "droit", "advocate",
           "assistant", "assistante", "coordinateur", "avocate", "avocat", "officer", "application", "associate",
           "cordonnateur", "finances", "communication", "communications", "strategic", "strategy", "purchase",
           "purchasing", "ecommerce", "commerce", "account", "negociateur", "lawyer", 'media', "ventes", "negotiator",
           "cci", "financiers", "financial", "financier", "relation", "sales", "ressources", "humaines", "finance",
           "customer", "product", "vp", "commercial", "commerciale", "planning", "strategical", "strategie",
           "interviewer", "erp", "rp", "sirh", "comptable", "coordinator", "coach", "advisory", "responsable",
           "resources", "human", "support", "rh", "hr", "cpo", "talent", "recruiting", "recruteur", "recrute",
           "recruiter", "chro", "planificateur", "secretaire", "treasurer", "organisateur", "organizer", "secretary",
           "relations", "clients", "comercial", "event", "planneur", "planner", "strategique", "recruitment",
           "logistics", "logistique", "marketing", 'client', "gestionnaire"]

management = ["head", "responsable", "architecte", "owner", "Leader", "entrepreneur", "entrepreneur-consultant",
              "chief", "chef",
              "management", "managment", "manager", "presidente", "principal", "direction", "cco", "dirigeante",
              "administrative", "dirigeant", "executive", "gerant", "gerante", "directrice", "chairman", "president",
              "cofounder", "manager", "leader", "investisseur", "pdg", "ceo", "cto", "directeur", "coo", "cfo", "cio",
              "cmo", "chief", "director", "founder", "funding", "fondateur", "founding", "co"]


def get_class(prod, manag, supp):
    if prod == 0 and manag == 0 and supp == 0:
        return "other"
    if (manag > 0):
        return "management"
    if (supp > prod and supp > manag) or (supp == prod):
        return "support"
    if prod > manag and prod > supp:
        return "production"


def fillClass(headline):
    tok_headline = nltk.word_tokenize(headline)
    nb_prod = 0
    nb_manag = 0
    nb_supp = 0

    for word in tok_headline:
        if word.lower() in production:
            nb_prod = nb_prod + 1
        if word.lower() in management:
            nb_manag = nb_manag + 1
        if word.lower() in support:
            nb_supp = nb_supp + 1
    try:
        pour_prod = float(nb_prod / (nb_manag + nb_supp + nb_prod)) * 100
    except:
        pour_prod = float(0)
    try:
        pour_manag = float(nb_manag / (nb_manag + nb_supp + nb_prod)) * 100
    except:
        pour_manag = float(0)
    try:
        pour_supp = float(nb_supp / (nb_manag + nb_supp + nb_prod)) * 100
    except:
        pour_supp = float(0)

    return pour_prod, pour_manag, pour_supp, get_class(pour_prod, pour_manag, pour_supp)


def apply_and_concat(dataframe, field, func, column_names):
    return pd.concat((
        dataframe,
        dataframe[field].apply(
            lambda cell: pd.Series(func(cell), index=column_names))), axis=1)


df2 = apply_and_concat(df, 'headline', fillClass,
                       ['pourcentage_production', 'pourcentage_management', 'pourcentage_support', 'class'])

from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0
detect('Entrepreneur-Consultant Senior')

nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()

nlpf = fr_core_news_md.load()
stopf = stopwords.words('french')

nlpa = en_core_web_md.load()
stopa = stopwords.words('english')


def preprocess(comment):
    try:
        comment = comment.lower()
        if detect(comment) == 'fr':
            comment = nlpf(comment)
            lemmatized = list()
            for word in comment:
                if len(word) > 3 and str(word) not in stopf and str(word) not in ['H/F', 'M/F', '(M/F)', '(H/F)']:
                    lemma = word.lemma_
                    if lemma:
                        lemmatized.append(lemma)

            return " ".join(lemmatized)
        else:
            comment = nlpa(comment)
            lemmatized = list()
            for word in comment:
                if len(word) > 3 and str(word) not in stopa:
                    lemma = word.lemma_
                    if lemma:
                        lemmatized.append(lemma)

            return " ".join(lemmatized)
    except:
        pass


df2['headline'] = df2['headline'].map(lambda s: preprocess(s))
df2

df_other = df2['class'] == 'other'
filtered_df = df[df_other]
filtered_df

df2 = df2.dropna()

df2

plt.figure(figsize=(80, 60))
df2[['headline', 'class']].groupby('class').count().plot.bar(ylim=0)
plt.show()

df2.loc[df2['class'] == "other"].count()

from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score, plot_confusion_matrix
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn import metrics

classes = ['management', 'other', 'production', 'support']
X = df2['headline']
y = df2['class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=True, random_state=42)
weights = compute_sample_weight("balanced", y_train)

y_test

# Approach 1: Naive Bayes classifier for multinomial models

nb = Pipeline([('vect', CountVectorizer()),
               ('tfidf', TfidfTransformer()),
               ('clf', MultinomialNB()), ])

nb.fit(X_train, y_train, **{'clf__sample_weight': weights})

y_pred = nb.predict(X_test)
print(metrics.classification_report(y_test, y_pred, target_names=classes))
plot_confusion_matrix(nb, X_test, y_test)
plt.show()

# Approach 2: Linear SVM


sgd = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                (
                    'clf',
                    SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None)), ])

sgd.fit(X_train, y_train, **{'clf__sample_weight': weights})

y_pred = sgd.predict(X_test)
print(metrics.classification_report(y_test, y_pred, target_names=classes))

plot_confusion_matrix(sgd, X_test, y_test)
plt.show()

# Approach 3: Logisistic Regression

logreg = Pipeline([('vect', CountVectorizer()),
                   ('tfidf', TfidfTransformer()),
                   ('clf', LogisticRegression(n_jobs=4, C=1e5)),
                   ])
logreg.fit(X_train, y_train, **{'clf__sample_weight': weights})

y_pred = logreg.predict(X_test)

print(metrics.classification_report(y_test, y_pred, target_names=classes))

plot_confusion_matrix(logreg, X_test, y_test)
plt.show()

from gensim.models import word2vec

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


def build_corpus(data):
    "Creates a list of lists containing words from each sentence"
    corpus = []
    for col in data['headline']:
        corpus.append(col)

    return corpus


corpus = build_corpus(df2)
corpus

vectorizer = TfidfVectorizer(min_df=10)
title_tfidf = vectorizer.fit_transform(corpus)
print("Shape of matrix after tfidf ", title_tfidf.shape)

tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
tsne_results = tsne.fit_transform(title_tfidf)

df_tsne = df2['headline'].copy()
df_tsne['tsne-2d-one'] = tsne_results[:, 0]
df_tsne['tsne-2d-two'] = tsne_results[:, 1]

import seaborn as sns

plt.figure(figsize=(16, 10))
sns.scatterplot(x='tsne-2d-one', y='tsne-2d-two', data=df_tsne, alpha=1)

df_tsne['class'] = df2['class']
df_tsne['class']

plt.figure(figsize=(5, 6), frameon=False, dpi=100)
plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
sns.scatterplot(x='tsne-2d-one', y='tsne-2d-two', hue='class', data=df_tsne, alpha=0.7)


def get_result_classification(post):
    r = logreg.predict(pd.Series(post))
    return r[0]
