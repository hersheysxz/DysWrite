# Structured English

Structured English expresses the logic of the DysWrite Dyslexia Risk Assessment process using plain English combined with simple programming constructs (IF-THEN-ELSE, DO-WHILE), making the process logic understandable to both technical and non-technical stakeholders (e.g., the thesis panel, adviser, and partner school).

## Structured English  Assess Dyslexia Risk Module

```
MODULE: ASSESS_DYSLEXIA_RISK

BEGIN

    READ handwriting_image FROM user upload

    IF image_format IS NOT valid THEN
        DISPLAY "Invalid image format. Please upload a JPG or PNG file."
        EXIT MODULE
    ENDIF

    PREPROCESS handwriting_image
        RESIZE image TO standard input dimensions
        NORMALIZE pixel values
        REMOVE noise/background artifacts

    EXTRACT features FROM preprocessed_image USING MobileNetV3
    CLASSIFY features USING CNN_Transformer_Model
    SET confidence_score TO classification output probability

    IF confidence_score >= 0.80 THEN
        SET risk_level TO "High Risk"
    ELSE IF confidence_score >= 0.50 THEN
        SET risk_level TO "Moderate Risk"
    ELSE
        SET risk_level TO "Low Risk"
    ENDIF

    GENERATE Grad-CAM heatmap FOR preprocessed_image
    STORE assessment_result (risk_level, confidence_score, heatmap_image, date)
    DISPLAY assessment_result TO user

END MODULE
```
