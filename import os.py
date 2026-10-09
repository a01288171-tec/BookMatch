import os
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_FILE = os.path.join(BASE_DIR, "books.csv")
HISTORY_FILE = os.path.join(BASE_DIR, "user_history.csv")




def create_history_file():
    """
    Creates the history file if it does not exist.
    """
    if not os.path.exists(HISTORY_FILE):
        df = pd.DataFrame(columns=["Name", "Age", "Language", "Genre"])
        df.to_csv(HISTORY_FILE, index=False)




def create_books_file():
    """
    Creates a sample books database if it does not exist.
    """
    if not os.path.exists(BOOKS_FILE):
        books = pd.DataFrame(
            [
                {"Title": "The Hobbit", "Genre": "Fantasy", "Language": "English", "MinAge": 16, "MaxAge": 18},
                {"Title": "Atomic Habits", "Genre": "Self-help", "Language": "English", "MinAge": 14, "MaxAge": 100},
            ]
        )
        books.to_csv(BOOKS_FILE, index=False)




def load_books():
    """
    Loads the books database.
    """
    create_books_file()
    try:
        books = pd.read_csv(BOOKS_FILE)
        if books.empty:
            print("No books available in the database.")
            return pd.DataFrame(columns=["Title", "Genre", "Language", "MinAge", "MaxAge"])
        return books
    except FileNotFoundError:
        print("Error: books.csv not found.")
        return None




def get_user_preferences():
    """
    Gets user information.
   
    """
    print("\n--- Book Preferences ---")


    name = input("Enter your name: ").strip()


    while True:
        try:
            age = int(input("Enter your age: "))
            if age > 0:
                break
            print("Age must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")


    language = input("Preferred language (English/Spanish): ").strip().capitalize()
    genre = input("Favorite genre (Fantasy, Adventure, Fiction, Self-help): ").strip().capitalize()


    return name, age, language, genre




def recommend_books(books, age, language, genre):
    """
    Returns one book that matches the user's age and preferences.
    """
    if books is None or books.empty:
        return pd.DataFrame(columns=["Title", "Genre", "Language", "MinAge", "MaxAge"])


    books = books.copy()
    books["Language"] = books["Language"].fillna("").astype(str)
    books["Genre"] = books["Genre"].fillna("").astype(str)


    recommendations = books[
        (books["Language"].str.lower() == language.lower())
        & (books["Genre"].str.lower() == genre.lower())
        & (books["MinAge"] <= age)
        & (books["MaxAge"] >= age)
    ]


    return recommendations.head(1)




def save_history(name, age, language, genre):
    """
    Saves search history.
    """
    create_history_file()
    new_entry = pd.DataFrame({
        "Name": [name],
        "Age": [age],
        "Language": [language],
        "Genre": [genre],
    })


    new_entry.to_csv(HISTORY_FILE, mode="a", header=False, index=False)




def view_history():
    """
    Displays user search history.
    """
    print("\n--- Search History ---")


    try:
        history = pd.read_csv(HISTORY_FILE)


        if history.empty:
            print("No history available.")
        else:
            print(history)


    except FileNotFoundError:
        print("History file not found.")




def show_statistics():
    """
    Displays simple statistics using Pandas.
    """
    print("\n--- Statistics ---")


    try:
        history = pd.read_csv(HISTORY_FILE)


        if history.empty:
            print("No data available.")
            return


        print(f"Total searches: {len(history)}")


        most_common_genre = history["Genre"].mode()[0]
        print(f"Most popular genre: {most_common_genre}")


    except FileNotFoundError:
        print("History file not found.")




def recommendation_menu():
    """
    Handles the recommendation process.
    """
    books = load_books()


    if books is None:
        return


    name, age, language, genre = get_user_preferences()
    recommendations = recommend_books(books, age, language, genre).head(1)


    print("\n--- Recommended Books ---")


    if recommendations.empty:
        print("No matching books found.")
    else:
        row = recommendations.iloc[0]
        print(f"- {row['Title']} ({row['Genre']}, {row['Language']})")


    save_history(name, age, language, genre)




def main():
    """
    Main program loop.
    """
    create_history_file()
    create_books_file()


    while True:
        print("\n====================")
        print(" BOOKMATCH")
        print("====================")
        print("1. Get Book Recommendation")
        print("2. View Search History")
        print("3. View Statistics")
        print("4. Exit")


        choice = input("Choose an option: ")


        if choice == "1":
            recommendation_menu()
        elif choice == "2":
            view_history()
        elif choice == "3":
            show_statistics()
        elif choice == "4":
            print("Thank you for using BookMatch!")
            break
        else:
            print("Invalid option. Try again.")




if __name__ == "__main__":
    main()
