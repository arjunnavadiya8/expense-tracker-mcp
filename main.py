import datetime
from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

mcp = FastMCP(name="Expense Tracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date DATE NOT NULL DEFAULT CURRENT_DATE
            )
        ''')

init_db()

@mcp.tool()
def add_expense(amount: float, category: str, description: str = None, date: str = None):
    """Add a new expense to the tracker.

    Args:
        amount: The amount of the expense.
        category: The category of the expense (e.g., Food, Transport, Utilities).
        description: Optional description of the expense.
        date: Optional date of the expense in YYYY-MM-DD format. Defaults to current date.
    """
    if date is None:
        date = datetime.date.today().strftime('%Y-%m-%d')

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (amount, category, description, date)
            VALUES (?, ?, ?, ?)
        ''', (amount, category, description, date))
        conn.commit()
    
    return f"Expense of {amount} added to {category} on {date}"

@mcp.tool()
def get_expenses(category: str = None, month: int = None, year: int = None):
    """Get a list of expenses.

    Args:
        category: Optional category to filter by.
        month: Optional month (1-12).
        year: Optional year.

    Returns:
        A list of expenses matching the criteria.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        query = "SELECT * FROM expenses WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if month and year:
            query += " AND strftime('%m', date) = ? AND strftime('%Y', date) = ?"
            params.extend([f'{month:02d}', str(year)])
        elif year:
            query += " AND strftime('%Y', date) = ?"
            params.append(str(year))
        
        query += " ORDER BY date DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        columns = [description[0] for description in cursor.description]
        expenses = [dict(zip(columns, row)) for row in rows]
        
        return expenses

@mcp.tool()
def get_summary(month: int, year: int):
    """Get a summary of expenses by category for a specific month.

    Args:
        month: The month (1-12).
        year: The year.

    Returns:
        A dictionary with categories as keys and total amounts as values.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, SUM(amount) as total
            FROM expenses
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
            GROUP BY category
        ''', (f'{month:02d}', str(year)))
        rows = cursor.fetchall()
        
        return {row[0]: row[1] for row in rows}

@mcp.tool()
def delete_expense(expense_id: int):
    """Delete an expense by its ID.

    Args:
        expense_id: The ID of the expense to delete.

    Returns:
        A confirmation message.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return f"No expense found with ID {expense_id}"
        
        return f"Expense with ID {expense_id} deleted successfully"




if __name__ == "__main__":
    mcp.run()
