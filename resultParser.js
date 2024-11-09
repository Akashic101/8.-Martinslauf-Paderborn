const fs = require("fs");
const Database = require("better-sqlite3");

// Step 1: Load and parse the JSON data
const jsonData = JSON.parse(fs.readFileSync("results.json", "utf-8"));
const results = jsonData.results;

// Step 2: Initialize SQLite database
const db = new Database("results.db");
db.exec(`
  CREATE TABLE IF NOT EXISTS results (
    teamName TEXT,
    firstName TEXT,
    lastName TEXT,
    ageGroupShort TEXT,
    nettoTime TEXT,
    rankMale TEXT,
    startNo INTEGER,
    combined TEXT,
    rankTotal TEXT,
    rankFemale TEXT,
    hash TEXT,
    rankAgeGroup TEXT
  );
`);

// Step 3: Prepare an insert statement
const insert = db.prepare(`
  INSERT INTO results (
    teamName, firstName, lastName, ageGroupShort, nettoTime, 
    rankMale, startNo, combined, rankTotal, rankFemale, 
    hash, rankAgeGroup
  ) VALUES (
    @teamName, @firstName, @lastName, @ageGroupShort, @nettoTime, 
    @rankMale, @startNo, @combined, @rankTotal, @rankFemale, 
    @hash, @rankAgeGroup
  );
`);

// Step 4: Insert data into the SQLite table
const insertMany = db.transaction((data) => {
  for (const row of data) {
    insert.run(row);
  }
});

insertMany(results);

console.log("Data has been successfully inserted into the SQLite database.");
