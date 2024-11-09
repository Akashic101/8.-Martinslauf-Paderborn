# 8. Martinslauf Paderborn

This repository contains an analysis of the results from the **8. Martinslauf Paderborn**, focusing specifically on the **10km-run** in which I participated. The data is sourced from the official results page of the event and parsed into a SQLite database for easy querying and analysis.

The data for the event is retrieved directly from [Davengo's official results](https://www.davengo.com/event/result/8-paderborner-martinslauf-2024/) and is stored in a SQLite database using the `better-sqlite3` library.

## How to Create the Database

While the SQLite database is already shipped in this repo you can manually create it yourself. For that, delete `results.db` and follow these steps:

### Prerequisites

Before running the script, ensure that you have the following software installed:

1. **Node.js**: You need Node.js installed on your machine. You can download it from [here](https://nodejs.org/).
2. **npm**: npm is the Node.js package manager and should be installed automatically when you install Node.js.

### Step 1: Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/akashic101/8-martinslauf-paderborn.git
cd 8-martinslauf-paderborn
```

### Step 2: Install Dependencies

The script relies on `axios` for making HTTP requests and `better-sqlite3` for interacting with the SQLite database. Install these dependencies using npm:

```bash
npm install
```

### Step 3: Run the Script

To create the SQLite database and insert the results, simply run the following command:

```bash
node resultParser.js
```

This will execute the script (`resultParser.js`), which performs the following steps:

1. **Fetch Data**: It makes HTTP requests to the official results page, retrieving paginated results for the 10km-run category.
2. **Parse and Insert Data**: The script parses the fetched data and inserts it into a SQLite database (`results.db`).
3. **Handle Pagination**: The script automatically handles pagination, fetching data in batches of 125 records per request, until all results are retrieved.

**Note**: You will most likely not be able to use this script to fetch the data from other results hosted on Davengo as the data is different for each event.

### Step 4: Verify the Database

Once the script has finished running, you can open the `results.db` SQLite database and query the data. For example, you can use an SQLite viewer like [DB Browser for SQLite](https://sqlitebrowser.org/) or query it directly from the command line:

```bash
sqlite3 results.db
```

Inside the SQLite shell, you can run SQL queries like:

```sql
SELECT * FROM results LIMIT 10;
```

This will display the first 10 entries from the results table.

### Data Source

The data is sourced directly from the official results page of the 8. Martinslauf in Paderborn, specifically for the **10km-run** category. The script makes POST requests to the Davengo results API, which returns the results in JSON format. This data includes information such as:

- **Team Name**
- **First Name**
- **Last Name**
- **Age Group**
- **Rank (Overall, Male, Female, Age Group)**
- **Start Number**
- **Netto Time**
- **Hash (for identifying participants uniquely)**

The results are paginated, and the script handles multiple requests to fetch all available results.

### Script Details

The main script is `resultParser.js`, which:

- **Makes POST requests** to the Davengo API with parameters like `category` (10km-run), `offset` (for pagination), and `term` (for search filtering).
- **Parses the returned JSON** data to extract relevant fields.
- **Inserts the parsed data into a SQLite database** (`results.db`), creating a table (`results`) if it doesn't already exist.

## How to Set Up the Python Environment

### Prerequisites

Before you begin, ensure you have the following installed:

1. **Python** (3.x): Python is required to run the script. You can download it from [here](https://www.python.org/downloads/).
2. **pip**: This is the Python package manager, which is automatically installed with Python.

You can verify that you have Python and pip installed by running:

```bash
python --version
pip --version
```

If Python or pip is not installed, please follow the instructions on the official Python website to install them.

### Step 1: Create a Virtual Environment

A **virtual environment** (venv) is a self-contained directory that contains the Python installation for a particular version of Python, along with any additional packages that you install. This allows you to manage dependencies for different projects separately.

To create a virtual environment:

1. **On Windows**:

   ```bash
   python -m venv venv
   ```

2. **On macOS/Linux**:
   ```bash
   python3 -m venv venv
   ```

This will create a folder named `venv` containing the virtual environment.

### Step 2: Activate the Virtual Environment

Now, activate the virtual environment to ensure that any dependencies installed will only affect this project and not other Python projects on your system.

1. **On Windows**:

   ```bash
   .\venv\Scripts\activate
   ```

2. **On macOS/Linux**:
   ```bash
   source venv/bin/activate
   ```

When the virtual environment is activated, your command prompt will change, indicating that you’re now working inside the venv.

### Step 3: Install Dependencies

With the virtual environment active, install the necessary dependencies listed in the `requirements.txt` file by running:

```bash
pip install -r requirements.txt
```

This will install the required packages, such as `matplotlib` and `pandas`, which are used in the script.

### Step 4: Run the Script to Generate the Image

Once the dependencies are installed, you can run the Python scripts to generate the images.

```bash
python boxPlot.py
python circularBar.py
python divergingPlot.py
```

### Step 5: Verify the Output

After the script finishes running, you should find the output in image-form in the `results` folder.

### Step 6: Deactivate the Virtual Environment (Optional)

When you're done, you can deactivate the virtual environment by running:

```bash
deactivate
```

This will return you to your system’s default Python environment.
