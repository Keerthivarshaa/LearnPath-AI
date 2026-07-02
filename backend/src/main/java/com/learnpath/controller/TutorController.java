package com.learnpath.controller;

import com.learnpath.dto.ChatMessage;
import com.learnpath.dto.TutorRequestDTO;
import com.learnpath.dto.TutorResponseDTO;
import com.learnpath.model.Progress;
import com.learnpath.model.User;
import com.learnpath.service.ProgressService;
import com.learnpath.service.TutorService;
import com.learnpath.service.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/tutor")
public class TutorController {

    private final TutorService tutorService;
    private final UserService userService;
    private final ProgressService progressService;

    public TutorController(TutorService tutorService, UserService userService, ProgressService progressService) {
        this.tutorService = tutorService;
        this.userService = userService;
        this.progressService = progressService;
    }

    @PostMapping("/chat")
    public ResponseEntity<?> sendMessage(@RequestBody TutorRequestDTO request) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Error: Unauthorized access!");
        }

        if (request == null || request.getMessage() == null || request.getMessage().trim().isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error: Prompt message cannot be empty!");
        }

        Optional<User> userOpt = userService.findByEmail(auth.getName());
        if (userOpt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Error: User not found!");
        }

        TutorResponseDTO response = tutorService.sendMessage(userOpt.get(), request.getMessage());
        return ResponseEntity.ok(response);
    }

    @GetMapping("/history")
    public ResponseEntity<?> getHistory() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Error: Unauthorized access!");
        }

        Optional<User> userOpt = userService.findByEmail(auth.getName());
        if (userOpt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Error: User not found!");
        }

        List<ChatMessage> history = tutorService.getHistory(userOpt.get().getEmail());
        return ResponseEntity.ok(history);
    }

    @GetMapping("/suggestions")
    public ResponseEntity<?> getSuggestions() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Error: Unauthorized access!");
        }

        Optional<User> userOpt = userService.findByEmail(auth.getName());
        if (userOpt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Error: User not found!");
        }

        User user = userOpt.get();
        Progress progress = progressService.getOrCreateProgress(user);
        List<String> suggestions = tutorService.getSuggestedQuestions(user, progress);
        return ResponseEntity.ok(suggestions);
    }
}
