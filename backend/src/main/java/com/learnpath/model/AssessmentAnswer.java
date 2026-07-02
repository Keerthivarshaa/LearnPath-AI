package com.learnpath.model;

import jakarta.persistence.*;

@Entity
@Table(name = "assessment_answers")
public class AssessmentAnswer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "result_id", nullable = false)
    private AssessmentResult assessmentResult;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "question_id", nullable = false)
    private Question question;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "selected_option_id", nullable = true)
    private Option selectedOption;

    @Column(name = "is_correct", nullable = false)
    private boolean isCorrect;

    @Column(nullable = false)
    private String topic;

    public AssessmentAnswer() {
    }

    public AssessmentAnswer(AssessmentResult assessmentResult, Question question, Option selectedOption, boolean isCorrect, String topic) {
        this.assessmentResult = assessmentResult;
        this.question = question;
        this.selectedOption = selectedOption;
        this.isCorrect = isCorrect;
        this.topic = topic;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public AssessmentResult getAssessmentResult() {
        return assessmentResult;
    }

    public void setAssessmentResult(AssessmentResult assessmentResult) {
        this.assessmentResult = assessmentResult;
    }

    public Question getQuestion() {
        return question;
    }

    public void setQuestion(Question question) {
        this.question = question;
    }

    public Option getSelectedOption() {
        return selectedOption;
    }

    public void setSelectedOption(Option selectedOption) {
        this.selectedOption = selectedOption;
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
}
