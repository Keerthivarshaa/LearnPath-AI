package com.learnpath.dto;

public class ProgressUpdateSubmit {
    private Double hours;
    private String topic;

    public ProgressUpdateSubmit() {
    }

    public ProgressUpdateSubmit(Double hours, String topic) {
        this.hours = hours;
        this.topic = topic;
    }

    public Double getHours() {
        return hours;
    }

    public void setHours(Double hours) {
        this.hours = hours;
    }

    public String getTopic() {
        return topic;
    }

    public void setTopic(String topic) {
        this.topic = topic;
    }
}
