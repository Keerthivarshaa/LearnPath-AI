package com.learnpath.service;

import com.learnpath.dto.ChatMessage;
import com.learnpath.model.Progress;
import com.learnpath.model.User;
import java.util.List;

public interface ChatProvider {
    String generateResponse(User user, Progress progress, List<ChatMessage> history, String userMessage);
}
