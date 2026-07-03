package com.learnpath.dto;

import java.util.Map;

/**
 * Wire-format response DTO for POST /ml/predict-readiness.
 *
 * Field names match ai-service/app/schemas/readiness.py's
 * ReadinessResponse JSON aliases exactly (camelCase - deliberately
 * aliased that way on the Python side specifically for Java
 * consumption), so no @JsonProperty mapping is needed here.
 */
public class ReadinessPredictionResponse {

    private Double readinessScore;
    private String readinessLevel;
    private String explanation;
    private Map<String, Double> engineeredFeatures;
    private String modelSource;

    public ReadinessPredictionResponse() {
    }

    public Double getReadinessScore() {
        return readinessScore;
    }

    public void setReadinessScore(Double readinessScore) {
        this.readinessScore = readinessScore;
    }

    public String getReadinessLevel() {
        return readinessLevel;
    }

    public void setReadinessLevel(String readinessLevel) {
        this.readinessLevel = readinessLevel;
    }

    public String getExplanation() {
        return explanation;
    }

    public void setExplanation(String explanation) {
        this.explanation = explanation;
    }

    public Map<String, Double> getEngineeredFeatures() {
        return engineeredFeatures;
    }

    public void setEngineeredFeatures(Map<String, Double> engineeredFeatures) {
        this.engineeredFeatures = engineeredFeatures;
    }

    public String getModelSource() {
        return modelSource;
    }

    public void setModelSource(String modelSource) {
        this.modelSource = modelSource;
    }
}
