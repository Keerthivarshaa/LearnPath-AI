package com.learnpath.controller;

import com.learnpath.dto.AssessmentResultDTO;
import com.learnpath.dto.AssessmentSubmitRequest;
import com.learnpath.dto.QuestionDTO;
import com.learnpath.model.User;
import com.learnpath.service.AssessmentService;
import com.learnpath.service.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/assessment")
public class AssessmentController {

    private final AssessmentService assessmentService;
    private final UserService userService;

    public AssessmentController(AssessmentService assessmentService, UserService userService) {
        this.assessmentService = assessmentService;
        this.userService = userService;
    }

    @GetMapping("/questions")
    public ResponseEntity<?> getQuestions() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Error: Unauthorized access!");
        }

        Optional<User> userOpt = userService.findByEmail(auth.getName());
        if (userOpt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Error: User not found!");
        }

        List<QuestionDTO> questions = assessmentService.getQuestionsForUser(userOpt.get());
        return ResponseEntity.ok(questions);
    }

    @PostMapping("/submit")
    public ResponseEntity<?> submitAssessment(@RequestBody AssessmentSubmitRequest request) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Error: Unauthorized access!");
        }

        if (request == null || request.getAnswers() == null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error: Missing submission answers!");
        }

        Optional<User> userOpt = userService.findByEmail(auth.getName());
        if (userOpt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Error: User not found!");
        }

        AssessmentResultDTO result = assessmentService.submitAssessment(userOpt.get(), request.getAnswers());
        return ResponseEntity.ok(result);
    }

    @GetMapping("/result")
    public ResponseEntity<?> getLatestResult() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Error: Unauthorized access!");
        }

        Optional<User> userOpt = userService.findByEmail(auth.getName());
        if (userOpt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Error: User not found!");
        }

        Optional<AssessmentResultDTO> resultOpt = assessmentService.getLatestResultForUser(userOpt.get());
        if (resultOpt.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        return ResponseEntity.ok(resultOpt.get());
    }
}
