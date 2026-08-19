# Pseudo-Code

The pseudocode below provides a step-by-step algorithmic description of the Dyslexia Risk Assessment process, serving as a bridge between the Structured English narrative and the actual Python implementation of the model.

## Pseudocode  AssessDyslexiaRisk() Function

```
FUNCTION AssessDyslexiaRisk(image):

    IF NOT IsValidFormat(image):
        RETURN Error("Invalid image format")
    END IF

    processedImage ← Preprocess(image)      // resize, normalize, denoise
    featureMap ← MobileNetV3.ExtractFeatures(processedImage)
    prediction ← CNNTransformer.Classify(featureMap)
    confidenceScore ← prediction.confidence

    IF confidenceScore >= 0.80:
        riskLevel ← "High Risk"
    ELSE IF confidenceScore >= 0.50:
        riskLevel ← "Moderate Risk"
    ELSE:
        riskLevel ← "Low Risk"
    END IF

    heatmap ← GradCAM.GenerateHeatmap(processedImage, CNNTransformer)

    result ← {
        riskLevel: riskLevel,
        confidenceScore: confidenceScore,
        heatmapImage: heatmap,
        dateAssessed: CurrentDate()
    }

    SaveToDatabase(result)
    RETURN result

END FUNCTION
```
