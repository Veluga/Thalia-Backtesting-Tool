CREATE TABLE AssetClass (
    ID INTEGER PRIMARY KEY,
    Name TEXT
);

CREATE TABLE Asset (
  ID INTEGER PRIMARY KEY,
  Name TEXT,
  AssetTicker TEXT UNIQUE,
  AssetClass TEXT
);

CREATE TABLE AssetValues (
    ID INTEGER PRIMARY KEY,
    AssetTicker TEXT,
    ADate TEXT,
    Price TEXT,
    IsInterpolated INTEGER
);

CREATE INDEX IX_Asset_AssetClass ON Asset(AssetClass);
CREATE INDEX UX_Values_AssetTicker ON AssetValues(AssetTicker);
CREATE INDEX IX_Values_IsInterpolated ON AssetValues(IsInterpolated);


