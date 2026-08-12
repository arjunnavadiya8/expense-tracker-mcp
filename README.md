# Expense Tracker MCP Server

A Model Context Protocol (MCP) server built with Python and **FastMCP** that allows LLM assistants (like Claude Desktop) to track, query, summarize, and delete personal expenses using a local **SQLite** database.

---

## 📌 Project Summary

This project provides an intelligent financial tracker backend accessible via MCP tools. With this MCP server, an AI assistant can manage your personal expenses directly through conversational prompts.

### Available Resources:
- **`config://categories`**: Provides a predefined JSON mapping of categories and sub-categories for both income and expenses.

### Available Tools:
- **`add_expense`**: Add a new expense with amount, category, optional description, and optional date.
- **`get_expenses`**: List and filter expenses by category, month, or year.
- **`delete_expense`**: Remove an expense record by its unique ID.
- **`add_income`**: Add a new income record (e.g., Salary, Investments).
- **`get_incomes`**: List and filter income records.
- **`delete_income`**: Remove an income record by its unique ID.
- **`get_summary`**: Generate a monthly summary grouped by spending and income categories.

---

## 🚀 Step-by-Step Setup & Implementation Guide

### Prerequisites
- [Python 3.10+](https://www.python.org/)
- [`uv`](https://github.com/astral-sh/uv) (Fast Python package installer and runner)
- [Claude Desktop](https://claude.ai/download) (or any MCP-compliant client)

---

### Step 1: Set Up the Project

Navigate to the project root directory:
```powershell
cd C:\Users\arjun\Desktop\papi\expense-tracker-mcp
```

Install the required dependencies using `uv`:
```powershell
uv pip install fastmcp
```

---

### Step 2: Project Architecture (`main.py`)

The application defines an MCP server using `FastMCP` and initializes an SQLite database (`expenses.db`) automatically upon execution:

```python
import datetime
from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
mcp = FastMCP(name="Expense Tracker")

# Database Initialization
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
```

---

### Step 3: Test Running the MCP Server

You can run the server locally to ensure there are no syntax errors:
```powershell
uv run python main.py
```

---

### Step 4: Integrate with Claude Desktop

#### Option A: Automatic Installation (Standard Claude Desktop)
If using standard Claude Desktop:
```powershell
uv run fastmcp install claude-desktop main.py
```

#### Option B: Manual Configuration (Windows Store Claude Desktop)
If using the Microsoft Store version of Claude Desktop, open your `claude_desktop_config.json`:
- **Path**: `%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json`

Add the server entry under `mcpServers`:
```json
{
  "mcpServers": {
    "expense-tracker": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "C:\\Users\\arjun\\Desktop\\papi\\expense-tracker-mcp\\main.py"
      ]
    }
  }
}
```

---

### Step 5: Restart Claude Desktop

1. Close and fully quit Claude Desktop.
2. Relaunch Claude Desktop.
3. Look for the 🔌 icon to verify that the **Expense Tracker** tools are active.

---

## 💬 Example Conversational Prompts

Once configured in Claude Desktop, you can interact with your tracker using natural prompts:

- *"Add an expense of $15.50 for lunch under Food category today."*
- *"Show all my Food expenses for this month."*
- *"Give me a spending summary for August 2026."*
- *"Delete expense ID 3."*