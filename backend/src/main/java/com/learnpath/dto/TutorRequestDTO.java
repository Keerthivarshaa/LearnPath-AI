package com.learnpath.dto;

public class TutorRequestDTO {
    private String message;

    public TutorRequestDTO() {
    }

    public TutorRequestDTO(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
