package com.learnpath.service;

import com.learnpath.dto.ChatMessage;
import com.learnpath.dto.TutorResponseDTO;
import com.learnpath.model.*;
import com.learnpath.repository.AssessmentResultRepository;
import org.springframework.stereotype.Service;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class TutorService {

    private final ChatProvider chatProvider;
    private final ProgressService progressService;
    private final AssessmentResultRepository assessmentResultRepository;

    // In-memory conversation history map keyed by user email
    private final Map<String, List<ChatMessage>> chatHistory = new ConcurrentHashMap<>();

    public TutorService(ChatProvider chatProvider, ProgressService progressService, AssessmentResultRepository assessmentResultRepository) {
        this.chatProvider = chatProvider;
        this.progressService = progressService;
        this.assessmentResultRepository = assessmentResultRepository;
    }

    public List<ChatMessage> getHistory(String email) {
        return chatHistory.computeIfAbsent(email, k -> new ArrayList<>());
    }

    public TutorResponseDTO sendMessage(User user, String userMessage) {
        Progress progress = progressService.getOrCreateProgress(user);
        List<ChatMessage> history = getHistory(user.getEmail());

        // Append user prompt
        history.add(new ChatMessage("USER", userMessage));

        // Generate response from the extensible ChatProvider
        String botReply = chatProvider.generateResponse(user, progress, history, userMessage);

        // Append assistant response
        history.add(new ChatMessage("ASSISTANT", botReply));

        // Limit memory history to last 50 messages to prevent excessive bloat
        if (history.size() > 50) {
            history.subList(0, history.size() - 50).clear();
        }

        // Award 10 XP for engagement
        progressService.awardXp(user, 10, "Interacted with AI Study Tutor");

        // Compile context-aware suggestions
        List<String> suggested = getSuggestedQuestions(user, progress);

        return new TutorResponseDTO(botReply, suggested);
    }

    public List<String> getSuggestedQuestions(User user, Progress progress) {
        List<String> suggestions = new ArrayList<>();
        String goal = user.getCertificationGoal();

        // 1. Contextual weaknesses from the latest scorecard
        Optional<AssessmentResult> latestResultOpt = assessmentResultRepository.findFirstByUserOrderByCompletedAtDesc(user);
        
        if (latestResultOpt.isPresent() && latestResultOpt.get().getWeakTopics() != null && !latestResultOpt.get().getWeakTopics().isEmpty()) {
            List<String> weak = latestResultOpt.get().getWeakTopics();
            suggestions.add(String.format("Explain best practices for %s", weak.get(0)));
            if (weak.size() > 1) {
                suggestions.add(String.format("Give me a study guide on %s", weak.get(1)));
            }
        }

        // 2. Add goal-based fallbacks to complete 3 options
        if (goal.contains("Solutions Architect") || goal.contains("Cloud")) {
            if (suggestions.size() < 3) suggestions.add("Explain EC2 pricing: On-Demand vs Reserved vs Spot");
            if (suggestions.size() < 3) suggestions.add("How do Multi-AZ RDS setups differ from Read Replicas?");
            if (suggestions.size() < 3) suggestions.add("Give me a mock practice quiz question");
        } else if (goal.contains("Java")) {
            if (suggestions.size() < 3) suggestions.add("Explain JVM Garbage Collection: G1GC vs ZGC");
            if (suggestions.size() < 3) suggestions.add("Show me Java 17 Pattern Matching syntax");
            if (suggestions.size() < 3) suggestions.add("Give me a mock practice quiz question");
        } else if (goal.contains("Security+")) {
            if (suggestions.size() < 3) suggestions.add("Explain symmetric vs asymmetric encryption");
            if (suggestions.size() < 3) suggestions.add("What is the difference between a Security Group and a NACL?");
            if (suggestions.size() < 3) suggestions.add("Give me a mock practice quiz question");
        } else {
            if (suggestions.size() < 3) suggestions.add("How do I structure my study roadmap milestones?");
            if (suggestions.size() < 3) suggestions.add("Give me a mock practice quiz question");
            if (suggestions.size() < 3) suggestions.add("How do I earn preparation XP?");
        }

        // Ensure exactly 3 suggestions
        return suggestions.subList(0, Math.min(3, suggestions.size()));
    }
}
