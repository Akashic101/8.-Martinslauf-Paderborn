const axios = require("axios");
const Database = require("better-sqlite3");

// Step 1: Initialize SQLite database
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

// Step 2: Prepare an insert statement
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

// Step 3: Prepare to handle requests and insert data into the database
const fetchData = async (offset = 0) => {
  const url =
    "https://www.davengo.com/event/result/8-paderborner-martinslauf-2024/search/list";
  const headers = {
    "User-Agent":
      "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
    Accept: "application/json, text/plain, */*",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "Content-Type": "application/json;charset=utf-8",
    Origin: "https://www.davengo.com",
    Referer:
      "https://www.davengo.com/event/result/8-paderborner-martinslauf-2024/search?category=10km%20Autohaus%20Krenz%20Lauf",
    DNT: "1",
    "Sec-GPC": "1",
    Connection: "keep-alive",
  };

  const data = {
    type: "simple",
    term: null,
    category: "10km Autohaus Krenz Lauf",
    offset: offset,
  };

  try {
    const response = await axios.post(url, data, { headers });
    const { results, navigation } = response.data;

    // Step 4: Insert the results into the SQLite database
    const insertMany = db.transaction((data) => {
      for (const row of data) {
        insert.run(row);
      }
    });
    insertMany(results);

    console.log(
      `Inserted ${results.length} results. Moving to the next page...`
    );

    // Check if there's a nextOffset to continue fetching more data
    if (navigation && navigation.nextOffset) {
      await fetchData(navigation.nextOffset);
    } else {
      console.log(
        "All data has been successfully inserted into the SQLite database."
      );
    }
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

// Step 5: Start the data fetching process
fetchData();
