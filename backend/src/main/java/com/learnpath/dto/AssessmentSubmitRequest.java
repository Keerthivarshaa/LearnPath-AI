package com.learnpath.dto;

import java.util.Map;

public class AssessmentSubmitRequest {
    private Map<Long, Long> answers;

    public AssessmentSubmitRequest() {
    }

    public AssessmentSubmitRequest(Map<Long, Long> answers) {
        this.answers = answers;
    }

    public Map<Long, Long> getAnswers() {
        return answers;
    }

    public void setAnswers(Map<Long, Long> answers) {
        this.answers = answers;
    }
}
