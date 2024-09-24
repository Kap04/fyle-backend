-- Write query to get number of graded assignments for each student:
SELECT 
    s.id AS student_id,
    s.user_id,
    COUNT(a.id) AS graded_assignments_count
FROM 
    students s
LEFT JOIN 
    assignments a ON s.id = a.student_id AND a.state = 'GRADED'
GROUP BY 
    s.id, s.user_id
ORDER BY 
    s.id;