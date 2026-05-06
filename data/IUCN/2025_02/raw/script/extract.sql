-- Critically Endangered
SELECT 'CRITICALLY ENDANGERED' AS CategoryHeader;
SELECT *
FROM RL_assessments_2025_02
WHERE wfo_id IS NOT NULL
  AND redlistCategory = 'Critically Endangered';

-- Endangered
SELECT 'ENDANGERED' AS CategoryHeader;
SELECT *
FROM RL_assessments_2025_02
WHERE wfo_id IS NOT NULL
  AND redlistCategory = 'Endangered';

-- Vulnerable
SELECT 'VULNERABLE' AS CategoryHeader;
SELECT *
FROM RL_assessments_2025_02
WHERE wfo_id IS NOT NULL
  AND redlistCategory = 'Vulnerable';

-- Near Threatened
SELECT 'NEAR THREATENED' AS CategoryHeader;
SELECT *
FROM RL_assessments_2025_02
WHERE wfo_id IS NOT NULL
  AND redlistCategory = 'Near Threatened';

-- Extinct
SELECT 'EXTINCT' AS CategoryHeader;
SELECT *
FROM RL_assessments_2025_02
WHERE wfo_id IS NOT NULL
  AND redlistCategory = 'Extinct';

-- Extinct in the Wild
SELECT 'EXTINCT IN THE WILD' AS CategoryHeader;
SELECT *
FROM RL_assessments_2025_02
WHERE wfo_id IS NOT NULL
  AND redlistCategory = 'Extinct in the Wild';

-- Least Concern
SELECT 'Least Concern' AS CategoryHeader;
SELECT *
FROM RL_assessments_2025_02
WHERE wfo_id IS NOT NULL
  AND redlistCategory = 'Least Concern';
 
-- Data Deficient
SELECT 'Data Deficient' AS CategoryHeader;
SELECT *
FROM RL_assessments_2025_02
WHERE wfo_id IS NOT NULL
  AND redlistCategory = 'Data Deficient';

SELECT 
    redlistCategory,
    COUNT(*) AS count
FROM RL_assessments_2025_02
WHERE redlistCategory IS NOT NULL
GROUP BY redlistCategory
ORDER BY count DESC;