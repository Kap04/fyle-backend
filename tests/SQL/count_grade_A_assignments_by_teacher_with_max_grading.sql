WITH teacher_grade_a_counts AS (
    SELECT 
        teacher_id,
        COUNT(*) AS grade_a_count
    FROM 
        assignments
    WHERE 
        state = 'GRADED' AND grade = 'A'
    GROUP BY 
        teacher_id
),
max_grade_a_count AS (
    SELECT MAX(grade_a_count) AS max_count
    FROM teacher_grade_a_counts
)
SELECT 
    tgac.teacher_id,
    tgac.grade_a_count
FROM 
    teacher_grade_a_counts tgac
JOIN 
    max_grade_a_count mgac ON tgac.grade_a_count = mgac.max_count
ORDER BY 
    tgac.teacher_id
LIMIT 1;