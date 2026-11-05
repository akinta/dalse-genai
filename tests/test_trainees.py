
# tests/test_trainees.py

# Import pytest so we can test expected exceptions.
import pytest

# Import the business functions that we want to test.
from trainees import (
    validate_score,
    calculate_total,
    get_grade,
    create_trainee,
    add_trainee,
)

# Import the storage functions.
from storage import load_trainees, save_trainees


def test_validate_score_accepts_zero():
    # ARRANGE: Choose the lowest valid score.
    score = 0

    # ACT: Validate the score.
    result = validate_score(score)

    # ASSERT: Zero is a valid score.
    assert result == 0.0


def test_validate_score_accepts_one_hundred():
    # Test the upper boundary of the valid score range.
    assert validate_score(100) == 100.0


def test_validate_score_rejects_negative_score():
    # A negative score must raise ValueError.
    with pytest.raises(ValueError):
        validate_score(-1)


def test_validate_score_rejects_score_above_one_hundred():
    # A score greater than 100 must be rejected.
    with pytest.raises(ValueError):
        validate_score(101)


def test_validate_score_rejects_text():
    # Text cannot be used as an assessment score.
    with pytest.raises(ValueError):
        validate_score("eighty")


def test_validate_score_rejects_boolean():
    # True must not accidentally be treated as score 1.
    with pytest.raises(ValueError):
        validate_score(True)


def test_calculate_total():
    # Arrange: choose known scores.
    practical = 80
    assignment = 70
    exam = 60

    # Act: calculate the weighted score.
    result = calculate_total(practical, assignment, exam)

    # Assert: 32 + 21 + 18 = 71.
    assert result == 71.0


def test_calculate_total_rejects_invalid_input():
    # The calculation must validate its inputs.
    with pytest.raises(ValueError):
        calculate_total(80, 120, 60)


@pytest.mark.parametrize(
    "score, expected_grade",
    [
        (75, "A"),
        (70, "A"),
        (65, "B"),
        (60, "B"),
        (55, "C"),
        (50, "C"),
        (47, "D"),
        (44, "F"),
        (0, "F"),
    ],
)
def test_get_grade(score, expected_grade):
    # Test several grading boundaries with one function.
    assert get_grade(score) == expected_grade


def test_create_trainee_passes_with_required_attendance():
    # Arrange and act: create a trainee with a score of 71
    # and attendance of 90 percent.
    trainee = create_trainee(
        trainee_id="DTH001",
        name="Ada Okafor",
        email="ada@example.com",
        practical=80,
        assignment=70,
        exam=60,
        attendance=90,
    )

    # Assert: verify the calculated values.
    assert trainee["total"] == 71.0
    assert trainee["grade"] == "A"
    assert trainee["status"] == "PASS"


def test_create_trainee_fails_attendance_requirement():
    # The trainee scores well but attendance is too low.
    trainee = create_trainee(
        trainee_id="DTH002",
        name="John Bello",
        email="john@example.com",
        practical=80,
        assignment=70,
        exam=60,
        attendance=60,
    )

    # Attendance below 75 percent prevents a pass.
    assert trainee["status"] == "NOT YET ELIGIBLE"


def test_create_trainee_rejects_empty_name():
    # An empty name must be rejected.
    with pytest.raises(ValueError):
        create_trainee(
            trainee_id="DTH003",
            name=" ",
            email="person@example.com",
            practical=80,
            assignment=70,
            exam=60,
            attendance=90,
        )


def test_add_trainee():
    # Start with an empty in-memory list.
    records = []

    # Create a valid trainee.
    trainee = create_trainee(
        trainee_id="DTH004",
        name="Mary James",
        email="mary@example.com",
        practical=80,
        assignment=70,
        exam=60,
        attendance=90,
    )

    # Add the trainee to the list.
    add_trainee(records, trainee)

    # Verify that the record was added.
    assert len(records) == 1
    assert records[0]["id"] == "DTH004"


def test_add_trainee_rejects_duplicate_id():
    # Create the first trainee.
    first = create_trainee(
        trainee_id="DTH005",
        name="Alice",
        email="alice@example.com",
        practical=80,
        assignment=70,
        exam=60,
        attendance=90,
    )

    # Create a second trainee with the same ID.
    second = create_trainee(
        trainee_id="dth005",
        name="Bob",
        email="bob@example.com",
        practical=60,
        assignment=60,
        exam=60,
        attendance=90,
    )

    # Add the first trainee.
    records = []
    add_trainee(records, first)

    # The duplicate ID must raise ValueError.
    with pytest.raises(ValueError):
        add_trainee(records, second)

    # The list must still contain only one trainee.
    assert len(records) == 1


def test_load_missing_file_returns_empty_list(tmp_path):
    # tmp_path is a temporary directory created by pytest.
    # The file has not been created, so loading returns [].
    missing_file = tmp_path / "missing.json"

    assert load_trainees(missing_file) == []


def test_save_and_load_trainees(tmp_path):
    # Create a temporary filename for this test.
    file_path = tmp_path / "trainees.json"

    # Prepare a sample record.
    records = [
        {
            "id": "DTH006",
            "name": "David",
            "total": 71.0,
        }
    ]

    # Save the record to JSON.
    save_trainees(records, file_path)

    # Load the record back from JSON.
    loaded_records = load_trainees(file_path)

    # Verify that the saved data was recovered.
    assert loaded_records == records


def test_load_invalid_json_raises_value_error(tmp_path):
    # Create a temporary file containing invalid JSON.
    file_path = tmp_path / "invalid.json"
    file_path.write_text("{this is not valid JSON", encoding="utf-8")

    # The storage module should report malformed JSON.
    with pytest.raises(ValueError):
        load_trainees(file_path)
