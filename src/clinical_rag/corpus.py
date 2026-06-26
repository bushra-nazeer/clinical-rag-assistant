"""Self-contained clinical reference corpus + a retrieval QA evaluation set.

General, public medical-reference knowledge (no PHI). This stands in for what
would be an indexed corpus of clinical guidelines / literature in production.
For educational/demo use only — not medical advice.
"""

from __future__ import annotations

CORPUS: list[dict] = [
    {"doc_id": "DM-DX", "title": "Type 2 Diabetes — Diagnosis", "topic": "diabetes",
     "text": "Type 2 diabetes is diagnosed by a fasting plasma glucose of 126 mg/dL or higher, "
             "an A1C of 6.5% or higher, or a 2-hour plasma glucose of 200 mg/dL or higher during "
             "an oral glucose tolerance test. Results should be confirmed by repeat testing."},
    {"doc_id": "DM-MGMT", "title": "Type 2 Diabetes — Management", "topic": "diabetes",
     "text": "First-line pharmacologic therapy for type 2 diabetes is metformin, alongside lifestyle "
             "modification. The general A1C target for many non-pregnant adults is below 7%. Therapy is "
             "intensified with additional agents such as GLP-1 receptor agonists or SGLT2 inhibitors when "
             "glycemic goals are not met."},
    {"doc_id": "DM-A1C", "title": "Interpreting A1C", "topic": "diabetes",
     "text": "Hemoglobin A1C reflects average blood glucose over roughly three months. An A1C below 5.7% is "
             "normal, 5.7% to 6.4% indicates prediabetes, and 6.5% or higher is consistent with diabetes."},
    {"doc_id": "HTN-BP", "title": "Hypertension — Blood Pressure Thresholds", "topic": "hypertension",
     "text": "Normal blood pressure is below 120/80 mmHg. Elevated is 120-129 systolic and below 80 diastolic. "
             "Stage 1 hypertension is 130-139/80-89 mmHg, and stage 2 is 140/90 mmHg or higher."},
    {"doc_id": "HTN-MGMT", "title": "Hypertension — Management", "topic": "hypertension",
     "text": "Initial antihypertensive options include thiazide diuretics, ACE inhibitors such as lisinopril, "
             "ARBs, and calcium channel blockers. Lifestyle changes — reduced sodium, weight loss, and exercise — "
             "are recommended for all patients."},
    {"doc_id": "ASTHMA", "title": "Asthma — Overview", "topic": "asthma",
     "text": "Asthma is a chronic inflammatory airway disease causing wheezing, cough, and shortness of breath. "
             "Short-acting beta agonists such as albuterol relieve acute symptoms; inhaled corticosteroids are "
             "the mainstay of long-term control."},
    {"doc_id": "LIPID", "title": "Hyperlipidemia and Statins", "topic": "hyperlipidemia",
     "text": "Statins such as atorvastatin lower LDL cholesterol and reduce cardiovascular risk. High-intensity "
             "statin therapy is recommended for patients with established atherosclerotic cardiovascular disease."},
    {"doc_id": "UTI", "title": "Urinary Tract Infection", "topic": "uti",
     "text": "Uncomplicated urinary tract infections present with dysuria, urinary frequency, and urgency. "
             "First-line treatment is typically nitrofurantoin or trimethoprim-sulfamethoxazole, guided by local "
             "resistance patterns."},
    {"doc_id": "GERD", "title": "Gastro-esophageal Reflux Disease", "topic": "gerd",
     "text": "GERD causes heartburn and regurgitation from reflux of stomach contents. Management includes weight "
             "loss, avoiding trigger foods, and acid suppression with proton pump inhibitors such as omeprazole."},
    {"doc_id": "ANX", "title": "Generalized Anxiety Disorder", "topic": "anxiety",
     "text": "Generalized anxiety disorder involves excessive, difficult-to-control worry. First-line treatments "
             "are cognitive behavioral therapy and SSRIs or SNRIs such as sertraline or venlafaxine."},
    {"doc_id": "CAD", "title": "Coronary Artery Disease", "topic": "cardiac",
     "text": "Coronary artery disease results from atherosclerotic narrowing of the coronary arteries. Management "
             "includes antiplatelet therapy with aspirin, high-intensity statins, blood-pressure control, and "
             "risk-factor modification."},
    {"doc_id": "CHESTPAIN", "title": "Acute Chest Pain Evaluation", "topic": "cardiac",
     "text": "Acute chest pain requires prompt evaluation for life-threatening causes. An electrocardiogram and "
             "cardiac troponin are obtained early to assess for acute coronary syndrome."},
    {"doc_id": "OBESITY", "title": "Obesity", "topic": "obesity",
     "text": "Obesity is defined as a body mass index of 30 kg/m2 or higher. Management combines dietary change, "
             "physical activity, behavioral therapy, and, when indicated, pharmacotherapy or bariatric surgery."},
    {"doc_id": "PNA", "title": "Community-Acquired Pneumonia", "topic": "respiratory",
     "text": "Community-acquired pneumonia presents with cough, fever, and an infiltrate on chest radiograph. "
             "Outpatient treatment for previously healthy patients is often amoxicillin or a macrolide."},
    {"doc_id": "OA", "title": "Osteoarthritis of the Knee", "topic": "musculoskeletal",
     "text": "Knee osteoarthritis causes joint pain worse with activity. Management includes exercise, weight loss, "
             "topical or oral NSAIDs, and physical therapy; joint replacement is considered for advanced disease."},
    {"doc_id": "OSA", "title": "Obstructive Sleep Apnea", "topic": "sleep",
     "text": "Obstructive sleep apnea causes repeated airway collapse during sleep, leading to snoring and daytime "
             "sleepiness. Diagnosis is by sleep study; continuous positive airway pressure (CPAP) is first-line therapy."},
]

QA_EVAL: list[dict] = [
    {"question": "What is the first-line medication for type 2 diabetes?", "relevant_doc_ids": ["DM-MGMT"]},
    {"question": "What A1C level confirms a diagnosis of diabetes?", "relevant_doc_ids": ["DM-DX", "DM-A1C"]},
    {"question": "What blood pressure is considered stage 2 hypertension?", "relevant_doc_ids": ["HTN-BP"]},
    {"question": "Which medications treat high blood pressure?", "relevant_doc_ids": ["HTN-MGMT"]},
    {"question": "How is asthma controlled long term?", "relevant_doc_ids": ["ASTHMA"]},
    {"question": "What lowers LDL cholesterol and cardiovascular risk?", "relevant_doc_ids": ["LIPID"]},
    {"question": "How is a urinary tract infection treated?", "relevant_doc_ids": ["UTI"]},
    {"question": "What is first-line therapy for obstructive sleep apnea?", "relevant_doc_ids": ["OSA"]},
    {"question": "What tests are done for acute chest pain?", "relevant_doc_ids": ["CHESTPAIN"]},
    {"question": "How is GERD managed?", "relevant_doc_ids": ["GERD"]},
]
