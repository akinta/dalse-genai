MIN_SCORE = 0
MAX_SCORE = 100


# Define the weighting of each assessment.
PRACTICAL_WEIGHT = 0.40
ASSIGNMENT_WEIGHT = 0.30
EXAM_WEIGHT = 0.30


def validate_score(score):
    """
    Check that a score is numeric and between 0 and 100.

    Raise ValueError if the score is invalid.
    Return a float if the score is valid.
    """

    # Boolean values are technically integers in Python.
    # Reject them because True and False are not meaningful scores.
    if isinstance(score, bool):
        raise ValueError("Score must be a number, not a boolean.")

    # Reject values that are not integers or floating-point numbers.
    if not isinstance(score, (int, float)):
        raise ValueError("Score must be numeric.")

    # Reject special floating-point values such as NaN and infinity.
    # A valid score must be finite.
    import math

    if not math.isfinite(score):
        raise ValueError("Score must be a finite number.")

    # Reject a score below zero or above 100.
    if score < MIN_SCORE or score > MAX_SCORE:
        raise ValueError("Score must be between 0 and 100.")

    # Convert valid scores into floats for consistent calculations.
    return float(score)


def calculate_total(practical, assignment, exam):
    """
    Calculate the weighted final score.

    Practical: 40%
    Assignment: 30%
    Examination: 30%
    """

    # Validate each score before performing calculations.
    practical = validate_score(practical)
    assignment = validate_score(assignment)
    exam = validate_score(exam)

    # Multiply each score by its weighting.
    practical_result = practical * PRACTICAL_WEIGHT
    assignment_result = assignment * ASSIGNMENT_WEIGHT
    exam_result = exam * EXAM_WEIGHT

    # Add the weighted scores and round the result to two decimals.
    total = practical_result + assignment_result + exam_result

    return round(total, 2)


def get_grade(total):
    """
    Convert a final score into a letter grade.
    """

    # Validate the final score before assigning a grade.
    total = validate_score(total)

    # Check the highest grade first.
    if total >= 70:
        return "A"

    # Scores from 60 to below 70 receive B.
    elif total >= 60:
        return "B"

    # Scores from 50 to below 60 receive C.
    elif total >= 50:
        return "C"

    # Scores from 45 to below 50 receive D.
    elif total >= 45:
        return "D"

    # Any lower score receives F.
    return "F"


def create_trainee(
    trainee_id,
    name,
    email,
    practical,
    assignment,
    exam,
    attendance
):
    """
    Validate trainee information and return a trainee dictionary.

    This function does not save the trainee to a file.
    Saving is the responsibility of storage.py.
    """

    # Ensure that the ID is a non-empty string.
    if not isinstance(trainee_id, str) or not trainee_id.strip():
        raise ValueError("Trainee ID cannot be empty.")

    # Ensure that the name is a non-empty string.
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Trainee name cannot be empty.")

    # Ensure that the email is a non-empty string.
    if not isinstance(email, str) or not email.strip():
        raise ValueError("Email cannot be empty.")

    # Validate all assessment scores.
    practical = validate_score(practical)
    assignment = validate_score(assignment)
    exam = validate_score(exam)

    # Attendance is also a percentage between 0 and 100.
    attendance = validate_score(attendance)

    # Calculate the weighted final score.
    total = calculate_total(practical, assignment, exam)

    # Determine the trainee's grade.
    grade = get_grade(total)

    # Apply both the score and attendance requirements.
    if total >= 50 and attendance >= 75:
        status = "PASS"
    else:
        status = "NOT YET ELIGIBLE"

    # Return a dictionary containing the trainee's information.
    return {
        "id": trainee_id.strip(),
        "name": name.strip(),
        "email": email.strip(),
        "practical": practical,
        "assignment": assignment,
        "exam": exam,
        "attendance": attendance,
        "total": total,
        "grade": grade,
        "status": status,
    }


def add_trainee(trainees, trainee):
    """
    Add a trainee to an in-memory list.

    Duplicate trainee IDs are not allowed.
    """

    # Check that the supplied collection is a list.
    if not isinstance(trainees, list):
        raise TypeError("Trainees must be stored in a list.")

    # Look for an existing trainee with the same ID.
    for existing in trainees:
        if existing["id"].casefold() == trainee["id"].casefold():
            raise ValueError(
                f"Trainee ID already exists: {trainee['id']}"
            )

    # Add the new trainee if no duplicate was found.
    trainees.append(trainee)

    # Return the updated list.
    return trainees
