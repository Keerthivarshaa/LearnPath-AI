package com.learnpath.dto;

public class AssessmentAnswerDTO {
    private Long questionId;
    private String questionText;
    private Long selectedOptionId;
    private Long correctOptionId;
    private boolean isCorrect;
    private String topic;
    private String correctExplanation;

    public AssessmentAnswerDTO() {
    }

    public AssessmentAnswerDTO(Long questionId, String questionText, Long selectedOptionId, Long correctOptionId, boolean isCorrect, String topic, String correctExplanation) {
        this.questionId = questionId;
        this.questionText = questionText;
        this.selectedOptionId = selectedOptionId;
        this.correctOptionId = correctOptionId;
        this.isCorrect = isCorrect;
        this.topic = topic;
        this.correctExplanation = correctExplanation;
    }

    public Long getQuestionId() {
        return questionId;
    }

    public void setQuestionId(Long questionId) {
        this.questionId = questionId;
    }

    public String getQuestionText() {
        return questionText;
    }

    public void setQuestionText(String questionText) {
        this.questionText = questionText;
    }

    public Long getSelectedOptionId() {
        return selectedOptionId;
    }

    public void setSelectedOptionId(Long selectedOptionId) {
        this.selectedOptionId = selectedOptionId;
    }

    public Long getCorrectOptionId() {
        return correctOptionId;
    }

    public void setCorrectOptionId(Long correctOptionId) {
        this.correctOptionId = correctOptionId;
    }

    public boolean isCorrect() {
        return isCorrect;
    }

    public void setCorrect(boolean correct) {
        isCorrect = correct;
    }

    public String getTopic() {
        return topic;
    }

    public void setTopic(String topic) {
        this.topic = topic;
    }

    public String getCorrectExplanation() {
        return correctExplanation;
    }

    public void setCorrectExplanation(String correctExplanation) {
        this.correctExplanation = correctExplanation;
    }
}
