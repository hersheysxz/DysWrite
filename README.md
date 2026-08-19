# DysWrite
### *A Mobile Application for the Early Detection of Dyslexia Through Handwriting Analysis Using MobileNetV3 Transfer Learning and Explainable AI*

---

## 1. Project Context

*   **Product Name:** **DysWrite**
*   **Academic Institution:** Don Mariano Marcos Memorial State University (DMMMSU) — South La Union Campus (SLUC)
*   **Domain:** Assistive technology for Special Education (SPED); early screening support for developmental dyslexia
*   **Target Users:** Students (children), Teachers, SPED Coordinators, Parents, Administrators
*   **Partner Schools:** Aringay Central Elementary School, Rosario Integrated School, Agoo East Elementary School

---

## 2. System Overview

### The Core Problem
Dyslexia in young learners often goes undetected in classroom settings because screening tools require specialist administration, are time-consuming, and are not readily accessible in most public elementary schools — especially in provincial areas. Teachers and parents typically have no low-cost, immediate way to flag handwriting patterns associated with dyslexia risk (e.g., letter reversals, inconsistent formation) for further professional evaluation.

### The DysWrite Solution
DysWrite is a mobile application that analyzes a child's handwriting sample and classifies it into indicative categories (**Normal**, **Reversal**, **Corrected**) using a deep learning pipeline built on **MobileNetV3** (via transfer learning) combined with a **CNN + Transformer** classification head. To keep the tool trustworthy and interpretable for non-technical users (teachers, parents), every prediction is paired with a **Grad-CAM** explainability overlay that visually highlights which regions of the handwriting influenced the model's decision. The system does not diagnose dyslexia — it provides an accessible, early screening signal to prompt timely referral to a qualified professional.

---

## 3. Data & Model Architecture

### Dataset
| Source | Composition |
|---|---|
| Kaggle Dyslexia Handwriting Dataset | 138,500 samples across **Normal**, **Reversal**, and **Corrected** classes |
| Local test set (2 partner schools) | 10 students, collected for real-world validation |
| Split | 80% training / 20% validation |

### Model Pipeline
```
[ Handwriting Sample (image capture / upload) ]
                  |
                  v
        [ Preprocessing: resize, denoise, normalize ]
                  |
                  v
     [ Feature Extraction — MobileNetV3 (transfer learning) ]
                  |
                  v
   [ Classification — CNN + Transformer head ]
                  |
        +---------+---------+
        |                   |
        v                   v
[ Risk Classification ]  [ Grad-CAM Explanation (XAI) ]
        |                   |
        +---------+---------+
                  v
        [ Compiled Detection Report ]
```

### Development Methodology
The system is developed using **Rapid Application Development (RAD)**, allowing iterative prototyping and feedback cycles with end users (teachers, SPED coordinators, parents) throughout development.

---

## 4. Evaluation Framework

### Functional & Non-Functional Requirements
Gathered from teachers, SPED coordinators, and parent-users at partner schools to define the system's functional scope and quality attributes.

### System Usability Scale (SUS)
End-user respondents evaluate the deployed application using the **System Usability Scale**, providing a standardized usability score to assess ease of use for non-technical users.

### ISO/IEC 25010-Based Quality Evaluation
Software quality (e.g., functional suitability, reliability, usability, performance efficiency) is assessed using a questionnaire structured around the **ISO/IEC 25010** quality model, administered to the same end-user groups.

---

## 5. Repository Diagram Assets

All system design diagrams are located in the `graphs-and-charts/` directory. Detailed explanations of each follow below.

| Diagram Name | Asset Path | Description |
| :--- | :--- | :--- |
| **DFD Stage 0 (Context)** | `graphs-and-charts/01_DFD/S0_DFD.svg` | Context diagram showing the DysWrite system boundary and its four external entities: Student, Teacher, Parent, Admin. |
| **DFD Stage 1** | `graphs-and-charts/01_DFD/S1_DFD.svg` | Decomposes the system into 4 core processes (Manage Accounts, Capture & Preprocess Sample, Run MobileNetV3 Inference & Explanation, Generate Report) and 4 data stores (D1–D4). |
| **DFD Stage 2 (Inference)** | `graphs-and-charts/01_DFD/S2_DFD.svg` | Deep-dive decomposition of Process 3.0 into feature extraction, classification, Grad-CAM explanation, and result compilation (3.1–3.4), with data stores D5–D7. |
| **Structured Chart** | `graphs-and-charts/02_Structured_Chart/Structured_Chart.svg` | Modular program-structure view showing module hierarchy, control flow, and data/control couples. |
| **HIPO VTOC Diagram** | `graphs-and-charts/03_HIPO_Diagram/hipo_vtoc.svg` | Visual Table of Contents mapping hierarchical functional modules, numbered consistently with the DFDs. |
| **HIPO IPO Charts** | `graphs-and-charts/03_HIPO_Diagram/hipo_ipo_charts.md` | Input-Process-Output tables detailing each module's data flow and logic. |
| **Structured English** | `graphs-and-charts/04_Structured_English/` | *(To be added)* Plain-English, controlled-syntax description of each process's logic. |
| **Pseudocode** | `graphs-and-charts/05_Pseudo_Code/` | *(To be added)* Algorithm-level breakdown of each module, based on the Structured English. |
| **Entity-Relationship Diagram (ERD)** | `graphs-and-charts/06_ERD/` | *(To be added)* Database schema in Chen notation covering users, samples, classifications, and reports. |
| **Data Dictionary** | `graphs-and-charts/07_Data_Dictionary/` | *(To be added)* Definitions of all data elements used across the DFDs and ERD. |

---

### 5.1 DFD — Data Flow Diagrams

Data Flow Diagrams model how information moves through the DysWrite system, without describing program structure or timing. Three levels of increasing detail are provided.

**Stage 0 — Context Diagram (`S0_DFD.svg`)**

Establishes the system boundary — DysWrite is drawn as a single process ("Process 0") surrounded by the four external entities it exchanges data with. The center circle represents the entire system; each surrounding rectangle is an external entity outside the system's control; arrows show data flowing in and out.

| Entity | Data → System | Data ← System |
|---|---|---|
| **Student** | Login, handwriting sample | Writing task, instructions |
| **Teacher** | Student samples, requests | Detection results, reports |
| **Parent** | Consent, login credentials | Result notification |
| **Admin** | Account, model config | System logs, model reports |

This is the highest level of abstraction — it answers "what talks to the system?" without revealing anything about internal logic.

**Stage 1 — Level 1 DFD (`S1_DFD.svg`)**

Opens up Process 0 into its four major internal processes, showing how data is passed between them and stored:

1. **1.0 Manage Accounts** — Validates and stores account/login data. Reads and writes **D1 Accounts**. Triggered by Admin's account setup requests.
2. **2.0 Capture & Preprocess Sample** — Receives a handwriting sample from the Student, stores the raw image in **D2 Handwriting Samples**, cleans/normalizes it, and stores the result in **D3 Preprocessed Data**.
3. **3.0 Run MobileNetV3 Inference & Explanation** — Retrieves preprocessed data from D3 and produces a "Detection result & explanation" — this process is a black box at this level; its internals are shown in Stage 2.
4. **4.0 Generate Report** — Takes the detection result from 3.0, stores it in **D4 Reports**, and delivers the formatted report to the Teacher and a notification to the Parent.

Reading the flow: follow the sequence 1.0 → 2.0 → 3.0 → 4.0 top to bottom; each process only starts once its required input data is available (e.g., 3.0 needs preprocessed data from D3, which only exists after 2.0 has run).

**Stage 2 — Level 2 DFD (`S2_DFD.svg`)**

Expands **Process 3.0** — the "black box" from Stage 1 — into its four internal sub-processes, since this is the most technically significant part of the system (the AI model pipeline):

1. **3.1 Extract Handwriting Features** — Runs the preprocessed image through the feature-extraction layers, producing a feature map stored in **D5 Feature Maps**.
2. **3.2 Run MobileNetV3 Classification (transfer learning)** — Reads the feature map from D5 and classifies the sample, producing a class label and confidence score, stored in **D6 Classification Output**.
3. **3.3 Generate XAI Explanation (Grad-CAM)** — Reads both the feature map (D5) and the predicted class (D6) to compute a Grad-CAM heatmap, showing which regions of the handwriting most influenced the prediction. Stored in **D7 Explanation Map**.
4. **3.4 Compile Detection Result & Explanation** — Merges the classification output (D6) and the explanation map (D7) into a single combined result, which is passed out of Process 3.0's boundary to **4.0 Generate Report** in Stage 1.

This diagram is what proves the system isn't a "black box" AI — every prediction is traceable back through explicit, auditable steps: feature extraction → classification → explanation → compilation. It also maps directly to the model architecture described in Section 3 (MobileNetV3 + CNN/Transformer classification head + Grad-CAM).

---

### 5.2 Structured Chart

While the DFDs show *how data flows*, the Structured Chart shows *how the software is organized into callable modules* — a program-structure view used for top-down design and implementation planning.

**Notation:**
- **Rectangles with sharp corners** = control/functional modules (program units).
- **Diamonds on a connecting line** = conditional calls (the module below is only called under a certain condition).
- **Plain solid lines (no arrowhead)** = unconditional calls (always executed as part of the parent's logic).
- **Rounded rectangles (pill-shaped)** = physical data stores/files.
- **Arrows with a hollow circle tail** = data couples (actual data values passed between modules).
- **Arrows with a filled circle tail** = control couples (flags/signals passed between modules, not raw data).
- **Curved arrow (loop symbol)** = a module that repeatedly invokes a child module until a condition is met.

**Structure, top to bottom:**

*Top Control Layer*
- `Detect_Dyslexia_Risk` — the root module that coordinates all subsystems.

*Subsystem Layer* (called by the root)
- `Manage_Input_Pipeline` — captures and validates incoming data.
- `Run_MobileNetV3_Inference` — runs the pre-trained model (transfer learning) plus XAI explanation.
- `Generate_Output_Report` — handles report formatting (called *conditionally*, indicated by the diamond — a report is only generated once a result is ready).

*Leaf / Utility Layer* (called by the subsystem modules)
- `Manage_Accounts` — verifies login credentials (child of `Manage_Input_Pipeline`).
- `Capture_Handwriting_Sample` — accesses the student's submission (child of `Manage_Input_Pipeline`); loops, repeatedly calling `Preprocess_Data` until the sample is valid.
- `Preprocess_Data` — cleans and validates the raw sample; exchanges "Preprocessed Sample" and "Raw Sample" data couples with its parent.
- `Extract_Features` — runs the MobileNetV3 backbone to extract a feature map (child of `Run_MobileNetV3_Inference`).
- `Classify_Dyslexia_Risk` — applies the pre-trained classifier to produce a risk score (sibling of `Extract_Features`).
- `Generate_XAI_Explanation` — produces the Grad-CAM heatmap (sibling module, reads feature map + predicted class).
- `Compile_Detection_Result` — merges the risk score and heatmap into a formatted report (child of `Generate_Output_Report`).
- `Store_Report` — writes the formatted report to the database (sibling of `Compile_Detection_Result`).

**Physical data stores referenced:**
- **D5 — Pretrained MobileNetV3 Weights**: loaded by `Extract_Features`, `Classify_Dyslexia_Risk`, and `Generate_XAI_Explanation`.
- **D4 — Reports Database**: written to by `Store_Report`.

Each DFD process (1.0–4.0) maps to a corresponding module here, and each DFD data store maps to a physical file/database — the Structured Chart and the DFDs describe the *same system* from two complementary angles (data flow vs. program structure).

---

### 5.3 HIPO Diagram — Hierarchy Plus Input-Process-Output

Documents each module's function using two complementary views, bridging the Structured Chart's module hierarchy with concrete input/output specifications useful for implementation.

**`hipo_vtoc.svg` — Visual Table of Contents (VTOC)**
A hierarchy chart listing every system module and its parent-child relationship, using the **same numbering as the DFDs** (0.0 → 1.0–4.0 → 3.1–3.4) so a reader can cross-reference any module across the DFD, Structured Chart, and HIPO diagram without confusion.

**`hipo_ipo_charts.md` — IPO Charts**
For every module in the VTOC, a table specifies:
- **Input** — the data received and its source.
- **Process** — the steps performed internally.
- **Output** — the data produced and its destination.

This includes the full breakdown of Process 3.0's sub-modules (3.1 Extract Features → 3.2 Classify → 3.3 Generate XAI Explanation → 3.4 Compile Result), plus a data-store cross-reference table (D1–D7) showing exactly which module writes to and reads from each store.

---

### 5.4 Structured English 

Will describe the step-by-step logic of each key process (Manage Accounts, Capture & Preprocess Sample, MobileNetV3 Inference, Generate Report) using controlled, plain-English statements (IF/THEN/ELSE, DO WHILE, REPEAT UNTIL), acting as a bridge between the DFD/Structured Chart's visual logic and the algorithm-level Pseudocode.

### 5.5 Pseudocode 

Will translate the Structured English into algorithm-level pseudocode for each module, closely mirroring how the modules will be implemented in the actual mobile application codebase.

### 5.6 Entity-Relationship Diagram (ERD) 
Will model the system's database structure in Chen notation, covering entities such as Users/Accounts, Handwriting Samples, Classification Results, Explanation Maps, and Reports — directly corresponding to the data stores (D1–D7) already established in the DFDs and Structured Chart.

### 5.7 Data Dictionary 

Will define every data element referenced across the DFDs, Structured Chart, and ERD — including field names, data types, sizes, and descriptions — ensuring consistent terminology throughout all documentation.

---

### 5.8 How These Diagrams Relate to Each Other

```
DFD (data flow)  ──────┐
                        ├──► Structured Chart (program structure) ──► HIPO (module I/O detail)
Numbering (0.0–4.0,     │                                                    │
3.1–3.4) stays          │                                                    ▼
consistent across ──────┘                                     Structured English → Pseudocode
all three                                                                    │
                                                                              ▼
                                                                 Implementation-ready modules
```

Every module number and data-store ID (D1–D7) is kept identical across all diagrams so that any reviewer can trace a single process (e.g., "3.2 Run MobileNetV3 Classification") through the DFD, Structured Chart, and HIPO diagram without ambiguity.

---

## 6. Repository Purpose

This repository is the single source of truth for the DysWrite Thesis 1 project, supporting:
*   **Checking and validation** of system design artifacts against DMMMSU thesis format.
*   **Testing** of the mobile application and its underlying model.
*   **Version control** across iterative revisions of diagrams, charts, and documentation.
*   **Maintenance** and collaboration among all group members and the thesis adviser.

---

## 7. Research & Development Team

**Student Researchers (DMMMSU – South La Union Campus, College of Computer Science):**

*   **Regacho, Rachel A.** 
*   **Bicera, Gerrald A.** 
*   **Garcia, Angeline G.** 
*   **Lachica, John Albert C.** 
*   **Velasquez, Regine J.** 

**Thesis Adviser:**
*   **Dungan, Belinda** — Thesis Adviser
