package com.learnpath.service;

import com.learnpath.dto.*;
import com.learnpath.model.*;
import com.learnpath.repository.AssessmentResultRepository;
import com.learnpath.repository.QuestionRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class AssessmentService {

    private final QuestionRepository questionRepository;
    private final AssessmentResultRepository assessmentResultRepository;
    private final ProgressService progressService;

    public AssessmentService(QuestionRepository questionRepository, AssessmentResultRepository assessmentResultRepository, ProgressService progressService) {
        this.questionRepository = questionRepository;
        this.assessmentResultRepository = assessmentResultRepository;
        this.progressService = progressService;
    }

    public List<QuestionDTO> getQuestionsForUser(User user) {
        String goal = user.getCertificationGoal();
        List<Question> questions = questionRepository.findByCertificationGoalOrderByDisplayOrderAsc(goal);

        // Fallback: If no questions match the specific goal, load default questions
        if (questions.isEmpty()) {
            questions = questionRepository.findByCertificationGoalOrderByDisplayOrderAsc("AWS Certified Solutions Architect");
        }
        // Double Fallback: Load any questions if the above is still empty
        if (questions.isEmpty()) {
            questions = questionRepository.findAll();
        }

        return questions.stream().map(this::convertToQuestionDTO).collect(Collectors.toList());
    }

    @Transactional
    public AssessmentResultDTO submitAssessment(User user, Map<Long, Long> submission) {
        String goal = user.getCertificationGoal();
        List<Question> questions = questionRepository.findByCertificationGoalOrderByDisplayOrderAsc(goal);
        if (questions.isEmpty()) {
            questions = questionRepository.findByCertificationGoalOrderByDisplayOrderAsc("AWS Certified Solutions Architect");
        }
        if (questions.isEmpty()) {
            questions = questionRepository.findAll();
        }

        AssessmentResult result = new AssessmentResult();
        result.setUser(user);
        result.setCompletedAt(LocalDateTime.now());
        result.setTotalQuestions(questions.size());

        int score = 0;
        List<AssessmentAnswer> answersList = new ArrayList<>();

        // Keep track of topic scores
        Map<String, List<Boolean>> topicResults = new HashMap<>();

        for (Question question : questions) {
            Long selectedOptionId = submission.get(question.getId());
            Option selectedOption = null;
            boolean isCorrect = false;

            if (selectedOptionId != null) {
                selectedOption = question.getOptions().stream()
                        .filter(opt -> opt.getId().equals(selectedOptionId))
                        .findFirst()
                        .orElse(null);
            }

            if (selectedOption != null) {
                isCorrect = selectedOption.isCorrect();
            }

            if (isCorrect) {
                score++;
            }

            // Record topic correctness
            topicResults.computeIfAbsent(question.getTopic(), k -> new ArrayList<>()).add(isCorrect);

            AssessmentAnswer answer = new AssessmentAnswer();
            answer.setQuestion(question);
            answer.setSelectedOption(selectedOption);
            answer.setCorrect(isCorrect);
            answer.setTopic(question.getTopic());
            result.addAnswer(answer);
            answersList.add(answer);
        }

        result.setScore(score);

        // Classify weak and strong topics
        List<String> strongTopics = new ArrayList<>();
        List<String> weakTopics = new ArrayList<>();

        for (Map.Entry<String, List<Boolean>> entry : topicResults.entrySet()) {
            String topic = entry.getKey();
            List<Boolean> results = entry.getValue();
            long correctCount = results.stream().filter(r -> r).count();
            double ratio = (double) correctCount / results.size();

            if (ratio >= 0.7) {
                strongTopics.add(topic);
            } else {
                weakTopics.add(topic);
            }
        }

        result.setStrongTopics(strongTopics);
        result.setWeakTopics(weakTopics);

        AssessmentResult savedResult = assessmentResultRepository.save(result);
        progressService.awardXp(user, ProgressService.ASSESSMENT_COMPLETION_XP, "Assessment completed: " + goal);
        progressService.checkAssessmentAchievements(user);
        return convertToResultDTO(savedResult);
    }

    public Optional<AssessmentResultDTO> getLatestResultForUser(User user) {
        return assessmentResultRepository.findFirstByUserOrderByCompletedAtDesc(user)
                .map(this::convertToResultDTO);
    }

    private QuestionDTO convertToQuestionDTO(Question question) {
        List<OptionDTO> optionDTOs = question.getOptions().stream()
                .map(opt -> new OptionDTO(opt.getId(), opt.getText()))
                .collect(Collectors.toList());

        return new QuestionDTO(
                question.getId(),
                question.getText(),
                question.getTopic(),
                question.getCategory(),
                question.getDifficulty().name(),
                question.getDisplayOrder(),
                optionDTOs
        );
    }

    private AssessmentResultDTO convertToResultDTO(AssessmentResult result) {
        List<AssessmentAnswerDTO> answerDTOs = result.getAnswers().stream().map(ans -> {
            Option correctOption = ans.getQuestion().getOptions().stream()
                    .filter(Option::isCorrect)
                    .findFirst()
                    .orElse(null);

            return new AssessmentAnswerDTO(
                    ans.getQuestion().getId(),
                    ans.getQuestion().getText(),
                    ans.getSelectedOption() != null ? ans.getSelectedOption().getId() : null,
                    correctOption != null ? correctOption.getId() : null,
                    ans.isCorrect(),
                    ans.getTopic(),
                    ans.getQuestion().getCorrectExplanation()
            );
        }).collect(Collectors.toList());

        return new AssessmentResultDTO(
                result.getId(),
                result.getScore(),
                result.getTotalQuestions(),
                result.getWeakTopics(),
                result.getStrongTopics(),
                result.getCompletedAt(),
                answerDTOs
        );
    }
}
