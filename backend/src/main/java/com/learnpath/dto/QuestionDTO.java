package com.learnpath.dto;

import java.util.List;

public class QuestionDTO {
    private Long id;
    private String text;
    private String topic;
    private String category;
    private String difficulty;
    private Integer displayOrder;
    private List<OptionDTO> options;

    public QuestionDTO() {
    }

    public QuestionDTO(Long id, String text, String topic, String category, String difficulty, Integer displayOrder, List<OptionDTO> options) {
        this.id = id;
        this.text = text;
        this.topic = topic;
        this.category = category;
        this.difficulty = difficulty;
        this.displayOrder = displayOrder;
        this.options = options;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public String getTopic() {
        return topic;
    }

    public void setTopic(String topic) {
        this.topic = topic;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getDifficulty() {
        return difficulty;
    }

    public void setDifficulty(String difficulty) {
        this.difficulty = difficulty;
    }

    public Integer getDisplayOrder() {
        return displayOrder;
    }

    public void setDisplayOrder(Integer displayOrder) {
        this.displayOrder = displayOrder;
    }

    public List<OptionDTO> getOptions() {
        return options;
    }

    public void setOptions(List<OptionDTO> options) {
        this.options = options;
    }
}
