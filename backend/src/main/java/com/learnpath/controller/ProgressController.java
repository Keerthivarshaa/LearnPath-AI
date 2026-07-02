package com.learnpath.controller;

import com.learnpath.dto.ProgressDTO;
import com.learnpath.dto.ProgressUpdateSubmit;
import com.learnpath.model.User;
import com.learnpath.service.ProgressService;
import com.learnpath.service.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/api/progress")
public class ProgressController {

    private final ProgressService progressService;
    private final UserService userService;

    public ProgressController(ProgressService progressService, UserService userService) {
        this.progressService = progressService;
        this.userService = userService;
    }

    @GetMapping
    public ResponseEntity<?> getProgress() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Error: Unauthorized access!");
        }

        Optional<User> userOpt = userService.findByEmail(auth.getName());
        if (userOpt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Error: User not found!");
        }

        ProgressDTO progress = progressService.getProgressDTO(userOpt.get());
        return ResponseEntity.ok(progress);
    }

    @PostMapping("/study-log")
    public ResponseEntity<?> logStudySession(@RequestBody ProgressUpdateSubmit request) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Error: Unauthorized access!");
        }

        if (request == null || request.getHours() == null || request.getTopic() == null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error: Missing hours or topic parameter!");
        }

        Optional<User> userOpt = userService.findByEmail(auth.getName());
        if (userOpt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Error: User not found!");
        }

        ProgressDTO progress = progressService.logStudySession(userOpt.get(), request.getHours(), request.getTopic());
        return ResponseEntity.ok(progress);
    }
}
