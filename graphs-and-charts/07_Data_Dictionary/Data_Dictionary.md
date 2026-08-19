# Data Dictionary

The data dictionary below defines each data element used across the entities of the DysWrite system, including its data type, size, description, and constraints.

## Table 2. Data Dictionary — USER

| Field Name | Data Type | Size | Description | Constraint |
|---|---|---|---|---|
| UserID | INT | 11 | Unique identifier for a registered user (teacher, parent, or SPED practitioner) | PK, Auto-increment |
| Name | VARCHAR | 100 | Full name of the user | Not Null |
| Email | VARCHAR | 100 | Email address used for login and notifications | Not Null, Unique |
| Password | VARCHAR | 255 | Hashed password for authentication | Not Null |
| Role | ENUM | 20 | User role: Teacher, Parent, or SPED Practitioner | Not Null |
| ContactNumber | VARCHAR | 15 | Contact number of the user | Nullable |

## Table 3. Data Dictionary — CHILD

| Field Name | Data Type | Size | Description | Constraint |
|---|---|---|---|---|
| ChildID | INT | 11 | Unique identifier for a child profile | PK, Auto-increment |
| UserID | INT | 11 | Reference to the guardian/teacher managing this profile | FK → USER.UserID |
| Name | VARCHAR | 100 | Full name of the child | Not Null |
| Age | INT | 2 | Age of the child in years | Not Null |
| Gender | ENUM | 10 | Gender of the child | Nullable |
| GradeLevel | VARCHAR | 20 | Current grade/year level of the child | Nullable |

## Table 4. Data Dictionary — HANDWRITING_SAMPLE

| Field Name | Data Type | Size | Description | Constraint |
|---|---|---|---|---|
| SampleID | INT | 11 | Unique identifier for a handwriting sample | PK, Auto-increment |
| ChildID | INT | 11 | Reference to the child who submitted the sample | FK → CHILD.ChildID |
| ImagePath | VARCHAR | 255 | File path/URL of the uploaded handwriting image | Not Null |
| SampleType | VARCHAR | 30 | Type of writing task (e.g., copying, dictation) | Nullable |
| DateUploaded | DATETIME | — | Date and time the sample was uploaded | Not Null |

## Table 5. Data Dictionary — ASSESSMENT

| Field Name | Data Type | Size | Description | Constraint |
|---|---|---|---|---|
| AssessmentID | INT | 11 | Unique identifier for an assessment result | PK, Auto-increment |
| SampleID | INT | 11 | Reference to the handwriting sample assessed | FK → HANDWRITING_SAMPLE.SampleID |
| RiskLevel | ENUM | 20 | Predicted dyslexia risk level: High, Moderate, or Low | Not Null |
| ConfidenceScore | DECIMAL | 5,4 | Model prediction confidence (0.0000 – 1.0000) | Not Null |
| GradCAMPath | VARCHAR | 255 | File path of the generated Grad-CAM heatmap image | Not Null |
| DateAssessed | DATETIME | — | Date and time the assessment was performed | Not Null |

## Table 6. Data Dictionary — REPORT

| Field Name | Data Type | Size | Description | Constraint |
|---|---|---|---|---|
| ReportID | INT | 11 | Unique identifier for a generated report | PK, Auto-increment |
| AssessmentID | INT | 11 | Reference to the assessment this report summarizes | FK → ASSESSMENT.AssessmentID |
| GeneratedDate | DATETIME | — | Date and time the report was generated | Not Null |
| Recommendations | TEXT | — | Suggested next steps or interventions based on the result | Nullable |
