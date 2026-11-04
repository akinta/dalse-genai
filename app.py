# Import the trainee business functions.
from trainees import create_trainee, add_trainee

# Import functions for reading and writing JSON files.
from storage import load_trainees, save_trainees


def ask_text(prompt):
    """Ask for text that must not be empty."""

    # Repeat until the user provides non-empty text.
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def ask_score(prompt):
    """Ask for a numeric score between 0 and 100."""

    # Repeat until the user supplies a valid score.
    while True:
        value = input(prompt).strip()

        try:
            # Convert the text into a floating-point number.
            score = float(value)

            # Reject values outside the permitted range.
            if not 0 <= score <= 100:
                print("Enter a score between 0 and 100.")
                continue
            

            # Return the validated score.
            return score

        except ValueError:
            # Handle text that cannot be converted into a number.
            print("Invalid number. Please try again.")


def register_trainee(trainees):
    """Collect trainee information and register the trainee."""

    # Ask the user for the trainee's basic information.
    trainee_id = ask_text("Trainee ID: ")
    name = ask_text("Full name: ")
    email = ask_text("Email address: ")

    # Collect the three assessment scores.
    practical = ask_score("Practical score (0-100): ")
    assignment = ask_score("Assignment score (0-100): ")
    exam = ask_score("Examination score (0-100): ")

    # Collect attendance as a percentage.
    attendance = ask_score("Attendance (0-100): ")

    # Create a validated trainee dictionary.
    trainee = create_trainee(
        trainee_id=trainee_id,
        name=name,
        email=email,
        practical=practical,
        assignment=assignment,
        exam=exam,
        attendance=attendance,
    )

    # Add the trainee and reject duplicate IDs.
    add_trainee(trainees, trainee)

    # Persist the updated list to the JSON file.
    save_trainees(trainees)

    # Display a simple registration confirmation.
    print("\nTrainee registered successfully!")
    print(f"Trainee ID: {trainee['id']}")
    print(f"Final score: {trainee['total']:.2f}/100")
    print(f"Grade: {trainee['grade']}")
    print(f"Status: {trainee['status']}")


def list_trainees(trainees):
    """Display all saved trainee records."""

    # Tell the user when there are no records.
    if not trainees:
        print("\nNo trainees have been registered.")
        return

    # Display the report heading.
    print("\nREGISTERED TRAINEES")
    print("-" * 80)

    # Display each trainee's main information.
    for trainee in trainees:
        print(
            f"{trainee['id']} | "
            f"{trainee['name']} | "
            f"{trainee['total']:.2f}/100 | "
            f"{trainee['grade']} | "
            f"{trainee['status']}"
        )


def main():
    """Start and control the application."""

    # Load existing trainee records at application startup.
    try:
        trainees = load_trainees()
    except (ValueError, OSError) as error:
        print(f"Could not load trainee records: {error}")
        return

    # Keep showing the menu until the user exits.
    while True:
        print("\n" + "=" * 45)
        print("DALSE TECH HUB - TRAINEE MANAGEMENT")
        print("=" * 45)
        print("1. Register trainee")
        print("2. List trainees")
        print("3. Exit")

        # Get the user's menu choice.
        choice = input("Choose an option: ").strip()

        if choice == "1":
            try:
                # Run the registration workflow.
                register_trainee(trainees)

            except (ValueError, OSError) as error:
                # Report validation, duplicate or file errors.
                print(f"Registration failed: {error}")

        elif choice == "2":
            # Display the current trainee list.
            list_trainees(trainees)

        elif choice == "3":
            # End the application cleanly.
            print("Thank you for using the application.")
            break

        else:
            # Handle menu choices other than 1, 2 or 3.
            print("Invalid option. Select 1, 2 or 3.")


# Run the menu only when this file is executed directly.
if __name__ == "__main__":
    main()

