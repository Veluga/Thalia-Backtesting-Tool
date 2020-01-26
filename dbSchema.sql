CREATE TABLE AssetClass (
    AssetClassName TEXT PRIMARY KEY
);

CREATE TABLE Asset (
    AssetTicker TEXT PRIMARY KEY,
    Name TEXT,
    AssetClassName TEXT
);

CREATE TABLE AssetValue (
    ID INTEGER PRIMARY KEY,
    AssetTicker TEXT,
    ADate TEXT,
    Price TEXT,
    IsInterpolated INTEGER
);

CREATE INDEX IX_Asset_AssetClass ON Asset(AssetClassName);
CREATE INDEX UX_Values_AssetTicker ON AssetValue(AssetTicker);
CREATE INDEX IX_Values_IsInterpolated ON AssetValue(IsInterpolated);


