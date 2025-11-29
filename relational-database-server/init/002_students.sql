
CREATE DATABASE IF NOT EXISTS studentdb;


USE studentdb;

CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(10) NOT NULL UNIQUE,
    fullname VARCHAR(100) NOT NULL,
    dob DATE,
    major VARCHAR(50)
);

INSERT INTO students (student_id, fullname, dob, major) VALUES
('SV001', N'Nguyễn Văn A', '2004-05-15', N'Khoa học Máy tính'),
('SV002', N'Trần Thị B', '2003-11-20', N'Kỹ thuật Phần mềm'),
('SV003', N'Lê Văn C', '2004-01-01', N'Mạng Máy tính');


-- Test insert:
INSERT INTO students (student_id, fullname, dob, major)
VALUES ('SV004', 'Nguyen Van F', '2003-09-10', 'Data Science');
--Check
SELECT *
FROM students
WHERE student_id = 'SV004';

--UPDATE:
UPDATE students
SET fullname = 'Nguyen Van F',
    major    = 'Machine Learning'
WHERE student_id = 'SV004';


--Delete:
DELETE FROM students
WHERE student_id = 'SV004';
--Check
SELECT * FROM students WHERE student_id = 'SV004';
SELECT * FROM students;