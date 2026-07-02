package com.learnpath.repository;

import com.learnpath.model.AssessmentResult;
import com.learnpath.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface AssessmentResultRepository extends JpaRepository<AssessmentResult, Long> {
    Optional<AssessmentResult> findFirstByUserOrderByCompletedAtDesc(User user);
    List<AssessmentResult> findByUserOrderByCompletedAtDesc(User user);
}
