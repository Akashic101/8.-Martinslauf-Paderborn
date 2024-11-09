const axios = require("axios");
const Database = require("better-sqlite3");

const db = new Database("results.db");

db.exec(`
  CREATE TABLE IF NOT EXISTS results_2024 (
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

db.exec(`
  CREATE TABLE IF NOT EXISTS results_2023 (
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

const insert2024 = db.prepare(`
  INSERT INTO results_2024 (
    teamName, firstName, lastName, ageGroupShort, nettoTime, 
    rankMale, startNo, combined, rankTotal, rankFemale, 
    hash, rankAgeGroup
  ) VALUES (
    @teamName, @firstName, @lastName, @ageGroupShort, @nettoTime, 
    @rankMale, @startNo, @combined, @rankTotal, @rankFemale, 
    @hash, @rankAgeGroup
  );
`);

const insert2023 = db.prepare(`
  INSERT INTO results_2023 (
    teamName, firstName, lastName, ageGroupShort, nettoTime, 
    rankMale, startNo, combined, rankTotal, rankFemale, 
    hash, rankAgeGroup
  ) VALUES (
    @teamName, @firstName, @lastName, @ageGroupShort, @nettoTime, 
    @rankMale, @startNo, @combined, @rankTotal, @rankFemale, 
    @hash, @rankAgeGroup
  );
`);

const fetchData = async (url, insertStatement, offset = 0) => {
  const headers = {
    "User-Agent":
      "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
    Accept: "application/json, text/plain, */*",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "Content-Type": "application/json;charset=utf-8",
    Origin: "https://www.davengo.com",
    Referer: url,
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

    const insertMany = db.transaction((data) => {
      for (const row of data) {
        insertStatement.run(row);
      }
    });
    insertMany(results);

    console.log(
      `Inserted ${results.length} results for ${url}. Moving to the next page...`
    );

    if (navigation && navigation.nextOffset) {
      await fetchData(url, insertStatement, navigation.nextOffset);
    } else {
      console.log(`All data for ${url} has been successfully inserted.`);
    }
  } catch (error) {
    console.error(`Error fetching data from ${url}:`, error);
  }
};

(async () => {
  const url2024 =
    "https://www.davengo.com/event/result/8-paderborner-martinslauf-2024/search/list";
  const url2023 =
    "https://www.davengo.com/event/result/7-paderborner-martinslauf-2023/search/list";

  console.log("Fetching results for 2024...");
  await fetchData(url2024, insert2024);

  console.log("Fetching results for 2023...");
  await fetchData(url2023, insert2023);
})();
