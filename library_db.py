import sqlite3

def create_database():
    # Connect to SQLite database (creates library.db if it doesn't exist)
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Create the books table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            available_copies INTEGER NOT NULL,
            times_borrowed INTEGER NOT NULL
        )
    ''')

    # Clear existing records if re-running the script
    cursor.execute('DELETE FROM books')

    # 100 Synthetic books across 4 categories (Science, Technology, Literature, History)
    sample_books = [
        # --- SCIENCE (25 books) ---
        ("A Brief History of Time", "Stephen Hawking", "Science", 3, 42),
        ("Cosmos", "Carl Sagan", "Science", 2, 38),
        ("The Selfish Gene", "Richard Dawkins", "Science", 4, 25),
        ("Silent Spring", "Rachel Carson", "Science", 1, 19),
        ("The Elegant Universe", "Brian Greene", "Science", 5, 14),
        ("Astrophysics for People in a Hurry", "Neil deGrasse Tyson", "Science", 6, 50),
        ("The Gene: An Intimate History", "Siddhartha Mukherjee", "Science", 2, 21),
        ("A Short History of Nearly Everything", "Bill Bryson", "Science", 4, 65),
        ("The Double Helix", "James D. Watson", "Science", 0, 30),
        ("The Structure of Scientific Revolutions", "Thomas S. Kuhn", "Science", 3, 12),
        ("The Emperor of All Maladies", "Siddhartha Mukherjee", "Science", 3, 27),
        ("What Is Life?", "Erwin Schrodinger", "Science", 1, 15),
        ("Pale Blue Dot", "Carl Sagan", "Science", 4, 45),
        ("The Man Who Mistook His Wife for a Hat", "Oliver Sacks", "Science", 2, 53),
        ("Awakenings", "Oliver Sacks", "Science", 3, 22),
        ("Chaos: Making a New Science", "James Gleick", "Science", 2, 18),
        ("The Demon-Haunted World", "Carl Sagan", "Science", 5, 41),
        ("The Grand Design", "Stephen Hawking", "Science", 0, 36),
        ("Packing for Mars", "Mary Roach", "Science", 4, 29),
        ("Stiff: The Curious Lives of Human Cadavers", "Mary Roach", "Science", 3, 44),
        ("Your Inner Fish", "Neil Shubin", "Science", 2, 17),
        ("The Origin of Species", "Charles Darwin", "Science", 1, 58),
        ("Six Easy Pieces", "Richard P. Feynman", "Science", 5, 33),
        ("Feynman Lectures on Physics", "Richard P. Feynman", "Science", 2, 49),
        ("The Fabric of the Cosmos", "Brian Greene", "Science", 3, 26),

        # --- TECHNOLOGY (25 books) ---
        ("Clean Code", "Robert C. Martin", "Technology", 4, 60),
        ("The Pragmatic Programmer", "Andrew Hunt", "Technology", 3, 55),
        ("Introduction to Algorithms", "Thomas H. Cormen", "Technology", 2, 40),
        ("Design Patterns", "Erich Gamma", "Technology", 1, 33),
        ("Python Crash Course", "Eric Matthes", "Technology", 7, 75),
        ("Artificial Intelligence: A Modern Approach", "Stuart Russell", "Technology", 2, 48),
        ("Refactoring", "Martin Fowler", "Technology", 3, 29),
        ("The Mythical Man-Month", "Frederick P. Brooks Jr.", "Technology", 5, 18),
        ("Code: The Hidden Language", "Charles Petzold", "Technology", 4, 51),
        ("Structure and Interpretation of Computer Programs", "Harold Abelson", "Technology", 1, 20),
        ("Effective Java", "Joshua Bloch", "Technology", 3, 62),
        ("You Don't Know JS", "Kyle Simpson", "Technology", 6, 70),
        ("Cracking the Coding Interview", "Gayle Laakmann McDowell", "Technology", 0, 95),
        ("Clean Architecture", "Robert C. Martin", "Technology", 2, 43),
        ("Domain-Driven Design", "Eric Evans", "Technology", 1, 24),
        ("Database System Concepts", "Abraham Silberschatz", "Technology", 2, 31),
        ("Operating System Concepts", "Abraham Silberschatz", "Technology", 3, 35),
        ("Computer Networks", "Andrew S. Tanenbaum", "Technology", 2, 28),
        ("Head First Design Patterns", "Eric Freeman", "Technology", 4, 52),
        ("Fluent Python", "Luciano Ramalho", "Technology", 3, 38),
        ("Programming Pearls", "Jon Bentley", "Technology", 1, 16),
        ("The Art of Computer Programming", "Donald Knuth", "Technology", 0, 22),
        ("Site Reliability Engineering", "Betsy Beyer", "Technology", 3, 27),
        ("Designing Data-Intensive Applications", "Martin Kleppmann", "Technology", 5, 84),
        ("Algorithms to Live By", "Brian Christian", "Technology", 4, 46),

        # --- LITERATURE (25 books) ---
        ("To Kill a Mockingbird", "Harper Lee", "Literature", 0, 45),
        ("1984", "George Orwell", "Literature", 0, 62),
        ("Pride and Prejudice", "Jane Austen", "Literature", 4, 31),
        ("The Great Gatsby", "F. Scott Fitzgerald", "Literature", 2, 36),
        ("Moby-Dick", "Herman Melville", "Literature", 1, 12),
        ("The Catcher in the Rye", "J.D. Salinger", "Literature", 3, 28),
        ("Jane Eyre", "Charlotte Bronte", "Literature", 2, 22),
        ("Lord of the Flies", "William Golding", "Literature", 0, 39),
        ("Animal Farm", "George Orwell", "Literature", 5, 74),
        ("Brave New World", "Aldous Huxley", "Literature", 3, 50),
        ("The Hobbit", "J.R.R. Tolkien", "Literature", 0, 88),
        ("The Fellowship of the Ring", "J.R.R. Tolkien", "Literature", 2, 79),
        ("Fahrenheit 451", "Ray Bradbury", "Literature", 4, 47),
        ("Crime and Punishment", "Fyodor Dostoevsky", "Literature", 1, 21),
        ("War and Peace", "Leo Tolstoy", "Literature", 1, 10),
        ("The Odyssey", "Homer", "Literature", 3, 19),
        ("The Iliad", "Homer", "Literature", 2, 15),
        ("Wuthering Heights", "Emily Bronte", "Literature", 3, 25),
        ("Great Expectations", "Charles Dickens", "Literature", 2, 30),
        ("A Tale of Two Cities", "Charles Dickens", "Literature", 4, 34),
        ("Frankenstein", "Mary Shelley", "Literature", 5, 56),
        ("Dracula", "Bram Stoker", "Literature", 3, 44),
        ("The Alchemist", "Paulo Coelho", "Literature", 6, 92),
        ("The Picture of Dorian Gray", "Oscar Wilde", "Literature", 2, 37),
        ("Les Miserables", "Victor Hugo", "Literature", 1, 18),

        # --- HISTORY (25 books) ---
        ("Sapiens: A Brief History of Humankind", "Yuval Noah Harari", "History", 5, 80),
        ("Guns, Germs, and Steel", "Jared Diamond", "History", 3, 34),
        ("A People's History of the United States", "Howard Zinn", "History", 2, 27),
        ("The Silk Roads", "Peter Frankopan", "History", 4, 41),
        ("The Wright Brothers", "David McCullough", "History", 1, 23),
        ("Team of Rivals", "Doris Kearns Goodwin", "History", 2, 16),
        ("1776", "David McCullough", "History", 3, 30),
        ("Homo Deus", "Yuval Noah Harari", "History", 4, 55),
        ("21 Lessons for the 21st Century", "Yuval Noah Harari", "History", 3, 48),
        ("The Histories", "Herodotus", "History", 1, 11),
        ("The Rise and Fall of the Third Reich", "William L. Shirer", "History", 2, 25),
        ("The Diary of a Young Girl", "Anne Frank", "History", 0, 70),
        ("A History of Western Philosophy", "Bertrand Russell", "History", 2, 19),
        ("The Crusades Through Arab Eyes", "Amin Maalouf", "History", 3, 21),
        ("Stalingrad", "Antony Beevor", "History", 1, 29),
        ("The Romanovs", "Simon Sebag Montefiore", "History", 2, 24),
        ("The Waning Middle Ages", "Johan Huizinga", "History", 1, 9),
        ("Meditation", "Marcus Aurelius", "History", 6, 68),
        ("The Peloponnesian War", "Thucydides", "History", 2, 14),
        ("Patton: A Genius for War", "Carlo D'Este", "History", 3, 20),
        ("Alexander the Great", "Philip Freeman", "History", 4, 32),
        ("Cleopatra", "Stacy Schiff", "History", 3, 26),
        ("Genghis Khan and the Making of the Modern World", "Jack Weatherford", "History", 5, 61),
        ("The Wright Brothers", "David McCullough", "History", 2, 18),
        ("Citizens: A Chronicle of the French Revolution", "Simon Schama", "History", 1, 13)
    ]

    # Insert records into the table
    cursor.executemany('''
        INSERT INTO books (title, author, category, available_copies, times_borrowed)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_books)

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database 'library.db' recreated successfully with 100 books across 4 categories!")

if __name__ == "__main__":
    create_database()